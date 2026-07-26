from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "software-evolution"
BOOTSTRAP = SKILL / "scripts" / "bootstrap_project_memory.py"
INSTALLER = ROOT / "install.py"


class RepositoryTests(unittest.TestCase):
    def test_bootstrap_creates_and_preserves_memory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-bootstrap-") as tmp:
            project = Path(tmp) / "sample-project"
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
                },
            )
            self.assertIn("created=3", first.stdout)

            architecture = memory / "architecture-memory.md"
            architecture.write_text(
                architecture.read_text(encoding="utf-8") + "\nSENTINEL\n",
                encoding="utf-8",
            )
            second = subprocess.run(
                ["python3", str(BOOTSTRAP), "--root", str(project), "--date", "2026-07-26"],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertIn("skipped=3", second.stdout)
            self.assertIn("SENTINEL", architecture.read_text(encoding="utf-8"))

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


if __name__ == "__main__":
    unittest.main()
