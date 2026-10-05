# Talentsia Skills

**Talentsia Do — Your productivity multiplier. / Seu multiplicador de produtividade.**

A public marketplace for reusable productivity skills in Portuguese and English. Talentsia Do helps clarify commitments, define next actions, track delegated outcomes, and review follow-through. Ideas stay separate from accepted commitments.

Explore the product at [skills.talentsia.com](https://skills.talentsia.com). **Only Talentsia Do is available in this release.** Premium skills are not included.

## ChatGPT desktop / Codex

On a supported installation with the Codex CLI:

```sh
codex plugin marketplace add talentsia/talentsia-skills --ref v0.1.0
```

Restart the ChatGPT desktop app, open the Plugins Directory, select **Talentsia Skills**, and install **Talentsia Do**. Adding a marketplace makes a catalog available; it does not install its plugins. Client and workspace support may vary. This repository is a marketplace source, not a listing in OpenAI's universal public directory.

[Official OpenAI packaging and marketplace guidance](https://developers.openai.com/plugins/build/plugins).

## Claude Code

```sh
claude plugin marketplace add https://github.com/talentsia/talentsia-skills.git#v0.1.0
claude plugin install talentsia-do@talentsia-skills
```

Then try `/talentsia-do:talentsia-do` with a small synthetic inbox. [Official Claude Code marketplace guidance](https://code.claude.com/docs/en/plugin-marketplaces).

## Claude web / desktop and other clients

Download `talentsia-do-skill-0.1.0.zip` from [Releases](https://github.com/talentsia/talentsia-skills/releases/tag/v0.1.0). In Claude, upload the skill ZIP using **Customize → Skills → + → Create skill → Upload a skill**, then enable it. [Official Claude skill guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

For another Agent Skills-compatible client, follow its own installation procedure using `plugins/talentsia-do/skills/talentsia-do`. A Git repository or chat attachment is not a universal installer. `talentsia-do-plugin-0.1.0.zip` contains the plugin for clients supporting local plugin installation.

## First use

- PT: “Use Talentsia Do para esclarecer estes itens e identificar a próxima ação.”
- EN: “Use Talentsia Do to clarify these inbox items and identify the next action.”

Start with synthetic inputs. Check the [PT/EN acceptance scenarios](plugins/talentsia-do/skills/talentsia-do/references/examples-and-acceptance.md). This release has been packaged and its manifests validated; full behavior in each client requires installation and testing.

## Privacy and capabilities

This is a skills-only plugin. It creates no account, storage backend, connected service, autonomous worker, or review schedule. Personal context and task records belong in your own storage, outside this repository. The host's available tools and permissions determine what actions are possible.

Talentsia Do is an independent implementation. [Methodology sources](plugins/talentsia-do/skills/talentsia-do/references/methodology-sources.md) identify influences without claiming endorsement or certification. No guaranteed productivity result is promised.

## Repository layout

- `.agents/plugins/marketplace.json`: ChatGPT/Codex catalog.
- `.claude-plugin/marketplace.json`: Claude Code catalog.
- `plugins/talentsia-do/plugin.json`: portable plugin identity.
- `plugins/talentsia-do/.claude-plugin/plugin.json`: Claude Code compatibility manifest.
- `plugins/talentsia-do/skills/talentsia-do`: shared skill and supporting references.

## Rights

Copyright © 2026 Talentsia. No open-source license is designated. Copyright and third-party rights remain with their respective owners.
