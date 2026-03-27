<!--
INSTRUCTIONS FOR AGENTS (COACH AND TRACKER)

This Task Register is the single source of truth for all project tasks.
It uses a 15-column schema to represent a three-layer hierarchy: Project -> Sub-project -> Task.

1. ROW TYPES:
   - PROJECT: A single row at the top. Defines project-level defaults. Leave task-specific fields blank.
   - SUBPROJECT: Defines a major workstream. Leave task-specific fields blank.
   - TASK: Defines an individual piece of work.

2. RACI INHERITANCE RULE:
   - If a RACI field (Owner, Accountable, Consulted, Informed) is blank on a TASK row, it inherits the value from its parent SUBPROJECT row.
   - If a RACI field is blank on a SUBPROJECT row, it inherits the value from the PROJECT row.
   - The PROJECT row is the top-level default and does not inherit.
   - Consulted (C) and Informed (I) can contain comma-separated lists of names or emails.

3. FIELD FORMATS:
   - Dependencies: Comma-separated list of Task IDs that must complete before this task can start.
   - Dates: YYYY-MM-DD format.
   - % Complete: Numeric value from 0 to 100.
   - Status: Must be one of: Not started, In progress, Complete, Blocked, Cancelled.

Do not modify the table headers.
-->

# Project Task Register

| Row Type | Task ID | Sub-project | Task name | Owner (R) | Accountable (A) | Consulted (C) | Informed (I) | Dependencies | Estimated hours | Start date | End date | % Complete | Status | Sprint |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PROJECT | P01 | Project Name | | Default Owner | Default Sponsor | | All Stakeholders | | | | | | | |
| SUBPROJECT | SP01 | Workstream Alpha | | Sub-project Lead | | | | | | | | | | |
| TASK | T01 | Workstream Alpha | First task description | Task Owner | | Expert A, Expert B | | | 8 | 2026-04-01 | 2026-04-02 | 0 | Not started | Sprint 1 |
| TASK | T02 | Workstream Alpha | Second task description | | | | | T01 | 16 | 2026-04-03 | 2026-04-05 | 0 | Not started | Sprint 1 |
| SUBPROJECT | SP02 | Workstream Beta | | | | | | | | | | | | |
| TASK | T03 | Workstream Beta | Third task description | | | | | | 4 | 2026-04-01 | 2026-04-01 | 0 | Not started | Sprint 1 |
