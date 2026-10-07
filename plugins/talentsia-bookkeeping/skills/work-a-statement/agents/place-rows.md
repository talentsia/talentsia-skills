---
name: place-rows
description: "Assign each staged statement row to an account in the entity's chart."
tools: ["ledger.chart.read/accounts"]
model: small-local
maxSteps: 2
input: {"rows": "list of {row_id, date, payee, amount}", "chart": "list of {account_id, name, type}"}
output: {"type": "object", "required": ["placed", "unplaced"], "properties": {"placed": {"type": "array", "items": {"type": "object", "required": ["row_id", "account_id"]}}, "unplaced": {"type": "array", "items": {"type": "object", "required": ["row_id", "reason"]}}}}
---

## Steps

1. Place each row on an account from the chart, by what the money was for.
2. Rows from the same payee usually belong together; place them consistently.
3. A row you cannot place goes in unplaced with the reason. Never force one.

## Done when

- Every row given is either placed or unplaced, never both.
