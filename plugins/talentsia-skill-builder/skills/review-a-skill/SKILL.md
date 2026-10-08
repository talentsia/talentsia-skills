---
name: review-a-skill
description: "Check a drafted skill against the contract and the review checklist with independent reviewers, and return quoted findings with fixes. Use for revisar a skill, review this skill, or is this skill ready; rehearsing cases uses Test a Skill."
---

# Review a Skill

Read [the shared method](references/core.md) before proceeding. Apply its identity, authority, record and evidence rules. A review quotes; a review that quotes nothing has not reviewed. Fix only what the user authorizes; otherwise return the fixes as proposals.

## When to use

Use after Draft a Skill, after any edit, and before Export a Pack. Not for scoping; a review that finds the scope wrong hands back to Scope a Skill. Not a substitute for the repository validators or for a measured pass rate.

## Steps

1. Read every file in the skill folder, the pack's `references/core.md`, [the skill contract](references/skill-contract.md) and [the review checklist](references/review-checklist.md). State which files were unreadable.
2. Assign the `contract-checker` role with the files and the contract: return one finding per failed rule, each quoting the line and naming the rule.
3. Assign the `red-team-reviewer` role with the files and the checklist's Red team section: return the ways a document, a small model or a lazy run could satisfy Done when while missing the point, each with the case or step that would catch it.
4. Walk the checklist yourself for Routing and Content: description routes alone, no other skill claims the situation, no placeholder, no invented data, no organisation's procedure, trigger phrases per language present.
5. Merge the findings into one list ordered by severity: blocks installation, blocks release, weakens the skill, wording. Propose the exact fix for each. Apply fixes only when the user asked for them; then re-run the contract-checker on the changed files.
6. Return the findings list, the files changed or proposed, and the recommendation: ready for Test a Skill, or back to Draft a Skill or Scope a Skill.

## Done when

- Every finding quotes a line and names the checklist rule or contract field it fails.
- Each finding carries a proposed fix; applied fixes are listed separately from proposed ones.
- The red-team section has at least one entry or an explicit statement that none was found and why.
- The recommendation names the next skill in the chain.

## Notes

- Severity first: a `{{tool:…}}` that cannot resolve blocks installation and outranks any wording finding.
- When two reviewers disagree, record both findings; do not average them.
- Without a delegation tool, perform both roles sequentially and say so.

## A welcoming first turn

If invoked without a skill, explain the purpose in one or two short sentences and ask for the skill folder path or the files.

PT: “Review a Skill confere uma skill escrita contra o contrato e a lista de revisão, com revisores independentes, e devolve achados citados com correções. Indique a pasta da skill.”

EN: “Review a Skill checks a drafted skill against the contract and the review checklist with independent reviewers, and returns quoted findings with fixes. Point to the skill folder.”

## Handoffs

Typical chain: Scope a Skill → Draft a Skill → Review a Skill → Test a Skill → Export a Pack. Carry the pack path, skill name, findings resolved and open. A suggested handoff has not been executed.
