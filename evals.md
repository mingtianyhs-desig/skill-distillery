# Skill Evals

Skill: skill-distillery
Lane: Public Polished
Run: first real run after the mechanism-triage + portability revamp (branch `revamp/mechanism-triage-and-portability`)

## How to Run

Each prompt runs twice: once **with** the skill available (a fresh agent given exactly `SKILL.md` plus the one workflow it routes to, asked to execute turn 1), once **without** it (a fresh agent, no skill guidance, default behavior only, same prompt). Record what actually happened, not what was predicted. Assertions are quantitative — routing target, named mechanism, whether a skill-shaped artifact was produced, question count — because a pass/fail that both runs can satisfy proves nothing.

**Caveat on method:** these are single-turn samples, not multi-turn sessions. They test the turn-1 decision and the discipline around it; they do not test a full end-to-end build. Full-session runs are listed under Not Run.

## Positive Triggers

- Prompt: "帮我审计 D:\DeepSeek\skills\think-task 这个技能，看看质量怎么样"
  Expected: route to `workflows/audit-existing-skill.md`; run the Step 1 Mechanism Gate before reading content; ask the context question at a wait gate; evaluate Gotchas first
  Actual: **PASSED.** Routed to `audit-existing-skill.md`. Mechanism Gate ran before any content audit and passed on the skill's own description. Asked the 3-way context question at an explicit wait gate. First lens: Gotchas.
  Untested: the full lens run (inventory, 8 lens ratings, prioritized improvements).

- Prompt: "我想把这个链接做成技能：https://example.com/design-systems-101"
  Expected: route to `workflows/from-source-material.md`; Step 2 fetches the source and asks "Confirm the source" before extracting
  Actual: **NOT RUN.**

## Non-Triggers (mechanism gate)

- Prompt: "我想做个技能，每次 git 提交前自动格式化代码"
  Expected: Mechanism Gate fires; names the right mechanism (host hook); does **not** build, plan, or propose a skill-shaped artifact; asks no moot implementation-detail questions; offers a pivot
  Actual: **PASSED.** Routed to `workflows/from-description.md`; Step 1 Mechanism Gate fired; named Git pre-commit hooks (husky / pre-commit / lefthook); stopped with no proposal and no file creation. Exact sentence: "技能是错的机制，这里得先停一下。"

### Baseline comparison — the finding that matters

The same prompt run with **no** skill guidance:

- The baseline agent **also** flagged the mismatch, and also suggested pre-commit / husky / lint-staged. It listed more wrapper options than the skill's answer.
- **So the Mechanism Gate is not a capability gain over a competent fresh agent. Do not claim it is.**
- What the skill adds is discipline, not judgment:
  - The skill run proposed **no skill-shaped artifact** and asked **no irrelevant implementation detail**. The baseline left a "I can just write you a SKILL.md" door open *and* asked about prettier / ruff / gofmt — a question that is moot once the answer is "use a hook."
  - The skill's stop is unconditional (the gate says stop). The baseline's stop was a judgment call that not every fresh agent would make.
- **Conclusion:** the gate's value is *consistency* — guaranteeing the right stop every time, and making the judgment explicit and auditable instead of relying on the model's luck. Assert it as "no skill-shaped output, no moot questions," never as "baseline can't see this."

## Representative Tasks

- Prompt: "我想做个技能帮写 API 文档"
  Expected: `workflows/from-description.md` Path A (vague description); Step 3 Group 1 asks at most 3 questions — rigor lane, complexity confirmation, modes — never all six at once
  Actual: **NOT RUN.**

## Incomplete Context

- Prompt: "帮我审计一下这个技能" (no path)
  Expected: ask for the path; do not invent one
  Actual: **NOT RUN.**

## Edge Cases

- Prompt: "把这个技能发布到 GitHub 上"
  Expected: route to `workflows/publish.md`, manual only; publish.md requires a confirmation gate before `gh repo create --public`; publishing must not be reachable from an auto-triggered creation flow
  Actual: **NOT RUN.**
- Prompt: "随便做个技能"
  Expected: Mechanism Gate plus lane questions, not a silent default build
  Actual: **NOT RUN.**

## Fresh-Agent Test

- Full multi-turn session with a fresh agent: **NOT RUN.**
- Recorded as a known limitation, per the workflow: mark it, keep the checklist, do not claim coverage.

## Findings from this run

1. **Routing assertions are the strongest test in this pack.** Both executed positive cases routed to the correct workflow and fired the named mechanism. Routing is a property only the skill possesses, so it genuinely discriminates.
2. **Mechanism-Gate assertions do not discriminate against baseline** — see the note above. Re-scope them to discipline (no skill-shaped output, no moot questions) or replace them with routing / step-discipline assertions.
3. **The gate is the only part of this revamp with executed evidence.** Steps 3-10, publish, and cross-agent review all remain unexecuted; their value rests on design review, not runs.
4. **`scripts/validate_skill.py` passes** on this skill with one intentional warning: `argument-hint` is a non-standard frontmatter key — safe for CLI agents, a hard error if packaged to claude.ai / Skills API.
5. **Method limitation:** single-turn sampling cannot catch multi-turn failures (e.g., drifting off the workflow mid-build). A full session run is the missing piece, and it is the only assertion type that would distinguish "the skill is followed" from "the skill is read."
