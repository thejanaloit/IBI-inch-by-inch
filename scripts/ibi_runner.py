#!/usr/bin/env python3
"""
One-by-one IBI driver: prints the next incomplete page/cell work item.
Does not mark Done — agent updates Excel + cell MD after real verify.
Stop only when every page Status is Done for required cycles.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def mesh_cells(mode: str) -> list[str]:
    if mode in ("1x1", "cycle-01", "c1"):
        # Placeholder: agent must measure page and expand; seed a coarse first strip
        # Real cell ids are written after screenshot measure. Seed r0-c0 as start.
        return ["r0-c0"]
    if mode in ("16", "16cell", "cycle-02", "c2"):
        return [f"r{r}-c{c}" for r in range(4) for c in range(4)]
    raise SystemExit(f"unknown mesh mode: {mode}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--cycle", default="cycle-01-1x1")
    ap.add_argument("--mesh", default="1x1", help="1x1 | 16cell")
    args = ap.parse_args()
    run = Path(args.run_dir)
    idx = json.loads((run / "pages-index.json").read_text(encoding="utf-8"))
    pages = idx.get("pages") or []
    cells = mesh_cells(args.mesh)

    next_item = None
    for p in pages:
        hid = p["id"]
        hard = run / "hardcoded" / f"{hid:05d}" / "page.json"
        if not hard.is_file():
            next_item = {"action": "HARDCODE", "page_id": hid, "path": p.get("path"), "url": p.get("url")}
            break
        cdir = run / "cycles" / args.cycle / f"page-{hid:05d}"
        for cell in cells:
            md = cdir / f"cell-{cell}.md"
            if not md.is_file():
                next_item = {
                    "action": "CELL",
                    "page_id": hid,
                    "cell": cell,
                    "path": p.get("path"),
                    "url": p.get("url"),
                    "cycle": args.cycle,
                    "out": str(md),
                }
                break
        if next_item:
            break

    if not next_item:
        # Check page-level done flags in index
        unfinished = [p for p in pages if (p.get("status") or "").upper() != "DONE"]
        if unfinished:
            next_item = {
                "action": "MARK_PAGE_DONE_OR_EXPAND_MESH",
                "hint": "All seeded cells have MD — expand 1x1 mesh from real page size, or set page status Done in Excel/index",
                "unfinished_page_ids": [p["id"] for p in unfinished[:20]],
                "unfinished_count": len(unfinished),
            }
        else:
            next_item = {"action": "STOP_ALLOWED", "message": "All pages Done for this cycle seed — confirm Excel Done"}

    print(json.dumps(next_item, indent=2))


if __name__ == "__main__":
    main()
