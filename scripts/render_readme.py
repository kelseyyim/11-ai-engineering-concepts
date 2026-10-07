#!/usr/bin/env python3
"""Render resource-first README indexes from core topics and concept notes."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def slug(text):
    text = text.lower().replace('`', '')
    return re.sub(r'[^\w\s-]', '', text).replace(' ', '-')


def resource_lines(note):
    """Keep the reviewed resource label and description in the chapter source."""
    section = note.split('## Learn more\n', 1)[1].split('Resource review:', 1)[0]
    return {match.group(1): line for line in section.splitlines()
            if (match := re.search(r'^- \[[^\]]+\]\((https://[^)]+)\)', line))}


def render(root=ROOT):
    items = json.loads((root / 'concepts.json').read_text())
    topics = json.loads((root / 'core-topics.json').read_text())
    by_id = {item['id']: item for item in items}
    toc, body, used = [], [], set()
    for topic in topics:
        title = topic['title']
        toc.append(f'- [{title}](#{slug(title)})')
        chapters = [by_id[number] for number in topic['chapters']]
        available = {}
        for chapter in chapters:
            for url, line in resource_lines((root / chapter['path']).read_text()).items():
                available.setdefault(url, line)
        body.extend([f'## {title}', ''])
        for url in topic['resources']:
            if url not in available:
                raise ValueError(f'{title}: resource is absent from its chapter sources: {url}')
            body.append(available[url])
        notes = ' · '.join(f"[{chapter['title']}]({chapter['path']})" for chapter in chapters)
        body.extend(['', f'Notes and exercises: {notes}', '',
                     '[⬆ Back to top](#table-of-contents)', ''])
        used.update(topic['chapters'])
    more = [f"- [{item['title']}]({item['path']})" for item in items if item['id'] not in used]
    if not more:
        more = ['More detailed notes and exercises are linked under each topic above.']
    original = (root / 'README.md').read_text()
    output = original
    for label, lines in [('TOC', toc), ('CONCEPTS', body), ('MORE', more)]:
        start, end = f'<!-- BEGIN {label} -->', f'<!-- END {label} -->'
        if output.count(start) != 1 or output.count(end) != 1:
            raise ValueError(f'Expected one {label} marker pair')
        before, rest = output.split(start)
        _, after = rest.split(end)
        output = before + start + '\n\n' + '\n'.join(lines).strip() + '\n\n' + end + after
    return original, output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    before, after = render()
    if args.check:
        if before != after:
            print('README indexes are stale. Run python3 scripts/render_readme.py')
            return 1
        print('README indexes are current.')
        return 0
    (ROOT / 'README.md').write_text(after)
    print('README indexes rendered.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
