---
name: record-money-that-moved
description: "Record actual movement of funds, on evidence that it moved."
---

## When to use

Use for a paid receipt or a remittance: evidence that money left or arrived. An invoice is not that.

## Steps

1. Record a payment only where the document shows the money gone: a paid receipt, or a line on a statement.
2. Record it with {{tool:ledger.payments.write/record_payment}}, or a receipt of money arriving with {{tool:ledger.payments.write/record_receipt}}.
3. A payment needs the expense account and the account the money left; choose both from {{tool:ledger.chart.read/accounts}}.
4. Use the date the movement happened, not the date the document was issued.
5. If the evidence does not say which account funded it, flag it with {{tool:ledger.review.flag/flag}}.
6. Read the entry back with {{tool:ledger.reports.read/entry}} before reporting it.

## Done when

- Every recorded movement is one the document shows as having happened.
- The entry was read back from the books before it was reported.
