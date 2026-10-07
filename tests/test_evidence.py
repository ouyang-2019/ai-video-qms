import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.evidence import EvidenceStore


class EvidenceStoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = EvidenceStore(self.root)
        self.src = self.root / "inputs"
        self.src.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write_source(self, name, text):
        path = self.src / name
        path.write_text(text, encoding="utf-8")
        return path

    def import_approved(self, text="角色三视图用于保持人物一致性 camera blocking"):
        row = self.store.import_source(
            self.write_source("source.md", text),
            "角色图规范",
            privacy="ai_allowed",
            stages=["assets"],
            facets=["art.character"],
        )
        return self.store.review(row["id"], "approved", "fixture")

    def test_empty_catalog_doctor(self):
        self.assertEqual(self.store.doctor()["sources"], 0)
        self.assertTrue(self.store.doctor()["ok"])

    def test_chinese_search(self):
        source = self.import_approved()
        result = self.store.search("三视图", target="remote")
        self.assertEqual(result["hits"][0]["id"], source["id"])

    def test_duplicate_import_deduplicates_by_sha(self):
        first = self.import_approved()
        second = self.store.import_source(self.write_source("copy.md", "角色三视图用于保持人物一致性 camera blocking"), "copy")
        self.assertEqual(first["id"], second["id"])

    def test_hash_drift_is_rejected(self):
        source = self.import_approved()
        blob = self.root / "data" / "corpus" / "blobs" / f"{source['sha256']}.md"
        blob.write_text("tampered", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.store.get(source["id"], target="remote")

    def test_approved_sha_is_not_auto_refreshed(self):
        source = self.import_approved()
        catalog = self.root / "data" / "corpus" / "catalog.json"
        data = json.loads(catalog.read_text(encoding="utf-8"))
        data["sources"][0]["sha256"] = "0" * 64
        catalog.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.store.get(source["id"], target="remote")

    def test_privacy_dynamic(self):
        source = self.import_approved()
        self.store.set_privacy(source["id"], "local")
        with self.assertRaises(ValueError):
            self.store.get(source["id"], target="remote")
        self.assertIn("角色三视图", self.store.get(source["id"], target="local")["text"])
        self.store.set_privacy(source["id"], "no_ai")
        with self.assertRaises(ValueError):
            self.store.get(source["id"], target="local")

    def test_pack_budget_exceeded_without_truncation(self):
        source = self.import_approved("角色三视图" * 100)
        with self.assertRaises(ValueError):
            self.store.pack([source["id"]], max_chars=20, target="remote")

    def test_path_traversal_id_rejected(self):
        with self.assertRaises(ValueError):
            self.store.get("../bad", target="local")

    def test_pending_and_excluded_visibility(self):
        row = self.store.import_source(self.write_source("pending.md", "分镜提示词"), "pending", privacy="local")
        self.assertEqual(self.store.search("分镜", target="local")["hits"], [])
        self.assertTrue(self.store.search("分镜", target="local", include_pending=True)["hits"])
        self.store.review(row["id"], "excluded", "not relevant")
        self.assertEqual(self.store.search("分镜", target="local", include_pending=True)["hits"], [])

    def test_stage_and_facet_filter(self):
        source = self.import_approved()
        self.assertEqual(self.store.search("角色", target="remote", stage="assets")["hits"][0]["id"], source["id"])
        self.assertEqual(self.store.search("角色", target="remote", stage="script")["hits"], [])
        self.assertEqual(self.store.search("角色", target="remote", facets=["art.character"])["hits"][0]["id"], source["id"])
        with self.assertRaises(ValueError):
            self.store.search("角色", stage="unknown")
        with self.assertRaises(ValueError):
            self.store.search("角色", facets=["x", "x"])


if __name__ == "__main__":
    unittest.main()
