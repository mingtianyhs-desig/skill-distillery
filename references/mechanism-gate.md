# Mechanism Gate

Run this gate **first** in every creation and audit entry point, before any extraction, synthesis, or content review. Its only job: confirm the thing is actually a skill — or stop and name the right mechanism. A skill is advisory instruction; the agent may run it when relevant, but nothing guarantees execution. Only a hook guarantees execution.

## The Decision

Ask of the user's request (create) or the skill under review (audit):

| Signal | Verdict | Right mechanism |
|--------|---------|-----------------|
| A reusable process or on-demand knowledge | ✅ Skill. Continue. | — |
| Must happen every time and can't be skipped (auto-format on commit, mandatory checks) | ❌ Not a skill | Host hook or external automation (e.g., husky, pre-commit, lefthook) |
| A fact or convention that should hold every session | ❌ Not a skill | Persistent instructions file (CLAUDE.md / AGENTS.md) |
| A one-off investigation that would flood the main context | ❌ Not a skill | Sub-agent |

## When it fires

- **Creation entry points** (from-description, from-recent-work) — before extracting or proposing. If the answer is not "skill," name the right mechanism and stop; offer the pivot (e.g., "use a pre-commit hook"), but do not build, plan, or propose a skill-shaped artifact, and do not ask moot implementation-detail questions.
- **Audit entry point** — before reviewing content. If the mechanism itself is wrong, the verdict is "replace the mechanism, don't fix the content" — say so plainly and stop.

## Why it matters

Building a skill for a hook's job ships something that never runs; the user's failure looks like your failure. The gate is cheap (one question) and prevents the most expensive mistake: a well-crafted skill that solves the wrong problem.

## What the gate does NOT prove

It does not prove the skill will be *good* — only that a skill is the right *kind* of artifact. After the gate passes, the normal synthesis → strategy → build → validate flow applies.
