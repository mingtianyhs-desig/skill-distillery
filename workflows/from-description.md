# Workflow: From Description

User describes what they want the skill to accomplish. Brainstorm if vague, propose directly if detailed.

## Required Reading

Read these reference files before proceeding:
1. `references/mechanism-gate.md`
2. `references/interactive-design-patterns.md`
3. `references/architecture-decisions.md`
4. `references/evaluation-patterns.md`

---

## Step 1: Listen & Assess

Read what the user provided. Determine which path to take:

### First: Mechanism Gate

Run the Mechanism Gate before designing anything — see `references/mechanism-gate.md`. If the answer is not "skill," name the right mechanism and stop; do not propose, build, or ask moot implementation-detail questions.

### Path A: Detailed Description

The user gave a clear, specific description of what the skill should do. Signs:
- Named specific functionality
- Described who it's for
- Mentioned trigger conditions or use cases
- Referenced similar tools or approaches

**Action:** Skip heavy brainstorming. Go directly to proposal:

> That's clear. To accomplish that, I'd structure it this way:
>
> **Name:** [suggested-name]
> **Core function:** [what it does]
> **Entry points:** [how users would invoke it]
> **Complexity:** [Simple / Medium / Complex]
>
> Sound right, or should I dig deeper on anything?

If user confirms → proceed to Step 3 (Strategy).

### Path B: Vague or Exploratory

The user has an idea but hasn't fleshed it out. Signs:
- "I want something that helps with..."
- "Can you make a skill for..."
- General domain without specific functionality
- No mention of who it's for or when to use it

**Action:** Brainstorm together. Ask 2-3 questions:

Use AskUserQuestion if available, plain text otherwise:

1. **"What problem does this skill solve?"**
   - What's the frustration or gap today?
   - What triggers someone to need this?

2. **"What does success look like after using it?"**
   - What's different? What did they produce?
   - How would they know it worked?

3. **"Can you give an example of how you'd use it?"**
   - "I'd type /skill-name and then..."
   - Concrete scenario, not abstract description

### Identify Skill Type

Based on the user's answers, identify which type of skill they're building. This shapes architecture decisions downstream.

| Type | Description | Architecture Implications |
|------|-------------|--------------------------|
| **Library/API Reference** | Correct usage of libraries, CLIs, SDKs with code snippets and pitfalls | Heavy on gotchas and code examples; often simple structure |
| **Product Verification** | Test and verification instructions, often paired with external tools | Scripts directory important; may need `allowed-tools` for test runners |
| **Data Fetching & Analysis** | Connect to data/monitoring infrastructure with workflow instructions | Needs credential handling guidance; config.json for dashboard IDs |
| **Business Process** | Automate repetitive workflows into single commands | Often simple instructions but complex dependencies; log files for consistency |
| **Code Scaffolding** | Generate boilerplate combining scripts with natural language requirements | Templates directory essential; scripts for deterministic generation |
| **Code Quality & Review** | Enforce standards, facilitate review, run via hooks or CI | Often uses `hooks` frontmatter; may run automatically, not just on invocation |
| **CI/CD & Deployment** | Deploy, monitor PRs, manage rollouts | Needs `disable-model-invocation: true`; safety hooks for destructive operations |
| **Runbook** | Transform symptoms into structured investigation reports | Router pattern common (different symptoms → different procedures) |
| **Infrastructure Operations** | Routine maintenance and operational procedures | Needs guardrails for destructive actions; on-demand hooks for safety |

Present to user:

> Based on what you've described, this sounds like a **[type]** skill. Does that match your intent?

This doesn't lock anything in — it's a lens that helps make better architecture choices later.

### Decision Gate

After initial questions and type identification:

> Ready to proceed with building, or would you like to explore more?

Per the question convention:
- **Proceed** — I have enough context to propose an approach
- **Explore more** — There are more details to clarify
- **Let me add context** — I want to provide additional information

---

## Step 2: Research (if needed)

Follow the Research Protocol from SKILL.md:

- If the skill involves external APIs/libraries, trigger the research gate
- Ask: "This involves [X]. Want me to research current best practices, or do you have enough context?"
- If yes: spawn 2-3 parallel sub-agents with scoped questions (one per topic: library docs, patterns, pitfalls)
- Feed findings back into the proposal — don't dump into skill files
- If the user already knows the domain well: skip entirely

---

## Step 3-13: Convergent Process

From here, follow the same process as the source-material workflow — **single source of truth; no parallel copies here**:

- **Steps 3-5: Skill Strategy → Evaluation Plan → Architecture Proposal** — `workflows/from-source-material.md`
- **Steps 6-10: Build → Gotchas → Validate → Eval & Smoke Test → Cross-Agent** — `workflows/build-and-validate.md`
- **Steps 11-13: Ship (README, Review, Publish)** — manual only, `workflows/publish.md`. Never auto-triggered.

---

## Success Criteria

This workflow is complete when:
- [ ] User's intent clearly understood (via detailed description or brainstorming)
- [ ] Research done if external dependencies involved
- [ ] Strategy decisions made interactively and architecture approved (Steps 3-5)
- [ ] Build & validation completed per `workflows/build-and-validate.md`
- [ ] Shipping (README, review, publish) deferred to the manual-only `workflows/publish.md` — never auto-triggered
