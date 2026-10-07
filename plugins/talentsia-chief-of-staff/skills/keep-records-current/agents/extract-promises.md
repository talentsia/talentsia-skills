---
name: extract-promises
description: "List every promise a document makes: who owes it, what, when in the document's own words, and what finished looks like."
tools: []
model: small-local
maxSteps: 1
input: {"document": "the finished work's text, as given", "today": "the date, for resolving dates that name no year"}
output: {"type": "object", "required": ["promises", "unowned"], "properties": {"promises": {"type": "array", "items": {"type": "object", "required": ["owner", "title", "due_words", "done_when"]}}, "unowned": {"type": "array"}}}
---

## Steps

1. Read the document to its end; who owes what is usually last.
2. A promise has one owner. Two names is two promises; no name goes in unowned.
3. Keep when the work happens in the document's own words, such as 'by Week 2'. Never invent a date.
4. Write done_when as one checkable line.

## Done when

- Every action the document assigns is a promise or listed as unowned.
