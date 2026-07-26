#!/usr/bin/env python3
"""Install the repository's software-evolution Skill for the current user."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys


SKILL_NAME = "software-evolution"


def default_target() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills" / SKILL_NAME

    home = Path.home()
    codex_skills = home / ".codex" / "skills"
    agents_skills = home / ".agents" / "skills"

    if codex_skills.exists():
        return codex_skills / SKILL_NAME
    if agents_skills.exists():
        return agents_skills / SKILL_NAME
    return codex_skills / SKILL_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install AI Software Evolution Agent as a user-level Codex Skill."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=None,
        help="Exact destination directory. Defaults to the detected user Skill location.",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy the Skill instead of creating a symbolic link.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the action without modifying the filesystem.",
    )
    return parser.parse_args()


def same_symlink(target: Path, source: Path) -> bool:
    if not target.is_symlink():
        return False
    try:
        return target.resolve(strict=True) == source.resolve(strict=True)
    except FileNotFoundError:
        return False


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    source = (repo_root / SKILL_NAME).resolve()
    target = (args.target.expanduser() if args.target else default_target()).absolute()
    mode = "copy" if args.copy else "symlink"

    if not (source / "SKILL.md").is_file():
        print(f"ERROR: Skill source is invalid: {source}", file=sys.stderr)
        return 2

    if target.exists() or target.is_symlink():
        if same_symlink(target, source) and not args.copy:
            print(f"OK: already installed: {target} -> {source}")
            return 0
        print(
            f"ERROR: target already exists and was not changed: {target}\n"
            "Choose another --target or remove/relocate the existing installation yourself.",
            file=sys.stderr,
        )
        return 3

    print(f"SOURCE: {source}")
    print(f"TARGET: {target}")
    print(f"MODE: {mode}")
    if args.dry_run:
        print("DRY-RUN: no files changed")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    if args.copy:
        shutil.copytree(source, target)
    else:
        target.symlink_to(source, target_is_directory=True)

    if not (target / "SKILL.md").is_file():
        print(f"ERROR: installation verification failed: {target}", file=sys.stderr)
        return 4

    if args.copy:
        print(f"INSTALLED: {target}")
    else:
        print(f"INSTALLED: {target} -> {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
