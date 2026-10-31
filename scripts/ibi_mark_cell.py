#!/usr/bin/env python3
"""Append/update a cell evidence MD and optionally set page status in pages-index.json."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--page-id", type=int, required=True)
    ap.add_argument("--cycle", default="cycle-01-1x1")
    ap.add_argument("--cell", required=True, help="e.g. r0-c0")
    ap.add_argument("--what", default="")
    ap.add_argument("--backend", default="")
    ap.add_argument("--verified", choices=["Y", "N", "N/A"], default="N")
    ap.add_argument("--proof", default="")
    ap.add_argument("--page-status", default="", help="TODO|IN_PROGRESS|PASS|Done")
    args = ap.parse_args()
    run = Path(args.run_dir)
    cdir = run / "cycles" / args.cycle / f"page-{args.page_id:05d}"
    cdir.mkdir(parents=True, exist_ok=True)
    md = cdir / f"cell-{args.cell}.md"
    body = "\n".join(
        [
            f"# Page {args.page_id} · {args.cycle} · {args.cell}",
            "",
            f"- When: {datetime.now(timezone.utc).isoformat()}",
            f"- What is in cell: {args.what}",
            f"- Backend built: {args.backend}",
            f"- Verified?: {args.verified}",
            f"- Proof: {args.proof}",
            "",
        ]
    )
    md.write_text(body, encoding="utf-8")
    print(f"wrote {md}")

    if args.page_status:
        idx_path = run / "pages-index.json"
        data = json.loads(idx_path.read_text(encoding="utf-8"))
        for p in data.get("pages") or []:
            if int(p["id"]) == args.page_id:
                p["status"] = args.page_status
                break
        idx_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"pages-index page {args.page_id} status={args.page_status}")


if __name__ == "__main__":
    main()
