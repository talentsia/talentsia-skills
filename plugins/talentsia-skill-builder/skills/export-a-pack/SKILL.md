---
name: export-a-pack
description: "Assemble a distributable pack from its skills: manifests, package instructions, README, synchronized reference exports, Edge catalog when complete, and the hand-over to the repository scripts. Use for exportar o pacote, build the pack, or make this installable; publishing and tagging remain maintainer steps."
---

# Export a Pack

Read [the shared method](references/core.md) before proceeding. Apply its identity, authority, record and evidence rules. The builder writes pack files into the designated folder and hands over; it does not build archives, tag, attest, publish or edit marketplace manifests.

## When to use

Use when every skill in a pack has passed Review a Skill and, ideally, Test a Skill, and the pack should be installable in a harness or submitted for Edge devices. Not for a single skill mid-draft, and not for release: that is the maintainer with the repository scripts.

## Steps

1. Read the pack folder, every `skills/*/SKILL.md` and `skill.json`, and [export layout](references/export-layout.md). List skills missing `skill.json` or `evals/cases.json`; the Edge render needs all of them.
2. Assign the `pack-assembler` role with the skill list and the layout: return `plugin.json`, `.claude-plugin/plugin.json`, `AGENTS.md`, `README.md` and, only when every skill is complete, `talentsia-package.json`, each filled from the skills' own descriptions with no invented facts.
3. Synchronise exports: copy the pack's `references/*.md` into each skill's `references/` and confirm they are byte-identical. Write or refresh `pocket/method.md` from `references/core.md`.
4. Assign the `contract-checker` role with the whole pack: every JSON parses, every relative link resolves, every skill's `openai.yaml` is present, no `<` placeholder, no file type other than `.md`/`.json`/`.yaml`/`.svg`, no credential or personal datum.
5. Write the files (or return them marked not saved) and read back the manifests to confirm. Do not write to `.agents/plugins/` or `.claude-plugin/` at the repository root.
6. Return the file tree, the validation and packaging commands from export layout, the marketplace entries and tag name as text for the maintainer, and `What I could not establish`: no pass rate measured, manifests not pinned to a tag, no archive built.

## Done when

- Both plugin manifests share name, version and homepage; icon paths resolve.
- Every skill folder has `SKILL.md`, `agents/openai.yaml` and reference exports identical to the pack's `references/`.
- `talentsia-package.json` exists only if every skill has `skill.json` and `evals/cases.json`, and lists exactly the skill folders.
- README names what the pack will not do and states that model behaviour is unmeasured until the harness runs.
- No marketplace manifest, tag, archive or release was created or claimed.

## Notes

- The README's install section follows the existing packs: marketplace path for ChatGPT desktop and Codex, `claude plugin` commands, Agent Skills folder, single skill file. Pin nothing to a tag the maintainer has not created.
- Keep the Edge render honest: a pack that is not fully contracted ships to harnesses only, and the README says so.

## A welcoming first turn

If invoked without a pack, explain the purpose in one or two short sentences and ask for the pack folder.

PT: “Export a Pack monta um pacote distribuível a partir das skills: manifestos, instruções, README, exportações sincronizadas e a entrega para os scripts do repositório. Publicar e marcar versão continuam sendo passos do mantenedor. Indique a pasta do pacote.”

EN: “Export a Pack assembles a distributable pack from its skills: manifests, instructions, README, synchronized exports and the hand-over to the repository scripts. Publishing and tagging remain maintainer steps. Point to the pack folder.”

## Handoffs

Typical chain: Scope a Skill → Draft a Skill → Review a Skill → Test a Skill → Export a Pack. Carry the pack path, files written, and the maintainer hand-over. A suggested handoff has not been executed.
