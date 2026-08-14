#!/usr/bin/env python3
import argparse
from pathlib import Path

PKG = r"""\usepackage{amsmath,amssymb,amsthm}
\usepackage{xcolor}
\usepackage{tcolorbox}
\usepackage{hyperref}
"""

ENV = r"""\newcommand{\customproblem}[2]{\subsubsection*{#1}#2}
"""

MAIN = r"""\documentclass[a4paper]{article}
\input{Set/Package_set.tex}
\input{Set/Environment_set.tex}
\begin{document}

% 标题部分
\begin{center}
    {\Huge \textbf{%TITLE%}} \\
\end{center}

\setcounter{tocdepth}{3}
\tableofcontents
\newpage

\end{document}
"""


def main() -> int:
    p = argparse.ArgumentParser(description="Create section tex scaffold under a Notes-like directory.")
    p.add_argument("--base", required=True, help="Base path, e.g. .../Notes")
    p.add_argument("--section-name", required=True, help="Section folder name")
    p.add_argument("--main-tex", required=True, help="Main tex filename")
    p.add_argument("--title", default="Section Notes")
    args = p.parse_args()

    section_dir = Path(args.base) / args.section_name
    set_dir = section_dir / "Set"
    set_dir.mkdir(parents=True, exist_ok=True)

    (set_dir / "Package_set.tex").write_text(PKG, encoding="utf-8")
    (set_dir / "Environment_set.tex").write_text(ENV, encoding="utf-8")
    (section_dir / args.main_tex).write_text(MAIN.replace("%TITLE%", args.title), encoding="utf-8")

    print(section_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
