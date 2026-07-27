from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "software-evolution"
TEMPLATE = SKILL / "templates" / "autopilot-run.md"
VALIDATOR = SKILL / "scripts" / "validate_run_completion.py"
RUN_RE = re.compile(
    r"<!--\s*software-evolution-run\s*(\{.*?\})\s*-->", re.DOTALL
)


class RunCompletionTests(unittest.TestCase):
    def completion_evidence(self, text: str) -> str:
        coverage = """## Governance coverage matrix

| Lane | Declared surface / critical outcome | Fresh evidence since last material repair | Status | Next uncovered/counterexample target |
|---|---|---|---|---|
| User and business outcomes | Checkout and account recovery | Browser journeys, API outcomes, and business-state checks | `covered` | None found |
| Engineering and reliability | Changed services and failure paths | Unit, integration, type, build, and error-path checks | `covered` | None found |
| Architecture and evolution | Capability ownership and dependency boundaries | Capability/rule duplicate scan and fitness checks | `covered` | None found |
| Runtime UX/browser | Navigation, checkout, and recovery | Browser success plus failure/recovery evidence | `covered` | None found |

- Current defect family and strongest candidates from the other lanes: `all reconciled`
- Reason the selected batch outranks cross-lane alternatives: `final challenge found no repair-ready candidate`
"""
        aggregate = """## Aggregate verification

- Commands/flows and results: `unit, integration, build, typecheck, and browser journeys passed`
- Reused evidence and unchanged-input fingerprints: `none`
- Final diff and unrelated-change review: `reviewed; no unrelated changes absorbed`
- Capability/business-rule/fitness re-scan: `passed with no repair-ready issue`
- Remaining proof gaps: `none`
"""
        stop = """## Stop and continuation

- Real terminal stop reason: `safe_work_exhausted`
- Legacy quota caused this stop: `must be no`
- Latest valid checkpoint: `RUN-TEST final verification`
- Auto-adoptable by next plain invocation: `no; completed`
- Explicit Resume required: `no`
- Next safe action: `none`
"""
        challenge = """## Completion challenge

- Fresh cross-lane counterexample search outside the current module/taxonomy/test pattern: `no repair-ready counterexample found`
- Open Ready/In-progress debt and finding reconciliation: `all closed, blocked with evidence, or not repair-ready`
- Recent/unclassified change review: `reviewed with no uncovered repair-ready work`
- Capability duplicate and business-rule split challenge: `no actionable split found`
- Critical journey and runtime UX evidence/blocker: `browser success and failure/recovery journeys passed`
- Repair-ready work remaining: `no`
- `validate_run_completion.py` command/result: `OK`
- Host durable goal completion allowed: `yes after validator OK`
"""
        text = re.sub(
            r"## Governance coverage matrix.*?(?=^## Execution metrics)",
            coverage + "\n",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )
        text = re.sub(
            r"## Aggregate verification.*?(?=^## Completion challenge)",
            aggregate + "\n",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )
        text = re.sub(
            r"## Completion challenge.*?(?=^## Stop and continuation)",
            challenge + "\n",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )
        return re.sub(
            r"## Stop and continuation.*?\Z",
            stop + "\n",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )

    def render(self, mutate, *, fill_completion_evidence: bool = True) -> str:
        text = TEMPLATE.read_text(encoding="utf-8")
        match = RUN_RE.search(text)
        self.assertIsNotNone(match)
        metadata = json.loads(match.group(1))
        mutate(metadata)
        if metadata.get("status") == "completed":
            metadata.update(
                {
                    "run_id": "RUN-TEST",
                    "branch": "main",
                    "head": "0123456789abcdef0123456789abcdef01234567",
                    "invocation_id": "INV-TEST",
                    "last_heartbeat_at": "2026-07-27T12:00:00+08:00",
                }
            )
        text = text[: match.start(1)] + json.dumps(metadata, indent=2) + text[match.end(1) :]
        if metadata.get("status") == "completed" and fill_completion_evidence:
            text = self.completion_evidence(text)
        return text

    def validate(self, text: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="software-evolution-run-") as tmp:
            path = Path(tmp) / "RUN-TEST.md"
            path.write_text(text, encoding="utf-8")
            return subprocess.run(
                ["python3", str(VALIDATOR), "--run", str(path), "--json"],
                text=True,
                capture_output=True,
            )

    def test_running_template_is_valid_with_pending_coverage(self) -> None:
        result = self.validate(TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual("OK", payload["status"])
        self.assertEqual("pending", payload["metadata"]["coverage"]["user_business"])

    def test_completed_run_rejects_single_cluster_exhaustion(self) -> None:
        def mutate(metadata: dict) -> None:
            metadata["status"] = "completed"
            metadata["terminal_reason"] = "safe_work_exhausted"
            metadata["coverage"]["engineering_reliability"] = "covered"
            metadata["coverage"]["open_repair_ready_work"] = False

        result = self.validate(self.render(mutate))
        self.assertEqual(2, result.returncode)
        payload = json.loads(result.stdout)
        joined = "\n".join(payload["errors"])
        self.assertIn("coverage.user_business", joined)
        self.assertIn("coverage.architecture_evolution", joined)
        self.assertIn("cross-lane", joined)
        self.assertIn("runtime UX", joined)

    def test_completed_run_requires_no_open_repair_ready_work(self) -> None:
        def mutate(metadata: dict) -> None:
            metadata["status"] = "completed"
            metadata["terminal_reason"] = "safe_work_exhausted"
            for lane in (
                "user_business",
                "engineering_reliability",
                "architecture_evolution",
            ):
                metadata["coverage"][lane] = "covered"
            metadata["coverage"]["runtime_ux"] = "covered"
            metadata["coverage"]["cross_lane_challenge"] = "passed"

        result = self.validate(self.render(mutate))
        self.assertEqual(2, result.returncode)
        self.assertIn("open repair-ready work", result.stdout)

    def test_balanced_completed_run_passes(self) -> None:
        def mutate(metadata: dict) -> None:
            metadata["status"] = "completed"
            metadata["terminal_reason"] = "safe_work_exhausted"
            for lane in (
                "user_business",
                "engineering_reliability",
                "architecture_evolution",
            ):
                metadata["coverage"][lane] = "covered"
            metadata["coverage"]["runtime_ux"] = "covered"
            metadata["coverage"]["cross_lane_challenge"] = "passed"
            metadata["coverage"]["open_repair_ready_work"] = False

        result = self.validate(self.render(mutate))
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_completed_run_rejects_placeholder_completion_evidence(self) -> None:
        def mutate(metadata: dict) -> None:
            metadata["status"] = "completed"
            metadata["terminal_reason"] = "safe_work_exhausted"
            for lane in (
                "user_business",
                "engineering_reliability",
                "architecture_evolution",
            ):
                metadata["coverage"][lane] = "covered"
            metadata["coverage"]["runtime_ux"] = "covered"
            metadata["coverage"]["cross_lane_challenge"] = "passed"
            metadata["coverage"]["open_repair_ready_work"] = False

        result = self.validate(
            self.render(mutate, fill_completion_evidence=False)
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("still contains TBD evidence", result.stdout)
        self.assertIn("must explicitly record no repair-ready work", result.stdout)
        self.assertIn("result OK", result.stdout)

    def test_interrupted_run_may_preserve_pending_coverage(self) -> None:
        def mutate(metadata: dict) -> None:
            metadata["status"] = "interrupted"
            metadata["terminal_reason"] = "host_interruption"

        result = self.validate(self.render(mutate))
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_scope_paths_must_be_repository_relative(self) -> None:
        for scope in ("../outside", "/tmp/outside", "C:\\outside"):
            with self.subTest(scope=scope):
                def mutate(metadata: dict) -> None:
                    metadata["scope_kind"] = "scoped"
                    metadata["scope_paths"] = [scope]

                result = self.validate(self.render(mutate))
                self.assertEqual(2, result.returncode)
                self.assertIn("repository-relative and non-escaping", result.stdout)

    def test_terminal_reason_must_match_terminal_status(self) -> None:
        def mutate(metadata: dict) -> None:
            metadata["status"] = "interrupted"
            metadata["terminal_reason"] = "failure_exhaustion"

        result = self.validate(self.render(mutate))
        self.assertEqual(2, result.returncode)
        self.assertIn("inconsistent with status interrupted", result.stdout)

    def test_repository_scope_cannot_collapse_to_current_batch_path(self) -> None:
        def mutate(metadata: dict) -> None:
            metadata["scope_kind"] = "repository"
            metadata["scope_paths"] = ["apps/web/src/lib"]

        result = self.validate(self.render(mutate))
        self.assertEqual(2, result.returncode)
        self.assertIn("retain '.'", result.stdout)


if __name__ == "__main__":
    unittest.main()
