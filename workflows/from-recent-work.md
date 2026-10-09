# Workflow: From Recent Work

Capture a process you just did with AI as a reusable skill. Turn "I figured this out" into "anyone can do this."

## Required Reading

Read these reference files before proceeding:
1. `references/synthesis-patterns.md`
2. `references/architecture-decisions.md`
3. `references/evaluation-patterns.md`

---

## Step 1: Understand What Happened

Figure out what the user just did and what they learned.

### First: Is this a skill at all? (Mechanism Gate)

Before capturing, apply this gate to what the user just did:

- **A reusable process others would repeat** → a skill. Continue. ✅
- **Must happen every time and can't be skipped** → a host hook or external automation, NOT a skill — a skill is advisory and may not run; only a hook guarantees execution.
- **A one-off investigation, not a repeatable process** → not a skill; don't capture it as one.
- **A fact or convention that should hold every session** → a persistent instructions file (CLAUDE.md / AGENTS.md type), NOT a skill.

If it's not a skill, say so plainly and name the right mechanism.

### Gather Context

Ask 2-3 questions:

1. **"What did you just do? What was the task?"**
   - What problem were you solving?
   - What was the end result?

2. **"What did you figure out along the way?"**
   - Any non-obvious steps or gotchas?
   - Decisions you had to make?
   - Things that didn't work before you found what did?

3. **"Do you want me to review our recent conversation for context?"**
   - If conversation history is available, scan it for the process
   - If git history is relevant, offer to check recent commits

### Source Material Options

Depending on what's available:

- **Conversation history** — Review recent messages for the process, decisions, and lessons learned
- **Git history** — Scan recent commits for what changed and why
- **User description** — Work from what they tell you
- **Combination** — Use all available sources

---

## Step 2: Extract the Reusable Process

From whatever context you gathered, extract:

### Repeatable Workflow
What steps would apply next time someone faces this problem? Order matters — what has to happen first?

### Decision Points
What choices did you face? What did you decide and why? These become the skill's interactive decision points.

### Pitfalls & Gotchas
What went wrong before it went right? What would you warn someone about?

### Essential Tools & Commands
What specific tools, libraries, commands, or APIs were critical?

### Present Extraction

```
CAPTURED PROCESS: [Task Name]

Workflow (repeatable steps):
1. [Step] — [Why this step matters]
2. [Step] — [Decision point: if X, do Y; if Z, do A]
3. [Step] — [Gotcha: watch out for...]

Key Decisions:
- [Decision] → [What we chose and why]

Pitfalls:
- [Thing that went wrong] → [How to avoid it]

Tools Used:
- [Tool/library] for [purpose]
```

> Here's what I captured from the process. Does this cover the important parts? Anything I'm missing or got wrong?

**Wait gate:** Confirm extraction accuracy before proceeding.

---

## Step 3-13: Convergent Process

From here, follow the same process as the source-material workflow — **the single source of truth is `workflows/from-source-material.md`**; don't maintain a parallel copy here:

- **Steps 3-10: Strategy → Evaluation Plan → Architecture → Build → Gotchas → Validate → Eval & Smoke Test → Cross-Agent Compatibility** — follow `workflows/from-source-material.md` in order.
- **Steps 11-13: Ship (README, Review, Publish)** — manual only, via `workflows/publish.md`. Never auto-triggered.

---

## Success Criteria

This workflow is complete when:
- [ ] Process understood from conversation history, git history, or user description
- [ ] Reusable workflow extracted with decision points and pitfalls
- [ ] Extraction validated by user
- [ ] Rigor lane selected
- [ ] Strategy decisions made interactively
- [ ] Evaluation plan matches the lane
- [ ] Architecture proposed and approved
- [ ] All files created following official spec
- [ ] Gotchas section reviewed and populated
- [ ] Quality checklist passed
- [ ] Eval or smoke test review completed at the chosen depth
- [ ] Cross-agent compatibility reviewed when lane/target agents require it
- [ ] Shipping (README, review, publish) deferred to the manual-only `workflows/publish.md` — never auto-triggered
