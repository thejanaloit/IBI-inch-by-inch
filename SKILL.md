---
name: ibi-inch-by-inch
description: >-
  IBI (Inch By Inch) — download every page of a given website, host locally,
  hardcode first, index 1..N, then mesh each page (1×1 inch then 16 cells) and
  wire/verify backend per cell until an Excel tracker marks every page Done.
  Use when the user says IBI, inch by inch, mesh page backend, or full site
  page-by-page functionality build with Excel completion gates.
disable-model-invocation: true
---

# IBI — Inch By Inch (web → local → mesh → backend → Excel Done)

Locked method. Do **not** skip phases. Do **not** stop until every cycle and every page is **Done** in the Excel workbook.

## Owner method (verbatim intent)

1. User gives any website / webpage.
2. Agent **first downloads every web page** of that site and **hosts locally**.
3. Build a **scripted one-by-one runner** that scales to thousands of pages (e.g. 10,000).
4. **Hardcode is mandatory** before soft/dynamic wiring.
5. **Index** every page `1, 2, 3, 4, 5, 6…`.
6. Take page **1**. Treat the page as large. Split into a **1×1 inch mesh** (grid).
7. Enter **cell 1** of that mesh → read content → **design + build backend** for that cell → **verify** (enter data / exercise controls).
8. Move to cell **2**, same work — continue until **every** 1×1 cell on the page is done.
9. That is **Cycle 1** for that page. Repeat Cycle 1 across **all** indexed pages (scripted order).
10. Later cycles: take each page again, split into **16 cells**, walk cell-by-cell, re-check functionality.
11. Maintain one **Excel** with **every** page. Tick fully functional only with evidence.
12. After all rounds execute, Excel shows **Done**. Runner may stop **only** when every cycle × every page is Done.

## When to use

- User says: IBI / inch by inch / mesh backend / page-by-page wire
- Full-site clone + backend adoption (Thushara, TyreDekho adapt, any URL)
- “Don’t stop until every button/section works”

## Artifacts (workspace contract)

Create under the active project (or `ibi-runs/<site-slug>/`):

```
ibi-runs/<site>/
  mirror/                 # downloaded HTML/CSS/JS/assets
  local-host.json         # port, root, started_at
  pages-index.json        # [{id, path, url, title, status}]
  hardcoded/              # mandatory hardcode packs per page/cell
  cycles/
    cycle-01-1x1/         # per-page cell logs + evidence
    cycle-02-16cell/
    cycle-NN-.../
  excel/
    IBI-TRACKER.xlsx      # ALL pages × ALL cycles
  scripts/                # generated runner for this site
```

## Phase 0 — Ingest (compulsory)

1. Resolve base URL (or local folder).
2. Crawl / sitemap / link discovery until **no unvisited in-site page** remains.
3. Download every page + assets into `mirror/`.
4. Serve locally (`npx serve`, CMS static, or project script). Record `local-host.json`.
5. Refuse to start Cycle 1 until local host smoke returns 200 for page id=1.

Script helpers (this skill):

- `scripts/ibi_discover_pages.py` — build `pages-index.json`
- `scripts/ibi_local_serve.py` — hint / start static serve
- `scripts/ibi_init_excel.py` — create tracker workbook
- `scripts/ibi_hardcode_stub.py` — mandatory hardcode pack skeleton
- `scripts/ibi_mesh_plan.py` — 1×1 or 16-cell mesh from measured page size
- `scripts/ibi_mark_cell.py` — mark cell/page cycle status
- `scripts/ibi_runner.py` — one-by-one page/cell driver (gate on Excel)

## Phase 1 — Index + hardcode (compulsory)

1. Write `pages-index.json` with sequential `id` starting at 1.
2. For each page, create `hardcoded/<id>/` with:
   - `page.json` — slug, title, controls inventory (buttons, forms, links)
   - `fixtures.json` — sample LKR/SL data if Thushara; never invent secrets
   - `backend-stubs.md` — endpoint names + payload shapes (hardcoded first)
3. **Hardcode gate:** no Cycle 1 cell work until hardcoded pack exists for that page id.

## Phase 2 — Cycle 1 (1×1 inch mesh)

For page `id` in order `1..N` (scripted; never random):

1. Open the **local** page (headed browser preferred).
2. Capture full viewport / full page screenshot.
3. Compute mesh: divide the **rendered page box** into **1×1 inch** cells (CSS px ≈ `96×96` at 96dpi; if DPI differs, use `inch * devicePixelsPerInch`). Label cells `r{row}-c{col}` left→right, top→bottom.
4. For each cell in order:
   - Focus / crop evidence for that cell
   - Inventory interactive + data content in the cell
   - Design backend for that content (API/route/table/lead/search/nav)
   - **Hardcode** behaviour first, then wire live BFF if available
   - Verify: click/type/submit; prove request or local state change
   - Write `cycles/cycle-01-1x1/page-<id>/cell-<r>-<c>.md` + proof PNG
   - Update Excel row for that page/cell → `PASS` only with proof path
5. Page Cycle 1 complete only when **every** cell is PASS (or `N/A` with written reason: empty/decorative).

## Phase 3 — Later cycles (16-cell + full-page tick)

1. **Cycle 2:** same pages, mesh = **16 equal cells** (4×4). Re-walk every cell; regression-check Cycle 1 backends.
2. Optional further cycles (owner may add): smaller mesh, mobile viewport, RBAC, empty/error.
3. After required cycles: for each page, set Excel **Fully functional** tick only if all cells in all required cycles are PASS/N/A.
4. When every page Fully functional → set workbook status **Done**.

## Excel tracker (locked columns)

Workbook: `excel/IBI-TRACKER.xlsx`

| Column | Meaning |
|--------|---------|
| Page ID | 1..N |
| Path / URL | local path + original URL |
| Title | page title |
| Hardcoded? | Y/N |
| Cycle | e.g. C1-1x1, C2-16 |
| Cell | r0-c0 … |
| What is in cell | short English |
| Backend built | endpoint / module |
| Verified? | Y/N |
| Proof | PNG/MD path |
| Page fully functional | tick after all cells/cycles |
| Status | TODO / IN_PROGRESS / PASS / N/A / Done |

**Stop rule:** do not declare the run finished until Status=Done for every Page ID and every required Cycle.

## Thushara / Sri Lanka locks (when site is Thushara)

- Currency **LKR** only — never ₹ / INR
- Market Sri Lanka (Middeniya)
- Prefer ERP/CMS `list_price` / live-stock; else “See LKR price in stock”
- Adopt existing PHP/MySQL backend when that is the product decision — do not replace backend for UI-only rebuilds

## Anti-patterns (forbidden)

- Skipping download/local host and working only on remote live URLs for Cycle 1
- Soft/dynamic-only wiring before hardcode pack
- Jumping to page 500 before page 1 mesh is complete (unless owner explicitly reorders index)
- Marking Excel PASS without proof path
- Stopping after “most pages” or “main CTAs only”

## Agent checklist (every turn)

1. Show current page id / cell / cycle from Excel
2. Do only the next incomplete cell (or finish hardcode gate)
3. Write evidence + Excel update
4. Advance via `ibi_runner.py` / status — never skip

## Sinhala (short)

Site එකක් දුන්නාම මුලින්ම හැම page එකම download කරලා local host. ඊට පස්සේ pages index (1,2,3…). Hardcode අනිවාර්යයි. Page 1 ගෙන 1×1 inch mesh — එක එක කොටසට content බලලා backend හදලා verify. හැම කොටසම. ඊට පස්සේ හැම page. ඊළඟ cycle: 16 කොටස්. Excel එකේ හැම page ටික්. Stop කරන්න පුළුවන් හැම cycle / හැම page Done උනාට පස්සේ විතරයි.
