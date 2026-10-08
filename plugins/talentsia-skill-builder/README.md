# Talentsia Skill Builder 0.1.0

Make skills the way Talentsia makes them. One free plugin, five skills, one method: Scope a Skill, Draft a Skill, Review a Skill, Test a Skill and Export a Pack. Six builder roles do the bounded parts as subagents. Eight references carry the skill contract, the template, the subagent and eval contracts, the capability vocabulary, the review checklist and the export layout, so the builder works from the same text a validator applies.

## What is in it

| Path | Purpose |
| --- | --- |
| `skills/scope-a-skill` | Agree when a skill applies, what done looks like, the failure it prevents, capabilities and subagents |
| `skills/draft-a-skill` | Write SKILL.md, skill.json, subagents, graded cases and harness metadata from the template, with the case-author, step-writer and contract-checker roles |
| `skills/review-a-skill` | Quote contract and checklist findings with fixes, with the contract-checker and red-team-reviewer roles |
| `skills/test-a-skill` | Rehearse graded cases in the conversation with the worker-rehearsal role; a rehearsal, never a pass rate |
| `skills/export-a-pack` | Assemble manifests, package instructions, README, exports and the hand-over to the repository scripts, with the pack-assembler role |
| [references/](references/core.md) | The material fed to every step: [skill contract](references/skill-contract.md), [template](references/skill-template.md), [subagent contract](references/subagent-contract.md), [eval design](references/eval-design.md), [capabilities](references/capabilities.md), [review checklist](references/review-checklist.md), [export layout](references/export-layout.md) |
| [agents/](agents/case-author.md) | The six builder roles: case-author, step-writer, contract-checker, red-team-reviewer, worker-rehearsal, pack-assembler |
| [pocket/method.md](pocket/method.md) | Compressed method for a single-file distribution |

## Install

The plugin follows the same layout as Talentsia Do and installs the same way once listed. Until it is listed and tagged, install from the plugin ZIP that `python3 scripts/package_builder.py --output /tmp/talentsia-skill-builder-release` writes, or point a host at `plugins/talentsia-skill-builder` in a checkout. ChatGPT desktop and Codex read `plugin.json` and each skill's `agents/openai.yaml`; Claude Code reads `.claude-plugin/plugin.json`; any Agent Skills host can use a `skills/<name>` folder, which carries its own reference exports.

In supported Codex clients use `$scope-a-skill`, `$draft-a-skill`, `$review-a-skill`, `$test-a-skill`, `$export-a-pack`; in Claude Code use `/talentsia-skill-builder:<name>`. Peça em português ou inglês.

## Make a skill

1. Describe the work to Scope a Skill: what it is, who does it now, what goes wrong. Agree the failure to prevent and the Done when lines.
2. Draft a Skill writes the files into the pack folder you designate, cases first, then steps, then the rest, and checks them against the contract.
3. Review a Skill returns quoted findings from two independent reviewers; apply what you authorize.
4. Test a Skill rehearses the cases in the conversation and tells you which steps or cases are unclear.
5. Export a Pack assembles the pack and hands over the validation and packaging commands.
6. Measure, from the repository: `python3 scripts/check_edge_skills.py`, `python3 scripts/eval_edge_skills.py --fake`, then `--model qwen3.5:9b` on a local model server. The maintainer flips `status` and the harness writes the pass rate.

The builder works from the same template as [talentsia-skill-template](../talentsia-skill-template/README.md), carried inside its references so a harness needs nothing else.

## Testing in ChatGPT

Test a Skill renders the skill as a device would and assigns a role to act as the worker, answering its tool calls with the case's observations, then grades the transcript against the case's expectations. This finds unclear steps, missing observations and undecidable `says` lines before a model run. It is not the measurement: a different model, a different renderer, no fixed seed. The builder records it as rehearsed and never writes it into `skill.json`.

## What it will not do

It performs none of the work a produced skill describes. It writes only into the pack folder you designate and returns files marked not saved when none is designated. It does not run network calls, build archives, create tags, edit marketplace manifests, publish, or mark a skill released. It grants no permission and writes none into a skill. It never invents people, organisations, dates or figures, and refuses to carry an organisation's procedures, credentials or personal data into a skill.

## License and verification limits

Static package checks cover manifests, frontmatter, roles, links and exports. The builder's own behaviour on a model is unmeasured; a produced skill's behaviour is unmeasured until the repository harness runs it. © 2026 Talentsia. Licensed under the [MIT License](LICENSE); business use is allowed. Names and logos are not licensed. Third-party rights remain with their owners.
