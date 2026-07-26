# AI Software Evolution Agent

一个长期可复用的 Codex Skill。它让 Codex 不再只是代码生成或报告型 Code Review 工具，而是以项目长期技术负责人的身份，持续治理：

- 用户体验和业务流程
- 前端、后端、数据库与稳定性
- 架构边界和业务能力复用
- 业务规则一致性
- 测试可靠性
- 技术债和工程记忆

在具备明确行为和验证条件时，Agent 会自主修改代码、补充测试并执行验证，而不是只输出问题报告。

## 仓库结构

```text
software-evolution-agent/
├── README.md
├── install.py
├── software-evolution/
│   ├── SKILL.md
│   ├── agents/
│   ├── workflows/
│   ├── governance/
│   ├── templates/
│   ├── memory/
│   └── scripts/
└── tests/
```

`software-evolution/` 本身就是完整 Skill 目录，可以单独复制、软链接或被其他 Skill/Plugin 仓库引用。

## 文档

- [安装与使用](docs/USAGE.md)
- [治理模型与安全设计](docs/DESIGN.md)
- [开发与验证](docs/DEVELOPMENT.md)

## 安装

克隆仓库后执行：

```bash
python3 install.py
```

安装器默认创建用户级软链接，不复制源码，因此仓库内更新会直接反映到 Codex。

查看安装计划但不写入：

```bash
python3 install.py --dry-run
```

复制安装而不是软链接：

```bash
python3 install.py --copy
```

指定其他 Skill 目录：

```bash
python3 install.py --target ~/.agents/skills/software-evolution
```

安装器不会覆盖已有的不同目录或软链接。

## 使用

```text
$software-evolution init
$software-evolution
$software-evolution deep
$software-evolution repair
$software-evolution repair DEBT-001
```

也可以在 Codex 中执行 `/skills`，然后选择 **AI Software Evolution Agent**。

### 模式

| 模式 | 作用 |
|---|---|
| `init` | 建立系统模型、架构记忆、能力地图、技术债和验证基线 |
| 默认模式 | 分析近期变化，治理 UX、工程质量和架构影响，自动修复低风险问题 |
| `deep` | 分阶段执行仓库级深度治理、能力收敛和技术债处理 |
| `repair` | 修复指定问题或债务项，补测试并完成分层验证 |

## 项目工程记忆

首次执行 `init` 后，默认在目标项目创建：

```text
docs/software-evolution/
├── architecture-memory.md
├── capability-map.md
└── technical-debt.md
```

初始化脚本默认不覆盖已有文件，可以安全重复执行。

## 安全边界

Skill 使用 R0–R4 风险分级：

- 明确 Bug、局部重复、缺失测试等低风险问题可自主修复。
- 共享模块和内部契约修改需要先建立影响范围和回滚边界。
- 数据模型、权限、核心业务模型和公共 API 必须先形成分阶段兼容方案。
- 生产修改、不可逆数据操作、凭证权限和 Git 历史重写始终需要明确确认。

任何修改都必须记录验证结果；未执行、失败和受阻检查不能被描述为“已验证”。

## 本地验证

```bash
python3 -m py_compile \
  software-evolution/scripts/bootstrap_project_memory.py \
  software-evolution/scripts/check_skill_integrity.py \
  install.py

python3 software-evolution/scripts/check_skill_integrity.py
python3 -m unittest discover -s tests -v
```
