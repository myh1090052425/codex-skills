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

    def test_template_is_valid(self) -> None:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "--config", str(TEMPLATE), "--json"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("OK", payload["status"])
        self.assertEqual([], payload["defaulted_paths"])
        effective = payload["effective_config"]
        self.assertEqual(240, effective["autopilot"]["max_runtime_minutes"])
        self.assertEqual(4, effective["autopilot"]["max_budget_windows"])
        self.assertTrue(effective["autopilot"]["continue_after_budget_checkpoint"])
        self.assertEqual(24, effective["budget"]["max_governance_files_changed"])
        self.assertEqual(96, effective["overnight_budget"]["max_governance_files_changed"])
        self.assertEqual(480, effective["overnight_budget"]["max_runtime_minutes"])

    def test_legacy_partial_config_gets_deterministic_effective_defaults(self) -> None:
        result = self.run_config(
            """version: 1
memory_dir: docs/software-evolution

autonomy:
  max_risk: R2
  allow_product_writes: true

budget:
  max_scope_items: 60
  max_findings: 12
  max_repair_batches: 2
  max_files_changed: 12
  reserve_verification_minutes: 15
""",
            json_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(12, payload["config"]["budget"]["max_files_changed"])
        effective = payload["effective_config"]
        self.assertEqual(240, effective["autopilot"]["max_runtime_minutes"])
        self.assertEqual(8, effective["autopilot"]["max_cycles"])
        self.assertEqual(4, effective["autopilot"]["max_budget_windows"])
        self.assertEqual(48, effective["autopilot"]["max_total_files_changed"])
        self.assertEqual(24, effective["budget"]["max_governance_files_changed"])
        self.assertEqual(480, effective["overnight_budget"]["max_runtime_minutes"])
        defaulted = set(payload["defaulted_paths"])
        for path in (
            "autopilot.max_runtime_minutes",
            "autopilot.max_cycles",
            "autopilot.max_budget_windows",
            "autopilot.max_total_files_changed",
            "autopilot.continue_after_budget_checkpoint",
            "budget.max_governance_files_changed",
            "deep_budget.max_governance_files_changed",
            "overnight_budget.max_governance_files_changed",
        ):
            with self.subTest(path=path):
                self.assertIn(path, defaulted)

    def test_explicit_new_budget_values_are_preserved(self) -> None:
        result = self.run_config(
            """version: 1
autopilot:
  max_runtime_minutes: 300
  max_budget_windows: 5
  continue_after_budget_checkpoint: false
budget:
  max_governance_files_changed: 31
""",
            json_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        effective = payload["effective_config"]
        self.assertEqual(300, effective["autopilot"]["max_runtime_minutes"])
        self.assertEqual(5, effective["autopilot"]["max_budget_windows"])
        self.assertFalse(effective["autopilot"]["continue_after_budget_checkpoint"])
        self.assertEqual(31, effective["budget"]["max_governance_files_changed"])
        self.assertNotIn(
            "budget.max_governance_files_changed", payload["defaulted_paths"]
        )

    def test_rejects_unknown_duplicate_bad_boolean_and_sensitive_keys(self) -> None:
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
            "no-unattended-checkpoint": "version: 1\nautopilot:\n  checkpoint_every_batch: false\n",
            "negative-governance-budget": "version: 1\nbudget:\n  max_governance_files_changed: -1\n",
            "zero-session-windows": "version: 1\nautopilot:\n  max_budget_windows: 0\n",
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
