from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DRIFT = ROOT / "software-evolution" / "scripts" / "check_checkpoint_drift.py"


class CheckpointDriftTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            text=True,
            capture_output=True,
            check=True,
        )

    def make_repo(self, base: Path) -> Path:
        repo = base / "repo"
        (repo / "src").mkdir(parents=True)
        (repo / "src" / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
        (repo / "README.md").write_text("baseline\n", encoding="utf-8")
        self.git(repo, "init", "-b", "main")
        self.git(repo, "config", "user.name", "Codex Test")
        self.git(repo, "config", "user.email", "codex@example.invalid")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "initial")
        return repo

    def snapshot(self, repo: Path) -> dict[str, object]:
        result = subprocess.run(
            [
                "python3",
                str(DRIFT),
                "--root",
                str(repo),
                "--snapshot",
                "--batch-id",
                "BATCH-TEST",
                "--mode",
                "repair",
                "--scope-path",
                "src/app.py",
            ],
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    def checkpoint(self, base: Path, metadata: dict[str, object]) -> Path:
        path = base / "BATCH-TEST.md"
        path.write_text(
            "<!-- software-evolution-checkpoint\n"
            + json.dumps(metadata, indent=2)
            + "\n-->\n# Batch\n",
            encoding="utf-8",
        )
        return path

    def classify(self, repo: Path, checkpoint: Path) -> str:
        result = subprocess.run(
            ["python3", str(DRIFT), "--root", str(repo), "--checkpoint", str(checkpoint)],
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.splitlines()[0]

    def test_no_safe_material_and_conflicting_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-drift-") as tmp:
            base = Path(tmp)
            repo = self.make_repo(base)
            checkpoint = self.checkpoint(base, self.snapshot(repo))

            self.assertEqual("NO_DRIFT", self.classify(repo, checkpoint))

            self.git(repo, "switch", "-c", "other")
            self.assertEqual("CONFLICTING_DRIFT", self.classify(repo, checkpoint))
            self.git(repo, "switch", "main")

            (repo / "notes.txt").write_text("untracked\n", encoding="utf-8")
            self.assertEqual("SAFE_DRIFT", self.classify(repo, checkpoint))
            (repo / "notes.txt").unlink()

            (repo / "README.md").write_text("tracked drift\n", encoding="utf-8")
            self.assertEqual("MATERIAL_DRIFT", self.classify(repo, checkpoint))
            self.git(repo, "checkout", "--", "README.md")

            (repo / "src" / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
            self.assertEqual("CONFLICTING_DRIFT", self.classify(repo, checkpoint))
            self.git(repo, "checkout", "--", "src/app.py")

            (repo / "README.md").write_text("new commit\n", encoding="utf-8")
            self.git(repo, "add", "README.md")
            self.git(repo, "commit", "-m", "advance head")
            self.assertEqual("MATERIAL_DRIFT", self.classify(repo, checkpoint))

    def test_content_change_is_detected_when_status_text_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-drift-content-") as tmp:
            base = Path(tmp)
            repo = self.make_repo(base)
            app = repo / "src" / "app.py"
            app.write_text("VALUE = 2\n", encoding="utf-8")
            checkpoint = self.checkpoint(base, self.snapshot(repo))
            app.write_text("VALUE = 3\n", encoding="utf-8")
            self.assertEqual("CONFLICTING_DRIFT", self.classify(repo, checkpoint))

    def test_snapshot_accepts_autopilot_and_overnight_modes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-drift-modes-") as tmp:
            repo = self.make_repo(Path(tmp))
            for mode in ("autopilot", "overnight"):
                with self.subTest(mode=mode):
                    result = subprocess.run(
                        [
                            "python3",
                            str(DRIFT),
                            "--root",
                            str(repo),
                            "--snapshot",
                            "--batch-id",
                            f"BATCH-{mode.upper()}",
                            "--mode",
                            mode,
                            "--scope-path",
                            "src/app.py",
                        ],
                        text=True,
                        capture_output=True,
                        check=True,
                    )
                    metadata = json.loads(result.stdout)
                    self.assertEqual(mode, metadata["mode"])
                    checkpoint = self.checkpoint(Path(tmp), metadata)
                    self.assertEqual("NO_DRIFT", self.classify(repo, checkpoint))

    def test_snapshot_accepts_repository_root_scope(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-drift-root-scope-") as tmp:
            repo = self.make_repo(Path(tmp))
            result = subprocess.run(
                [
                    "python3",
                    str(DRIFT),
                    "--root",
                    str(repo),
                    "--snapshot",
                    "--scope-path",
                    ".",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertEqual(["."], json.loads(result.stdout)["scope_paths"])

    def test_snapshot_rejects_non_portable_scope(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-drift-scope-") as tmp:
            repo = self.make_repo(Path(tmp))
            result = subprocess.run(
                [
                    "python3",
                    str(DRIFT),
                    "--root",
                    str(repo),
                    "--snapshot",
                    "--scope-path",
                    "../outside",
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(2, result.returncode)
            self.assertEqual("UNKNOWN", result.stdout.splitlines()[0])
            self.assertIn("project-relative", result.stdout)

    def test_invalid_checkpoint_is_unknown(self) -> None:
        with tempfile.TemporaryDirectory(prefix="software-evolution-drift-invalid-") as tmp:
            base = Path(tmp)
            repo = self.make_repo(base)
            checkpoint = base / "invalid.md"
            checkpoint.write_text("# no metadata\n", encoding="utf-8")
            result = subprocess.run(
                ["python3", str(DRIFT), "--root", str(repo), "--checkpoint", str(checkpoint)],
                text=True,
                capture_output=True,
            )
            self.assertEqual(2, result.returncode)
            self.assertEqual("UNKNOWN", result.stdout.splitlines()[0])


if __name__ == "__main__":
    unittest.main()
