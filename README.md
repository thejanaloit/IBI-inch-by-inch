# IBI — Inch By Inch

Cursor skill + scripts: download every page of a site → host locally → **hardcode first** → index `1..N` → 1×1 inch mesh per page → design/build/verify backend cell-by-cell → later 16-cell cycle → Excel Done gate.

**Stop only when every cycle × every page is Done.**

## Install (Cursor skill)

Copy or clone this folder to:

- Personal: `~/.cursor/.../AgentStores/.../skills/ibi-inch-by-inch/`
- Or project: `<repo>/.cursor/skills/ibi-inch-by-inch/`

Open `SKILL.md` when the user says **IBI** / **inch by inch**.

## Scripts

| Script | Role |
|--------|------|
| `ibi_discover_pages.py` | Build `pages-index.json` |
| `ibi_init_excel.py` | Create `excel/IBI-TRACKER.xlsx` |
| `ibi_local_serve.py` | Write `local-host.json` / optional serve |
| `ibi_hardcode_stub.py` | Mandatory hardcode pack skeleton |
| `ibi_mesh_plan.py` | 1×1 or 16-cell mesh from page size |
| `ibi_mark_cell.py` | Write cell evidence MD |
| `ibi_runner.py` | Next incomplete HARDCODE / CELL / STOP |

Needs: Python 3.10+, `openpyxl` for Excel init.

## Thushara locks

When the site is Thushara Tyre: **LKR** only, Sri Lanka, adopt PHP/MySQL — see `SKILL.md`.
