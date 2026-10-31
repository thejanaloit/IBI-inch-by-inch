#!/usr/bin/env python3
"""Create mandatory hardcoded/<id>/ pack skeleton for a page."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--page-id", type=int, required=True)
    args = ap.parse_args()
    run = Path(args.run_dir)
    idx = json.loads((run / "pages-index.json").read_text(encoding="utf-8"))
    page = next((p for p in idx["pages"] if int(p["id"]) == args.page_id), None)
    if not page:
        raise SystemExit(f"page id {args.page_id} not in index")
    d = run / "hardcoded" / f"{args.page_id:05d}"
    d.mkdir(parents=True, exist_ok=True)
    page_json = {
        "id": args.page_id,
        "path": page.get("path"),
        "url": page.get("url"),
        "title": page.get("title"),
        "controls": [],
        "apis": [],
        "hardcoded": True,
        "notes": "Fill controls/apis before Cycle 1 cells. Soft wiring only after this pack is real.",
    }
    (d / "page.json").write_text(json.dumps(page_json, indent=2), encoding="utf-8")
    (d / "fixtures.json").write_text(
        json.dumps({"currency": "LKR", "locale": "si-LK / en-LK", "samples": []}, indent=2),
        encoding="utf-8",
    )
    (d / "backend-stubs.md").write_text(
        f"# Backend stubs — page {args.page_id}\n\n- List endpoints + payload shapes (hardcoded first).\n",
        encoding="utf-8",
    )
    page["hardcoded"] = True
    (run / "pages-index.json").write_text(json.dumps(idx, indent=2), encoding="utf-8")
    print(f"wrote {d}")


if __name__ == "__main__":
    main()
