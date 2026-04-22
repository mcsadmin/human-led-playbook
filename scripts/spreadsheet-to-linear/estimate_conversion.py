"""
estimate_conversion.py
======================
Converts estimated hours (from the planning spreadsheet) into Linear's
native abstract estimate points, using a team-configurable conversion matrix.

Linear supports four estimate scales. This module defaults to the T-Shirt
scale, which is the most intuitive for non-engineering teams. The active
scale is set in the skill's config file (generated during Phase 0 preflight).

Usage
-----
    from estimate_conversion import convert_hours_to_points, SCALE_TSHIRT

    points = convert_hours_to_points(6.5, scale=SCALE_TSHIRT)
    # Returns: 3  (i.e., "M" on the T-Shirt scale)

Linear Estimate Scales (native values)
---------------------------------------
    T-Shirt:     1=XS, 2=S, 3=M, 4=L, 5=XL  (extended: 6=XXL, 7=XXXL)
    Fibonacci:   1, 2, 3, 5, 8               (extended: 13, 21)
    Exponential: 1, 2, 4, 8, 16              (extended: 32, 64)
    Linear:      1, 2, 3, 4, 5               (extended: 6, 7)

Note: Linear stores the *numeric value* of the estimate, not the label.
      For T-Shirt sizes, 1=XS, 2=S, 3=M, 4=L, 5=XL in the API.
"""

from __future__ import annotations
from typing import Optional


# ---------------------------------------------------------------------------
# Scale definitions
# Each entry is a tuple of (max_hours_inclusive, linear_points_value, label)
# Rows are evaluated in order; the first row where hours <= max_hours is used.
# A max_hours of None means "anything above the previous threshold".
# ---------------------------------------------------------------------------

SCALE_TSHIRT = [
    # (max_hours, points_value, human_label)
    (2,    1, "XS"),
    (4,    2, "S"),
    (8,    3, "M"),
    (16,   4, "L"),
    (None, 5, "XL"),   # > 16 hours → XL
]

SCALE_FIBONACCI = [
    (1,    1,  "1"),
    (2,    2,  "2"),
    (4,    3,  "3"),
    (8,    5,  "5"),
    (None, 8,  "8"),   # > 8 hours → 8 points
]

SCALE_EXPONENTIAL = [
    (1,    1,  "1"),
    (2,    2,  "2"),
    (4,    4,  "4"),
    (8,    8,  "8"),
    (None, 16, "16"),  # > 8 hours → 16 points
]

SCALE_LINEAR = [
    (2,    1, "1"),
    (4,    2, "2"),
    (6,    3, "3"),
    (8,    4, "4"),
    (None, 5, "5"),    # > 8 hours → 5 points
]

# Map scale names (as stored in config) to their definitions
SCALES: dict[str, list] = {
    "tshirt":      SCALE_TSHIRT,
    "fibonacci":   SCALE_FIBONACCI,
    "exponential": SCALE_EXPONENTIAL,
    "linear":      SCALE_LINEAR,
}

# Default scale used when none is specified
DEFAULT_SCALE = "tshirt"


# ---------------------------------------------------------------------------
# Core conversion function
# ---------------------------------------------------------------------------

def convert_hours_to_points(
    hours: float | int | str | None,
    scale: list | None = None,
    scale_name: str = DEFAULT_SCALE,
) -> Optional[int]:
    """
    Convert an estimated hours value to a Linear estimate points value.

    Parameters
    ----------
    hours : float | int | str | None
        The estimated hours from the spreadsheet. Accepts numeric types or
        a string representation (e.g., "6.5"). Returns None if the value
        is missing, zero, or cannot be parsed.
    scale : list | None
        A custom scale definition (list of tuples). If provided, takes
        precedence over `scale_name`.
    scale_name : str
        Name of the built-in scale to use: "tshirt", "fibonacci",
        "exponential", or "linear". Defaults to "tshirt".

    Returns
    -------
    int | None
        The Linear estimate points value, or None if hours is invalid.
    """
    # --- Parse and validate input ---
    if hours is None:
        return None
    try:
        hours_float = float(hours)
    except (ValueError, TypeError):
        return None
    if hours_float <= 0:
        return None

    # --- Resolve scale ---
    active_scale = scale if scale is not None else SCALES.get(scale_name, SCALE_TSHIRT)

    # --- Walk the scale thresholds ---
    for max_hours, points_value, _label in active_scale:
        if max_hours is None or hours_float <= max_hours:
            return points_value

    # Fallback: return the last defined points value
    return active_scale[-1][1]


def convert_hours_to_label(
    hours: float | int | str | None,
    scale: list | None = None,
    scale_name: str = DEFAULT_SCALE,
) -> Optional[str]:
    """
    Like convert_hours_to_points, but returns the human-readable label
    (e.g., "M" for T-Shirt, "5" for Fibonacci).
    """
    if hours is None:
        return None
    try:
        hours_float = float(hours)
    except (ValueError, TypeError):
        return None
    if hours_float <= 0:
        return None

    active_scale = scale if scale is not None else SCALES.get(scale_name, SCALE_TSHIRT)

    for max_hours, _points_value, label in active_scale:
        if max_hours is None or hours_float <= max_hours:
            return label

    return active_scale[-1][2]


def describe_scale(scale_name: str = DEFAULT_SCALE) -> str:
    """
    Returns a human-readable description of a scale's thresholds,
    suitable for inclusion in the Phase 0 preflight report.
    """
    active_scale = SCALES.get(scale_name, SCALE_TSHIRT)
    lines = [f"Estimate conversion matrix (scale: {scale_name}):", ""]
    lines.append(f"  {'Hours Range':<20} {'Points':<8} {'Label'}")
    lines.append(f"  {'-'*20} {'-'*8} {'-'*8}")

    prev_max = 0
    for i, (max_hours, points_value, label) in enumerate(active_scale):
        if max_hours is None:
            range_str = f"> {prev_max} hrs"
        elif i == 0:
            range_str = f"≤ {max_hours} hrs"
        else:
            range_str = f"{prev_max + 0.01:.1f} – {max_hours} hrs"
        lines.append(f"  {range_str:<20} {points_value:<8} {label}")
        if max_hours is not None:
            prev_max = max_hours

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Convenience: batch conversion for a list of task dicts
# ---------------------------------------------------------------------------

def enrich_tasks_with_estimates(
    tasks: list[dict],
    hours_key: str = "estimated_hours",
    points_key: str = "estimate_points",
    label_key: str = "estimate_label",
    scale_name: str = DEFAULT_SCALE,
) -> list[dict]:
    """
    Given a list of task dicts (as produced by parse_spreadsheet.py),
    add `estimate_points` and `estimate_label` keys to each dict.

    Parameters
    ----------
    tasks : list[dict]
        List of task dictionaries, each expected to have an `hours_key` field.
    hours_key : str
        The key in each task dict containing the estimated hours value.
    points_key : str
        The key to write the converted points value into.
    label_key : str
        The key to write the human-readable label into.
    scale_name : str
        The estimate scale to use for conversion.

    Returns
    -------
    list[dict]
        The same list with `points_key` and `label_key` added to each dict.
    """
    for task in tasks:
        hours = task.get(hours_key)
        task[points_key] = convert_hours_to_points(hours, scale_name=scale_name)
        task[label_key] = convert_hours_to_label(hours, scale_name=scale_name)
    return tasks


# ---------------------------------------------------------------------------
# CLI: print the active scale matrix (useful during Phase 0 preflight)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    scale_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SCALE
    if scale_arg not in SCALES:
        print(f"Unknown scale '{scale_arg}'. Available: {', '.join(SCALES.keys())}")
        sys.exit(1)

    print(describe_scale(scale_arg))
    print()

    # Quick self-test
    test_hours = [0.5, 1, 2, 3, 4, 5, 6, 8, 10, 16, 20, 40]
    print(f"  {'Hours':<8} {'Points':<8} {'Label'}")
    print(f"  {'-'*8} {'-'*8} {'-'*8}")
    for h in test_hours:
        pts = convert_hours_to_points(h, scale_name=scale_arg)
        lbl = convert_hours_to_label(h, scale_name=scale_arg)
        print(f"  {h:<8} {pts:<8} {lbl}")
