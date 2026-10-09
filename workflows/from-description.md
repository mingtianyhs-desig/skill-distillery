# Workflow: From Description

User describes what they want the skill to accomplish. Brainstorm if vague, propose directly if detailed.

## Required Reading

Read these reference files before proceeding:
1. `references/interactive-design-patterns.md`
2. `references/architecture-decisions.md`
3. `references/evaluation-patterns.md`

---

## Step 1: Listen & Assess

Read what the user provided. Determine which path to take:

### First: Is this a skill at all? (Mechanism Gate)

Before designing anything, apply this gate to what the user described:

- **A reusable process or on-demand knowledge** → a skill. Continue. ✅
- **Must happen every time and can't be skipped** → a host hook or external automation, NOT a skill. A skill is advisory instruction — the agent may run it when relevant, but nothing guarantees execution; only a hook does. Tell the user the mechanism is wrong and stop.
- **A fact or convention that should hold every session** → a persistent instructions file (CLAUDE.md / AGENTS.md type), NOT a skill.
- **A one-off investigation that would flood the main context** → a sub-agent, NOT a skill.

If it's not a skill, say so plainly and name the right mechanism. Don't build a skill for a hook's job.

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

If AskUserQuestion is available:
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

From here, follow the same process as the source-material workflow:

**Step 3: Skill Strategy** — Choose the rigor lane, then make interactive decisions about invocation, interactivity, modes, complexity, and target agents. See `workflows/from-source-material.md` Step 3.

**Step 4: Evaluation Plan** — Define smoke prompts or an eval pack based on the lane. See `workflows/from-source-material.md` Step 4.

**Step 5: Architecture Proposal** — Propose exact file structure with rationale. Wait for approval. See `workflows/from-source-material.md` Step 5.

**Step 6: Build** — Create all files following official spec. See `workflows/from-source-material.md` Step 6.

**Step 7: Gotchas Review** — Ensure gotchas section is populated with real Claude failure modes. See `workflows/from-source-material.md` Step 7.

**Step 8: Validate** — Run quality checklist. See `workflows/from-source-material.md` Step 8.

**Step 9: Eval & Smoke Test Review** — Run or simulate the planned checks. See `workflows/from-source-material.md` Step 9.

**Step 10: Cross-Agent Compatibility Review** — Evaluate cross-agent support when the lane or target agents require it. See `workflows/from-source-material.md` Step 10.

**Step 11-13: Ship (README, Review, Publish)** — Manual only, never auto-triggered. See `workflows/publish.md`.

---

## Success Criteria

This workflow is complete when:
- [ ] User's intent clearly understood (via detailed description or brainstorming)
- [ ] Research done if external dependencies involved
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
