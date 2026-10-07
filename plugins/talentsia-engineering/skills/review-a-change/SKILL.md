---
name: review-a-change
description: "Judge a prepared change against its brief, its checks and its claims, and return one verdict a person can act on."
---

## When to use

Use when a prepared change needs review. Change nothing yourself: a reviewer who edits is no longer reviewing.

## Steps

1. Read the change record you were handed: what it says it did, which checks it says ran, and the brief it cites.
2. Read the diff with {{tool:code.change.prepare/diff}} and every changed file with {{tool:code.repo.read/read}}; a diff without its surroundings hides what it broke.
3. Run every check yourself with {{tool:code.checks.run/check}}. Your run is the evidence; the engineer's report of it is a claim.
4. Check the claims and what reads each added file with {{agent:check-claims}}.
5. Write each problem as: file, line, what is wrong, what would fix it. A problem without a location is an opinion.
6. End with exactly one verdict, APPROVE, CHANGES NEEDED or REJECT, and the reasons under it. Change nothing yourself.

## Done when

- Every check was run in this job by the reviewer.
- The answer ends with exactly one of APPROVE, CHANGES NEEDED, REJECT.
- Every problem raised names a file and a line.
