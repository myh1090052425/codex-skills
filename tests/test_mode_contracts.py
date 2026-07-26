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
        self.assertIn("`RUN-*` or `BATCH-*`", resume)
        self.assertIn("latest_batch_id", resume)
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
            "autopilot",
            "overnight",
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

    def test_default_command_is_zero_prerequisite_autopilot(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        self.assertIn("`$software-evolution` or `autopilot [scope]`", skill)
        self.assertIn("No prerequisite command is required for the default route", skill)
        self.assertNotIn("`$software-evolution` or `govern", skill)
        self.assertIn("without requiring the user to run `init`, `audit`, or `govern` first", autopilot)
        self.assertIn("execute the safe initialization procedure", autopilot)
        self.assertIn("continue in the same run", autopilot)
        self.assertIn("immediately select the next safe batch", autopilot)

    def test_verify_can_independently_accept_run_or_batch(self) -> None:
        verify = (SKILL / "workflows" / "verify.md").read_text(encoding="utf-8")
        self.assertIn("`RUN-*`, `BATCH-*`", verify)
        self.assertIn("verify every claimed batch plus aggregate checks", verify)

    def test_ui_default_prompt_starts_zero_prerequisite_autopilot(self) -> None:
        agent = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        for phrase in ("$software-evolution", "零前置 Autopilot", "自动初始化", "持续发现"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, agent)

    def test_overnight_has_unattended_safety_and_resume_contract(self) -> None:
        overnight = (SKILL / "workflows" / "overnight.md").read_text(encoding="utf-8")
        governance = (SKILL / "governance" / "unattended-execution.md").read_text(encoding="utf-8")
        prompt = (SKILL / "templates" / "scheduled-overnight-task.md").read_text(encoding="utf-8")
        for phrase in (
            "isolated worktree",
            "overnight_budget",
            "final configured verification window",
            "Never perform",
            "RUN-*",
        ):
            self.assertIn(phrase, overnight)
        self.assertIn("Neither profile requires the user to run `init`, `audit`, or `govern` first", governance)
        self.assertIn("reuse the existing Overnight ledger and `overnight_budget`", (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8"))
        self.assertIn("Do not rerun Autopilot startup", overnight)
        self.assertIn("Do not wait for routine confirmation", prompt)
        self.assertIn("Never deploy", prompt)

    def test_public_docs_use_the_same_mode_vocabulary(self) -> None:
        documents = [
            ROOT / "README.md",
            ROOT / "docs" / "USAGE.md",
            ROOT / "docs" / "DESIGN.md",
        ]
        modes = (
            "autopilot",
            "overnight",
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
