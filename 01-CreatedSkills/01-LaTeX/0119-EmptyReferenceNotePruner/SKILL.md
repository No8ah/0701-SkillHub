---
name: 0119-EmptyReferenceNotePruner
description: When the user says “删除没有填写内容的引用和注”, remove empty LaTeX sections like \textbf{引用:} / \textbf{注:} that contain only placeholder lines (e.g. \hspace*{2em} 1. \quad) from .tex files, without changing any other content.
---

# TeX Prune Empty Ref/Note

删除 LaTeX 文档中“未填写内容”的 `\textbf{引用:}` 与 `\textbf{注:}` 占位块（只包含类似 `\hspace*{2em} 1. \quad` 的空条目时才删除），其余内容保持不变。

## 适用输入

- 用户明确说：`删除没有填写内容的引用和注`（或同义表达）
- 目标文件为 `.tex`（例如你上传的 `Chapter1_NMSDE.tex`）

## 删除规则（必须同时满足才删）

对每个块分别判断：

- 块头为单独一行：`\textbf{引用:}` 或 `\textbf{注:}`（允许前置缩进）
- 块内只包含：空行 + 若干条目行 `\hspace*{2em} <数字>. \quad`（其后无任何文字） + 空行

如果 `\textbf{引用:}`/`\textbf{注:}` 下方出现了任何非空内容（例如 `\hyperref[...]`、文字说明、公式等），则**绝不删除**。

## Quick Start

- 就地修改（推荐）：
  - `python3 /Users/quzinan/.codex/skills/tex-prune-empty-refnote/scripts/prune_empty_refnote.py /path/to/file.tex`

- 只检查不写入：
  - `python3 /Users/quzinan/.codex/skills/tex-prune-empty-refnote/scripts/prune_empty_refnote.py --check /path/to/file.tex`

## 对 `Chapter1_NMSDE.tex` 的典型用法

- `python3 /Users/quzinan/.codex/skills/tex-prune-empty-refnote/scripts/prune_empty_refnote.py \
  /Users/quzinan/Downloads/Code/Lecture/Numerical\ Methods\ for\ Solving\ Differential\ Equations/Chapter1/Notes/Chapter1_NMSDE.tex`
