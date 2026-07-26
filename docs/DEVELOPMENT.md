# 开发与验证

## 修改原则

- 保持 `software-evolution/SKILL.md` 为核心导航和执行入口。
- 将详细流程放入 `workflows/`，详细规则放入 `governance/`。
- 将可复制的项目输出放入 `templates/` 和 `memory/`。
- 不在 Skill 目录中新增独立 README、安装说明或变更日志；仓库级说明统一放在根目录或 `docs/`。
- 新增脚本时必须使用标准库优先，并提供可重复测试。
- 不降低自主修改的风险门禁或验证完整性。

## 本地验证

```bash
python3 -m py_compile \
  install.py \
  software-evolution/scripts/bootstrap_project_memory.py \
  software-evolution/scripts/check_skill_integrity.py

python3 software-evolution/scripts/check_skill_integrity.py
python3 -m unittest discover -s tests -v
```

如果本机存在系统 `skill-creator`，还应执行：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  software-evolution
```

## Pull Request 检查

GitHub Actions 会自动执行：

- Python 脚本语法检查。
- Skill 必需文件、frontmatter、链接和模板完整性检查。
- 工程记忆初始化幂等性测试。
- 安装器 dry-run、软链接和复制安装测试。

提交前不要包含：

- `.DS_Store`
- `__pycache__/`
- `*.pyc`
- `docs/state/`
- 本机 Codex 安装目录或软链接
- 凭证、测试账号和环境私密配置
