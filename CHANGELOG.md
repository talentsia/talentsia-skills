# Changelog

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
