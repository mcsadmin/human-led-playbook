# Human-Led Project Coaching Playbook

A generic framework for AI-coached, human-delivered projects. This playbook provides the structural model, operational processes, agent prompts, reusable templates, and tested scripts needed to coach a project from goal to delivery using the two-agent (Coach + Tracker) pattern.

## Repository Structure

```
human-led-playbook/
├── docs/                  # Process design documents
│   ├── vsm_map.md         # Viable System Model map for the coaching pattern
│   ├── working_method_protocol.md  # Operational rhythm, processes, and artifacts
│   ├── project_initiation_protocol.md  # Protocol for standing up new projects
│   ├── gantt_script_requirements.md    # Approved requirements spec for render_gantt.py
│   ├── linear_ontology_mapping.md      # How Project/Sub-project/Task maps to Linear
│   └── spreadsheet_to_linear_skill_plan.md  # Design spec for the Linear translation skill
├── prompts/               # Agent master prompts and templates
│   ├── project_coach_master_prompt.md          # Durable Project Coach prompt
│   ├── project_tracker_prompt_template.md      # Disposable Project Tracker template
│   ├── initiation_facilitator_prompt.md        # Lightweight initiation facilitator prompt
│   └── spreadsheet_to_linear_coach_prompt.md   # Coach prompt for Linear handoff workflow
├── templates/             # Reusable data structure templates
│   ├── task_register_template.md  # Empty task register schema
│   ├── dsm_template.md            # Empty Dependency Structure Matrix format
│   ├── working_brief_template.md  # Empty working brief template
│   └── issue_body_template.md     # Standard Linear Issue body template
├── scripts/               # Tested tooling
│   ├── render_gantt.py    # Python script to render Gantt chart from task register
│   └── spreadsheet-to-linear/     # Scripts for translating task register into Linear
│       ├── config_schema.py        # Shared data model and configuration structures
│       ├── estimate_conversion.py  # Hours-to-Linear-points conversion matrix
│       ├── preflight.py            # Phase 0: query Linear workspace, produce readiness report
│       ├── parse_spreadsheet.py    # Phase 1: parse .xlsx, resolve names, produce review doc
│       └── create_linear_artifacts.py  # Phase 2: create Initiative, Projects, Issues in Linear
└── README.md
```

## How to Use This Playbook

1. **Start a new project** by creating a project-specific repository (e.g., `odoo-project`).
2. **Launch a Project Coach** task using the master prompt from `prompts/project_coach_master_prompt.md`, giving it access to both this playbook repository and the project repository.
3. **The Coach** will guide the team through requirements elicitation, sub-project definition, and plan generation, using the templates from this repository.
4. **When the plan is approved**, the Coach produces a Tracker briefing package and a disposable Project Tracker is instantiated.
5. **The Tracker** facilitates sprint-by-sprint execution, updating the task register and re-rendering the Gantt chart as needed.
6. **If significant re-planning is needed**, the team re-engages the Coach.

## Spreadsheet-to-Linear Workflow

For projects using **Linear.app** as the execution environment, the playbook includes a three-phase skill that translates an approved task register spreadsheet into a fully structured set of Linear artifacts (Initiative, Projects, Issues, and Dependencies).

The workflow is governed by `prompts/spreadsheet_to_linear_coach_prompt.md` and executed via the five scripts in `scripts/spreadsheet-to-linear/`. It operates as follows:

- **Phase 0 — Preflight:** Query the live Linear workspace to produce a readiness report and a blank spreadsheet template with valid member names and labels pre-populated.
- **Phase 1 — Parse and Review:** Parse the completed spreadsheet, resolve all names to Linear IDs, convert hour estimates to T-shirt points, and produce a human-reviewable plan document. No Linear artifacts are created until the team approves this document.
- **Phase 2 — Execute:** Create the full Linear structure (Initiative → Projects → Issues → Dependencies) with idempotency — re-running the script updates existing records rather than creating duplicates.

The key ontology mapping is: **Project → Initiative**, **Sub-project → Project**, **Task → Issue**. See `docs/linear_ontology_mapping.md` for the full reference.

## Related Repositories

- `mcsadmin/ai-build-playbook` — The companion playbook for technical builds with coding agent handoff.
- Project-specific repositories (e.g., `mcsadmin/odoo-project`) contain the project's working brief, scope document, and delivery artifacts.
