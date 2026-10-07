#!/usr/bin/env python3
"""Render the two marked README indexes from concepts.json and concept notes."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def slug(text):
    text = text.lower().replace('`', '')
    return re.sub(r'[^\w\s-]', '', text).replace(' ', '-')


def render(root=ROOT):
    items = json.loads((root / 'concepts.json').read_text())
    toc, body = [], []
    group = None
    for item in items:
        if item['group'] != group:
            group = item['group']
            toc.extend([f"### {group}", ''])
            body.extend([f"# {group}", ''])
        heading = f"{item['id']}. {item['title']}"
        toc.append(f"{item['id']}. [{item['title']}](#{slug(heading)})")
        note = (root / item['path']).read_text()
        resources = note.split('## Learn more\n', 1)[1].split('Resource review:', 1)[0].strip()
        body.extend([f'## {heading}', '', item['summary'], '',
                     f"[Explanation, exercise, and pitfalls]({item['path']})", '',
                     '### Resources', '', resources, '', '[⬆ Back to top](#table-of-contents)', ''])
    original = (root / 'README.md').read_text()
    output = original
    for label, lines in [('TOC', toc), ('CONCEPTS', body)]:
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
