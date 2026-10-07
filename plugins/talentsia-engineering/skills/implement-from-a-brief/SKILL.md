---
name: implement-from-a-brief
description: "Turn a written brief into a reviewed, previewed change in an authorised repository, without claiming anything a tool did not return."
---

## When to use

Use when you are handed a brief to implement. Not for merging or deploying: a prepared change waits for review and a person's approval.

## Steps

1. Plan the change with {{agent:plan-changes}}: the concrete changes the brief asks for and the files each touches.
2. Read the repository with {{tool:code.repo.read/repos}} and every file you will touch with {{tool:code.repo.read/read}}, so your change fits its structure.
3. Make each change with {{tool:code.repo.write/write}} for a whole file or {{tool:code.repo.write/replace}} for a passage. Leave what the brief did not ask about alone.
4. Run every check the repository lists with {{tool:code.checks.run/check}}. If one fails, read its output, fix the cause, and run it again.
5. Read your own change with {{tool:code.change.prepare/diff}}, then {{agent:self-review}}: every sentence you wrote needs a source in the brief.
6. Prepare it with {{tool:code.change.prepare/prepare}}: a one-line title and a summary of what changed, why, which checks ran with what result.
7. Build a preview with {{tool:code.preview/preview}} if the repository offers one, and report the address it returns.
8. End with: the change id, the files, each check's result, the preview address, and anything the brief asked for that you could not do.

## Done when

- A change was prepared in this job and its id reported.
- Every check the repository offers was run in this job and its result reported as returned.
- No claim about building, testing or previewing appears without the tool result behind it.

## Notes

- A file nothing reads is a specification, not a control. Say so when a change only adds one.
