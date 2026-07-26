# Software Evolution 控制面与治理闭环升级

- 更新时间：2026-07-26
- 线程目标：将现有 `software-evolution` Skill 从“会发现并修复问题”升级为具备只读控制面、独立验收、发布治理、运行反馈、专业路由、决策治理、恢复协议和预算控制的长期技术负责人 Agent。
- 状态：待提交/发布

## 进展

- 已完成九种模式及 Write Policy：`init`、`audit`、`govern`、`repair`、`verify`、`deep`、`release-check`、`observe`、`resume`。
- 已将公共流程拆为共享只读证据阶段、只读出口和可写出口，消除无条件 Repair。
- 已新增发布/迁移、可观测性、专业路由、决策、预算/漂移、Architecture Fitness 治理规则。
- 已新增 Audit、Verification、Release、Observation、Incident、Decision、Batch、Specialist Handoff 模板。
- 已新增受限项目配置、健康基线、配置校验和 Git Checkpoint Drift 脚本。
- 初始化器已升级为非覆盖式创建完整项目控制面。
- README、使用、设计、开发文档和 GitHub Actions 已同步新模式。
- 已完成结构、只读安全、脚本行为、恢复预算、文档一致性、可移植性和 Git Scope 七个角度的 Review。
- Review 发现已修复：只读模式隐含写入、Read-only Bootstrap、同路径内容漂移漏检、相对路径逃逸、配置目录逃逸、JSON 模板转义、本机绝对路径、安装缓存夹带、Init 语义不一致、Resume 权限继承、浏览器流程数据写入和稳定 ID 不一致。
- 当前自动测试 19 项全部通过；8 项最终本地门禁全部通过。

## 阻塞

- N/A；当前无已知阻塞。

## 下一步

1. 提交并推送控制面升级。
2. 确认 GitHub Actions `Validate Skill` 通过。
3. 记录发布 Commit、CI 结果并归档本线程。
4. 在真实项目中分别前向验证 `audit`、`govern`、`verify`、`release-check` 和 `resume`。

## 验证结果

1. Python 语法检查：通过。
2. 配置模板校验：通过。
3. `python3 software-evolution/scripts/check_skill_integrity.py`：通过，47 个必需文件、9 个模式契约。
4. `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py software-evolution`：通过。
5. `python3 -m unittest discover -s tests -v`：19 项全部通过。
6. 47 个 Markdown 文件的表格和本地链接检查：通过。
7. `git diff --check`：通过。
8. 本机路径、凭证模式和已跟踪缓存/生成物检查：通过。
9. GitHub Actions：待推送后验证。

## 相关文件

- `software-evolution/SKILL.md`
- `software-evolution/workflows/`
- `software-evolution/governance/`
- `software-evolution/templates/`
- `software-evolution/memory/`
- `software-evolution/scripts/`
- `tests/`
- `README.md`
- `docs/`
- `.github/workflows/validate.yml`

## 关键决策

- `audit`、`verify`、`release-check` 和 `observe` 默认严格只读；只有用户显式要求或指定 `--record` 时，才允许持久化模式报告和必要 `DEC-*` 决策包，且仍不得修改产品代码、项目配置、数据或生产状态。
- `govern` 只允许小批次 R1/R2 自主修复；`repair` 只修复已被证明的问题；`deep` 必须声明预算并分片执行。
- `resume` 必须校验分支、HEAD、工作树状态与内容、Scope Drift；无法证明原写权限和验证条件时降级为只读重建证据。
- 主 Skill 负责识别和路由安全、供应链、数据、性能/成本、UX、数据库和 CI/CD 专业治理，不把全部专项规则继续塞入主流程。
- 生产环境默认只读；部署、回滚、迁移、告警/Flag/权限修改、数据写入和 Git 历史重写继续要求明确批准。
- 稳定治理 ID 统一使用 `CAP-*`、`FIND-*`、`DEBT-*`、`DEC-*`、`BATCH-*`、`VER-*`、`REL-*`、`FIT-*`。
