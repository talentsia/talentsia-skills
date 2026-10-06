# Changelog

## Talentsia Work 0.1.0

New free pack, released separately from Talentsia Do and tagged `talentsia-work-v0.1.0`. It lets an assistant in Codex or Claude Code hold a seat in a Talentsia organisation. It contains:

- six skills sharing one seat protocol: Connect Seat, Start Work, Deliver Work, Keep Promises, Hand Over and What Needs Me;
- four role agents: Content Designer, Content Writer, Software Engineer and Executive Assistant;
- a standard-library MCP client (15 tools) that signs each request with the seat's own credential;
- `setup_seat.py`, which checks a credential without printing it and writes one Codex or Claude Code agent per seat.

The package carries no organisation content, addresses or keys. Procedures are read live from the organisation's device. Codex loads the plugin from `.codex-plugin/plugin.json`, Claude Code from `.claude-plugin/plugin.json`. Model behaviour and live-workspace behaviour are not run in CI. Artifacts carry SHA-256 checksums and are not yet signed.

## 0.5.1

Clarifies license scope: the original skill content and documentation are CC BY-NC-SA 4.0; repository Python scripts and GitHub Actions code are PolyForm Noncommercial 1.0.0. Adds separate full license texts and a license index. These are source-available noncommercial licenses, not OSI-approved open-source licenses. Business use of the CC-licensed content is not automatically permitted. Prior releases retain the license terms under which they were distributed; this clarification does not revoke previously granted rights.

Corrects stale package-maintenance documentation to reflect the current three-artifact release process and the single `scripts/skill_file.py` generator.

## 0.5.0

**One skill, three artifacts, a license.** Each release now publishes exactly `SKILL-talentsia-do-<version>.md` (the complete pack as one skill file, for attaching to chats or Projects), `talentsia-do-skill-<version>.zip` (the same file as `talentsia-do/SKILL.md` for clients that upload skill ZIPs, such as Claude web/desktop) and `talentsia-do-plugin-<version>.zip` (the native ten-skill plugin). Removed: the ten individual skill ZIPs, the Project reference and Project instructions files, the start text, the pocket ZIP and `scripts/mobile_reference.py` / `scripts/pocket.py`, replaced by `scripts/skill_file.py`. The Project route now uses the skill file itself with a one-sentence Project instruction. Fewer files means one version to track and one thing to replace when updating.

Adds the repository license: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (`LICENSE`, summary in `NOTICE.md`). Use freely, share and adapt with attribution under the same terms, not for sale; premium packs and membership services are offered separately. Replaces earlier “no open-source license is designated” statements.

The ten skills, shared references, plugin manifests, catalog identities and installation commands are unchanged apart from the version. Model behavior and real app behavior remain unexecuted. Prior tags and their assets remain available.

## 0.4.3

The pocket edition now ships the ten skills as one pack file, `SKILL-talentsia-do-<version>.md`: `SKILL.md`-style frontmatter, the shared method, the full instructions of all ten skills, and the review-and-planning and authority references, meant to be attached to a new chat. The per-skill `SKILL-<skill>-*.md` files from 0.4.2 are dropped: the skills hand work to each other and are more useful together. `SKILL-talentsia-do-start-<version>.md` remains as the short pasteable text; Project instructions and reference are unchanged. No skill, reference, manifest or installation change beyond the version.

## 0.4.2

Pocket texts are now shaped and named as skill files: `SKILL-<skill>-<version>.md` and `SKILL-talentsia-do-start-<version>.md`, each opening with `name`/`description` frontmatter like a `SKILL.md`, so assistants recognize an attached file as a skill to follow. Guidance changes from “paste” to “attach one skill file and send the activation sentence, or paste”; the pocket zip is for the website and bulk download and should not be attached to a chat. Motivated by assistant feedback in a 2026-10-05 ChatGPT mobile test: an attached zip was not followed strictly, and a single skill file would have been. Replaces the `talentsia-do-card-*` and `talentsia-do-start-*` names introduced in 0.4.0; no skill, reference, manifest or installation change beyond the version.

## 0.4.1

Pocket texts now open with a short instruction to the assistant to treat the text as operating instructions whether pasted or attached, and the human-facing line includes the activation request to send if the assistant hesitates. Motivated by a 2026-10-05 test on the ChatGPT mobile app (free plan): the start prompt worked when pasted, but when attached as a file the assistant initially treated it as reference material. No skill, reference, manifest or installation change beyond the version.

## 0.4.0

Adds a **pocket edition** for people who cannot install plugins: phone users, ChatGPT plans without a personal marketplace, and any chat client. Three pasteable artifacts are generated from the same canonical source by `scripts/pocket.py`: a start prompt with the shared method and all ten workflows (`talentsia-do-start-<version>.md`), one card per skill (`talentsia-do-card-<skill>-<version>.md`), and Project instructions designed to pair with the existing Project reference file (`talentsia-do-project-instructions-<version>.md`). The release bundles them with the Project reference in `talentsia-do-pocket-<version>.zip` with an `index.json` of sizes and hashes.

Adds `plugins/talentsia-do/pocket/method.md`, a hand-kept compressed form of `references/core.md`; it is a summary for pasting, not a second method, and must be revised with the core. Candidate checks now verify pocket texts against source, enforce character budgets so each stays pasteable, and verify the pocket ZIP contents. Documentation now routes by what the user has in hand (any chat, Project, desktop marketplace, Claude Code, skill upload) instead of asking them to identify a product tier.

The ten skills, shared references, plugin manifests, catalog identities, archive names and installation commands are unchanged apart from the version. Existing installations keep working; sources pinned to earlier tags stay on those versions. No backend, permission expansion, new license, premium content or guaranteed result is introduced. Pasted-text behavior in real apps remains unexecuted.

## 0.3.0

Strengthens the shared method across the same ten skills: novice capture and optional mind sweep; trusted-store bootstrap with verified writes and honest fallbacks; explicit state handoffs; useful contexts, person agendas and bring-forward tied to a real mechanism; context/time/energy filtering before priority; predefined, incoming and defining work; independent executable next actions; guided eleven-function weekly review with coverage gaps; five-step natural planning, six horizons and reference-read failure behavior.

Adds an indexed Project reference and expands synthetic regression fixtures from 32 to 64. Package validation, isolated reference closure and fresh local runtime discovery/source reads were checked on the reviewed candidate. Behavior fixtures and real mobile app behavior remain unexecuted. Version promotion does not imply broader behavioral validation.

Existing records, personal context and external automation remain outside the public package. No backend, permission expansion, new license or guaranteed result is introduced. Prior tags/releases are preserved.

## 0.2.0

Replaces the broad legacy `skills/talentsia-do/SKILL.md` entrypoint with exactly ten skills in the same Talentsia Do plugin. No legacy eleventh skill remains. Names: `clear-my-head`, `organize-my-work`, `plan-my-day`, `move-forward`, `prepare`, `do-with-me`, `follow-through`, `make-room`, `resume`, `review`.

Shared methodology, authority and trusted-record guidance has one canonical source with identical self-contained exports in each skill. Each skill has PT/EN examples, precise triggers and OpenAI UI metadata. Adds synthetic behavior evaluation cases and a dependency-free packaging/structure validator. Release includes one plugin ZIP and ten individual skill ZIPs.

Migration: update the marketplace and plugin, then use natural requests or the new invocation names. Existing records/IDs remain where they are; no data conversion or external action is performed. If the old skill was installed separately by ZIP, it may remain alongside the updated plugin: inspect the new version first, then manually disable/remove that legacy copy to avoid overlapping discovery. Installation-only migration has not been automated.

Marketplace identity `talentsia-skills`, plugin identity `talentsia-do`, website `https://skills.talentsia.com`, sparse-checkout-compatible Git source and Claude compatibility are retained. Earlier tags/releases remain immutable. No new integrations, backend, credentials, payment, premium content or Site download changes.

## 0.1.1

Added the supported OpenAI websiteURL and portable/Claude homepage fields. Synchronized the pinned catalog and package version.

## Initial main catalog correction

Changed the OpenAI catalog from a local path absent in catalog-only sparse checkouts to an independently fetched Git subdirectory.

## 0.1.0

Initial public Talentsia Do plugin and marketplace with a single broad workflow skill.
