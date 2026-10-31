#!/usr/bin/env python3
"""Given page width/height in CSS px, emit 1x1-inch or 16-cell mesh plan (96 dpi default)."""
from __future__ import annotations

import argparse
import json
import math


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=float, required=True, help="page width CSS px")
    ap.add_argument("--height", type=float, required=True, help="page height CSS px")
    ap.add_argument("--dpi", type=float, default=96.0)
    ap.add_argument("--mode", choices=["1x1", "16cell"], default="1x1")
    args = ap.parse_args()
    if args.mode == "16cell":
        cols, rows = 4, 4
        cw, ch = args.width / cols, args.height / rows
    else:
        inch = args.dpi
        cols = max(1, math.ceil(args.width / inch))
        rows = max(1, math.ceil(args.height / inch))
        cw = ch = inch
    cells = []
    for r in range(rows):
        for c in range(cols):
            cells.append(
                {
                    "id": f"r{r}-c{c}",
                    "x": round(c * cw, 2),
                    "y": round(r * ch, 2),
                    "w": round(min(cw, args.width - c * cw), 2),
                    "h": round(min(ch, args.height - r * ch), 2),
                }
            )
    print(json.dumps({"mode": args.mode, "rows": rows, "cols": cols, "cell_count": len(cells), "cells": cells}, indent=2))


if __name__ == "__main__":
    main()
