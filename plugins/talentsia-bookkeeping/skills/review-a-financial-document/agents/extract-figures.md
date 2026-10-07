---
name: extract-figures
description: "Choose the amount owed, any money that moved, the date and the reference from candidates the document actually contains."
tools: ["documents.inspect/extract_text"]
model: small-local
maxSteps: 1
input: {"text": "the document's text", "candidates": "amounts, dates and references found in it, with their labels"}
output: {"type": "object", "required": ["proves", "unsure"], "properties": {"proves": {"enum": ["owed", "moved", "neither"]}, "amount": {"type": ["string", "null"]}, "date": {"type": ["string", "null"]}, "reference": {"type": ["string", "null"]}, "unsure": {"type": "array"}}}
---

## Steps

1. Choose only among the candidates given. A figure not in the document does not exist.
2. The sum owed is the labelled total due, never the largest number or the last one.
3. A date with no year, or one the calendar does not have, goes in unsure.
4. Being unsure is an answer: list what you could not choose and why.

## Done when

- Every value chosen appears verbatim among the candidates.
