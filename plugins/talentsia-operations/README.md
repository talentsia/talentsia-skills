# Talentsia Operations

Looking after the device a team runs on, and getting what arrives to the right person.

Free, basic edition for Talentsia Edge workers. MIT licensed. The contract these skills follow is [docs/edge-worker-skills.md](../../docs/edge-worker-skills.md); validate with `python3 scripts/check_edge_skills.py`.

| Skill | What it does | Replaces |
|---|---|---|
| [`check-the-device`](skills/check-the-device/SKILL.md) | Inspect the device a worker runs on and repair only what its policy permits, reporting what was observed rather than what was expected. | `edge_health_check` v1 |
| [`route-an-arriving-document`](skills/route-an-arriving-document/SKILL.md) | Identify what an arriving document is, record it, file it, and pass it to whoever owns that kind of work. | `document_intake_routing` v1 |
