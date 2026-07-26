# Software Evolution 连续预算与自动续跑修复

- 更新时间：2026-07-26
- 线程目标：修复真实项目前向验证暴露的预算记账与正常预算停止问题，使默认 Autopilot 不因治理文件占用产品文件额度或单个预算窗口结束而要求用户手工 `resume`。
- 状态：本地实现与验证完成，待 GitHub 发布验证

## 进展

- 已基于真实运行 `RUN-SE-AUTOPILOT-20260726-01` 和 `BATCH-SE-FALLBACK-20260726-01` 证明三项根因：Governance 文件错误占用 Implementation 文件额度、验证时间底线被当作一次性余额、Budget Window 被错误当作用户交互停止点。
- 已实现 Autopilot Session/Window 双层预算。默认 Session 为 240 分钟、8 Cycle、4 Window、48 个总 Implementation 文件；单 Window 为 60 Scope、12 Finding、2 Repair Batch、12 个 Implementation 文件、24 个 Governance 文件和 15 分钟验证底线。
- 已实现 Implementation/Governance 双账本；配置的 `memory_dir`、RUN/BATCH、治理报告和当前状态线程不再消耗产品 `max_files_changed`。
- `reserve_verification_minutes` 已明确为墙钟时间底线；执行测试不会把它记成余额 0，每个新 Window 都从剩余 Session 时间重新建立底线。
- Config Validator 新增模板默认值合并，JSON 输出包含 `config`、`effective_config` 和 `defaulted_paths`；旧版部分配置不再触发 Agent 自行发明 90 分钟等临时额度。
- 默认 Autopilot 可自动接管唯一、明确、非活跃 owner 持有的 budget-only `partial`；旧 Session 已过期时创建 linked successor，不篡改历史。
- 新 Run 元数据包含 `invocation_id`、`session_deadline`、`last_heartbeat_at`、`window_index` 和 `predecessor_run_id`。活跃 owner 的重叠 branch/scope 禁止接管或新建；未知 liveness 按歧义处理。
- 正常 Window 到限后会停止本窗口编辑、完成验证与复扫、更新 Window Ledger、重置窗口计数并在同一次 invocation 继续。只有显式 `continue_after_budget_checkpoint: false` 才形成配置型暂停点。
- 目标项目 `.software-evolution.yml` 已显式补齐新预算，Validator 输出 `defaulted_paths: []`；Run-01/Batch-01 历史记账纠正为 7 个 Implementation、5 个 Governance，仍保留真实 `partial` 终态。
- 未接管或覆盖目标项目活跃 Run-02。其前向运行已完成 Window 1 的两个批次，并在同一次 invocation 进入 Window 2，证明新续跑契约已实际生效。

## 多角度 Review

1. **预算记账**：默认值相互一致，Governance 独立记账，重复路径按适用 Window/Session 唯一计数；零 Repair/Implementation/Total/Governance 额度确定性降级只读。
2. **Window 自动续跑**：普通 Window 只作为验证与封账边界；续跑开启时禁止结束响应或要求 `resume`，显式关闭时记录 `configured checkpoint`。
3. **Session 硬停止**：仅运行时间、总 Cycle、总 Window、总 Implementation 文件、连续失败、安全/漂移/Host 中断等真实条件可终止；终止前必须寻找更小可完整验证批次。
4. **Resume 语义**：只用于真实中断、漂移、歧义或指定 RUN/BATCH；不能重置已消费 Session 预算，也不能代替普通 Window rollover。
5. **旧配置兼容**：部分旧配置通过 bundled template 确定性合并，显式值（包括显式暂停）保持不变；模板和目标项目配置均通过 JSON Validator。
6. **并发 Run 所有权**：新增可机读 owner/deadline/heartbeat；活跃或 liveness 不明的重叠 Run 禁止接管和并发新建，只有已证明的显式不重叠 Scope 可独立推进。
7. **文档一致性**：SKILL、OpenAI UI metadata、README、USAGE、DESIGN、DEVELOPMENT、Workflow、Governance、Template 和 CI 使用同一预算与恢复词汇；Markdown 链接、表格和本机路径扫描通过。
8. **安全与外部副作用**：Autopilot/Overnight 仍只授权仓库本地可逆 R1/R2；Commit/Push、部署、Migration 执行、生产/共享数据、权限、凭证、告警、Flag、远端发布和 R3/R4 保持独立授权门禁。

Review 中额外修复了三个边界：另一个活跃 owner 存在时不得走“否则新建 Run”；显式关闭自动续跑与零 Governance 额度必须有确定语义；heartbeat/deadline 必须进入可机读 Run 元数据。

## 验证结果

- `python3 -m py_compile install.py software-evolution/scripts/*.py tests/*.py`：通过。
- Config 模板 JSON Validator：`status: OK`，`defaulted_paths: []`。
- 目标项目配置 JSON Validator：`status: OK`，`defaulted_paths: []`。
- Skill Integrity：52 个必需文件、11 个模式契约、Frontmatter、链接、元数据、模板和可移植性通过。
- Skill Creator `quick_validate.py`：`Skill is valid!`。
- `python3 -m unittest discover -s tests -v`：33/33 通过。
- Budget coherence、Markdown 链接/表格、本机绝对路径、Secret-shaped content、tracked `.DS_Store`/`__pycache__`/`*.pyc` 和 `git diff --check`：通过。
- 本地存在的 `.DS_Store`、`__pycache__/`、`*.pyc` 均为 ignored，未纳入提交。

## 阻塞

- 本地实现无阻塞；尚待提交、推送并确认 GitHub Actions `Validate Skill`。

## 下一步

1. 复核最终 Git Diff 和提交范围。
2. 使用中文 Commit Message 提交并推送 `main`。
3. 确认 GitHub Actions `Validate Skill` 成功后归档本线程。

## 相关文件

- `software-evolution/SKILL.md`
- `software-evolution/workflows/autopilot.md`
- `software-evolution/workflows/common-loop.md`
- `software-evolution/workflows/overnight.md`
- `software-evolution/workflows/resume.md`
- `software-evolution/governance/budget-and-drift.md`
- `software-evolution/governance/unattended-execution.md`
- `software-evolution/memory/software-evolution.config.template.yml`
- `software-evolution/scripts/validate_project_config.py`
- `software-evolution/scripts/check_skill_integrity.py`
- `software-evolution/templates/autopilot-run.md`
- `software-evolution/templates/batch-checkpoint.md`
- `tests/`
- `README.md`、`docs/USAGE.md`、`docs/DESIGN.md`、`docs/DEVELOPMENT.md`

## 关键决策

- `budget.max_files_changed` 只约束 Implementation 文件，不再与治理状态文件共用额度。
- 单个 Budget Window 是内部安全检查点，不是默认 Autopilot 的用户交互边界。
- `reserve_verification_minutes` 是墙钟时间底线，不是可消费余额。
- `resume` 只用于真实中断、漂移、歧义或显式目标恢复；正常 Window 滚动不要求用户再次下命令。
- 活跃 invocation owner 是并发边界；Autopilot 不以自治为理由接管或创建重叠 Run。
