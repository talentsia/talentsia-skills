---
name: record-what-is-owed
description: "Record an amount due without representing it as money already paid."
---

## When to use

Use for invoices, bills, renewal notices and tax demands: amounts owed, not payments.

## Steps

1. An invoice, a bill, a renewal notice and a tax demand are amounts owed, not payments.
2. Record them with {{tool:ledger.bills.write/record_bill}}, never as a payment. Add the supplier first with {{tool:ledger.bills.write/add_contact}} if it is new.
3. Take the due date from the document. If it prints none, flag it with {{tool:ledger.review.flag/flag}}; never guess.
4. Copy the document's own invoice or account number into the reference.
5. Read the resulting open amount back with {{tool:ledger.reports.read/open_payables}} rather than asserting it.

## Done when

- The bill appears as an open payable the application itself computes.
- No payment was recorded for a document that only shows an amount due.
