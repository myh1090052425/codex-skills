# Project State

- 更新时间：2026-07-26
- 仓库：`myh1090052425/codex-skills`
- 默认分支：`main`

## 项目总览

本仓库维护 `AI Software Evolution Agent`。完整 Skill 位于 `software-evolution/`；仓库同时提供安装器、使用与设计文档、自动测试和 GitHub Actions 校验。

## 活跃线程索引

- 当前无活跃线程。

## 已完成/归档

- [Software Evolution 单命令 Autopilot 与睡后编程](2026-07-26-software-evolution-autopilot-v1.md) — 2026-07-26 完成；零前置 Autopilot、Overnight 睡后编程、RUN/BATCH 恢复、八角度 Review、25 项测试和 GitHub Actions 已完成。
- [Software Evolution 控制面与治理闭环升级](2026-07-26-software-evolution-control-plane-v1.md) — 2026-07-26 完成；九种模式、只读/可写双出口、发布与运行治理、恢复预算、七角度 Review、19 项测试和 GitHub Actions 已完成。
- [Software Evolution Skill 创建与发布](2026-07-26-software-evolution-skill-local.md) — 2026-07-26 完成；Skill、仓库文档、测试、状态文件和 CI 已发布到 GitHub。

## 候选下一步

1. 在真实项目中前向验证 `$software-evolution`、`overnight`、`verify RUN-*` 和 `resume RUN-*`。
2. 根据真实项目反馈迭代治理规则、风险阈值、预算默认值和专项 Skill 路由。
3. 为被频繁触发的安全、数据库、UX、性能/成本领域逐步建设独立专项 Skill。

## 阻塞

- 当前无阻塞。

## 最近提交

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
