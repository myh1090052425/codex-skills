# Project State

- 更新时间：2026-07-26
- 仓库：`myh1090052425/codex-skills`
- 默认分支：`main`

## 项目总览

本仓库维护 `AI Software Evolution Agent`。完整 Skill 位于 `software-evolution/`；仓库同时提供安装器、使用与设计文档、自动测试和 GitHub Actions 校验。

## 活跃线程索引

- [Software Evolution Skill 创建与发布](2026-07-26-software-evolution-skill-local.md) — Skill 和 GitHub 仓库结构已完成，正在发布到远端。

## 候选下一步

1. 完成 `main` 分支首次推送并检查远端文件结构。
2. 确认 GitHub Actions 校验结果。
3. 在真实项目中运行 `$software-evolution init` 做首轮前向验证。

## 阻塞

- 当前无阻塞；远端为空仓库，当前用户具有管理员权限。

## 最近提交

- `440d3c5 feat: 创建 AI Software Evolution Agent Skill`

## 关键决策

- GitHub 仓库使用顶层 `software-evolution/` 作为可见、可独立安装的 Skill 目录。
- 用户级 Codex 安装只保留指向仓库源码的软链接，不把本机安装目录提交到 GitHub。
- 仓库提交 `docs/state/`，用于 Codex 跨会话恢复；其中不得记录凭证、私密配置或不可移植的本机绝对路径。
- 项目工程记忆默认写入目标项目的 `docs/software-evolution/`，与本仓库的 `docs/state/` 分工不同。
