# 使用指南

## 安装

在仓库根目录执行：

```bash
python3 install.py
```

安装器会把 `software-evolution/` 安装为用户级 Codex Skill。默认使用软链接，因此拉取仓库更新后无需重复复制 Skill。

常用参数：

```bash
# 只查看安装计划
python3 install.py --dry-run

# 复制安装而不是软链接
python3 install.py --copy

# 指定安装目录
python3 install.py --target ~/.agents/skills/software-evolution
```

安装器不会覆盖已有的不同安装。如目标目录已经存在，应先人工确认其内容，再决定迁移或删除。

## 触发方式

```text
$software-evolution init
$software-evolution
$software-evolution deep
$software-evolution repair
$software-evolution repair DEBT-001
```

也可以在 Codex 中使用 `/skills` 选择 **AI Software Evolution Agent**。

## 初始化模式

```text
$software-evolution init
```

初始化模式负责：

- 读取仓库规则、产品文档、代码入口和测试说明。
- 建立系统运行单元、模块、领域、数据和外部集成模型。
- 识别关键用户、核心流程和业务能力。
- 建立测试、构建和运行基线。
- 创建长期工程记忆。

默认输出：

```text
docs/software-evolution/
├── architecture-memory.md
├── capability-map.md
└── technical-debt.md
```

已有记忆文件不会被初始化脚本覆盖。

## 默认治理模式

```text
$software-evolution
```

默认优先检查：

1. 用户明确指定的范围。
2. 当前未提交改动。
3. 当前分支相对基线的近期变化。
4. 技术债中优先级最高且具备验证条件的问题。

Agent 会自主处理能够明确证明、影响范围有限且可以验证的低风险问题。

## 深度治理模式

```text
$software-evolution deep
```

深度治理会先建立覆盖清单，再分阶段检查：

- 用户界面、菜单、表单、表格、弹窗及关键业务流程。
- 前端、后端、数据库和异步任务。
- 事务、幂等、并发、超时、重试、缓存、消息和资源生命周期。
- 模块边界、依赖方向、循环依赖和职责分配。
- 重复业务能力、业务规则分裂和技术债。

深度模式不会在一个修改批次中无边界重写整个系统。未能安全完成的问题会进入技术债队列，并记录下一步和验证要求。

## 修复模式

```text
$software-evolution repair DEBT-001
```

可以提供：

- Technical Debt ID
- Finding ID
- Capability ID
- 文件、模块、功能或业务流程范围

修复流程包括复现、调用链追踪、风险判断、最小根因修改、回归测试、分层验证和记忆更新。

## 浏览器治理

当项目可以在本地或测试环境运行并且存在浏览器能力时，Agent 应：

- 使用测试账号登录，不绕过认证。
- 从菜单开始遍历关键流程，而不是只访问深链接。
- 检查加载、空数据、错误、成功反馈和权限不足状态。
- 检查 Console 和失败的网络请求。
- 修复后重新执行同一业务流程。

不能运行项目时，Agent 会明确标记 UX 结论只来自静态证据。

## 验证结果含义

- `passed`：检查已执行并满足验收标准。
- `failed`：检查已执行但未通过。
- `blocked`：环境、依赖、权限或业务决策缺失。
- `not run`：有意识地未执行，并记录原因。

只有风险等级要求的验证全部通过，问题才可以标记为 `verified`。
