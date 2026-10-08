---
name: draft-a-skill
description: "Write a skill's files from an agreed scope: SKILL.md, skill.json, subagents, graded cases and harness metadata, using the bundled template and builder roles. Use for escrever a skill, draft the skill files, or generate the skill; agreeing the scope uses Scope a Skill."
---

# Draft a Skill

Read [the shared method](references/core.md) before proceeding. Apply its identity, authority, record and evidence rules. Write only into the designated pack folder; without one, return every file as a fenced block with its path, marked **not saved**.

## When to use

Use when a scope exists (from Scope a Skill or supplied by the user) and the files should be written. Not for inventing scope mid-draft: when the scope is missing a failure to prevent or Done when lines, run Scope a Skill first. Not for reviewing or testing.

## Steps

1. Read the scope, the destination pack's `references/core.md`, any existing skill in the pack with a similar name, and [the skill template](references/skill-template.md). Reuse the pack's version, publisher, tier, edition and license.
2. Assign the `case-author` role with the scope and [eval design](references/eval-design.md): return `evals/cases.json` with the regression case first, then an ordinary, a boundary and, if a step depends on a tool, a missing-input case.
3. Assign the `step-writer` role with the scope, the cases and [capabilities](references/capabilities.md): return `## Steps` and `## Done when` such that every case can be passed by following the steps, and every `{{tool:…}}` resolves to a required interface.
4. If the scope declares a subagent, assign the `step-writer` role again for each `agents/<name>.md`: design the output schema first, then at most six steps; `tools` only narrows.
5. Fill the remaining skeletons yourself: frontmatter, When to use, Notes, the welcoming first turn in each supported language, Handoffs, `skill.json` with `status` `draft`, `summary` equal to `description`, `verification` equal to Done when, `subagents` equal to the files written, and `agents/openai.yaml`.
6. Assign the `contract-checker` role with every file and [the skill contract](references/skill-contract.md); fix each finding it quotes. Search every file for `<` and remove any placeholder left.
7. Write the files (or return them marked not saved), copy the pack's `references/*.md` into the skill's `references/`, read back one written file to confirm, and report the tree. Offer Review a Skill.

## Done when

- Every file in the template exists for the skill, parses, and contains no `<` placeholder.
- `skill.json.summary` equals the description; `verification` equals the Done when lines; `subagents` equals the files in `agents/`; `status` is `draft`; `model.evals` is `{}`.
- Every `{{tool:…}}` names a required interface and a defined operation; every `{{agent:…}}` names a written subagent.
- `evals/cases.json` has at least three cases and one regression case, and no observation contains a name, organisation, date or figure that could read as real.
- The contract-checker's findings are quoted and resolved, or listed under What I could not establish.

## Notes

- Write cases before steps. A step no case would catch is a step nobody will notice failing.
- Prefer a `read` before every `write`, fewer interfaces, fewer subagents. Eight steps is a limit, not a target.
- Without a delegation tool, perform the three roles sequentially in the order above and say "role analysis was sequential".

## A welcoming first turn

If invoked without a scope, explain the purpose in one or two short sentences and ask for the scope block or offer Scope a Skill.

PT: “Draft a Skill escreve os arquivos de uma skill a partir de um escopo acordado: entrada, contrato, subagentes e casos de teste. Envie o escopo ou peça para definir um com Scope a Skill.”

EN: “Draft a Skill writes a skill's files from an agreed scope: entrypoint, contract, subagents and graded cases. Send the scope, or ask to define one with Scope a Skill.”

## Handoffs

Typical chain: Scope a Skill → Draft a Skill → Review a Skill → Test a Skill → Export a Pack. Carry the pack path, skill name, files written or proposed, and the contract-checker's open findings. A suggested handoff has not been executed.
