# Talentsia Do 0.5.1

Seu multiplicador de produtividade. / Your productivity multiplier.

One free plugin, ten skills, one bilingual method: Clear My Head, Organize My Work, Plan My Day, Move Forward, Prepare, Do With Me, Follow Through, Make Room, Resume and Review.

## Install and choose a skill

No installation available on your device? Each release ships **one skill file**, `SKILL-talentsia-do-<version>.md`, with all ten skills and the shared method: attach it to a new chat and send “Use the attached Talentsia Do skill in this conversation.” See the [repository README](https://github.com/talentsia/talentsia-skills#the-skill-file-one-file-no-installation).

Use the public [Talentsia Skills marketplace](https://github.com/talentsia/talentsia-skills). In ChatGPT desktop, use Add → Marketplace with repo `talentsia/talentsia-skills`, branch `main`, path `.agents/plugins`; update or install Talentsia Do and check version 0.5.1. On a supported Codex CLI, add with `codex plugin marketplace add talentsia/talentsia-skills --ref main --sparse .agents/plugins`.

Claude Code: `claude plugin marketplace add https://github.com/talentsia/talentsia-skills.git#v0.5.1`, then `claude plugin install talentsia-do@talentsia-skills`.

Choose by current need: capture → Clear My Head; clarify inbox → Organize My Work; choose today → Plan My Day; unblock a project → Move Forward; readiness → Prepare; execute → Do With Me; track promised results → Follow Through; reduce overload → Make Room; checkpoint/return → Resume; reconcile the system → Review. Reset composes skills; Someday/Maybe is a state.

Peça em português ou inglês. Exemplos: “Use Clear My Head para capturar estas ideias”; “Use Do With Me para revisar este texto, sem enviar”. In supported Codex clients use `$clear-my-head` or `$review`; in Claude Code use `/talentsia-do:clear-my-head` or `/talentsia-do:review`.

The old `$talentsia-do` skill is replaced, not retained as an eleventh entry. Keep existing record locations, IDs and history. No personal registry or private project is changed by this package.

## Shared records and limits

Each skill reads its `references/core.md`, exported from the same canonical [shared method](references/core.md). Personal context stays in the user's own storage. Installation supplies no storage backend, connected accounts, running agent or future monitor. With no storage, output is a portable record marked not saved. Human authority controls commitments and external actions.

Test the included PT/EN examples with synthetic inputs after installation. Manifest/structure validation is distinct from model behavior testing.

See [methodology sources](references/methodology-sources.md). This is an independent implementation; no endorsement or guaranteed result is claimed. © 2026 Talentsia. Talentsia Do is licensed under the [MIT License](LICENSE); business use is allowed. Names and logos are not licensed. Third-party rights remain with their owners.

## Verification limits

The release contains 64 synthetic behavior fixtures. Static package/reference/archive/skill-file checks passed. Model behavior fixtures and real app behavior remain unexecuted. A successful installation or source read does not prove the model applied the instructions.

Connected Premium source pilot: the same plugin can route Plan My Day through current entitlement checks when the existing host exposes the confirmed tools. [Routing](references/connected-premium.md). Free remains usable without a connection. This source candidate does not configure a live Premium service.
