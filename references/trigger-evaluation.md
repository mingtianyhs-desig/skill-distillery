# Trigger Evaluation

Loaded when a skill's *description triggering* needs systematic verification — not the smoke check (build-and-validate Step 4 runs 1-3 prompts for Quick Personal), but the rigorous version: Public Polished skills, or any skill whose triggering is shaky (under/over-triggering observed).

This is the **description-triggering analog of gotcha #5** ("don't validate by mentally running the workflow — run real baselines"). Don't guess whether a description triggers correctly — run queries and measure it.

## Why this exists

skill-distillery teaches putting trigger keywords in `description` and a `Not for` boundary. But authoring triggers is not the same as verifying they fire. A description that looks right can under-trigger (the skill never loads when it should) or over-trigger (loads for near-miss queries it should defer). Only running real queries catches this.

## Methodology

### 1. Design the query set (20, split 10/10)

**Should-trigger (10)**: varied phrasings of the same intent — formal + casual, cases that don't name the skill, uncommon use cases, cases where the skill competes with others but should win. Realistic and concrete (file paths, context, column names, URLs, backstory, casual speech, typos, varied length).

**Should-not-trigger (10) — near-misses**: queries that *share keywords or concepts* with the skill but need something different. Adjacent domains, ambiguous phrasing where a naive keyword match would trigger but shouldn't. **Not** obviously-irrelevant queries (those prove nothing). The near-miss is the highest-signal test: it verifies the `Not for` boundary actually excludes the right things.

**Substance rule**: each query must be substantive enough to benefit from a skill. Trivial one-step lookups may not trigger *any* skill regardless of description — they're noise. Give each query enough context that a skill genuinely helps.

### 2. Execute (run each query, check trigger, 3x for reliability)

For each query, check whether the skill is consulted/loaded. Run each 3 times — model triggering is stochastic; a single run is unreliable. Record trigger rate per query.

**Degradation (portability — never require a specific CLI or subagent):**
- **Subagents available** (Claude Code, Cowork): dispatch a subagent per query to test triggering, in parallel.
- **No subagents** (DSH, claude.ai): the agent runs inline — treat the description as an `available_skills` entry, and for each query self-assess "would this description be consulted?" Run 2-3 description variants against the query set and compare. This is less rigorous but catches gross under/over-triggering.

### 3. Select (train/test split, pick by test score, avoid overfit)

Split the 20 queries: ~60% train, ~40% held-out test. Propose 2-3 description variants (rewording triggers, sharpening `Not for`, adding/removing keywords). Run each variant against the **train** set. Pick the variant with the best **test**-set trigger accuracy — never pick by train score alone (that overfits to the queries you designed). If a variant wins train but loses test, it's overfit; keep the simpler one.

This mirrors skill-creator's loop (which automates it via a CLI script) — here the agent executes the same logic manually. The automation is environment-specific and not prescribed; the methodology is portable.

## Lane proportionality

- **Quick Personal**: skip — the smoke check (1-3 prompts) is enough.
- **Team Internal**: run this only if triggering is observed to be shaky.
- **Public Polished**: run this — a misfiring description is a million-user bug.

## What this does NOT replace

Behavioral evals (does the skill do the right thing when it runs) are separate. Trigger-eval only answers "does the right skill load for the right queries." A skill can trigger correctly and still behave badly — that's the eval-step's job.

## Boundary

If the runtime has no concept of model-invoked skills (e.g., skills are always-loaded persistent instructions), triggering isn't a question — skip this entirely. Trigger-eval only applies where a model decides whether to load the skill from `description`.
