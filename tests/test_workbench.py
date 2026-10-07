import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

SOURCE_ROOT = Path(__file__).resolve().parents[1]
CLI = SOURCE_ROOT / "tools" / "qms.py"


def run_cli(root, *args):
    return subprocess.run([sys.executable, "-X", "utf8", str(CLI), "--root", str(root), *args], cwd=str(root), encoding="utf-8", capture_output=True)


class WorkbenchCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name) / "AI 视频 QMS Clone"
        shutil.copytree(SOURCE_ROOT, self.root, ignore=shutil.ignore_patterns(".git", "data", "__pycache__", "*.pyc", "node_modules"))

    def tearDown(self):
        self.tmp.cleanup()

    def json_ok(self, *args):
        result = run_cli(self.root, *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def ensure_demo_hashes(self):
        index = self.root / "examples" / "methods" / "index.json"
        data = json.loads(index.read_text(encoding="utf-8"))
        for row in data["sources"]:
            row["sha256"] = __import__("hashlib").sha256((self.root / row["file"]).read_bytes()).hexdigest()
            row.setdefault("privacy", "ai_allowed")
            row.setdefault("license_status", "MIT")
        index.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return data

    def seal_single_crlf_fixture(self):
        doc_rel = "documents/test/CRLF-DOC.md"
        doc_path = self.root / "standards" / doc_rel
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        raw = b"# CRLF controlled doc\r\n\r\nLine one.\r\nLine two.\r\n"
        doc_path.write_bytes(raw)
        registry = {
            "schema_version": 1,
            "title": "CRLF test registry",
            "version": "0.0.1",
            "release_required": True,
            "documents": [
                {
                    "id": "CRLF-DOC",
                    "title": "CRLF Controlled Doc",
                    "level": 3,
                    "kind": "sop",
                    "version": "1.0.0",
                    "file": doc_rel,
                    "stages": ["script"],
                    "models": ["common"],
                    "model_versions": ["*"],
                    "platforms": ["*"],
                    "modes": ["*"],
                    "styles": [],
                    "status": "released",
                    "verification": "structural",
                    "privacy": "ai_allowed",
                    "source_ids": ["TEST-SOURCE"],
                    "requires": [],
                }
            ],
            "profiles": [
                {"model": "h3", "version": "h3", "platform": "prompt-only", "modes": ["T2VA"], "status": "released", "source_ids": ["TEST-SOURCE"]}
            ],
        }
        sources = {
            "schema_version": 1,
            "sources": [
                {"source_id": "TEST-SOURCE", "source_kind": "internal", "captured_at": "2026-10-07", "license_status": "test", "verification": "structural", "privacy": "ai_allowed"}
            ],
        }
        registry_path = self.root / "standards" / "registry.json"
        sources_path = self.root / "standards" / "sources.json"
        registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sources_path.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        expected = hashlib.sha256(raw).hexdigest()
        release = {
            "schema_version": 1,
            "registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
            "sources_sha256": hashlib.sha256(sources_path.read_bytes()).hexdigest(),
            "documents": [{"id": "CRLF-DOC", "file": doc_rel, "version": "1.0.0", "sha256": expected}],
        }
        (self.root / "standards" / "release-content.json").write_text(json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return doc_path, expected
    def test_doctor_profiles_and_facets(self):
        report = self.json_ok("doctor")
        self.assertTrue(report["ok"], report)
        self.assertGreaterEqual(report["standards"]["counts"]["documents"], 100)
        self.assertGreaterEqual(len(self.json_ok("profiles")["profiles"]), 8)
        facets = self.json_ok("facets")["facets"]
        self.assertIn("performance.microexpression", facets)
        self.assertIn("layout.grid_3x3", facets)

    def test_missing_manifest_is_rejected_without_runtime_cache(self):
        (self.root / "standards" / "release-content.json").unlink()
        result = run_cli(self.root, "doctor")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("release-content.json", result.stderr)
        self.assertFalse((self.root / "data" / "cache" / "runtime-standards").exists())

    def test_get_pack_use_sealed_file_bytes_for_crlf_documents(self):
        doc_path, expected = self.seal_single_crlf_fixture()
        before = doc_path.read_bytes()
        node = self.json_ok("select", "--stage", "script")
        self.assertEqual(node["documents"][0]["sha256"], expected)
        got = self.json_ok("get", "CRLF-DOC")
        self.assertEqual(got["source"]["sha256"], expected)
        self.assertIn("Line one.", got["text"])
        packed = run_cli(self.root, "pack", "--ids", "CRLF-DOC", "--max-chars", "5000")
        self.assertEqual(packed.returncode, 0, packed.stderr)
        self.assertIn(expected, packed.stdout)
        manifest = json.loads((self.root / "standards" / "release-content.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["documents"][0]["sha256"], expected)
        self.assertEqual(doc_path.read_bytes(), before)
    def test_model_tuple_is_required_for_video(self):
        result = run_cli(self.root, "select", "--stage", "video", "--model", "h3")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Full model/version/platform/mode tuple", result.stderr)
        ok = self.json_ok("select", "--stage", "video", "--model", "h3", "--version", "h3", "--platform", "prompt-only", "--mode", "T2VA")
        self.assertTrue(ok["documents"])

    def test_bundle_budget_and_no_overwrite(self):
        result = run_cli(self.root, "bundle", "--stage", "script", "--max-chars", "10")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("budget", result.stderr)
        out = self.root / "data" / "bundle.md"
        first = self.json_ok("bundle", "--stage", "script", "--out", str(out))
        self.assertTrue(out.exists())
        self.assertGreater(first["characters"], 1000)
        second = run_cli(self.root, "bundle", "--stage", "script", "--out", str(out))
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("already exists", second.stderr)
        blocked = run_cli(self.root, "bundle", "--stage", "script", "--out", str(self.root / "standards" / "x.md"))
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("cannot be written", blocked.stderr)

    def test_import_review_search_get_pack_and_hash_drift(self):
        source = self.root / "data" / "输入 提示.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("角色三视图用于锁定人物一致性，包含正面侧面背面。", encoding="utf-8")
        row = self.json_ok("import", "--file", str(source), "--title", "角色三视图方法", "--privacy", "ai_allowed", "--stage", "assets", "--facets", "asset.turnaround")
        source_id = row["id"]
        self.assertEqual(row["status"], "pending")
        self.json_ok("review", "--id", source_id, "--decision", "approved", "--reason", "test approval")
        hits = self.json_ok("search", "三视图", "--stage", "assets", "--facets", "asset.turnaround")
        self.assertEqual(hits["hits"][0]["id"], source_id)
        got = self.json_ok("get", source_id)
        self.assertIn("正面侧面背面", got["text"])
        packed = run_cli(self.root, "pack", "--ids", source_id, "--max-chars", "5000")
        self.assertEqual(packed.returncode, 0, packed.stderr)
        self.assertIn("<source_data>", packed.stdout)
        self.assertIn("license_status", packed.stdout)
        catalog = self.root / "data" / "corpus" / "catalog.json"
        data = json.loads(catalog.read_text(encoding="utf-8"))
        data["sources"][0]["sha256"] = "0" * 64
        catalog.write_text(json.dumps(data), encoding="utf-8")
        drift = run_cli(self.root, "get", source_id)
        self.assertNotEqual(drift.returncode, 0)
        self.assertIn("hash", drift.stderr)

    def test_context_uses_search_as_clues_and_explicit_evidence_as_full_text(self):
        source = self.root / "data" / "method.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("杯子停顿方法：手先停，眼神再到杯子。", encoding="utf-8")
        row = self.json_ok("import", "--file", str(source), "--title", "杯子停顿", "--privacy", "ai_allowed", "--stage", "craft", "--facets", "performance.microexpression")
        self.json_ok("review", "--id", row["id"], "--decision", "approved", "--reason", "test approval")
        clue = run_cli(self.root, "context", "--task", "micro-performance", "--query", "杯子停顿", "--max-chars", "120000")
        self.assertEqual(clue.returncode, 0, clue.stderr)
        self.assertIn("RAG Search Clues", clue.stdout)
        self.assertNotIn("<source_data>", clue.stdout)
        explicit = run_cli(self.root, "context", "--task", "micro-performance", "--query", "杯子停顿", "--facets", "performance.microexpression", "--max-chars", "120000")
        self.assertEqual(explicit.returncode, 0, explicit.stderr)
        self.assertIn(row["id"], explicit.stdout)
        full = run_cli(self.root, "context", "--task", "micro-performance", "--evidence-ids", row["id"], "--max-chars", "120000")
        self.assertEqual(full.returncode, 0, full.stderr)
        self.assertIn("<source_data>", full.stdout)
        small = run_cli(self.root, "context", "--task", "micro-performance", "--evidence-ids", row["id"], "--max-chars", "100")
        self.assertNotEqual(small.returncode, 0)
        self.assertIn("budget", small.stderr)

    def test_all_wiki_tasks_context(self):
        tasks = json.loads((self.root / "wiki" / "index.json").read_text(encoding="utf-8"))["tasks"]
        for task in tasks:
            args = ["context", "--task", task, "--max-chars", "240000"]
            if task == "assets":
                args += ["--model", "gpt-image", "--version", "gpt-image-2-2026-04-21", "--platform", "openai-images-api", "--mode", "T2I"]
            if task == "video":
                args += ["--model", "h3", "--version", "h3", "--platform", "prompt-only", "--mode", "T2VA"]
            result = run_cli(self.root, *args)
            self.assertEqual(result.returncode, 0, f"{task}: {result.stderr}")
            self.assertIn("Controlled Standards Bundle", result.stdout)

    def test_wiki_and_mixed_pack_controlled_document(self):
        wiki = run_cli(self.root, "wiki", "--task", "storyboard")
        self.assertEqual(wiki.returncode, 0, wiki.stderr)
        self.assertIn("分镜", wiki.stdout)
        packed = run_cli(self.root, "pack", "--ids", "QM-001", "--max-chars", "50000")
        self.assertEqual(packed.returncode, 0, packed.stderr)
        self.assertIn("AI视频生产质量手册", packed.stdout)
        self.assertIn("source_ids", packed.stdout)

    def test_all_image_taxonomy_routes_and_semantics(self):
        taxonomy = json.loads((self.root / "standards" / "metadata" / "image-taxonomy.json").read_text(encoding="utf-8"))
        no_semantics = run_cli(self.root, "image-route", "--purpose", "prop", "--layout", "grid_3x3")
        self.assertNotEqual(no_semantics.returncode, 0)
        self.assertIn("semantics", no_semantics.stderr)
        for task in taxonomy["tasks"]:
            for layout in taxonomy["layouts"]:
                semantics = "temporal_sequence" if task["id"] == "storyboard_sequence" else ("single_state" if layout["id"] == "single" else "independent_collection")
                result = run_cli(self.root, "image-route", "--purpose", task["id"], "--layout", layout["id"], "--semantics", semantics)
                if task["id"] == "storyboard_sequence" and layout["id"] == "single":
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("conflicts", result.stderr)
                    continue
                self.assertEqual(result.returncode, 0, f"{task['id']} {layout['id']}: {result.stderr}")
                data = json.loads(result.stdout)
                self.assertEqual(data["model_contract"], "unresolved")
                self.assertNotIn("selection", data)
                self.assertTrue(data["model_tuple_required_for_execution"])
                self.assertFalse(data["generation_executed"])
                self.assertIn(task["facet"], data["facets"])
                self.assertIn(layout["facet"], data["facets"])
        explicit = self.json_ok("image-route", "--purpose", "turnaround", "--layout", "grid_3x3", "--semantics", "independent_collection", "--model", "gpt-image", "--version", "gpt-image-2-2026-04-21", "--platform", "openai-images-api", "--mode", "T2I")
        self.assertEqual(explicit["model_contract"], "resolved")
        self.assertIn("selection", explicit)
        unknown = run_cli(self.root, "image-route", "--purpose", "unknown", "--layout", "grid_3x3", "--semantics", "independent_collection")
        self.assertNotEqual(unknown.returncode, 0)
        self.assertIn("gap", unknown.stderr)

    def test_seed_demo_requires_hash_and_does_not_reapprove_excluded(self):
        self.ensure_demo_hashes()
        seeded = self.json_ok("seed-demo")
        self.assertEqual(seeded["imported"], 6)
        self.assertIn("no audiovisual validation", seeded["sources"][0]["reason"])
        first_id = seeded["sources"][0]["id"]
        self.json_ok("review", "--id", first_id, "--decision", "excluded", "--reason", "excluded fixture")
        excluded = run_cli(self.root, "seed-demo")
        self.assertNotEqual(excluded.returncode, 0)
        self.assertIn("excluded", excluded.stderr)

    def test_seed_demo_hash_drift_fails_preflight(self):
        data = self.ensure_demo_hashes()
        data["sources"][0]["sha256"] = "0" * 64
        (self.root / "examples" / "methods" / "index.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = run_cli(self.root, "seed-demo")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hash drift", result.stderr)
        self.assertFalse((self.root / "data" / "corpus" / "catalog.json").exists())

    def test_shot_check_invalid_plan_returns_nonzero(self):
        plan_path = self.root / "data" / "invalid-shot.json"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text("{}", encoding="utf-8")
        result = run_cli(self.root, "shot-check", "--plan", str(plan_path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('"ok": false', result.stdout)

    def test_shot_check_and_bundle(self):
        plan = {"project_id": "demo", "intent": "测试完整镜头设计", "audience": "短剧制作团队", "continuity_baseline": "角色坐在桌边，右手拿杯子。", "model": {"model": "h3", "version": "h3", "platform": "prompt-only", "mode": "T2VA"}, "shots": [{"id": "S1", "duration_seconds": 3, "story_change": "角色发现杯子不见了。", "start_state": "杯子在桌面右侧。", "end_state": "角色视线落到空位。", "assets": ["character-ref"], "evidence_ids": [], "departments": {}, "performances": [{"character_id": "A", "objective": "确认杯子位置", "stimulus": "手摸到空桌面", "baseline": "身体正坐，呼吸平稳", "beats": [{"start": 0, "end": 1.4, "body": "右手停在桌面", "gaze": "视线从手移到桌面", "face": "眼睑轻收", "breath": "短暂停顿"}, {"start": 1.4, "end": 3, "body": "肩膀轻微前倾", "gaze": "看向杯子原位置", "face": "嘴角收紧", "breath": "缓慢呼出"}]}]}]}
        facet_map = {"writing": ["script.beat"], "performance": ["performance.microexpression"], "blocking": ["blocking.position"], "props": ["props.state"], "wardrobe": ["art.costume"], "environment": ["art.scene"], "camera": ["camera.motion"], "lighting": ["art.light"], "action": ["action.physics"], "vfx": ["vfx.lifecycle"], "voice": ["audio.voice"], "sound": ["audio.foley"], "editing": ["edit.rhythm"], "continuity": ["continuity.state"]}
        for domain, facets in facet_map.items():
            plan["shots"][0]["departments"][domain] = {"status": "designed", "design": f"{domain} design", "acceptance": f"{domain} observable acceptance", "facets": facets}
        plan_path = self.root / "data" / "shot-plan.json"
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        check = self.json_ok("shot-check", "--plan", str(plan_path))
        self.assertTrue(check["ok"], check)
        bundle_path = self.root / "data" / "shot-bundle.md"
        bundle = self.json_ok("shot-bundle", "--plan", str(plan_path), "--out", str(bundle_path), "--max-chars", "240000")
        self.assertTrue(bundle_path.exists())
        self.assertIn("bundle_sha256", bundle)
        self.assertIn("镜头制作执行包", bundle_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
