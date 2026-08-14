#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

PLACEHOLDER_STEP_RE = re.compile(r"^\s*\\hspace\*\{2em\}\s*\\textbf\{Step1:\}\\quad\s*$")

TEMPLATE = r"""
\hspace*{2em} \textbf{Step1:}\quad 对偶单元上的积分守恒关系 - $W(x_{N - \frac{1}{2}}) - W(b) + \int_{x_{N - \frac{1}{2}}}^{x_{N}} q(x) u dx = \int_{x_{N - \frac{1}{2}}}^{x_{N}} f(x) dx$

\hspace*{2em} \textbf{Step2:}\quad Sub2 - 通量函数 - $W(x) = p(x) \frac{du}{dx}$

\hspace*{4em} 1. 因此 - $W(b) = p(b) \frac{du}{dx}\bigg|_{x=b} = -\beta_{0}u(b) - \beta_{1}$

\hspace*{2em} \textbf{Step3:}\quad Sub2 - 右半点通量近似 - $W(x_{N - \frac{1}{2}}) \approx a_{N} \cdot \frac{u_{N} - u_{N-1}}{h_{N}}$

\hspace*{2em} \textbf{Step4:}\quad Sub2 - 反应项有限体积近似 - $\int_{x_{N - \frac{1}{2}}}^{x_N} q(x)u\,dx \approx \frac{h_N}{2} d_N u_N$

\hspace*{2em} \textbf{Step5:}\quad Sub2 - 源项积分重构 - $\int_{x_{N - \frac{1}{2}}}^{x_N} f(x)\,dx = \frac{h_N}{2}\phi_N$

\hspace*{2em} \textbf{Step6:}\quad 网格函数 - $u_N = u(b)$

\hspace*{2em} \textbf{Step7:}\quad 计算处理

\hspace*{4em} 1. 化简 - $a_{N} \frac{u_{N} - u_{N-1}}{h_{N}} + \left(\beta_{0} + \frac{h_N}{2} d_N\right)u_N + \beta_1 - \frac{h_N}{2}\phi_N = 0$

\hspace*{2em} \textbf{Step8:}\quad 定义

\hspace*{4em} 1. 第二对偶单元上的离散守恒方程

\qed
""".strip("\n")


def process(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    changes = 0
    while i < len(lines):
        if PLACEHOLDER_STEP_RE.match(lines[i]):
            out.append(TEMPLATE + "\n")
            changes += 1
            i += 1
            continue
        out.append(lines[i])
        i += 1
    return "".join(out), changes


def main() -> int:
    p = argparse.ArgumentParser(description="Fill tongli derivation placeholder Step1 blocks.")
    p.add_argument("--file", required=True)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()

    path = Path(args.file)
    old = path.read_text(encoding="utf-8")
    new, n = process(old)
    if args.check:
        print(n)
        return 1 if n else 0
    if n:
        path.write_text(new, encoding="utf-8")
    print(n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
