# Export layout

How Export a Pack assembles a distributable from the skills in a pack. The builder writes files into the designated pack folder; building archives, tagging, attesting and publishing are maintainer steps performed by the repository's scripts and listed here so the builder can hand them over exactly.

## One source, two renders

The pack folder is the source. Two renders are produced from it without editing the skills by hand.

**Harness render** (Codex, ChatGPT desktop, Claude Code, Agent Skills hosts, single skill file):

- `plugin.json` with `extensions.com.openai.interface`, `logo` and `composerIcon` pointing to `assets/<pack>.svg`, `websiteURL` and `homepage` set to the pack's site.
- `.claude-plugin/plugin.json` with the same `name`, `version`, `homepage`.
- `skills/<skill>/agents/openai.yaml` for every skill.
- `skills/<skill>/references/*.md` byte-identical to `references/*.md`.
- `pocket/method.md` kept in step with `references/core.md`.
- `{{tool:a.b/op}}` read as "the host's tool for `a.b` `op`, if available"; `{{agent:name}}` read as "assign the `name` role, or perform it sequentially".

**Edge render** (Talentsia Edge devices and seats, skills.talentsia.com):

- `talentsia-package.json`: `schema` `talentsia-package/v1`, `name`, `version`, `publisher`, `tier`, `edition`, `license`, `targets`, `description`, `skills` listing every folder.
- `skills/<skill>/skill.json` with `budget.entrypointTokens` computed from When to use + Steps + Done when.
- Only `.md` and `.json`; `openai.yaml` and `references/` exports are not loaded by a device and may be omitted from the device archive.

Adding `talentsia-package.json` routes the pack into the Edge validators; add it only when every skill in the pack carries `skill.json` and `evals/cases.json`.

## Pack-level files

| File | Content |
| --- | --- |
| `AGENTS.md` | Layout, how exports are synchronised, what the validators enforce, content rules, release checklist |
| `README.md` | Version, what is in it, install per host, how to choose a skill, limits, **what it will not do**, license |
| `LICENSE` | MIT |
| `assets/<pack>.svg` | 128x128 |
| `references/` | The pack's method; `core.md` always, others with a stated load trigger |
| `pocket/method.md` | Compressed `core.md` for the single-file distribution |

## Synchronise exports

From the repository root:

```
for s in plugins/<pack>/skills/*/; do mkdir -p "$s/references"; cp plugins/<pack>/references/*.md "$s/references/"; done
```

Then confirm: `diff -r plugins/<pack>/references plugins/<pack>/skills/<skill>/references` for each skill.

## Validate

```
python3 scripts/check_edge_skills.py          # Edge contract, when talentsia-package.json exists
python3 scripts/eval_edge_skills.py --fake    # harness and cases, no model
python3 scripts/package.py --output /tmp/out  # repo-wide links and JSON; Do plugin build
```

A pack with its own packaging script follows `scripts/package.py`: validate manifests, frontmatter, exports, icons and links; write the ZIP outside the repository; refuse symlinks, absolute paths, `..`, `.git`, `.env`, `.sqlite`, `.pem`.

## Distributables

| Destination | Artifact | Produced by |
| --- | --- | --- |
| ChatGPT desktop / Codex marketplace | entry in `.agents/plugins/marketplace.json` pinned to a tag | maintainer, at release |
| Claude Code marketplace | entry in `.claude-plugin/marketplace.json` | maintainer, at release |
| Plugin ZIP | `<pack>-plugin-<version>.zip` of the pack folder | packaging script |
| Single skill file | `SKILL-<pack>-<version>.md` from `pocket/method.md` and the skills | `scripts/skill_file.py` pattern |
| Edge device | the pack folder under a release tag, read by skills.talentsia.com | maintainer, after evals |

A release ships a fixed set of artifacts with `SHA256SUMS` and a validation report. Never upload a locally rebuilt ZIP over a CI artifact.

## Hand-over from the builder

Export a Pack ends by returning: the file tree written, the validation commands to run, the marketplace entries to add (as text, not written), the release tag name to use, and `What I could not establish`, which always includes: no model pass rate measured; manifests not yet pinned to a tag; no archive built.
