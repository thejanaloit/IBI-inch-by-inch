#!/usr/bin/env python3
"""Write local-host.json and print a static-serve command for the mirror folder."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--mirror", default="mirror")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--start", action="store_true", help="start http.server in foreground")
    args = ap.parse_args()
    run = Path(args.run_dir)
    root = (run / args.mirror).resolve()
    if not root.is_dir():
        raise SystemExit(f"mirror missing: {root}")
    meta = {
        "port": args.port,
        "root": str(root),
        "url": f"http://127.0.0.1:{args.port}/",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "hint": f"python -m http.server {args.port} --directory \"{root}\"",
    }
    out = run / "local-host.json"
    out.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))
    if args.start:
        import os
        import subprocess

        os.chdir(root)
        subprocess.call(["python", "-m", "http.server", str(args.port)])


if __name__ == "__main__":
    main()
