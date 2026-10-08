# Talentsia Skill Template package instructions

This plugin is a template, not a product. It contains one placeholder skill, a canonical shared method under `references/`, a compressed pocket method, one subagent role template and these instructions. Copy it to start a new pack; do not publish it, list it in a marketplace manifest or treat `template-skill` as a usable workflow. It must never be added to a `talentsia-package.json` or given a `skill.json`, which would route it into the Edge skill validators.

## Layout the new pack keeps

```
plugins/<pack-name>/
  plugin.json                  agent-plugins manifest; version, interface, icon paths
  .claude-plugin/plugin.json   same name, version and homepage
  AGENTS.md                    package instructions for maintainers and assistants
  README.md                    what it is, how to install, limits, license
  LICENSE                      MIT
  assets/<pack-name>.svg       128x128 icon referenced by plugin.json
  references/*.md              canonical shared method; the only place it is edited
  pocket/method.md             hand-kept compressed core, revised with core.md
  agents/<role>.md             optional subagent roles; craft only, no organisational facts
  skills/<skill-name>/
    SKILL.md                   entrypoint; frontmatter name and description only
    agents/openai.yaml         interface block: display_name, short_description, default_prompt
    references/*.md            byte-identical exports of ../../references
```

Each skill explicitly reads a self-contained export, so hosts that expose only one skill folder still get the whole method. Shared references are not skills. The method is one per pack, never one per skill.

## Rules the Do validator enforces, kept here on purpose

- `skills/<name>/SKILL.md` frontmatter has exactly `name` and `description`. `name` equals the folder name and matches `[a-z0-9-]{1,64}`. `description` is a double-quoted JSON string of 1 to 1024 characters that says what the skill does, when to use it, which phrases trigger it in each supported language and which neighbouring skill owns the adjacent case.
- `agents/openai.yaml` starts with `interface:`; `short_description` is 25 to 64 characters; `default_prompt` contains `$<name>`.
- The body contains `[the shared method](references/core.md)` and reads it first.
- Every relative Markdown link in the repository resolves to an existing file; every JSON file parses; no symlinks.
- Exports under each skill's `references/` are byte-identical to the canonical `references/`.

## Editing

Edit only `references/*.md`, then synchronise exports from the repository root:

```
for s in plugins/<pack-name>/skills/*/; do mkdir -p "$s/references"; cp plugins/<pack-name>/references/*.md "$s/references/"; done
diff -r plugins/<pack-name>/references plugins/<pack-name>/skills/<skill-name>/references
```

Adapt `scripts/package.py` for the new pack (plugin path, expected skill names, manifest and marketplace assertions) rather than validate by hand. Revise `pocket/method.md` in the same change whenever `references/core.md` changes meaning; keep it a summary, not a second method.

## Content rules

- Replace every `<placeholder>`; delete a section the pack does not need instead of leaving it generic. Search for `<` before release.
- Keep one multilingual instruction base per skill. Do not fork skills by language.
- Examples describe the shape of an input. No invented people, organisations, addresses, identifiers, dates or figures anywhere in the package, including tests and evals.
- Personal records, organisational facts, credentials and standing rules stay outside the package. Role files carry craft only.
- The human owns decisions; the assistant stewards evidence and records. No skill grants a permission. Say so in the README.
- Keep `SKILL.md` short; the harness loads it on every invocation. Move detail into a conditional reference with a stated trigger in the core's loading table.

## Before distribution

Validate JSON, frontmatter, local references, exact skill discovery count, icons and archive contents. Confirm no `<` placeholder remains, no secret or personal datum is present, and the README names what the pack does not do. Static validation is distinct from model behaviour testing; author synthetic cases under `evals/` and state in the README which were run. Preserve attribution and existing rights.
