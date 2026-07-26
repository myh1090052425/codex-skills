# Software Evolution 单命令 Autopilot 与睡后编程

- 更新时间：2026-07-26
- 线程目标：纠正默认入口设计，使 `$software-evolution`/`/software-evolution` 在任何项目中自动初始化控制面、建立认知、发现并修复问题、补测试、验证、再扫描并持续执行安全批次；补充 `overnight` 无人值守运行契约。
- 状态：已完成并发布

## 进展

- 已将无参数 `$software-evolution` 路由为零前置 `autopilot`，不再要求用户手工执行 `init → audit → govern`。
- 控制面缺失时会自动非覆盖式初始化，并在同一次运行中继续发现、证明、修复、补测试、验证、复扫和下一批选择。
- 已新增 `overnight` 睡后编程 Profile，包含隔离 worktree 优先、时间/循环/批次/文件/失败预算、最终验证预留和无人值守安全边界。
- 已新增 `RUN-*` 运行账本、Scheduled Task Prompt 模板和 `docs/software-evolution/runs/` 控制面目录。
- 已让 `resume` 支持 `RUN-*`/`BATCH-*`，并让 `verify` 能独立验收整个运行及其所有批次。
- 已更新 README、USAGE、DESIGN、DEVELOPMENT、Agent Metadata、配置模板、Bootstrap、内存模板和治理报告模板。
- 已按 OpenAI 官方文档复核：Codex 会自动检测 Skill 变更；未刷新时可重启；桌面端 Scheduled Tasks 可结合 Skill、本地项目和隔离 worktree，访问本地文件时电脑与应用需要保持运行。

## 多角度 Review 结果

1. **单命令语义**：确认默认入口完整覆盖自动初始化、建模、发现、修复、测试、验证、复扫和继续下一批。
2. **控制面初始化**：Bootstrap 新增 `runs/`，重复执行不覆盖已有文件，Dry Run 无副作用。
3. **循环与预算**：普通 Autopilot 和 Overnight 分别使用自身预算；已消除 Overnight 可能重置普通预算或创建嵌套 `RUN-*` 的歧义。
4. **无人值守安全**：生产写入、部署、迁移、权限/凭证、告警/Flag、远端发布、破坏性 Git 和 R3/R4 继续禁止自动执行。
5. **恢复与漂移**：修复 `check_checkpoint_drift.py` 未接受 `autopilot`/`overnight` 的问题；完整性脚本现在自动比较 11 个模式注册表，防止再次漏项。
6. **独立验收**：补齐 `RUN-*` Verify 契约，要求逐批和 Aggregate Evidence 验收。
7. **文档与触发**：SKILL、Agent 默认 Prompt、README、USAGE、DESIGN 和 DEVELOPMENT 已统一为零前置 Autopilot。
8. **可移植性与发布范围**：未发现本机绝对路径、凭证、Private Key、Token、缓存文件或无关改动。

## 阻塞

- 当前无阻塞。

## 下一步

1. 在真实业务项目中前向验证默认 `$software-evolution` 和 `$software-evolution overnight`。
2. 验证 `verify RUN-*`、`resume RUN-*` 和跨会话 Drift 恢复。
3. 根据真实运行反馈调整预算、风险阈值和专项 Skill 路由。

## 验证结果

- `python3 -m py_compile install.py software-evolution/scripts/*.py tests/*.py`：通过。
- 配置模板校验：通过。
- `check_skill_integrity.py`：通过，52 个必需文件、11 个模式契约。
- `skill-creator quick_validate.py`：通过。
- `python3 -m unittest discover -s tests -v`：25 项全部通过。
- `git diff --check`：通过。
- Markdown 本地链接和表格结构：通过。
- 可移植性、敏感信息和 tracked cache/generated artifact 检查：通过。
- 主提交：`d793893 feat: 实现单命令 Autopilot 与睡后编程`，已推送 `origin/main`。
- GitHub Actions：`Validate Skill` Run `30207427651`，结论 `success`。

## 相关文件

- `software-evolution/SKILL.md`
- `software-evolution/agents/openai.yaml`
- `software-evolution/workflows/autopilot.md`
- `software-evolution/workflows/overnight.md`
- `software-evolution/workflows/resume.md`
- `software-evolution/governance/unattended-execution.md`
- `software-evolution/templates/autopilot-run.md`
- `software-evolution/templates/scheduled-overnight-task.md`
- `software-evolution/memory/software-evolution.config.template.yml`
- `software-evolution/scripts/`
- `README.md`
- `docs/`
- `tests/`

## 关键决策

- 默认无参数入口必须是完整 Autopilot，而不是要求用户编排多个模式。
- `init`、`audit`、`govern`、`repair` 等模式继续保留，但仅作为高级控制面。
- 睡后编程只允许可证明、可回滚、可验证的 R1/R2 源码批次；不得把无人值守授权扩展到部署、生产写入、权限、迁移或远端发布。
- Overnight 继承 Autopilot 的自主循环，但必须沿用自身 `RUN-*` 和 `overnight_budget`，不得创建嵌套运行或重置预算。
- GitHub Actions 成功后才将本线程归档为完成；主提交对应 CI 已通过。
