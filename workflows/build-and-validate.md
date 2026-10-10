# Workflow: Build & Validate

Shared execution steps for every creation workflow — building, gotchas review, validation, evals, and cross-agent review. **Single source of truth** for these steps; reached from a creation workflow after the architecture is approved. For shipping (README, review, publish), see `workflows/publish.md` (manual only).

## Required Reading

1. `references/quality-checklist.md`
2. `references/evaluation-patterns.md`
3. `references/official-spec.md` — when building or auditing frontmatter
4. `references/cross-agent-compatibility.md` — when the lane or target agents require it

---

## Step 1: Build

Create all files following the official spec. Order:

1. Reference files first (foundation)
2. Workflow files (if router pattern)
3. `evals.md` when required by lane, using `templates/eval-pack.md`
4. SKILL.md last (references everything else)

For each file:

- Follow the appropriate template from `templates/` as a starting point
- Adapt based on the synthesis and strategy decisions from the calling workflow
- Use standard markdown headings
- Keep SKILL.md lean: under 150 lines for Quick Personal, 200 for simple shared skills, 300 for router skills
- Include concrete examples
- Keep research notes, rationale, and eval prompts out of SKILL.md unless needed at runtime

If decisions arise during build, follow the question convention (options when supported, numbered plain text otherwise). Don't guess on important choices.

---

## Step 2: Gotchas Review

Before validation, explicitly review the skill's gotchas content. This is the highest-signal content in any skill.

**Check:**

- Does the skill have a dedicated `## Gotchas` section (in SKILL.md or a reference file)?
- Are there at least 3-5 specific gotchas for non-trivial skills?
- Does each gotcha use "don't do X because Y" structure?
- Are gotchas based on real failure modes (not theoretical warnings)?

**If gotchas are thin or missing**, think through:

1. What would the agent get wrong on first attempt applying this knowledge?
2. What are the most common misinterpretations of this domain?
3. What looks correct but is subtly wrong?
4. What does the source material explicitly warn against?

Add or strengthen gotchas before proceeding to validation.

---

## Step 3: Validate

Run the deterministic checks, then the manual checklist:

1. Run `scripts/validate_skill.py <skill-directory>` — errors must be fixed; review every warning.
2. Read `references/quality-checklist.md` and run through every item (gotchas first):

- Rigor lane selected and followed
- Eval depth matches lane
- Frontmatter valid and complete
- Description includes trigger keywords, within the 1,536-char cap
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

## Step 4: Eval & Smoke Test Review

Run the evaluation plan **for real** — record what the agent actually did, not what you expected. Every prompt also gets a **no-skill baseline run**: if with-skill and baseline behave identically, the prompt has no discriminating power (ceiling effect); replace it or add a behavioral assertion (rounds taken, when a tactic switches).

### Change-Scoped Runs (after an iteration, not the full suite)

After a change — not at a ship/milestone gate — run only the evals whose assertions touch the changed area, not the whole suite. First map the change to affected evals: which sections, stages, or behaviors did it touch, and which evals assert those? Run just those, plus their no-skill baselines. The full suite runs at ship/milestone gates, where the cost is justified. When the change-to-eval mapping is uncertain, run more rather than less — anything skipped still gets caught at the gate. This keeps the recurring iteration cost cheap without lowering the ship bar. (The lane rules below set run *depth*; the ship gate sets suite *breadth*.)

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

Fix any failed Public Polished eval before moving on.

---

## Step 5: Cross-Agent Compatibility Review

Skip this for Quick Personal skills unless the user requested multiple-agent support. For Team Internal and Public Polished skills, read `references/cross-agent-compatibility.md` and evaluate:

- Identify every host-specific feature used
- Check for plain-text fallbacks (question convention)
- Verify tool references are action-oriented (not tool-name-specific)
- Check frontmatter is packaging-safe for claude.ai / Skills API (six standard fields only)
- Assign degradation rating

Present:

> Cross-agent compatibility: **[Degrades Gracefully / Full / Host-Dependent]**
> - [X] features are host-enhanced with fallbacks
> - [Y] features are universal
> - [Specific fixes needed, if any]

---

## Success Criteria

Shared completion criteria for the build & validate phase:

- [ ] All files created following official spec
- [ ] Gotchas section reviewed and populated with real failure modes
- [ ] `scripts/validate_skill.py` passes (errors fixed, warnings reviewed)
- [ ] Quality checklist passed
- [ ] Eval or smoke test review completed at the chosen depth — real runs with no-skill baseline
- [ ] Cross-agent compatibility reviewed when lane/target agents require it
