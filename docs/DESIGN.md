# 设计说明

## 1. 定位

`software-evolution` 是长期质量治理控制面，不是巨型检查清单。它负责建立系统认知、证明问题、控制修改、独立验收、管理发布和吸收运行反馈，让多轮 AI 开发不会持续积累平行能力、规则分裂和不可验证 Patch。

## 2. 渐进披露结构

```text
SKILL.md                 # 触发、模式路由、不可违反规则
workflows/               # 每种模式的执行协议
governance/              # 专项规则与门禁
templates/               # Finding/Decision/Batch/Report 等可复制产物
memory/                  # 目标项目初始化模板
scripts/                 # 低自由度、可测试的控制脚本
```

`SKILL.md` 只承担导航和核心契约；详细规则按当前任务加载，避免每次把全部治理知识塞入上下文。

## 3. 默认先 Autopilot，再按需分模式

无参数 `$software-evolution` 是完整 `autopilot`，而不是 `govern` 的别名。它不要求任何前置命令：控制面缺失时自动初始化，然后在同一运行中进入发现、修复、测试、验证和再扫描循环。

```text
$software-evolution
→ Auto-bootstrap when missing
→ Establish a stable parent Run scope and three-lane candidate portfolio
→ Model / Inspect / Prove / Prioritize across lanes
→ Repair / Test / Verify / Re-scan
→ Write a proportional recoverable checkpoint
→ Continue the globally highest-value safe fully verifiable batch
→ Prove cross-lane completion before a completed terminal state
```

`overnight` 是更长的无人值守 Profile，使用隔离优先和 `RUN-*` 账本，在宿主保持可用且存在安全可验证工作时持续执行；文件、Finding、Cycle、Batch 和耗时仅作遥测。

其余模式是高级控制面：

- `init` 只建立治理控制面。
- `audit`、`verify`、`release-check`、`observe` 严格只读。
- `govern`、`repair` 是用户定向的小批次写模式。
- `deep` 是分片式深度治理。
- `resume` 只恢复真实中断、漂移、歧义或指定 `RUN-*`/`BATCH-*`；普通批次 Checkpoint 由 Autopilot 自动继续。

模式先确定允许做什么，再确定如何做，避免把只读审计隐式升级为 Repair，也避免把默认自主治理错误拆成用户手工编排。

## 4. 双出口治理闭环

共享证据阶段：

```text
Orient → Model → Scope → Inspect → Prove → Prioritize → Decide
```

只读出口：

```text
Report / Verdict / Decision / Specialist Handoff
```

可写出口：

```text
Plan → Baseline → Repair → Verify → Re-scan → Remember → Checkpoint
```

公共流程不再无条件包含 Repair。“不要只输出报告”仅适用于已选择可写模式且证据、风险、业务权威、可逆性和验证均满足的情况。

### 4.1 覆盖控制与完成证明

连续 Run 维护稳定的父范围和三主线候选组合：用户/业务、工程/可靠性、架构/演进。当前文件夹、Schema、错误类型或测试模式只是发现簇；Batch 可以窄，但不能把父 Run 缩成当前问题族。每次继续同一问题族前都要与另外两条主线的最强候选比较，避免因为易搜索、易测试或易 Patch 而陷入局部最优。

对于可安全运行的用户界面，浏览器关键旅程是完成门禁，不是可选加分项。静态源码、组件测试或 HTTP 200 只能支持局部结论，不能宣布运行态 UX 已覆盖。

`safe work exhausted` 使用 schema-v3 `RUN-*` 证明：最后一次实质修复后重新覆盖三主线，搜索当前模块/分类/测试模式之外的反例，核对开放债务、近期变化、能力重复、业务规则分裂、关键旅程与健康失败，并运行 `validate_run_completion.py`。失败时必须继续或记录真实 `partial|blocked|interrupted`，不能完成 Run 或宿主持久 Goal。

## 5. 三个核心治理方向

### 5.1 用户体验与业务结果

运行条件允许时优先通过浏览器、API 或 Job 实测：

- 导航和入口是否可发现。
- 操作路径、表单、表格、弹窗是否符合任务。
- Loading、Empty、Error、Success、Permission、Retry、Recovery 是否完整。
- UI 成功是否对应真实业务状态。
- 权限提示是否有效且不泄露数据。

发现必须追到拥有该行为的组件、API、领域规则、数据副作用和反馈链路。静态证据只能支撑静态结论。

### 5.2 工程质量与可靠性

沿完整调用链检查：

```text
UI/API/Job/Event
→ Handler/Controller
→ Use Case/Service
→ Domain Rule
→ Repository/External Effect
→ Data/Event/User/Operator Feedback
```

重点包括职责、类型/状态、异常、事务、幂等、并发、超时、重试、缓存/消息一致性、SQL/锁、资源生命周期、配置和可观测性。

### 5.3 架构健康与持续演进

所有新增/修改通过演进门禁：

- 业务能力是否已经存在。
- 数据和规则的 Canonical Owner 是否明确。
- 是否创建平行 Service/Endpoint/DTO/Validator/Permission/Query/Event。
- 是否扩大条件分支和临时兼容路径。
- Flag、Adapter、Dual Write 是否有退出条件。
- 是否破坏依赖方向、部署边界或一致性模型。
- 是否应增加 Architecture Fitness Function 防止复发。

## 6. 语义级业务能力重复识别

Capability Signature：

```text
actor intent
+ business outcome/state effect
+ aggregate/data owner
+ inputs/outputs
+ invariants/authorization
+ state transition
+ side effects/events
+ entry points/callers
+ consistency/deployment constraints
```

算法：

1. 从领域术语、同义词、Route、UI Label、Command/Event、Table、Permission、DTO 字段构造搜索集合。
2. 从每个入口追踪到最终状态、数据和事件效果。
3. 归一化输入输出并比较边界值、权限、幂等、事务和失败行为。
4. 比较调用方、历史原因、数据/部署所有权。
5. 分类为 `canonical`、`adapter`、`specialization`、`duplicate`、`uncertain`。
6. Accidental Duplicate 使用一个 Canonical Finding/Debt/Decision 聚合，避免碎片化修补。

反误判规则：数据所有权、部署、授权、监管、一致性或失败隔离不同的实现可能是合理 Adapter/Boundary，不能为文本复用强行合并。

## 7. 架构防腐机制

### Capability Reuse Gate

新增业务能力前必须完成语义搜索和所有权决策。

### Business Consistency Gate

持续对比状态机、Enum、字段含义、阈值、计算、资格、权限、时间/金额和成功失败语义；权威不明确则创建 `DEC-*`。

### Architecture Fitness Functions

将重要边界转成可重复命令或检查：依赖方向、Cycle、数据写入边界、API/Event Schema、迁移兼容、关键规则单一 Owner、测试/性能/观测门禁。每个 Fitness Function 有原因、Scope、期望、Gate、Owner 和 Exception Expiry。

### Temporary Change Control

Feature Flag、Fallback、Adapter、兼容分支、Dual Write 必须记录原因、Owner、两条路径的测试/遥测、退出条件和 Target Version/Trigger。

### Re-scan

修复后重新检查调用方、能力地图、规则来源、边界和 Fitness Function，不能只看修改文件通过测试。

## 8. 控制面文件

目标项目中的：

- `architecture-memory.md`：事实、边界、历史、Fitness、发布和观测模型。
- `capability-map.md`：业务能力、别名、Owner、实现、调用方、规则和副作用。
- `technical-debt.md`：可验证债务生命周期。
- `health-baseline.json`：质量门禁、关键流程、SLI/SLO、已知失败和观测缺口。
- `decisions/DEC-*.md`：权威和选项。
- `batches/BATCH-*.md`：仅在风险、漂移恢复、兼容分阶段、仓库规则或复杂交接需要时保存独立批次元数据。
- `runs/RUN-*.md`：连续治理的权威账本，保存稳定父范围、三主线覆盖、运行态 UX、跨主线挑战、验证指纹、真实停止原因和恢复入口。
- `reports/`：Audit、Verification、Release、Observation 证据。

稳定 ID 让 Finding、Decision、Repair、Verification、Release、Autopilot 和 Resume 共享一个长期上下文。

## 9. 决策治理

Agent 不能猜时不只说“需要确认”，而是生成最小决策包：问题、已知权威、缺口、受影响能力/数据/调用方、2–3 个选项、兼容性、推荐、不决策后果、批准点和最终生效范围。

待决策期间可以继续只读证据和可逆准备，但不能实现依赖该语义的分支。

## 10. 专业能力路由

主 Skill 只负责识别、边界、优先级、集成和记忆；安全隐私、供应链、数据、性能成本、UX、数据库、CI/CD 交给可用专项 Skill 深入分析。路由继承父模式的读写权限，不能通过 Specialist 绕过只读或批准边界。

## 11. 发布治理

`release-check` 绑定 exact source/artifact identity，检查：

- Required CI、测试、构建和 unresolved P0/P1。
- API/Event/Schema/Client 兼容。
- Expand/Migrate/Contract、Backfill、锁和恢复。
- Old/New Mixed Version、Retry/Idempotency。
- Feature Flag、Canary、Stop Condition、Rollback/Roll-forward。
- 发布前、中、后的业务与技术 SLI。

它只输出 `READY`、`CONDITIONAL`、`BLOCKED`、`UNKNOWN`，绝不把检查行为等同部署授权。

## 12. 运行反馈闭环

`observe` 将用户结果映射到 SLI/SLO、日志、指标、Trace、告警、队列/缓存/数据库和支持反馈，重点发现：静默失败、Durable Completion 前记录成功、Retry 重复计数、Trace 断裂、长周期盲区和 Alert 与用户影响脱节。

Runtime Finding 必须记录环境、版本、窗口、过滤条件、样本/事件量、能力和替代解释。Correlation 不是 Root Cause。修复后定义观察窗口、目标、Guardrail 和 Rollback Threshold。

## 13. 睡后编程执行模型

`autopilot` 是默认零前置多批循环；`overnight` 在其上增加隔离优先和持久 `RUN-*` 连续性账本。每次调用本身只授权配置允许的可逆 R1/R2 源码、测试和治理文件修改，不授权生产、部署、远端发布或 R3/R4 受保护操作。

无人值守运行不等待宽泛决策：生成 `DEC-*`/Specialist Handoff，跳过被阻塞项并选择其他独立工作。每个语义批次完成验证和比例化 Checkpoint 后刷新三主线候选并立即选择下一项；文件数、Finding、Cycle、Batch 和耗时只作遥测。单一问题族耗尽不是完成。只有跨主线完成证明通过、全部剩余工作真实阻塞，或 Host 中断/挂起/限流/结束时才形成终态；普通 Checkpoint 不能完成宿主持久 Goal。

## 14. 连续执行、Checkpoint 与恢复

配置先通过 Validator 合并为 `effective_config`。当前控制面只保留真正影响权限和证据完整性的配置；旧 `budget`、`deep_budget`、`overnight_budget` 与旧 `autopilot.max_*` 配额为兼容输入，会被列入 `deprecated_paths` 并从 `effective_config` 剥离。

批次边界是语义边界：一个根因、业务能力、不变量、契约边界或兼容阶段。文件数、Diff 大小、Finding 数、Cycle、Batch 数和耗时只作 Blast Radius、覆盖、趋势和恢复遥测，不得制造硬停止、重置权限或要求用户重复发命令。大范围修改通过更强的调用方分析、回滚和验证来控制，而不是通过任意文件上限控制。

`RUN-*` 是权威连续账本，小型 R1 可以只增加 Run 行并复用 Finding/Debt/Verification 证据；只有风险、漂移恢复、兼容分阶段、仓库规则或复杂交接需要时才创建独立 `BATCH-*`。Checkpoint 记录 branch、HEAD、worktree fingerprint/entries、scope paths、模式、风险、变更遥测、invocation owner/heartbeat、最后门禁、决定/批准和下一步。默认启动可在 Drift、权威和最后门禁校验后自动接管唯一、非活跃且安全可恢复的宿主中断或旧配额型 `partial`；另一个活跃 owner 的重叠 branch/scope 禁止接管和并发新建。显式 `resume` 分类：

- `NO_DRIFT`
- `SAFE_DRIFT`
- `MATERIAL_DRIFT`
- `CONFLICTING_DRIFT`
- `UNKNOWN`

只有 No Drift 和经确认的 Safe Drift 能直接继续。真实停止条件必须准确落入完成、阻塞或中断语义：`completed` 要求三主线与运行态 UX 覆盖、簇外反例挑战、开放工作核对和 Run Validator 全部通过；否则真实停止状态是 `partial`、`blocked` 或 `interrupted`。宿主中断、挂起、限流或结束是中断，不得伪装成完成。

## 15. 自动修改安全与验收完整性

写入必须同时满足 Mode、Risk、Authority、Reversibility、Verification 五个 Gate。R3 使用兼容性分阶段方案，R4 在操作点显式批准。

`verify` 从 Artifact 和权威验收标准重新建模，不接受实现者的自证。失败时保持只读并输出 Repair Handoff。昂贵验证仅能在命令、环境、Revision、输入、依赖和受影响路径指纹一致时复用。

同一修复假设连续失败三次后隔离该假设并重新建模，不能盲目第四次修改；若仍有其他独立安全工作，治理循环继续。修改未达到风险所需测试、运行或观察证据时只能标记 `partial`、`failed` 或 `blocked`。
