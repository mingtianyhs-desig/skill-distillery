# Research Protocol

When and how to research during skill creation. Research is **on demand, not by default** — most skill creation doesn't need it. Trigger only when one of the conditions below fires; otherwise skip entirely.

## When to trigger
- Skill involves external APIs or libraries needing current docs
- Domain where best practices shift fast (frameworks, deployment patterns)
- Audit reveals the skill references outdated libraries or patterns
- User explicitly asks: "Can you research X?"

## When NOT to trigger
- Source material is self-contained (articles, talks)
- User already knows the domain
- Skill is about internal processes or conventions
- Simple skills that don't reference external tools

## How to ask
One gate before spawning anything:

> This involves [X]. Want me to research current best practices, or do you have enough context?

Per the question convention (options when supported, numbered plain text otherwise):
- **Yes, research first** — Fetch current documentation for accurate implementation
- **No, I have context** — Proceed with what we have

## How to execute
Spawn 2-3 parallel sub-agents (fast, cheap, good at retrieval) with specific, scoped questions. Not "research everything about X" — scope to what you actually need. One topic per agent.

Example agent prompts:
- "Fetch current Supabase RLS patterns from official docs"
- "Find current best practices for React Native navigation libraries"
- "Check if [library] is still actively maintained"

Use Context7 MCP when available: `resolve-library-id` → `query-docs` for library documentation.

## How to use results
Feed research back into synthesis and strategy — inform the principles and architecture. Don't dump raw findings into reference files. Present key findings to the user before proceeding.
