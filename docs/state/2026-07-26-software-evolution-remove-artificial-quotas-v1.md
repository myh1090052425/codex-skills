# Software Evolution 去除人为数量配额

- 更新时间：2026-07-26
- 线程目标：纠正将文件数、Cycle、Window、Finding 和 Repair Batch 数量作为 Autopilot 硬停止条件的设计错误，使自主治理由风险、证据、可回滚性和验证能力控制，而不是按计数停止。
- 状态：待发布

## 进展

- 已重新对照用户原始目标：有明确问题且具备验证条件时应自主修复、补测试、验证、复扫并继续，不应因修改文件数量达到任意阈值而退回用户。
- 已移除默认配置中的 Session/Window、文件、Finding、Cycle、Repair Batch 和验证预留配额；`autopilot` 只保留 `continue_until_no_safe_work: true` 与 `checkpoint_every_batch: true`。
- 已将 Autopilot、Overnight 和 Deep 统一为 `CONTINUOUS_WRITE`：按根因、业务能力、不变量、契约边界或兼容阶段形成语义批次，在每批验证和 Checkpoint 后继续下一项安全工作。
- 已将文件数、Diff、Finding、Cycle、Batch 和耗时降为 Blast Radius、审计、趋势与恢复遥测，明确禁止作为授权、拆批或终止条件。
- 已将风险控制收敛为 Mode、Risk、Authority、Reversibility、Verification；高文件数只提高调用方分析、回滚和验证要求，不自动触发停工或询问。
- 已将同一修复假设连续失败三次的处理改为“隔离该假设并继续其他独立安全工作”，不再结束整个治理运行。
- 已把默认恢复扩展为：唯一、非活跃、Drift-safe 的宿主中断或旧配额型 `partial` 可由下一次普通 `$software-evolution` 自动接管；歧义、漂移和指定恢复继续使用 `resume <id>`。
- 已将治理文件 `budget-and-drift.md` 重命名为 `continuity-and-drift.md`，移除 Audit、Govern、Repair、Repair Plan 和状态模板中的旧本地执行预算语义。
- 已更新 README、USAGE、DESIGN、DEVELOPMENT、Skill Metadata、运行/批次模板、配置 Validator、完整性检查和回归测试。

## 兼容性

- 旧 `budget`、`deep_budget`、`overnight_budget` 与旧 `autopilot.max_*` 仍可被 Validator 解析，避免既有项目配置失效。
- 旧键保留在 JSON 的原始 `config` 中用于诊断，但从 `effective_config` 中剥离，并通过 `deprecated_paths` 明确报告。
- 已使用完整旧配置 Fixture 执行兼容验证：状态 `OK`，旧配额全部进入 `deprecated_paths`，有效 Autopilot 配置只保留连续执行和逐批 Checkpoint。首次只读检查时一个真实项目仍使用旧配额并得到同样结果；后续并行项目任务已自行迁移该配置，最终只读复核仍为 `OK`、`deprecated_paths=[]`。本线程未修改该项目任何文件。

## 多角度 Review

1. **目标一致性**：默认命令无需前置模式，安全可验证工作存在时持续发现、修复、验证和复扫。
2. **行为契约**：Autopilot、Overnight、Deep 使用连续写契约；Audit、Verify、Release Check、Observe 保持严格只读。
3. **风险边界**：移除数量配额后仍保留业务权威、R3/R4、生产/外部副作用、可逆性、验证和用户并行改动门禁。
4. **恢复与并发**：Run owner/heartbeat、Drift 五分类、有效 Checkpoint、唯一可恢复 partial 自动接管和重叠 scope 禁止并发保持有效。
5. **配置迁移**：新模板无人工配额；旧配置兼容读取但不能恢复旧行为；显式旧暂停开关为 no-op。
6. **失败隔离**：三次失败只隔离单一假设，仍继续其他独立安全工作。
7. **结构与文档**：Skill 链接、模式、模板、Agent Metadata、README、USAGE、DESIGN、DEVELOPMENT 已统一到连续自治模型。
8. **可移植性与仓库卫生**：无本机绝对路径、私钥标记或 tracked `.DS_Store`/`__pycache__`/`*.pyc`；业务项目改动未进入本仓库范围。

## 验证结果

- `python3 -m py_compile install.py software-evolution/scripts/*.py tests/*.py`：通过。
- `python3 software-evolution/scripts/check_skill_integrity.py`：通过，52 个必需文件、11 个模式契约。
- 系统 `skill-creator` `quick_validate.py software-evolution`：通过。
- 新配置模板 Validator JSON：`status=OK`、`defaulted_paths=[]`、`deprecated_paths=[]`。
- 完整旧配置 Fixture：`status=OK`，9 个旧路径进入 `deprecated_paths`，旧配额不进入 `effective_config`。
- 真实项目最终配置只读复核：`status=OK`、`deprecated_paths=[]`；并行项目改动未进入本仓库。
- `python3 -m unittest discover -s tests -v`：35/35 通过。
- 根文档链接、Skill 内链接、可移植性/Secret 扫描、tracked 垃圾文件扫描和 `git diff --check`：通过。

## 阻塞

- 当前无实现阻塞。
- GitHub Commit、Push 和远端 `Validate Skill` 尚待完成。

## 下一步

1. 复核最终 Diff 和 Staged Scope。
2. 使用中文 Commit Message 提交并推送 `main`。
3. 确认 GitHub Actions `Validate Skill` 成功后归档本线程。

## 相关文件

- `software-evolution/SKILL.md`
- `software-evolution/workflows/`
- `software-evolution/governance/`
- `software-evolution/memory/software-evolution.config.template.yml`
- `software-evolution/scripts/validate_project_config.py`
- `software-evolution/scripts/check_skill_integrity.py`
- `software-evolution/templates/`
- `tests/`
- `README.md`、`docs/`

## 关键决策

- 文件数量是观测和 Review 信息，不是风险模型，也不是用户授权边界。
- 批次边界按一个根因、一个业务能力、一个不变量、一个契约边界或一个兼容性阶段划分，不按文件数量划分。
- 默认持续执行，直到没有安全可验证工作、所有候选均被真实权威/安全/环境/漂移边界阻塞，或 Host 中断。
- Skill 不再自行发明运行时长或验证预留配额；Host 明确提供的生命周期只用于判断能否完整完成当前验证。
- 旧配额只作为迁移输入和历史证据，永远不能重新成为有效执行控制。
