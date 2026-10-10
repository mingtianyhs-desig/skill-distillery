# Skill Specification（事实底座）

> **前置声明**：本文件是官方文档的**工作子集**——字段、上限、打包行为只收录本技能关心的问题，且可能滞后。**字段全集与最新行为以 https://code.claude.com/docs/en/skills 为准，构建或审计技能前先核对线上文档。**

## Commands and Skills Are Merged

Custom slash commands and skills are now the same thing. `.claude/commands/review.md` and `.claude/skills/review/SKILL.md` both create `/review`. If both exist, the skill takes precedence.

## SKILL.md Structure

YAML frontmatter + standard markdown body:

```markdown
---
name: my-skill
description: What it does and when to use it
---

# My Skill

## Quick Start
[Immediate actionable guidance]

## Instructions
[Step-by-step procedures]

## Examples
[Concrete usage examples]
```

## Frontmatter Reference

All fields are optional. Only `description` is recommended. "Standard" = part of the [Agent Skills](https://agentskills.io) open spec; everything else is a Claude Code extension.

| Field | Standard | Default | Description |
|-------|----------|---------|-------------|
| `name` | ✓ | directory name | Lowercase letters, numbers, hyphens. Max 64 chars. |
| `description` | ✓ | — | What it does AND when to use it. Claude uses this for auto-discovery. **Combined with `when_to_use`, truncated at 1,536 characters in the skill listing** (not 1,024 — that limit is from a different spec). |
| `when_to_use` | — | No | Additional context for when to invoke, such as trigger phrases. Appended to `description` in the listing and counts toward the 1,536 cap. **Prefer putting trigger phrases here over squeezing them into `description`.** |
| `argument-hint` | — | — | Autocomplete hint. Example: `[issue-number]`. **Must be removed before packaging outside Claude Code — see "Packaging Compatibility" below (hard error).** |
| `disable-model-invocation` | — | `false` | Prevents Claude from auto-loading. For manual workflows with side effects. |
| `user-invocable` | — | `true` | Set `false` to hide from `/` menu. For background knowledge. |
| `allowed-tools` | ✓ | — | Tools Claude can use without permission prompts. Example: `Read, Bash(git *)`. |
| `disallowed-tools` | — | — | Tools **removed** from Claude's available pool while this skill is active — the safety counterpart of `allowed-tools`. Accepts space/comma-separated string or YAML list. Restriction clears on the next message. Can't remove `EndConversation` while any other tool remains. |
| `paths` | — | — | Glob patterns limiting when the skill auto-activates. When set, loads only while working with matching files. Same format as path-specific rules. |
| `model` | — | inherited | Force a specific model: `haiku`, `sonnet`, `opus`. Prefer leaving unset — the skill shouldn't hard-code its creator's model. |
| `context` | — | — | Set `fork` to run in isolated subagent context. |
| `agent` | — | — | Subagent type when `context: fork`: `Explore`, `Plan`, `general-purpose`, or custom agent name. |
| `hooks` | — | — | Hooks scoped to this skill's lifecycle. See Hooks in Skills below. |
| `metadata` | ✓ | — | Free-form YAML map for your own key-value data (entitlement, catalog). Claude Code doesn't act on it; drops values that aren't a map. Don't reuse field names like `paths` as keys. |
| `license` | ✓ | — | License covering the skill. Claude Code accepts but doesn't act on it. |
| `compatibility` | ✓ | — | Environment requirements (intended products, system prerequisites). Up to 500 chars. Claude Code accepts but doesn't act on it. |

## Packaging Compatibility（Claude Code 之外）

Claude Code follows the Agent Skills open standard and extends it. **Outside Claude Code** (claude.ai upload, Skills API, `package_skill.py`), only the six standard fields are accepted:

```
allowed-tools, compatibility, description, license, metadata, name
```

Any other key is a **hard error, not a silent ignore**:

```
Unexpected key(s) in SKILL.md frontmatter: argument-hint.
```

Consequences for this skill's templates: an `argument-hint` emitted by `templates/` will break packaging on those distribution paths. Body-only features (dynamic context injection, subagent execution) don't function outside Claude Code. Claude Code accepts the six standard fields unchanged, so spec-compliant frontmatter loads in Claude Code without modification.

## Invocation Control

| Frontmatter | User invokes | Claude invokes | When loaded |
|-------------|-------------|----------------|-------------|
| (default) | Yes | Yes | Description always in context; full content on invocation |
| `disable-model-invocation: true` | Yes | No | Description NOT in context; loads only when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; loads when relevant |

**Use `disable-model-invocation: true`** for workflows with side effects: deploy, commit, triage, send messages. Prevents Claude from deciding to deploy because your code looks ready.

**Use `user-invocable: false`** for background knowledge: coding conventions, domain context, legacy system docs.

## 成本：技能是每轮常驻的税金

- **技能列表里的每个技能每轮都在消耗 context，无论是否被使用。** 精简不是审美，是每轮烧掉的 token——这是"渐进式披露"最有力的论据：metadata（name + description）常驻（截断于 1,536），正文触发时才加载（<500 行），支撑文件按需（不限）。
- **`/skill-doctor`（Claude Code）** 可查看每个技能的成本与使用情况——构建后用它核对自己技能的真实占用。

## Skill Locations & Priority

```
Enterprise (highest) → Personal → Project → Plugin (lowest)
```

| Type | Path |
|------|------|
| Personal | `~/.claude/skills/<name>/SKILL.md` |
| Project | `.claude/skills/<name>/SKILL.md` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` (namespaced as `plugin:skill`) |

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking |
| `$ARGUMENTS[N]` or `$N` | Specific argument by 0-based index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing the skill's SKILL.md. Claude Code 内用它引用自带文件；**跨 agent 用"路径相对于技能自身目录"约定（见 SKILL.md 顶部）** |
| `${CLAUDE_PLUGIN_DATA}` | Stable folder for data that persists beyond skill upgrades. Use for logs, config, cached results. |

If `$ARGUMENTS` is not present in the skill content, arguments are appended automatically.

## Dynamic Context Injection

The `` !`command` `` syntax runs shell commands before content reaches Claude:

```markdown
## Context
- Current branch: !`git branch --show-current`
- Changed files: !`gh pr diff --name-only`
```

Commands execute at load time. Claude only sees the output. Claude Code only.

## Subagent Execution

Add `context: fork` to run in isolation:

```yaml
---
name: deep-research
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly...
```

The skill content becomes the subagent's prompt. No access to conversation history. Claude Code only.

## Hooks in Skills

Skills can define lifecycle hooks via the `hooks` frontmatter field. These run shell commands at specific points during skill execution.

**Use cases:**
- **Safety guardrails** — Block destructive commands (`rm -rf`, `DROP TABLE`, `force-push`) while the skill is active
- **Directory constraints** — Restrict edits to specific paths during the skill's execution
- **Logging** — Track skill invocations for usage measurement
- **Setup/teardown** — Run setup scripts when the skill starts, cleanup when it ends

Hooks defined in a skill are scoped to that skill's lifecycle only. Claude Code only.

## Persistent Data Storage

Skills that need to store data across invocations can use `${CLAUDE_PLUGIN_DATA}`. This is distinct from the skill directory itself, which may be overwritten on updates.

## Writing Effective Descriptions

**Frame descriptions as trigger conditions, not summaries.** Claude scans descriptions to decide when to invoke a skill. Write them as "when should the agent reach for this?" not "what does this skill contain?" — and move trigger phrases to `when_to_use` where available.

```yaml
# Good — trigger-oriented, tells the agent WHEN to activate
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Bad — summary that doesn't tell the agent when to activate
description: Helps with documents

# Bad — describes contents instead of triggers
description: A comprehensive guide to PDF manipulation with examples and best practices
```

To verify a description actually triggers correctly (not just reads well), run trigger-evaluation — see [trigger-evaluation.md](trigger-evaluation.md). Authoring triggers is not the same as verifying they fire.

## Key Rules

- SKILL.md under 500 lines — split detailed content into reference files
- Standard markdown headings — `##`, `###` (not XML tags)
- Concrete examples — not abstract descriptions
- Consistent terminology throughout
- No time-sensitive information (use "current method" / "legacy" pattern)
- Default to one recommended approach with escape hatch, not a menu of options
- `disable-model-invocation: true` for any workflow with side effects — or, where the whole skill must stay auto-invocable, isolate the side-effecting steps behind a manual-only entry point (this skill's own pattern for publishing)
- Test with real usage scenarios, not test cases

## Distribution

- **Project skills**: Commit `.claude/skills/` to version control
- **Plugins**: Add `skills/` directory to plugin
- **Enterprise**: Deploy via managed settings
- **Marketplace**: Package and publish — verify the six-field frontmatter rule above before packaging
