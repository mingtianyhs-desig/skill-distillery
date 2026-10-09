# Skill Evals Template

Use for Team Internal and Public Polished skills. Delete sections that exceed the chosen lane.

```markdown
# Skill Evals

Skill: {{SKILL_NAME}}
Lane: {{Quick Personal / Team Internal / Public Polished}}

## How to Run

Run each prompt below **twice**: once with the skill available, once without it (baseline), in fresh sessions. Record the **actual** result next to each Expected — what really happened, not what you predicted. If with-skill and baseline both pass identically, the prompt has no discriminating power (ceiling effect); prefer prompts where behavior quality differs (rounds taken, when a tactic switches), not just pass/fail.

## Positive Triggers

- Prompt: "{{Prompt that should activate the skill}}"
  Expected: {{What the agent should do}}
  Actual: {{recorded result from the real run}}

- Prompt: "{{Prompt that should activate the skill}}"
  Expected: {{What the agent should do}}
  Actual: {{recorded result from the real run}}

## Non-Triggers

- Prompt: "{{Adjacent request that should not activate the skill}}"
  Expected: {{What should happen instead}}
  Actual: {{recorded result — did it stay silent?}}

## Representative Tasks

- Prompt: "{{Realistic task}}"
  Expected: {{Workflow or output shape}}
  Actual: {{recorded result — which steps were taken?}}
  Success signals:
  - {{Signal}}
  - {{Signal}}

## Incomplete Context

- Prompt: "{{Request missing an important input}}"
  Expected: {{Question, fallback, or safe behavior}}
  Actual: {{recorded result}}

## Edge Cases

Use for Public Polished skills.

- Prompt: "{{Messy, adversarial, or ambiguous task}}"
  Expected: {{Correct boundary or behavior}}
  Actual: {{recorded result}}
  Failure signals:
  - {{Signal}}
  - {{Signal}}

## Fresh-Agent Test

Use for Public Polished skills.

- Install/load steps:
- Positive trigger result: {{from actual run}}
- Representative task result: {{from actual run}}
- Non-trigger result: {{from actual run}}
- Baseline comparison: {{did with-skill differ from without-skill?}}
- Limitations:
```
