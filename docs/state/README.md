# Project State

- 更新时间：2026-07-27
- 仓库：`myh1090052425/codex-skills`
- 默认分支：`main`

## 项目总览

本仓库维护 `AI Software Evolution Agent`。完整 Skill 位于 `software-evolution/`；仓库同时提供安装器、使用与设计文档、自动测试和 GitHub Actions 校验。

## 活跃线程索引

- [Software Evolution 真实运行行为纠偏](2026-07-27-software-evolution-real-run-correctness-v1.md) — 本地实现与 50 项测试通过，待推送和 GitHub Actions；新增三主线覆盖、浏览器门禁、schema-v3 完成证明和比例化控制面。

## 已完成/归档

- [Software Evolution 去除人为数量配额](2026-07-26-software-evolution-remove-artificial-quotas-v1.md) — 2026-07-26 完成；人工文件/Finding/Cycle/Batch/Window 配额已退出有效控制面，连续自治、旧配置兼容、35 项测试、多角度 Review 与 GitHub Actions 已通过。
- [Software Evolution 连续预算与自动续跑修复](2026-07-26-software-evolution-continuous-budget-v1.md) — 2026-07-26 完成；该版本的双层数量预算后来被确认违背持续自治目标，已由“去除人为数量配额”线程废弃并迁移。
- [Software Evolution 单命令 Autopilot 与睡后编程](2026-07-26-software-evolution-autopilot-v1.md) — 2026-07-26 完成；零前置 Autopilot、Overnight 睡后编程、RUN/BATCH 恢复、八角度 Review、25 项测试和 GitHub Actions 已完成。
- [Software Evolution 控制面与治理闭环升级](2026-07-26-software-evolution-control-plane-v1.md) — 2026-07-26 完成；九种模式、只读/可写双出口、发布与运行治理、恢复预算、七角度 Review、19 项测试和 GitHub Actions 已完成。
- [Software Evolution Skill 创建与发布](2026-07-26-software-evolution-skill-local.md) — 2026-07-26 完成；Skill、仓库文档、测试、状态文件和 CI 已发布到 GitHub。

## 候选下一步

1. 推送本线程改动并确认 GitHub Actions `Validate Skill` 成功。
2. 继续在真实项目中验证 `$software-evolution overnight`、`verify RUN-*` 和真实中断后的 `resume RUN-*`。
3. 根据长期运行数据迭代治理规则、风险阈值、Checkpoint/恢复策略和专项 Skill 路由。
4. 为被频繁触发的安全、数据库、UX、性能/成本领域逐步建设独立专项 Skill。

## 阻塞

- 当前无阻塞。

## 最近提交

- `10c74ec fix: 移除 Autopilot 人为数量配额`
- `6c96a79 fix: 修复 Autopilot 预算记账与自动续跑`
- `d793893 feat: 实现单命令 Autopilot 与睡后编程`
- `f53a34c docs: 记录软件演进控制面发布结果`
- `462fce0 feat: 升级软件演进 Agent 控制面`
- `e9dfc3e docs: 更新 GitHub 发布状态`

## 关键决策

- GitHub 仓库使用顶层 `software-evolution/` 作为可见、可独立安装的 Skill 目录。
- 用户级 Codex 安装只保留指向仓库源码的软链接，不把本机安装目录提交到 GitHub。
- 仓库提交 `docs/state/`，用于 Codex 跨会话恢复；其中不得记录凭证、私密配置或不可移植的本机绝对路径。
- 项目工程记忆默认写入目标项目的 `docs/software-evolution/`，与本仓库的 `docs/state/` 分工不同。
- GitHub Actions 的 `Validate Skill` 必须通过后才可宣称仓库发布有效。
- Autopilot 的活跃 invocation owner 是并发边界；新 Run 元数据必须记录可机读 deadline/heartbeat，禁止接管或创建范围重叠的新 Run。
- 文件、Finding、Cycle、Batch 和耗时只作遥测；自治是否继续由风险、业务权威、可逆性、验证、并行漂移和 Host 生命周期决定。
