---
name: scope-a-skill
description: "Turn described work into an agreed skill scope: when to use it, what done looks like, the failure it prevents, the capabilities and subagents it needs. Use for definir uma skill, scope a new skill, or what should this skill do; writing the files uses Draft a Skill."
---

# Scope a Skill

Read [the shared method](references/core.md) before proceeding. Apply its identity, authority, record and evidence rules. The builder proposes and drafts; the user owns scope, destination and publication. Nothing is measured here.

## When to use

Use when someone describes work a worker should do and no skill exists yet, or when an existing skill's purpose is unclear. Not for writing files: that is Draft a Skill. Not for choosing which existing skill to install.

## Steps

1. Read what the user gave: the work, who does it today, what goes wrong, which pack it belongs to. Read the pack's `references/core.md` and existing skills if a pack is named, so the new skill does not claim a situation another skill already owns.
2. Name the failure the skill exists to prevent, in one sentence. If the user cannot name one, the skill is probably a habit rather than a skill; say so and offer to stop.
3. Write the completion contract first: three to five `Done when` lines a person could check against a tool result or an artifact, following [the skill contract](references/skill-contract.md).
4. Write `When to use` as one paragraph including when not to use it, and a `description` line with trigger phrases in each language the pack supports and the adjacent skill named.
5. List the fewest capabilities from [capabilities](references/capabilities.md) that let the steps resolve, and decide whether any part merits a subagent under [the subagent contract](references/subagent-contract.md). Fewer is better; say why each is needed.
6. Return the scope as a compact block: name, description, when to use, done when, failure to prevent, capabilities, subagents, open questions. Ask at most one question that would change the scope. Offer Draft a Skill.

## Done when

- The failure to prevent is one sentence the user agreed to or corrected.
- Every Done when line is checkable against a tool result or artifact, not against intent.
- Every capability listed is named by at least one intended step; every subagent has an independent, verifiable part.
- No name, organisation, date or figure from the user's description was copied into the scope as an example.

## Notes

- A scope that needs more than eight steps is two skills. Propose the split and the handoff between them.
- When the user's description contains their organisation's procedure, keep it out of the scope: the device supplies procedures at run time. Note what the skill will read from the device instead.

## A welcoming first turn

If invoked without a description, explain the purpose in one or two short sentences and invite one: the work, what goes wrong, who does it now.

PT: “Scope a Skill ajuda a transformar um trabalho descrito em uma skill com limites claros: quando usar, o que é estar pronto, e a falha que ela evita. Descreva o trabalho como ele acontece hoje.”

EN: “Scope a Skill turns described work into a skill with clear limits: when to use it, what done looks like, and the failure it prevents. Describe the work as it happens today.”

## Handoffs

Typical chain: Scope a Skill → Draft a Skill → Review a Skill → Test a Skill → Export a Pack. Carry the pack path, the agreed scope block and open questions. A suggested handoff has not been executed.
