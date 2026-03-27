# Requirements Specification — `render_gantt.py`
### Structured Artifacts Build | 27 March 2026
### Status: Approved

---

## 1. Execution Environment

The script runs inside a **Manus sandbox** (Python 3.11, `matplotlib` pre-installed), invoked by a Manus Project Coach agent via shell command. There is no GUI and no interactive display. The script must write output to a file path only — `plt.show()` must never be called.

---

## 2. Interface

```
python render_gantt.py <path/to/task_register.md> [<path/to/output.png>]
```

- **Argument 1 (required):** Path to a task register Markdown file conforming to `templates/task_register_template.md`.
- **Argument 2 (optional):** Output PNG path. Default: `gantt.png` in the same directory as the input file.

---

## 3. Parsing

- Reads the Markdown table and identifies rows by the `Row Type` column (`PROJECT`, `SUBPROJECT`, `TASK`).
- Only `TASK` rows are rendered as bars.
- `SUBPROJECT` rows provide group labels and date-range bands.
- The `PROJECT` row provides the chart title.
- **RACI inheritance** is resolved at parse time: any blank `Owner (R)` field on a `TASK` row is filled from its parent `SUBPROJECT` row, which in turn inherits from the `PROJECT` row if also blank.
- Column names are matched by header value, not by position, to be robust against column reordering.

---

## 4. Date Handling

| Scenario | Behaviour |
|---|---|
| Both `Start date` and `End date` present | Use as-is |
| `Start date` present, `End date` absent | Calculate `End date` from `Start date` + `Estimated hours` (8-hour working days, Mon–Fri) |
| `Start date` absent, `Dependencies` present | Calculate `Start date` as the working day after the latest `End date` of all dependency tasks; then calculate `End date` as above |
| Neither date nor dependencies present | Render a visible warning label on the chart ("No date — check register"); do not crash |

---

## 5. Visual Output

| Element | Specification |
|---|---|
| **Chart title** | Project name from the `PROJECT` row |
| **Y-axis** | Task names, grouped by sub-project |
| **X-axis** | Date axis, auto-scaled to the full project date range |
| **Sub-project grouping** | A full-width coloured band spanning the sub-project's date range, with the sub-project name as a label (A1 — labelled band) |
| **Task bars** | Full duration shown as a light-coloured bar; filled segment proportional to `% Complete` shown as a darker overlay |
| **Owner label** | Displayed in small text immediately to the right of the bar end (B2) |
| **Status colour** | Not started: grey; In progress: blue; Complete: green; Blocked: red; Cancelled: light grey with hatch |
| **Output format** | PNG, minimum 1600px wide, 150 dpi |

Dependency arrows are not required in this version. Chronological ordering within each sub-project group is sufficient.

---

## 6. Error Handling

| Error condition | Behaviour |
|---|---|
| File not found | Clear error message; exit code 1 |
| Malformed Markdown table (wrong column count) | Print offending row number; exit code 1 |
| Invalid date format | Print offending Task ID and field; skip task; continue |
| `% Complete` out of range | Clamp to 0–100; print warning |
| Unknown `Status` value | Render in grey; print warning |
| Empty task register (no TASK rows) | Print warning; exit code 0 |

---

## 7. Approved Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Sub-project grouping style | A1 — Labelled band | User preference |
| Owner label placement | B2 — Right of bar end | User preference; always visible regardless of bar length |
| Rendering library | `matplotlib` | Pre-installed in Manus sandbox; reliable static PNG; no export toolchain |
| Display mode | `savefig` only — no `plt.show()` | CLI/sandbox execution; no GUI available |

---

*This document was approved by the user before build began. Any deviation from this specification during build must be flagged explicitly.*
