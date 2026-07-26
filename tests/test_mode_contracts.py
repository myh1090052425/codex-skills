from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "software-evolution"


class ModeContractTests(unittest.TestCase):
    def test_read_only_modes_declare_and_enforce_read_only_exit(self) -> None:
        for name in ("audit", "verify", "release-check", "observe"):
            with self.subTest(mode=name):
                text = (SKILL / "workflows" / f"{name}.md").read_text(encoding="utf-8")
                self.assertIn("WRITE POLICY: READ_ONLY", text)
                self.assertIn("Do not", text)
                self.assertNotIn("WRITE POLICY: BOUNDED_WRITE", text)

    def test_read_only_modes_do_not_bootstrap_or_update_memory(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        observe = (SKILL / "workflows" / "observe.md").read_text(encoding="utf-8")
        self.assertIn("Never run it from `audit`, `verify`, `release-check`, `observe`", skill)
        self.assertIn("never update them in observe mode", observe)
        self.assertIn("persist only the observation report", observe)

    def test_common_loop_separates_read_only_and_writable_exits(self) -> None:
        text = (SKILL / "workflows" / "common-loop.md").read_text(encoding="utf-8")
        read_index = text.index("## Read-only exit")
        write_index = text.index("## Writable exit")
        self.assertLess(read_index, write_index)
        self.assertIn("Do not perform it in the read-only mode", text)

    def test_deep_and_resume_have_budget_and_drift_guards(self) -> None:
        deep = (SKILL / "workflows" / "deep.md").read_text(encoding="utf-8")
        resume = (SKILL / "workflows" / "resume.md").read_text(encoding="utf-8")
        self.assertIn("Verification reserve", deep)
        for classification in (
            "NO_DRIFT",
            "SAFE_DRIFT",
            "MATERIAL_DRIFT",
            "CONFLICTING_DRIFT",
            "UNKNOWN",
        ):
            self.assertIn(classification, resume)

    def test_skill_routes_all_modes(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for mode in (
            "init",
            "audit",
            "govern",
            "repair",
            "verify",
            "deep",
            "release-check",
            "observe",
            "resume",
        ):
            self.assertIn(f"workflows/{mode}.md", text)

    def test_public_docs_use_the_same_mode_vocabulary(self) -> None:
        documents = [
            ROOT / "README.md",
            ROOT / "docs" / "USAGE.md",
            ROOT / "docs" / "DESIGN.md",
        ]
        modes = (
            "init",
            "audit",
            "govern",
            "repair",
            "verify",
            "deep",
            "release-check",
            "observe",
            "resume",
        )
        for document in documents:
            text = document.read_text(encoding="utf-8")
            for mode in modes:
                with self.subTest(document=document.name, mode=mode):
                    self.assertIn(mode, text)


if __name__ == "__main__":
    unittest.main()
