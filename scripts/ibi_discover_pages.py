#!/usr/bin/env python3
"""Build pages-index.json from a local mirror or a start URL list file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse


def collect_from_mirror(mirror: Path) -> list[dict]:
    pages: list[dict] = []
    for p in sorted(mirror.rglob("*.html")):
        rel = p.relative_to(mirror).as_posix()
        pages.append(
            {
                "path": rel,
                "url": "/" + rel.replace("index.html", "").rstrip("/") + ("/" if rel.endswith("index.html") else ""),
                "title": p.stem,
                "file": str(p),
            }
        )
    return pages


def collect_from_url_file(path: Path, base: str) -> list[dict]:
    pages = []
    for line in path.read_text(encoding="utf-8").splitlines():
        u = line.strip()
        if not u or u.startswith("#"):
            continue
        full = urljoin(base, u)
        path_part = urlparse(full).path or "/"
        pages.append({"path": path_part.lstrip("/"), "url": full, "title": path_part, "file": None})
    return pages


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True, help="ibi-runs/<site>")
    ap.add_argument("--mirror", default="mirror")
    ap.add_argument("--url-list", default="", help="optional text file of paths/URLs")
    ap.add_argument("--base-url", default="")
    args = ap.parse_args()
    run = Path(args.run_dir)
    run.mkdir(parents=True, exist_ok=True)
    mirror = run / args.mirror
    if args.url_list:
        raw = collect_from_url_file(Path(args.url_list), args.base_url or "http://127.0.0.1/")
    else:
        if not mirror.is_dir():
            raise SystemExit(f"mirror missing: {mirror}")
        raw = collect_from_mirror(mirror)
    index = []
    for i, row in enumerate(raw, start=1):
        index.append(
            {
                "id": i,
                "path": row["path"],
                "url": row["url"],
                "title": row.get("title") or row["path"],
                "file": row.get("file"),
                "status": "TODO",
                "hardcoded": False,
            }
        )
    out = run / "pages-index.json"
    out.write_text(json.dumps({"page_count": len(index), "pages": index}, indent=2), encoding="utf-8")
    print(f"wrote {out} count={len(index)}")


if __name__ == "__main__":
    main()
