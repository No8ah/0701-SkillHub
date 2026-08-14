#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path


FORMATS = ("png", "pdf", "svg")


def candidate_commands():
    for name in ("drawio", "draw.io", "diagrams.net"):
        exe = shutil.which(name)
        if exe:
            yield [exe]

    mac_apps = [
        "/Applications/draw.io.app/Contents/MacOS/draw.io",
        "/Applications/diagrams.net.app/Contents/MacOS/diagrams.net",
        "/Applications/Draw.io.app/Contents/MacOS/draw.io",
    ]
    for p in mac_apps:
        if Path(p).exists():
            yield [p]


def run_export(cmd, src: Path, fmt: str, dst: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*cmd, "--export", "--format", fmt, "--output", str(dst), str(src)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: export_drawio.py <file.drawio>", file=sys.stderr)
        return 2

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"[FAIL] Missing file: {src}", file=sys.stderr)
        return 1

    commands = list(candidate_commands())
    if not commands:
        print("[FAIL] No draw.io/diagrams.net CLI found. Install diagrams.net desktop app or drawio CLI, then rerun.", file=sys.stderr)
        return 1

    last_error = ""
    for cmd in commands:
        ok = True
        for fmt in FORMATS:
            dst = src.with_suffix(f".{fmt}")
            proc = run_export(cmd, src, fmt, dst)
            if proc.returncode != 0 or not dst.exists():
                ok = False
                last_error = (proc.stderr or proc.stdout or "export failed").strip()
                break
        if ok:
            print("[OK] Exported: " + ", ".join(str(src.with_suffix(f'.{fmt}')) for fmt in FORMATS))
            return 0

    print(f"[FAIL] Export command failed: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
