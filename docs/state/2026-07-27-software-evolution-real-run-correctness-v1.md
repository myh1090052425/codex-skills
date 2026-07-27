# Software Evolution 真实运行行为纠偏

- 更新时间：2026-07-27
- 线程目标：基于真实 Autopilot 长会话回放，纠正 Skill 虽能连续执行但容易陷入单一技术问题族、错误宣称 safe work exhausted、缺少修复后浏览器体验验证、治理台账开销过重的问题，使默认命令真正覆盖用户/业务、工程/可靠性、架构/演进三条主线。
- 状态：已完成并发布

## 真实运行证据

- 指定会话本地记录约 28 MB、11,828 条事件、2,407 次工具调用，其中 2,259 次为 Shell 命令。
- 会话建立了 38 个 Batch；22 个为 Web 相关，22 个名称含 `PROTOCOL`，说明候选选择明显集中在同一响应协议问题族。
- 浏览器自动化仅在 init 阶段执行过一次只读烟测；后续大量 Web 修复未重新执行浏览器关键流程或截图/网络验证。
- Run 曾在当前响应边界候选耗尽后宣称 `safe work exhausted`，随后继续运行立即发现退出登录 false-success 问题，证明完成结论缺少跨治理主线反证扫描。
- 现有验证很强，但重复执行大量全仓验证与逐 Batch 治理文件，产品治理价值和控制面成本失衡。

## 根因

1. “跨三条治理主线扫描”只有原则，没有可验收的完成门禁。
2. 默认 Run 的仓库级范围会被当前 Batch/问题族悄然缩窄。
3. `safe work exhausted` 未要求最后一次修复后的跨主线反例搜索和运行态 UX 证据。
4. Browser 规则是“可用时优先”，未成为可运行 UI 项目的完成前置条件。
5. Run/Batch/验证记录缺少控制面比例原则和可复用验证证据规则。
6. 宿主持久 Goal 的完成状态没有绑定 Run 完成门禁。

## 已完成

1. 新增 `governance/coverage-and-completion.md`：维护用户/业务、工程/可靠性、架构/演进三主线候选组合；父 Run 与当前发现簇/Batch 分离；加入运行态 UX、跨主线完成挑战和比例化控制面。
2. 默认无范围 Autopilot 的 `scope_kind=repository`、`scope_paths=["."]` 保持稳定；同一问题族兄弟项必须与其他主线候选比较，单一问题族耗尽不再是停止条件。
3. 可安全运行的用户界面在仓库级完成前必须有浏览器关键旅程证据；用户可见修复后必须复验受影响旅程。
4. Run 模板升级为 schema v3，记录三主线覆盖、运行态 UX、开放 repair-ready 工作、跨主线挑战、验证复用指纹和真实 terminal reason。
5. 新增可执行 `scripts/validate_run_completion.py`：验证 Run 身份、仓库相对 scope、状态/终止原因一致性、三主线与 UX 覆盖、无开放修复、完整 Git SHA，以及覆盖矩阵、聚合验证、完成挑战和终止区无 `TBD` 占位证据。
6. 宿主持久 Goal 与父 Run 绑定；普通 Checkpoint、响应边界、恢复一个 Batch 或耗尽单一问题族都不能完成 Goal。
7. `RUN-*` 成为连续序列权威账本；小型 R1 不再机械创建独立 `BATCH-*`。验证只有在命令、环境、Revision、输入、依赖和受影响路径指纹一致时才能复用。
8. 同步 Autopilot、Common Loop、Deep、Overnight、Resume、UX、验证、技术债/记忆、报告模板、UI Metadata、README/USAGE/DESIGN/DEVELOPMENT 和 GitHub Actions。

## 验证结果

- `python3 -m py_compile install.py software-evolution/scripts/*.py tests/*.py`：通过。
- `check_skill_integrity.py`：54 个必需文件、11 个模式、链接、模板、Metadata 和可移植性通过。
- `skill-creator quick_validate.py`：`Skill is valid!`。
- `validate_run_completion.py` 运行中模板正例：通过。
- Run Completion 正反例覆盖单一问题族伪完成、开放修复、占位证据、非便携 scope、状态/终止原因不一致、仓库范围塌缩和完整完成：9/9 通过。
- 全部仓库测试：50/50 通过。
- 根文档链接、私有路径/Secret、旧 schema/控制文案、Tracked 生成噪音和 `git diff --check`：通过。

## 多角度 Review

1. **原始需求完整性**：UX、工程质量、架构/能力、持续演进、业务一致性、测试、稳定性、技术债、工程记忆和自主修改边界均保留；本次补的是闭环控制，不是替换原治理能力。
2. **真实会话反例**：单一 `PROTOCOL` 问题族不能缩小父 Run；继续同族前必须跨主线比较；刚宣布完成又发现新问题会被认定为覆盖失败并重开 Run。
3. **UX/browser**：可运行 UI 的关键旅程和用户可见修复后复验成为完成门禁，静态代码、Schema、组件测试或 HTTP 200 不能替代。
4. **工程验证正确性**：窄测试按修复、相关测试按波次、全仓门禁按风险/最终验收执行；昂贵验证复用必须匹配完整输入指纹。
5. **架构与能力主线**：能力所有权、重复能力、规则分裂、依赖方向和 Fitness Function 是独立主线，不会被易测试的工程问题永久饿死。
6. **Run/Batch scope 与恢复**：父 Run 稳定、Batch 语义窄；恢复时先 Drift/最后门禁，旧 Run 必须迁移 schema v3 后才能完成。
7. **宿主与无人值守**：Host durable goal 只在 Run Validator 通过后完成；Host 结束记录 `interrupted`，当前 Host 仍活跃且恢复路径明确时 Agent 自行继续。
8. **控制面成本**：Run 是 canonical ledger，小型 R1 可内联记录；独立 Batch/报告仅在风险、漂移、兼容或交接确有需要时创建。
9. **完成证明强度**：Validator 不接受只改 Metadata 的形式完成；真实身份、完整 SHA、正文证据、开放工作和终止语义均有机器门禁及负例测试。
10. **可移植性与发布**：无业务项目名称/本机路径/凭证进入公共 Skill 文档；安装复制包含新脚本；CI 已同步新 Validator 和测试。

## 阻塞

- 当前无实现阻塞。
- 目标业务项目存在大量并行改动且指定会话仍在运行；本线程始终只读分析，未修改、Stage、Commit 或 Push 该业务项目。

## 发布结果

- 功能提交：`b1a5a23 fix: 强化 Autopilot 覆盖与完成证明`。
- 已推送：`main`。
- GitHub Actions：`Validate Skill` Run `30234111201`，结论 `success`。
- 后续：在新的真实项目 Run 中观察三主线候选是否均衡、浏览器门禁是否被执行，以及完成 Validator 是否阻止形式化终止。

## 相关文件

- `software-evolution/SKILL.md`
- `software-evolution/workflows/`
- `software-evolution/governance/coverage-and-completion.md`
- `software-evolution/templates/autopilot-run.md`
- `software-evolution/scripts/validate_run_completion.py`
- `tests/test_run_completion.py`
- `README.md`
- `docs/USAGE.md`
- `docs/DESIGN.md`
- `docs/DEVELOPMENT.md`
- `.github/workflows/validate.yml`

## 关键决策

- 数量仍只作遥测；本次新增的是语义覆盖门禁，不是新的文件/Finding/Cycle/时间配额。
- 默认 Run 必须维护仓库级候选组合；单个 Batch 可以窄，但不能把 Run 偷换成当前问题族。
- `safe work exhausted` 是需要机器与正文证据共同证明的强结论，而不是当前搜索词没有结果。
- 旧 Run 内容不重写；恢复时保留历史并增量迁移 schema v3，完成前重新验证。
