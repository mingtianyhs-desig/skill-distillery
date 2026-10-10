# Cross-Consistency Scan

Run this scan **before presenting an audit** (audit-existing-skill Step 10) and **after any structural change** to a skill (new files, renamed files, content moves). It catches the mechanical drift that lens ratings miss — orphaned files, broken links, dangling section refs, stale inventories, and duplicated checklists that have diverged. This is the "don't trust lens ratings alone" gotcha made executable.

`scripts/validate_skill.py` already covers the SKILL.md subset (frontmatter, link integrity, §-ref integrity, orphans, drift). The scan below **extends it to ALL files** plus inventory and redundancy checks.

## 1. Orphan check (all files)

Every file in `references/`, `workflows/`, `templates/`, `scripts/` is reachable: indexed in SKILL.md's Reference/Workflow/Template/Script tables, or linked from a file that is. A file never mentioned anywhere is orphaned — the agent can never reach it, and it rots silently.

## 2. Link resolution (all files)

Every markdown link in every file — not just SKILL.md — resolves to an existing file: bracketed text linked to a parenthesized path, resolved relative to the file that contains it. Links to external URLs (http/https) are exempt.

**Template false positives:** templates show users where to put links. A placeholder written as a live linked path to a file that doesn't exist yet reads as broken to a naive checker (exactly the mistake this document's first draft made). Write template examples as prose or backticked code — never as a live link to a non-existent file.

## 3. Section-ref integrity (all files)

Every `§N.N` / `§N.N.N` reference in prose maps to a numbered heading `# N.N ...` in the same file. A §-ref with no matching heading means a section move or renumber left a dangling pointer. (Dash form — `§1-9` list-item refs — is intentionally not checked.)

## 4. Inventory sync (README, evals)

- The README "What's inside" file tree lists every actual file — and no deleted ones. A tree that lags the real files misleads every reader.
- `evals.md` honestly reflects current coverage: behaviors added after the last run are marked untested, not silently claimed.

## 5. Redundancy / single-source check

Two places stating the same rule **will** diverge. Spot-check for duplicated enumerations: if the same checklist or count list appears in a workflow AND a reference, the reference is the single source — the workflow should point to it, not re-list it. (This is how duplicated lane eval-packs and the audit Step 8 checklist were caught and de-duplicated.)

## Boundary

The scan is mechanical and cheap — run it whenever structure changes. It does **not** replace the evaluative lenses (rigor, gotchas, security, synthesis...): it only verifies the skill is internally consistent. Consistency is necessary, not sufficient.
