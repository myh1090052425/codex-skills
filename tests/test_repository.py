from __future__ import annotations

import json
import re
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "software-evolution"
BOOTSTRAP = SKILL / "scripts" / "bootstrap_project_memory.py"
INTEGRITY = SKILL / "scripts" / "check_skill_integrity.py"
VALIDATOR = SKILL / "scripts" / "validate_project_config.py"
INSTALLER = ROOT / "install.py"


class RepositoryTests(unittest.TestCase):
    def test_bootstrap_creates_complete_control_plane_and_preserves_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-bootstrap-") as tmp:
            project = Path(tmp) / 'sample-"project'
            project.mkdir()

            first = subprocess.run(
                ["python3", str(BOOTSTRAP), "--root", str(project), "--date", "2026-07-26"],
                text=True,
                capture_output=True,
                check=True,
            )
            memory = project / "docs" / "software-evolution"
            self.assertEqual(
                {path.name for path in memory.iterdir()},
                {
                    "architecture-memory.md",
                    "capability-map.md",
                    "technical-debt.md",
                    "health-baseline.json",
                    "decisions",
                    "batches",
                    "runs",
                    "reports",
                },
            )
            self.assertEqual(
                {path.name for path in (memory / "reports").iterdir()},
                {"audit", "verification", "release", "observation"},
            )
            config = project / ".software-evolution.yml"
            self.assertTrue(config.is_file())
            self.assertIn("created_files=5", first.stdout)
            self.assertIn("created_dirs=7", first.stdout)
            health = json.loads((memory / "health-baseline.json").read_text(encoding="utf-8"))
            self.assertEqual('sample-"project', health["project"])
            self.assertEqual('sample-"project', health["repository"])
            for generated in (
                memory / "architecture-memory.md",
                memory / "capability-map.md",
                memory / "technical-debt.md",
                memory / "health-baseline.json",
            ):
                self.assertNotIn(str(project.parent), generated.read_text(encoding="utf-8"))
            subprocess.run(
                ["python3", str(VALIDATOR), "--config", str(config)],
                text=True,
                capture_output=True,
                check=True,
            )

            architecture = memory / "architecture-memory.md"
            architecture.write_text(
                architecture.read_text(encoding="utf-8") + "\nSENTINEL\n",
                encoding="utf-8",
            )
            config.write_text(config.read_text(encoding="utf-8") + "\n# SENTINEL\n", encoding="utf-8")
            second = subprocess.run(
                ["python3", str(BOOTSTRAP), "--root", str(project), "--date", "2026-07-26"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertIn("skipped_files=5", second.stdout)
            self.assertIn("existing_dirs=7", second.stdout)
            self.assertIn("SENTINEL", architecture.read_text(encoding="utf-8"))
            self.assertIn("SENTINEL", config.read_text(encoding="utf-8"))

    def test_bootstrap_dry_run_is_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-dry-run-") as tmp:
            project = Path(tmp) / 'sample-"project'
            project.mkdir()
            result = subprocess.run(
                ["python3", str(BOOTSTRAP), "--root", str(project), "--dry-run"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertIn("CREATE_DIR", result.stdout)
            self.assertIn("CREATE", result.stdout)
            self.assertEqual([], list(project.iterdir()))

    def test_bootstrap_rejects_relative_paths_that_escape_project(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-escape-") as tmp:
            project = Path(tmp) / "sample-project"
            project.mkdir()
            result = subprocess.run(
                [
                    "python3",
                    str(BOOTSTRAP),
                    "--root",
                    str(project),
                    "--output-dir",
                    "../outside",
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("escapes project root", result.stderr)
            self.assertFalse((Path(tmp) / "outside").exists())

    def test_installer_supports_symlink_and_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-install-") as tmp:
            tmp_path = Path(tmp)
            link_target = tmp_path / "links" / "software-evolution"
            copy_target = tmp_path / "copies" / "software-evolution"

            dry_run = subprocess.run(
                ["python3", str(INSTALLER), "--target", str(link_target), "--dry-run"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertIn("DRY-RUN", dry_run.stdout)
            self.assertFalse(link_target.exists())

            subprocess.run(
                ["python3", str(INSTALLER), "--target", str(link_target)],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertTrue(link_target.is_symlink())
            self.assertTrue((link_target / "SKILL.md").is_file())

            subprocess.run(
                ["python3", str(INSTALLER), "--target", str(copy_target), "--copy"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertFalse(copy_target.is_symlink())
            self.assertTrue((copy_target / "SKILL.md").is_file())
            self.assertTrue((copy_target / "workflows" / "audit.md").is_file())
            self.assertTrue((copy_target / "workflows" / "autopilot.md").is_file())
            self.assertTrue((copy_target / "workflows" / "overnight.md").is_file())
            self.assertTrue((copy_target / "scripts" / "check_checkpoint_drift.py").is_file())
            self.assertFalse(any(path.name == "__pycache__" for path in copy_target.rglob("*")))
            self.assertFalse(any(path.suffix == ".pyc" for path in copy_target.rglob("*")))

    def test_autopilot_run_template_has_parseable_resume_metadata(self) -> None:
        template = (SKILL / "templates" / "autopilot-run.md").read_text(encoding="utf-8")
        match = re.search(r"<!--\s*software-evolution-run\s*(\{.*?\})\s*-->", template, re.DOTALL)
        self.assertIsNotNone(match)
        metadata = json.loads(match.group(1))
        self.assertEqual(2, metadata["schema_version"])
        self.assertEqual("RUN-TBD", metadata["run_id"])
        self.assertIn("latest_batch_id", metadata)
        self.assertNotIn("window_index", metadata)
        self.assertIn("predecessor_run_id", metadata)
        self.assertEqual("INV-TBD", metadata["invocation_id"])
        self.assertEqual("", metadata["host_deadline"])
        self.assertEqual("ISO-8601-TBD", metadata["last_heartbeat_at"])
        for heading in (
            "## Continuity state",
            "## Execution metrics",
            "## Checkpoint ledger",
        ):
            self.assertIn(heading, template)
        self.assertIn("Counts are telemetry only", template)
        self.assertIn("Implementation paths touched", template)
        self.assertIn("Governance paths touched", template)
        self.assertIn("Legacy quota caused this stop: `must be no`", template)
        self.assertNotIn("Session hard budget", template)
        self.assertNotIn("Verification floor minutes", template)

    def test_skill_integrity_script(self) -> None:
        result = subprocess.run(
            ["python3", str(INTEGRITY)],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("11 mode contracts", result.stdout)


if __name__ == "__main__":
    unittest.main()
