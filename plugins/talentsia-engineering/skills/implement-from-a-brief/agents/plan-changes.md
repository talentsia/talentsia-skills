---
name: plan-changes
description: "List the concrete changes a brief asks for and the files each touches."
tools: ["code.repo.read/files", "code.repo.read/read"]
model: small-local
maxSteps: 3
input: {"brief": "the brief, in full", "repository": "the repository's name"}
output: {"type": "object", "required": ["changes", "out_of_scope"], "properties": {"changes": {"type": "array", "items": {"type": "object", "required": ["file", "change"]}}, "out_of_scope": {"type": "array"}}}
---

## Steps

1. Read the brief to the end, then list the files it touches with {{tool:code.repo.read/files}}.
2. Read each file you will change with {{tool:code.repo.read/read}} so the plan fits its structure.
3. One entry per change; anything the brief did not ask for goes in out_of_scope.

## Done when

- Every change names a file that exists or one the brief asks to create.
