# 01-CreatedSkills — 自研 Skills

按领域分类的自研 Skills。

| 目录 | 领域 | Skills |
|------|------|--------|
| [01-LaTeX/](01-LaTeX/) | LaTeX 工具链 | 0101–0118 |
| [02-Research/](02-Research/) | 科研辅助 | 0201–0203 |
| [03-Coding/](03-Coding/) | 编码/工作流 | 03xx |
| [04-Visualization/](04-Visualization/) | 可视化 | 0401–0402 |
| [08-Workflow/](08-Workflow/) | 部署/同步 | 0801–0803 |

每个 Skill 目录结构：

```
<SkillID>-<FunctionName>/
├── SKILL.md    # 技能定义（frontmatter name 与目录名一致）
├── scripts/    # 辅助脚本
└── references/ # 参考文档
```

安装：将整个 skill 目录复制到 `~/.claude/skills/`（或项目 `.claude/skills/`）。
