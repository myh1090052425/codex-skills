from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "software-evolution" / "scripts" / "validate_project_config.py"
TEMPLATE = ROOT / "software-evolution" / "memory" / "software-evolution.config.template.yml"


class ProjectConfigTests(unittest.TestCase):
    def run_config(self, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="software-evolution-config-") as tmp:
            path = Path(tmp) / ".software-evolution.yml"
            path.write_text(content, encoding="utf-8")
            return subprocess.run(
                ["python3", str(VALIDATOR), "--config", str(path)],
                text=True,
                capture_output=True,
            )

    def test_template_is_valid(self) -> None:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "--config", str(TEMPLATE)],
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("OK:", result.stdout)
        self.assertIn("allow_record_persistence: true", TEMPLATE.read_text(encoding="utf-8"))

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
