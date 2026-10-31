#!/usr/bin/env python3
"""Minimal IBI MCP server (stdio JSON-RPC style tools via mcp package if present)."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("pip install mcp", file=sys.stderr)
    raise

mcp = FastMCP("ibi-inch-by-inch")
ROOT = Path(__file__).resolve().parents[1]

@mcp.tool()
def ibi_status(run_dir: str) -> str:
    """Return pages-index + STATUS for an IBI run directory."""
    run = Path(run_dir)
    idx = json.loads((run / "pages-index.json").read_text(encoding="utf-8")) if (run / "pages-index.json").is_file() else {}
    pages = idx.get("pages") or []
    done = sum(1 for p in pages if str(p.get("status","")).lower()=="done")
    st = (run / "STATUS.md").read_text(encoding="utf-8") if (run / "STATUS.md").is_file() else ""
    return json.dumps({"page_count": idx.get("page_count"), "done": done, "status_md": st[:2000]}, indent=2)

@mcp.tool()
def ibi_next(run_dir: str, cycle: str = "cycle-01-1x1") -> str:
    """Next incomplete work item via ibi_runner.py."""
    script = ROOT / "scripts" / "ibi_runner.py"
    out = subprocess.check_output([sys.executable, str(script), "--run-dir", run_dir, "--cycle", cycle], text=True)
    return out

@mcp.tool()
def ibi_batch(run_dir: str, start_id: int = 1, end_id: int = 10) -> str:
    """Run batch hardcode+mesh for page id range (requires Playwright)."""
    script = Path(run_dir) / "scripts" / "ibi_batch_pages.py"
    if not script.is_file():
        return "missing ibi_batch_pages.py in run-dir/scripts"
    out = subprocess.check_output([sys.executable, str(script), "--run-dir", run_dir, "--start-id", str(start_id), "--end-id", str(end_id)], text=True, timeout=600)
    return out[-4000:]

if __name__ == "__main__":
    mcp.run()
