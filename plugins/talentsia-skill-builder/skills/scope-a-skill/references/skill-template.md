# Skill template

The exact skeletons Draft a Skill fills. Replace every `<placeholder>`; delete an optional section the skill does not need instead of leaving it generic. Nothing in these skeletons may be shipped with a `<` left in it.

## SKILL.md

```markdown
---
name: <skill-name>
description: "<What it does and when to use it. Trigger phrases in <language A> and <language B>. Adjacent case: use <neighbouring-skill>.>"
---

# <Skill Display Name>

Read <a Markdown link with text `the shared method` and target `references/core.md`> before proceeding. Apply its identity, language, authority, record and evidence rules. Without storage return a portable record marked **not saved**; without tools distinguish drafts/proposals from performed work.

## When to use

<One paragraph: the situation this is for, and when not to use it.>

## Steps

1. <Read first: {{tool:<interface>/<operation>}}. State what is missing when it is material.>
2. <The core move, as one act with a verb and an object.>
3. <Delegate a bounded part with {{agent:<name>}} if the skill has one; otherwise delete this line and renumber.>
4. <Verify proportionally to the result.>
5. <Record or return the result; name the next step or the decision needed.>

## Done when

- <A checkable statement taken from a tool result or an artifact, not from the shape of the day.>
- <A bound: at most, exactly, never.>
- <The thing the skill exists to prevent did not happen.>

## Notes

- <What a large model benefits from and a small one can do without. Delete the section if empty.>

## A welcoming first turn

If invoked without content, explain the purpose in one or two short sentences and invite the input the skill needs. Do not ask for setup, a destination or a questionnaire before being useful.

<Language A>: “<What this skill helps with and what to send. No names, dates or figures.>”

<Language B>: “<The same, in the other language.>”

## Handoffs

Typical chain in this pack: <skill> → <skill> → <skill>. Carry IDs, evidence, state, proposed and confirmed changes. A suggested handoff has not been executed.
```

## skill.json

```json
{
  "schema": "talentsia-skill/v1",
  "id": "talentsia.<domain>.<skill-name>",
  "version": "0.1.0",
  "status": "draft",
  "publisher": "talentsia",
  "tier": "free",
  "edition": "basic",
  "license": "MIT",
  "targets": ["edge-worker"],
  "summary": "<identical to SKILL.md description>",
  "appliesTo": ["<work_kind>"],
  "requires": {
    "capabilities": ["<interface>@1"],
    "runtime": ">=0.10.0"
  },
  "model": {
    "minContextTokens": 8192,
    "tiers": ["small-local", "frontier"],
    "evals": {}
  },
  "budget": {
    "entrypointTokens": 0,
    "referencesTokens": 0
  },
  "verification": [
    "<identical to each Done when line>"
  ],
  "reads": [],
  "subagents": ["<name>"],
  "replaces": []
}
```

## agents/openai.yaml

```yaml
interface:
  display_name: "<Skill Display Name>"
  short_description: "<25 to 64 characters>"
  default_prompt: "Use $<skill-name> to <one sentence>."
```

## agents/<name>.md

```markdown
---
name: <name>
description: "<What it decides or produces, in one sentence.>"
tools: []
model: small-local
maxSteps: 1
input: {"<field>": "<what it is, in plain words>", "<field>": "<what it is>"}
output: {"type": "object", "required": ["<field>"], "properties": {"<field>": {"type": "<type>"}}}
---

## Steps

1. <One act over the input.>
2. <One bound or exclusion.>

## Done when

- <A statement the device can check against the output schema.>
```

`tools` lists `interface/operation` pairs among the skill's own capabilities, or stays empty. `maxSteps` is at most 6. The output is a JSON Schema object with `required`; a malformed result is a failed step, never prose to trust. A subagent cannot start another subagent.

## evals/cases.json

```json
{
  "schema": "talentsia-skill-evals/v1",
  "skill": "talentsia.<domain>.<skill-name>",
  "cases": [
    {
      "id": "<kebab-id>",
      "title": "<The behaviour, as a sentence>",
      "given": {
        "goal": "<The job as the worker receives it>",
        "observations": {
          "<interface>/<operation>": "<what the tool returns in this case, as shape not data>",
          "agent:<name>": {"<field>": "<what the subagent returns>"}
        }
      },
      "expect": {
        "calls": ["<interface>/<operation>"],
        "notCalls": [],
        "agents": ["<name>"],
        "says": ["<a meaning the answer must convey>"],
        "notSays": ["<a meaning the answer must not convey>"]
      },
      "regression": true
    }
  ]
}
```

At least three cases; one marked `regression` for the failure the skill exists to prevent. Observation keys that are not operations (`document`, `brief`, `today`) are what arrived with the job. Observation values describe the shape of what a tool returns; they never carry names, organisations, dates or figures that could read as real.

## Harness-only files

`references/*.md`: byte-identical copies of the pack's `references/`. `pocket/method.md`: the pack's compressed core. These exist so a host that exposes one skill folder still has the method; a device does not load them.
