---
name: find-landmines
description: "Find what could go wrong in this meeting, each traced to a record."
tools: []
model: small-local
maxSteps: 1
input: {"meeting": "title, attendees, purpose", "record": "promises and decisions about these people and this subject"}
output: {"type": "object", "required": ["landmines"], "properties": {"landmines": {"type": "array", "items": {"type": "object", "required": ["what", "source_ref"]}}}}
---

## Steps

1. Look for what was left unresolved, what nobody has mentioned since, and which number will not survive a question.
2. Keep only what you can point at in the record. An empty list is a valid answer.

## Done when

- Every landmine names the record it came from.
