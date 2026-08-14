---
name: 0113-DefinitionSplitter
description: Decompose (拆解) a LaTeX lecture-note block into N structured parts, following the pattern in Lecture6_SP.tex (Line20-133 -> Line135-285). Use when the user says “将…拆解为…个部分” and wants the content rewritten as multiple smaller \\customproblem blocks (each with its own toc entry/label/引用/注 and proof steps), preserving math and meaning.
---

# TeX Decompose Parts

## Workflow

当用户说“将 **拆解为 * 个部分”时，把指定 `.tex` 中的一段内容拆解成**指定数量**的结构化小块，输出风格对齐：
“将 `Lecture6_SP.tex` Line20-133 中的内容拆解为 `Lecture6_SP.tex` Line135-285”。

### 1) 锁定输入与目标

- **输入片段**：优先根据用户给出的 `文件 + Line范围` 定位；如果用户给的是标题/label，也可以用 `rg` 搜索定位到对应的 `\\customproblem{...}{...}` 块。
- **目标位置**：
  - 如果用户明确给了“拆解为 File LineX-Y”（或类似目标区间），就**用拆解结果覆盖/生成在该区间**（必要时以最小改动调整边界）。
  - 如果用户没给目标位置：默认把拆解结果**紧跟在原片段之后插入**（不删原文），并用与文档一致的分页/间隔（例如 `\\clearpage` / `\\newpage`）保持排版。

### 2) 决定“拆解”为哪些部分

按“Lecture6 引理1.1 → 引理1.1(1)/(2)/...”的做法：

- **优先拆分点**：原块里最外层 `enumerate` 的每个 `\\item`（或每个定理/引理的独立结论、每段证明）。
- **数量约束**：用户指定 `N` 个部分时必须产出 **恰好 N 个**部分：
  - 若自然分点数 = `N`：一一对应。
  - 若自然分点数 > `N`：按相邻主题合并成 `N` 组（保证每组内部连贯）。
  - 若自然分点数 < `N`：把最长/最关键部分再细分（按证明 Step、定义/结论/推导/小结拆分）。

### 3) 生成每个“部分”的 LaTeX 结构（对齐 Lecture6 示例）

对每个 part `k=1..N`，生成一个块（名称按原名加 `(k)`）：

- 一个 `\\customproblem{<原标题>(k)}{ ... }`，其 `{ ... }` 中包含该 part 的“设/则/结论”等（从原文抽取对应段落）。
- 一个对应的 `\\addcontentsline{toc}{subsubsection}{...}`：沿用原文风格，把 part 的结论（含必要数学式）写进 toc 字符串。
- 一个 `\\phantomsection\\label{...}`：沿用原 label 模式，必要时在末尾加 `(k)`（不改 `<SP>` 这类占位符格式）。
- `\\textbf{引用:}` 与 `\\textbf{注:}`：若原块在该部分没有填任何内容，则保留空占位：
  - `\\hspace*{2em} 1. \\quad`
- 证明体裁与缩进：
  - `Proof:` 行（或 `\\begin{tcolorbox}` 内）使用 `Step1/Step2/...` 的行内结构，缩进用 `\\hspace*{2em}`（更深层用 `4em/6em/...`），整体风格与 `Lecture6_SP.tex` 一致。

### 4) 保真与最小改动原则

- **不改数学/语义**：只做结构化拆解、重排、补充必要的连接词（不引入新结论）。
- **不乱动全局结构**：除拆解区间外不改别处；避免重命名无关 label；保持原有缩进与环境（`enumerate`、`tcolorbox` 等）风格一致。
- **拆解说明**：在回复里用一句话总结映射关系，例如：
  - “将 `Lecture6_SP.tex` Line20-133 拆解为 `Lecture6_SP.tex` Line135-285（共 N 部分）。”

## Style Reference

如需对齐具体细节，直接打开并对照：
- `Lecture/Stochastic Process/Lecture Notes/Lecture6/Notes/Lecture6_SP.tex`（示例：Line20-133 与 Line135-285）
