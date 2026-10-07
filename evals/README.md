# Behavior evaluation plan

These 64 synthetic cases are **not executed model results**. Static package checks prove discoverability and contained artifacts, not reasoning or successful runtime loading. Cases and expected observable outcomes are in [cases.json](cases.json).

## Run in the target client

Install Talentsia Do 0.5.2, verify exactly ten skills, then start independent synthetic contexts for each case. Provide its prompt and raw records, with tools/persistence disabled unless the case explicitly requires an isolated mock record store. Do not give the model the expected answer. For routing cases, let the host select naturally rather than forcing the skill; also check explicit invocations. Record which skill loaded and the produced artifact/output.

For duplicate capture, compare original and resulting IDs/count. For stale writes, use a synthetic mock store that changes I-8 to revision 3 after the initial read; verify the actual write targets the current revision or is withheld. A textual promise to reconcile is not a passed stale-write test. For external boundaries, verify no message/calendar/third-party tool call occurs. For no-storage cases, verify no durable-save or future-monitoring claim. For Do With Me, inspect the actual work product, not only a description of intended work.

Run the ten paired PT/EN cases and the twelve shared-boundary/routing cases. Record client/model/version, loaded skills, available tools, raw output, record diffs, side effects and pass/fail against the observable rubric. Keep personal/live records outside the test. Do not declare PASS from a keyword match alone.

Current status: authored and statically checked; model behavior and new-version ChatGPT UI loading **not run**. No automated network/model runner or future schedule is included.

The same cases apply to the skill file: attach `SKILL-talentsia-do-<version>.md` to a fresh chat with no plugin installed, send the activation sentence, then run the case prompt; repeat with the file placed in a Project whose instructions say to apply it. Routing cases check that the right workflow is named and applied from the file alone; record client and app surface (phone/desktop/web). Skill-file behavior is **not run**.

The additional 32 fixtures cover the audit gaps. Cases needing actual storage failures, reference failures, changing revisions or instrumented handoffs require an isolated harness; their text alone is not a simulated failure. Use the released package in a supported isolated context. Keep live records outside these tests.
