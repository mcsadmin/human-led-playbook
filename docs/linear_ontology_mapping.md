# Linear Ontology Mapping (Revised)

> **Version 2 — April 2026**
> This document supersedes the original ontology mapping. It has been revised to accurately reflect Linear's native affordances, verified against the official Linear documentation as of April 2026.

---

## Purpose

This project uses Linear for project management. Linear has its own ontology that differs from conventional project management terminology. Because the team will sometimes use generic terms in conversation, the mappings below must be understood clearly to avoid confusion.

---

## Linear's Object Hierarchy

Linear organises work in a three-tier containment hierarchy, with two cross-cutting concepts (Cycles and Milestones) that apply at the issue level.

### Initiative

An Initiative is the **top-level container** in Linear. It assembles a curated list of Projects and is presented at the workspace level. Initiatives express the goals and objectives an organisation aims to achieve and allow leadership to monitor progress across multiple Projects and long timelines. Each Initiative has a lifecycle status (Planned, Active, or Completed), an owner, a target date, and a rich-text description.

Initiatives can be nested as **sub-initiatives** up to five levels deep, although this capability requires the Enterprise plan. In this project's context, the entire Insight Membership Marketing effort is a single Initiative in Linear, even though the team refers to it as a "project" in conversation.

| Property | Description |
|---|---|
| Name | Required. The Initiative's title. |
| Status | Planned, Active, or Completed. |
| Owner | A workspace member responsible for the Initiative. |
| Target date | The expected completion date. |
| Summary | A short summary (max 255 characters). |
| Description | Rich Markdown description. |

### Project

A Project is the **mid-level container** in Linear. It groups Issues toward a specific, time-bound deliverable such as a feature launch or a workstream. Projects have their own overview pages displaying all related Issues, milestones, documents, and progress graphs. A Project can span multiple teams and is assigned to one or more Initiatives.

In this project's context, what the coaching framework and the team refer to as "sub-projects" are represented as Projects in Linear.

| Property | Description |
|---|---|
| Name | Required. The Project's title. |
| Lead | The workspace member responsible for the Project. |
| Start date | When work begins (can be set at day, month, or quarter precision). |
| Target date | When work is expected to complete (same precision options). |
| Priority | None, Urgent, High, Medium, or Low. |
| State | The Project's lifecycle state (e.g., Planned, In Progress, Completed). |
| Description | Rich Markdown description. |
| Labels | Project-level labels for categorisation. |
| Teams | One or more teams associated with the Project. |

### Issue

An Issue is the **bottom-level unit of work** in Linear. Each Issue belongs to exactly one team and is identified by a team-prefixed number (e.g., MCS-42). Issues can have sub-issues (parent/child nesting) to break down larger tasks into smaller pieces.

In this project's context, what the coaching framework and the team refer to as "tasks" are represented as Issues in Linear.

| Property | Description |
|---|---|
| Title | Required. A concise description of the work. |
| Description | Rich Markdown body with full detail. |
| Status | Follows the team's workflow (e.g., Backlog, Todo, In Progress, Done, Cancelled). |
| Assignee | The person responsible for completing the Issue. |
| Priority | None (0), Urgent (1), High (2), Normal (3), Low (4). |
| Estimate | An abstract complexity/size value on the team's chosen scale (see Estimates below). |
| Due date | The date by which the Issue should be completed. |
| Labels | Issue-level labels for categorisation. |
| Project | The Project this Issue belongs to (an Issue can belong to at most one Project). |
| Cycle | The Cycle (sprint) this Issue is assigned to. |
| Milestone | The Project Milestone this Issue is assigned to (within its Project). |

### Cycle

A Cycle is Linear's term for a **time-boxed iteration**, equivalent to what the team and the coaching framework refer to as a "sprint." Cycles are configured per-team with a fixed duration (1 to 8 weeks) and repeat automatically on a regular cadence. Linear auto-creates upcoming Cycles based on the configured schedule.

Cycles are **not** created ad-hoc with arbitrary start and end dates. Instead, the team configures a cadence (e.g., two-week cycles starting on Mondays), and Linear generates the cycle schedule. Unfinished Issues roll over to the next Cycle automatically.

| Property | Description |
|---|---|
| Duration | 1 to 8 weeks, configured in Team Settings. |
| Start day | The day of the week each Cycle begins. |
| Cooldown | Optional rest period between Cycles. |
| Upcoming count | Number of future Cycles to pre-create (max 15). |

### Milestone

A Milestone is a concept used to **further organise Issues within a single Project**. Milestones represent meaningful stages of completion and allow the team to track progress toward intermediate goals within a Project. Issues within a Project can be assigned to Milestones and filtered accordingly.

---

## Terminology Mapping

The following table provides a cross-reference between the three vocabularies in play: what the team says in conversation, what the coaching framework documents use, and what appears in Linear.

| Team / Conversation | Coaching Framework | Linear |
|---|---|---|
| Project | Project | Initiative |
| Sub-project | Sub-project | Project |
| Task | Task | Issue |
| Sub-task | Sub-task | Sub-issue |
| Sprint | Sprint | Cycle |
| Phase / Stage | Milestone | Milestone |

When writing or reading any project document, the coaching framework terms should be used. When creating or referencing items in Linear, the Linear terms must be used. This glossary serves as the authoritative mapping between the two.

---

## Dependency and Relation Affordances

The original version of this document stated that "Linear Issues cannot have formal dependencies." This has been verified as **incorrect**. Linear provides structured dependency relations at multiple levels of its hierarchy, as documented below.

### Issue-Level Relations

Linear supports three types of formal relations between Issues, accessible via the Issue sidebar, keyboard shortcuts, or the command menu:

| Relation Type | Meaning | Visual Indicator |
|---|---|---|
| **Blocked by** | This Issue cannot proceed until the blocking Issue is resolved. | Orange flag in sidebar. |
| **Blocking** | This Issue is preventing another Issue from proceeding. | Red flag in sidebar (turns green when resolved). |
| **Related** | A general association between two Issues. | Listed under Related in sidebar. |
| **Duplicate** | Marks an Issue as a duplicate of another; the duplicate is cancelled. | Status changed to Cancelled. |

These relations are fully supported in Linear's API and MCP integration via the `blockedBy` and `blocks` fields on Issues. The skill uses these to represent task dependencies from the spreadsheet.

> **Source**: [Issue relations — Linear Docs](https://linear.app/docs/issue-relations)

### Project-Level Dependencies

Linear also supports formal **blocked-by / blocking** relationships between Projects. These are visualised on the timeline view as dependency lines (blue when valid, red when violated). Only end-to-start dependencies are currently supported.

> **Source**: [Project dependencies — Linear Docs](https://linear.app/docs/project-dependencies)

### Initiative-Level Dependencies

Initiatives do **not** currently have native dependency relations. Where the coaching framework identifies dependencies between sub-projects (which map to Linear Projects), these should be represented using Project-level dependencies.

---

## Estimates

Linear's estimate system measures **abstract complexity or size**, not hours. Estimates are configured per-team and use one of the following scales:

| Scale | Values | Extended |
|---|---|---|
| Exponential | 1, 2, 4, 8, 16 | 32, 64 |
| Fibonacci | 1, 2, 3, 5, 8 | 13, 21 |
| Linear | 1, 2, 3, 4, 5 | 6, 7 |
| T-Shirt | XS, S, M, L, XL | XXL, XXXL |

Because the coaching framework's task register records **estimated hours**, these cannot be directly mapped to Linear's estimate field without a conversion decision. The recommended approach is to record estimated hours in the Issue description and use Linear's native estimate scale for relative sizing if the team chooses to adopt it.

---

## Practical Implications for the Spreadsheet-to-Linear Workflow

The following table summarises how each spreadsheet column maps to Linear, noting any constraints or conversion requirements.

| Spreadsheet Column | Linear Field | Notes |
|---|---|---|
| Task ID (e.g., T01) | Issue title prefix or description | Used as a stable identifier for idempotency. |
| Sub-project | Project name | One Linear Project per unique Sub-project value. |
| Task name | Issue title | Direct mapping. |
| Owner (R) | Issue assignee | Matched by name against Linear workspace members. |
| Accountable (A) | Issue description (RACI section) | No native "Accountable" field in Linear. |
| Consulted (C) | Issue description (RACI section) | No native "Consulted" field in Linear. |
| Informed (I) | Issue description (RACI section) | No native "Informed" field in Linear. |
| Dependencies | Issue `blockedBy` relations | Mapped to formal blocked-by relations between Issues. |
| Estimated hours | Issue description | Not directly mappable to Linear estimates (see above). |
| Start date | Issue description or Project start date | Issues have only a due date, not a start date. |
| End date | Issue due date | Direct mapping. |
| % Complete | Issue status | Approximated via workflow status (e.g., In Progress, Done). |
| Status | Issue status | Mapped to team workflow states. |
| Sprint | Issue Cycle assignment | Requires Cycles to be configured and active in the team. |

---

## Change Log

| Version | Date | Changes |
|---|---|---|
| 1 | — | Original document. |
| 2 | April 2026 | Corrected Issue dependency statement. Added Project-level dependencies. Added Estimates section. Added Milestones. Added Cycle configuration detail. Added practical mapping table. Restructured for completeness. |
