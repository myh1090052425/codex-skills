#!/usr/bin/env python3
"""Validate Software Evolution RUN metadata and completion evidence gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


RUN_COMMENT_RE = re.compile(
    r"<!--\s*software-evolution-run\s*(\{.*?\})\s*-->", re.DOTALL
)
SCHEMA_VERSION = 3
CORE_LANES = (
    "user_business",
    "engineering_reliability",
    "architecture_evolution",
)
LANE_STATES = {"pending", "covered", "blocked"}
RUNTIME_UX_STATES = {"pending", "covered", "blocked", "not_applicable"}
CHALLENGE_STATES = {"pending", "passed", "blocked"}
RUN_STATUSES = {
    "running",
    "verification",
    "completed",
    "partial",
    "blocked",
    "failed",
    "interrupted",
}
TERMINAL_REASONS = {
    "",
    "safe_work_exhausted",
    "authority_evidence_environment_blocked",
    "protected_boundary",
    "drift",
    "failure_exhaustion",
    "host_interruption",
}
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "run_id",
    "profile",
    "status",
    "branch",
    "head",
    "scope_kind",
    "scope_paths",
    "latest_batch_id",
    "predecessor_run_id",
    "invocation_id",
    "host_deadline",
    "last_heartbeat_at",
    "coverage",
    "terminal_reason",
}
REQUIRED_COVERAGE = {
    *CORE_LANES,
    "runtime_ux",
    "cross_lane_challenge",
    "open_repair_ready_work",
}
REQUIRED_HEADINGS = (
    "## Governance coverage matrix",
    "## Aggregate verification",
    "## Completion challenge",
    "## Stop and continuation",
)
COMPLETION_LABELS = (
    "Fresh cross-lane counterexample search",
    "Open Ready/In-progress debt and finding reconciliation",
    "Recent/unclassified change review",
    "Capability duplicate and business-rule split challenge",
    "Critical journey and runtime UX evidence/blocker",
    "Repair-ready work remaining",
    "validate_run_completion.py",
)
PLACEHOLDER_METADATA = {
    "RUN-TBD",
    "FULL_GIT_SHA",
    "INV-TBD",
    "ISO-8601-TBD",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Software Evolution RUN ledger before completion."
    )
    parser.add_argument("--run", required=True, help="Path to RUN-*.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    return parser.parse_args()


def load_run(path: Path) -> tuple[dict[str, Any] | None, str, list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return None, "", [f"run file does not exist: {path}"]
    text = path.read_text(encoding="utf-8")
    match = RUN_COMMENT_RE.search(text)
    if not match:
        return None, text, ["run file has no parseable software-evolution-run metadata"]
    try:
        metadata = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        return None, text, [f"run metadata is invalid JSON: {exc}"]
    if not isinstance(metadata, dict):
        errors.append("run metadata must be a JSON object")
        return None, text, errors
    return metadata, text, errors


def section_body(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    match = re.search(r"^## ", text[start:], re.MULTILINE)
    end = len(text) if match is None else start + match.start()
    return text[start:end].strip()


def has_placeholder(value: Any) -> bool:
    return not isinstance(value, str) or not value.strip() or value in PLACEHOLDER_METADATA or "TBD" in value


def validate(metadata: dict[str, Any], text: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(metadata))
    if missing:
        errors.append("run metadata missing fields: " + ", ".join(missing))
        return errors

    if metadata.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"run schema_version must be {SCHEMA_VERSION}; migrate an active legacy run before claiming completion"
        )

    status = metadata.get("status")
    if status not in RUN_STATUSES:
        errors.append(f"unsupported run status: {status!r}")

    if metadata.get("profile") not in {"autopilot", "overnight", "deep"}:
        errors.append("profile must be autopilot, overnight, or deep")
    if not isinstance(metadata.get("run_id"), str) or not metadata["run_id"].startswith("RUN-"):
        errors.append("run_id must be a RUN-* identifier")
    for key in ("branch", "head", "invocation_id", "last_heartbeat_at"):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            errors.append(f"{key} must be a non-empty string")

    scope_kind = metadata.get("scope_kind")
    scope_paths = metadata.get("scope_paths")
    if scope_kind not in {"repository", "scoped"}:
        errors.append("scope_kind must be repository or scoped")
    if not isinstance(scope_paths, list) or not scope_paths or not all(
        isinstance(item, str) and item.strip() for item in scope_paths
    ):
        errors.append("scope_paths must be a non-empty string list")
    else:
        for item in scope_paths:
            if (
                item.startswith(("/", "\\"))
                or re.match(r"^[A-Za-z]:[\\/]", item)
                or ".." in Path(item).parts
            ):
                errors.append(f"scope path must be repository-relative and non-escaping: {item}")
        if scope_kind == "repository" and "." not in scope_paths:
            errors.append("repository scope must retain '.' in scope_paths")

    coverage = metadata.get("coverage")
    if not isinstance(coverage, dict):
        errors.append("coverage must be an object")
        coverage = {}
    missing_coverage = sorted(REQUIRED_COVERAGE - set(coverage))
    if missing_coverage:
        errors.append("coverage missing fields: " + ", ".join(missing_coverage))

    for lane in CORE_LANES:
        if lane in coverage and coverage[lane] not in LANE_STATES:
            errors.append(f"coverage.{lane} must be pending, covered, or blocked")
    if (
        "runtime_ux" in coverage
        and coverage["runtime_ux"] not in RUNTIME_UX_STATES
    ):
        errors.append(
            "coverage.runtime_ux must be pending, covered, blocked, or not_applicable"
        )
    if (
        "cross_lane_challenge" in coverage
        and coverage["cross_lane_challenge"] not in CHALLENGE_STATES
    ):
        errors.append(
            "coverage.cross_lane_challenge must be pending, passed, or blocked"
        )
    if "open_repair_ready_work" in coverage and type(
        coverage["open_repair_ready_work"]
    ) is not bool:
        errors.append("coverage.open_repair_ready_work must be boolean")

    terminal_reason = metadata.get("terminal_reason")
    if terminal_reason not in TERMINAL_REASONS:
        errors.append(f"unsupported terminal_reason: {terminal_reason!r}")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"run ledger missing heading: {heading}")

    if status in {"running", "verification"} and terminal_reason != "":
        errors.append(f"{status} run must not have a terminal_reason")

    if status == "completed":
        for key in ("run_id", "branch", "head", "invocation_id", "last_heartbeat_at"):
            if has_placeholder(metadata.get(key)):
                errors.append(f"completed run requires non-placeholder {key}")
        if not re.fullmatch(r"[0-9a-fA-F]{40}|[0-9a-fA-F]{64}", str(metadata.get("head", ""))):
            errors.append("completed run head must be a full Git commit SHA")
        if terminal_reason != "safe_work_exhausted":
            errors.append(
                "completed runs must use terminal_reason safe_work_exhausted; blockers and host interruption are not completion"
            )
        for lane in CORE_LANES:
            if coverage.get(lane) not in {"covered", "blocked"}:
                errors.append(
                    f"completed run requires coverage.{lane}=covered or blocked"
                )
        if coverage.get("runtime_ux") not in {
            "covered",
            "blocked",
            "not_applicable",
        }:
            errors.append(
                "completed run requires runtime UX evidence, an explicit blocker, or a proven non-UI scope"
            )
        if coverage.get("cross_lane_challenge") != "passed":
            errors.append(
                "completed run requires a passed cross-lane completion challenge"
            )
        if coverage.get("open_repair_ready_work") is not False:
            errors.append(
                "completed run cannot retain open repair-ready work"
            )

        coverage_section = section_body(text, "## Governance coverage matrix")
        aggregate_section = section_body(text, "## Aggregate verification")
        challenge_section = section_body(text, "## Completion challenge")
        stop_section = section_body(text, "## Stop and continuation")
        for heading, body in (
            ("Governance coverage matrix", coverage_section),
            ("Aggregate verification", aggregate_section),
            ("Completion challenge", challenge_section),
            ("Stop and continuation", stop_section),
        ):
            if not body:
                errors.append(f"completed run requires populated {heading}")
            elif "TBD" in body:
                errors.append(f"completed run {heading} still contains TBD evidence")
        for label in COMPLETION_LABELS:
            if label not in challenge_section:
                errors.append(f"completion challenge missing evidence label: {label}")
        if not re.search(
            r"Repair-ready work remaining:\s*`?no\b",
            challenge_section,
            re.IGNORECASE,
        ):
            errors.append("completion challenge must explicitly record no repair-ready work")
        validator_line = next(
            (line for line in challenge_section.splitlines() if "validate_run_completion.py" in line),
            "",
        )
        if "OK" not in validator_line:
            errors.append("completion challenge must record validate_run_completion.py result OK")
    elif status in {"partial", "blocked", "failed", "interrupted"}:
        if terminal_reason == "":
            errors.append(f"{status} run requires a real terminal_reason")
        allowed_by_status = {
            "partial": {
                "authority_evidence_environment_blocked",
                "protected_boundary",
                "drift",
                "failure_exhaustion",
                "host_interruption",
            },
            "blocked": {
                "authority_evidence_environment_blocked",
                "protected_boundary",
                "drift",
            },
            "failed": {"failure_exhaustion"},
            "interrupted": {"host_interruption"},
        }
        if terminal_reason not in allowed_by_status[status]:
            errors.append(
                f"terminal_reason {terminal_reason!r} is inconsistent with status {status}"
            )

    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.run)
    metadata, text, errors = load_run(path)
    if metadata is not None:
        errors.extend(validate(metadata, text))
    payload = {
        "status": "OK" if not errors else "ERROR",
        "run": str(path),
        "metadata": metadata,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        print(f"OK: {path}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
