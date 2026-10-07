#!/usr/bin/env python3
"""Validate curriculum invariants, chapter structure, and generated indexes."""
import datetime
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_readme import render, slug


def validate(root=ROOT):
    errors = []
    items = json.loads((root / 'concepts.json').read_text())
    ids = [x['id'] for x in items]
    if (not ids or any(type(number) is not int or number < 1 for number in ids)
            or len(set(ids)) != len(ids)):
        errors.append('Catalog IDs must be unique positive integers; there is no fixed count.')
    if len({x['slug'] for x in items}) != len(items) or len({x['path'] for x in items}) != len(items):
        errors.append('Slugs and paths must be unique.')
    if any(not x['group'].strip() for x in items):
        errors.append('Each chapter needs a nonempty group.')
    topics = json.loads((root / 'core-topics.json').read_text())
    titles = [slug(x['title']) for x in topics]
    if not titles or any(not title for title in titles) or len(set(titles)) != len(titles):
        errors.append('Core topic headings must be nonempty and have unique anchors.')
    for topic in topics:
        chapters, resources = topic['chapters'], topic['resources']
        if not chapters or len(set(chapters)) != len(chapters) or not set(chapters) <= set(ids):
            errors.append(f"{topic['title']}: chapter references must be known, nonempty, and unique.")
        if (not resources or len(set(resources)) != len(resources)
                or any(not url.startswith('https://') for url in resources)):
            errors.append(f"{topic['title']}: resources must be nonempty, unique HTTPS URLs.")
    expected = {x['path'] for x in items}
    actual = {str(p.relative_to(root)) for p in (root / 'concepts').glob('*.md')}
    if expected != actual:
        errors.append('Concept files do not match catalog paths.')
    for item in items:
        path = root / item['path']
        if not path.is_file():
            continue
        text = path.read_text()
        if text.splitlines()[0] != f"# {item['id']}. {item['title']}":
            errors.append(f'{item["path"]}: heading differs from catalog.')
        for section in ['Why it matters', 'Build it', 'Watch out', 'Learn more']:
            if f'## {section}\n' not in text:
                errors.append(f'{item["path"]}: missing section {section}')
        if len(re.findall(r'\]\(https://', text)) < 2:
            errors.append(f'{item["path"]}: needs at least two HTTPS resources.')
        date = re.search(r'Resource review: (\d{4}-\d{2}-\d{2})\.', text)
        if not date:
            errors.append(f'{item["path"]}: missing resource review date.')
        else:
            try:
                datetime.date.fromisoformat(date.group(1))
            except ValueError:
                errors.append(f'{item["path"]}: invalid date.')
        if len(text.split()) < 180:
            errors.append(f'{item["path"]}: chapter is too short to be a useful note.')
    try:
        before, after = render(root)
        if before != after:
            errors.append('README indexes are stale; run scripts/render_readme.py.')
    except (KeyError, ValueError, IndexError, FileNotFoundError) as exc:
        errors.append(f'Could not render README: {exc}')
    return errors


if __name__ == '__main__':
    errors = validate()
    print('\n'.join(errors) if errors else 'Core topics, chapter structure, and README indexes passed.')
    raise SystemExit(bool(errors))
