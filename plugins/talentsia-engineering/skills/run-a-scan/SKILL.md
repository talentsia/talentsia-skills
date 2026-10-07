---
name: run-a-scan
description: "Run a named scan over an authorised repository and report exactly what it found, with the log it wrote."
---

## When to use

Use when asked to scan a repository, such as for vulnerable dependencies. Whether a finding matters is a person's call; your job is that they see it.

## Steps

1. Call {{tool:code.repo.read/repos}} to see which repositories exist and which checks each offers. A scan is one of those checks, by name.
2. Run it with {{tool:code.checks.run/check}}. Wait for the result; do not describe what it will find.
3. Report each finding as returned: the package or item, the version, the advisory identifiers, and where it was found.
4. Report the count and the log path. A scan that found nothing says so plainly; one that could not run says why and stops.
5. Do not rank or dismiss findings.

## Done when

- The scan was run by name in this job.
- The findings reported match the tool's output, including the count.
