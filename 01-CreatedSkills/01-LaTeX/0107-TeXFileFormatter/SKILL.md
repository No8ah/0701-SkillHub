---
name: 0107-TeXFileFormatter
description: Format LaTeX/TeX files conservatively. Use when user asks “格式化tex文件”. The formatter normalizes tabs/trailing spaces, ensures `\clearpage` + `\newpage` before each `\section*{...}` / `\subsection*{...}`, and can optionally break long inline math around `=` / `\leqslant` inside `$...$`.
---

# 格式化 TeX 文件

参考：`tools/skills_example/Example_格式化tex文件.md`（核心区间 `187-618`，补充示例 `663-786, 788-799`）。

## 何时使用

- 用户明确要求“格式化 tex 文件 / 格式化 latex”。
- 目标是排版一致性，不是重写内容语义。

## 快速命令

```bash
python3 scripts/format_tex.py --check <file-or-dir>
python3 scripts/format_tex.py --check --diff <file-or-dir>
python3 scripts/format_tex.py <file-or-dir>
python3 scripts/format_tex.py --break-long-math <file-or-dir>
```

## 工作流

1. 先跑 `--check`，确认会改哪些文件。  
2. 需要人工先看改动时，使用 `--check --diff`。  
3. 再执行写回命令（默认不拆长公式；只有显式传 `--break-long-math` 才拆）。

## 规则（严格）

1. 统一 `\t` 为 4 空格，并移除行尾空白。  
2. 在每个 `\section*{...}` 与 `\subsection*{...}` 前确保存在连续的 `\clearpage` + `\newpage`。缺失则自动补齐。  
3. `--break-long-math` 开启后，仅在长行且位于 `$...$` 内的 ` = ` / ` \leqslant ` 处分行。  
4. 不改 `\label{...}`、`\addcontentsline{...}`、`\customproblem{...}` 等语义内容。

## 边界与协作

- 本技能是“保守格式化”，不做公式语义改写、不重排题目结构。  
- 如果用户还要求补前文注释（文件头元信息），串行调用 `填写Tex前文注释` 技能。  
- `--check`：无变更返回码 `0`；有变更返回码 `1`；读写错误返回码 `2`。
