# AI Software Evolution Agent

[![Validate Skill](https://github.com/myh1090052425/codex-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/myh1090052425/codex-skills/actions/workflows/validate.yml)

一个长期可复用的 Codex Skill。它把 Codex 定位为软件系统的长期技术负责人，而不是代码生成器、普通 Code Review 或报告型扫描工具。

它持续治理：

- 用户体验与业务流程质量
- 前端、后端、数据库与系统可靠性
- 架构边界、业务能力复用与业务规则一致性
- 测试、发布、迁移、回滚与运行反馈
- 技术债、决策记录、工程记忆与中断恢复

核心原则是：**先证明，再决策；只读与可写分离；修改必须验证；运行结果反哺架构。**

## 快速安装

```bash
git clone https://github.com/myh1090052425/codex-skills.git
cd codex-skills
python3 install.py
```

默认创建用户级软链接，因此仓库更新会直接反映到 Codex。Codex 通常会自动检测 Skill 变更；如果当前界面没有出现更新，再重启 Codex。安装计划预览、复制安装和自定义目录：

```bash
python3 install.py --dry-run
python3 install.py --copy
python3 install.py --target ~/.agents/skills/software-evolution
```

安装器不会覆盖已有的不同目录或软链接。

## 一个命令直接启动

在任何目标项目中打开 Codex，直接输入：

```text
$software-evolution
```

这就是默认 `autopilot`。**不需要先执行 `init`、`audit` 或 `govern`。** Agent 会在同一次运行中自动：

```text
检测/初始化治理控制面
→ 建立系统与业务认知
→ 发现并证明问题
→ 判断优先级
→ 选择语义完整的安全修复批次
→ 修改代码
→ 补充测试
→ 自动验证
→ 重扫调用方、能力、规则与架构
→ 写入可恢复 Checkpoint
→ 只要仍有安全、可完整验证的工作，就在同一次调用中继续
→ 仅在真实停止条件或宿主中断时保存终态
```

需要更长的无人值守“睡后编程”窗口时：

```text
$software-evolution overnight
$software-evolution overnight services/order
```

如果宿主把 Slash Command 作为文本传递，也可以写 `/software-evolution ...`。还可以在 `/skills` 中选择 **AI Software Evolution Agent**。

高级控制入口仍然保留：

```text
$software-evolution autopilot [scope]
$software-evolution overnight [scope]
$software-evolution init
$software-evolution audit [scope]
$software-evolution govern [scope]
$software-evolution repair [FIND/DEBT/DEC/scope]
$software-evolution verify [branch/commit/PR/RUN/BATCH/id]
$software-evolution deep [scope]
$software-evolution release-check [branch/commit/release]
$software-evolution observe [flow/service]
$software-evolution resume [RUN/BATCH/id]
```

## 十一种模式

| 模式 | 目标 | 默认写入行为 |
|---|---|---|
| `autopilot`（无参数默认） | 自动初始化/安全接管未完 Run，并持续治理到没有安全可验证工作 | 连续执行语义完整的 R1/R2 修复批次 |
| `overnight` | 在宿主可用期间执行长时间无人值守治理 | 连续 R1/R2 修复；数量只作遥测 |
| `init` | 只建立控制面、系统模型、能力地图和基线 | 仅创建/更新治理文件，不改产品 |
| `audit` | 只读证明问题、分级、形成修复/决策输入 | 不修改；`--record` 才持久化报告 |
| `govern` | 手工选择范围的日常治理 | 小批次 R1/R2 自动修复 |
| `repair` | 定向修复已证明问题 | 目标化修改、补测试、验证 |
| `verify` | 独立验收改动、PR、分支或债务关闭 | 不修改；失败交回 repair |
| `deep` | 分片式深度治理与能力收敛 | 在声明范围内连续执行可完整验证的修复波次 |
| `release-check` | 发布、迁移、混合版本、回滚就绪检查 | 严格只读，不部署 |
| `observe` | 用日志、指标、Trace、告警和反馈校正治理 | 生产只读，不改告警/配置/数据 |
| `resume` | 恢复真实中断、漂移、歧义或指定 `RUN-*`/`BATCH-*` | 继承原模式；无法证明时降级只读 |

`init`、`audit`、`govern`、`repair` 是高级控制面，不是默认命令的前置步骤。普通批次 Checkpoint 会自动继续，不需要 `resume`；只读模式不会因为发现“明显问题”而偷偷修改代码。

## 治理闭环

所有模式共享只读证据阶段：

```text
Orient → Model → Scope → Inspect → Prove → Prioritize → Decide
```

之后分流：

```text
只读模式 → Report / Verdict / Decision
可写模式 → Plan → Baseline → Repair → Verify → Re-scan → Remember → Checkpoint
```

可写模式会在风险、业务权威、可逆性和验证条件满足时自主完成修复。一个批次按根因、业务能力、不变量、契约边界或兼容阶段划分，而不是按文件数量划分；文件数、Finding 数、批次数和耗时只作遥测。每批验证并写入 Checkpoint 后，只要还有独立的安全可验证工作就继续。不具备完整证据时形成 Finding、Decision、Specialist Handoff 或 Blocked Checkpoint，并继续其他独立安全工作。

## 睡后编程与无人值守边界

`overnight` 使用独立 `RUN-*` 账本并优先在隔离 worktree 中运行，在宿主任务仍可用且存在安全可验证工作时持续推进。它不会因为文件数、Cycle、Finding 或 Batch 数达到阈值停工；遇到业务决策、凭证、环境或高风险问题时记录并跳过，继续其他独立安全任务，不会一直等用户回复。

无人值守授权不包括部署、生产迁移/数据修复、Flag/告警/权限/凭证、远端发布、Force Push、历史重写或 R3/R4 契约变更。实际使用本地 Scheduled Tasks 时，电脑需要保持开机且 Codex/ChatGPT 桌面应用保持运行。

## 项目控制面

首次执行默认 `autopilot`/`overnight`（或显式 `init`）会非覆盖式创建：

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
└── reports/
    ├── audit/
    ├── verification/
    ├── release/
    └── observation/
```

稳定 ID：`CAP-*`、`FIND-*`、`DEBT-*`、`DEC-*`、`BATCH-*`、`RUN-*`、`VER-*`、`REL-*`、`FIT-*`。

`.software-evolution.yml` 控制最大风险等级、是否允许产品代码写入、连续执行与逐批 Checkpoint、只读报告持久化、发布门禁、观察窗口、专业路由和架构适应度检查。所有执行都使用 Validator 输出的 `effective_config`。

连续自治采用语义批次和可恢复 Checkpoint：

- 一个批次由一个根因、业务能力、不变量、契约边界或兼容阶段定义；一个合理修复可以影响一个或数百个文件。
- 文件数、Diff 大小、Finding 数、Cycle、Batch 数和耗时只作 Blast Radius、审计、趋势和恢复遥测，绝不是授权或停止条件。
- 每个批次都必须完成风险所需验证并记录 `BATCH-*`；普通 Checkpoint 后自动选择下一项工作。
- 旧 `budget`、`deep_budget`、`overnight_budget` 和旧 `autopilot.max_*` 配额键仍可被 Validator 解析，便于老项目升级，但会从 `effective_config` 中剥离并列入 `deprecated_paths`，Agent 必须忽略。
- 另一个仍活跃的 invocation owner 是并发边界；默认命令不会接管它，也不会创建范围重叠的新 Run。
- 下一次普通 `$software-evolution` 可在 Drift、权威和最后门禁校验后自动接管唯一、明确的宿主中断或旧配额型 `partial`；显式 `resume` 只用于无法自动接管的中断、漂移、歧义或指定恢复。

真实停止条件只有：重扫后没有可修复问题；剩余工作全部缺业务权威、审批、证据、环境或专项能力；需要受保护外部操作或 R3/R4 决策；并行漂移使候选工作不安全；同一假设失败三次后该假设被隔离且没有其他安全工作；或宿主中断、挂起、限流、结束任务。

## 三个核心治理方向

### 1. 用户与业务结果

运行条件允许时优先使用浏览器/API/任务流验证入口可发现性、操作路径、表单/表格/弹窗、加载/空数据/错误/成功/权限状态，以及最终业务状态。静态代码不能替代可运行的 UX 证据。

### 2. 工程可靠性

沿入口、编排、领域规则、持久化/外部副作用、用户/运维反馈的完整链路检查职责、事务、幂等、并发、超时、重试、缓存/消息一致性、SQL、资源释放、异常和可观测性。

### 3. 架构与持续演进

每次新增能力前都要搜索现有 Capability；每次修复后都要检查边界、依赖方向、重复能力、规则分裂、临时分支、Feature Flag 退出条件和 Architecture Fitness Function，防止 Patch 永久化。

## 如何识别“不同代码实现同一业务能力”

Skill 不依赖文本重复，而比较：

```text
actor intent + business outcome/state effect + data owner
+ inputs/outputs + invariants/authorization + state transition
+ side effects/events + callers + consistency/deployment constraints
```

候选被分类为：

- `canonical`：权威实现
- `adapter`：协议/入口适配
- `specialization`：明确附加约束
- `duplicate`：相同效果和规则的平行实现
- `uncertain`：业务权威或证据不足

只有语义、规则和数据效果相同才收敛；不同数据所有权、部署、授权、一致性或监管边界不会为了“复用”被强行合并。

## 专业治理路由

主 Skill 负责识别风险、保留系统上下文、设置优先级和整合结果；安全隐私、供应链、数据治理、性能成本、UX、数据库、CI/CD 等深度问题会路由到可用专项 Skill。没有专项能力时生成结构化 handoff，不把主 Skill 膨胀成无边界巨型 Prompt。

## 自动修改安全

风险分为 R0–R4：

- R0：只读证据。
- R1：局部 Bug、缺失测试、明确低风险修复，可在可写模式自主完成。
- R2：共享模块、内部契约、事务/重试/性能调整，仅在影响、回滚和验证均明确时执行。
- R3：数据模型、权限、核心业务语义、公共 API/Event，先形成决策与分阶段兼容方案。
- R4：生产、部署/回滚、不可逆数据、凭证权限、Git 历史重写，必须在操作时获得明确批准。

每个修改批次都要求基线、回归测试、分层验证、最终 Diff/调用方检查、架构复扫和可恢复 Checkpoint。同一修复假设连续失败三次后停止，不进行第四次盲改。

## 仓库结构

```text
codex-skills/
├── README.md
├── install.py
├── software-evolution/      # 可独立安装的完整 Skill
│   ├── SKILL.md
│   ├── agents/
│   ├── workflows/
│   ├── governance/
│   ├── templates/
│   ├── memory/
│   └── scripts/
├── docs/
│   ├── USAGE.md
│   ├── DESIGN.md
│   ├── DEVELOPMENT.md
│   └── state/               # 仓库开发恢复状态，提交到 Git
├── tests/
└── .github/workflows/validate.yml
```

`docs/state/` 是本仓库自身的跨会话开发状态；目标项目里的 `docs/software-evolution/` 是被治理项目的长期工程记忆，两者职责不同。

## 文档与验证

- [安装与使用](docs/USAGE.md)
- [治理模型与安全设计](docs/DESIGN.md)
- [开发、测试与发布](docs/DEVELOPMENT.md)

本地验证：

```bash
python3 -m py_compile install.py software-evolution/scripts/*.py
python3 software-evolution/scripts/check_skill_integrity.py
python3 software-evolution/scripts/validate_project_config.py \
  --config software-evolution/memory/software-evolution.config.template.yml --json
python3 -m unittest discover -s tests -v
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py software-evolution
```
