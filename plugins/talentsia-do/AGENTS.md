# Talentsia Do package instructions

This free plugin contains exactly ten skills sharing one canonical method under `references/`. Each skill explicitly reads a self-contained export. Read the relevant SKILL.md and shared core before changing workflow. The human decides commitments; the assistant stewards evidence and records.

After editing canonical references, run `python3 scripts/package.py` from repository root to synchronize reference exports and create the plugin archive. Never edit exported reference copies independently. Maintain one bilingual instruction base per skill. `pocket/method.md` is the hand-kept compressed form of `references/core.md` used by `scripts/skill_file.py` for the single skill file; revise it in the same change whenever the core method changes meaning, and keep it a summary rather than a second method. Personal records, contexts, identities and secrets stay outside this package.

Before distribution validate JSON, frontmatter, local references, exact ten-skill discovery, icons and archive contents. Preserve attribution and existing rights. The package includes an optional read-only remote Do MCP connection. No backend implementation, private method source, entitlement, running worker or automatic external actions are supplied. Packaging does not authorize accounts, payments, messages or permission expansion.
