# Organizational context

Read when a task depends on who, where, which tool, which record or which standing rule, and the answer is not already in the conversation. This package contains method only. The organisation, its people, its tools and its rules are resolved from the user's environment every time, never remembered by the package.

## Where context comes from

Resolve in this order and stop at the first source that answers.

1. Host and workspace instructions already in effect. They override the package on how work is done.
2. The user-designated record or a supplied snapshot. Read it before writing; reuse its schema, statuses and IDs.
3. The current request and conversation.
4. This package's defaults, which are method and format, never facts.

A later source does not override an earlier one on how work is done; it may add facts the earlier one lacks.

## What to resolve, and when

Resolve only what the current step needs: the record location and owner; the user's timezone and locale when timing is material; the languages in use; the tools actually available and their real permissions; the people or roles a step involves and who holds authority; the standing rules that constrain the step. Unknown remains unknown; do not fill a gap with a plausible value.

If a needed fact is absent, ask one focused question that names the fact and why it is needed to proceed. Do not ask for setup, a questionnaire or a full profile before being useful. Proceed on the smallest stated assumption when asking would cost more than the risk of being wrong, and mark the assumption in the output.

## What stays outside the package

Never write into the package, a skill, a role file, an example or a test: organisation or person names, addresses or endpoints, record paths, identifiers, keys or tokens, standing rules copied from a workspace, or any real data from a conversation. Examples in instructions describe the shape of an input, not a sample organisation. When adapting this template, keep examples free of invented people, companies, dates and figures.

Do not search unrelated personal files to infer context. Do not retain context across conversations unless the host provides an authorized mechanism and the user knows it is used.

## Reporting context used

When context shaped the result, say which source supplied it: the workspace instructions, the record read, the user's statement, or an assumption. This lets the user correct the source rather than the symptom.
