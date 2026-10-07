#!/usr/bin/env python3
"""Check README resource count, topic anchors, and duplicate URLs (offline)."""
from pathlib import Path
import re
from urllib.parse import urldefrag, urlsplit

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = re.compile(r'^- [📜🎥] \[([^\]]+)\]\((https://[^\s)]+)\)$')
TITLE = re.compile(r'^# (\d+) AI Engineering Resources$')


def slug(text):
    return re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')


def validate(text, root=ROOT):
    errors, resources, headings = [], [], set()
    lines = text.splitlines()
    title = TITLE.fullmatch(lines[0]) if lines else None
    for line in lines:
        if match := re.match(r'^#{1,6} (.+)$', line):
            headings.add(slug(match.group(1)))
        if not line.startswith(('- 📜', '- 🎥')):
            continue
        match = RESOURCE.fullmatch(line)
        if not match:
            errors.append(f'Malformed resource entry: {line}')
        else:
            resources.append(match.group(2))
            if line.startswith('- 🎥') and urlsplit(match.group(2)).hostname != 'www.youtube.com':
                errors.append('Video resources must use a verified YouTube URL.')
    urls = [urldefrag(url)[0] for url in resources]
    if not resources:
        errors.append('The resource list is empty.')
    if not title or int(title.group(1)) != len(set(urls)):
        errors.append('Title must count the unique article and video URLs.')
    if len(urls) != len(set(urls)):
        errors.append('Duplicate learning-resource URL.')
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if link.startswith('#'):
            if link[1:] not in headings:
                errors.append(f'Missing topic anchor: {link}')
        elif urlsplit(link).scheme:
            try:
                parsed = urlsplit(link)
                valid = (parsed.scheme == 'https' and parsed.hostname and not parsed.username
                         and not parsed.password and parsed.port in (None, 443))
            except ValueError:
                valid = False
            if not valid:
                errors.append(f'Invalid public HTTPS URL: {link}')
        else:
            target = (root / urldefrag(link)[0]).resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                errors.append(f'Missing or out-of-repository local link: {link}')
    for section in ('Introduction', 'Community', 'Table of Contents', 'Contributors'):
        if f'## {section}' not in text:
            errors.append(f'Missing section: {section}')
    return errors, len(resources)


if __name__ == '__main__':
    errors, count = validate((ROOT / 'README.md').read_text())
    print('\n'.join(errors) if errors else f'{count} unique resources; title, topic anchors, and links passed.')
    raise SystemExit(bool(errors))
