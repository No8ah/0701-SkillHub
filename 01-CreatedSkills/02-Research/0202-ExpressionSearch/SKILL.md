---
name: 0202-ExpressionSearch
description: Search LaTeX files for incomplete mathematical expressions, empty customproblem templates, and missing addcontentsline formulas; fill them by cross-referencing patterns from related subfiles.
---

# Search Expression

Search and fill incomplete mathematical expressions in LaTeX study notes. Operates on structured subfile-based LaTeX documents with `\customproblem` environments and `\addcontentsline` table-of-contents entries.

## Pattern Catalog

### 1. Empty `\customproblem` templates

A `\customproblem` with empty 设/如果/则 sections:

```latex
\customproblem{补充 - 定义 - Content - 二维向前差分格式的时间差分算子}{

    设:
    \begin{enumerate}
        \item
    \end{enumerate}
    如果:
    \begin{enumerate}
        \item
    \end{enumerate}
    定义:
    \[
        \quad \triangleq \quad
        \text{名称}
    \]
    }
```

Detection:
```bash
grep -n '\\item\s*$' <file> | head -5
```

Fill pattern: look for the corresponding **filled** template in a sibling subfile (e.g., the 1D version of the same operator/property) and adapt with appropriate dimension/index notation.

### 2. Empty addcontentsline (no `$` formula)

```bash
grep -n "addcontentsline.*subsubsection" <file> | grep -v '\$'
```

Fix by adding the mathematical expression after `-`:
```latex
\addcontentsline{toc}{subsubsection}{... - $\frac{u_j^{n+1} - u_j^n}{\tau}$}
```

The formula should match the definition in the corresponding `\customproblem`.

### 3. Empty `$:= \quad \text{...}$` in 设 items

Detect:
```bash
grep -n '\$:=' <file>
```

Fix by extracting the formula from the definition or from a sibling file:
```latex
\item $\frac{u_j^{n+1} - u_j^n}{\tau} := \quad \text{描述}$
```

## Cross-Reference Strategy

When filling a template, find a filled reference in the same course's notes:

1. **1D → 1D**: Same subfile structure, different scheme
   - Example: Forward difference → Backward difference operators
   - Adapt the time level ($t_n$ vs $t_{n+1}$) and sign of Taylor expansion terms

2. **1D → 2D**: Extend by adding $y$ dimension
   - Add $y_k$ index, $h_y$ step size, $\delta_y^2$ operator
   - One property becomes two ($u_{xx}$ + $u_{yy}$)

3. **Forward → Backward → Crank-Nicolson**: Sequential pattern
   - Time derivative: forward (at $t_n$) vs backward (at $t_{n+1}$) vs center (at $t_{n+1/2}$)
   - Spatial: old time level ($n$) vs new time level ($n+1$) vs average

## Common Templates

### Time difference operator property

设:
- $u_j^n$ (网格函数值), $\tau$ (时间步长), $u_j^n = u(x_j, t_n)$ (网格函数与真解的关系)
如果:
- $u(x,t) \in C^2$ (关于 $t$ 具有二阶连续偏导数)
则:
- $u_t(x_j, t_n) = \frac{u_j^{n+1} - u_j^n}{\tau} + O(\tau)$

### Space center difference operator property

设:
- $u_j^n$ (网格函数值), $h$ (空间步长), $u_j^n = u(x_j, t_n)$
如果:
- $u(x,t) \in C^4$ (关于 $x$ 具有四阶连续偏导数)
则:
- $u_{xx}(x_j, t_n) = \frac{u_{j+1}^n - 2u_j^n + u_{j-1}^n}{h^2} + O(h^2)$

### Truncation error

设:
- $(x_j, t_n) \in \mathbb{R}^2$ (二维网格点)
- $u_j^n$ (网格函数值)
如果:
- $R_j^n = O(\tau + h^2)$
则:
- $R_j^n = \frac{u_j^{n+1} - u_j^n}{\tau} - a \frac{u_{j+1}^n - 2u_j^n + u_{j-1}^n}{h^2} - f_j$

## Workflow

```bash
# 1. Find all empty addcontentsline entries
grep -n "addcontentsline.*subsubsection" *.tex | grep -v '\$'

# 2. Find empty customproblem templates (empty \item)
grep -n '\\item\s*$' *.tex | grep -B5 '\\customproblem'

# 3. Find empty := expressions
grep -n '\$:=' *.tex

# 4. For each empty template, find the matching filled template
#    in a sibling file and adapt
```
