# 开发、测试与发布

## 1. 修改原则

- `software-evolution/SKILL.md` 只保留触发、模式路由、核心契约和渐进披露链接，正文不得超过 500 行。
- 执行流程放 `workflows/`，领域门禁放 `governance/`，可复制产物放 `templates/`/`memory/`。
- 易错、需一致执行的逻辑使用 `scripts/`，优先 Python 标准库并提供测试。
- 不在 Skill 目录内新增 README、Changelog 或重复安装文档；仓库级说明放根目录和 `docs/`。
- 新模式必须先定义 Write Policy，再定义目标、Procedure、Prohibited Behavior 和 Verdict/Completion。
- 配置只能缩小自治范围，不能降低 R4、生产只读、验证或仓库规则。
- 不进行无关格式化、依赖升级或重构。

## 2. 当前结构契约

Skill 必须包含十一种 Workflow：

```text
autopilot overnight init audit govern repair verify deep release-check observe resume
```

无参数入口必须映射 `autopilot`，自动初始化缺失控制面、安全接管唯一可恢复 partial，并在每个语义批次 Checkpoint 后同调用续跑。无参数父 Run 保持仓库级范围，维护用户/业务、工程/可靠性、架构/演进三主线候选；CI 应阻止再次映射为 `govern`、要求手工前置模式、把单一问题族耗尽当完成，或把文件/Finding/Cycle/Batch 数量当终止点。

Write Policy：

```text
CONTROL_PLANE_ONLY
READ_ONLY
BOUNDED_WRITE
CONTINUOUS_WRITE
INHERITED_OR_READ_ONLY
```

`check_skill_integrity.py` 会校验必需文件、Frontmatter、链接、模式 Marker、Agent Metadata、模板、配置、JSON 和可移植性。

## 3. 脚本职责

### `bootstrap_project_memory.py`

- 非覆盖式创建 `.software-evolution.yml`、四个基础 Memory 文件和报告/决策/批次/运行账本目录。
- 使用独占创建避免并发覆盖。
- `--dry-run` 不得产生文件或目录。

### `validate_project_config.py`

- 只支持两空格 Mapping + Scalar 的受限 YAML。
- 拒绝重复/未知键、Tab、复杂 YAML、非小写 Boolean 和敏感键。
- `observe.production_read_only` 必须为 `true`。
- 输出原始 `config`、确定性合并后的 `effective_config`、`defaulted_paths` 和 `deprecated_paths`；旧数量/时间配额仅兼容解析并从有效行为中剥离。

### `check_checkpoint_drift.py`

- `--snapshot` 生成 Batch Metadata。
- 比较 Branch、HEAD、Worktree Fingerprint/Entries 和 Scope Paths。
- 输出 `NO_DRIFT`、`SAFE_DRIFT`、`MATERIAL_DRIFT`、`CONFLICTING_DRIFT` 或 `UNKNOWN`。

### `validate_run_completion.py`

- 校验 schema-v3 `RUN-*` 的父范围、三主线覆盖、运行态 UX、跨主线挑战、开放修复状态和真实终止原因。
- `completed` 只允许 `safe_work_exhausted`，且必须证明无开放 repair-ready 工作；覆盖矩阵、聚合验证、完成挑战和终止区不能保留 `TBD` 占位证据。
- 运行中和真实 `partial|blocked|failed|interrupted` 可以保留未完成覆盖，但必须记录真实 terminal reason。

## 4. 本地验证

```bash
python3 -m py_compile \
  install.py \
  software-evolution/scripts/bootstrap_project_memory.py \
  software-evolution/scripts/check_skill_integrity.py \
  software-evolution/scripts/validate_project_config.py \
  software-evolution/scripts/check_checkpoint_drift.py \
  software-evolution/scripts/validate_run_completion.py

python3 software-evolution/scripts/check_skill_integrity.py

python3 software-evolution/scripts/validate_project_config.py \
  --config software-evolution/memory/software-evolution.config.template.yml --json

python3 software-evolution/scripts/validate_run_completion.py \
  --run software-evolution/templates/autopilot-run.md --json

python3 -m unittest discover -s tests -v

git diff --check
```

本机存在系统 `skill-creator` 时还必须运行：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  software-evolution
```

## 5. 多角度 Review 清单

### 结构

- Frontmatter 只有 `name` 和 `description`。
- SKILL 链接、Workflow、Governance、Template、Memory、Script 完整。
- `agents/openai.yaml` 与模式语义一致。

### 只读安全

- `audit`、`verify`、`release-check`、`observe` 都包含 `WRITE POLICY: READ_ONLY`。
- 无隐式 Repair、Git/生产/外部写入。
- `--record` 只允许模式报告，不升级权限。

### 行为

- Bootstrap 首次完整创建，重复执行不覆盖，Dry Run 不写。
- Config Validator 覆盖成功、重复键、未知键、Boolean、风险、敏感键和安全底线。
- Drift 覆盖 No/Safe/Material/Conflicting/Unknown。
- Symlink/Copy 安装仍有效。

### Autopilot、睡后编程、连续性与恢复

- 默认命令无需 `init`/`audit`/`govern` 前置，自动 Bootstrap 后继续修复循环。
- `autopilot`、`overnight`、`deep` 使用 `CONTINUOUS_WRITE`，在安全可验证工作存在时持续执行。
- 批次按根因、业务能力、不变量、契约边界或兼容阶段划分，不能按文件数量机械拆分。
- 文件、Diff、Finding、Cycle、Batch 和耗时只作遥测；CI 必须阻止这些计数重新成为授权或停止条件。
- 旧 `budget`/`deep_budget`/`overnight_budget` 与旧 `autopilot.max_*` 可兼容解析，但必须进入 `deprecated_paths` 且不出现在 `effective_config`。
- 唯一且 Drift-safe 的宿主中断或旧配额型 partial 可由下一次默认命令在权威和最后门禁校验后自动接管；Resume 只处理无法自动接管的中断、漂移、歧义或指定恢复。
- 活跃 invocation owner 的重叠 branch/scope 禁止接管或新建；未知 liveness 必须按歧义处理。
- `RUN-*` 记录稳定父范围、三主线覆盖、运行态 UX、跨主线挑战、变更遥测、验证指纹和真实终止原因。
- 小型 R1 不必机械创建独立 `BATCH-*`；控制面应比例化并复用已有 Finding/Debt/Decision/Verification 证据。
- 可安全运行的 UI 必须在完成前有浏览器关键旅程证据，用户可见修复后必须复验。
- `safe work exhausted` 必须通过 schema-v3 Run Completion Validator，单一问题族耗尽或普通 Checkpoint 不能完成 Run/宿主持久 Goal。
- 同一命令、环境、Revision、输入、依赖和受影响路径指纹一致时才允许复用昂贵验证。
- 同一修复假设连续失败三次时只隔离该假设；仍须继续其他独立安全工作。
- Deep 在扫描前声明范围、关键能力/流程、不变量和证据覆盖，不声明人工文件/Finding/Batch 配额。
- 真实停止条件必须是安全工作耗尽、权威/审批/证据/环境/专项能力阻塞、受保护边界、冲突漂移或宿主中断。

### 文档一致性

- SKILL、README、USAGE、DESIGN、Workflow 的模式名、默认 Autopilot 路由、睡后编程边界、读写语义和 Verdict 一致。
- 每个新增模式都有对应模板/报告出口。

### 可移植性与安全

- 不包含本机绝对路径、凭证、Private Key、Token 或测试账号。
- 不提交 `.DS_Store`、`__pycache__/`、`*.pyc`、本机安装软链接。
- `git diff --check` 通过。

### GitHub 发布

- 检查 Git Status 和 Staged Scope。
- 中文 Commit Message。
- Push 后确认远端目录和 GitHub Actions `Validate Skill` 成功。

## 6. 仓库状态文件

`docs/state/` **需要提交**，它负责本仓库跨会话恢复。每次实质工作按仓库规则更新入口和线程文件，但不得写入本机绝对路径、凭证、完整临时日志或其他不可移植信息。

目标项目中的 `docs/software-evolution/` 与本仓库 `docs/state/` 是两套不同状态：前者是被治理系统的工程记忆，后者是本 Skill 仓库的开发上下文。

## 7. 提交范围

提交：

- 本任务相关 Skill、脚本、模板、文档、测试和 CI。
- 本线程 `docs/state/*.md` 及入口索引必要更新。

不提交：

- `.DS_Store`
- `__pycache__/`、`*.pyc`
- `.pytest_cache/`、Coverage 输出
- 凭证、Token、测试账号、生产数据
- 用户级 Codex 安装目录或本机软链接
- 与当前任务无关的其他线程/改动

## 8. CI

GitHub Actions 执行：

- 全部 Python 脚本语法检查。
- 配置模板验证。
- Skill 结构、链接、模式、安全和模板完整性检查。
- Bootstrap、Config、Drift、Run Completion、Mode Contract、Installer 测试。

只有本地验证和远端 `Validate Skill` 都通过，才能声明发布完成。
