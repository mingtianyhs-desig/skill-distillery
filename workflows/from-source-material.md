# Workflow: From Source Material

Turn an article, talk, framework, or advice into a strategic, interactive skill.

## Required Reading

Read these reference files before proceeding:
1. `references/synthesis-patterns.md`
2. `references/architecture-decisions.md`
3. `references/evaluation-patterns.md`

---

## Step 1: Ingest Source Material

Detect what the user provided and ingest it:

- **URL** — Fetch the content at the URL
- **File path** — Read the file (supports .md, .pdf, .txt, .html)
- **Pasted content** — Work with what's in the conversation

After reading, present a brief summary:

> Here's what I'm working with: **[title/topic]** — [1-2 sentence summary of what the source covers].
> Is this the right source? Anything I should know about your intent before I start extracting?

**Wait gate:** Confirm the source is correct before proceeding.

---

## Step 2: Bottom-Up Extraction

Extract strategy from the source material. Do NOT restructure it — distill it.

For each of these categories, identify what the source provides:

### Core Principles (3-7)
What are the fundamental ideas that make this approach work? Each should be actionable, non-obvious, and testable.

### Mental Models
What frameworks does this teach for thinking about the problem? Decision trees, taxonomies, spectrums, matrices, or process loops.

### Decision Heuristics
What rules-of-thumb does it provide? "If X, do Y. If Z, do A instead."

### Context Separation
Which advice always applies (universal) vs. which depends on the situation (context-dependent)?

### Gotchas & Anti-Patterns
What does it say NOT to do? What common mistakes does it call out? Where would Claude specifically be likely to fail when applying this knowledge? Structure each as "don't do X because Y."

### Success Criteria
How would you know you're doing this well? What does good output look like?

### Present Synthesis

Format as a structured summary:

```
SYNTHESIS: [Source Title]

Core Principles:
1. [Principle] — [One-line explanation]
2. [Principle] — [One-line explanation]
3. ...

Mental Model: [Brief description of the framework]

Key Heuristics:
- If [X], then [Y]
- If [Z], then [A]

Gotchas (where Claude will fail):
- Don't [X] because [Y]
- Don't [X] because [Y]

Context-Dependent (not universal):
- [Advice] applies when [condition]
```

> Here's what I extracted from the source. Does this capture the essence? Anything missing, wrong, or that I'm weighting too heavily?

**Wait gate:** Do not proceed until the user validates the synthesis. Adjust if they push back.

---

## Step 3: Skill Strategy

Interactive decisions about how the skill should work. Per the question convention, render options when supported, numbered plain text otherwise. **At most 2-3 questions per round, with a confirm between the two groups** — never dump all six at once.

### Group 1: Skill Form

**Q1 — Rigor lane:** "What kind of skill are we making?"

- **Quick personal** — Fast capture for one high-context user; concise `SKILL.md`; 1-3 smoke prompts; no README/publication by default
- **Team internal** — Shared skill; clear enough for teammates; eval-light pack; README optional
- **Public polished** — Publishable skill; README, eval pack, fresh-agent test, and compatibility review required

**Q2 — Complexity (confirm, don't ask):** Infer from the source material: simple (one file, <200 lines of instruction) / medium (1-3 reference files) / complex (multiple workflows + references + maybe templates). Present: "Based on the source material, this is [complexity]. Does that feel right?"

**Q3 — Modes:** "Does this skill need multiple modes?"

- **Yes** — [Ask user to describe the modes]
- **No** — Single workflow
- **Not sure** — "Based on the source material, I'd suggest [recommendation]. Does that feel right?"

**Wait gate:** Confirm the form before moving to integration questions.

### Group 2: Integration

**Q4 — Invocation:** "What should trigger this skill?"

- **Manual only** — User invokes explicitly (set `disable-model-invocation: true`)
- **Auto-detect** — Agent loads when relevant (description-driven)
- **Both** — User can invoke manually, agent can also auto-detect (default)

**Q5 — Interactivity:** "How interactive should this skill be?"

- **Guided** — Discovery phase, multiple questions, wait gates
- **Direct** — User provides input, skill executes immediately
- **Adaptive** — Ask 1-2 clarifying questions, then execute

**Q6 — Target agents:** "Where will this skill be used?" (Ask only when the lane or publication implies multiple agents; Quick Personal defaults to "current agent only" and skips.)

- **Single host (current agent only)** — Can use that host's native features without fallbacks
- **Primary host, others welcome** (recommended for public skills) — Build for the primary host but include plain-text fallbacks so other agents can use it
- **Universal** — Must work equally well across all agents; action-oriented language, no host-specific features

This answer shapes the build:
- **Single host:** Use native question/option rendering freely, reference specific tools
- **Primary + others:** Option rendering with plain-text fallback, action-oriented language; host-specific fields (e.g., `allowed-tools`) are fine — other hosts ignore them
- **Universal:** Plain-text questions only, no tool-name references, no host-specific features

For Quick Personal skills, ask this only when the user mentions multiple agents or publication. Otherwise default to single host and keep moving.

### Research Gate

If the skill involves external APIs, libraries, or a fast-moving domain, follow the Research Protocol — see `references/research-protocol.md` (gate, execution, result handling). Otherwise skip research entirely.

---

## Step 4: Evaluation Plan

Read `references/evaluation-patterns.md`, then create the right-sized test plan for the chosen lane.

### Quick Personal

Capture 1-3 smoke prompts. These can live in your working notes unless the user asks for an `evals.md`.

Include:
- 1 positive trigger prompt
- 1 representative task prompt
- Optional incomplete-context prompt

### Team Internal & Public Polished

Create or plan an `evals.md` following the chosen lane's minimum eval pack in `references/evaluation-patterns.md` (Required Reading). Don't re-list the per-lane prompt counts here — evaluation-patterns is the single source; this workflow follows it.

Present:

```
EVALUATION PLAN: [skill-name]

Lane: [Quick Personal / Team Internal / Public Polished]
Artifacts: [SKILL.md only / evals.md / README / references]
Test prompts:
- [Prompt] -> [Expected behavior]
- ...
Fresh-agent test: [Required / Optional / Skipped]
```

For Team Internal and Public Polished skills, this is a wait gate. For Quick Personal skills, proceed after presenting the smoke prompts unless the user objects.

---

## Step 5: Architecture Proposal

Based on the strategy decisions, propose the exact file structure:

```
PROPOSED ARCHITECTURE: [skill-name]

Structure: [Simple / Simple + References / Router]
Rigor lane: [Quick Personal / Team Internal / Public Polished]

[skill-name]/
├── SKILL.md                    # [What goes here]
├── evals.md                    # [If Team Internal or Public Polished]
├── README.md                   # [If Public Polished or requested]
├── references/                 # [If needed]
│   ├── [file-a].md            # [What it contains]
│   └── [file-b].md            # [What it contains]
└── workflows/                  # [If router pattern]
    ├── [workflow-a].md         # [What it does]
    └── [workflow-b].md         # [What it does]

Rationale:
- [Why this structure vs. alternatives]
- [What goes in SKILL.md vs. references]
- [Why X reference files, not more/fewer]
- [How the lane affected artifact count and validation depth]
```

> Here's my proposed structure. Shall I proceed, or would you adjust anything?

**Wait gate:** Do not build until user approves the architecture.

---

## Step 6-10: Build & Validate

Building, gotchas review, validation, evals, and cross-agent review are shared execution steps — **single source of truth: `workflows/build-and-validate.md`**. Follow it in order after the architecture is approved:

1. Build
2. Gotchas Review
3. Validate (`scripts/validate_skill.py` + quality checklist)
4. Eval & Smoke Test Review (real runs with no-skill baseline)
5. Cross-Agent Compatibility Review

---

## Step 11-13: Ship (README, Review, Publish) — Manual Only

README generation, independent review, and publication have external side effects (public repo, distribution). They are isolated in a dedicated manual entry point so an auto-triggered creation flow can never reach them:

**See `workflows/publish.md`.** Run it only when the user explicitly asks to publish or ship. Never auto-trigger it.

---

## Success Criteria

This workflow is complete when:
- [ ] Source material read and understood
- [ ] Synthesis validated by user
- [ ] Rigor lane selected
- [ ] Strategy decisions made interactively
- [ ] Evaluation plan matches the lane
- [ ] Architecture proposed and approved
- [ ] Build & validation completed per `workflows/build-and-validate.md`
- [ ] Shipping (README, review, publish) deferred to the manual-only `workflows/publish.md` — never auto-triggered
- [ ] User can invoke the skill and it works as designed
