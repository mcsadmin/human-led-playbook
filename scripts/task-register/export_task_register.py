"""
export_task_register.py  (v3 — direct-colour Gantt)

Reads docs/task_register.md and produces:
  1. docs/task_register.csv           — flat CSV of all TASK rows
  2. docs/task_register_gantt.xlsx    — two-sheet workbook:
       Sheet 1 "Task Register"  — editable data table (source of truth)
       Sheet 2 "Gantt"          — Gantt chart with bars painted directly
                                   in the correct sub-project colour

Bar logic: cells are painted directly in Python — no Excel formulas or
conditional formatting required, so the chart renders in all spreadsheet apps.
To refresh after editing Sheet 1, re-run this script.
"""

import csv
import re
from datetime import date, timedelta
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

REGISTER_PATH = Path("docs/task_register.md")
CSV_PATH      = Path("docs/task_register.csv")
XLSX_PATH     = Path("docs/task_register_gantt.xlsx")

HEADERS = [
    "Row Type", "Task ID", "Sub-project", "Task name",
    "Owner (R)", "Accountable (A)", "Consulted (C)", "Informed (I)",
    "Dependencies", "Estimated hours", "Start date", "End date",
    "% Complete", "Status", "Sprint",
]

SUBPROJECTS = [
    ("SP01", "CRM Setup and Pipelines",             "4472C4", "D9E1F2"),
    ("SP02", "Email Integration",                   "70AD47", "E2EFDA"),
    ("SP03", "Ticketing and Helpdesk Integration",  "FFC000", "FFF2CC"),
    ("SP04", "Platform-to-Odoo Integration",        "ED7D31", "FCE4D6"),
    ("SP05", "CRM Training and Adoption",           "A5A5A5", "EDEDED"),
    ("SP06", "Analytics and Reporting",             "5B9BD5", "DDEBF7"),
    ("SP07", "Helpdesk Training",                   "9E4FCC", "F4CCFF"),
]
SP_BAR   = {name: bar  for _, name, bar, _    in SUBPROJECTS}
SP_LIGHT = {name: lite for _, name, _,   lite in SUBPROJECTS}

SPRINT_LIGHT = {
    "Sprint 1": "DEEAF1", "Sprint 2": "E2EFDA", "Sprint 3": "FFF2CC",
    "Sprint 4": "FCE4D6", "Sprint 5": "EDEDED", "Sprint 6": "F4CCFF",
}

def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)

def bdr(color="CCCCCC"):
    s = Side(style="thin", color=color)
    return Border(left=s, right=s, top=s, bottom=s)

def parse_md_table(path):
    rows, in_table = [], False
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("| Row Type"):
            in_table = True; continue
        if in_table and re.match(r"^\|[-| ]+\|$", line):
            continue
        if in_table and line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            # Accept 15-column (planning-only) or 18-column (with coaching fields) rows
            if len(cells) >= len(HEADERS):
                rows.append(dict(zip(HEADERS, cells[:len(HEADERS)])))
        elif in_table and not line.startswith("|"):
            break
    return rows

all_rows  = parse_md_table(REGISTER_PATH)
task_rows = [r for r in all_rows if r["Row Type"] == "TASK"]

# 1. CSV
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=HEADERS)
    writer.writeheader()
    writer.writerows(task_rows)
print(f"CSV written: {CSV_PATH}  ({len(task_rows)} task rows)")

# 2. XLSX
wb = openpyxl.Workbook()

# ── Sheet 1: Task Register ──────────────────────────────────────────────────
ws1 = wb.active
ws1.title = "Task Register"

HDR_FILL = fill("1F3864")
HDR_FONT = Font(bold=True, color="FFFFFF", size=10)

col_widths = [12, 8, 30, 44, 10, 14, 22, 12, 14, 10, 12, 12, 10, 12, 10]
for ci, (h, w) in enumerate(zip(HEADERS, col_widths), start=1):
    c = ws1.cell(row=1, column=ci, value=h)
    c.fill = HDR_FILL; c.font = HDR_FONT
    c.alignment = Alignment(horizontal="center", wrap_text=True)
    c.border = bdr()
    ws1.column_dimensions[get_column_letter(ci)].width = w
ws1.row_dimensions[1].height = 30

for ri, row in enumerate(task_rows, start=2):
    sp   = row["Sub-project"]
    rfill = fill(SP_LIGHT.get(sp, "FFFFFF"))
    for ci, h in enumerate(HEADERS, start=1):
        val = row[h]
        if h in ("Start date", "End date") and val:
            try:
                val = date.fromisoformat(val)
            except ValueError:
                pass
        c = ws1.cell(row=ri, column=ci, value=val)
        c.fill = rfill; c.border = bdr()
        c.alignment = Alignment(vertical="center", wrap_text=(ci in (4, 7, 8)))
        c.font = Font(size=9)
        if isinstance(val, date):
            c.number_format = "DD-MMM-YY"

ws1.freeze_panes = "A2"
ws1.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}1"

# ── Sheet 2: Gantt (direct-colour) ─────────────────────────────────────────
ws2 = wb.create_sheet("Gantt")

# Derive timeline bounds from the actual task dates (no blank leading columns)
task_dates = []
for r in task_rows:
    for field in ("Start date", "End date"):
        try:
            task_dates.append(date.fromisoformat(r[field]))
        except (ValueError, TypeError):
            pass

if task_dates:
    earliest = min(task_dates)
    latest   = max(task_dates)
    # Snap to the Monday on or before the earliest task start
    GANTT_START = earliest - timedelta(days=earliest.weekday())
    # Extend to the Sunday on or after the latest task end, then to next Monday
    GANTT_END = latest + timedelta(days=(6 - latest.weekday()))
else:
    GANTT_START = date.today() - timedelta(days=date.today().weekday())
    GANTT_END   = GANTT_START + timedelta(weeks=12)

mondays = []
d = GANTT_START
while d <= GANTT_END:
    mondays.append(d)
    d += timedelta(weeks=1)

FIXED_COLS   = 5
WEEK_START_C = FIXED_COLS + 1
TOTAL_COLS   = FIXED_COLS + len(mondays)

GANTT_HDR_FILL = fill("1F3864")
GANTT_HDR_FONT = Font(bold=True, color="FFFFFF", size=9)

# Row 1: month labels
month_groups = {}
for wi, mon in enumerate(mondays):
    month_groups.setdefault(mon.strftime("%b %Y"), []).append(WEEK_START_C + wi)

for month_key, cols in month_groups.items():
    sc, ec = min(cols), max(cols)
    c = ws2.cell(row=1, column=sc, value=month_key)
    c.fill = GANTT_HDR_FILL
    c.font = Font(bold=True, color="FFFFFF", size=10)
    c.alignment = Alignment(horizontal="center", vertical="center")
    if ec > sc:
        ws2.merge_cells(start_row=1, start_column=sc, end_row=1, end_column=ec)

# Row 2: week date labels
for wi, mon in enumerate(mondays):
    col = WEEK_START_C + wi
    c = ws2.cell(row=2, column=col, value=mon.strftime("%d %b"))
    c.fill = GANTT_HDR_FILL
    c.font = Font(bold=True, color="FFFFFF", size=8)
    c.alignment = Alignment(horizontal="center", vertical="center", text_rotation=45)
    ws2.column_dimensions[get_column_letter(col)].width = 5

ws2.row_dimensions[1].height = 20
ws2.row_dimensions[2].height = 52

# Fixed column headers (rows 1+2 merged)
fixed_hdrs   = ["ID", "Task Name", "Owner", "Est Hrs", "Sprint"]
fixed_widths = [6, 40, 9, 7, 9]
for ci, (h, w) in enumerate(zip(fixed_hdrs, fixed_widths), start=1):
    for r in (1, 2):
        c = ws2.cell(row=r, column=ci, value=h if r == 1 else "")
        c.fill = GANTT_HDR_FILL; c.font = GANTT_HDR_FONT
        c.alignment = Alignment(horizontal="center", vertical="center")
    ws2.merge_cells(start_row=1, start_column=ci, end_row=2, end_column=ci)
    ws2.column_dimensions[get_column_letter(ci)].width = w

# Task rows
current_row = 3
current_sp  = None

for task in task_rows:
    sp     = task["Sub-project"]
    sprint = task["Sprint"]
    bar_hex = SP_BAR.get(sp, "4472C4")
    row_hex = SPRINT_LIGHT.get(sprint, "FFFFFF")
    row_fill = fill(row_hex)
    bar_fill = fill(bar_hex)
    b2 = bdr("DDDDDD")

    # Sub-project section header
    if sp != current_sp:
        current_sp = sp
        c = ws2.cell(row=current_row, column=1, value=f"  {sp}")
        c.fill = fill(bar_hex)
        c.font = Font(bold=True, color="FFFFFF", size=9)
        c.alignment = Alignment(vertical="center")
        ws2.merge_cells(start_row=current_row, start_column=1,
                        end_row=current_row, end_column=TOTAL_COLS)
        ws2.row_dimensions[current_row].height = 16
        current_row += 1

    # Fixed cells
    for ci, val in enumerate([
        task["Task ID"],
        task["Task name"],
        task["Owner (R)"],
        task["Estimated hours"],
        task["Sprint"],
    ], start=1):
        c = ws2.cell(row=current_row, column=ci, value=val)
        c.fill = row_fill; c.border = b2
        c.font = Font(size=8, bold=(ci == 1))
        c.alignment = Alignment(
            horizontal="center" if ci != 2 else "left",
            vertical="center",
            wrap_text=(ci == 2),
        )

    # Parse dates
    try:
        t_start = date.fromisoformat(task["Start date"])
        t_end   = date.fromisoformat(task["End date"])
    except (ValueError, TypeError):
        ws2.row_dimensions[current_row].height = 18
        current_row += 1
        continue

    # Paint timeline
    first_bar = True
    for wi, mon in enumerate(mondays):
        col      = WEEK_START_C + wi
        week_end = mon + timedelta(days=6)
        c = ws2.cell(row=current_row, column=col)
        c.border = bdr("EEEEEE")
        if t_start <= week_end and t_end >= mon:
            c.fill = bar_fill
            if first_bar:
                c.value = task["Owner (R)"]
                c.font  = Font(size=7, bold=True, color="FFFFFF")
                c.alignment = Alignment(horizontal="left", vertical="center")
                first_bar = False
        else:
            c.fill = row_fill

    ws2.row_dimensions[current_row].height = 18
    current_row += 1

ws2.freeze_panes = f"{get_column_letter(WEEK_START_C)}3"

# Legend
legend_row = current_row + 2
c = ws2.cell(row=legend_row, column=1, value="Legend — Sub-projects")
c.font = Font(bold=True, size=9)
ws2.merge_cells(start_row=legend_row, start_column=1,
                end_row=legend_row, end_column=5)
for li, (sp_id, sp_name, bar_hex, _) in enumerate(SUBPROJECTS):
    r = legend_row + 1 + li
    c1 = ws2.cell(row=r, column=1, value=sp_id)
    c1.fill = fill(bar_hex)
    c1.font = Font(bold=True, color="FFFFFF", size=8)
    c1.alignment = Alignment(horizontal="center")
    c2 = ws2.cell(row=r, column=2, value=sp_name)
    c2.font = Font(size=8)
    ws2.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)

wb.save(XLSX_PATH)
print(f"XLSX written: {XLSX_PATH}")
