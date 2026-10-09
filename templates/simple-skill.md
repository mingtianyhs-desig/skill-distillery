# Simple Skill Template

Use this template for single-workflow skills. Target under 150 lines for Quick Personal skills and under 200 lines for shared simple skills. Copy, customize, and delete anything that is not needed at runtime.

```markdown
---
name: {{SKILL_NAME}}
description: "{{What it does}}. Use when {{trigger conditions}}. Triggers on: {{keyword1}}, {{keyword2}}, {{keyword3}}."
# argument-hint 仅 Claude Code 识别（autocomplete 提示）。若经 claude.ai 上传 / Skills API /
# package_skill.py 分发，必须删除此字段——否则硬报错 "Unexpected key(s) in SKILL.md frontmatter"。
# argument-hint: "[{{expected input}}]"
allowed-tools: Read, Bash
---

# {{Skill Display Name}}

{{1-2 sentence operational premise. What should the agent remember while doing the work?}}

## Quick Start

**Example invocations:**
> "{{example user input 1}}"
> "{{example user input 2}}"

---

## Core Checks

{{2-4 operational checks. These are things the agent actively verifies, not background philosophy.}}

1. **{{Check 1}}** — {{What to verify}}
2. **{{Check 2}}** — {{What to verify}}
3. **{{Check 3}}** — {{What to verify}}

---

## Workflow

1. **{{Intake}}** — {{What to read or ask. Ask only the minimum needed questions.}}
2. **{{Execute}}** — {{Core steps.}}
3. **{{Verify}}** — {{How to check the result before responding.}}
4. **{{Deliver}}** — {{Output shape.}}

---

## Optional Modes

{{Delete this section unless the skill truly has distinct workflows. If modes are needed, route by user intent first and ask only when ambiguous.}}

| Signal | Mode | Do |
|--------|------|----|
| {{User asks for X}} | {{Mode A}} | {{Action}} |
| {{User asks for Y}} | {{Mode B}} | {{Action}} |

---

## Gotchas

Common failure points — where Claude gets this wrong:

- **Don't {{X}}** because {{Y}}. Instead, {{correct approach}}.
- **Don't {{X}}** because {{Y}}. Instead, {{correct approach}}.
- **Don't {{X}}** because {{Y}}. Instead, {{correct approach}}.

---

## Working With Incomplete Information

{{Delete if obvious. Include only the minimum policy for missing inputs.}}

{{Optional: For deeper procedure, see [reference.md](reference.md).}}
```

## Customization Notes

- **Delete unused sections** — If no modes needed, remove the mode selection and collapse into a single workflow
- **Keep research out** — Put rationale, raw notes, and eval prompts outside SKILL.md unless needed at runtime
- **Add wait gates** only at genuine decision points
- **Keep under the lane target** — <150 lines for Quick Personal, <200 for simple shared skills
- **Description + `when_to_use`** combined are truncated at **1,536 chars** in the skill listing — keep trigger keywords specific and inside that cap
