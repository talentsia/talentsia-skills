# The skill contract

What a Talentsia skill is and the rules a validator applies to it. A skill is know-how: prose a person can read before trusting it. It carries no code and grants nothing the worker does not already hold. One source shape serves two destinations: an LLM harness plugin (Codex, ChatGPT, Claude Code, any Agent Skills host) and a Talentsia Edge device or seat.

## Package layout

```
plugins/<pack>/
  plugin.json                  harness manifest: name, version, interface, icon
  .claude-plugin/plugin.json   same name, version, homepage
  talentsia-package.json       Edge catalog: name, version, tier, edition, license, skills   (Edge target only)
  AGENTS.md                    package instructions
  README.md                    what it is, install, limits, what it will not do, license
  LICENSE                      MIT
  assets/<pack>.svg            128x128 icon
  references/*.md              the pack's shared method; the only place it is edited
  pocket/method.md             compressed core for a single-file distribution
  skills/<skill>/
    SKILL.md                   the entrypoint
    skill.json                 the machine contract
    agents/openai.yaml         harness interface block
    agents/<name>.md           subagents, if any
    evals/cases.json           at least three graded cases
    references/*.md            byte-identical exports of ../../references   (harness target only)
```

Only `.md` and `.json` under a skill folder (`openai.yaml` is the one harness exception and is not shipped to a device). No symlinks. Every relative Markdown link resolves. Every JSON file parses.

## SKILL.md

Frontmatter is exactly two fields:

```
---
name: <folder-name>
description: "<JSON-quoted string, 1 to 1024 characters>"
---
```

`name` equals the folder and matches `[a-z0-9-]{1,64}`. `description` says what the skill does, when to use it, which phrases trigger it in each supported language, and which neighbouring skill owns the adjacent case. A host routes on this line alone.

Body, in this order:

| Section | Rule |
| --- | --- |
| first paragraph | `Read `, then a Markdown link whose text is exactly `the shared method` and whose target is exactly `references/core.md`, then ` before proceeding.` and the pack's one-line boundary statement (harness target). The Do validator matches this link byte for byte |
| `## When to use` | One paragraph: the situation, and when not to use it |
| `## Steps` | Numbered `1.` to `n.`, at most eight, each at most 300 characters, each an act somebody could check. Tools as `{{tool:<interface>/<operation>}}`, never a tool name. Subagents as `{{agent:<name>}}` |
| `## Done when` | One checkable statement per `- ` line. This is the completion contract and is copied verbatim into `skill.json.verification` |
| `## Notes` | Optional. What a large model benefits from and a small one can do without |

On a small model a device renders only When to use, Steps and Done when. Entrypoint budget: about 1,500 tokens; good skills run 200 to 600. No `## ` heading appears twice.

A harness plugin may add, after Notes: `## A welcoming first turn` (what to say when invoked with no content, in each supported language) and `## Handoffs` (the chain in the pack). A device ignores them.

## skill.json

| Field | Rule |
| --- | --- |
| `schema` | `talentsia-skill/v1` |
| `id` | `talentsia.<domain>.<folder>` |
| `version` | semver. Patch: wording. Minor: compatible additions. Major: changed requirements or behaviour a person would notice |
| `status` | `draft` until evals have run on the tiers it claims; then `released`. The builder writes only `draft` |
| `publisher`, `tier`, `edition`, `license` | Match the package: `talentsia`, `free`, `basic`, `MIT` for this repository |
| `targets` | Any of `edge-worker`, `seat`, `personal` |
| `summary` | Identical to SKILL.md `description` |
| `appliesTo` | Kinds of work that load it, `[a-z][a-z0-9_]{1,63}` |
| `requires.capabilities` | Interfaces from the capability vocabulary as `name@1`; `requires.runtime` as a semver range |
| `model` | `minContextTokens`, `tiers` claimed from `small-local`, `large-local`, `frontier`, and `evals` (empty object until measured) |
| `budget` | `entrypointTokens`, `referencesTokens`; computed by the build, write a rough estimate |
| `verification` | Identical to the Done when lines |
| `reads` | Reference material in the worker's knowledge the skill is carried out against. A filter, never a grant. Usually `[]` |
| `subagents` | Names of `agents/<name>.md` |
| `replaces` | `[{"id": "<old-kind>", "version": <n>}]` or `[]` |

## agents/openai.yaml (harness target)

```
interface:
  display_name: "<Skill Display Name>"
  short_description: "<25 to 64 characters>"
  default_prompt: "Use $<name> to <one sentence>."
```

## Authority rules the contract encodes

A step that asks for something the worker is not allowed to do is refused by the device whatever the skill says. A `{{tool:…}}` must name an interface the skill requires and an operation the vocabulary defines; one that cannot resolve fails installation, never silently mid-job. Nothing practice-specific belongs in a basic skill: a profession's rules, a jurisdiction, one client's application, one organisation's procedure. Everything published is MIT; premium is gated by entitlement, not license.

## Versioning and status

Patch for wording, minor for compatible additions, major when requirements or noticeable behaviour change. A skill moves to `released` when, on the small local reference model, it passes at least two thirds of its cases, every `regression` case passes, no case hit a server error, and it claims `small-local`. Only the eval harness writes `model.evals`; only the maintainer flips `status`.
