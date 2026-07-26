#!/usr/bin/env python3
"""Validate the software-evolution skill structure, contracts, and local links."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


REQUIRED_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
    "workflows/common-loop.md",
    "workflows/init.md",
    "workflows/audit.md",
    "workflows/govern.md",
    "workflows/repair.md",
    "workflows/verify.md",
    "workflows/deep.md",
    "workflows/release-check.md",
    "workflows/observe.md",
    "workflows/resume.md",
    "governance/mode-contracts.md",
    "governance/autonomy-and-risk.md",
    "governance/user-experience.md",
    "governance/code-quality-and-reliability.md",
    "governance/architecture-and-capabilities.md",
    "governance/evolution-and-business-consistency.md",
    "governance/testing-and-validation.md",
    "governance/technical-debt-and-memory.md",
    "governance/specialist-routing.md",
    "governance/decision-governance.md",
    "governance/release-and-migrations.md",
    "governance/observability-and-sre.md",
    "governance/budget-and-drift.md",
    "governance/architecture-fitness.md",
    "templates/finding-record.md",
    "templates/repair-plan.md",
    "templates/verification-record.md",
    "templates/governance-report.md",
    "templates/audit-report.md",
    "templates/verification-report.md",
    "templates/release-readiness.md",
    "templates/observation-report.md",
    "templates/incident-review.md",
    "templates/decision-record.md",
    "templates/batch-checkpoint.md",
    "templates/specialist-handoff.md",
    "memory/architecture-memory.template.md",
    "memory/capability-map.template.md",
    "memory/technical-debt.template.md",
    "memory/software-evolution.config.template.yml",
    "memory/health-baseline.template.json",
    "scripts/bootstrap_project_memory.py",
    "scripts/check_skill_integrity.py",
    "scripts/validate_project_config.py",
    "scripts/check_checkpoint_drift.py",
}
MODE_WORKFLOWS = {
    "init": ("workflows/init.md", "WRITE POLICY: CONTROL_PLANE_ONLY"),
    "audit": ("workflows/audit.md", "WRITE POLICY: READ_ONLY"),
    "govern": ("workflows/govern.md", "WRITE POLICY: BOUNDED_WRITE"),
    "repair": ("workflows/repair.md", "WRITE POLICY: BOUNDED_WRITE"),
    "verify": ("workflows/verify.md", "WRITE POLICY: READ_ONLY"),
    "deep": ("workflows/deep.md", "WRITE POLICY: BUDGETED_WRITE"),
    "release-check": ("workflows/release-check.md", "WRITE POLICY: READ_ONLY"),
    "observe": ("workflows/observe.md", "WRITE POLICY: READ_ONLY"),
    "resume": ("workflows/resume.md", "WRITE POLICY: INHERITED_OR_READ_ONLY"),
}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
CHECKPOINT_COMMENT_RE = re.compile(
    r"<!--\s*software-evolution-checkpoint\s*(\{.*?\})\s*-->", re.DOTALL
)
LOCAL_PATH_RE = re.compile(r"(?:/Users/[^\s`]+|[A-Za-z]:\\\\Users\\\\[^\s`]+)")
SECRET_MARKERS = ("-----BEGIN PRIVATE KEY-----", "-----BEGIN OPENSSH PRIVATE KEY-----")


def validate_frontmatter(root: Path, errors: list[str]) -> str:
    path = root / "SKILL.md"
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append("SKILL.md has no valid YAML frontmatter block")
        return text
    frontmatter = match.group(1)
    fields = [
        line.split(":", 1)[0].strip()
        for line in frontmatter.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and ":" in line
    ]
    if fields != ["name", "description"]:
        errors.append("SKILL.md frontmatter must contain only name and description in that order")
    if "name: software-evolution" not in frontmatter:
        errors.append("SKILL.md name must be software-evolution")
    body_lines = text[match.end() :].splitlines()
    if len(body_lines) > 500:
        errors.append(f"SKILL.md body has {len(body_lines)} lines; maximum is 500")
    if re.search(r"\bTODO\b", text, re.IGNORECASE):
        errors.append("SKILL.md still contains TODO text")
    return text


def validate_links(root: Path, errors: list[str]) -> None:
    for markdown in sorted(root.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            clean = target.strip().split("#", 1)[0]
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            link_path = (markdown.parent / clean).resolve()
            try:
                link_path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{markdown.relative_to(root)} link escapes skill root: {target}")
                continue
            if not link_path.exists():
                errors.append(f"broken link in {markdown.relative_to(root)}: {target}")


def validate_templates(root: Path, errors: list[str]) -> None:
    for template_name in (
        "architecture-memory.template.md",
        "capability-map.template.md",
        "technical-debt.template.md",
        "health-baseline.template.json",
    ):
        path = root / "memory" / template_name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token in ("{{PROJECT_NAME}}", "{{DATE}}", "{{REPOSITORY_REFERENCE}}"):
            if token not in text:
                errors.append(f"{template_name} missing placeholder {token}")

    health = root / "memory" / "health-baseline.template.json"
    if health.is_file():
        rendered = (
            health.read_text(encoding="utf-8")
            .replace("{{PROJECT_NAME}}", "sample")
            .replace("{{DATE}}", "2026-07-26")
            .replace("{{REPOSITORY_REFERENCE}}", "sample")
        )
        try:
            json.loads(rendered)
        except json.JSONDecodeError as exc:
            errors.append(f"health baseline template is invalid JSON: {exc}")

    checkpoint = root / "templates" / "batch-checkpoint.md"
    if checkpoint.is_file():
        match = CHECKPOINT_COMMENT_RE.search(checkpoint.read_text(encoding="utf-8"))
        if not match:
            errors.append("batch checkpoint template has no parseable metadata comment")
        else:
            try:
                metadata = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                errors.append(f"batch checkpoint metadata is invalid JSON: {exc}")
            else:
                required = {
                    "schema_version",
                    "batch_id",
                    "mode",
                    "branch",
                    "head",
                    "worktree_fingerprint",
                    "worktree_entries",
                    "worktree_path_fingerprints",
                    "scope_paths",
                }
                missing = sorted(required - set(metadata))
                if missing:
                    errors.append(
                        "batch checkpoint metadata missing fields: " + ", ".join(missing)
                    )
                if metadata.get("schema_version") != 1:
                    errors.append("batch checkpoint schema_version must be 1")

    config = root / "memory" / "software-evolution.config.template.yml"
    validator = root / "scripts" / "validate_project_config.py"
    if config.is_file() and validator.is_file():
        with tempfile.TemporaryDirectory(prefix="software-evolution-integrity-") as tmp:
            candidate = Path(tmp) / ".software-evolution.yml"
            candidate.write_text(config.read_text(encoding="utf-8"), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(validator), "--config", str(candidate)],
                text=True,
                capture_output=True,
            )
            if result.returncode != 0:
                errors.append(
                    "project config template failed validation: "
                    + (result.stdout + result.stderr).strip()
                )


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_text = validate_frontmatter(root, errors)
    validate_links(root, errors)
    validate_templates(root, errors)

    for mode, (relative, marker) in MODE_WORKFLOWS.items():
        path = root / relative
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if marker not in text:
                errors.append(f"{relative} missing mode marker: {marker}")
        if mode not in skill_text:
            errors.append(f"SKILL.md does not mention mode: {mode}")
        if relative not in skill_text:
            errors.append(f"SKILL.md does not link workflow: {relative}")

    agent_yaml = root / "agents/openai.yaml"
    if agent_yaml.is_file():
        agent_text = agent_yaml.read_text(encoding="utf-8")
        for key in ("display_name:", "short_description:", "default_prompt:"):
            if key not in agent_text:
                errors.append(f"agents/openai.yaml missing {key}")
        if "$software-evolution" not in agent_text:
            errors.append("agents/openai.yaml default_prompt must mention $software-evolution")

    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root)
        if relative.as_posix() == "scripts/check_skill_integrity.py":
            continue  # This validator necessarily contains the detection patterns.
        if path.suffix.lower() not in {".md", ".yml", ".yaml", ".json", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if LOCAL_PATH_RE.search(text):
            errors.append(f"non-portable local user path in {path.relative_to(root)}")
        for marker in SECRET_MARKERS:
            if marker in text:
                errors.append(f"secret/private-key marker in {path.relative_to(root)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} error(s)")
        return 1

    print(
        f"OK: {len(REQUIRED_FILES)} required files, {len(MODE_WORKFLOWS)} mode contracts, "
        "frontmatter, links, metadata, templates, and portability validated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
