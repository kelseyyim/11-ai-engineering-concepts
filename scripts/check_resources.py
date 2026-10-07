#!/usr/bin/env python3
"""Check README resource count, numbering, duplicates, and local links (offline)."""
from pathlib import Path
import re
from urllib.parse import urldefrag, urlsplit

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = re.compile(r'^(\d+)\. \[([^\]]+)\]\((https://[^\s)]+)\) — (\S.*)$')
TITLE = re.compile(r'^# (\d+) Essential AI Engineering Resources$')


def validate(text, root=ROOT):
    errors, resources = [], []
    lines = text.splitlines()
    title = TITLE.fullmatch(lines[0]) if lines else None
    for line in lines:
        if not re.match(r'^\d+\. ', line):
            continue
        match = RESOURCE.fullmatch(line)
        if not match:
            errors.append(f'Malformed resource entry: {line}')
        else:
            resources.append(match.groups())
    urls = [urldefrag(entry[2])[0] for entry in resources]
    if not resources:
        errors.append('The resource list is empty.')
    if not title or int(title.group(1)) != len(set(urls)):
        errors.append('Title must count the unique numbered learning-resource URLs.')
    if [int(entry[0]) for entry in resources] != list(range(1, len(resources) + 1)):
        errors.append('Resource numbering must be consecutive.')
    if len(urls) != len(set(urls)):
        errors.append('Duplicate learning-resource URL.')
    for url in urls:
        try:
            parsed = urlsplit(url)
            valid = parsed.hostname and not parsed.username and not parsed.password and parsed.port in (None, 443)
        except ValueError:
            valid = False
        if not valid:
            errors.append(f'Invalid public HTTPS URL: {url}')
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if urlsplit(link).scheme or link.startswith('#'):
            continue
        target = (root / urldefrag(link)[0]).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            errors.append(f'Missing or out-of-repository local link: {link}')
    return errors, len(resources)


if __name__ == '__main__':
    errors, count = validate((ROOT / 'README.md').read_text())
    print('\n'.join(errors) if errors else f'{count} unique resources; title, numbering, and local links passed.')
    raise SystemExit(bool(errors))
