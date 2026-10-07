---
name: review-the-books
description: "Look over the assigned entity's books for work that is unfinished or wrong, using the application's own figures."
---

## When to use

Use for a routine review of an entity's books or of recent changes to them. A review changes nothing in the books.

## Steps

1. Name the books from {{tool:ledger.entity.read/entity}}. A report about an entity names it from a tool, never from memory.
2. Ask the application for its figures: {{tool:ledger.reports.read/open_payables}}, {{tool:ledger.reports.read/entries}} and {{tool:ledger.reports.read/expense_summary}}.
3. Do not add rows up yourself. The application's totals are the authoritative ones.
4. Look for what is due soon, what is unresolved, and what is missing evidence.
5. Raise a notification with {{tool:operator.notify/notify}} only where something genuinely needs a person. Silence is a valid outcome.

## Done when

- Every figure reported came from the application, not from arithmetic.
- The entity was named from a tool result.
