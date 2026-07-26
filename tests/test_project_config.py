from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "software-evolution" / "scripts" / "validate_project_config.py"
TEMPLATE = ROOT / "software-evolution" / "memory" / "software-evolution.config.template.yml"


class ProjectConfigTests(unittest.TestCase):
    def run_config(
        self, content: str, *, json_output: bool = False
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="software-evolution-config-") as tmp:
            path = Path(tmp) / ".software-evolution.yml"
            path.write_text(content, encoding="utf-8")
            command = ["python3", str(VALIDATOR), "--config", str(path)]
            if json_output:
                command.append("--json")
            return subprocess.run(command, text=True, capture_output=True)

    def test_template_is_valid_and_contains_no_artificial_quotas(self) -> None:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "--config", str(TEMPLATE), "--json"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("OK", payload["status"])
        self.assertEqual([], payload["defaulted_paths"])
        self.assertEqual([], payload["deprecated_paths"])

        effective = payload["effective_config"]
        self.assertEqual(
            {
                "continue_until_no_safe_work": True,
                "checkpoint_every_batch": True,
            },
            effective["autopilot"],
        )
        for legacy_section in ("budget", "deep_budget", "overnight_budget"):
            self.assertNotIn(legacy_section, effective)
        for legacy_key in (
            "max_runtime_minutes",
            "max_cycles",
            "max_budget_windows",
            "max_total_files_changed",
            "max_consecutive_failed_batches",
            "continue_after_budget_checkpoint",
        ):
            self.assertNotIn(legacy_key, effective["autopilot"])

    def test_legacy_quota_controls_are_accepted_but_removed_from_effective_config(self) -> None:
        result = self.run_config(
            """version: 1
memory_dir: docs/software-evolution

autonomy:
  max_risk: R2
  allow_product_writes: true

autopilot:
  max_runtime_minutes: 300
  max_cycles: 9
  max_budget_windows: 5
  max_total_files_changed: 99
  max_consecutive_failed_batches: 3
  continue_after_budget_checkpoint: false

budget:
  max_scope_items: 60
  max_findings: 12
  max_repair_batches: 2
  max_files_changed: 12
  max_governance_files_changed: 24
  reserve_verification_minutes: 15

deep_budget:
  max_scope_items: 120
  max_findings: 24
  max_repair_batches: 4
  max_files_changed: 48
  max_governance_files_changed: 48
  reserve_verification_minutes: 30

overnight_budget:
  max_runtime_minutes: 480
  max_cycles: 16
  max_scope_items: 240
  max_findings: 48
  max_repair_batches: 8
  max_files_changed: 96
  max_governance_files_changed: 96
  max_consecutive_failed_batches: 4
  reserve_verification_minutes: 45
""",
            json_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)

        # Preserve the supplied document for diagnostics and migration tooling.
        self.assertEqual(12, payload["config"]["budget"]["max_files_changed"])
        self.assertFalse(
            payload["config"]["autopilot"]["continue_after_budget_checkpoint"]
        )

        # Effective behavior is continuous regardless of obsolete quota values.
        effective = payload["effective_config"]
        self.assertTrue(effective["autopilot"]["continue_until_no_safe_work"])
        self.assertTrue(effective["autopilot"]["checkpoint_every_batch"])
        for legacy_section in ("budget", "deep_budget", "overnight_budget"):
            self.assertNotIn(legacy_section, effective)
        for legacy_key in (
            "max_runtime_minutes",
            "max_cycles",
            "max_budget_windows",
            "max_total_files_changed",
            "max_consecutive_failed_batches",
            "continue_after_budget_checkpoint",
        ):
            self.assertNotIn(legacy_key, effective["autopilot"])

        deprecated = set(payload["deprecated_paths"])
        for path in (
            "autopilot.max_runtime_minutes",
            "autopilot.max_cycles",
            "autopilot.max_budget_windows",
            "autopilot.max_total_files_changed",
            "autopilot.max_consecutive_failed_batches",
            "autopilot.continue_after_budget_checkpoint",
            "budget",
            "deep_budget",
            "overnight_budget",
        ):
            with self.subTest(path=path):
                self.assertIn(path, deprecated)

    def test_legacy_pause_flag_is_a_noop_not_an_autopilot_kill_switch(self) -> None:
        result = self.run_config(
            """version: 1
autopilot:
  continue_after_budget_checkpoint: false
""",
            json_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(
            payload["effective_config"]["autopilot"]["continue_until_no_safe_work"]
        )
        self.assertTrue(
            payload["effective_config"]["autopilot"]["checkpoint_every_batch"]
        )
        self.assertEqual(
            ["autopilot.continue_after_budget_checkpoint"],
            payload["deprecated_paths"],
        )

    def test_rejects_unknown_duplicate_bad_boolean_and_safety_regressions(self) -> None:
        cases = {
            "unknown": "version: 1\nunknown_section:\n  value: true\n",
            "duplicate": "version: 1\nversion: 1\n",
            "boolean": "version: 1\nreadonly:\n  allow_record_persistence: yes\n",
            "sensitive": "version: 1\nauth:\n  api_token: abc\n",
            "camel-sensitive": "version: 1\nauth:\n  accessToken: abc\n",
            "risk": "version: 1\nautonomy:\n  max_risk: R9\n",
            "production-write": "version: 1\nobserve:\n  production_read_only: false\n",
            "escaping-memory": "version: 1\nmemory_dir: ../outside\n",
            "absolute-memory": "version: 1\nmemory_dir: /tmp/outside\n",
            "disable-continuation": (
                "version: 1\nautopilot:\n  continue_until_no_safe_work: false\n"
            ),
            "disable-checkpoints": (
                "version: 1\nautopilot:\n  checkpoint_every_batch: false\n"
            ),
            # Legacy values are ignored only after they pass syntax/type validation.
            "negative-legacy-file-count": (
                "version: 1\nbudget:\n  max_files_changed: -1\n"
            ),
            "zero-legacy-window-count": (
                "version: 1\nautopilot:\n  max_budget_windows: 0\n"
            ),
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                result = self.run_config(content)
                self.assertEqual(1, result.returncode)
                self.assertIn("ERROR:", result.stdout)

    def test_rejects_ambiguous_yaml_features_and_indentation(self) -> None:
        for content in (
            "version: 1\nitems: [a, b]\n",
            "version: 1\n autonomy:\n  max_risk: R2\n",
            "version: 1\nautonomy:\n\tmax_risk: R2\n",
        ):
            with self.subTest(content=content):
                result = self.run_config(content)
                self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()
