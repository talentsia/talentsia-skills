---
name: extract-policy-fields
description: "Take the insurer, policy number, cover period and premium from a policy document, and any terms that contradict each other."
tools: ["documents.inspect/extract_text"]
model: small-local
maxSteps: 1
input: {"text": "the document's text"}
output: {"type": "object", "required": ["insurer", "policy_number", "cover_from", "cover_to", "premium", "contradictions"], "properties": {"insurer": {"type": ["string", "null"]}, "policy_number": {"type": ["string", "null"]}, "cover_from": {"type": ["string", "null"]}, "cover_to": {"type": ["string", "null"]}, "premium": {"type": ["string", "null"]}, "contradictions": {"type": "array"}}}
---

## Steps

1. Take each value only as printed. Null when the document does not state it.
2. List any two terms in the document that contradict each other, quoting both.

## Done when

- Every value is printed in the document or null.
