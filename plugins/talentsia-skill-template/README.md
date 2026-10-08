# Talentsia Skill Template 0.1.0

A starting point for new Talentsia skill packs. It shows the structure that Talentsia Do uses — one shared method, self-contained exports per skill, explicit human authority, bounded subagents — without any of Do's workflows. It performs no work, stores nothing, connects to nothing and is not listed in any marketplace.

## What is in it

| Path | Purpose |
| --- | --- |
| [plugin.json](plugin.json) and [.claude-plugin/plugin.json](.claude-plugin/plugin.json) | Manifests for the two harness families; same name, version and homepage |
| [AGENTS.md](AGENTS.md) | Package instructions: layout, validator rules, sync command, content rules, release checklist |
| [references/core.md](references/core.md) | The shared method: how the harness reads the package, identity, authority and guardrails, organizational context, one trusted record, filters, subagents, output contract, handoffs, failure handling |
| [references/operating-instructions.md](references/operating-instructions.md) | Owner, steward and specialist roles; delegation and authority |
| [references/subagents.md](references/subagents.md) | When to delegate, the assignment brief, the return contract, orchestrator duties |
| [references/organizational-context.md](references/organizational-context.md) | Where context comes from, what to resolve, what stays outside the package |
| [references/methodology-sources.md](references/methodology-sources.md) | Attribution and licensing statement |
| [pocket/method.md](pocket/method.md) | Compressed core for a single-file distribution; revised with core.md |
| [agents/role-template.md](agents/role-template.md) | Layout for a reusable subagent role |
| [skills/template-skill/SKILL.md](skills/template-skill/SKILL.md) | The skill entrypoint layout, with its interface metadata and reference exports |

## Start a new pack

The quickest route is the [Talentsia Skill Builder](../talentsia-skill-builder/README.md), whose skills scope, draft, review, rehearse and export packs in this layout from inside a harness. By hand:

1. Copy `plugins/talentsia-skill-template` to `plugins/<pack-name>`. Rename the icon and update both manifests: `name`, `version`, `description`, `displayName`, `shortDescription`, `longDescription`, `defaultPrompt`, `logo`, `composerIcon`.
2. Write the pack's method in `references/core.md` first. Fill identity, authority, filters and hard limits; delete what the domain does not need. Revise `pocket/method.md` to match.
3. Rename `skills/template-skill` to the first skill. One folder per skill; name equals folder; frontmatter has `name` and `description` only. Fill `agents/openai.yaml`.
4. Add roles under `agents/` only if a skill delegates. Roles carry craft; organisational facts arrive at run time.
5. Synchronise exports with the command in [AGENTS.md](AGENTS.md); adapt `scripts/package.py` for the new pack; author synthetic cases under `evals/`.
6. Search the pack for `<` and remove every placeholder. Write the README's "what it will not do" section before the install section.

## Principles the template encodes

Progressive disclosure: `SKILL.md` is short and always loaded; the core is loaded once; every other reference has a stated trigger. Instructions are the package; everything else is data. The human owns decisions and external actions; the assistant stewards evidence and records and holds no hidden permission. One trusted record shared by every skill, never a registry per skill; without storage, a portable record marked not saved. Subagents receive exact inputs, exact references, read-only authority and done criteria, and their returns are verified before they change anything. Organisational context is resolved from the environment each time and never embedded. Examples describe the shape of an input and never invent people, organisations or data.

## What it will not do

It is not installable as a working pack and `template-skill` is not a workflow. Copying it creates no storage backend, connected account, running agent, schedule or permission. It is not referenced by the marketplace manifests or by any release script, and must not be given a `talentsia-package.json` or `skill.json`.

© 2026 Talentsia. Licensed under the [MIT License](LICENSE); business use is allowed. Names and logos are not licensed. Third-party rights remain with their owners.
