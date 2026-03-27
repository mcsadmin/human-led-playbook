# Human-Led Project Coaching Playbook

A generic framework for AI-coached, human-delivered projects. This playbook provides the structural model, operational processes, agent prompts, reusable templates, and tested scripts needed to coach a project from goal to delivery using the two-agent (Coach + Tracker) pattern.

## Repository Structure

```
human-led-playbook/
├── docs/                  # Process design documents
│   ├── vsm_map.md         # Viable System Model map for the coaching pattern
│   └── working_method_protocol.md  # Operational rhythm, processes, and artifacts
├── prompts/               # Agent master prompts and templates
│   ├── project_coach_master_prompt.md  # Durable Project Coach prompt
│   └── project_tracker_prompt_template.md  # Disposable Project Tracker template
├── templates/             # Reusable data structure templates
│   ├── task_register_template.md  # Empty task register schema
│   └── dsm_template.md    # Empty Dependency Structure Matrix format
├── scripts/               # Tested tooling
│   └── render_gantt.py    # Python script to render Gantt chart from task register
└── README.md
```

## How to Use This Playbook

1. **Start a new project** by creating a project-specific repository (e.g., `odoo-project`).
2. **Launch a Project Coach** task using the master prompt from `prompts/project_coach_master_prompt.md`, giving it access to both this playbook repository and the project repository.
3. **The Coach** will guide the team through requirements elicitation, sub-project definition, and plan generation, using the templates from this repository.
4. **When the plan is approved**, the Coach produces a Tracker briefing package and a disposable Project Tracker is instantiated.
5. **The Tracker** facilitates sprint-by-sprint execution, updating the task register and re-rendering the Gantt chart as needed.
6. **If significant re-planning is needed**, the team re-engages the Coach.

## Related Repositories

- `mcsadmin/ai-build-playbook` — The companion playbook for technical builds with coding agent handoff.
- Project-specific repositories (e.g., `mcsadmin/odoo-project`) contain the project's working brief, scope document, and delivery artifacts.
