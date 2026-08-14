# Chapter3_DI.tex “添加 $\star$” 格式参考

目标：当需要给某个“补充 - 定义 …”目录项/标题做星标时，在**可见标题字符串**中把 `定义 -` 写成 `定义 $\star$ -`；不要修改 `\label{...}`。

## 参考片段（Chapter3_DI.tex：约 2652 行附近）

```tex
\customproblem{补充 - 定义 - Content - 外积下的可分离核}{
    ...
}

\addcontentsline{toc}{subsubsection}{补充 - 定义 $\star$ - Content - 外积下的可分离核 - $W = \boldsymbol{a}\boldsymbol{b}^{T}$}

\phantomsection\label{def:<DI>:<chap3>:<补充 - 定义 - Content - 外积下的可分离核>}
```

## 强约束

1. 星标只出现在“可见标题/目录项”的字符串中（如 `\addcontentsline` 的第三个参数）。
2. `\phantomsection\label{...}` 的内容保持不变（即使标题有 `$\star$`，label 也不加星标）。
3. 保留两侧空格：`定义␠$\star$␠-`。

