# IBI reference

## Mesh sizing

At 96 CSS dpi, **1 inch ≈ 96 px**. For a page `W×H`:

```text
cols = ceil(W / 96)
rows = ceil(H / 96)
cell id = r{row}-c{col}  # 0-based, row-major
```

Cycle 2 uses a fixed **4×4 = 16** equal rectangles over the same page box.

## Hardcode pack shape

`hardcoded/00001/page.json`:

```json
{
  "id": 1,
  "path": "index.html",
  "controls": [{"label": "Search Compatible Tyres", "kind": "button", "use": "search_catalog"}],
  "apis": [{"method": "GET", "path": "/api/suggest"}]
}
```

## Evidence per cell

`cycles/cycle-01-1x1/page-00001/cell-r0-c0.md` must include:

- What is visible
- Backend designed/built
- Verification steps + result
- Proof PNG path

## Stop law

`ibi_runner.py` returns `STOP_ALLOWED` only when page statuses are Done. Agent must still confirm Excel `IBI-TRACKER.xlsx` shows Done for every Page ID × required Cycle.
