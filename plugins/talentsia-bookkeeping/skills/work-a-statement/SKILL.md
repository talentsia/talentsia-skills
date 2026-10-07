---
name: work-a-statement
description: "Bring every posted line of an account statement into the books, then prove the books against it."
---

## When to use

Use when a bank or card statement arrives, or rows from one are waiting to be placed.

## Steps

1. A statement goes in whole: {{tool:ledger.statements.import/import}} stages every row at once. Never record its rows one by one.
2. Read what is waiting with {{tool:ledger.statements.import/review_queue}}.
3. Place the rows in batches with {{agent:place-rows}}, then record them with {{tool:ledger.statements.import/categorise}}, grouping rows from one payee.
4. Balances and totals printed on a statement are not movements. The import leaves them out; do not record them either.
5. Once every row you can place is placed, reconcile against the closing balance the statement prints with {{tool:ledger.reconcile/reconcile}}.
6. A row you cannot place, or a statement with no closing balance, goes to a person with {{tool:operator.notify/notify}}, never skipped silently.

## Done when

- The statement was imported, not retyped.
- Every row is placed on an account or named to a person as needing one.
- The books were reconciled through the statement's last date, or a person was told why they could not be.

## Notes

- Recording rows one by one was tried: 45 of 53 rows never arrived.
- A batch is sized to what a job can finish, not to what fits in a response.
