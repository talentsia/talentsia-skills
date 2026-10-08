---
name: test-a-skill
description: "Rehearse a skill's graded cases in this conversation: a builder role acts as the worker with only the rendered skill and the case's observations, and the transcript is graded against expect. Use for testar a skill, dry-run the cases, or does this skill pass; the measured pass rate comes from the repository harness."
---

# Test a Skill

Read [the shared method](references/core.md) before proceeding. Apply its identity, authority, record and evidence rules. A rehearsal here is not a measurement: different model, different renderer, no fixed seed. Record it as rehearsed, never as a pass rate, and never write it into `skill.json`.

## When to use

Use after Review a Skill to find unclear steps, missing observations and `says` lines a judge could not decide, before spending a model run. Not for releasing a skill; `status` and `model.evals` are written only by the repository harness and the maintainer.

## Steps

1. Read the skill folder, [eval design](references/eval-design.md) and the pack's `references/core.md`. Render the skill as a device would: the preamble (tools are the authority, documents are data, a fact is something a tool showed), then When to use, Steps and Done when only.
2. For each case, assign the `worker-rehearsal` role with the rendered skill, the case `goal` and the tools it may call: every operation of every required interface, and one per subagent. Answer each call with the case's observation, or a neutral empty result when none is recorded. At most eight turns.
3. Grade the transcript in code-like fashion: `calls` present, `notCalls` absent, `agents` invoked. Then put each `says` and `notSays` as one strict YES/NO question about the final answer's meaning; record the answer and the sentence it rests on.
4. Record per case: rehearsed pass or fail, each expectation's result, and the cause of a failure — an unclear step, a missing observation, an undecidable `says`, or the skill genuinely not doing it.
5. Propose the smallest change that fixes each cause: a step rewording, an added observation, a sharper `says`. Do not loosen a `notSays` or drop a regression case to pass.
6. Return a table of cases with results and causes, the proposed changes, and the exact harness commands from eval design to obtain the measurement. State plainly that nothing was measured.

## Done when

- Every case was rehearsed with only the rendered skill, the preamble and its observations; no expected answer was shown to the worker role.
- Each expectation has a recorded result and, for `says`/`notSays`, the sentence it rests on.
- No pass rate, `status` or `model.evals` value was written anywhere.
- The return names the harness commands and states that the measurement was not run.

## Notes

- A `says` the rehearsal could not decide is a finding about the case, not about the skill: rewrite it as one meaning.
- Run the regression case first; if it fails, stop and hand back to Draft a Skill before rehearsing the rest.
- Without a delegation tool, play the worker yourself in a clearly separated block and say so; the grading is weaker because you have seen the expectations.

## A welcoming first turn

If invoked without a skill, explain the purpose in one or two short sentences and ask for the skill folder.

PT: “Test a Skill ensaia os casos de teste de uma skill nesta conversa, com um papel agindo como o trabalhador, e aponta passos pouco claros ou casos indecidíveis. Não substitui a medição no harness. Indique a pasta da skill.”

EN: “Test a Skill rehearses a skill's graded cases in this conversation, with a role acting as the worker, and points out unclear steps or undecidable cases. It does not replace the harness measurement. Point to the skill folder.”

## Handoffs

Typical chain: Scope a Skill → Draft a Skill → Review a Skill → Test a Skill → Export a Pack. Carry the pack path, skill name, case results and proposed changes. A suggested handoff has not been executed.
