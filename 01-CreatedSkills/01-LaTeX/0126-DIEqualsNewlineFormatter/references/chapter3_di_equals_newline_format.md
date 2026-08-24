# Chapter3_DI.tex 长等式按等号换行（参考）

目标：在展示公式里，遇到长等式链时，把每个顶层 `=` 单独放在一行（表达式一行、`=` 一行、表达式一行……），保持其他排版（如矩阵环境）不变。

## 参考片段（Chapter3_DI.tex：2417–2432）

```tex
\[
    \omega
    =
    \begin{bmatrix}
        1 \\ 2 \\ 1
    \end{bmatrix}
    \begin{bmatrix}
        1 & 2 & 1
    \end{bmatrix}
    =
    \begin{bmatrix}
        1 & 2 & 1 \\
        2 & 4 & 2 \\
        1 & 2 & 1
    \end{bmatrix}
\]
```

## 强约束

1. `=` 独占一行，并使用与相邻表达式相同的缩进层级。
2. 不改变数学内容：仅调整换行/空白。
3. 不打乱子环境内部格式（如 `bmatrix` 的行列布局）。

