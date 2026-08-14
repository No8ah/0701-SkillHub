---
name: 0101-ChapterLogicFormatter
description: Organize LaTeX chapter subfiles into a standardized Definition → Property → Theorem logical structure. Use when the user asks to organize, restructure, or format the logical flow of a chapter's subsections, or to convert content into the 定义→性质→定理 template pattern.
---

# format-chapter-logic

Given a LaTeX subfile with the standardized header, insert content blocks after `% Content` in a strict definition-first logical order.

## Block Sequence (Canonical)

After `% Content`, every subfile follows this exact pattern:

```
% Content
  ↓
[定义块] — one, names the concept
  ↓
[性质(1) 块] — first property of the concept
  ↓
[性质(2) 块] — second property of the concept
  ↓
[定理块] — theorem tying it together
  ↓
\end{document}
```

Each block is on its own page (`\clearpage\newpage`). **All subsection titles use `\textcolor{blue}`.**

## Naming Rules

### Rule 1: Cumulative vocabulary

The `<定义名称>` in the definition block becomes the **prefix** for all property and theorem blocks in that subfile:

| Block | Title format |
|-------|-------------|
| 定义 | `<定义名称>` |
| 性质(1) | `<定义名称>的性质(1) - <中文描述>` |
| 性质(2) | `<定义名称>的性质(2) - <中文描述>` |
| 定理 | `<定义名称>的定理 - <中文描述>` |

**Properties and theorems never introduce a new prefix.** They reference the definition's name.

### Rule 2: Chinese descriptions are short and substantive

`<中文描述>` is 2–8 characters, describing the block's content. Examples:
- `矩阵恒等式`, `逗留时间`, `灭绝概率`, `详细平衡方程`
- `极限存在性`, `阈值行为`
- `Kelly 引理`, `Burke 定理`

**Never use placeholders like `输入定理名称`.** If the mathematical content is not yet decided, leave the whole subsection empty rather than writing a placeholder title.

### Rule 3: Property numbering is sequential

`性质(1)` then `性质(2)`. When inserting a new property, update the numbers of all following properties.

### Rule 4: `\customproblem` type and label match the block type

| Block | `\customproblem` type | Label prefix |
|-------|----------------------|-------------|
| 定义 | `补充 - 定义 - Content - <name>` | `def:<course>:<chap>:<id>` |
| 性质 | `补充 - 性质 - Content - <name>` | `prop:<course>:<chap>:<id>` |
| 定理 | `补充 - 定理 - Content - <name>` | `thm:<course>:<chap>:<id>` |

## Template Blocks

### Definition

```latex
\clearpage
\newpage

\subsection*{\textcolor{blue}{<定义名称>}}
\addcontentsline{toc}{subsection}{\textcolor{blue}{<定义名称>}}

    \customproblem{补充 - 定义 - Content - <定义名称>}{

    设:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    如果:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    定义:
    \[
        \ldots \quad \triangleq \quad \text{<定义名称>}
    \]
    }

    \addcontentsline{toc}{subsubsection}{补充 - 定义 - Content - <定义名称>}

    \phantomsection\label{def:<course>:<chap>:<id>}
```

### Property

```latex
\clearpage
\newpage

\subsection*{\textcolor{blue}{<定义名称>的性质(N) - <中文描述>}}
\addcontentsline{toc}{subsection}{\textcolor{blue}{<定义名称>的性质(N) - <中文描述>}}

    \customproblem{补充 - 性质 - Content - <定义名称>的性质(N) - <中文描述>}{

    设:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    如果:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    则:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    }
    \addcontentsline{toc}{subsubsection}{补充 - 性质 - Content - <定义名称>的性质(N) - <中文描述>}

    \phantomsection\label{prop:<course>:<chap>:<id>}
```

### Theorem

```latex
\clearpage
\newpage

\subsection*{\textcolor{blue}{<定义名称>的定理 - <中文描述>}}
\addcontentsline{toc}{subsection}{\textcolor{blue}{<定义名称>的定理 - <中文描述>}}

    \customproblem{补充 - 定理 - Content - <定义名称>的定理 - <中文描述>}{

    设:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    如果:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    则:
    \begin{enumerate}

        \item ...

    \end{enumerate}
    }

    \addcontentsline{toc}{subsubsection}{补充 - 定理 - Content - <定义名称>的定理 - <中文描述>}

    \phantomsection\label{thm:<course>:<chap>:<id>}
```

## Prerequisites

The main chapter file must include `\usepackage[UTF8]{ctex}` for Chinese character support:

```latex
\documentclass[a3paper]{book}
\input{Set/Package_set.tex}
\input{Set/Environment_set.tex}
\usepackage[UTF8]{ctex}   % ← required
\linespread{1.9}
```

Chinese text inside math mode must be wrapped in `\text{...}`:

```latex
% Wrong:
\quad \triangleq \quad 连续时间马氏链
% Correct:
\quad \triangleq \quad \text{连续时间马氏链}
```

## Post-creation Verification

After filling all subfiles, verify:

1. **Every subfile has all 4 blocks** (定义, 性质(1), 性质(2), 定理)
2. **No placeholder names** — grep for `输入定理名称`
3. **All blocks in a subfile share the same `<定义名称>` prefix**
4. **Property numbering is (1), (2) sequentially**
5. **Labels are unique** across all subfiles in the chapter
6. **No Chinese characters appear bare in math mode** (use `\text{}`)

## Content note

The `\customproblem` blocks are left as skeletons — the `设:/如果:/则:` items contain placeholder content. This skill provides the structural framework; filling in the substantive mathematical content (definitions, proofs, derivations) is a separate task.
