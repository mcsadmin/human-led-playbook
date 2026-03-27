#!/usr/bin/env python3
"""
render_gantt.py — Gantt Chart Renderer for the Human-Led Playbook
==================================================================

Reads a task register Markdown file conforming to
templates/task_register_template.md and produces a Gantt chart PNG.

Usage:
    python render_gantt.py <path/to/task_register.md> [<path/to/output.png>]

Execution environment:
    Designed for use inside a Manus sandbox (Python 3.11, matplotlib
    pre-installed). CLI only — no interactive display. Output is written
    to a file via plt.savefig(); plt.show() is never called.

Requirements specification:
    See docs/gantt_script_requirements.md in the human-led-playbook
    repository for the full approved specification.
"""

import sys
import os
import re
from datetime import date, timedelta, datetime

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — required for sandbox use
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.dates as mdates
import numpy as np


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "Row Type", "Task ID", "Sub-project", "Task name",
    "Owner (R)", "Accountable (A)", "Consulted (C)", "Informed (I)",
    "Dependencies", "Estimated hours", "Start date", "End date",
    "% Complete", "Status", "Sprint",
]

STATUS_COLORS = {
    "not started": "#AAAAAA",
    "in progress": "#4A90D9",
    "complete":    "#5BAD6F",
    "blocked":     "#D94A4A",
    "cancelled":   "#CCCCCC",
}

STATUS_COMPLETE_COLORS = {
    "not started": "#888888",
    "in progress": "#1A5FA0",
    "complete":    "#2E7A45",
    "blocked":     "#A01A1A",
    "cancelled":   "#AAAAAA",
}

SUBPROJECT_BAND_ALPHA = 0.08
SUBPROJECT_BAND_COLORS = [
    "#4A90D9", "#5BAD6F", "#D9A84A", "#9B59B6",
    "#E67E22", "#1ABC9C", "#E74C3C", "#2980B9",
]

WORKING_HOURS_PER_DAY = 8


# ---------------------------------------------------------------------------
# Working-day utilities
# ---------------------------------------------------------------------------

def is_working_day(d: date) -> bool:
    """Return True if d is Monday–Friday."""
    return d.weekday() < 5


def next_working_day(d: date) -> date:
    """Return the next working day on or after d."""
    while not is_working_day(d):
        d += timedelta(days=1)
    return d


def add_working_hours(start: date, hours: float) -> date:
    """
    Return the end date after adding `hours` working hours starting from
    `start` (inclusive). Assumes 8-hour working days, Mon–Fri.
    """
    if hours <= 0:
        return start
    days_needed = int(hours / WORKING_HOURS_PER_DAY)
    remainder = hours % WORKING_HOURS_PER_DAY
    if remainder > 0:
        days_needed += 1
    current = start
    days_added = 0
    while days_added < days_needed:
        if is_working_day(current):
            days_added += 1
            if days_added < days_needed:
                current += timedelta(days=1)
        else:
            current += timedelta(days=1)
    return current


def day_after(d: date) -> date:
    """Return the next working day after d."""
    return next_working_day(d + timedelta(days=1))


# ---------------------------------------------------------------------------
# Markdown table parser
# ---------------------------------------------------------------------------

def parse_markdown_table(filepath: str) -> tuple[list[str], list[dict]]:
    """
    Parse a Markdown pipe table from filepath.

    Returns:
        (headers, rows) where headers is a list of column names and rows
        is a list of dicts mapping column name -> cell value (stripped).

    Raises:
        FileNotFoundError: if filepath does not exist.
        ValueError: if the table structure is malformed.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    # Find table lines: lines starting with '|' that are not comments
    table_lines = [
        (i + 1, line.rstrip())
        for i, line in enumerate(lines)
        if line.strip().startswith("|") and not line.strip().startswith("<!--")
    ]

    if not table_lines:
        raise ValueError("No Markdown table found in the file.")

    # First table line is the header row
    lineno, header_line = table_lines[0]
    headers = [h.strip() for h in header_line.strip("|").split("|")]

    # Second line is the separator — skip it
    data_lines = table_lines[2:]  # skip header + separator

    rows = []
    for lineno, line in data_lines:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise ValueError(
                f"Row {lineno} has {len(cells)} cells but header has "
                f"{len(headers)} columns. Check the table structure."
            )
        rows.append(dict(zip(headers, cells)))

    return headers, rows


# ---------------------------------------------------------------------------
# Column validation
# ---------------------------------------------------------------------------

def validate_columns(headers: list[str]) -> None:
    """Raise ValueError if any required column is missing."""
    missing = [c for c in REQUIRED_COLUMNS if c not in headers]
    if missing:
        raise ValueError(
            f"Task register is missing required columns: {missing}\n"
            f"Found columns: {headers}"
        )


# ---------------------------------------------------------------------------
# RACI inheritance resolver
# ---------------------------------------------------------------------------

def resolve_raci_inheritance(rows: list[dict]) -> list[dict]:
    """
    Apply RACI inheritance: blank RACI fields on TASK rows inherit from
    their parent SUBPROJECT row, which inherits from the PROJECT row.

    Inheritance applies to: Owner (R), Accountable (A), Consulted (C),
    Informed (I).

    Returns a new list of dicts with inheritance applied.
    """
    raci_fields = ["Owner (R)", "Accountable (A)", "Consulted (C)", "Informed (I)"]

    project_defaults = {f: "" for f in raci_fields}
    current_subproject_raci = {f: "" for f in raci_fields}

    resolved = []
    for row in rows:
        row = dict(row)  # copy
        row_type = row.get("Row Type", "").strip().upper()

        if row_type == "PROJECT":
            for f in raci_fields:
                project_defaults[f] = row.get(f, "").strip()
            resolved.append(row)

        elif row_type == "SUBPROJECT":
            for f in raci_fields:
                val = row.get(f, "").strip()
                current_subproject_raci[f] = val if val else project_defaults[f]
                row[f] = current_subproject_raci[f]
            resolved.append(row)

        elif row_type == "TASK":
            for f in raci_fields:
                val = row.get(f, "").strip()
                if not val:
                    row[f] = current_subproject_raci[f]
            resolved.append(row)

        else:
            # Unknown row type — pass through unchanged with a warning
            print(
                f"WARNING: Unknown Row Type '{row_type}' for Task ID "
                f"'{row.get('Task ID', '?')}' — row will be skipped in rendering."
            )
            resolved.append(row)

    return resolved


# ---------------------------------------------------------------------------
# Date resolution
# ---------------------------------------------------------------------------

def parse_date(value: str, task_id: str, field: str) -> date | None:
    """
    Parse a YYYY-MM-DD date string. Returns None and prints a warning
    if the value is blank or malformed.
    """
    value = value.strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        print(
            f"WARNING: Invalid date format '{value}' in Task ID '{task_id}', "
            f"field '{field}' — this task will be flagged on the chart."
        )
        return None


def parse_hours(value: str, task_id: str) -> float:
    """Parse estimated hours. Returns 0.0 on blank or invalid input."""
    value = value.strip()
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        print(
            f"WARNING: Invalid estimated hours '{value}' for Task ID "
            f"'{task_id}' — defaulting to 0."
        )
        return 0.0


def parse_completion(value: str, task_id: str) -> float:
    """Parse % Complete. Clamps to 0–100."""
    value = value.strip()
    if not value:
        return 0.0
    try:
        pct = float(value)
    except ValueError:
        print(
            f"WARNING: Invalid % Complete '{value}' for Task ID '{task_id}' "
            f"— defaulting to 0."
        )
        return 0.0
    if pct < 0:
        print(f"WARNING: % Complete {pct} for Task ID '{task_id}' clamped to 0.")
        return 0.0
    if pct > 100:
        print(f"WARNING: % Complete {pct} for Task ID '{task_id}' clamped to 100.")
        return 100.0
    return pct


def resolve_dates(task_rows: list[dict]) -> list[dict]:
    """
    Resolve start and end dates for all TASK rows, applying the date
    handling rules from the requirements specification.

    Modifies rows in-place (adds '_start', '_end', '_date_warning' keys).
    Returns the modified list.
    """
    # Build a map of task_id -> resolved end date for dependency lookups
    end_date_map: dict[str, date] = {}

    for row in task_rows:
        task_id = row.get("Task ID", "?").strip()
        hours = parse_hours(row.get("Estimated hours", ""), task_id)

        start = parse_date(row.get("Start date", ""), task_id, "Start date")
        end = parse_date(row.get("End date", ""), task_id, "End date")

        deps_raw = row.get("Dependencies", "").strip()
        dep_ids = [d.strip() for d in deps_raw.split(",") if d.strip()] if deps_raw else []

        date_warning = False

        # Case 1: both dates present — use as-is
        if start and end:
            pass

        # Case 2: start present, end absent — calculate end from hours
        elif start and not end:
            if hours > 0:
                end = add_working_hours(start, hours)
            else:
                end = start  # zero-duration task

        # Case 3: start absent, dependencies present — calculate start from deps
        elif not start and dep_ids:
            latest_dep_end = None
            for dep_id in dep_ids:
                dep_end = end_date_map.get(dep_id)
                if dep_end:
                    if latest_dep_end is None or dep_end > latest_dep_end:
                        latest_dep_end = dep_end
            if latest_dep_end:
                start = day_after(latest_dep_end)
                start = next_working_day(start)
                if hours > 0:
                    end = add_working_hours(start, hours)
                else:
                    end = start
            else:
                # Dependencies listed but none resolved yet — flag
                date_warning = True

        # Case 4: neither date nor resolvable dependencies
        else:
            date_warning = True

        row["_start"] = start
        row["_end"] = end if end else start
        row["_date_warning"] = date_warning

        if start:
            end_date_map[task_id] = row["_end"]

    return task_rows


# ---------------------------------------------------------------------------
# Main rendering function
# ---------------------------------------------------------------------------

def render_gantt(input_path: str, output_path: str) -> None:
    """
    Parse the task register at input_path and write a Gantt chart PNG
    to output_path.
    """
    # --- Parse ---
    print(f"Parsing: {input_path}")
    headers, rows = parse_markdown_table(input_path)
    validate_columns(headers)

    # --- Resolve RACI inheritance ---
    rows = resolve_raci_inheritance(rows)

    # --- Separate row types ---
    project_row = next(
        (r for r in rows if r.get("Row Type", "").strip().upper() == "PROJECT"),
        None,
    )
    subproject_rows = [
        r for r in rows if r.get("Row Type", "").strip().upper() == "SUBPROJECT"
    ]
    task_rows = [
        r for r in rows if r.get("Row Type", "").strip().upper() == "TASK"
    ]

    if not task_rows:
        print("WARNING: No TASK rows found in the task register. Nothing to render.")
        sys.exit(0)

    # --- Resolve dates ---
    task_rows = resolve_dates(task_rows)

    # --- Determine project title ---
    project_title = "Project Gantt Chart"
    if project_row:
        sp_val = project_row.get("Sub-project", "").strip()
        tn_val = project_row.get("Task name", "").strip()
        project_title = sp_val or tn_val or project_title

    # --- Build ordered list of (subproject_name, [task_rows]) ---
    # Preserve sub-project order as they appear in the register
    subproject_order = []
    seen = set()
    for r in rows:
        rt = r.get("Row Type", "").strip().upper()
        sp = r.get("Sub-project", "").strip()
        if rt in ("SUBPROJECT", "TASK") and sp and sp not in seen:
            subproject_order.append(sp)
            seen.add(sp)

    tasks_by_subproject: dict[str, list[dict]] = {sp: [] for sp in subproject_order}
    for t in task_rows:
        sp = t.get("Sub-project", "").strip()
        if sp in tasks_by_subproject:
            tasks_by_subproject[sp].append(t)
        else:
            # Task belongs to an unlisted sub-project
            tasks_by_subproject.setdefault(sp, []).append(t)
            if sp not in subproject_order:
                subproject_order.append(sp)

    # --- Determine overall date range ---
    all_starts = [t["_start"] for t in task_rows if t["_start"]]
    all_ends = [t["_end"] for t in task_rows if t["_end"]]

    if not all_starts or not all_ends:
        print("WARNING: Could not determine a date range. Check task register dates.")
        sys.exit(0)

    project_start = min(all_starts)
    project_end = max(all_ends)
    # Add a small margin on each side
    chart_start = project_start - timedelta(days=2)
    chart_end = project_end + timedelta(days=5)

    # --- Build y-axis entries ---
    # Each entry is either a task row or a subproject label placeholder
    y_entries = []  # list of dicts: type, label, task (if type==task)
    for sp in subproject_order:
        sp_tasks = tasks_by_subproject.get(sp, [])
        if not sp_tasks:
            continue
        y_entries.append({"type": "subproject_label", "label": sp, "tasks": sp_tasks})
        for t in sp_tasks:
            y_entries.append({"type": "task", "label": t.get("Task name", "").strip(), "task": t})

    n_rows = len(y_entries)

    # --- Figure sizing ---
    row_height = 0.4
    fig_height = max(4, n_rows * row_height + 2)
    fig_width = 16

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # --- Convert dates to matplotlib date numbers ---
    def to_num(d: date) -> float:
        return mdates.date2num(datetime(d.year, d.month, d.day))

    # --- Draw subproject bands ---
    sp_color_map = {}
    for idx, sp in enumerate(subproject_order):
        color = SUBPROJECT_BAND_COLORS[idx % len(SUBPROJECT_BAND_COLORS)]
        sp_color_map[sp] = color

    # Collect y indices for each subproject
    sp_y_ranges: dict[str, list[int]] = {}
    for y_idx, entry in enumerate(y_entries):
        if entry["type"] == "task":
            sp = entry["task"].get("Sub-project", "").strip()
            sp_y_ranges.setdefault(sp, []).append(y_idx)

    for sp, y_indices in sp_y_ranges.items():
        if not y_indices:
            continue
        sp_tasks = tasks_by_subproject.get(sp, [])
        sp_starts = [t["_start"] for t in sp_tasks if t["_start"]]
        sp_ends = [t["_end"] for t in sp_tasks if t["_end"]]
        if not sp_starts or not sp_ends:
            continue

        band_start = to_num(min(sp_starts) - timedelta(days=1))
        band_end = to_num(max(sp_ends) + timedelta(days=1))
        y_bottom = min(y_indices) - 0.5
        y_top = max(y_indices) + 0.5
        band_height = y_top - y_bottom

        ax.barh(
            y=(y_bottom + y_top) / 2,
            width=band_end - band_start,
            left=band_start,
            height=band_height,
            color=sp_color_map.get(sp, "#AAAAAA"),
            alpha=SUBPROJECT_BAND_ALPHA,
            zorder=0,
        )

    # --- Draw task bars ---
    y_labels = []
    for y_idx, entry in enumerate(y_entries):
        if entry["type"] == "subproject_label":
            y_labels.append(f"  ▶  {entry['label']}")
            continue

        task = entry["task"]
        task_id = task.get("Task ID", "").strip()
        task_name = entry["label"] or task_id
        y_labels.append(f"    {task_name}")

        start = task["_start"]
        end = task["_end"]
        date_warning = task["_date_warning"]
        pct = parse_completion(task.get("% Complete", "0"), task_id)
        status = task.get("Status", "").strip().lower()
        owner = task.get("Owner (R)", "").strip()

        if date_warning or not start:
            # Draw a warning marker
            ax.text(
                to_num(chart_start + timedelta(days=3)),
                y_idx,
                "⚠ No date — check register",
                va="center",
                ha="left",
                fontsize=7,
                color="#CC6600",
                style="italic",
            )
            continue

        bar_start = to_num(start)
        bar_end = to_num(end + timedelta(days=1))  # end is inclusive
        bar_width = bar_end - bar_start

        base_color = STATUS_COLORS.get(status, "#AAAAAA")
        fill_color = STATUS_COMPLETE_COLORS.get(status, "#888888")

        is_cancelled = status == "cancelled"

        # Full-duration bar
        ax.barh(
            y_idx,
            width=bar_width,
            left=bar_start,
            height=0.35,
            color=base_color,
            zorder=2,
            hatch="///" if is_cancelled else None,
            edgecolor="white" if not is_cancelled else "#999999",
            linewidth=0.5,
        )

        # % Complete overlay
        if pct > 0 and not is_cancelled:
            fill_width = bar_width * (pct / 100.0)
            ax.barh(
                y_idx,
                width=fill_width,
                left=bar_start,
                height=0.35,
                color=fill_color,
                zorder=3,
            )

        # Owner label to the right of bar
        if owner:
            ax.text(
                bar_end + 0.3,
                y_idx,
                owner,
                va="center",
                ha="left",
                fontsize=7,
                color="#333333",
                zorder=4,
            )

    # --- Y-axis formatting ---
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(y_labels, fontsize=8)
    ax.invert_yaxis()

    # Style subproject label rows
    for y_idx, entry in enumerate(y_entries):
        if entry["type"] == "subproject_label":
            sp = entry["label"]
            ax.get_yticklabels()[y_idx].set_fontweight("bold")
            ax.get_yticklabels()[y_idx].set_color(sp_color_map.get(sp, "#333333"))

    # --- X-axis formatting ---
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.xticks(rotation=45, ha="right", fontsize=8)

    ax.set_xlim(to_num(chart_start), to_num(chart_end))

    # --- Grid ---
    ax.grid(axis="x", which="major", linestyle="--", linewidth=0.5, alpha=0.5, zorder=1)
    ax.grid(axis="x", which="minor", linestyle=":", linewidth=0.3, alpha=0.3, zorder=1)

    # --- Today line ---
    today = date.today()
    if chart_start <= today <= chart_end:
        ax.axvline(
            x=to_num(today),
            color="#CC0000",
            linewidth=1.2,
            linestyle="--",
            zorder=5,
            label="Today",
        )
        ax.text(
            to_num(today),
            -0.7,
            "Today",
            ha="center",
            va="bottom",
            fontsize=7,
            color="#CC0000",
            transform=ax.get_xaxis_transform(),
        )

    # --- Legend ---
    legend_patches = [
        mpatches.Patch(color=STATUS_COLORS["not started"], label="Not started"),
        mpatches.Patch(color=STATUS_COLORS["in progress"], label="In progress"),
        mpatches.Patch(color=STATUS_COLORS["complete"], label="Complete"),
        mpatches.Patch(color=STATUS_COLORS["blocked"], label="Blocked"),
        mpatches.Patch(color=STATUS_COLORS["cancelled"], label="Cancelled", hatch="///"),
    ]
    ax.legend(
        handles=legend_patches,
        loc="lower right",
        fontsize=7,
        framealpha=0.8,
        ncol=5,
    )

    # --- Title and labels ---
    ax.set_title(project_title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=9)

    # --- Spines ---
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # --- Save ---
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Gantt chart written to: {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python render_gantt.py <path/to/task_register.md> "
            "[<path/to/output.png>]"
        )
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        base = os.path.splitext(input_path)[0]
        output_path = base + "_gantt.png"

    try:
        render_gantt(input_path, output_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
