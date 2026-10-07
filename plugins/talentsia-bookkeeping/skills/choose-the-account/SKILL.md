---
name: choose-the-account
description: "Put a recording in the right place in the entity's own chart of accounts."
---

## When to use

Use whenever a recording needs an account. The chart belongs to the entity; never invent one.

## Steps

1. Read the chart with {{tool:ledger.chart.read/accounts}} and choose only from what it returns, by account id.
2. Never invent a category or post to an account that is not listed.
3. Choose by what the money was for, not by who was paid.
4. If nothing in the chart reasonably fits, that is a question for a person, not a guess.

## Done when

- Every account used came from the chart the application returned.
