#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_drawio_xml.py <file.drawio>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"[FAIL] Missing file: {path}", file=sys.stderr)
        return 1

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        print(f"[FAIL] XML parse error: {exc}", file=sys.stderr)
        return 1

    root = tree.getroot()
    if root.tag != "mxfile":
        print(f"[FAIL] Root tag is {root.tag!r}, expected 'mxfile'", file=sys.stderr)
        return 1

    graph_models = root.findall(".//mxGraphModel")
    cells = root.findall(".//mxCell")
    if not graph_models:
        print("[FAIL] No mxGraphModel found", file=sys.stderr)
        return 1
    if len(cells) < 3:
        print("[FAIL] Too few mxCell elements for an editable diagram", file=sys.stderr)
        return 1

    print(f"[OK] Valid draw.io XML: {path} ({len(cells)} mxCell elements)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
