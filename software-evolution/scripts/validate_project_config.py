#!/usr/bin/env python3
"""Validate the restricted YAML project control-plane configuration.

The parser intentionally supports mappings and scalar values only, avoiding a runtime
PyYAML dependency and rejecting ambiguous YAML features.
"""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re
import sys
from typing import Any


KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
INT_RE = re.compile(r"^-?[0-9]+$")

BUDGET_SCHEMA = {
    "max_scope_items": ("int", 1),
    "max_findings": ("int", 1),
    "max_repair_batches": ("int", 0),
    "max_files_changed": ("int", 0),
    "reserve_verification_minutes": ("int", 0),
}
SCHEMA: dict[str, Any] = {
    "version": ("version", None),
    "memory_dir": ("relative_path", None),
    "autonomy": {
        "max_risk": ("risk", None),
        "allow_product_writes": ("bool", None),
    },
    "autopilot": {
        "max_cycles": ("int", 1),
        "max_consecutive_failed_batches": ("int", 1),
        "checkpoint_every_batch": ("required_true", None),
    },
    "budget": BUDGET_SCHEMA,
    "deep_budget": BUDGET_SCHEMA,
    "overnight_budget": {
        "max_runtime_minutes": ("int", 1),
        "max_cycles": ("int", 1),
        "max_scope_items": ("int", 1),
        "max_findings": ("int", 1),
        "max_repair_batches": ("int", 0),
        "max_files_changed": ("int", 0),
        "max_consecutive_failed_batches": ("int", 1),
        "reserve_verification_minutes": ("int", 0),
    },
    "readonly": {"allow_record_persistence": ("bool", None)},
    "release": {
        "require_required_checks": ("bool", None),
        "require_rollback_plan": ("bool", None),
        "require_mixed_version_check": ("bool", None),
    },
    "observe": {
        "production_read_only": ("readonly_true", None),
        "default_window_minutes": ("int", 1),
    },
    "specialist_routing": {
        "security": ("routing", None),
        "supply_chain": ("routing", None),
        "data": ("routing", None),
        "performance_cost": ("routing", None),
        "ux": ("routing", None),
        "database": ("routing", None),
        "ci_cd": ("routing", None),
    },
    "fitness": {"enforce_registered_checks": ("bool", None)},
}


class ConfigError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate .software-evolution.yml")
    parser.add_argument("--config", default=".software-evolution.yml")
    parser.add_argument("--json", action="store_true", help="Emit a JSON result.")
    return parser.parse_args()


def strip_inline_comment(value: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote == '"':
            escaped = True
            continue
        if char in ("'", '"'):
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
            continue
        if char == "#" and quote is None and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    if quote is not None:
        raise ConfigError("unterminated quoted scalar")
    return value.rstrip()


def parse_scalar(raw: str, line_number: int) -> Any:
    if raw == "true":
        return True
    if raw == "false":
        return False
    if raw in {"True", "False", "TRUE", "FALSE", "yes", "no", "on", "off"}:
        raise ConfigError(
            f"line {line_number}: booleans must use lowercase true or false"
        )
    if INT_RE.fullmatch(raw):
        return int(raw)
    if raw.startswith(("[", "{", "&", "*", "!", "|", ">")):
        raise ConfigError(
            f"line {line_number}: lists, objects, anchors, tags, and block scalars are unsupported"
        )
    if raw[:1] in {"'", '"'}:
        try:
            value = ast.literal_eval(raw)
        except (SyntaxError, ValueError) as exc:
            raise ConfigError(f"line {line_number}: invalid quoted scalar") from exc
        if not isinstance(value, str):
            raise ConfigError(f"line {line_number}: quoted scalar must be a string")
        return value
    if not raw:
        raise ConfigError(f"line {line_number}: empty scalar")
    return raw


def parse_restricted_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any], str]] = [(-2, root, "")]

    for line_number, original in enumerate(text.splitlines(), 1):
        if "\t" in original:
            raise ConfigError(f"line {line_number}: tabs are not allowed")
        if not original.strip() or original.lstrip().startswith("#"):
            continue
        indent = len(original) - len(original.lstrip(" "))
        if indent % 2:
            raise ConfigError(f"line {line_number}: indentation must use two-space steps")
        content = strip_inline_comment(original[indent:])
        if not content:
            continue
        if ":" not in content:
            raise ConfigError(f"line {line_number}: expected key: value")
        key, raw_value = content.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not KEY_RE.fullmatch(key):
            raise ConfigError(f"line {line_number}: invalid key {key!r}")
        compact_key = key.lower().replace("_", "").replace("-", "")
        if any(
            marker in compact_key
            for marker in ("password", "passwd", "token", "secret", "credential", "privatekey")
        ):
            raise ConfigError(f"line {line_number}: sensitive key is forbidden: {key}")

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack or indent != stack[-1][0] + 2:
            raise ConfigError(f"line {line_number}: invalid indentation level")
        parent = stack[-1][1]
        path = f"{stack[-1][2]}.{key}" if stack[-1][2] else key
        if key in parent:
            raise ConfigError(f"line {line_number}: duplicate key {path}")

        if raw_value == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child, path))
        else:
            parent[key] = parse_scalar(raw_value, line_number)

    return root


def validate_value(path: str, value: Any, rule: tuple[str, Any], errors: list[str]) -> None:
    kind, constraint = rule
    if kind == "version":
        if type(value) is not int or value != 1:
            errors.append(f"{path} must be integer 1")
    elif kind == "string":
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path} must be a non-empty string")
    elif kind == "relative_path":
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path} must be a non-empty project-relative path")
        else:
            candidate = value.strip()
            windows_absolute = bool(re.match(r"^[A-Za-z]:[\\/]", candidate)) or candidate.startswith("\\")
            parts = candidate.replace("\\", "/").split("/")
            if (
                Path(candidate).is_absolute()
                or windows_absolute
                or candidate.startswith("~")
                or "\\" in candidate
                or candidate in {".", ".."}
                or ".." in parts
            ):
                errors.append(f"{path} must stay inside the project and use a portable relative path")
    elif kind == "bool":
        if type(value) is not bool:
            errors.append(f"{path} must be true or false")
    elif kind == "readonly_true":
        if value is not True:
            errors.append(f"{path} must be true; project config cannot authorize production writes")
    elif kind == "required_true":
        if value is not True:
            errors.append(f"{path} must be true; unattended runs require per-batch checkpoints")
    elif kind == "int":
        if type(value) is not int or value < constraint:
            errors.append(f"{path} must be an integer >= {constraint}")
    elif kind == "risk":
        if value not in {"R0", "R1", "R2", "R3", "R4"}:
            errors.append(f"{path} must be one of R0, R1, R2, R3, R4")
    elif kind == "routing":
        if value not in {"auto", "required", "off"}:
            errors.append(f"{path} must be auto, required, or off")


def validate_mapping(
    data: dict[str, Any], schema: dict[str, Any], prefix: str, errors: list[str]
) -> None:
    for key in data:
        path = f"{prefix}.{key}" if prefix else key
        if key not in schema:
            errors.append(f"unknown key: {path}")
            continue
        expected = schema[key]
        value = data[key]
        if isinstance(expected, dict):
            if not isinstance(value, dict):
                errors.append(f"{path} must be a mapping")
            else:
                validate_mapping(value, expected, path, errors)
        else:
            if isinstance(value, dict):
                errors.append(f"{path} must be a scalar")
            else:
                validate_value(path, value, expected, errors)


def validate_config(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validate_mapping(data, SCHEMA, "", errors)
    if "version" not in data:
        errors.append("missing required key: version")
    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.config).expanduser()
    if not path.is_file():
        message = f"config file not found: {path}"
        if args.json:
            print(json.dumps({"status": "ERROR", "errors": [message]}))
        else:
            print(f"ERROR: {message}", file=sys.stderr)
        return 2

    try:
        data = parse_restricted_yaml(path.read_text(encoding="utf-8"))
        errors = validate_config(data)
    except (OSError, UnicodeError, ConfigError) as exc:
        errors = [str(exc)]

    if errors:
        if args.json:
            print(json.dumps({"status": "INVALID", "errors": errors}, indent=2))
        else:
            for error in errors:
                print(f"ERROR: {error}")
            print(f"INVALID: {len(errors)} error(s)")
        return 1

    if args.json:
        print(json.dumps({"status": "OK", "config": data}, indent=2))
    else:
        print(f"OK: valid software-evolution config: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
