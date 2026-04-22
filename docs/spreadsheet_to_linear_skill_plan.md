# Comprehensive Plan: Spreadsheet-to-Linear Skill (v4)

> **Document purpose**: This plan describes the design, workflow, and implementation approach for a reusable Manus skill that transforms a project planning task-register (Markdown or Spreadsheet) into structured artifacts in Linear.app.
> 
> **Version 4 Updates**: Incorporates the expanded upstream schema (Context/Why), the refined Issue body template (simplified RACI, Cycle-based scheduling), and the automated Estimate Conversion Matrix.

---

## 1. Direction and Vision

The team's project planning workflow begins with a coaching session (facilitated by a Manus agent) that produces a task-register containing a structured breakdown of work. This register captures not just the *What* (tasks grouped by sub-project, dependencies, dates, sprints), but crucially the *Why* (context, reasoning) and the *Success Criteria* discussed during the session.

Linear.app is the team's execution environment. Today, translating the task register into Linear requires manual creation of Initiatives, Projects, and Issues — a tedious process that risks losing the rich context generated during planning.

The **spreadsheet-to-linear** skill bridges this gap. It enables Manus to read the task register, validate it against the live Linear workspace, produce a human-reviewable plan, and — upon approval — create the full Linear structure programmatically, preserving all context and metadata.

---

## 2. The Three-Phase Workflow

To shift constraint discovery (e.g., missing team members, missing labels) as far left as possible, the skill operates in three distinct phases.

### Phase 0 — Preflight Readiness

Before the team finalises their planning spreadsheet, they invoke the skill to run a preflight check.

1. **Query Linear State:** Manus uses the Linear MCP to retrieve the current workspace members, available issue labels (grouped by parent), and existing Cycles.
2. **Produce Readiness Report:** Manus generates a Markdown report showing the exact names to use for team members and the available labels. It also flags if Cycles are not yet configured and provides coaching instructions for setting them up.
3. **Generate Config & Template:** Manus produces a configuration file containing the resolved names, labels, and the **Estimate Conversion Matrix** (see Section 6). It generates a blank `.xlsx` template with data-validation dropdowns for the "Owner" and "Labels" columns.

*Outcome: The team builds their spreadsheet using validated names and labels, eliminating downstream errors.*

### Phase 1 — Parse, Resolve, and Produce Review Document

Once the team has a completed task register, they invoke the skill to map it to Linear.

1. **Markdown to Spreadsheet (Optional):** If the team provides a Markdown task register (`task_register.md`), Manus runs the incorporated `export_task_register.py` script to generate the `.xlsx` spreadsheet (complete with a colour-coded Gantt chart). If the team provides a spreadsheet directly, this step is skipped.
2. **Parse the Spreadsheet:** Manus reads the "Task Register" sheet, extracting every task row and grouping them by sub-project.
3. **Cross-Reference & Convert:** Manus queries Linear again to ensure the workspace state hasn't changed since Phase 0. It matches Owner names to Linear members, validates Sprint assignments against existing Cycles, and **converts Estimated Hours to Linear Estimate Points** using the conversion matrix.
4. **Produce Review Document:** Manus generates a structured Markdown document showing exactly what will be created: the Initiative name, the Projects (sub-projects), and every Issue with its mapped assignee, dependencies, Cycle, converted estimate, and the full text of the *Why* and *Acceptance Criteria*. Any remaining ambiguities are flagged for human resolution.

*Outcome: The team reviews the proposed Linear structure, makes any final corrections directly in the Markdown document, and approves it.*

### Phase 2 — Create Linear Artifacts (Execution)

When the team returns the approved review document, Manus executes the creation plan.

1. **Create/Identify Initiative:** Manus links to an existing Initiative or creates a new one.
2. **Create Projects:** For each sub-project, Manus creates a Linear Project linked to the Initiative and the team. Start and target dates are derived from the task dates.
3. **Create Issues (First Pass):** Manus creates all Issues using the structured template (see Section 5), assigning them to the correct Project, Cycle, and Owner, and setting the native `estimate` field.
4. **Set Dependencies (Second Pass):** Once all Linear Issue IDs are known, Manus makes a second pass to set `blockedBy` relations based on the spreadsheet dependencies.
5. **Summary Report:** Manus delivers a final report with links to all created artifacts.

---

## 3. Script Incorporation and Expanded Schema

The existing `export_task_register.py` script (which generates the spreadsheet and Gantt chart from Markdown) will be incorporated into the skill as a refactored module.

**Refactoring Requirements:**
- **Parameterisation:** The hardcoded sub-project list, colour palette, and sprint names must be extracted into a configuration file generated during Phase 0.
- **Preflight Injection:** The script will accept the Phase 0 preflight data to inject validation references (e.g., valid Owner names, available labels) into the generated spreadsheet.
- **Preserve Gantt:** The direct-colour Gantt chart logic will be preserved, driven by the new configuration.

**Crucially, the upstream schema must be expanded.** To capture the context generated during the coaching session, the Markdown task register (and the resulting spreadsheet) must include three new columns:
1. **Context / Why:** A paragraph explaining the reasoning behind the task.
2. **Task Breakdown:** A bulleted or numbered list of sub-steps.
3. **Acceptance Criteria:** A numbered list of conditions that must be met for the task to be considered done.

The coach agent must be instructed to populate these columns, using HTML `<br>` tags or single-line representations in the Markdown table, which the export script will translate into proper line breaks in the Excel sheet.

---

## 4. Ontology Mapping Summary

The skill relies on a strict mapping between the team's planning vocabulary and Linear's native affordances.

| Planning Term | Linear Artifact | Notes |
|---|---|---|
| Project | Initiative | Top-level container. |
| Sub-project | Project | Mid-level container. Supports start/target dates. |
| Task | Issue | Atomic unit of work. |
| Sprint | Cycle | Auto-generated time-boxes. Cannot be created ad-hoc. |
| Dependencies | `blockedBy` relation | Formal end-to-start blocking relations between Issues. |
| Estimated Hours | Issue `estimate` | Converted to abstract points via the Conversion Matrix. |

---

## 5. Structured Issue Template

When creating Issues in Linear, the skill will use a structured Markdown template that combines the user's preferred requirement-driven format (What/Why/Success Criterion) with the metadata from the spreadsheet. 

**Issue Title:**
`[{Task ID}] {Task name}`

**Issue Description Body:**
```markdown
### What
{Task name}

**Context / Why:**
{Context / Why}

### Task Breakdown
{Task Breakdown — formatted as Markdown checkboxes}

### Acceptance Criteria
{Acceptance Criteria — formatted as a numbered list}

---
*Auto-generated from planning register*

### Planning Metadata
- **Accountable:** {Accountable (A)} *(if different from Assignee)*
- **Sprint / Cycle:** {Sprint}
- **Estimated Hours:** {Estimated hours} hrs *(= {Estimate Points} pts on team scale)*
- **Dependencies:** {Dependencies}
- **MoSCoW:** {MoSCoW label}
```

**Design Rationale:**
1. **Cycles replace Start/End Dates:** Because Issues live within Cycles (Sprints), the Cycle provides the scheduling container. There is no Start Date or End Date in the Issue body.
2. **RACI is simplified:** The native Linear `Assignee` field carries the Responsible role. Only the Accountable person is noted in the description, and only when they differ from the Assignee.
3. **Estimates are dual-tracked:** The native `estimate` field receives the converted points value, enabling Linear's velocity tracking. The original hours figure is retained in the description for reference.

---

## 6. Estimate Conversion Matrix

Because the planning spreadsheet captures "Estimated Hours" but Linear requires abstract points (e.g., T-shirt sizes or Fibonacci), the skill includes an automated conversion module (`estimate_conversion.py`).

During Phase 0, the team configures which Linear scale they use. The skill then automatically converts hours to points during Phase 1.

**Default T-Shirt Scale Conversion:**
- ≤ 2 hours = 1 point (XS)
- 2.1 – 4 hours = 2 points (S)
- 4.1 – 8 hours = 3 points (M)
- 8.1 – 16 hours = 4 points (L)
- > 16 hours = 5 points (XL)

---

## 7. Idempotency and Error Handling

The skill is designed to be safely re-runnable.

- **Project Idempotency:** Before creating a Project, the skill searches for an existing Project with the same name under the same Initiative. If found, it updates rather than duplicates.
- **Issue Idempotency:** Before creating an Issue, the skill searches for an existing Issue whose title contains the same Task ID prefix (e.g., `[T01]`) within the same Project. If found, it updates rather than duplicates.
- **Cycle Setup:** Because Cycles cannot be created via the API, Phase 0 and Phase 1 explicitly check for their existence and provide coaching instructions if they are missing.
- **Unresolved Names:** If an Owner name cannot be matched to a Linear member, the Phase 1 review document flags it for human correction before any artifacts are created.

---

## 8. Skill File Structure

```
spreadsheet-to-linear/
├── SKILL.md                              # Workflow instructions (three phases)
├── scripts/
│   ├── preflight.py                      # Phase 0: queries Linear, produces readiness report
│   ├── export_task_register.py           # Markdown → spreadsheet (refactored from existing)
│   ├── parse_spreadsheet.py              # Phase 1: spreadsheet → structured JSON
│   ├── estimate_conversion.py            # Phase 1: hours → Linear points conversion
│   └── config_schema.py                  # Shared schema for sub-project/sprint config
├── references/
│   ├── ontology-mapping.md               # Revised Linear ontology mapping
│   └── spreadsheet-schema.md             # Expected column layout and types
└── templates/
    ├── review_template.md                # Phase 1 review document template
    ├── preflight_report_template.md      # Phase 0 readiness report template
    └── issue_body_template.md            # The structured issue description template
```

---
*End of Plan*
