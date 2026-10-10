---
name: skill-distillery
description: "Create or audit agent skills (Claude Code and other AI tools). Synthesizes source material (articles, frameworks, talks) bottom-up into strategic, interactive skills — or audits existing skills through a multi-lens framework. Use when creating, auditing, or improving skills, or turning articles/processes into skills. 中文触发：制作技能、创建技能、技能审计、技能评审、技能评估、改进技能、梳理技能、把文章或流程做成技能。"
when_to_use: "Triggers on: create skill, build skill, new skill, skill from article, turn this into a skill, capture this as a skill, audit skill, review skill, evaluate skill, improve skill, add reference, publish skill. 中文触发：制作技能、创建技能、技能审计、技能评审、技能评估、改进技能、梳理技能、分析技能、把文章做成技能、捕获流程为技能、发布技能。"
argument-hint: "[URL, file path, skill path, or description]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, AskUserQuestion, Agent
---

# Skill Distillery

Distill raw material into potent skills. Articles, talks, frameworks, recent AI work, or just an idea — skill-distillery extracts the strategy bottom-up and builds interactive, well-architected skills from it.

**The core insight:** Good skills aren't restructured content — they're distilled strategy. A 5,000-word article becomes a 300-line skill by extracting principles, mental models, and decision frameworks, not by reformatting paragraphs.

**Two conventions apply everywhere:**

- **Paths** — Every path referenced in this skill (references, workflows, templates, scripts) is relative to the skill's own directory (the one containing SKILL.md), not the user's current working directory. Resolve the skill directory first, then join the relative path.
- **Questions & options** — For any multiple-choice decision: render tappable options when the runtime supports them, otherwise ask as a numbered plain-text question. Don't repeat fallback boilerplate below; this one convention applies to all workflows. Ask at most 2-3 questions at a time.

## Quick Start

**From an article or framework:**
> `/skill-distillery https://example.com/great-article-about-design-systems`
> `/skill-distillery ~/Documents/talk-transcript.md`

**From recent AI work:**
> `/skill-distillery capture` — "I just figured out a great process for X, help me turn it into a skill"

**From a description:**
> `/skill-distillery` — "I want a skill that helps me write better API documentation"

**Audit an existing skill:**
> `/skill-distillery audit ~/.claude/skills/my-skill`
> `/skill-distillery review` — "Can you audit the skill in my skills folder?"

**Add to an existing skill:**
> `/skill-distillery add reference` — "I want to add a new reference file to my-skill"

---

## Core Principles

These apply to everything skill-distillery does:

1. **Bottom-up synthesis over content restructuring** — Extract principles and mental models from source material. Don't reformat — distill.

2. **Interactive by default** — Use AskUserQuestion for tappable decisions. Ask 2-3 questions at a time, not a wall. Provide shortcuts when context is already available.

3. **Propose before building** — Always present synthesis, architecture, and approach for user approval before creating files. Wait gates at every decision point.

4. **Progressive disclosure** — SKILL.md stays lean (200-300 lines). Reference files contain depth. Load conditionally based on what the user needs.

5. **Opinionated defaults** — Suggest interactive patterns proven in good skills (a discovery phase for guided workflows, mode detection for multi-mode skills). The user can override, but the defaults should be good.

6. **Research on demand, not by default** — Most skill creation doesn't need research. Trigger it only when external APIs/libraries are involved or the user explicitly asks. See Research Protocol below.

7. **Tailored to the user's specific goal** — Not generic skill-making advice. Every decision adapts to what this particular user is building for this particular purpose.

8. **Gotchas are the highest-signal content** — The most valuable part of any skill is where the agent typically fails. Every skill should have a dedicated gotchas section documenting specific failure points with "don't do X because Y" structure. Gotchas come from anticipating real failure modes, not theoretical anti-patterns. See `## Gotchas` below for this skill's own.

9. **Right-sized rigor by audience** — Quick personal skills stay lean; team skills get enough tests to share safely; public skills require evals, fresh-agent validation, and README/publication polish. Ask about target agents early when the skill may be shared, since Claude-only vs. universal support shapes tool and interaction choices.

---

## Gotchas

Where this skill itself typically fails — "don't do X because Y." These are the highest-signal lines in the whole skill.

- **Don't restructure source material into a skill** — because reformatted paragraphs are content, not strategy. Extract 3-7 principles and the mental model first; if you can't articulate them, you haven't read the source.
- **Don't skip Step 2's source-confirmation gate** — because synthesizing the wrong source is faster than fixing a wrong skill, and the user's intent is never in the article. Confirm the source and intent before extracting.
- **Don't build before the Mechanism Gate** — because a hook's job can't be fixed by better skill content. You'll ship a skill that never runs, and the user's failure will look like your failure. Run the gate first; if it's a hook, name the mechanism and stop.
- **Don't treat confirmation as agreement with your hypothesis** — because "OK, go" is often the polite answer to the wrong assumption. Write the hypothesis down first so it can be proven wrong.
- **Don't validate by mentally running the workflow** — because your imagination is calibrated to your own reading, not the reader's. Run the prompts against a no-skill baseline; if both behave identically, the prompt proves nothing.
- **Don't let SKILL.md grow past the reader's attention** — because it lands in context on every turn and burns tokens whether or not it is used. Push detail into references; keep SKILL.md under 300 lines.
- **Don't leave publishing reachable from an auto-triggered flow** — because `gh repo create --public` with no human in the loop is a footgun, not a feature. Publishing lives behind a manual entry point plus a confirmation gate.
- **Don't hard-code models, hosts, or years** — because the skill is agent-agnostic by design. "`Use Sonnet for this`" or "`as of 2026`" will be wrong on another host and read as sloppiness here. Use 'current' phrasing and leave the model unset.

---

## Rigor Lanes

Choose a lane early — it controls investigation depth, artifact count, and validation: **Quick Personal** (one author), **Team Internal** (shared), or **Public Polished** (published). Full criteria and per-lane requirements live in [evaluation-patterns.md](references/evaluation-patterns.md); load it before planning validation. Thorough investigation is valuable for every lane — the difference is where it lives (rationale informs distillation; only execution-critical instructions belong in runtime files).

---

## Research Protocol

Research is **on demand, not by default** — most skill creation doesn't need it. Trigger only when the skill involves external APIs/libraries, a fast-moving domain, an audit reveals outdated patterns, or the user asks. Otherwise skip entirely. Full protocol (gate, execution, result handling) in [research-protocol.md](references/research-protocol.md); load it only when a trigger fires.

---

## Entry Point Detection

Detect what the user provided and route to the right workflow:

| User Input | Route To |
|-----------|----------|
| URL (http/https) | `workflows/from-source-material.md` |
| File path to article/doc/transcript | `workflows/from-source-material.md` |
| File path to SKILL.md or skill directory | `workflows/audit-existing-skill.md` |
| "audit", "review", "evaluate" in args | `workflows/audit-existing-skill.md` |
| Source material (URL/article/repo) + existing skill + "optimize/improve/align using" | `workflows/audit-existing-skill.md` + `references/benchmark-against-sources.md` (benchmark variant — not from-source-material) |
| "capture", "just did", "turn this process" | `workflows/from-recent-work.md` |
| "add reference", "add workflow", "add script" | `workflows/add-component.md` |
| "publish", "发布" | `workflows/publish.md` (manual only — never reached by auto-trigger) |
| Description of what they want | `workflows/from-description.md` |
| No arguments / unclear | Ask what they'd like to do |

### Detection Logic

If the runtime substitutes `$ARGUMENTS` (Claude Code), use it directly. Otherwise, treat the user's current message as `$ARGUMENTS` — most runtimes pass the user's input there or append it automatically.

1. Check `$ARGUMENTS` for URLs → from-source-material
2. Check `$ARGUMENTS` for file paths → read the file, determine if it's a skill (has YAML frontmatter with `name`/`description`) or source material
3. Check `$ARGUMENTS` for keywords: "audit", "review", "evaluate", "improve" → audit-existing-skill
   - If sources (URLs/articles/repos) accompany an existing skill + improve/optimize/align → audit **benchmark variant** (load `references/benchmark-against-sources.md`), NOT from-source-material (which creates new skills)
4. Check `$ARGUMENTS` for keywords: "add reference", "add workflow", "add component" → add-component
5. Check `$ARGUMENTS` for keywords: "capture", "just did", "turn this into" → from-recent-work
6. If `$ARGUMENTS` contains a description → from-description
7. If no arguments, ask per the question convention:

- **Turn source material into a skill** — I have an article, talk, or framework
- **Capture recent work** — I just did something and want to save the process
- **Describe what I want** — I'll explain what the skill should do
- **Audit an existing skill** — Evaluate a skill I have or found

**After selecting a workflow, read it and follow it exactly.**

---

## Reference Index

All supporting knowledge in `references/`:

| File | Contents | Load When |
|------|----------|-----------|
| [mechanism-gate.md](references/mechanism-gate.md) | Confirm it's a skill, not a hook/CLAUDE.md/subagent — run before any creation or audit entry | Creation and audit entry points (first step) |
| [official-spec.md](references/official-spec.md) | Skill spec — frontmatter fields, features, format. Authoritative source is the live online docs; check before building | Building or auditing skills |
| [research-protocol.md](references/research-protocol.md) | When and how to research during creation (gate, execution, result handling) | Only when a research trigger fires (external APIs/libraries, fast-moving domain) |
| [benchmark-against-sources.md](references/benchmark-against-sources.md) | Audit an existing skill against external source material — absorbed/diverged/absent mapping; "nothing to import" is valid | When sources accompany an existing skill + optimize/improve/align verb |
| [trigger-evaluation.md](references/trigger-evaluation.md) | Systematic description-trigger verification (20 should/shouldn't queries, near-miss negatives, train/test) — the description analog of gotcha #5 | Public Polished skills, or when triggering is shaky |
| [synthesis-patterns.md](references/synthesis-patterns.md) | How to extract principles from source material | Source material or recent work entry points |
| [architecture-decisions.md](references/architecture-decisions.md) | Simple vs. router, when to use each file type | Architecture proposal step (all workflows) |
| [interactive-design-patterns.md](references/interactive-design-patterns.md) | Discovery, modes, wait gates, AskUserQuestion | Strategy step and audit workflow |
| [quality-checklist.md](references/quality-checklist.md) | Validation checklist | Validate step (all workflows) |
| [evaluation-patterns.md](references/evaluation-patterns.md) | Rigor lanes and eval pack design | Before planning validation |
| [cross-agent-compatibility.md](references/cross-agent-compatibility.md) | Cross-agent review guide | Cross-agent review step (all workflows) |
| [independent-review-brief.md](references/independent-review-brief.md) | Pre-baked instructions for independent review sub-agent | Optional review step in build workflows |

## Workflow Index

| Workflow | Purpose |
|----------|---------|
| [from-source-material.md](workflows/from-source-material.md) | Article/talk/framework → skill (flagship workflow) |
| [from-description.md](workflows/from-description.md) | Blank slate → brainstorm → skill |
| [from-recent-work.md](workflows/from-recent-work.md) | Capture AI process as reusable skill |
| [build-and-validate.md](workflows/build-and-validate.md) | Shared build → gotchas → validate → eval → cross-agent steps |
| [audit-existing-skill.md](workflows/audit-existing-skill.md) | Full-framework audit with 8 evaluation lenses |
| [add-component.md](workflows/add-component.md) | Add reference/workflow/script/template to existing skill |
| [publish.md](workflows/publish.md) | Publish/ship a finished skill (manual only — never auto-triggered) |

This skill's own eval pack: [evals.md](evals.md) — real runs, baseline comparison, and the cases still untested.

## Templates

Ready-to-copy starting points in `templates/`:

| Template | Use When |
|----------|----------|
| [simple-skill.md](templates/simple-skill.md) | Single-workflow skills under 200 lines |
| [router-skill.md](templates/router-skill.md) | Multi-workflow skills with shared principles |
| [eval-pack.md](templates/eval-pack.md) | Team Internal or Public Polished eval packs |

## Scripts

| Script | Use When |
|--------|----------|
| [validate_skill.py](scripts/validate_skill.py) | Deterministic checks: frontmatter, 1,536 cap, packaging warnings, link integrity, internal section-ref integrity, orphans, drift. Pure stdlib — runs in any environment (`python validate_skill.py <skill-dir>`). Run it during validation (see `workflows/build-and-validate.md` Step 3) |
