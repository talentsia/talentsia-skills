---
name: check-against-brief
description: "Compare a deliverable with its brief, item by item."
tools: []
model: small-local
maxSteps: 1
input: {"brief": "what was asked for", "delivered": "the deliverable's text", "checks": "results of any named checks, as the runtime recorded them"}
output: {"type": "object", "required": ["verdict", "missing"], "properties": {"verdict": {"enum": ["accept", "accept_with_gaps", "return"]}, "missing": {"type": "array"}, "must_change": {"type": ["string", "null"]}}}
---

## Steps

1. List what the brief asked for and mark each as delivered or not.
2. A worker saying a check passed is a claim; only a recorded check result is evidence.
3. Return only for one named thing that must change; otherwise accept and list the gaps.

## Done when

- One verdict, and must_change set whenever the verdict is return.
