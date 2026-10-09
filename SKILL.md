---
name: skill-distillery
description: "Create or audit agent skills (Claude Code and other AI tools). Synthesizes source material (articles, frameworks, talks) bottom-up into strategic, interactive skills — or audits existing skills through a multi-lens framework. Use when creating new skills, turning articles into skills, capturing AI workflows as skills, auditing/reviewing existing skills, or improving skill quality. Triggers on: create skill, build skill, new skill, skill from article, turn this into a skill, capture this as a skill, audit skill, review skill, evaluate skill, improve skill."
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
- **Don't skip Step 2's source-confirmation gate** — because synthesizing the wrong source is faster than fixing a wrong skill, and the user's intent is never in the article.
- **Don't build before the Mechanism Gate** — because a hook's job can't be fixed by better skill content. You'll ship a skill that never runs, and the user's failure will look like your failure.
- **Don't treat confirmation as agreement with your hypothesis** — because "OK, go" is often the polite answer to the wrong assumption. Write the hypothesis down first so it can be proven wrong.
- **Don't validate by mentally running the workflow** — because your imagination is calibrated to your own reading, not the reader's. Run the prompts against a no-skill baseline; if both behave identically, the prompt proves nothing.
- **Don't let SKILL.md grow past the reader's attention** — because it lands in context on every turn and burns tokens whether or not it is used. Push detail into references; keep SKILL.md under 300 lines.
- **Don't leave publishing reachable from an auto-triggered flow** — because `gh repo create --public` with no human in the loop is a footgun, not a feature. Publishing lives behind a manual entry point plus a confirmation gate.
- **Don't hard-code models, hosts, or years** — because the skill is agent-agnostic by design. "`Use Sonnet for this`" or "`as of 2026`" will be wrong on another host and read as sloppiness here.

---

## Rigor Lanes

Choose a lane early and let it control investigation depth, artifact count, and validation:

| Lane | Use When | Default Output | Validation |
|------|----------|----------------|------------|
| Quick Personal | The skill is for one high-context author | Concise `SKILL.md`; optional notes | 1-3 smoke prompts |
| Team Internal | The skill will be reused by teammates or multiple agents | `SKILL.md` plus focused references; README optional | Trigger/non-trigger prompts plus representative tasks |
| Public Polished | The skill is meant to be published or presented as a polished artifact | `SKILL.md`, README, eval pack, progressive references | Eval pack, fresh-agent test, compatibility review |

Thorough investigation is still valuable for every lane. The difference is where it lives: research notes and rationale inform the distillation, while only execution-critical instructions belong in runtime skill files.

---

## Research Protocol

When and how to research during skill creation.

**When to trigger:**
- Skill involves external APIs or libraries needing current docs
- Domain where best practices shift fast (frameworks, deployment patterns)
- Audit reveals the skill references outdated libraries or patterns
- User explicitly asks: "Can you research X?"

**When NOT to trigger:**
- Source material is self-contained (articles, talks)
- User already knows the domain
- Skill is about internal processes or conventions
- Simple skills that don't reference external tools

**How to ask:** One gate before spawning anything:

> This involves [X]. Want me to research current best practices, or do you have enough context?

Per the question convention:
- **Yes, research first** — Fetch current documentation for accurate implementation
- **No, I have context** — Proceed with what we have

**How to execute:** Spawn 2-3 parallel sub-agents (fast, cheap, good at retrieval) with specific, scoped questions. Not "research everything about X" — scope to what you actually need.

Example agent prompts:
- "Fetch current Supabase RLS patterns from official docs"
- "Find current best practices for React Native navigation libraries"
- "Check if [library] is still actively maintained"

Use Context7 MCP when available: `resolve-library-id` → `query-docs` for library documentation.

**How to use results:** Feed research back into synthesis and strategy — inform the principles and architecture. Don't dump raw findings into reference files. Present key findings to user before proceeding.

---

## Entry Point Detection

Detect what the user provided and route to the right workflow:

| User Input | Route To |
|-----------|----------|
| URL (http/https) | `workflows/from-source-material.md` |
| File path to article/doc/transcript | `workflows/from-source-material.md` |
| File path to SKILL.md or skill directory | `workflows/audit-existing-skill.md` |
| "audit", "review", "evaluate" in args | `workflows/audit-existing-skill.md` |
| "capture", "just did", "turn this process" | `workflows/from-recent-work.md` |
| "add reference", "add workflow", "add script" | `workflows/add-component.md` |
| "publish", "发布" | `workflows/publish.md` (manual only — never reached by auto-trigger) |
| Description of what they want | `workflows/from-description.md` |
| No arguments / unclear | Ask what they'd like to do |

### Detection Logic

1. Check `$ARGUMENTS` for URLs → from-source-material
2. Check `$ARGUMENTS` for file paths → read the file, determine if it's a skill (has YAML frontmatter with `name`/`description`) or source material
3. Check `$ARGUMENTS` for keywords: "audit", "review", "evaluate", "improve" → audit-existing-skill
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
| [official-spec.md](references/official-spec.md) | Skill spec — frontmatter fields, features, format. Authoritative source is the live online docs; check before building | Building or auditing skills |
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
| [validate_skill.py](scripts/validate_skill.py) | Deterministic checks: frontmatter, 1,536 cap, packaging warnings, link integrity, orphans, drift. Pure stdlib — runs in any environment (`python validate_skill.py <skill-dir>`). Run it during validation (see `workflows/build-and-validate.md` Step 3) |
