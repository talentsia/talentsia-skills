---
name: review-a-financial-document
description: "Establish what a financial document actually proves, before recording anything."
---

## When to use

Use first, whenever a financial document arrives to be booked. Not for recording it: this skill decides what the document proves.

## Steps

1. Read the document with {{tool:documents.inspect/inspect}} before saying anything about it.
2. Check whether these books already rest on it with {{tool:ledger.documents.lookup/find_by_document}}. If they do, the work is done.
3. Decide what it proves, and take its figures, with {{agent:extract-figures}}: an amount owed, money that moved, or neither.
4. Take every figure from the document. A number that is not printed does not exist.
5. If a figure that matters cannot be read, flag it with {{tool:ledger.review.flag/flag}} rather than estimating it.

## Done when

- Every recorded figure appears in the document it came from.
- The same document was not recorded twice.

## Notes

- A looser number pattern offers an invoice number, an account number and a year as amounts. Amounts carry a currency marker or two decimals.
