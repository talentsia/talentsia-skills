# Changelog

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
