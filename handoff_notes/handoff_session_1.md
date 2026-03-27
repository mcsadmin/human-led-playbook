# Handoff Note — Session 1: Requirements Clarification
### Structured Artifacts Build | 27 March 2026

---

## What Was Decided

1. **Task register schema extended to 15 columns.** The original 11-column specification from the Technical Briefing was extended to reflect a three-layer hierarchy (Project → Sub-project → Task) and a full RACI model. The agreed column set is: `Row Type`, `Task ID`, `Sub-project`, `Task name`, `Owner (R)`, `Accountable (A)`, `Consulted (C)`, `Informed (I)`, `Dependencies`, `Estimated hours`, `Start date`, `End date`, `% Complete`, `Status`, `Sprint`.

2. **Explicit `Row Type` column adopted (Option A).** Row type is declared explicitly using controlled values (`PROJECT`, `SUBPROJECT`, `TASK`) rather than inferred from blank fields. This makes the register unambiguous for both LLM agents and the rendering script.

3. **RACI inheritance rule confirmed.** A task row inherits any blank RACI field from its parent sub-project row; a sub-project row inherits any blank RACI field from the project row. The project row (Row Type = `PROJECT`) is the top-level default and does not inherit from anything. This rule will be documented in the template's instructional comment block.

4. **`% Complete` column added (0–100, numeric).** `Status` carries the categorical state (`Not started` / `In progress` / `Complete` / `Blocked` / `Cancelled`); `% Complete` carries the numeric progress for Gantt bar rendering.

5. **DSM reading convention: Row depends on Column.** A mark (X) in row T03, column T01 means T03 depends on T01.

6. **Gantt rendering library: `matplotlib`.** Static PNG output, no additional export toolchain required.

7. **Test scenario: agent-invented.** The build agent will create a dummy project for Session 4 validation.

## What Was Parked

Nothing. All open questions from the requirements checklist were resolved.

## Implications

- The three-layer hierarchy and RACI inheritance rule add meaningful complexity to the rendering script (Session 3). The script must resolve inherited RACI values before rendering, and must handle the `PROJECT` row (which has no dates or task-level fields) without error.
- The `% Complete` column requires the Gantt script to render a filled bar segment within each task bar, in addition to the full task duration bar.
- The `Consulted (C)` and `Informed (I)` columns may contain comma-separated lists; the script must not attempt to parse these as single values.

## What Session 2 Must Address

Build the two Markdown templates:
1. `templates/task_register_template.md` — empty table with 15-column headers, instructional comment block, and example rows for each of the three row types (PROJECT, SUBPROJECT, TASK).
2. `templates/dsm_template.md` — empty template with a 3×3 worked example and clear reading instructions (Row depends on Column convention).

Present both to the user for review before proceeding to Session 3.

---

*Committed at end of Session 1. Next session: Session 2 — Build the Templates.*
