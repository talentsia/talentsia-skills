---
name: rank-candidates
description: "Choose at most three priorities for today, each with why today, and at most one alert."
tools: []
model: small-local
maxSteps: 1
input: {"priorities": "what the executive said matters, in their words", "candidates": "list of {ref, what, evidence} gathered from tool results"}
output: {"type": "object", "required": ["priorities", "alert", "handled"], "properties": {"priorities": {"type": "array", "maxItems": 3, "items": {"type": "object", "required": ["ref", "why_today"]}}, "alert": {"type": ["object", "null"]}, "handled": {"type": "array"}}}
---

## Steps

1. Rank by what the executive said matters, never by what looks busy.
2. Keep a candidate only if its evidence says why today: what changed, what falls due, what closes.
3. Three is a limit, not a target. Two good ones beat three where the third was padding.
4. At most one alert, and only for something that genuinely threatens an outcome.

## Done when

- No more than three priorities and one alert.
- Every priority's why_today comes from its evidence.
