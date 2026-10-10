# Benchmark Against External Sources

Loaded when the user provides source material (URLs, file paths, articles, repo links) ALONGSIDE an existing skill, with a verb like "optimize / improve / align / refine using [sources]". This is a variant of the audit workflow — it does NOT create a new skill (that's `workflows/from-source-material.md`). The sources are a BENCHMARK to check the skill against, not input to re-distill.

Run this BEFORE the 8 audit lenses — its findings inform the Synthesis lens (audit Step 5) especially.

## Why this exists

"Optimize skill X using repo Y" is a common request. Without a protocol the agent either (a) treats it as creation and re-distills from the sources (wrong — the skill already exists), or (b) force-imports source content to justify the "optimization" (worse — violates the "don't restructure source material" gotcha; if the skill already absorbed the source, importing more is bloat). The protocol forces a third path: check what's already absorbed, record deliberate divergences, then pivot to the structural lenses for the real improvements.

## Protocol

1. **Ingest the sources.** Fetch each source's content. Extract the principles / techniques / mental models each teaches (3-7 per source). Distill strategy, don't reformat prose.

2. **Map per principle.** For each extracted principle, classify against the existing skill:
   - **Already absorbed** — cite WHERE in the skill it lives (section + line). No cite = not absorbed.
   - **Deliberately diverged** — the skill does the opposite or omits it on purpose. Record the divergence AND the reason in a design note (a "Design Notes" / "参见" section in the skill) so a future maintainer doesn't "fix" it by re-importing the source's version. Divergence without a stated reason will be re-imported; divergence WITH a reason survives.
   - **Absent and relevant** — candidate improvement. Feed to the audit lenses.

3. **"Nothing to import" is a valid outcome.** If every principle is absorbed or deliberately diverged, the deliverable is: (a) the alignment+divergence design note (prevents regression), (b) pivot to the 8 structural audit lenses (architecture, gotchas, interactive, etc.) for real improvements. Do NOT force a source-driven improvement to justify the session — that is content restructuring, the thing the "don't restructure source material" gotcha forbids. Report "sources already distilled; value was recording alignment + divergence + structural audit" plainly.

4. **Pivot.** Hand the benchmark findings (absorbed map, divergence notes, absent candidates) to the 8 lenses. The Synthesis lens (Step 5) uses the absorbed/diverged map to answer "is the source perspective preserved?" with evidence, not impression.

## Evidence requirement

Declaring "absorbed" REQUIRES a citation (skill section + line). An uncited "absorbed" is a guess, and guesses skip real gaps. If you can't cite where, treat it as absent-and-relevant.

## Boundary

- Source + NO existing skill → `workflows/from-source-material.md` (creation), not this.
- Source + existing skill + verb "make one like it" → `from-source-material.md` (creation), not this.
- Source + existing skill + verb "optimize / improve / align / refine using" → THIS protocol.
