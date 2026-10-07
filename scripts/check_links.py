#!/usr/bin/env python3
"""Check local Markdown links/anchors; optionally check public HTTP links.

A deliberately small parser for this repo's inline Markdown links, not a general
CommonMark implementation. Code fences are ignored. External fragments are not
checked. HTTP success alone cannot establish editorial quality or API accuracy.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urldefrag, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HOSTS = frozenset({
    'arxiv.org', 'aws.amazon.com', 'cheatsheetseries.owasp.org',
    'developers.openai.com', 'docs.aws.amazon.com', 'docs.github.com',
    'docs.langchain.com', 'docs.ollama.com', 'docs.python.org',
    'docs.temporal.io', 'github.com', 'huggingface.co', 'json-schema.org',
    'learn.microsoft.com', 'modelcontextprotocol.io', 'opentelemetry.io',
    'platform.claude.com', 'sbert.net', 'www.anthropic.com',
})


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


# Redirects are reported for review, never followed to an unreviewed destination.
urlopen = build_opener(NoRedirect()).open


def prose(text):
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)


def anchors(text):
    result = set()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', prose(text), re.M):
        base = re.sub(r'[^\w\s-]', '', title.lower().replace('`', '')).replace(' ', '-')
        candidate, n = base, 0
        while candidate in result:
            n += 1
            candidate = f'{base}-{n}'
        result.add(candidate)
    return result


def links(text):
    return re.findall(r'\[[^\]\n]+\]\(([^\s)]+)\)', prose(text))


def scan(root=ROOT):
    errors, external = [], set()
    local_count = 0
    root = root.resolve()
    for source in sorted(root.rglob('*.md')):
        if any(p in {'.git', 'node_modules'} or p.startswith('.venv') for p in source.relative_to(root).parts):
            continue
        for href in links(source.read_text()):
            parsed = urlsplit(href)
            if parsed.scheme in {'http', 'https'}:
                external.add(urldefrag(href)[0])
                continue
            if parsed.scheme or parsed.netloc:
                errors.append(f'{source.relative_to(root)}: unsupported link {href}')
                continue
            local_count += 1
            target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            if not target.is_relative_to(root):
                errors.append(f'{source.relative_to(root)}: link escapes repository: {href}')
            elif not target.exists():
                errors.append(f'{source.relative_to(root)}: missing {href}')
            elif parsed.fragment and target.suffix == '.md' and unquote(parsed.fragment) not in anchors(target.read_text()):
                errors.append(f'{source.relative_to(root)}: missing anchor {href}')
    return errors, sorted(external), local_count


def check_external(url, timeout=10):
    """Reviewed HTTPS hosts only, no redirects, credentials, or cookies.

    A host allowlist is not a network sandbox. Run in a trusted environment with
    appropriate DNS and egress controls; do not run arbitrary PR code with secrets.
    """
    parsed = urlsplit(url)
    try:
        allowed = (parsed.scheme == 'https' and parsed.hostname in REVIEWED_HOSTS
                   and parsed.port in {None, 443} and not parsed.username
                   and not parsed.password)
    except ValueError:
        allowed = False
    if not allowed:
        return {'url': url, 'status': 'review', 'detail': 'URL is outside the reviewed HTTPS host allowlist'}
    for method in ('HEAD', 'GET'):
        try:
            request = Request(url, method=method, headers={'User-Agent': 'ai-engineering-concepts-link-check/1.0'})
            with urlopen(request, timeout=timeout) as response:
                code = response.status
                return {'url': url, 'status': 'ok' if 200 <= code < 400 else 'broken', 'detail': str(code), 'final_url': response.url}
        except HTTPError as exc:
            if method == 'HEAD' and exc.code in {403, 405, 501}:
                continue
            needs_review = 300 <= exc.code < 400 or exc.code in {401, 403, 429}
            return {'url': url, 'status': 'review' if needs_review else 'broken', 'detail': str(exc.code)}
        except (URLError, TimeoutError, OSError) as exc:
            return {'url': url, 'status': 'review', 'detail': type(exc).__name__}
    return {'url': url, 'status': 'review', 'detail': 'unresolved'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--external', action='store_true', help='Opt in to public HTTP requests')
    parser.add_argument('--json', action='store_true', help='Print a machine-readable report')
    args = parser.parse_args()
    errors, urls, local_count = scan()
    checks = []
    if args.external:
        with ThreadPoolExecutor(max_workers=4) as executor:
            checks = list(executor.map(check_external, urls))
    report = {'local_links': local_count, 'local_errors': errors, 'external_urls': len(urls),
              'external_checked': args.external, 'external_results': checks}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f'{local_count} local links; {len(errors)} errors; {len(urls)} unique external URLs.')
        for error in errors:
            print(error)
        if not args.external:
            print('External HTTP checks not run; use --external when network access is available.')
        for check in checks:
            if check['status'] != 'ok':
                print(f"{check['status']}: {check['url']} ({check['detail']})")
    return 1 if errors or any(x['status'] != 'ok' for x in checks) else 0


if __name__ == '__main__':
    raise SystemExit(main())
