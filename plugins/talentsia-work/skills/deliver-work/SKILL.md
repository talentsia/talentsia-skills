---
name: deliver-work
description: "File finished work from a Talentsia seat: upload images, file the deliverable with its open questions, link it to the task and close the task, each only on the person's say-so. Use for entregar o trabalho, file this deliverable, or finish my Talentsia task."
---

# Deliver Work

Read [the seat protocol](references/seat-protocol.md) before proceeding, then follow the seat's own procedures from `how_this_seat_works`; they override this skill on how the work is done.

Delivering puts work in the organisation's register under the seat's name. Show the person what will be filed and **file only when they say to**.

1. Check the work against the task's done line and the seat's procedures (`how_this_seat_works`, if not read this session). Call `read_deliverables` so the filing builds on earlier versions instead of standing beside them.
2. Pictures go first. Call `file_image` with the path to each PNG, JPEG or WebP (up to 8 MB) on this machine, and keep the name each one returns.
3. Assemble the body: the work itself in full, as markdown, naming each image that was returned. End it with the section headed exactly `## What I could not establish`, listing each open point and who could answer it. If there are none, write "Nothing open." under the heading.
4. On the person's go-ahead, call `file_deliverable` with the title, the body, the `taskId` and the `objectiveId` the task serves. It lands as a draft and nothing is published. Then call `say_what_you_are_doing`, naming what was filed.
5. Close the task with `finish_task` only when the person says it is done, with a note saying what was produced and under what title it was filed. Only work the seat holds, or work that was handed over or given up on, can be closed. If the device refuses, report the refusal as it came.

Never describe work you have not made as filed. Never say a deliverable was published, posted or sent: approval and publishing happen on the device, by a person.

**PT:** “Pode registrar o carrossel e encerrar a tarefa.” Upload the images, file with open questions, then close. **EN:** “Draft looks good, don't file yet.” Prepare the body and stop before `file_deliverable`.
