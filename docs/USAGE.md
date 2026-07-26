# 使用指南

## 1. 安装与更新

```bash
git clone https://github.com/myh1090052425/codex-skills.git
cd codex-skills
python3 install.py
```

默认安装为用户级软链接。拉取仓库更新后 Codex 通常会自动检测新版本；如果 Skill 列表或当前界面没有刷新，再重启 Codex。

```bash
python3 install.py --dry-run   # 仅查看
python3 install.py --copy      # 复制安装
python3 install.py --target ~/.agents/skills/software-evolution
```

安装器不会覆盖不同的既有安装。

## 2. 第一次及以后使用

在目标项目根目录打开 Codex，第一次和以后都只需要：

```text
$software-evolution
```

默认进入 `autopilot`。控制面不存在时，Agent 会自动非覆盖式创建并在同一次运行中继续建立认知、审计、修复、补测试、验证和再扫描；**不会要求用户再执行 `init → audit → govern`。**

```text
.software-evolution.yml
docs/software-evolution/
├── architecture-memory.md
├── capability-map.md
├── technical-debt.md
├── health-baseline.json
├── decisions/
├── batches/
├── runs/
└── reports/{audit,verification,release,observation}/
```

需要睡后编程时执行：

```text
$software-evolution overnight
```

它使用有限的时间、循环、批次、文件和验证预算持续执行，遇到需要决定或批准的项目会记录并跳过，继续其他安全工作。也可以在 `/skills` 中选择 **AI Software Evolution Agent**。`/software-evolution ...` 在宿主作为普通文本传递时与 `$software-evolution ...` 等价。

## 3. 模式选择

### `autopilot [scope]`：默认单命令持续治理

```text
$software-evolution
$software-evolution autopilot
$software-evolution autopilot src/orders
```

零前置启动：缺少控制面时自动初始化，然后循环执行建模、发现、证明、优先级、修复、测试、验证、复扫和记忆更新。完成一批后继续下一批，直到安全工作耗尽、预算不足、全部剩余项被阻塞或运行被中断。

### `overnight [scope]`：睡后编程

```text
$software-evolution overnight
$software-evolution overnight services/payment
```

使用 `overnight_budget`、隔离 worktree 优先策略、`RUN-*` 账本和最终验证预留执行长时间无人值守治理。不会等待常规确认；需要业务权威、生产操作、远端发布或 R3/R4 变更时记录并跳过。

本地 Scheduled Task 运行期间需要电脑保持开机且 Codex/ChatGPT 桌面应用保持运行。建议先人工观察前几次运行，再逐步放大预算。

### `init`：建立系统认知

```text
$software-evolution init
```

适合新项目或工程记忆缺失时。输出架构、领域、关键流程、能力、验证、发布与可观测性基线；未知项明确标记，不猜业务规则。

### `audit [scope]`：严格只读审计

```text
$software-evolution audit
$software-evolution audit src/billing
$software-evolution audit checkout-flow --record
```

用于先确认原因、影响和优先级。默认不修改代码、测试、配置、工程记忆、Git 或外部系统。`--record` 只允许把报告写入 `reports/audit/`，不会升级为修复模式。

审计 Verdict：

- `CLEAR_WITHIN_SCOPE`
- `FINDINGS_CONFIRMED`
- `DECISION_REQUIRED`
- `SPECIALIST_REQUIRED`
- `INSUFFICIENT_EVIDENCE`

### `govern [scope]`：手工范围治理

```text
$software-evolution govern
$software-evolution govern src/orders
```

优先治理用户范围、当前改动、分支 Diff、Ready 技术债和关键流程。可以完成 R1 和边界明确的 R2 小批次修复；每批必须补测试、验证、复扫并建立 `BATCH-*` Checkpoint。

### `repair [id/scope]`：定向修复

```text
$software-evolution repair FIND-014
$software-evolution repair DEBT-007
$software-evolution repair DEC-003
```

只修复已证明、已决策或 Ready 的问题。流程包括复现、调用链、风险/预算、最小根因修改、回归测试、分层验证、能力/架构复扫和记忆更新。

### `verify [target/id]`：独立验收

```text
$software-evolution verify HEAD
$software-evolution verify main..feature/order-timeout
$software-evolution verify BATCH-021
```

独立从业务规则、契约、调用方和验收标准重建预期，不把实现者报告当作证据。失败时输出 repair handoff，但不自行修改。

Verdict：`VERIFIED`、`PARTIAL`、`FAILED`、`BLOCKED`、`UNKNOWN`。

### `deep [scope]`：预算化深度治理

```text
$software-evolution deep
$software-evolution deep services/payment
```

先声明覆盖清单和预算，再分片检查 UX、工程可靠性、业务能力/规则、架构、数据库、发布、观测和技术债。预算至少包括：范围项、Finding 数、修复批次、变更文件数和验证预留。输出应说“当前切片完成”，除非真的覆盖了全部声明范围。

### `release-check [target]`：发布门禁

```text
$software-evolution release-check HEAD
$software-evolution release-check release/2026.07
```

检查目标身份、Artifact 来源、CI、契约、迁移顺序、混合版本、Feature Flag、灰度、停止条件、回滚和发布后观察。严格只读，不部署、不回滚、不执行迁移。

Verdict：`READY`、`CONDITIONAL`、`BLOCKED`、`UNKNOWN`。

### `observe [flow/service]`：运行反馈

```text
$software-evolution observe checkout
$software-evolution observe order-worker --record
```

将关键流程映射到 SLI/SLO、日志、指标、Trace、告警、队列/数据库和用户反馈，识别静默失败、误报成功和告警盲区。生产默认只读；不会修改告警、Dashboard、Flag、配置或数据。

### `resume [RUN/BATCH/id]`：恢复中断运行或批次

```text
$software-evolution resume RUN-20260726-01
$software-evolution resume BATCH-021
```

读取 Checkpoint，比较 branch、HEAD、worktree fingerprint 和 scope paths：

- `NO_DRIFT`：重验最后门禁后继续。
- `SAFE_DRIFT`：仅有范围外未跟踪文件，人工确认后继续。
- `MATERIAL_DRIFT`：只读重建证据，不直接编辑。
- `CONFLICTING_DRIFT`：停止旧路径并解决冲突或新建批次。
- `UNKNOWN`：无法证明原上下文，降级只读。

## 4. Scope、运行账本和稳定 ID

Scope 可以是：文件、目录、模块、页面、业务流程、Capability、Finding、Debt、Decision、Batch、分支、Commit、PR、Release 或服务。

稳定 ID：

- `CAP-*` 业务能力
- `FIND-*` 发现
- `DEBT-*` 技术债
- `DEC-*` 决策
- `BATCH-*` 批次检查点
- `VER-*` 验收
- `REL-*` 发布检查
- `FIT-*` 架构适应度检查

使用 ID 能避免跨会话重新解释问题。

## 5. 项目配置

`autopilot` 控制默认循环次数、连续失败上限和每批强制 Checkpoint；`overnight_budget` 额外控制最长运行分钟、循环、批次、文件和最终验证预留。

`.software-evolution.yml` 使用受限 YAML（仅 Mapping + Scalar），可控制：

```yaml
version: 1
memory_dir: docs/software-evolution

autonomy:
  max_risk: R2
  allow_product_writes: true

budget:
  max_scope_items: 60
  max_findings: 12
  max_repair_batches: 2
  max_files_changed: 12
  reserve_verification_minutes: 15
```

完整模板位于 `software-evolution/memory/software-evolution.config.template.yml`。验证：

```bash
python3 <skill-root>/scripts/validate_project_config.py \
  --config .software-evolution.yml
```

配置拒绝重复键、未知键、非标准布尔值、敏感键和复杂 YAML 特性。`readonly.allow_record_persistence` 只能允许显式 `--record` 写治理报告/决策包，不能自动写入。`observe.production_read_only` 必须为 `true`。即使 `max_risk: R4`，R4 操作仍必须获得显式批准。

## 6. 业务能力复用门禁

任何新增 Service、Endpoint、Component、DTO、Validator、权限规则、Query、Event 或 Utility 前，Agent 必须：

1. 从 Capability Map 和代码搜索业务术语、同义词、UI 标签、Route、Event、Table、Permission 和 Side Effect。
2. 沿调用链比较最终业务结果、数据所有权、规则、状态变化、权限和副作用。
3. 分类 `canonical`、`adapter`、`specialization`、`duplicate`、`uncertain`。
4. 选择复用、扩展、适配或新建，并记录原因。

不能因为代码长得像就强行抽象，也不能因为命名不同就忽略语义重复。

## 7. 决策与专业路由

业务语义、权限、数据、公共契约或迁移存在权威缺口时，Agent 创建 `DEC-*`，给出选项、兼容性、推荐和“不决策”的后果。

安全/隐私、供应链、数据、性能成本、UX、数据库、CI/CD 触发专项治理时，主 Skill 会加载可用专项 Skill；没有能力时生成 Specialist Handoff，而不是假装完成深度结论。

## 8. 浏览器、测试和运行环境

- 浏览器治理优先使用本地/测试环境和批准的测试账号，不绕过认证。
- Read-only 模式不会运行已知会更新 Snapshot、共享数据库、Lockfile 或 tracked generated source 的命令。
- 所有检查记录 `passed`、`failed`、`blocked`、`not run`。
- 修改后必须检查最终 Diff、调用方、契约、架构适应度和运行/发布影响。
- 需要真实流量窗口才能验证的问题保持 `partial`，直到观察阈值满足。

## 9. 生产与外部操作

以下操作始终在实际执行点要求明确批准：部署、回滚、生产迁移/回填/数据修复、Feature Flag 修改、告警或采样修改、权限/凭证、远端删除、Force Push/历史重写。

源码层的自主修复授权不会自动扩展到这些操作。
