---
name: review-an-insurance-document
description: "Review one insurance document and establish what it actually says."
---

## When to use

Use when a policy, schedule or certificate arrives. Never invent a value the document does not state.

## Steps

1. Read the document with {{tool:documents.inspect/inspect}} before stating anything about it.
2. Establish the insurer, the policy number, the cover period and the premium with {{agent:extract-policy-fields}}.
3. Never invent a value the document does not state. Say it is absent instead.
4. Note any term that contradicts another term in the same document.
5. Record what you established with {{tool:documents.register/register}}.

## Done when

- Every value reported can be pointed at in the document.
- Anything absent is reported as absent rather than estimated.
