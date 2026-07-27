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
                self.assertNotIn("WRITE POLICY: CONTINUOUS_WRITE", text)

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
        self.assertIn(
            "without requiring `init`, `audit`, `govern`, or routine `resume`",
            autopilot,
        )
        self.assertIn("execute [init.md](init.md) automatically", autopilot)
        self.assertIn("continue in the same run", autopilot)
        self.assertIn("immediately select the next globally highest-value safe root cause", autopilot)

    def test_continuous_modes_use_continuous_write_contract(self) -> None:
        for mode in ("autopilot", "overnight", "deep"):
            with self.subTest(mode=mode):
                text = (SKILL / "workflows" / f"{mode}.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("WRITE POLICY: CONTINUOUS_WRITE", text)
                self.assertIn("continue", text.lower())

    def test_counts_are_telemetry_and_never_stop_conditions(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        continuity = (SKILL / "governance" / "continuity-and-drift.md").read_text(
            encoding="utf-8"
        )
        batch = (SKILL / "templates" / "batch-checkpoint.md").read_text(
            encoding="utf-8"
        )
        agent = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("## Checkpoint cadence, not quotas", autopilot)
        self.assertIn("telemetry only", autopilot)
        self.assertIn(
            "One successful repair, a large diff, or a high file count is never a stop condition",
            autopilot,
        )
        self.assertIn("A coherent repair may touch one file or hundreds", continuity)
        self.assertIn("Never use the metrics to manufacture a hard stop", continuity)
        self.assertIn("These values are telemetry, never execution limits", batch)
        self.assertIn("不得作为停止条件", agent)

    def test_semantic_batch_boundary_replaces_file_quota(self) -> None:
        continuity = (SKILL / "governance" / "continuity-and-drift.md").read_text(
            encoding="utf-8"
        )
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        for phrase in (
            "one root cause, capability, invariant, contract boundary, or compatibility stage",
            "Known callers and affected data/runtime boundaries",
            "Reversibility and rollback/roll-forward path",
            "Availability of regression and broader verification",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, continuity)
        self.assertIn("“Smallest coherent” is semantic", autopilot)
        self.assertIn("Split a coherent root-cause repair merely to satisfy a file quota", autopilot)

    def test_autopilot_has_only_real_stop_conditions(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        self.assertIn("## Real stop conditions", autopilot)
        for phrase in (
            "Do not infer `safe work exhausted` from the current search query or taxonomy",
            "user/business, engineering/reliability, and architecture/evolution coverage",
            "open_repair_ready_work=false",
            "validate_run_completion.py",
            "Use `partial`, `blocked`, or `interrupted` instead",
            "the host interrupts, rate-limits, suspends, or ends the task",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, autopilot)
        self.assertIn("is never a stop condition", autopilot)

    def test_targeted_modes_do_not_reintroduce_local_execution_budgets(self) -> None:
        for relative in (
            "workflows/audit.md",
            "workflows/govern.md",
            "workflows/repair.md",
            "templates/audit-report.md",
            "templates/governance-report.md",
            "templates/repair-plan.md",
        ):
            with self.subTest(relative=relative):
                text = (SKILL / relative).read_text(encoding="utf-8")
                self.assertNotIn("budget", text.lower())

    def test_three_failed_attempts_quarantine_only_that_hypothesis(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        risk = (SKILL / "governance" / "autonomy-and-risk.md").read_text(
            encoding="utf-8"
        )
        unattended = (SKILL / "governance" / "unattended-execution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Quarantine the same failing repair hypothesis after three attempts", skill)
        self.assertIn("Continue other independent safe work", risk)
        self.assertIn("Continue independent safe work after quarantining", unattended)

    def test_autopilot_does_not_create_overlapping_owned_runs(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        continuity = (SKILL / "governance" / "continuity-and-drift.md").read_text(
            encoding="utf-8"
        )
        unattended = (SKILL / "governance" / "unattended-execution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("another active owner's run", autopilot)
        self.assertIn("Unknown liveness is ambiguous, not abandoned", autopilot)
        self.assertIn("Another active owner is a concurrency boundary", continuity)
        self.assertIn("Unknown liveness is ambiguous, not abandoned", unattended)

    def test_recoverable_partial_is_adopted_but_quota_is_not_restored(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        continuity = (SKILL / "governance" / "continuity-and-drift.md").read_text(
            encoding="utf-8"
        )
        resume = (SKILL / "workflows" / "resume.md").read_text(encoding="utf-8")
        self.assertIn("Recoverable partial auto-adoption", autopilot)
        self.assertIn("## Recoverable partial adoption", continuity)
        self.assertIn("Do not recreate or honor an obsolete quota", continuity)
        self.assertIn(
            "Treat historical file/cycle/window/finding/batch quotas as deprecated evidence",
            resume,
        )
        self.assertIn("Do not reset or recreate obsolete quota counters", resume)

    def test_resume_uses_drift_and_real_interruption_not_routine_checkpoints(self) -> None:
        resume = (SKILL / "workflows" / "resume.md").read_text(encoding="utf-8")
        self.assertIn("drifted, ambiguous, specifically targeted, or otherwise non-auto-adoptable", resume)
        self.assertIn("Normal batch checkpoints continue automatically", resume)
        self.assertIn("Do not use `resume` to restart work after a normal checkpoint", resume)
        for classification in (
            "NO_DRIFT",
            "SAFE_DRIFT",
            "MATERIAL_DRIFT",
            "CONFLICTING_DRIFT",
            "UNKNOWN",
        ):
            self.assertIn(classification, resume)

    def test_default_run_scope_does_not_collapse_to_current_cluster(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        common = (SKILL / "workflows" / "common-loop.md").read_text(encoding="utf-8")
        coverage = (SKILL / "governance" / "coverage-and-completion.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("scope_kind=repository", autopilot)
        self.assertIn("later Batch scopes must not replace the parent scope", autopilot)
        self.assertIn("current defect family does not become the implicit Run scope", common)
        self.assertIn("Completing it never shrinks the parent run", coverage)

    def test_autopilot_completion_requires_cross_lane_challenge(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        common = (SKILL / "workflows" / "common-loop.md").read_text(encoding="utf-8")
        run_template = (SKILL / "templates" / "autopilot-run.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Cross-lane completion challenge", autopilot)
        self.assertIn("outside the current module/taxonomy/test pattern", autopilot)
        self.assertIn("counterexample search outside the current module/taxonomy/test pattern", common)
        self.assertIn("## Completion challenge", run_template)
        self.assertIn("validate_run_completion.py", run_template)

    def test_runnable_ui_requires_browser_evidence_before_completion(self) -> None:
        ux = (SKILL / "governance" / "user-experience.md").read_text(encoding="utf-8")
        coverage = (SKILL / "governance" / "coverage-and-completion.md").read_text(
            encoding="utf-8"
        )
        common = (SKILL / "workflows" / "common-loop.md").read_text(encoding="utf-8")
        self.assertIn("Browser/runtime evidence is a completion gate", ux)
        self.assertIn("Static source review", coverage)
        self.assertIn("component tests alone are insufficient", common)

    def test_host_goal_completion_is_bound_to_run_validator(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        unattended = (SKILL / "governance" / "unattended-execution.md").read_text(
            encoding="utf-8"
        )
        common = (SKILL / "workflows" / "common-loop.md").read_text(encoding="utf-8")
        self.assertIn("bind it to the active `RUN-*`", autopilot)
        self.assertIn("Do not mark that goal complete", unattended)
        self.assertIn("Do not mark a host durable goal complete", common)

    def test_control_plane_is_proportional_and_verification_can_be_reused(self) -> None:
        coverage = (SKILL / "governance" / "coverage-and-completion.md").read_text(
            encoding="utf-8"
        )
        common = (SKILL / "workflows" / "common-loop.md").read_text(encoding="utf-8")
        self.assertIn("## Proportional control plane", coverage)
        self.assertIn("A small R1 repair may use a concise Run row", coverage)
        self.assertIn("matching command/environment/revision/input/dependency fingerprints", common)

    def test_single_defect_family_exhaustion_is_not_safe_work_exhausted(self) -> None:
        autopilot = (SKILL / "workflows" / "autopilot.md").read_text(encoding="utf-8")
        common = (SKILL / "workflows" / "common-loop.md").read_text(encoding="utf-8")
        self.assertIn("exhaustion of the current defect family is never a stop condition", autopilot)
        self.assertIn("one exhausted taxonomy", common)

    def test_verify_can_independently_accept_run_or_batch(self) -> None:
        verify = (SKILL / "workflows" / "verify.md").read_text(encoding="utf-8")
        self.assertIn("`RUN-*`, `BATCH-*`", verify)
        self.assertIn("verify every claimed batch plus aggregate checks", verify)

    def test_ui_default_prompt_starts_continuous_zero_prerequisite_autopilot(self) -> None:
        agent = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        for phrase in ("$software-evolution", "零前置连续 Autopilot", "自动初始化", "持续发现"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, agent)

    def test_overnight_uses_host_lifecycle_not_local_quotas(self) -> None:
        overnight = (SKILL / "workflows" / "overnight.md").read_text(encoding="utf-8")
        governance = (SKILL / "governance" / "unattended-execution.md").read_text(
            encoding="utf-8"
        )
        prompt = (SKILL / "templates" / "scheduled-overnight-task.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "isolated worktree",
            "while the host remains available",
            "Never perform",
            "RUN-*",
        ):
            self.assertIn(phrase, overnight)
        self.assertIn(
            "Neither profile requires `init`, `audit`, `govern`, or routine `resume` first",
            governance,
        )
        self.assertIn("Do not rerun Autopilot startup", overnight)
        self.assertIn("Do not wait for routine confirmation", prompt)
        self.assertIn("Do not stop because of file, finding, cycle, checkpoint, or repair-batch counts", prompt)
        self.assertIn("Never deploy", prompt)

    def test_public_docs_use_mode_vocabulary_and_continuous_model(self) -> None:
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
            self.assertIn("遥测", text)
            self.assertIn("真实停止条件", text)
            self.assertNotIn("Session 硬上限", text)
            self.assertNotIn("Window 到限", text)


if __name__ == "__main__":
    unittest.main()
