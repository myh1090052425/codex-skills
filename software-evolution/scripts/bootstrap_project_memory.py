#!/usr/bin/env python3
"""Create missing software-evolution memory files in a target project.

The script is deliberately non-destructive: existing files are never overwritten.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import sys


TEMPLATES = {
    "architecture-memory.template.md": "architecture-memory.md",
    "capability-map.template.md": "capability-map.md",
    "technical-debt.template.md": "technical-debt.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create missing AI software-evolution project memory files."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/software-evolution",
        help="Directory relative to --root, or an absolute path.",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Date inserted into templates (YYYY-MM-DD by default).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without creating files.",
    )
    return parser.parse_args()


def resolve_output_dir(root: Path, output_arg: str) -> Path:
    output = Path(output_arg).expanduser()
    return output.resolve() if output.is_absolute() else (root / output).resolve()


def render(template: str, *, project_name: str, root: Path, date: str) -> str:
    return (
        template.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{REPOSITORY_PATH}}", str(root))
        .replace("{{DATE}}", date)
    )


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"ERROR: project root is not a directory: {root}", file=sys.stderr)
        return 2

    skill_root = Path(__file__).resolve().parent.parent
    template_dir = skill_root / "memory"
    output_dir = resolve_output_dir(root, args.output_dir)
    project_name = root.name or "project"

    missing_templates = [name for name in TEMPLATES if not (template_dir / name).is_file()]
    if missing_templates:
        print(
            "ERROR: missing skill templates: " + ", ".join(missing_templates),
            file=sys.stderr,
        )
        return 3

    actions: list[tuple[str, Path]] = []
    for template_name, output_name in TEMPLATES.items():
        destination = output_dir / output_name
        actions.append(("skip" if destination.exists() else "create", destination))

    if args.dry_run:
        for action, destination in actions:
            print(f"{action.upper()}: {destination}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    created = 0
    skipped = 0

    for template_name, output_name in TEMPLATES.items():
        destination = output_dir / output_name
        if destination.exists():
            print(f"SKIP: {destination} already exists")
            skipped += 1
            continue

        source = (template_dir / template_name).read_text(encoding="utf-8")
        content = render(source, project_name=project_name, root=root, date=args.date)

        # Exclusive creation prevents a concurrent agent from being overwritten.
        try:
            fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            print(f"SKIP: {destination} was created concurrently")
            skipped += 1
            continue

        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        print(f"CREATE: {destination}")
        created += 1

    print(f"SUMMARY: created={created} skipped={skipped} directory={output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
