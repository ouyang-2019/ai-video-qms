import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.evidence import EvidenceStore


class EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        self.store = EvidenceStore(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def source(self, privacy='ai_allowed'):
        p = self.root / 'method.md'
        p.write_text('杯子停顿：手指先停止，目光再移动。', encoding='utf-8')
        row = self.store.import_source(p, '杯子表演', privacy=privacy, stages=['craft'])
        return self.store.review(row['id'], 'approved', 'test full-text method review')

    def tamper(self, field, value):
        p = self.root / 'data/corpus/catalog.json'
        data = json.loads(p.read_text(encoding='utf-8'))
        data['sources'][0][field] = value
        p.write_text(json.dumps(data), encoding='utf-8')

    def test_empty_read_does_not_create_data(self):
        self.assertTrue(self.store.doctor()['ok'])
        self.store.search('杯子')
        self.assertFalse((self.root / 'data').exists())

    def test_invalid_privacy_fails_closed(self):
        row = self.source()
        self.tamper('privacy', 'unexpected')
        with self.assertRaises(ValueError):
            self.store.get(row['id'])

    def test_catalog_id_must_match_full_hash(self):
        self.source()
        self.tamper('id', 'SRC-' + '0' * 24)
        with self.assertRaises(ValueError):
            self.store.get('SRC-' + '0' * 24)

    def test_duplicate_import_keeps_provenance_and_tightens_privacy(self):
        row = self.source()
        p = self.root / 'copy.md'
        p.write_text('杯子停顿：手指先停止，目光再移动。', encoding='utf-8')
        duplicate = self.store.import_source(p, 'private copy', url='https://example.test/method', privacy='local', stages=['craft'])
        self.assertEqual(row['id'], duplicate['id'])
        with self.assertRaises(ValueError):
            self.store.get(row['id'], target='remote')
        self.assertTrue(any(o.get('url') == 'https://example.test/method' for o in duplicate['occurrences']))

    def test_invalid_target_is_rejected_even_when_empty(self):
        with self.assertRaises(ValueError):
            self.store.search('x', target='unexpected')

    def test_review_requires_reason(self):
        row = self.source()
        with self.assertRaises(ValueError):
            self.store.review(row['id'], 'approved', '')

    def test_latest_no_ai_works_with_missing_blob(self):
        row = self.source()
        blob = self.root / ('data/corpus/blobs/' + row['sha256'] + '.md')
        blob.unlink()
        self.store.set_privacy(row['id'], 'no_ai')
        with self.assertRaises(ValueError):
            self.store.get(row['id'], target='local')
        self.assertEqual(self.store.search('杯子', target='local')['hits'], [])

    def test_blob_directory_cannot_escape_repository(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        parent = self.root / 'data/corpus'
        parent.mkdir(parents=True, exist_ok=True)
        link = parent / 'blobs'
        if link.exists():
            link.rmdir()
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(str(exc))
        p = self.root / 'untrusted.md'
        p.write_text('not permitted outside repository', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.store.import_source(p, 'escape')
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
