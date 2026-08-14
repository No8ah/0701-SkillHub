- 之前

\documentclass[../Chapter6_OM_Hw_共轭梯度法.tex]{subfiles}
\begin{document}

\customproblem{第6次作业 - Exercise 3}{

Let the matrix $\boldsymbol{A}\in\mathbb{R}^{n\times n}$ be symmetric positive definite, and let the vectors $\boldsymbol{d}_{1},\boldsymbol{d}_{2},\ldots,\boldsymbol{d}_{n}$ be conjugate with respect to $\boldsymbol{A}$. Prove:
}

\addcontentsline{toc}{subsubsection}{第6次作业 - Exercise 3 - 向量关于 $\boldsymbol{A}$ 共轭 - $\surd$}

\phantomsection\label{prob:<OM>:<HW6>:<第6次作业 - Exercise 3>}

    \textbf{简明思路:}

\begin{enumerate}

    \item[(a)] For any $\boldsymbol{x}\in\mathbb{R}^{n}$,
    \[
        \boldsymbol{x} = \sum_{i=1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}.
    \]

        \begin{enumerate}
        
            \item $\{\boldsymbol{d}_{1}, \cdots, \boldsymbol{d}_{n}\}$ 是 $\mathbb{R}^{n}$ 下的一组基
            
            \begin{tcolorbox}
            
                \textbf{Step1:}\quad 考虑 - $\sum\limits_{i = 1}^{n}c_{i}\boldsymbol{d}_{i} = \boldsymbol{0}$

                    \hspace*{2em} 1. 其中 - $c_{1}, \cdots, c_{n} \in \mathbb{R}$

                \textbf{Step2:}\quad $Fixed\ j$\ , \ 同左乘 $\boldsymbol{d}_{j}^{T}\boldsymbol{A}$

                    \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A} \sum\limits_{i = 1}^{n}c_{i}\boldsymbol{d}_{i}
                    =
                    \boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{0}
                    =
                    \boldsymbol{0}$

                \textbf{Step3:}\quad Chap6\_Sc1 - 向量关于 $\boldsymbol{A}$ 共轭 - $\forall \ i \neq j
                \ , \
                \boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{j} = 0$

                    \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A} \sum\limits_{i = 1}^{n}c_{i}\boldsymbol{d}_{i}
                    =
                    c_{j}\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j}$

                \textbf{Step4:}\quad $\boldsymbol{A}$ 对称正定

                    \hspace*{2em} 1. 因此 - $\forall \ \boldsymbol{d}_{j} \neq \boldsymbol{0}
                    \ , \
                    \boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j} > 0$

                    \hspace*{2em} 2. 进而 - $c_{j} = 0
                    \ , \
                    j = 1, \cdots, n$

                \textbf{Step5:}\quad $Summary$ - $\{\boldsymbol{d}_{1}, \cdots, \boldsymbol{d}_{n}\}$线性无关

                    \hspace*{2em} 1. 因此 - $\{\boldsymbol{d}_{1}, \cdots, \boldsymbol{d}_{n}\}$ 是 $\mathbb{R}^{n}$ 下的一组基

                    \hspace*{2em} 2. 进而 - $\forall \ \boldsymbol{x} \in \mathbb{R}^{n}
                    \ , \
                    \exists \ 1 \ a_{1}, \cdots, a_{n} \in \mathbb{R}
                    \quad S.t. \quad
                    \boldsymbol{x} = \sum\limits_{i = 1}^{n}a_{i}\boldsymbol{d}_{i}$

                \qed
            
            \end{tcolorbox}

            \item 求系数 $a_{i}$
            
            \begin{tcolorbox}
            
                \textbf{Step1:}\quad 考虑 - $\boldsymbol{x} = \sum\limits_{i = 1}^{n}a_{i}\boldsymbol{d}_{i}$

                    \hspace*{2em} 1. 其中 - $a_{1}, \cdots, a_{n} \in \mathbb{R}$
                
                \textbf{Step2:}\quad $Fixed\ j$\ , \ 同左乘 $\boldsymbol{d}_{j}^{T}\boldsymbol{A}$

                    \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{x}
                    =
                    \boldsymbol{d}_{j}^{T}\boldsymbol{A} \sum\limits_{i = 1}^{n}a_{i}\boldsymbol{d}_{i}$

                \textbf{Step3:}\quad Chap6\_Sc1 - 向量关于 $\boldsymbol{A}$ 共轭 - $\forall \ i \neq j
                \ , \
                \boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{j} = 0$

                    \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{x}
                    =
                    a_{j}\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j}$

                \textbf{Step4:}\quad $\boldsymbol{A}$ 对称正定

                    \hspace*{2em} 1. 因此 - $\forall \ \boldsymbol{d}_{j} \neq \boldsymbol{0}
                    \ , \
                    \boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j} > 0$

                    \hspace*{2em} 2. 进而 - $a_{j} = \frac{\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j}}
                    \ , \
                    j = 1, \cdots, n$

                \textbf{Step5:}\quad $Summary$ - $a_{i} 
                =
                \frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}
                \ , \
                i = 1, \cdots, n$
            
            \end{tcolorbox}

            \item $Summary$:\quad $\forall \ \boldsymbol{x} \in \mathbb{R}^{n}
            \ , \
            \boldsymbol{x}
            =
            \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

        \end{enumerate}

    \item[(b)] Could you calculate $\boldsymbol{A}^{-1}\boldsymbol{x}$?

    \begin{tcolorbox}

        \textbf{Step1:}\quad 题目条件 - $\boldsymbol{A}$对称正定

            \hspace*{2em} 1. 因此 - $\boldsymbol{A}^{-1}\ \exists$

        \textbf{Step2:}\quad 假设 - $\boldsymbol{y}
        =
        \boldsymbol{A}^{-1}\boldsymbol{x}$

        \textbf{Step3:}\quad 题目条件 - $\forall \ \boldsymbol{x} \in \mathbb{R}^{n}
        \ , \
        \boldsymbol{x}
        =
        \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

            \hspace*{2em} 1. 因此 - $\boldsymbol{y}
            =
            \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{y}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$
            
            \hspace*{2em} 2. 代入 - $\boldsymbol{A}^{-1}\boldsymbol{x}
            =
            \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\bigl(\boldsymbol{A}^{-1}\boldsymbol{x}\bigr)}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

            \hspace*{2em} 3. 化简 - $\boldsymbol{A}^{-1}\boldsymbol{x}
            =
            \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

        \textbf{Step4:}\quad $Summary$ - $\boldsymbol{A}^{-1}\boldsymbol{x}
        =
        \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

        \qed

    \end{tcolorbox}

\end{enumerate}

\clearpage
\newpage

\end{document}

- 之后

\documentclass[../Chapter6_OM_Hw_共轭梯度法.tex]{subfiles}

    \begin{document}

        %\setcounter{section}{3}
        %\tableofcontents
        %\clearpage
        %\newpage

    \customproblem{第6次作业 - Exercise 3}{

    Let the matrix $\boldsymbol{A}\in\mathbb{R}^{n\times n}$ be symmetric positive definite, and let the vectors $\boldsymbol{d}_{1},\boldsymbol{d}_{2},\ldots,\boldsymbol{d}_{n}$ be conjugate with respect to $\boldsymbol{A}$. Prove:
    }

    \addcontentsline{toc}{subsubsection}{第6次作业 - Exercise 3 - 向量关于 $\boldsymbol{A}$ 共轭 - $\surd$}

    \phantomsection\label{prob:<OM>:<HW6>:<第6次作业 - Exercise 3>}

        \textbf{简明思路:}

    \begin{enumerate}

        \item[(a)] For any $\boldsymbol{x}\in\mathbb{R}^{n}$,
        \[
            \boldsymbol{x} = \sum_{i=1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}.
        \]

            \begin{enumerate}
            
                \item $\{\boldsymbol{d}_{1}, \cdots, \boldsymbol{d}_{n}\}$ 是 $\mathbb{R}^{n}$ 下的一组基
                
                \begin{tcolorbox}
                
                    \textbf{Step1:}\quad 考虑 - $\sum\limits_{i = 1}^{n}c_{i}\boldsymbol{d}_{i} = \boldsymbol{0}$

                        \hspace*{2em} 1. 其中 - $c_{1}, \cdots, c_{n} \in \mathbb{R}$

                    \textbf{Step2:}\quad $Fixed\ j$\ , \ 同左乘 $\boldsymbol{d}_{j}^{T}\boldsymbol{A}$

                        \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A} \sum\limits_{i = 1}^{n}c_{i}\boldsymbol{d}_{i}
                        =
                        \boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{0}
                        =
                        \boldsymbol{0}$

                    \textbf{Step3:}\quad Chap6\_Sc1 - 向量关于 $\boldsymbol{A}$ 共轭 - $\forall \ i \neq j
                    \ , \
                    \boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{j} = 0$

                        \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A} \sum\limits_{i = 1}^{n}c_{i}\boldsymbol{d}_{i}
                        =
                        c_{j}\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j}$

                    \textbf{Step4:}\quad $\boldsymbol{A}$ 对称正定

                        \hspace*{2em} 1. 因此 - $\forall \ \boldsymbol{d}_{j} \neq \boldsymbol{0}
                        \ , \
                        \boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j} > 0$

                        \hspace*{2em} 2. 进而 - $c_{j} = 0
                        \ , \
                        j = 1, \cdots, n$

                    \textbf{Step5:}\quad $Summary$ - $\{\boldsymbol{d}_{1}, \cdots, \boldsymbol{d}_{n}\}$线性无关

                        \hspace*{2em} 1. 因此 - $\{\boldsymbol{d}_{1}, \cdots, \boldsymbol{d}_{n}\}$ 是 $\mathbb{R}^{n}$ 下的一组基

                        \hspace*{2em} 2. 进而 - $\forall \ \boldsymbol{x} \in \mathbb{R}^{n}
                        \ , \
                        \exists \ 1 \ a_{1}, \cdots, a_{n} \in \mathbb{R}
                        \quad S.t. \quad
                        \boldsymbol{x} = \sum\limits_{i = 1}^{n}a_{i}\boldsymbol{d}_{i}$

                    \qed
                
                \end{tcolorbox}

                \item 求系数 $a_{i}$
                
                \begin{tcolorbox}
                
                    \textbf{Step1:}\quad 考虑 - $\boldsymbol{x} = \sum\limits_{i = 1}^{n}a_{i}\boldsymbol{d}_{i}$

                        \hspace*{2em} 1. 其中 - $a_{1}, \cdots, a_{n} \in \mathbb{R}$
                    
                    \textbf{Step2:}\quad $Fixed\ j$\ , \ 同左乘 $\boldsymbol{d}_{j}^{T}\boldsymbol{A}$

                        \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{x}
                        =
                        \boldsymbol{d}_{j}^{T}\boldsymbol{A} \sum\limits_{i = 1}^{n}a_{i}\boldsymbol{d}_{i}$

                    \textbf{Step3:}\quad Chap6\_Sc1 - 向量关于 $\boldsymbol{A}$ 共轭 - $\forall \ i \neq j
                    \ , \
                    \boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{j} = 0$

                        \hspace*{2em} 1. 因此 - $\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{x}
                        =
                        a_{j}\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j}$

                    \textbf{Step4:}\quad $\boldsymbol{A}$ 对称正定

                        \hspace*{2em} 1. 因此 - $\forall \ \boldsymbol{d}_{j} \neq \boldsymbol{0}
                        \ , \
                        \boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j} > 0$

                        \hspace*{2em} 2. 进而 - $a_{j} = \frac{\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{j}^{T}\boldsymbol{A}\boldsymbol{d}_{j}}
                        \ , \
                        j = 1, \cdots, n$

                    \textbf{Step5:}\quad $Summary$ - $a_{i} 
                    =
                    \frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}
                    \ , \
                    i = 1, \cdots, n$
                
                \end{tcolorbox}

                \item $Summary$:\quad $\forall \ \boldsymbol{x} \in \mathbb{R}^{n}
                \ , \
                \boldsymbol{x}
                =
                \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

            \end{enumerate}

        \item[(b)] Could you calculate $\boldsymbol{A}^{-1}\boldsymbol{x}$?

        \begin{tcolorbox}

            \textbf{Step1:}\quad 题目条件 - $\boldsymbol{A}$对称正定

                \hspace*{2em} 1. 因此 - $\boldsymbol{A}^{-1}\ \exists$

            \textbf{Step2:}\quad 假设 - $\boldsymbol{y}
            =
            \boldsymbol{A}^{-1}\boldsymbol{x}$

            \textbf{Step3:}\quad 题目条件 - $\forall \ \boldsymbol{x} \in \mathbb{R}^{n}
            \ , \
            \boldsymbol{x}
            =
            \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

                \hspace*{2em} 1. 因此 - $\boldsymbol{y}
                =
                \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{y}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$
                
                \hspace*{2em} 2. 代入 - $\boldsymbol{A}^{-1}\boldsymbol{x}
                =
                \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\bigl(\boldsymbol{A}^{-1}\boldsymbol{x}\bigr)}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

                \hspace*{2em} 3. 化简 - $\boldsymbol{A}^{-1}\boldsymbol{x}
                =
                \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

            \textbf{Step4:}\quad $Summary$ - $\boldsymbol{A}^{-1}\boldsymbol{x}
            =
            \sum\limits_{i = 1}^{n}\frac{\boldsymbol{d}_{i}^{T}\boldsymbol{x}}{\boldsymbol{d}_{i}^{T}\boldsymbol{A}\boldsymbol{d}_{i}}\boldsymbol{d}_{i}$

            \qed

        \end{tcolorbox}

    \end{enumerate}

    \clearpage
    \newpage

\end{document}
