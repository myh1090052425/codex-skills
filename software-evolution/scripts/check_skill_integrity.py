#!/usr/bin/env python3
"""Validate the software-evolution skill's internal structure and Markdown links."""

from __future__ import annotations

import re
from pathlib import Path
import sys


REQUIRED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "workflows/common-loop.md",
    "workflows/init.md",
    "workflows/govern.md",
    "workflows/deep.md",
    "workflows/repair.md",
    "governance/autonomy-and-risk.md",
    "governance/user-experience.md",
    "governance/code-quality-and-reliability.md",
    "governance/architecture-and-capabilities.md",
    "governance/evolution-and-business-consistency.md",
    "governance/testing-and-validation.md",
    "governance/technical-debt-and-memory.md",
    "templates/finding-record.md",
    "templates/repair-plan.md",
    "templates/verification-record.md",
    "templates/governance-report.md",
    "memory/architecture-memory.template.md",
    "memory/capability-map.template.md",
    "memory/technical-debt.template.md",
    "scripts/bootstrap_project_memory.py",
    "scripts/check_skill_integrity.py",
}

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    warnings: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(skill_text)
        if not match:
            errors.append("SKILL.md has no valid YAML frontmatter block")
        else:
            frontmatter = match.group(1)
            fields = [
                line.split(":", 1)[0].strip()
                for line in frontmatter.splitlines()
                if line.strip() and not line.lstrip().startswith("#") and ":" in line
            ]
            if fields != ["name", "description"]:
                errors.append(
                    "SKILL.md frontmatter must contain only name and description in that order"
                )
            if "name: software-evolution" not in frontmatter:
                errors.append("SKILL.md name must be software-evolution")

        for target in LINK_RE.findall(skill_text):
            if target.startswith(("http://", "https://", "#")):
                continue
            link_path = (root / target.split("#", 1)[0]).resolve()
            try:
                link_path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"SKILL.md link escapes skill root: {target}")
                continue
            if not link_path.exists():
                errors.append(f"broken SKILL.md link: {target}")

        if re.search(r"\bTODO\b", skill_text, re.IGNORECASE):
            errors.append("SKILL.md still contains TODO text")

        body_lines = skill_text[match.end() :].splitlines() if match else skill_text.splitlines()
        if len(body_lines) > 500:
            warnings.append(f"SKILL.md body has {len(body_lines)} lines; keep it under 500")

    agent_yaml = root / "agents/openai.yaml"
    if agent_yaml.is_file():
        agent_text = agent_yaml.read_text(encoding="utf-8")
        for key in ("display_name:", "short_description:", "default_prompt:"):
            if key not in agent_text:
                errors.append(f"agents/openai.yaml missing {key}")
        if "$software-evolution" not in agent_text:
            errors.append("agents/openai.yaml default_prompt must mention $software-evolution")

    for template_name in (
        "architecture-memory.template.md",
        "capability-map.template.md",
        "technical-debt.template.md",
    ):
        template = root / "memory" / template_name
        if template.is_file():
            text = template.read_text(encoding="utf-8")
            for token in ("{{PROJECT_NAME}}", "{{DATE}}", "{{REPOSITORY_PATH}}"):
                if token not in text:
                    errors.append(f"{template_name} missing placeholder {token}")

    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(
        f"OK: {len(REQUIRED_FILES)} required files, frontmatter, links, metadata, and templates validated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
