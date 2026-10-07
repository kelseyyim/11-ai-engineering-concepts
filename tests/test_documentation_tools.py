from contextlib import contextmanager
from pathlib import Path
import json
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from scripts.check_links import anchors, check_external, links, scan
from scripts.check_content import validate
from scripts.render_readme import render, slug

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def copied_docs():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        shutil.copytree(ROOT / 'concepts', root / 'concepts')
        for name in ('README.md', 'concepts.json', 'core-topics.json'):
            shutil.copy(ROOT / name, root / name)
        yield root


class LinkTests(unittest.TestCase):
    def test_fences_ignored(self):
        text = '# Title\n```sh\n[example](missing.md)\n```\n[real](ok.md)'
        self.assertEqual(links(text), ['ok.md'])

    def test_anchors_and_duplicates(self):
        self.assertEqual(anchors('# Hi, world!\n## Hi, world!\n### `code` (API)'), {'hi-world', 'hi-world-1', 'code-api'})

    def test_heading_suffix_collision(self):
        self.assertEqual(anchors('# Foo\n# Foo\n# Foo-1'), {'foo', 'foo-1', 'foo-1-1'})

    def test_slug_matches_heading(self):
        value = '21. Model Context Protocol (MCP)'
        self.assertIn(slug(value), anchors('# ' + value))

    def test_local_paths_and_anchors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('# Start\n[good](topic.md#some-topic)\n[bad](topic.md#missing)\n[absent](gone.md)')
            (root / 'topic.md').write_text('# Some topic\n[home](README.md#start)')
            errors, urls, count = scan(root)
            self.assertEqual(count, 4)
            self.assertEqual(len(errors), 2)
            self.assertEqual(urls, [])

    def test_root_escape_and_unsupported_scheme(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('[escape](../private.md)\n[bad](file:///tmp/private)')
            errors, _, _ = scan(root)
            self.assertEqual(len(errors), 2)

    def test_external_urls_are_deduplicated_without_fragments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('[a](https://example.com/docs#one)\n[b](https://example.com/docs#two)')
            errors, urls, _ = scan(root)
            self.assertEqual(errors, [])
            self.assertEqual(urls, ['https://example.com/docs'])

    def test_actual_repo_local_links(self):
        self.assertEqual(scan()[0], [])

    def test_optional_sdk_environment_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '.venv-bedrock').mkdir()
            (root / '.venv-bedrock/vendor.md').write_text('[not our link](missing.md)')
            self.assertEqual(scan(root), ([], [], 0))

    def test_external_success(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.status, response.url = 200, 'https://docs.ollama.com/docs'
        with patch('scripts.check_links.urlopen', return_value=response):
            self.assertEqual(check_external(response.url)['status'], 'ok')

    def test_head_fallback(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.status, response.url = 200, 'https://docs.ollama.com/docs'
        error = HTTPError(response.url, 405, 'no HEAD', None, None)
        with patch('scripts.check_links.urlopen', side_effect=[error, response]) as fetch:
            self.assertEqual(check_external(response.url)['status'], 'ok')
            self.assertEqual(fetch.call_args_list[0].args[0].method, 'HEAD')
            self.assertEqual(fetch.call_args_list[1].args[0].method, 'GET')

    def test_blocked_is_not_healthy(self):
        url = 'https://docs.ollama.com/docs'
        for code, expected in ((403, 'review'), (429, 'review'), (404, 'broken')):
            with patch('scripts.check_links.urlopen', side_effect=HTTPError(url, code, 'failed', None, None)):
                self.assertEqual(check_external(url)['status'], expected)

    def test_network_failure_needs_review(self):
        with patch('scripts.check_links.urlopen', side_effect=URLError('offline')):
            self.assertEqual(check_external('https://docs.ollama.com/docs')['status'], 'review')

    def test_loopback_not_contacted(self):
        with patch('scripts.check_links.urlopen') as fetch:
            self.assertEqual(check_external('http://127.0.0.1/docs')['status'], 'review')
            fetch.assert_not_called()

    def test_unapproved_hosts_credentials_and_ports_not_contacted(self):
        with patch('scripts.check_links.urlopen') as fetch:
            for url in ['https://192.168.1.1/', 'https://169.254.169.254/',
                        'https://example.com/', 'https://user:pass@docs.ollama.com/',
                        'https://docs.ollama.com:444/', 'http://docs.ollama.com/']:
                self.assertEqual(check_external(url)['status'], 'review')
            fetch.assert_not_called()

    def test_redirects_need_review(self):
        url = 'https://docs.ollama.com/docs'
        with patch('scripts.check_links.urlopen', side_effect=HTTPError(url, 302, 'redirect', {'Location': 'http://169.254.169.254/'}, None)) as fetch:
            self.assertEqual(check_external(url)['status'], 'review')
            self.assertEqual(fetch.call_count, 1)


class ContentTests(unittest.TestCase):
    def test_actual_repo_structure(self):
        self.assertEqual(validate(), [])

    def test_render_is_idempotent(self):
        self.assertEqual(*render())

    def test_duplicate_id_regression(self):
        with copied_docs() as root:
            items = json.loads((root / 'concepts.json').read_text())
            items[-1]['id'] = items[0]['id']
            (root / 'concepts.json').write_text(json.dumps(items))
            self.assertTrue(any('unique positive integers' in e for e in validate(root)))

    def test_catalog_size_and_groups_are_not_fixed(self):
        with copied_docs() as root:
            items = json.loads((root / 'concepts.json').read_text())
            topics = json.loads((root / 'core-topics.json').read_text())
            core_ids = {number for topic in topics for number in topic['chapters']}
            optional = next(item for item in items if item['id'] not in core_ids)
            items.remove(optional)
            (root / optional['path']).unlink()
            items[0]['group'] = 'A useful new grouping'
            (root / 'concepts.json').write_text(json.dumps(items))
            (root / 'README.md').write_text(render(root)[1])
            self.assertEqual(validate(root), [])

    def test_topic_count_is_not_fixed(self):
        with copied_docs() as root:
            topics = json.loads((root / 'core-topics.json').read_text())
            removed = topics.pop()
            (root / 'core-topics.json').write_text(json.dumps(topics))
            (root / 'README.md').write_text(render(root)[1])
            self.assertEqual(validate(root), [])
            more = (root / 'README.md').read_text().split('<!-- BEGIN MORE -->')[1]
            items = json.loads((root / 'concepts.json').read_text())
            for item in items:
                if item['id'] in removed['chapters']:
                    self.assertIn(item['path'], more)

    def test_duplicate_topic_anchor(self):
        with copied_docs() as root:
            topics = json.loads((root / 'core-topics.json').read_text())
            topics[-1]['title'] = topics[0]['title'].upper() + '!'
            (root / 'core-topics.json').write_text(json.dumps(topics))
            self.assertTrue(any('unique anchors' in error for error in validate(root)))

    def test_unknown_topic_chapter(self):
        with copied_docs() as root:
            topics = json.loads((root / 'core-topics.json').read_text())
            topics[0]['chapters'].append(9999)
            (root / 'core-topics.json').write_text(json.dumps(topics))
            self.assertTrue(any('chapter references' in error for error in validate(root)))

    def test_unreviewed_resource_cannot_enter_readme(self):
        with copied_docs() as root:
            topics = json.loads((root / 'core-topics.json').read_text())
            topics[0]['resources'].append('https://example.com/unreviewed')
            (root / 'core-topics.json').write_text(json.dumps(topics))
            self.assertTrue(any('absent from its chapter sources' in error for error in validate(root)))

    def test_duplicate_topic_resource(self):
        with copied_docs() as root:
            topics = json.loads((root / 'core-topics.json').read_text())
            topics[0]['resources'].append(topics[0]['resources'][0])
            (root / 'core-topics.json').write_text(json.dumps(topics))
            self.assertTrue(any('unique HTTPS URLs' in error for error in validate(root)))

    def test_resources_before_notes_and_labs(self):
        readme = render()[1]
        self.assertTrue(readme.startswith('# AI Engineering Concepts\n'))
        topics = json.loads((ROOT / 'core-topics.json').read_text())
        for topic in topics:
            section = readme.split(f"## {topic['title']}\n", 1)[1].split('\n## ', 1)[0]
            first_line = section.strip().splitlines()[0]
            self.assertRegex(first_line, r'^- \[.+\]\(https://')
            self.assertLess(section.index(topic['resources'][-1]), section.index('Notes and exercises:'))
        self.assertLess(readme.index(topics[-1]['resources'][-1]), readme.index('## Hands-on labs'))

    def test_every_chapter_remains_reachable(self):
        readme = render()[1]
        for item in json.loads((ROOT / 'concepts.json').read_text()):
            self.assertIn(f"]({item['path']})", readme)

    def test_heading_regression(self):
        with copied_docs() as root:
            path = root / 'concepts/01-llm-mental-models.md'
            path.write_text(path.read_text().replace('# 1.', '# 999.', 1))
            self.assertTrue(any('heading differs' in e for e in validate(root)))

    def test_stale_readme(self):
        with copied_docs() as root:
            path = root / 'README.md'
            path.write_text(path.read_text().replace('Hugging Face LLM course', 'A stale resource label'))
            self.assertTrue(any('indexes are stale' in e for e in validate(root)))

    def test_missing_markers(self):
        with copied_docs() as root:
            path = root / 'README.md'
            path.write_text(path.read_text().replace('<!-- BEGIN TOC -->', ''))
            with self.assertRaises(ValueError):
                render(root)
