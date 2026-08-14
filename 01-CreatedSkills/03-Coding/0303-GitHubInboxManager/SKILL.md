---
name: github-inbox-manager
description: >
  将 GitHub 项目搜索 + Zotero README 表格入库 + Inbox 清理工作流。
  当用户给出 Project_Inbox / Skill_Inbox / MCP_Inbox / Website_Inbox / arXiv_Inbox / DOI_Inbox
  片段并要求"搜索 GitHub 地址 / 入库到 tabularx / 归档 / 清理 Inbox"时使用。
  触发动词: 搜索 GitHub 地址、入库、归档、清理 Inbox、archive。
---

# GitHub Inbox Manager

将选中片段中的 GitHub 项目搜索地址后，入库到 Zotero 的
`01_Projects/01_Projects_README.tex` 和 `13_Skills/13_Skills_README.tex`
的 tabularx 表格中；Inbox 标题保持不动；已入库内容从 Inbox 中删除。

## 输入格式（用户粘贴的 Inbox 片段）

```
Project\_Inbox

项目名1
https://github.com/xxx/yyy
项目名2

Skill\_Inbox

skill-a

MCP\_Inbox

mcp-x

Website\_Inbox

WebtoAGI

arXiv\_Inbox

2605.28424v1

DOI\_Inbox

10.32629/mcmf.v5i4.2573
```

## Step 1 — 搜索 GitHub 地址

对每个项目名调用 GitHub 搜索（用 `.mcp.json` 中的 token，避免 MCP 缓存 token 报错）：

```bash
TOKEN=$(python3 -c "import json; d=json.load(open('/Users/quzinan/Downloads/Code/.mcp.json')); print(d['mcpServers']['github']['env']['GITHUB_PERSONAL_ACCESS_TOKEN'])")

curl -s -H "Authorization: Bearer $TOKEN" "https://api.github.com/search/repositories?q=<QUERY>&sort=stars&per_page=1"
```

**批量搜索**：写入 `/tmp/queries_batch.json`（JSON 数组），用
`scripts/search_batch.py`（位于本 skill 目录）循环执行，每次间隔 3s 防 403 限流。

**匹配规则**：
- 已知 URL（用户直接给出 `https://github.com/...`）→ 直接用，不搜索
- 结果不准时精修：`q=<name> in:name`，必要时 `org:xxx` 或换关键词
- NOT FOUND / 明显不匹配（⭐ 个位数且描述无关）→ 保留在 Inbox 中
- 重复项（表中已存在）→ 跳过入库，但仍从 Inbox 删除

## Step 2 — 入库到 tabularx

### 01_Projects_README.tex 表格分类

| 表格 | 行格式 |
|------|--------|
| Work Projects / Research Projects | `\textbf{name} & 功能 & \url{URL}  & $\surd$ \\` |
| AI Agent 实验 / 量化/金融 / 多媒体/创意 / 杂项工具 | 同上 |
| MCP Servers | `\textbf{name} & 功能 & \url{URL} & $\times$ \\` |
| Website | `\textbf{name} & 功能 & \url{URL} & $\times$ \\` |

**表格列**：`名称 & 类型/功能 & 仓库地址 & 是否配置`

### 13_Skills_README.tex 表格分类

| 表格 | 行格式 |
|------|--------|
| 01 Work Skills / 02 Research / 03 Toy | `\textbf{name} & 功能 & \href{URL}{GitHub} \\` |

**表格列**：`名称 & 功能 & 下载地址`

### 插入方法（已验证）

用 Python 按行号定位插入点（避免转义问题）：

```python
with open('01_Projects_README.tex') as f:
    lines = f.readlines()

def find(marker):
    for i in range(len(lines)):
        if marker in lines[i]:
            return i
    return -1

insert_rows = [
    '    \\textbf{X} & 功能 & \\url{https://github.com/a/b}  & $\\surd$ \\\\\n',
]
idx = find('某已有行标记')   # 插入到该行之后
lines[idx+1:idx+1] = insert_rows
```

在 `\bottomrule` 前插入；每行以 `\\` 结尾；带下划线的名字转义 `\_`。

## Step 3 — Inbox 标题保持不动

`Project\_Inbox`、`Skill\_Inbox`、`MCP\_Inbox`、`Website\_Inbox`、
`arXiv\_Inbox`、`DOI\_Inbox` 这些标题行永远保留，即使内容清空。

## Step 4 — 删除已入库内容

对 Inbox 块按行重建：保留「未找到/未入库」项，删除「已入库」项。
使用 `scripts/inbox_clean.py`（本 skill 目录），参数为保留项列表：

```bash
python3 ~/.claude/skills/0303-GitHubInboxManager/scripts/inbox_clean.py \
  /Users/quzinan/Desktop/Zotero/01_Projects/01_Projects_README.tex \
  '["VoiceChat 11B","Codar","WebtoAGI"]'
```

保留规则：
- 未找到的 GitHub 项目（VoiceChat 11B、Codar、Umomi 等）→ 保留
- arXiv ID、DOI → 永远保留（非 GitHub 内容）
- 已入库项 → 删除

## 编译验证

```bash
cd /Users/quzinan/Desktop/Zotero/01_Projects && xelatex -interaction=nonstopmode 01_Projects_README.tex
cd /Users/quzinan/Desktop/Zotero/13_Skills && xelatex -interaction=nonstopmode 13_Skills_README.tex
```

## Gotchas

- **GitHub MCP 服务器缓存旧 token**：MCP 工具可能报 "Bad credentials"，直接用
  curl + `.mcp.json` 中的 token，不要依赖 MCP 工具搜索。
- **搜索限流 403**：`search/repositories` 未认证限 10 req/min，批量搜索必须
  `sleep 3`；失败项单独重试。
- **Python heredoc 转义陷阱**：`'''...\\textbf...'''` 在 bash heredoc 中
  `\\` 会变成 `\`，用行号定位 + `lines[idx+1:idx+1] = [...]` 最稳。
- **重复入库**：入库前 grep 表中是否已有该 URL，跳过重复。
- **star 数不可靠**：泛词（spaCy、orca、galaxy）会匹配到无关仓库，用
  `in:name` 精修。
