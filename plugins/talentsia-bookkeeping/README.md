# Talentsia Bookkeeping

The basic bookkeeping a worker needs to keep books safely: read the document before recording, record what is owed as owed, import statements whole, and choose only accounts that exist.

Free, basic edition for Talentsia Edge workers. MIT licensed. The contract these skills follow is [docs/edge-worker-skills.md](../../docs/edge-worker-skills.md); validate with `python3 scripts/check_edge_skills.py`.

| Skill | What it does | Replaces |
|---|---|---|
| [`review-a-financial-document`](skills/review-a-financial-document/SKILL.md) | Establish what a financial document actually proves, before recording anything. | `bookkeeping_document_review` v2 |
| [`review-the-books`](skills/review-the-books/SKILL.md) | Look over the assigned entity's books for work that is unfinished or wrong, using the application's own figures. | `bookkeeping_review` v2 |
| [`choose-the-account`](skills/choose-the-account/SKILL.md) | Put a recording in the right place in the entity's own chart of accounts. | `expense_classification` v2 |
| [`record-what-is-owed`](skills/record-what-is-owed/SKILL.md) | Record an amount due without representing it as money already paid. | `obligation_tracking` v2 |
| [`work-a-statement`](skills/work-a-statement/SKILL.md) | Bring every posted line of an account statement into the books, then prove the books against it. | `process_bank_statement` v3 |
| [`record-money-that-moved`](skills/record-money-that-moved/SKILL.md) | Record actual movement of funds, on evidence that it moved. | `transaction_extraction` v2 |

This is the free, basic edition, as Talentsia Do is. The enhanced edition (tax treatment, multiple entities, partnerships and K-1s, depreciation, jurisdiction rules) is premium, in `talentsia-premium-skills`, and replaces these when installed.
