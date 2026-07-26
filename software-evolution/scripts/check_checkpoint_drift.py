#!/usr/bin/env python3
"""Create Git checkpoint metadata or classify drift from a batch checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any


CHECKPOINT_RE = re.compile(
    r"<!--\s*software-evolution-checkpoint\s*(\{.*?\})\s*-->", re.DOTALL
)
BATCH_ID_RE = re.compile(r"^BATCH-[A-Za-z0-9._-]+$")
VALID_MODES = {"init", "audit", "govern", "repair", "verify", "deep", "release-check", "observe", "resume"}
VALID_CLASSES = {
    "NO_DRIFT",
    "SAFE_DRIFT",
    "MATERIAL_DRIFT",
    "CONFLICTING_DRIFT",
    "UNKNOWN",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check software-evolution batch drift.")
    parser.add_argument("--root", default=".", help="Git repository root.")
    parser.add_argument("--checkpoint", help="Batch Markdown file to compare.")
    parser.add_argument("--snapshot", action="store_true", help="Print current metadata JSON.")
    parser.add_argument("--batch-id", default="BATCH-TBD")
    parser.add_argument("--mode", default="repair")
    parser.add_argument("--scope-path", action="append", default=[])
    parser.add_argument("--json", action="store_true", help="Emit classification as JSON.")
    return parser.parse_args()


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def ensure_repo(root: Path) -> None:
    result = run_git(root, "rev-parse", "--is-inside-work-tree", check=False)
    if result.returncode != 0 or result.stdout.strip() != b"true":
        raise ValueError(f"not a Git work tree: {root}")


def current_branch(root: Path) -> str:
    result = run_git(root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    return result.stdout.decode("utf-8", "replace").strip() if result.returncode == 0 else "DETACHED"


def current_head(root: Path) -> str:
    return run_git(root, "rev-parse", "HEAD").stdout.decode().strip()


def status_raw(root: Path) -> bytes:
    return run_git(
        root, "status", "--porcelain=v1", "-z", "--untracked-files=all"
    ).stdout


def parse_status(raw: bytes) -> list[dict[str, str]]:
    parts = raw.split(b"\0")
    entries: list[dict[str, str]] = []
    index = 0
    while index < len(parts):
        item = parts[index]
        index += 1
        if not item:
            continue
        text = item.decode("utf-8", "surrogateescape")
        if len(text) < 4:
            continue
        status = text[:2]
        path = text[3:]
        entries.append({"status": status, "path": path})
        if "R" in status or "C" in status:
            if index < len(parts) and parts[index]:
                old_path = parts[index].decode("utf-8", "surrogateescape")
                entries.append({"status": status, "path": old_path})
                index += 1
    return sorted(entries, key=lambda item: (item["path"], item["status"]))


def normalize_path(path: str) -> str:
    value = path.strip().replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value.rstrip("/") or "."


def normalize_scope_path(path: str) -> str:
    value = normalize_path(path)
    windows_absolute = bool(re.match(r"^[A-Za-z]:/", value)) or value.startswith("//")
    if value == ".":
        return value
    parts = value.split("/")
    if (
        Path(value).is_absolute()
        or windows_absolute
        or value.startswith("~")
        or value == ".."
        or ".." in parts
    ):
        raise ValueError(f"scope path must be a portable project-relative path: {path}")
    return value


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return "file:" + digest.hexdigest()


def fingerprint_path(root: Path, relative: str) -> str:
    path = root / relative
    if path.is_symlink():
        target = os.readlink(path).encode("utf-8", "surrogateescape")
        return "symlink:" + hashlib.sha256(target).hexdigest()
    if path.is_file():
        return hash_file(path)
    if path.is_dir():
        diff = run_git(root, "diff", "--submodule=short", "--", relative, check=False)
        return "directory:" + hashlib.sha256(diff.stdout).hexdigest()
    return "missing"


def path_fingerprints(root: Path, entries: list[dict[str, str]]) -> dict[str, str]:
    paths = sorted({normalize_path(entry["path"]) for entry in entries})
    return {path: fingerprint_path(root, path) for path in paths}


def worktree_fingerprint(
    root: Path, raw_status: bytes, fingerprints: dict[str, str]
) -> str:
    digest = hashlib.sha256()
    digest.update(b"status\0")
    digest.update(raw_status)
    digest.update(b"\0unstaged\0")
    digest.update(run_git(root, "diff", "--binary", "--no-ext-diff").stdout)
    digest.update(b"\0staged\0")
    digest.update(run_git(root, "diff", "--cached", "--binary", "--no-ext-diff").stdout)
    digest.update(b"\0paths\0")
    digest.update(json.dumps(fingerprints, sort_keys=True).encode("utf-8"))
    return digest.hexdigest()


def snapshot(root: Path, *, batch_id: str, mode: str, scope_paths: list[str]) -> dict[str, Any]:
    ensure_repo(root)
    if not BATCH_ID_RE.fullmatch(batch_id):
        raise ValueError(f"invalid batch ID: {batch_id}")
    if mode not in VALID_MODES:
        raise ValueError(f"invalid originating mode: {mode}")
    normalized_scopes = sorted({normalize_scope_path(path) for path in scope_paths if path.strip()})
    raw = status_raw(root)
    entries = parse_status(raw)
    fingerprints = path_fingerprints(root, entries)
    return {
        "schema_version": 1,
        "batch_id": batch_id,
        "mode": mode,
        "branch": current_branch(root),
        "head": current_head(root),
        "worktree_fingerprint": worktree_fingerprint(root, raw, fingerprints),
        "worktree_entries": entries,
        "worktree_path_fingerprints": fingerprints,
        "scope_paths": normalized_scopes,
    }


def overlaps_scope(path: str, scope_paths: list[str]) -> bool:
    candidate = normalize_path(path)
    for scope in scope_paths:
        normalized = normalize_path(scope)
        if normalized == ".":
            return True
        if candidate == normalized or candidate.startswith(normalized + "/"):
            return True
        if normalized.startswith(candidate + "/"):
            return True
    return False


def parse_checkpoint(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = CHECKPOINT_RE.search(text)
    if not match:
        raise ValueError("checkpoint metadata comment not found")
    try:
        metadata = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid checkpoint JSON: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("checkpoint metadata must be a JSON object")
    if metadata.get("schema_version", 1) != 1:
        raise ValueError("unsupported checkpoint schema_version")
    for key in ("branch", "head", "worktree_fingerprint"):
        if not isinstance(metadata.get(key), str) or not metadata[key]:
            raise ValueError(f"checkpoint metadata missing string field: {key}")
    if "worktree_entries" in metadata and not isinstance(metadata["worktree_entries"], list):
        raise ValueError("checkpoint worktree_entries must be a list")
    if "worktree_path_fingerprints" in metadata and not isinstance(
        metadata["worktree_path_fingerprints"], dict
    ):
        raise ValueError("checkpoint worktree_path_fingerprints must be an object")
    if "scope_paths" in metadata:
        if not isinstance(metadata["scope_paths"], list) or not all(
            isinstance(item, str) for item in metadata["scope_paths"]
        ):
            raise ValueError("checkpoint scope_paths must be a list of strings")
        metadata["scope_paths"] = [normalize_scope_path(item) for item in metadata["scope_paths"]]
    if "batch_id" in metadata and (
        not isinstance(metadata["batch_id"], str)
        or not BATCH_ID_RE.fullmatch(metadata["batch_id"])
    ):
        raise ValueError("checkpoint batch_id is invalid")
    if "mode" in metadata and metadata["mode"] not in VALID_MODES:
        raise ValueError("checkpoint mode is invalid")
    return metadata


def entry_pairs(entries: list[Any]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        status = entry.get("status")
        path = entry.get("path")
        if isinstance(status, str) and isinstance(path, str):
            pairs.add((status, normalize_path(path)))
    return pairs


def normalized_fingerprints(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {
        normalize_path(str(path)): fingerprint
        for path, fingerprint in value.items()
        if isinstance(fingerprint, str)
    }


def is_ancestor(root: Path, expected_head: str, current: str) -> bool | None:
    result = run_git(root, "merge-base", "--is-ancestor", expected_head, current, check=False)
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def classify(root: Path, expected: dict[str, Any]) -> tuple[str, list[str], dict[str, Any]]:
    current = snapshot(
        root,
        batch_id=str(expected.get("batch_id", "BATCH-TBD")),
        mode=str(expected.get("mode", "unknown")),
        scope_paths=[str(item) for item in expected.get("scope_paths", [])],
    )
    reasons: list[str] = []

    if current["branch"] != expected["branch"]:
        reasons.append(f"branch changed: {expected['branch']} -> {current['branch']}")
        return "CONFLICTING_DRIFT", reasons, current

    head_changed = current["head"] != expected["head"]
    if head_changed:
        relation = is_ancestor(root, expected["head"], current["head"])
        if relation is False:
            reasons.append("current HEAD does not descend from checkpoint HEAD")
            return "CONFLICTING_DRIFT", reasons, current
        if relation is None:
            reasons.append("unable to establish checkpoint/current HEAD ancestry")
            return "UNKNOWN", reasons, current
        reasons.append("HEAD advanced since checkpoint")

    if current["worktree_fingerprint"] == expected["worktree_fingerprint"] and not head_changed:
        return "NO_DRIFT", ["branch, HEAD, and worktree fingerprint match"], current

    expected_pairs = entry_pairs(expected.get("worktree_entries", []))
    current_pairs = entry_pairs(current["worktree_entries"])
    delta_pairs = expected_pairs.symmetric_difference(current_pairs)

    expected_fingerprints = normalized_fingerprints(
        expected.get("worktree_path_fingerprints", {})
    )
    current_fingerprints = normalized_fingerprints(
        current.get("worktree_path_fingerprints", {})
    )
    content_delta_paths = {
        path
        for path in set(expected_fingerprints) | set(current_fingerprints)
        if expected_fingerprints.get(path) != current_fingerprints.get(path)
    }
    delta_paths = {path for _, path in delta_pairs} | content_delta_paths
    scope_paths = [str(item) for item in expected.get("scope_paths", [])]

    if scope_paths and any(overlaps_scope(path, scope_paths) for path in delta_paths):
        reasons.append("worktree drift overlaps checkpoint scope")
        return "CONFLICTING_DRIFT", reasons, current

    if head_changed:
        return "MATERIAL_DRIFT", reasons, current

    statuses_by_path: dict[str, set[str]] = {}
    for status, path in expected_pairs | current_pairs:
        statuses_by_path.setdefault(path, set()).add(status)
    if delta_paths and all(statuses_by_path.get(path) == {"??"} for path in delta_paths):
        reasons.append("only untracked out-of-scope paths or their contents changed")
        return "SAFE_DRIFT", reasons, current

    if not expected_pairs and not expected_fingerprints:
        reasons.append("worktree fingerprint changed and checkpoint lacks comparable path metadata")
    else:
        reasons.append("tracked or status-significant out-of-scope worktree changes detected")
    return "MATERIAL_DRIFT", reasons, current


def emit(classification: str, reasons: list[str], current: dict[str, Any], as_json: bool) -> None:
    if classification not in VALID_CLASSES:
        classification = "UNKNOWN"
    if as_json:
        print(
            json.dumps(
                {"classification": classification, "reasons": reasons, "current": current},
                indent=2,
            )
        )
    else:
        print(classification)
        for reason in reasons:
            print(f"- {reason}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        if args.snapshot:
            current = snapshot(
                root,
                batch_id=args.batch_id,
                mode=args.mode,
                scope_paths=args.scope_path,
            )
            print(json.dumps(current, indent=2))
            return 0
        if not args.checkpoint:
            raise ValueError("--checkpoint is required unless --snapshot is used")
        expected = parse_checkpoint(Path(args.checkpoint).expanduser())
        classification, reasons, current = classify(root, expected)
        emit(classification, reasons, current, args.json)
        return 0
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as exc:
        emit("UNKNOWN", [str(exc)], {}, args.json)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
