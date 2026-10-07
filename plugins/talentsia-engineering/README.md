# Talentsia Engineering

Implementing a brief as a reviewed change, reviewing a change against its brief, and running a named scan, in repositories a worker is authorised on.

Free, basic edition for Talentsia Edge workers. MIT licensed. The contract these skills follow is [docs/edge-worker-skills.md](../../docs/edge-worker-skills.md); validate with `python3 scripts/check_edge_skills.py`.

| Skill | What it does | Replaces |
|---|---|---|
| [`implement-from-a-brief`](skills/implement-from-a-brief/SKILL.md) | Turn a written brief into a reviewed, previewed change in an authorised repository, without claiming anything a tool did not return. | `implement_from_brief` v1 |
| [`review-a-change`](skills/review-a-change/SKILL.md) | Judge a prepared change against its brief, its checks and its claims, and return one verdict a person can act on. | `review_a_change` v1 |
| [`run-a-scan`](skills/run-a-scan/SKILL.md) | Run a named scan over an authorised repository and report exactly what it found, with the log it wrote. | `run_a_scan` v1 |

None of these skills publishes, merges or deploys. Merging exists only inside a release a person approved, and no skill may require it.
