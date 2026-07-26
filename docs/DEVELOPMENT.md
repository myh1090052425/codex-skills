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

无参数入口必须映射 `autopilot`，自动初始化缺失控制面、接管唯一 budget-only partial，并在正常 Window 到限后同调用续跑；CI 应阻止再次映射为 `govern`、要求手工前置模式或把 Window 当终止点。

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

- 非覆盖式创建 `.software-evolution.yml`、四个基础 Memory 文件和报告/决策/批次/运行账本目录。
- 使用独占创建避免并发覆盖。
- `--dry-run` 不得产生文件或目录。

### `validate_project_config.py`

- 只支持两空格 Mapping + Scalar 的受限 YAML。
- 拒绝重复/未知键、Tab、复杂 YAML、非小写 Boolean 和敏感键。
- `observe.production_read_only` 必须为 `true`。
- 输出原始 `config`、确定性合并后的 `effective_config` 和 `defaulted_paths`；校验 Session/Window、Governance 文件额度、Overnight 与验证底线。

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
  --config software-evolution/memory/software-evolution.config.template.yml --json

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

### Autopilot、睡后编程、恢复与预算

- 默认命令无需 `init`/`audit`/`govern` 前置，自动 Bootstrap 后继续修复循环。
- 旧版部分配置得到完整 `effective_config`，不得自行发明临时额度。
- Session/Window 双层预算清晰；Window 到限后同调用 rollover，不返回要求用户 `resume`。
- Implementation/Governance 双分账；治理文件不得消费产品文件额度。
- Verification Reserve 是墙钟 floor，不是执行测试后归零的 balance。
- 唯一 budget-only partial 可由下一次默认命令自动接管；Resume 只处理真实中断、漂移、歧义或指定恢复。
- 活跃 invocation owner 的重叠 branch/scope 禁止接管或新建；未知 liveness 必须按歧义处理。
- 显式 `continue_after_budget_checkpoint: false` 和零 Governance 额度均有确定的暂停/只读语义。
- Overnight 有隔离、时间、循环、批次、文件、失败和验证门禁。
- `RUN-*` 记录 Session、当前 Window、Window Ledger、双文件账本和真实终止原因。
- Deep 在扫描前声明范围、Finding、批次、文件和验证预留。

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
- Bootstrap、Config、Drift、Mode Contract、Installer 测试。

只有本地验证和远端 `Validate Skill` 都通过，才能声明发布完成。
