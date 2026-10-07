---
name: close-loops
description: "Make sure what people promised actually happens, without spending the executive on it."
---

## When to use

Use for the routine check of what is owed and slipping. Not for recording new promises; that is keep-records-current.

## Steps

1. Read what is owed with {{tool:commitments.read/list}}. The ones nobody has mentioned and the ones with no date are where loops open.
2. Go to the source before asking the owner: if a worker can tell you whether it happened, look with {{tool:work.history.read/outcomes}}.
3. Chase before escalating. A promise two days out that nobody has mentioned wants a quiet reminder, not an executive.
4. Escalate with {{tool:operator.notify/notify}} only when a deadline has passed, an owner has gone quiet after being asked, or something waits on it.
5. Say what a slip costs. 'Overdue' is a state; 'this is what the board deck is waiting on' is a reason to care.
6. Record what you did on the promise with {{tool:commitments.write/update}}. Recording a chase is not moving the promise.

## Done when

- Anything escalated has been chased at least once first, or is already past its deadline.
- Every action taken is recorded against the commitment.
