# Workflow: Publish

Ship a finished skill for `npx skills` installation. **Manual entry only** — this workflow has external side effects (creating a public GitHub repo, distributing the skill). Never reach it from an auto-triggered flow; run only when the user explicitly asks to publish.

## Entry Condition

Run only when BOTH hold:

- The skill is built and validated (creation workflow Steps 1-10 done), AND
- The user explicitly says "publish", "发布", "ship it", or asks for an install command.

If you reached this file any other way, stop and ask whether the user actually wants to publish.

## Step 1: Generate README (if missing)

Create `README.md` alongside SKILL.md with:

1. **Skill name** as heading
2. **Install command** prominently displayed (use placeholder `owner/repo` if not yet published):
   ```
   npx skills add <owner/repo>
   ```
3. **What it does** — 2-3 sentences explaining the skill's purpose
4. **Who it's for** — target audience and common use cases
5. **Usage examples** — invocation commands (`/skill-name`, `/skill-name argument`)
6. **What's inside** — file tree showing SKILL.md + references
7. **Compatibility** — based on the target-agent decision from the creation workflow:
   - Claude Code only: "Built for Claude Code."
   - Claude Code primary: "Built for Claude Code. Degrades gracefully on other agents."
   - Universal: "Works across all coding agents."
8. **License** — MIT unless user specifies otherwise

Keep the README concise — under 100 lines. It's a landing page, not documentation.

## Step 2: Independent Review (Optional)

For Public Polished skills, offer a fresh-eyes review from an independent sub-agent. For Team Internal skills, offer it when the skill is complex or high-impact. Skip by default for Quick Personal skills.

> Skill looks good from my end. Want me to get a second opinion? I can spawn an independent review agent that reads the skill cold — no context from our building conversation — and flags anything it catches.

If the user opts in, read `references/independent-review-brief.md` and spawn one sub-agent (fast and sharp enough for review work) with this brief:

> You are an independent reviewer evaluating a freshly built skill. You were NOT involved in building it — that's the point.
>
> **Skill to review:** [full path to skill directory]
>
> **Your instructions are in:** [path to skill-distillery]/references/independent-review-brief.md — read that first.
>
> **Also read these skill-distillery references for evaluation criteria:**
> - references/synthesis-patterns.md
> - references/interactive-design-patterns.md
> - references/architecture-decisions.md
>
> Then read the entire skill (all files) and evaluate it according to the review brief. Return structured findings.

### Filter and Present

When the review agent returns findings, **don't just pass them through**. Act as a filter:

```
REVIEW FINDING: [Title]
Severity: [Critical / Important / Nit]
Reviewer says: [Their observation]
My take: [AGREE / DISAGREE / PARTIALLY AGREE] — [Brief rationale from your building context]
```

Be honest. If the reviewer caught something you missed, say so. If you disagree, explain why — you have context the reviewer doesn't. After presenting all findings, let the user pick which to fix, then implement and confirm what changed.

## Step 3: Publish

**Confirmation gate — do not skip:** before running any command, present the complete plan and get explicit confirmation:

> Publishing plan:
> - New public repo: `https://github.com/<owner>/<repo>` (created via `gh repo create <repo> --public`)
> - Files to push: SKILL.md, references/, README.md
> - After publish, anyone can install with `npx skills add <owner>/<repo>`

Proceed only after the user confirms. Then:

1. Create a public GitHub repo: `gh repo create <repo> --public`
2. Copy the skill files (SKILL.md, references/, README.md) into a temp directory
3. Initialize git, commit, and push
4. Update the README.md install command from placeholder to the real `owner/repo`
5. Present the repo URL and install command:

> Published at: https://github.com/<owner>/<repo>
>
> Anyone can install with:
> ```
> npx skills add <owner>/<repo>
> ```

## Success Criteria

This workflow is complete when:
- [ ] README generated when the lane requires it
- [ ] Independent review offered when the lane warrants it
- [ ] Explicit user confirmation received before ANY external action
- [ ] Public repo created and skill pushed
- [ ] README install command updated to the real repo
