# Human-Led Project Coaching — Working Method Protocol

### A Generic Process for AI-Coached, Human-Delivered Projects

---

## 1. Purpose of This Document

This document defines the operational rhythm, processes, and key artifacts for the **Human-Led Project Coaching** pattern. It provides a practical guide for the project team and the AI agents (Project Coach and Project Tracker) on how to collaborate effectively to deliver the project.

This protocol is designed to be used in conjunction with the `vsm_map_human_led.md` document, which provides the underlying structural model for this process. Where the VSM map explains *why* the system is structured a certain way, this protocol explains *how* to operate it.

## 2. Core Principles

Our work is guided by a set of core principles that ensure clarity, accountability, and effective asynchronous collaboration.

| Principle | Description |
|---|---|
| **Repository as Single Source of Truth** | All project artifacts, plans, status documents, and decisions are stored in the designated GitHub repository. If it is not in the repository, it does not exist. |
| **The Plan is a Commitment** | The project plan and its associated Gantt chart represent a forecast and a commitment. Sprints are the mechanism for adapting to reality, and the re-planning loop is the mechanism for responding to significant change. |
| **Asynchronous First** | We default to asynchronous communication through repository commits and status documents. Synchronous sessions (the "warm" part of the rhythm) are reserved for high-value activities like planning, complex problem-solving, and decision-making. |
| **Accountability via RACI** | All work has a clearly defined **R**esponsible, **A**ccountable, **C**onsulted, and **I**nformed party. This is defined at the project level in the Working Brief and at the task level within the project plan. |

## 3. The Project Lifecycle

The project moves through three distinct but cyclical phases, each facilitated by a specific agent.

### Phase 1: Project Initiation & Planning

*   **Agent:** Project Coach
*   **Goal:** To produce a complete, realistic, and approved project plan.

This initial phase is an intensive series of coaching sessions focused on deconstructing the project goal into a concrete plan. The Project Coach guides the team through the following activities:

1.  **Requirements Elicitation:** Through a series of structured conversations, the Coach helps the team define the project's objectives, scope, and constraints.
2.  **Sub-Project Definition:** The project is broken down into loosely coupled sub-projects. For each, the Coach helps the team draft a **Sub-Project Brief** detailing its specific goals, deliverables, and acceptance criteria.
3.  **Dependency Analysis:** The Coach creates a **Dependency Structure Matrix (DSM)** to map the relationships and sequencing between all defined tasks and sub-projects.
4.  **Task Register & Plan Generation:** Using the sub-project briefs, the DSM, and the team's availability model, the Coach populates the **Task Register** — a structured table where each row is a task and columns carry all metadata (Task ID, sub-project, task name, owner, accountable person, dependencies, estimated hours, start date, end date, status). The Coach then renders a **Gantt chart** from the task register using a committed rendering script (Python). Both the task register and the rendered Gantt chart are committed to the repository.
5.  **Review and Approval:** The team reviews the complete plan for feasibility and commitment. Once approved, the planning phase is complete.

**Outcome:** An approved Project Plan, ready for handoff to the Project Tracker.

### Phase 2: Execution & Tracking

*   **Agent:** Project Tracker
*   **Goal:** To deliver the project according to the plan, sprint by sprint.

Once the plan is approved, the Project Coach's work is paused, and a disposable Project Tracker agent is instantiated with the plan. The project now enters a regular delivery cadence.

1.  **Sprint Cadence:** The project operates in fixed-length sprints, typically two weeks.
2.  **Sprint Planning:** At the start of each sprint, the team meets with the Project Tracker. The Tracker presents the next set of available tasks from the task register, and the team commits to a realistic scope for the upcoming sprint based on their documented availability.
3.  **Execution:** Team members work on their assigned tasks.
4.  **Status Updates:** Progress is reported to the Project Tracker, which updates the central project status.
5.  **Sprint Review & Reporting:** At the end of the sprint, the team reviews progress. The Tracker generates a **Sprint State Document**, which includes a burndown chart and a summary of achievements and challenges, and commits it to the repository.

### Phase 3: Re-planning & Adaptation

*   **Agent:** Project Coach
*   **Goal:** To adjust the master plan in response to significant, unforeseen change.

This phase is triggered when an issue arises that cannot be resolved within the current sprint or by adjusting the next one. This constitutes a **Course-Correction Signal** (as defined in the VSM).

1.  **Escalation:** The Project Tracker flags a major blocker, or the team identifies a need for a fundamental change (e.g., a major de-scope or a new dependency).
2.  **Engage the Coach:** The team initiates a new session with the durable Project Coach, providing the context for the required re-planning.
3.  **Re-planning Session:** The Coach reviews the latest status documents from the repository and facilitates a session to adjust the plan. This may involve revising sub-project briefs, updating the DSM, altering the task register, and re-rendering the Gantt chart.
4.  **Approve and Redeploy:** The team approves the new plan. The old Project Tracker is retired, and a new, fresh Tracker is instantiated with the revised plan.

This cycle ensures the project can adapt to major changes without losing the discipline of the original commitment.

## 4. Key Artifacts

All artifacts are stored as Markdown files in the `/docs` folder of the project's GitHub repository.

| Artifact | Purpose | Created By | Updated By |
|---|---|---|---|
| **Working Brief** | Defines the project's direction, identity, team, and decision authority (S5). | Project Coach | Project Coach (on re-plan) |
| **Scope Document** | Details the project's scope using MoSCoW, forming the boundary for all work (S5). | Project Coach | Project Coach (on re-plan) |
| **Domain Glossary** | A living document defining key terms and concepts to ensure shared understanding. | Project Coach | Team & Coach (as needed) |
| **VSM Map** | The structural model for the coaching pattern itself. | Design Coach | N/A (Framework level) |
| **Working Method Protocol** | This document; the operational guide for the project. | Design Coach | N/A (Framework level) |
| **Sub-Project Briefs** | Detailed descriptions of each independent workstream. | Project Coach | Project Coach (on re-plan) |
| **Dependency Structure Matrix (DSM)** | A matrix visualizing all task dependencies, used to optimize sequencing. | Project Coach | Project Coach (on re-plan) |
| **Task Register** | The structured data model for all tasks: IDs, owners, dependencies, dates, status. The single source of truth for task information. | Project Coach | Project Tracker (status updates) |
| **Gantt Rendering Script** | A Python script committed to the repository that renders the Gantt chart from the task register. | Project Coach | Project Coach (if schema changes) |
| **Project Plan (Gantt Chart)** | A rendered visual view of the task register. Regenerated from the task register as needed. | Project Coach | Project Coach / Tracker (on re-render) |
| **Sprint State Document** | A report on the progress and outcomes of a single sprint. | Project Tracker | Project Tracker (end of sprint) |
| **Session Handoff Notes** | A summary of decisions and actions from a synchronous coaching session. | Project Coach | Project Coach (end of session) |

## 5. Roles & Responsibilities (RACI)

| Activity | Project Sponsor | Project Lead | Team Member | Project Coach | Project Tracker |
|---|---|---|---|---|---|
| **Define Project Goal** | **A** | **R** | **C** | **C** | **I** |
| **Approve Project Plan** | **A** | **R** | **C** | **I** | **I** |
| **Execute Tasks** | **I** | **A** | **R** | **I** | **I** |
| **Report Progress** | **I** | **A** | **R** | **I** | **C** |
| **Facilitate Sprint Planning** | **I** | **C** | **R** | **I** | **A** |
| **Approve Re-plan** | **A** | **R** | **C** | **C** | **I** |
| **Facilitate Re-planning** | **C** | **R** | **R** | **A** | **I** |

---

*This document is a generic pattern stored in the `human-led-playbook` framework. It should be read alongside the project-specific working brief and scope document for the project being coached.*
