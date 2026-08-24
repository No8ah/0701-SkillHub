#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys


BEGIN_RE = re.compile(r"\\begin\{([^}]*)\}")
END_RE = re.compile(r"\\end\{([^}]*)\}")


def split_top_level_equals(s: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    brace_depth = 0
    env_stack: list[str] = []
    i = 0
    while i < len(s):
        if s[i] == "\\":
            m_begin = BEGIN_RE.match(s, i)
            if m_begin:
                env_stack.append(m_begin.group(1))
                token = m_begin.group(0)
                buf.append(token)
                i += len(token)
                continue
            m_end = END_RE.match(s, i)
            if m_end:
                if env_stack and env_stack[-1] == m_end.group(1):
                    env_stack.pop()
                token = m_end.group(0)
                buf.append(token)
                i += len(token)
                continue
            if i + 1 < len(s):
                buf.append(s[i : i + 2])
                i += 2
                continue

        ch = s[i]
        if ch == "{":
            brace_depth += 1
        elif ch == "}":
            brace_depth = max(0, brace_depth - 1)

        if ch == "=" and brace_depth == 0 and not env_stack:
            parts.append("".join(buf))
            buf = []
            i += 1
            continue

        buf.append(ch)
        i += 1

    parts.append("".join(buf))
    return parts


def normalize_whitespace(s: str) -> str:
    # Keep internal newlines (e.g. bmatrix) as-is; only trim outside.
    return s.strip()


def format_chain(parts: list[str], indent: str) -> str:
    parts = [normalize_whitespace(p) for p in parts if normalize_whitespace(p)]
    if not parts:
        return ""
    out: list[str] = [f"{indent}{parts[0]}"]
    for p in parts[1:]:
        out.append(f"{indent}=")
        out.append(f"{indent}{p}")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Format a long LaTeX equality chain so each top-level '=' is on its own line (DI style)."
    )
    parser.add_argument(
        "--wrap",
        action="store_true",
        help="Wrap output in \\[ ... \\] with a 4-space inner indent.",
    )
    parser.add_argument(
        "--indent",
        default="    ",
        help="Indent used for each line inside the display math block (default: 4 spaces).",
    )
    args = parser.parse_args(argv)

    src = sys.stdin.read()
    src = src.strip("\n")

    parts = split_top_level_equals(src)
    body = format_chain(parts, args.indent)

    if args.wrap:
        print("\\[")
        if body:
            print(body)
        print("\\]")
    else:
        print(body)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
