# Writing skills for Talentsia Edge workers

Written for: anyone writing a skill that a Talentsia Edge worker installs from
skills.talentsia.com, whether at Talentsia or outside it.

An Edge worker is a resident AI worker on a customer's own device, often on a
small local model such as `qwen3.5:9b`. It installs skills the way a phone
installs apps. A skill is **know-how**: prose a person can read before trusting
it. It never carries code and never grants the worker anything it doesn't
already hold.

Validate before every commit:

```
python3 scripts/check_edge_skills.py
```

---

## 1. A package

```
plugins/<package>/
  talentsia-package.json   name, version, tier, edition, license, the skills it contains
  LICENSE                  MIT
  README.md
  skills/<skill>/
    SKILL.md               the skill, in the open agent-skill format
    skill.json             the machine contract
    agents/<name>.md       subagents, if any
    evals/cases.json       at least three graded cases
```

- Only `.md` and `.json` files are allowed under a package. Code of any kind is
  refused.
- Everything published on skills.talentsia.com is **MIT**, premium included.
  Premium is gated by entitlement, not by license.
- This repository holds the **free, basic edition** of each domain. Enhanced
  editions live in `talentsia-premium-skills`, and replace the basic skill they
  extend.
- **Nothing practice-specific belongs here.** A profession's rules, a market's
  language and register, a jurisdiction, or one client's application all belong
  in premium. One organisation's own way of working is neither: it is that
  organisation's procedure, on its own device.

## 2. SKILL.md

Frontmatter is exactly `name` (equal to the folder) and `description`, a
JSON-quoted string.

The body has these sections, in this order:

```markdown
## When to use
One paragraph: the situation this is for, and when not to use it.

## Steps
1. At most eight, each at most 300 characters, each an act somebody could check.
2. Tools are named as {{tool:<interface>/<operation>}}, never by tool name.
3. A subagent is named as {{agent:<name>}}.

## Done when
- One checkable statement per line. This is the completion contract.

## Notes
- Optional. What a large model benefits from and a small one can do without.
```

Why the shape is fixed:
- **Small models get a compact form.** On a small model the device renders only
  "When to use", "Steps" and "Done when". The entrypoint is capped at about
  1,500 tokens. Today's skills run 200 to 600.
- **Tool references resolve at install.** A `{{tool:…}}` must name an interface
  the skill requires, and an operation that interface defines. The device then
  swaps in the real tool it has installed. A reference with nothing to resolve
  to fails installation; it never fails silently mid-job.
- **Authority stays with the device.** A step that asks for something the worker
  isn't allowed is refused by the device whatever the skill says. Skills can
  only *require*; they never grant.

## 3. skill.json

| Field | Rule |
|---|---|
| `schema` | `talentsia-skill/v1` |
| `id` | `talentsia.<domain>.<folder>` |
| `version` | semver. Patch: wording. Minor: compatible additions. Major: changed requirements, or behaviour a person would notice |
| `status` | `draft` until its evals have run on the tiers it claims, then `released` |
| `publisher`, `tier`, `edition`, `license` | Must match the package |
| `targets` | `edge-worker`, `seat`, `personal` |
| `summary` | Identical to SKILL.md's `description` |
| `appliesTo` | The kinds of work that load it, such as `bookkeeper_document` |
| `requires.capabilities` | Interfaces from [capabilities/v1.json](../capabilities/v1.json), as `name@1` |
| `model` | `minContextTokens`, the `tiers` it claims, and `evals`: its pass rate per model once measured |
| `budget` | Entrypoint tokens, computed by the build |
| `verification` | Identical to the "Done when" lines |
| `reads` | Reference material in the worker's knowledge this skill is carried out against. A filter, never a grant |
| `subagents` | The names of its `agents/*.md` |
| `replaces` | The old skill this supersedes, as `{id, version}` |

## 4. Subagents

A subagent is the same worker thinking in a smaller room. It starts with a fresh
context: its own instructions plus its input, nothing else. That's what lets a 9B
model do a long job as several short, focused calls.

Frontmatter: `name`, `description`, and the following.

| Field | Rule |
|---|---|
| `tools` | A JSON list of `interface/operation`, each among the skill's own interfaces. It only ever narrows, and it may be empty |
| `model` | One of `small-local`, `large-local`, `frontier` |
| `maxSteps` | At most 6 |
| `input` | A JSON object naming each field it receives |
| `output` | A JSON Schema object. The device validates every result against it, and a malformed result is a failed step, never prose to trust |

The body has "Steps" and "Done when".

A subagent cannot start another subagent. It has no identity and no queue; to
hand work to a colleague, use the handoff capability.

## 5. Evals

`evals/cases.json` is `talentsia-skill-evals/v1`, with at least three cases. One
should be the failure the skill exists to prevent, marked `"regression": true`.

```json
{"id": "imported-whole", "title": "A statement is imported, not retyped",
 "given": {"goal": "Work the September statement.",
           "observations": {"ledger.statements.import/import": "53 rows staged"}},
 "expect": {"calls": ["ledger.statements.import/import"], "agents": ["place-rows"],
            "notCalls": [], "says": [], "notSays": []},
 "regression": true}
```

- `observations` are what each tool returns in the case.
- `calls` and `notCalls` name operations.
- `says` and `notSays` are statements a grader checks the answer against. They
  describe meaning, not exact wording.

- An observation keyed by something other than an operation (`document`,
  `brief`, `today`) is what arrived with the job. The harness hands it over as
  the job's opening observation, before the first turn.
- An observation keyed `agent:<name>` is what that subagent returns. Without
  one a subagent returns `{"status": "ok"}`, and an operation the case
  recorded nothing for returns an empty, neutral result.

The harness runs every case on each tier the skill claims. A skill becomes
`released` with its pass rates published in `model.evals`, and the store shows
them. "Can a 9B run this?" is a number an author sees before submitting.

### Running them

```
python3 scripts/eval_edge_skills.py --model qwen3.5:9b --base-url http://<ollama>:11434
python3 scripts/eval_edge_skills.py --package bookkeeping --skill work-a-statement \
    --model llama3.1:8b --tier small-local --json results.json
python3 scripts/eval_edge_skills.py --model qwen3.5:9b --write-results
python3 scripts/eval_edge_skills.py --fake
```

- The skill is rendered as a device renders it: a short runtime preamble, then
  the compact form (When to use, Steps, Done when) for `small-local`, or the
  full form with Notes for `large-local` and `frontier`. `{{tool:a.b/op}}`
  becomes the tool `a_b_op`, and `{{agent:name}}` the tool `agent_name`.
- The worker is offered every operation of every interface the skill
  requires, and one tool per subagent. Arguments are not graded.
- Ollama `/api/chat` at temperature 0, seed 1, `num_ctx` 16384, thinking off,
  at most 8 turns. `--base-url` defaults to `$OLLAMA_BASE_URL`.
- `calls`, `notCalls` and `agents` are graded in code from the calls made.
  `says` and `notSays` are put to a judge model (`--judge-model`, default the
  same model) as one YES/NO question each. A case passes only if every
  expectation holds.
- `--write-results` records each skill's pass rate in skill.json
  `model.evals[<model>]`, rounded to two places. Nothing is written for a
  skill whose run hit a model-server error.
- `--fake` uses a built-in model that calls exactly what each case expects. It
  needs no server and proves the harness and the cases, never a skill: a case
  that fails under it expects something the skill does not offer. CI runs it.
- A skill the validator refuses is not evaluated. Exit status is 0 when every
  case passed, 1 when one failed, 2 when the run could not be trusted.

## 6. Capabilities

[capabilities/v1.json](../capabilities/v1.json) is the vocabulary skills write
against: interfaces such as `ledger.bills.write`, each with named operations.
The value beside each operation is how today's devices bind it, for
reference only; a skill never names it. Adding an interface or operation is a
change to the Edge runtime as well as to this file, so it is proposed, not just
added.
