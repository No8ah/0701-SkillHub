---
name: 0108-DefinitionSectionStarAdder
description: Insert unnumbered LaTeX section headers with `\star \star \star` based on `\customproblem{补充 - 定义/定理 - Content - ...}` titles. Use when prompts say “根据定义添加section并添加3 star” or ask to add heading blocks before definition/theorem problems, including matching `\addcontentsline` entries, while keeping problem bodies unchanged.
---

# 根据定义添加section并添加3 star

## Quick Start

- 预览：
  `python3 scripts/add_section_3star_from_definition.py path/to/file.tex > /tmp/out.tex`
- 原地修改：
  `python3 scripts/add_section_3star_from_definition.py --in-place path/to/file.tex`

## 规则（严格）

1. 扫描 `\customproblem{TITLE}{...}`。
2. 仅匹配两类标题：
   - `补充 - 定义 - Content - ...`
   - `补充 - 定理 - Content - ...`
3. 从 `Content -` 后提取主题名，主题取第一个 ` - ` 前的片段。
4. 在该 `\customproblem` 前插入块（若未存在）：
   - 定义块：
     - `\clearpage`
     - `\newpage`
     - `\subsection*{\textcolor{blue}{<主题> $\star \star \star$}}`
     - `\addcontentsline{toc}{subsection}{\textcolor{blue}{<主题> $\star \star \star$}}`
   - 定理块：
     - `\clearpage`
     - `\newpage`
     - `\section*{\textcolor{red}{<主题> $\star \star \star$}}`
     - `\addcontentsline{toc}{section}{\textcolor{red}{<主题> $\star \star \star$}}`
5. 防重复：若 `\customproblem` 前最近的非空语句已包含对应 `\addcontentsline{toc}{subsection|section}{...<主题> $\star \star \star$...}`，则跳过。

## 约束

- 仅新增标题块，不改 `\customproblem` 正文。
- 不改 `\label`、`\phantomsection`、公式与证明内容。
- 不删除用户已有内容。

## 参考

- `references/Example_根据定义添加section并添加3 star.md`
