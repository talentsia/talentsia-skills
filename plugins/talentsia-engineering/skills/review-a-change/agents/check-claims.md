---
name: check-claims
description: "Check each claim a change adds against its brief, and locate every problem."
tools: []
model: small-local
maxSteps: 1
input: {"brief": "the brief the change cites", "diff": "the change's diff with surrounding lines"}
output: {"type": "object", "required": ["findings"], "properties": {"findings": {"type": "array", "items": {"type": "object", "required": ["file", "line", "problem", "fix"]}}}}
---

## Steps

1. For each added sentence, ask whether the brief says the product can back it.
2. For each added file, ask what reads it. Nothing reading it is a finding.
3. Write each problem with its file, line, what is wrong and what would fix it.

## Done when

- Every finding has a file and a line.
