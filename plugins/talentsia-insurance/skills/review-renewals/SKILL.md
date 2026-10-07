---
name: review-renewals
description: "Find the real future obligations in an insurance document and make each one a dated task."
---

## When to use

Use when a document may carry a renewal or payment date someone must act on. Only dates the document actually prints.

## Steps

1. Read the document with {{tool:documents.inspect/inspect}}.
2. Identify any date by which a person must act, such as a premium or renewal date.
3. Create a task with {{tool:tasks.write/create}} only for an obligation the document actually states, with the date as written.
4. Do not create a task for a date that has already passed.

## Done when

- Every task created corresponds to a date printed in the document.
- No task was created for a date already past.
