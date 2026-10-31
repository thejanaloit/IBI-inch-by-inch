# Minimal IBI run (local HTML folder)

```bash
# 1) Create run dir + put pages in mirror/
mkdir -p ibi-runs/demo/mirror
# copy *.html into mirror/

# 2) Index
python scripts/ibi_discover_pages.py --run-dir ibi-runs/demo

# 3) Excel
python scripts/ibi_init_excel.py --run-dir ibi-runs/demo

# 4) Local host metadata (+ optional --start)
python scripts/ibi_local_serve.py --run-dir ibi-runs/demo --port 8765

# 5) Next work item
python scripts/ibi_runner.py --run-dir ibi-runs/demo --cycle cycle-01-1x1 --mesh 1x1

# 6) After hardcode gate
python scripts/ibi_hardcode_stub.py --run-dir ibi-runs/demo --page-id 1

# 7) Mesh plan from measured page size (example 1280x2400)
python scripts/ibi_mesh_plan.py --width 1280 --height 2400 --mode 1x1

# 8) Mark a cell after verify
python scripts/ibi_mark_cell.py --run-dir ibi-runs/demo --page-id 1 --cell r0-c0 \
  --what "hero CTA" --backend "POST /api/leads" --verified Y --proof proof/r0-c0.png
```

Stop only when `ibi_runner.py` returns `STOP_ALLOWED` **and** Excel Status=Done for all pages × cycles.
