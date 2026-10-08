# Capabilities

The vocabulary skills write against, `talentsia-capabilities/v1`. A skill names an interface and an operation as `{{tool:<interface>/<operation>}}` and lists the interface in `skill.json.requires.capabilities` as `<interface>@1`. The device binds each operation to the tool it has installed and the worker holds; a skill never names a tool. A reference that cannot resolve fails installation. Requiring an interface asks for it; it never grants it.

The repository file `capabilities/v1.json` is authoritative and may have grown since this copy. When drafting inside the repository, read it; when drafting in a harness without the repository, use this table and mark the choice for verification.

| Interface | Operations | Reaches |
| --- | --- | --- |
| `documents.inspect` | `inspect`, `extract_text`, `metadata` | a document that arrived with the job |
| `documents.register` | `register` | the organisation's document registry |
| `files.workspace` | `list`, `read`, `write`, `move`, `mkdir` | the worker's own workspace files |
| `host.observe` | `system`, `services`, `logs` | the device's health |
| `host.services.restart` | `restart` | a device service |
| `operator.notify` | `notify` | the person responsible for the device |
| `memory.learn` | `learn`, `recall` | the worker's own memory |
| `work.history.read` | `activity`, `outcomes` | what this seat has done |
| `team.read` | `roster`, `context`, `gaps` | who else works here and what they hold |
| `artifacts.read` | `list`, `search`, `read` | artifacts other work produced |
| `artifacts.dispose` | `dispose` | retire an artifact |
| `work.handoff` | `delegate` | hand work to a colleague seat |
| `decisions.prepare` | `raise` | put a decision to a person |
| `staffing.request` | `request` | ask for a seat to be filled |
| `commitments.mine` | `list`, `update` | this seat's own promises |
| `intent.read` | `priorities`, `measures` | what the person said matters |
| `intent.propose` | `propose` | propose a change to intent |
| `commitments.read` | `list` | the organisation's promises |
| `commitments.write` | `record`, `update`, `date` | record or change a promise |
| `decisions.read` | `list` | open decisions |
| `briefs.write` | `brief`, `meeting_brief` | write a brief |
| `attention.read` | `inbox`, `attention` | what has arrived and what needs attention |
| `attention.write` | `record` | record an attention item |
| `calendar.read` | `today`, `week`, `meeting`, `categorise` | the calendar |
| `drafts.write` | `draft_reply` | draft a reply for a person to send |
| `ledger.entity.read` | `entity`, `partners` | the bookkeeping entity and its counterparties |
| `ledger.chart.read` | `accounts` | the chart of accounts |
| `ledger.reports.read` | `open_payables`, `entries`, `entry`, `expense_summary`, `financial_summary` | ledger reports |
| `ledger.documents.lookup` | `find_by_document` | entries behind a document |
| `ledger.bills.write` | `record_bill`, `add_contact` | record a bill or contact |
| `ledger.payments.write` | `record_payment`, `record_receipt` | record money moved |
| `ledger.statements.import` | `import`, `review_queue`, `categorise` | import and review a statement |
| `ledger.reconcile` | `reconcile` | reconcile |
| `ledger.review.flag` | `flag` | flag an entry for a person |
| `code.repo.read` | `repos`, `files`, `read`, `search` | an authorised repository |
| `code.repo.write` | `write`, `replace` | change a file in it |
| `code.checks.run` | `check` | run its checks |
| `code.change.prepare` | `diff`, `prepare` | prepare a change for review |
| `code.preview` | `preview` | preview a change |
| `tasks.write` | `create`, `update` | tasks |

## Choosing

Prefer a `read` before any `write`. Require the fewest interfaces that let every step resolve; an interface no step names is a question a reviewer will ask. A step that needs something not in this table is out of scope for a basic skill: say so rather than name a tool. Adding an interface or operation is a change to the Edge runtime and is proposed to the maintainers, not written into a skill.

## Harness rendering

A chat harness has no capability vocabulary. When a skill is rendered for a harness, read `{{tool:a.b/op}}` as "using the host's tool for `a.b` `op`, if one is available; otherwise say the step could not be performed". The Edge render keeps the literal reference.
