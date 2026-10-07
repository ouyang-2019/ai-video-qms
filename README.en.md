# AI Video QMS

A portable, four-tier quality system for AI video, short drama, animation and image assets.

**Choose controlled procedures → navigate Wiki methods → retrieve original evidence → load the necessary Skills → create and inspect the deliverable.**

The public edition provides 143 controlled documents, 8 dated model/platform profiles, 4 installable Skills, an extensible image taxonomy (19 purposes × 10 layouts), local full-text RAG, shot-plan checks and 6 original examples. Python 3.10+ and Node 20+ are required; no package installation or paid generation is needed.

```bash
git clone https://github.com/ouyang-2019/ai-video-qms.git
cd ai-video-qms
python -X utf8 tools/qms.py doctor
python -X utf8 tools/qms.py seed-demo
python -X utf8 tools/qms.py search "gaze cup pause"
python -X utf8 tools/qms.py shot-check --plan examples/cup-pause/shot-plan.json
```

The four tiers are manual, procedure, SOP/Skill, and template/example/record. The ISO 9001 inspired organization is not a certification claim. Structural, source review, approval, API execution and audiovisual inspection remain separate evidence states.

Private production records, collected third-party prompt texts, media and credentials are not included. New evidence starts pending; approvals bind to full SHA256. Local-only and no-AI restrictions are checked at retrieval time, and packs never silently truncate.

See the [Chinese guide](README.md), [quick start](docs/QUICKSTART.md), [source policy](docs/SOURCE_INTAKE.md) and [third-party notices](THIRD_PARTY_NOTICES.md). Original code and authored public documentation are MIT licensed.
