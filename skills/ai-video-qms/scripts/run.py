#!/usr/bin/env python3
"""Portable runner for the public AI Video QMS skills."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _candidate_from_runtime(skill_dir: Path) -> Path | None:
    runtime = skill_dir / ".runtime.json"
    if not runtime.is_file():
        return None
    try:
        value = json.loads(runtime.read_text(encoding="utf-8")).get("repository_root")
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(value, str) or not value.strip():
        return None
    return Path(value).expanduser().resolve()


def _find_repo() -> Path:
    candidates: list[Path] = []
    env = os.environ.get("AI_VIDEO_QMS_HOME")
    if env:
        candidates.append(Path(env).expanduser().resolve())
    here = Path(__file__).resolve()
    candidates.append(_candidate_from_runtime(here.parents[1]) or Path("__missing__"))
    candidates.extend(here.parents)
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "qms-project.json").is_file():
            return candidate
    raise SystemExit(
        "AI Video QMS repository not found. Set AI_VIDEO_QMS_HOME, create .runtime.json with "
        "repository_root, or keep the skill inside a repository containing qms-project.json."
    )


def main() -> int:
    repo = _find_repo()
    qms = repo / "tools" / "qms.py"
    if not qms.is_file():
        raise SystemExit(f"Missing runtime CLI: {qms}")
    cmd = [sys.executable, "-X", "utf8", str(qms), "--root", str(repo), *sys.argv[1:]]
    completed = subprocess.run(cmd)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
