# 0303-GitHubInboxManager

将 GitHub 项目搜索 + Zotero README 表格入库 + Inbox 清理工作流封装为 Skill。

## 功能

| Step | 动作 |
|------|------|
| 1 | 使用 GitHub API 搜索选中项目的仓库地址（批量、防限流） |
| 2 | 入库到 `01_Projects/01_Projects_README.tex` 和 `13_Skills/13_Skills_README.tex` 的 tabularx 表格 |
| 3 | Inbox 标题（Project/Skill/MCP/Website/arXiv/DOI\_Inbox）保持不动 |
| 4 | 删除已入库内容，保留未匹配项 |

## 文件

```
0303-GitHubInboxManager/
├── SKILL.md              # 工作流文档（触发动词 + 4 步 + Gotchas）
└── scripts/
    ├── search_batch.py   # 批量 GitHub 搜索（3s 间隔防 403）
    └── inbox_clean.py    # Inbox 清理（保留指定项列表）
```

## 使用

安装到 `~/.claude/skills/0303-GitHubInboxManager/`，向 Claude 粘贴 Inbox 片段并说
"搜索 GitHub 地址 / 入库 / 归档 / 清理 Inbox" 即自动触发。

### search_batch.py

```bash
echo '["item1","item2"]' > /tmp/queries_batch.json
python3 scripts/search_batch.py   # 输出 → /tmp/search_results.json
```

### inbox_clean.py

```bash
python3 scripts/inbox_clean.py <README.tex> '["未找到项1","arXiv ID"]'
```

## Gotchas

- GitHub MCP 服务器会缓存旧 token，搜索直接用 `.mcp.json` 中的 token + curl
- `search/repositories` 未认证限 10 req/min，批量必须 `sleep 3`
- Python heredoc 中 `\\` 转义易错，表格插入用行号定位
- 入库前 grep 检查重复；泛词（spaCy/orca）用 `in:name` 精修
