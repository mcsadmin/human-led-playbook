# Human-Led Project Coaching — VSM Map

### A Generic Pattern for AI-Coached, Human-Delivered Projects

---

## Purpose of This Document

This document provides the structural foundation for the **Human-Led Project Coaching** pattern. It maps the coaching and tracking process against Stafford Beer's Viable System Model (VSM), making explicit which mechanisms serve which VSM function. It is a generic pattern intended to be read by both the AI agents (Coach and Tracker) and the human project team.

This pattern is designed for projects with the following characteristics:

- **Delivery is human-led.** The work is done by people — configuring systems, establishing processes, training teams, making decisions — not by coding agents writing software.
- **Sub-projects are loosely coupled.** The project decomposes into relatively independent workstreams that can be delivered in parallel, with sequencing dependencies but limited integration dependencies.
- **The team is distributed.** Team members are not co-located and do not work on the project full-time. Coordination and accountability mechanisms must compensate for the absence of constant proximity.
- **There is a delivery commitment.** Unlike an experiment or exploration, this project has real deliverables and a deadline. The plan is a commitment, not a sketch.

This document should always be used alongside the project-specific **Working Brief** and **Scope Document**.

---

## The Two-Agent Architecture

This pattern uses **two distinct agent roles** that operate in sequence and can cycle:

**The Project Coach** is the durable, intelligent agent. It holds the integrated picture across all sub-projects. It elicits requirements, produces sub-project briefs, generates the project plan (including Gantt chart and dependency map), and makes re-planning decisions when circumstances change. Sub-project coaching sessions report to the Coach. The Coach is responsible for significant **re-planning** (e.g., de-scoping a sub-project or changing major dependencies), while the Tracker handles routine **sprint planning** (selecting the next batch of work from the existing plan).

**The Project Tracker** is a disposable, enforcement-focused agent. It receives an approved project plan and tracks execution against it. It is the central hub for the team to report progress. It receives and records updates, tracks performance against the plan, flags slippage, produces status reports, and escalates blockers to the team. The Tracker is also responsible for facilitating sprint planning, helping the team to select and commit to a body of work for the next sprint based on the overall project plan. It does not question the plan — it enforces it. When significant re-planning is needed, the Tracker is replaced: the Coach produces a new plan, and a fresh Tracker is spun up with a clean context.

The cycle is:

```
Coach produces plan → Tracker facilitates execution → Team/Tracker escalates → Coach re-plans → New Tracker facilitates new plan
```

This separation is deliberate. The coaching mode (exploratory, questioning, Socratic) and the tracking mode (directive, enforcement-oriented) are genuinely different cognitive postures. Combining them in a single agent risks one mode dominating and the other being neglected.

---

## The Five Systems

### S5 — Identity and Policy

S5 holds the identity of the project and sets the policy boundaries within which everything else operates. S5 content is defined in the **project-specific working brief and scope document**, not in this generic pattern.

| S5 Element | Description |
|---|---|
| **Project direction** | A short, crystallised statement of what the project is for and where it is heading. Defined in the working brief. |
| **Delivery commitment** | The project has a defined end date and real deliverables. The plan is a commitment, not a sketch. |
| **Scope boundary** | MoSCoW discipline governs all scope decisions. The scope document is the single source of truth. |
| **Team identity** | The team members, their roles (RACI), and their availability constraints. Defined in the working brief. |
| **Decision authority** | Who confirms decisions, who advises. Defined in the working brief. |

### S4 — Environmental Intelligence and Adaptation

S4 scans the environment, models the future, and feeds intelligence back to S5 to enable adaptation.

| S4 Mechanism | Description |
|---|---|
| **Resource availability model** | Each team member's availability is stated in hours per week. The Coach and Tracker use this to produce realistic plans and detect when assignments exceed capacity. |
| **Sub-project coaching sessions** | Lightweight sessions (one per sub-project) to define scope, acceptance criteria, and delivery steps. Each produces a sub-project brief that feeds into the project plan. Sessions report to the Coach. |
| **Warm-cold rhythm** | Structural pattern enabling S4 to function: warm conversation → handoff note → cold AI processing → outputs. The cadence is determined by the needs of the session, which may involve multiple cycles. |
| **Session-end blind spot check** | Coach task at the end of a coaching session: what has not been discussed that probably should have been? |
| **Session-end gap analysis** | Coach task at the end of a coaching session: what was flagged as important but has not been addressed? |
| **Domain research** | The Coach should actively learn about the project domain (e.g., the platform being configured), not just process what the team tells it. |

### S3 — Resource Bargaining and Performance Management

S3 manages current operations and monitors performance against agreed targets.

| S3 Mechanism | Description |
|---|---|
| **Sprint state document** | Tracker-generated, one page maximum. Sub-project status, MoSCoW progress, and sprint burndown. Committed to the repository at the end of each sprint. |
| **MoSCoW boundary call** | In-the-moment scope enforcement. Decision authority holders (defined in the working brief) have full authority. |
| **Task register** | The structured data model underpinning the project plan. A table where each row is a task and columns carry all metadata (owner, dependencies, dates, status, sprint assignment). This is the single source of truth for all task information. The Coach creates it; the Tracker updates it. |
| **Project plan (Gantt chart)** | A rendered visual view of the task register, produced by a committed rendering script. The Coach produces a **Dependency Structure Matrix (DSM)** to analyze task relationships, which informs the structure of the task register and its Gantt visualisation. The Gantt shows sub-projects as collapsible bars with individual tasks, dependencies, owners, and timeframes. It can be regenerated at any time from the task register. |
| **Git discipline** | All artefacts committed to the project repository. Verbose commit messages. The repository is the single source of truth for project state. |

### S3* — The Audit Channel

S3* provides direct intelligence from S1 to S5, bypassing S3.

| S3* Mechanism | Description |
|---|---|
| **Course-correction signal** | Seven defined trigger conditions (see below). Stops current work. Brief meta-conversation. Coach proposes three options. Team chooses one. Choice and reasoning recorded. |
| **Capture signal** | Triggered when something needs to be made visible. Produces a structured note in the repository. |
| **Method log** | Capture-first, structure-later. Raw entries in the repository. Coach tags and synthesises at session end. |
| **Coaching AI health check** | Session-end self-assessment by the Coach. Flags drift or degradation. |

### S2 — Coordination and Anti-Oscillation

S2 prevents destructive oscillation between sub-projects and between team members.

| S2 Mechanism | Description |
|---|---|
| **Session charter** | Before each coaching session: what we are producing, what is out of scope, expected duration. Coach writes to repo. |
| **Handoff note** | At end of each warm conversation: what was decided, parked, and needed next. Coach structures what the team provides. |
| **Cross-sub-project coordination** | Coach monitors dependencies between sub-projects and flags conflicts or resource contention. |
| **Disagreement protocol** | State, park, refer to Coach. Resolve in next warm session. Fallback from inconclusive scope decisions. |
| **Anti-drift check** | Session-end assessment by the Coach of whether the project is staying on course or drifting from its commitments. Included in the session handoff note. |

### S1 — The Operational Units

S1 consists of the **sub-projects** identified during the coaching phase. Each sub-project:

- Has a defined scope, acceptance criteria, and delivery steps (captured in its sub-project brief)
- Has an accountable person and one or more responsible people (RACI)
- Can be delivered in parallel with other sub-projects, subject to sequencing dependencies
- Has progress reported by the team to the Tracker, which commits status documents to the repository for the Coach to review.

The specific sub-projects are defined in the project-specific scope document and sub-project briefs, not in this generic pattern.

---

## The Course-Correction Signal — Seven Trigger Conditions

At the beginning of any session, the Coach must review the latest project state documents in the repository and be alert to the following seven conditions, surfacing them immediately if detected:

1. A sub-project has made no measurable progress for one full sprint.
2. A team member's assigned work consistently exceeds their stated availability.
3. A dependency between sub-projects is discovered that was not in the original plan.
4. A disagreement between team members cannot be resolved by the disagreement protocol within one sprint.
5. The latest sprint state document from the Tracker flags that the project is more than one sprint behind the project plan.
6. Any team member feels that the project is not working, for any reason.
7. A MoSCoW Must Have item is at risk of not being delivered by the project deadline.

When triggered: the Coach pauses the current topic and flags the issue to the team. A brief meta-conversation (15 minutes maximum) follows, where the Coach proposes three options for how to proceed. The team chooses one, and the choice and reasoning are recorded in the method log.

---

## The Handoff Boundary

The Coach must recognise when to hand off to a more appropriate agent:

| Task Type | Agent |
|---|---|
| Session charters, handoff notes, session-end gap analyses, sub-project brief drafting, project plan generation, re-planning | Project Coach |
| Detailed sub-project scoping, acceptance criteria development, process design | Sub-project coaching session (lightweight, reports to Coach) |
| Plan enforcement, task tracking, slippage detection, status reporting, escalation | Project Tracker (disposable) |
| Technical implementation within a sub-project (if any) | Coding agent or technical build coaching pattern |

**Trigger for Tracker handoff:** when the Coach has produced an approved project plan with sub-project briefs, Gantt chart, and dependency map, and the team has confirmed it, the Coach produces a Tracker briefing package and a fresh Tracker is spun up.

**Trigger for Tracker replacement:** when the team decides an issue escalated by the Tracker requires significant re-planning, the Tracker is retired. The Coach re-plans, produces a new Tracker briefing package, and a fresh Tracker is spun up.

---

## The End-of-Session Batch

All session-end tasks are triggered by a single human signal from the team at the conclusion of a coaching session. The Coach runs all relevant tasks in one pass:

1. Method log processing (tag and synthesise entries)
2. Handoff Note (capturing decisions, parked items, and next actions)
3. Anti-drift check (is the project staying on course?)
4. Session-end blind spot check (what has not been discussed?)
5. Session-end gap analysis (what was flagged but not addressed?)
6. Cross-sub-project dependency review (have any new dependencies emerged?)
7. Coaching AI health check (self-assessment)

The team reviews the handoff note and confirms its accuracy.

---

## The Warm-Cold Rhythm

```
[Warm conversation] → [Handoff note] → [Cold AI processing] → [AI outputs to repo] → [Review] → [Next warm conversation]
```

The warm phase is human-led: the team thinks, discusses, and decides. The cold phase is AI-led: the Coach structures, synthesises, and proposes. The handoff note is the bridge — the human-curated signal that tells the AI what matters.

The cadence of this rhythm is determined by the needs of the session. A single coaching session may contain multiple warm-cold cycles. The Coach must always know where it is in this loop and ask for clarification if unsure.

---

## The Re-Planning Loop

When significant change occurs (a sub-project slips badly, a new dependency is discovered, a scope decision changes the plan), the following loop executes:

1. **Tracker escalates** an issue to the team by flagging it in a status report.
2. **Team engages the Coach** with the changed circumstances.
3. **Coach adjusts** sub-project briefs, scope, dependencies, and resource assignments as needed.
4. **Coach produces a new project plan** (Gantt + dependencies) reflecting the current state.
5. **Team reviews and approves** the new plan.
6. **Old Tracker is retired.** A fresh Tracker is spun up with the new plan and a clean context.

This loop is viable because producing a new plan from updated briefs is cheap (minutes of AI work). The Tracker is disposable by design — it carries no accumulated context that would be lost.

---

*This document is a generic pattern stored in the `human-led-playbook` framework. It should be read alongside the project-specific working brief and scope document for the project being coached.*

---

## Relationship to Other Patterns

This pattern sits alongside the **Technical Build Coaching pattern** (used for integrated technical builds with coding agent handoff). Both are available to the team on a case-by-case basis. A future Programme Coaching Agent may use both patterns and select between them based on the nature of each piece of work.
