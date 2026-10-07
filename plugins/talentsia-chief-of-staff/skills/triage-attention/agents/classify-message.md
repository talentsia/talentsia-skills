---
name: classify-message
description: "Judge one message: which pile it belongs in and the specific next step."
tools: []
model: small-local
maxSteps: 1
input: {"message": "sender (the inner sender for a forward), subject, summary, received", "priorities": "what the executive said matters"}
output: {"type": "object", "required": ["pile", "next_step"], "properties": {"pile": {"enum": ["needs_now", "decision", "monitoring", "handled", "someone_elses"]}, "next_step": {"type": "string"}, "draft": {"type": "boolean"}, "trade": {"type": ["string", "null"]}}}
---

## Steps

1. Ask what goes wrong if they never see it. If nothing much, it is monitoring or handled.
2. It is a decision only if a person must choose between real options.
3. Name the specific next step in one sentence, with the date or figure that makes it specific.
4. A message forwarded by the executive is from its original sender, not from the executive.

## Done when

- One pile and one specific next step.
