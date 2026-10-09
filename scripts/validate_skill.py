#!/usr/bin/env python3
"""
validate_skill.py — deterministic skill checks. Pure Python standard library,
no dependencies, runs in any agent environment.

Usage:
    python validate_skill.py <skill-directory>

Exit code:
    0 = no errors (warnings allowed and printed)
    1 = errors found

Checks mirror the deterministic items in references/quality-checklist.md:
frontmatter validity, name/description rules, the 1,536-char listing cap,
packaging compatibility (six-field rule), line counts, link integrity,
orphan files, and drift (hard-coded years, model names).

What this script CANNOT check (still manual, per the checklist): synthesis
quality, gotcha depth, interactivity, evaluation completeness.
"""

import re
import sys
from pathlib import Path

STANDARD_FIELDS = {
    "name", "description", "license", "compatibility", "metadata", "allowed-tools",
}


def strip_quotes(value):
    """Strip one pair of surrounding single/double quotes, unescape inner quotes."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        quote = value[0]
        inner = value[1:-1]
        if quote == '"':
            inner = inner.replace('\\"', '"').replace('\\\\', '\\')
        else:
            inner = inner.replace("\\'", "'")
        return inner
    return value


def parse_frontmatter(text):
    """Minimal YAML-ish frontmatter parser for the flat key: value fields skills
    use. Handles quoted strings, inline lists [a, b], block lists (- item),
    empty values, comments, and indented subkeys (metadata maps).
    Returns (dict, error)."""
    if not text.startswith("---"):
        return None, "missing frontmatter (SKILL.md must start with ---)"
    lines = text.splitlines()
    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    else:
        return None, "unterminated frontmatter (no closing ---)"

    fm = {}
    current_key = None
    for raw in fm_lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 0 and ":" in raw:
            key, _, val = raw.partition(":")
            key = key.strip()
            val = val.strip()
            current_key = key
            if not val:
                fm[key] = None
            elif val.startswith("[") and val.endswith("]"):
                fm[key] = [
                    strip_quotes(v.strip())
                    for v in val[1:-1].split(",")
                    if v.strip()
                ]
            else:
                fm[key] = strip_quotes(val)
        elif indent >= 2 and current_key:
            if stripped.startswith("- "):
                item = strip_quotes(stripped[2:].strip())
                entry = fm.get(current_key)
                if not isinstance(entry, list):
                    entry = []
                    fm[current_key] = entry
                entry.append(item)
            elif ":" in stripped:
                subkey, _, subval = stripped.partition(":")
                subval = subval.strip()
                entry = fm.get(current_key)
                if not isinstance(entry, dict):
                    entry = {}
                    fm[current_key] = entry
                entry[subkey.strip()] = strip_quotes(subval) if subval else None
    return fm, None


def check_skill(skill_dir):
    errors, warnings = [], []
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md not found"], warnings

    content = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, err = parse_frontmatter(content)
    if err:
        errors.append(err)
    else:
        # name
        name = fm.get("name")
        if not name:
            errors.append("missing 'name' in frontmatter")
        else:
            if not re.fullmatch(r"[a-z0-9-]+", str(name)):
                errors.append(f"name '{name}' must be kebab-case (lowercase letters, digits, hyphens)")
            if str(name).startswith("-") or str(name).endswith("-") or "--" in str(name):
                errors.append(f"name '{name}' cannot start/end with hyphen or contain '--'")
            if len(str(name)) > 64:
                errors.append(f"name too long ({len(name)} chars; max 64)")
            if str(name) != skill_dir.name:
                warnings.append(f"frontmatter name '{name}' != directory name '{skill_dir.name}'")

        # description + when_to_use combined cap
        desc = str(fm.get("description") or "")
        wtu = str(fm.get("when_to_use") or "")
        if not desc:
            errors.append("missing 'description' in frontmatter")
        if "<" in desc or ">" in desc:
            errors.append("description cannot contain angle brackets (< or >)")
        if len(desc) + len(wtu) > 1536:
            errors.append(f"description+when_to_use = {len(desc) + len(wtu)} chars, over the 1,536 listing cap")

        # packaging compatibility
        nonstandard = sorted(set(fm) - STANDARD_FIELDS)
        if nonstandard:
            warnings.append(
                f"non-standard frontmatter keys {nonstandard} — CLI agents ignore them, "
                "but they hard-error when packaged to claude.ai / Skills API (see official-spec)"
            )

        # line counts
        line_count = len(content.splitlines())
        if line_count > 500:
            errors.append(f"SKILL.md is {line_count} lines (max 500)")
        elif line_count > 300:
            warnings.append(f"SKILL.md is {line_count} lines — over the router target (~300)")

        # drift: hard-coded years and model names in the body
        body = content.split("---", 2)[-1]
        for m in re.finditer(r"\b20(?:2[5-9]|3[0-9])\b", body):
            line_no = body[: m.start()].count("\n") + 1
            warnings.append(f"hard-coded year '{m.group(0)}' in body (line {line_no}) — use 'current' phrasing")
        for kw in ("Sonnet", "haiku", "opus", "Claude Code only"):
            for m in re.finditer(rf"\b{re.escape(kw)}\b", body):
                line_no = body[: m.start()].count("\n") + 1
                warnings.append(f"model/host hard-code '{kw}' in body (line {line_no}) — keep agent-agnostic")
                break

    # link integrity: backtick paths and markdown links to known subdirs
    link_re = re.compile(
        r"`((?:references|workflows|templates|scripts)/[A-Za-z0-9_./\-]+)`"
        r"|\[[^\]]*\]\(((?:references|workflows|templates|scripts)/[A-Za-z0-9_./\-]+)\)"
    )
    for m in link_re.finditer(content):
        target = m.group(1) or m.group(2)
        if not (skill_dir / target).exists():
            errors.append(f"SKILL.md links to missing file: {target}")

    # orphan scan: every non-SKILL.md file should be mentioned somewhere
    all_text = ""
    for f in skill_dir.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".py", ".json"):
            try:
                all_text += f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
    for f in sorted(skill_dir.rglob("*")):
        if f.is_file() and f.name != "SKILL.md" and f.suffix in (".md", ".py", ".json"):
            rel = f.relative_to(skill_dir).as_posix()
            if rel not in all_text and f.name not in all_text:
                warnings.append(f"orphan file (never referenced): {rel}")

    return errors, warnings


def main(argv):
    if len(argv) != 1:
        print("usage: python validate_skill.py <skill-directory>")
        return 2
    errors, warnings = check_skill(argv[0])
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"FAIL: {e}")
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) — skill is NOT valid")
        return 1
    print(f"\nOK — {len(warnings)} warning(s). Skill is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
