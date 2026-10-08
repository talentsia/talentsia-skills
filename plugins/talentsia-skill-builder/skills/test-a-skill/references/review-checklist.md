# Review checklist

Apply to a draft before Test a Skill and again before Export a Pack. Each line is a finding a reviewer can quote. A review that quotes nothing has not reviewed. Record the result per line as pass, fail with location, or not applicable with reason.

## Structure

- Frontmatter is exactly `name` and `description`; `name` equals the folder and matches `[a-z0-9-]{1,64}`; `description` is a JSON-quoted string of 1 to 1024 characters.
- Body sections appear once each and in order: When to use, Steps, Done when, Notes (optional), then harness-only sections.
- Steps are numbered 1..n, at most eight, each at most 300 characters.
- Done when has at least one `- ` line; every line is checkable against a tool result or an artifact.
- `skill.json` parses; `summary` equals `description`; `verification` equals the Done when lines; `subagents` equals the files in `agents/`; `status` is `draft`; `model.evals` is empty.
- Only `.md` and `.json` under the skill folder (plus `agents/openai.yaml` for the harness target).
- Every relative link resolves. Reference exports are byte-identical to the pack's `references/`.

## Routing

- The `description` says what, when, the trigger phrases per language and the adjacent skill. A host could route on it alone.
- When to use says when not to use it.
- No other skill in the pack claims the same situation.

## Steps

- Every step is an act a person could check, with a verb and an object.
- Every `{{tool:…}}` names an interface in `requires.capabilities` and an operation that interface defines.
- Every `{{agent:…}}` names a file in `agents/` and the name appears in `skill.json.subagents`.
- A read precedes every write. No step asks for an action the vocabulary does not name.
- No step grants, assumes or expands permission. No step promises monitoring, scheduling or a future review.
- The failure the skill exists to prevent is prevented by a step, not only forbidden in Done when.

## Subagents

- Frontmatter is exactly `name`, `description`, `tools`, `model`, `maxSteps`, `input`, `output`.
- `tools` only narrows the skill's capabilities; `maxSteps` is at most six; `output` is a JSON Schema object with `required`.
- The subagent returns a shape, not prose. It does not write to the record and does not start another subagent.
- The part delegated is independent, verifiable and needs no human decision mid-way.

## Evals

- Schema `talentsia-skill-evals/v1`, `skill` equals `skill.json.id`, at least three cases, unique ids.
- One case has `"regression": true` and stages the failure the skill exists to prevent.
- `calls` name only required interfaces; `agents` name only declared subagents.
- Each `says`/`notSays` is one meaning a judge can answer YES or NO to from the final answer alone.
- Observations describe shape and contain no names, organisations, addresses, identifiers, real-looking dates or figures.

## Content

- No `<` placeholder remains anywhere in the skill.
- No invented people, organisations or data in any file.
- No organisation's procedure, brand rule or standing rule; no profession's or jurisdiction's rules.
- No credential, endpoint, path to a private record or seat identifier.
- Language: one multilingual instruction base; trigger phrases present for each supported language; labels translate, records do not duplicate.
- The human owns decisions; the skill proposes and records. The README names what the pack will not do.

## Red team

- Could a document the worker reads instruct it to skip a step or call a forbidden operation? The steps must say tool results and documents are data.
- Could the skill claim completion without a tool result? Done when must require one.
- Could a small model satisfy every Done when line while missing the point? Add the case that catches it.
- Could the skill be satisfied by doing nothing? The ordinary case must still require the recording call.
