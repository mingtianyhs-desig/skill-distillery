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

- **URL** — Fetch with WebFetch, extract the content
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

If the skill involves external APIs, libraries, or domains where best practices shift fast:

> This involves [X]. Want me to research current best practices before building, or do you have enough context?

If research requested: spawn 2-3 parallel sub-agents with scoped questions (one per topic). Present findings before proceeding.

---

## Step 4: Evaluation Plan

Read `references/evaluation-patterns.md`, then create the right-sized test plan for the chosen lane.

### Quick Personal

Capture 1-3 smoke prompts. These can live in your working notes unless the user asks for an `evals.md`.

Include:
- 1 positive trigger prompt
- 1 representative task prompt
- Optional incomplete-context prompt

### Team Internal

Create or plan an `evals.md` with:
- 3 positive trigger prompts
- 1-2 negative/non-trigger prompts
- 2 representative task prompts
- 1 incomplete-context prompt
- Expected behavior bullets

### Public Polished

Create or plan an `evals.md` with:
- 5 positive trigger prompts
- 3 negative/non-trigger prompts
- 3 representative task prompts
- 2 edge-case or adversarial prompts
- 1 incomplete-context prompt
- Fresh-agent test checklist
- Expected behavior, success signals, and failure signals

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

## Step 6: Build

Create all files following the official spec. Order:
1. Reference files first (foundation)
2. Workflow files (if router pattern)
3. `evals.md` when required by lane, using `templates/eval-pack.md`
4. SKILL.md last (references everything else)

For each file:
- Follow the appropriate template from `templates/` as a starting point
- Adapt based on the synthesis from Step 2 and strategy from Step 3
- Use standard markdown headings
- Keep SKILL.md lean: under 150 lines for Quick Personal, 200 for simple shared skills, 300 for router skills
- Include concrete examples from the source material
- Keep research notes, rationale, and eval prompts out of SKILL.md unless needed at runtime

If decisions arise during build, follow the question convention (options when supported, numbered plain text otherwise). Don't guess on important choices.

---

## Step 7: Gotchas Review

Before validation, explicitly review the skill's gotchas content. This is the highest-signal content in any skill.

**Check:**
- Does the skill have a dedicated `## Gotchas` section (in SKILL.md or a reference file)?
- Are there at least 3-5 specific gotchas for non-trivial skills?
- Does each gotcha use "don't do X because Y" structure?
- Are gotchas based on real Claude failure modes (not theoretical warnings)?

**If gotchas are thin or missing**, think through:
1. What would Claude get wrong on first attempt applying this knowledge?
2. What are the most common misinterpretations of this domain?
3. What looks correct but is subtly wrong?
4. What does the source material explicitly warn against?

Add or strengthen gotchas before proceeding to validation.

---

## Step 8: Validate

Read `references/quality-checklist.md` and run through every item (note: gotchas are now the first section):

- Rigor lane selected and followed
- Eval depth matches lane
- Frontmatter valid and complete
- Description includes trigger keywords
- Line counts within limits
- All files cross-referenced
- Standard markdown headings
- Concrete examples present
- Interactivity patterns in place (if applicable)

Present the validation report:

> Skill created at [path]. Validation report:
> - [X] items pass
> - [Y] items need attention: [list them]

---

## Step 9: Eval & Smoke Test Review

Run the evaluation plan from Step 4 **for real** — record what the agent actually did, not what you expected. Every prompt also gets a **no-skill baseline run**: if with-skill and baseline behave identically, the prompt has no discriminating power (ceiling effect); replace it or add a behavioral assertion (rounds taken, when a tactic switches).

### Quick Personal
- Run the 1-3 smoke prompts for real: one positive trigger, one representative task, and (if applicable) one non-trigger
- Run each prompt once more without the skill as the baseline
- Fix obvious trigger, workflow, or verbosity problems
- Report any prompt you could not test

### Team Internal
- Check positive and negative trigger prompts
- Check representative task prompts against expected behavior
- Confirm `evals.md` records expected behavior clearly

### Public Polished
- Check the full eval pack
- Run at least one positive trigger, one representative task, and one non-trigger in the current environment
- Perform the fresh-agent test if available
- If a true fresh-agent test is unavailable, mark that limitation in the validation report and keep the checklist in `evals.md`

Present:

> Eval review:
> - [X] prompts pass
> - [Y] prompts need fixes
> - Fresh-agent test: [passed / unavailable / skipped by lane]

Fix any failed Public Polished eval before moving on.

---

## Step 10: Cross-Agent Compatibility Review

Skip this for Quick Personal skills unless the user requested multiple-agent support. For Team Internal and Public Polished skills, read `references/cross-agent-compatibility.md` and evaluate:

- Identify every Claude Code-specific feature used
- Check for plain-text fallbacks
- Verify tool references are action-oriented (not tool-name-specific)
- Assign degradation rating

Present:

> Cross-agent compatibility: **[Degrades Gracefully / Full / Claude Code-Dependent]**
> - [X] features are Claude Code-enhanced with fallbacks
> - [Y] features are universal
> - [Specific fixes needed, if any]

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
- [ ] All files created following official spec
- [ ] Gotchas section reviewed and populated with real failure modes
- [ ] Quality checklist passed
- [ ] Eval or smoke test review completed at the chosen depth
- [ ] Cross-agent compatibility reviewed when lane/target agents require it
- [ ] Shipping (README, review, publish) deferred to the manual-only `workflows/publish.md` — never auto-triggered
- [ ] User can invoke the skill and it works as designed
