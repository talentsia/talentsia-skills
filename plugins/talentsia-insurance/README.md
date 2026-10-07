# Talentsia Insurance

Reading insurance documents for what they actually say, comparing options, and turning real deadlines into tasks.

Free, basic edition for Talentsia Edge workers. MIT licensed. The contract these skills follow is [docs/edge-worker-skills.md](../../docs/edge-worker-skills.md); validate with `python3 scripts/check_edge_skills.py`.

| Skill | What it does | Replaces |
|---|---|---|
| [`review-an-insurance-document`](skills/review-an-insurance-document/SKILL.md) | Review one insurance document and establish what it actually says. | `insurance_document_review` v1 |
| [`compare-policies`](skills/compare-policies/SKILL.md) | Compare insurance options and surface the material differences, with a recommendation and what must be resolved first. | `policy_comparison` v1 |
| [`review-renewals`](skills/review-renewals/SKILL.md) | Find the real future obligations in an insurance document and make each one a dated task. | `renewal_review` v1 |

This is the free, basic edition. An enhanced premium edition (lines of business, jurisdictions, claims) can replace it later.
