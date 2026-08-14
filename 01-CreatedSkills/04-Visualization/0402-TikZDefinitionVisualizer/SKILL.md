---
name: 0402-TikZDefinitionVisualizer
description: 为 LaTeX 笔记中的定义块（尤其是 `\\customproblem{...}{...}`）处理 TikZ 图示，并保持原有结构不变。用于“用 tikz 画图示/补充图示”或“把图示注释掉/取消注释”请求，目标文件通常是 `.tex`。重点是图示必须位于定义块内部，不破坏 `\\addcontentsline` 与 `\\label`，且 TikZ 环境内不出现中文字符。
---

# Draw Tikz Definition Figure

按“先定位定义，再选择模式，再验证”的顺序执行。

## Workflow

1. 读取用户给定的 `.tex` 行号或定义块，确认目标是哪个 `\customproblem{...}{...}`。
2. 根据请求选择模式：
   `draw`：新增或更新图示；
   `comment`：注释图示块；
   `uncomment`：取消注释图示块。
3. `draw` 模式：提取定义中的核心量和几何关系（例如 `h_1`、`h_2`、`h=\sqrt{h_1^2+h_2^2}`），并在定义块内部插入
   `图示:` + `center` + `tikzpicture`（放在“定义公式”前或紧邻公式处）。
4. `comment/uncomment` 模式：仅操作 `图示:` 与其后 `\begin{center}...\end{center}` 区域，不改公式和目录行。
5. 保持以下结构不变：
   `\addcontentsline{...}`、`\phantomsection\label{...}`、已有目录文本与编号。
6. 若当前工程未加载 TikZ，则补充 `\usepackage{tikz}` 和必要 `\usetikzlibrary{...}`。
7. 在提交前运行 `scripts/check_tikz_no_chinese.py <tex-file-or-dir>`，确保所有激活的 `tikzpicture` 内无中文。
8. 运行一次最小编译检查（如 `xelatex -halt-on-error`）确认无新报错。

## Placement Rules

- 把图放在 `\customproblem` 的内容大括号内，不要放到块外。
- 不改动定义公式的数学含义，只补充图示解释。
- 图中变量命名与正文一致（`h_1/h_2/h`、`(i,j)` 等）。
- 优先简洁示意图：单元格、步长箭头、关键对角线或法向量，不做无关装饰。
- `tikzpicture` 环境内部禁止出现中文（包括注释、`\node{...}` 文本、标签说明）。统一使用英文或数学符号。
- 注释模式默认同时注释 `图示:` 行与后续 `center` 块，保持块内相对缩进不变。

## Standard Pattern

优先使用如下结构（根据定义内容替换图中元素）：

```tex
图示:
\begin{center}
    \begin{tikzpicture}[scale=1.1,>=Stealth]
        % 根据定义绘制关键几何对象与标注
    \end{tikzpicture}
\end{center}
定义:
\[
    ...
\]
```

对于网格尺度定义，可使用“单元对角线”模板：

```tex
\coordinate (O) at (0,0);
\coordinate (A) at (3,0);
\coordinate (B) at (0,2);
\coordinate (C) at (3,2);
\draw[thick] (O) -- (A) -- (C) -- (B) -- cycle;
\draw[<->] (0,-0.45) -- (3,-0.45) node[midway,below] {$h_1$};
\draw[<->] (-0.45,0) -- (-0.45,2) node[midway,left] {$h_2$};
\draw[red,thick,->] (O) -- (C);
\node[red,above] at (1.45,1.1) {$h$};
```

## Script

- `scripts/check_tikz_no_chinese.py`
- 作用：扫描 `.tex` 文件中激活的 `tikzpicture` 环境，若包含中文字符则报错并给出行号。
- 用法：

```bash
python3 scripts/check_tikz_no_chinese.py path/to/file.tex
python3 scripts/check_tikz_no_chinese.py path/to/tex-directory
```

- `scripts/comment_center_blocks.py`
- 作用：批量注释或取消注释 `图示:` 与其后 `\begin{center}...\end{center}` 区域。
- 用法：

```bash
python3 scripts/comment_center_blocks.py path/to/file.tex --mode comment
python3 scripts/comment_center_blocks.py path/to/file.tex --mode uncomment
python3 scripts/comment_center_blocks.py path/to/dir --mode comment --dry-run
```

## Output Contract

- 返回结果时说明修改了哪个文件和行号附近内容。
- 明确说明是否完成编译检查；若未运行，给出原因。
