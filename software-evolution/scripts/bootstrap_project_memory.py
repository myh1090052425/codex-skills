#!/usr/bin/env python3
"""Create the non-destructive software-evolution control plane in a project."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys


MEMORY_TEMPLATES = {
    "architecture-memory.template.md": "architecture-memory.md",
    "capability-map.template.md": "capability-map.md",
    "technical-debt.template.md": "technical-debt.md",
    "health-baseline.template.json": "health-baseline.json",
}
CONFIG_TEMPLATE = "software-evolution.config.template.yml"
CONTROL_DIRS = (
    "decisions",
    "batches",
    "runs",
    "reports/audit",
    "reports/verification",
    "reports/release",
    "reports/observation",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create missing AI software-evolution project control-plane files."
    )
    parser.add_argument("--root", default=".", help="Project root; defaults to cwd.")
    parser.add_argument(
        "--output-dir",
        default="docs/software-evolution",
        help="Memory directory relative to --root, or an explicit absolute path.",
    )
    parser.add_argument(
        "--config-path",
        default=".software-evolution.yml",
        help="Config path relative to --root, or an explicit absolute path.",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Date inserted into templates (YYYY-MM-DD by default).",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show actions without creating anything."
    )
    return parser.parse_args()


def resolve_path(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"relative control-plane path escapes project root: {value}") from exc
    return resolved


def render(
    template: str, *, project_name: str, repository_reference: str, date: str, json_safe: bool = False
) -> str:
    if json_safe:
        return (
            template.replace('"{{PROJECT_NAME}}"', json.dumps(project_name, ensure_ascii=False))
            .replace('"{{REPOSITORY_REFERENCE}}"', json.dumps(repository_reference, ensure_ascii=False))
            .replace('"{{DATE}}"', json.dumps(date, ensure_ascii=False))
        )
    return (
        template.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{REPOSITORY_REFERENCE}}", repository_reference)
        .replace("{{DATE}}", date)
    )


def exclusive_write(destination: Path, content: str) -> bool:
    """Write once. Return False when another process/file already won."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(content)
    return True


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: project root is not a directory: {root}", file=sys.stderr)
        return 2

    skill_root = Path(__file__).resolve().parent.parent
    template_dir = skill_root / "memory"
    required_templates = set(MEMORY_TEMPLATES) | {CONFIG_TEMPLATE}
    missing = sorted(name for name in required_templates if not (template_dir / name).is_file())
    if missing:
        print("ERROR: missing skill templates: " + ", ".join(missing), file=sys.stderr)
        return 3

    try:
        output_dir = resolve_path(root, args.output_dir)
        config_path = resolve_path(root, args.config_path)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    project_name = root.name or "project"

    file_specs: list[tuple[Path, Path]] = [
        (template_dir / CONFIG_TEMPLATE, config_path),
        *[
            (template_dir / template_name, output_dir / output_name)
            for template_name, output_name in MEMORY_TEMPLATES.items()
        ],
    ]
    directory_specs = [output_dir / relative for relative in CONTROL_DIRS]

    for directory in [output_dir, *directory_specs]:
        if directory.exists() and not directory.is_dir():
            print(f"ERROR: control-plane directory path is a file: {directory}", file=sys.stderr)
            return 4
    for _, destination in file_specs:
        if destination.exists() and not destination.is_file():
            print(f"ERROR: control-plane file path is not a file: {destination}", file=sys.stderr)
            return 4

    if args.dry_run:
        for directory in directory_specs:
            print(f"{'EXISTS_DIR' if directory.is_dir() else 'CREATE_DIR'}: {directory}")
        for _, destination in file_specs:
            print(f"{'SKIP' if destination.exists() else 'CREATE'}: {destination}")
        return 0

    created_dirs = 0
    existing_dirs = 0
    output_dir.mkdir(parents=True, exist_ok=True)
    for directory in directory_specs:
        if directory.is_dir():
            print(f"EXISTS_DIR: {directory}")
            existing_dirs += 1
        else:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"CREATE_DIR: {directory}")
            created_dirs += 1

    created_files = 0
    skipped_files = 0
    for source, destination in file_specs:
        if destination.exists():
            print(f"SKIP: {destination} already exists")
            skipped_files += 1
            continue
        content = render(
            source.read_text(encoding="utf-8"),
            project_name=project_name,
            repository_reference=project_name,
            date=args.date,
            json_safe=source.suffix == ".json",
        )
        if exclusive_write(destination, content):
            print(f"CREATE: {destination}")
            created_files += 1
        else:
            print(f"SKIP: {destination} was created concurrently")
            skipped_files += 1

    print(
        "SUMMARY: "
        f"created_files={created_files} skipped_files={skipped_files} "
        f"created_dirs={created_dirs} existing_dirs={existing_dirs} "
        f"memory_dir={output_dir} config={config_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
