---
name: self-review
description: "Find every sentence in a diff that has no source in the brief."
tools: []
model: small-local
maxSteps: 1
input: {"brief": "the brief", "diff": "the change's diff"}
output: {"type": "object", "required": ["unsupported"], "properties": {"unsupported": {"type": "array", "items": {"type": "object", "required": ["file", "text"]}}}}
---

## Steps

1. For each added sentence or claim, find what in the brief supports it.
2. List each one with no source. An empty list is a valid answer.

## Done when

- Every unsupported claim names its file.
