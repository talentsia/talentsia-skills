---
name: compare-clauses
description: "Compare two sets of policy terms and list the differences that matter."
tools: []
model: small-local
maxSteps: 1
input: {"a": "terms of the first option", "b": "terms of the second option"}
output: {"type": "object", "required": ["differences"], "properties": {"differences": {"type": "array", "items": {"type": "object", "required": ["term", "a", "b"]}}}}
---

## Steps

1. Compare cover limits, excesses and exclusions, term by term.
2. Only terms present in the evidence. A term in neither is not a difference.

## Done when

- Every difference quotes both sides.
