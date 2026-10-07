---
name: match-existing
description: "Compare extracted promises with those already recorded: which are new, which exist, which existing ones gain a date."
tools: []
model: small-local
maxSteps: 1
input: {"extracted": "the promises extract-promises returned", "recorded": "the promises already recorded"}
output: {"type": "object", "required": ["new", "already", "needs_date"], "properties": {"new": {"type": "array"}, "already": {"type": "array"}, "needs_date": {"type": "array"}}}
---

## Steps

1. The same open promise from the same owner is one promise, however it is reworded.
2. An existing undated promise that the document now dates goes in needs_date.

## Done when

- Every extracted promise is in exactly one list.
