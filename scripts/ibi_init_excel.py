#!/usr/bin/env python3
"""Create IBI-TRACKER.xlsx with one row scaffold per page (expand cells as cycles run)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

COLS = [
    "Page ID",
    "Path / URL",
    "Title",
    "Hardcoded?",
    "Cycle",
    "Cell",
    "What is in cell",
    "Backend built",
    "Verified?",
    "Proof",
    "Page fully functional",
    "Status",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run = Path(args.run_dir)
    idx_path = run / "pages-index.json"
    if not idx_path.is_file():
        raise SystemExit("pages-index.json missing — run ibi_discover_pages.py first")
    data = json.loads(idx_path.read_text(encoding="utf-8"))
    pages = data.get("pages") or []
    try:
        from openpyxl import Workbook
    except ImportError as e:
        raise SystemExit("pip install openpyxl") from e

    wb = Workbook()
    ws = wb.active
    ws.title = "IBI"
    ws.append(COLS)
    for p in pages:
        ws.append(
            [
                p["id"],
                p.get("url") or p.get("path"),
                p.get("title"),
                "N",
                "",
                "",
                "",
                "",
                "N",
                "",
                "N",
                "TODO",
            ]
        )
    xdir = run / "excel"
    xdir.mkdir(parents=True, exist_ok=True)
    out = xdir / "IBI-TRACKER.xlsx"
    wb.save(out)
    print(f"wrote {out} rows={len(pages)}")


if __name__ == "__main__":
    main()
