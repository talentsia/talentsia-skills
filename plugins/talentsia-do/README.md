# Talentsia Do 0.4.3

Seu multiplicador de produtividade. / Your productivity multiplier.

One free plugin, ten skills, one bilingual method: Clear My Head, Organize My Work, Plan My Day, Move Forward, Prepare, Do With Me, Follow Through, Make Room, Resume and Review.

## Install and choose a skill

No installation available on your device? The release ships a **pocket edition**: pasteable texts (a start prompt, one card per skill, and Project instructions with a reference file) generated from this same source. See the [repository README](https://github.com/talentsia/talentsia-skills#pocket-edition-paste-no-installation).

Use the public [Talentsia Skills marketplace](https://github.com/talentsia/talentsia-skills). In ChatGPT desktop, use Add → Marketplace with repo `talentsia/talentsia-skills`, branch `main`, path `.agents/plugins`; update or install Talentsia Do and check version 0.4.3. On a supported Codex CLI, add with `codex plugin marketplace add talentsia/talentsia-skills --ref main --sparse .agents/plugins`.

Claude Code: `claude plugin marketplace add https://github.com/talentsia/talentsia-skills.git#v0.4.3`, then `claude plugin install talentsia-do@talentsia-skills`.

Choose by current need: capture → Clear My Head; clarify inbox → Organize My Work; choose today → Plan My Day; unblock a project → Move Forward; readiness → Prepare; execute → Do With Me; track promised results → Follow Through; reduce overload → Make Room; checkpoint/return → Resume; reconcile the system → Review. Reset composes skills; Someday/Maybe is a state.

Peça em português ou inglês. Exemplos: “Use Clear My Head para capturar estas ideias”; “Use Do With Me para revisar este texto, sem enviar”. In supported Codex clients use `$clear-my-head` or `$review`; in Claude Code use `/talentsia-do:clear-my-head` or `/talentsia-do:review`.

The old `$talentsia-do` skill is replaced, not retained as an eleventh entry. Keep existing record locations, IDs and history. No personal registry or private project is changed by this package.

## Shared records and limits

Each skill reads its `references/core.md`, exported from the same canonical [shared method](references/core.md). Personal context stays in the user's own storage. Installation supplies no storage backend, connected accounts, running agent or future monitor. With no storage, output is a portable record marked not saved. Human authority controls commitments and external actions.

Test the included PT/EN examples with synthetic inputs after installation. Manifest/structure validation is distinct from model behavior testing.

See [methodology sources](references/methodology-sources.md). This is an independent implementation; no endorsement or guaranteed result is claimed. No open-source license is designated; copyright and third-party rights remain with their owners.

## Verification limits

The release contains 64 synthetic behavior fixtures. Static package/reference/archive/pocket checks passed. Model behavior fixtures, real mobile app behavior and pasted pocket-text behavior remain unexecuted. A successful installation or source read does not prove the model applied the instructions.
