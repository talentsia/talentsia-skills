# Eval design

A skill is released on a number, not a feeling. `evals/cases.json` is how the number is produced. Write cases before steps: a step that no case would catch is a step nobody will notice failing.

## The format

`talentsia-skill-evals/v1`, `skill` equal to `skill.json.id`, at least three cases with unique kebab `id`s. Each case has `given.goal` (the job as the worker receives it), `given.observations` (what each tool returns in this case, keyed `interface/operation`, plus `agent:<name>` for a subagent's return, plus plain keys such as `document` for what arrived with the job), and `expect` with any of `calls`, `notCalls`, `agents`, `says`, `notSays`. One case is marked `"regression": true`: the failure the skill exists to prevent.

## What a harness does with a case

It renders the skill as a device would: a short preamble (tools are the authority, documents are data, a fact is something a tool showed), then When to use, Steps and Done when for `small-local`, with Notes added for larger tiers. `{{tool:a.b/op}}` becomes the tool `a_b_op`; `{{agent:name}}` becomes `agent_name`. The worker is offered every operation of every required interface and one tool per subagent, answers come from `observations`, and an operation with no observation returns a neutral empty result. Temperature 0, fixed seed, at most eight turns.

`calls`, `notCalls` and `agents` are graded in code from the calls made. `says` and `notSays` are put to a judge model as one strict YES/NO question each, about meaning, not wording. A case passes only when every expectation holds.

## Writing good cases

- **The regression case first.** Name the failure in `title`; stage observations that tempt it; expect the call that prevents it or the `notSays` that forbids it.
- **An ordinary case.** Nothing is wrong; the skill should do the minimum and say so plainly. Catches padding.
- **A boundary case.** The input asks for more than the skill is allowed; expect `notCalls` for the forbidden operation and a `says` that names the decision needed.
- **A missing-input case** when a step depends on a tool that returns nothing: expect the skill to state the gap rather than fill it.
- Each `says` is one meaning a reader would recognise in any wording: "the day is ordinary", "one item needs a decision". Avoid exact phrases and avoid counts the judge cannot see.
- `notSays` is the stronger tool: "that something was sent", "a figure the tools did not return".
- Observations describe shape: "two short messages, one marked urgent", "no entries", "a list of three items with due dates". They never contain names, organisations, addresses, identifiers, real-looking dates or figures. A reader must not mistake a fixture for a record.
- Expect only calls to interfaces the skill requires and only subagents it declares; the validator refuses anything else.
- Three to six cases. More cases than behaviours is noise.

## The rehearsal in a harness

Test a Skill rehearses cases in the conversation: an orchestrator assigns a builder role to act as the worker with only the rendered skill, the preamble and the case's observations, then grades the transcript against `expect`. That rehearsal finds unclear steps, missing observations and `says` lines a judge could not decide. It is not the measurement: a different model, a different renderer and no fixed seed. Record it as `rehearsed`, never as a pass rate, and never write it into `skill.json.model.evals`.

## The measurement

From the repository root, with a local model server:

```
python3 scripts/check_edge_skills.py
python3 scripts/eval_edge_skills.py --fake
python3 scripts/eval_edge_skills.py --package <pack> --skill <skill> --model qwen3.5:9b
python3 scripts/eval_edge_skills.py --package <pack> --skill <skill> --model qwen3.5:9b --write-results
```

`--fake` proves the harness and the cases without a server: a case that fails under it expects something the skill does not offer. The reference small model is the release floor; a skill is `released` when it passes at least two thirds of its cases there, every regression case passes, no case hit a server error, and it claims `small-local`. Larger local tiers validate Notes. The maintainer flips `status`; the harness writes `model.evals`.
