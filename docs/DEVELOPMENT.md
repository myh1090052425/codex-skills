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

Skill 必须包含九种 Workflow：

```text
init audit govern repair verify deep release-check observe resume
```

Write Policy：

```text
CONTROL_PLANE_ONLY
READ_ONLY
BOUNDED_WRITE
BUDGETED_WRITE
INHERITED_OR_READ_ONLY
```

`check_skill_integrity.py` 会校验必需文件、Frontmatter、链接、模式 Marker、Agent Metadata、模板、配置、JSON 和可移植性。

## 3. 脚本职责

### `bootstrap_project_memory.py`

- 非覆盖式创建 `.software-evolution.yml`、四个基础 Memory 文件和报告/决策/批次目录。
- 使用独占创建避免并发覆盖。
- `--dry-run` 不得产生文件或目录。

### `validate_project_config.py`

- 只支持两空格 Mapping + Scalar 的受限 YAML。
- 拒绝重复/未知键、Tab、复杂 YAML、非小写 Boolean 和敏感键。
- `observe.production_read_only` 必须为 `true`。

### `check_checkpoint_drift.py`

- `--snapshot` 生成 Batch Metadata。
- 比较 Branch、HEAD、Worktree Fingerprint/Entries 和 Scope Paths。
- 输出 `NO_DRIFT`、`SAFE_DRIFT`、`MATERIAL_DRIFT`、`CONFLICTING_DRIFT` 或 `UNKNOWN`。

## 4. 本地验证

```bash
python3 -m py_compile \
  install.py \
  software-evolution/scripts/bootstrap_project_memory.py \
  software-evolution/scripts/check_skill_integrity.py \
  software-evolution/scripts/validate_project_config.py \
  software-evolution/scripts/check_checkpoint_drift.py

python3 software-evolution/scripts/check_skill_integrity.py

python3 software-evolution/scripts/validate_project_config.py \
  --config software-evolution/memory/software-evolution.config.template.yml

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

### 恢复与预算

- Deep 在扫描前声明范围、Finding、批次、文件和验证预留。
- Resume 对每种 Drift 有明确行为。
- 预算不足时不开始下一批修复。

### 文档一致性

- SKILL、README、USAGE、DESIGN、Workflow 的模式名、读写语义和 Verdict 一致。
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
- Bootstrap、Config、Drift、Mode Contract、Installer 测试。

只有本地验证和远端 `Validate Skill` 都通过，才能声明发布完成。
