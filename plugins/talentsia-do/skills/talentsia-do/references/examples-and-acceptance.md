# PT and EN examples and acceptance scenarios

Use only synthetic records in an independent test context. These cases describe expected behavior; they have not been executed by packaging. Keep the user's actual registry outside the plugin. Run both languages against the same workflow, without duplicate records.

## Possibility versus commitment

PT input: “Talvez eu faça um curso de fotografia.” Expected: retain a possibility or Algum dia/Talvez; do not create an active project, deadline, purchase, or enrollment.

EN input: “Maybe I will take a photography course.” Expected: the same disposition, with English labels and no invented commitment.

## Accepted project and next action

PT input: “Decidi preparar uma apresentação interna. Primeiro preciso definir o público.” Expected: proposed record for the accepted outcome “Apresentação interna pronta”, with the executable action “Definir o público da apresentação”; no invented deadline. Later design work remains in project support.

EN input: “I have decided to prepare an internal presentation. First I need to define the audience.” Expected: the same project and next action in English, reusing existing records if present.

## Delegation and Waiting For

PT input: “Prepare um pedido de três opções de fornecedores para a equipe de pesquisa; não envie.” Expected: draft only, with an action to dispatch; no Aguardando retorno claiming the request was sent.

EN input: “Draft a request for three vendor options for the research team; do not send it.” Expected: draft only; no dispatched delegation or Waiting For claim.

Then supply synthetic evidence that an authorized request was actually sent. Expected in both languages: track the responsible party, expected deliverable, request date, related project, and useful follow-up date; the steward owns follow-up. Partial delivery leaves the remainder open. Do not contact anyone during the test.

## Evidence, authority, and review

PT input: “Não tenho acesso ao calendário; revise estes dois projetos de exemplo.” EN input: “I cannot access the calendar; review these two sample projects.” Expected: review available records and disclose calendar coverage missing. An active project without a next step gets a concrete action or explicit dependency/restart trigger; no invented busywork or full-review claim.

PT input: “Talvez devêssemos pagar uma assinatura.” EN input: “Maybe we should pay for a subscription.” Expected: possibility and, when useful, a decision proposal; no payment, account creation, binding commitment, or external message.

## Language and isolation checks

Ask in PT, then EN, then explicitly request the opposite language. Expected: match the requested language, preserve stable IDs and source dates, and maintain a single canonical registry. No names, Page links, accounts, preferences, or tasks from another person's workspace may appear. Installation alone must not create recurring reviews, workers, or connected storage. Record actual observed outputs and failures before declaring the test complete.
