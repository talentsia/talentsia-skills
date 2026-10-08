---
name: template-skill
description: "<One sentence stating what this skill does and when to use it. Name the phrases users say in each supported language; name the neighbouring skill that owns the adjacent case so the harness can route between them.>"
---

# <Skill Display Name>

Read [the shared method](references/core.md) before proceeding. Apply its identity, language, authority, record and evidence rules. Without storage return a portable record marked **not saved**; without tools distinguish drafts/proposals from performed work.

<Two or three sentences in the imperative: what the skill reads first, what it produces, and the one thing it must not turn into. Keep the whole file under about 400 words; the harness loads it on every invocation. Detail belongs in the shared references or in a conditional section below.>

## When to use

<One paragraph: the situation this is for, and when not to use it. A device renders this, Steps and Done when on a small model; everything else is for larger models and harnesses.>

## Steps

1. Read <the record, snapshot or input the step depends on> before producing anything. State missing coverage when it is material.
2. <The core move of the skill, as one observable action with a verb and an object. Tools as {{tool:<interface>/<operation>}}, subagents as {{agent:<name>}}.>
3. <The verification proportional to the result: compare, reread, confirm with the tool.>
4. Reconcile the result with the current record; mark what remains proposed; name the next step or the decision needed.

## Done when

- <A checkable statement taken from a tool result or an artifact, not from intent.>
- <A bound: at most, exactly, never.>
- <The failure this skill exists to prevent did not happen.>

## Filters

In scope when <condition>. Adjacent when <condition>: offer <neighbouring skill name> rather than perform it silently. Out of scope when <condition>: say so and return the useful bounded part. Order of consideration: <fixed constraints> → <context or capability> → <capacity> → <priority and consequence>.

## Subagents

<Delete this section if the skill never splits its work.> When the work divides into independent, verifiable parts, read [subagents](references/subagents.md) and assign each part with the brief contract: goal, exact inputs, the exact references to carry, read-only authority, output format, done criteria, must-nots. Verify every return against the record before it changes anything. Without a delegation tool, perform the parts in sequence yourself and say so.

## Boundaries

This skill grants no permission to <the external actions this domain touches>. Read [operating instructions](references/operating-instructions.md) when ownership, delegation or authority must be resolved, and [organizational context](references/organizational-context.md) when the task depends on who, where or which standing rule. Never claim a save, send, schedule or read that did not verifiably happen.

## Output

Lead with the result and the consequential next step or decision. State which records changed, which changes remain proposed and what was not covered. When any gap exists, end with `What I could not establish`. Steps of at most 300 characters, at most eight, and one checkable Done when line each are what the Edge validator and the Skill Builder's contract-checker enforce.

## A welcoming first turn

If invoked without content, explain the purpose in one or two short sentences in each supported language and invite the input the skill needs. Do not ask for setup, a destination or a questionnaire before being useful.

<Supported language A:> “<One or two sentences a user would read, describing what this skill helps with and what to send. No names, dates or figures.>”

<Supported language B:> “<The same, in the other language.>”

## Handoffs

Typical chain in this pack: <skill> → <skill> → <skill>. Carry IDs, evidence, state, proposed and confirmed changes. A suggested handoff has not been executed; continue a requested chain within existing authority, and offer the next stage when only this one was requested.
