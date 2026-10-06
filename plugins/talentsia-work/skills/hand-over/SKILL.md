---
name: hand-over
description: "File new work from a Talentsia seat, for itself or handed to one of the organisation's own workers, with what finished looks like and what it serves. Use for passar para outro, file a task for the device, or hand this to the Legal worker."
---

# Hand Over

Read [the seat protocol](references/seat-protocol.md) before proceeding, then follow the seat's own procedures from `how_this_seat_works`; they override this skill on how the work is done.

Filed work belongs either to this seat or to another worker on the device. Get both the owner and the done line right before filing.

1. Decide whose it is. Work the seat will do itself is filed without `forWorker`: it is held in the seat's name and shows as working at once, so the device's own worker does not start it too. Work only the device or another worker can do (running a check behind the gateway, adopting a pushed branch, a legal review) is filed with `forWorker` set to that worker, and the device decides whether this seat may hand work to it. If it refuses, report who the seat may ask, as the device said.
2. Write the `goal` in English, specific enough to act on without this conversation: what to do, on what, and the references that matter (task, deliverable or branch names). Write the `done` line as one checkable sentence. Set `objectiveId` from `objectives` when the work serves one.
3. Show the person the goal, the done line and the recipient. **File with `file_task` when they agree.** Then call `say_what_you_are_doing` on the current task, if there is one, naming what was handed over and to whom.

Do not hand over work in order to avoid it, and do not split one piece of work into many tasks that each say less. If the person is changing direction rather than adding work, use What Needs Me instead.

**PT:** “Peça ao jurídico para revisar este texto.” File for that worker with a checkable done line, after approval. **EN:** “I pushed the branch; get the device to adopt it.” Hand it to the device's engineer, naming the branch.
