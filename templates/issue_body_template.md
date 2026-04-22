# Issue Body Template (v2)

> **Usage:** This template is used by the `spreadsheet-to-linear` skill during Phase 2 (Execution) to populate the `description` field of each newly created Linear Issue. Placeholder tokens in `{curly braces}` are replaced by the skill at runtime.

---

## Template

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
- [ ] Step 1
- [ ] Step 2

### Acceptance Criteria
{Acceptance Criteria — formatted as a numbered list}
1. Criterion one
2. Criterion two

---
*Auto-generated from planning register*

### Planning Metadata
- **Accountable:** {Accountable (A)} *(if different from Assignee)*
- **Sprint / Cycle:** {Sprint}
- **Estimated Hours:** {Estimated hours} hrs *(= {Estimate Points} pts on team scale)*
- **Dependencies:** {Dependencies}
- **MoSCoW:** {MoSCoW label}
```

---

## Field Notes

| Token | Source | Linear Mapping |
| :--- | :--- | :--- |
| `{Task ID}` | Spreadsheet column A | Prefix in Issue title for idempotency |
| `{Task name}` | Spreadsheet column B | Issue `title` (native) |
| `{Context / Why}` | Spreadsheet expanded column | Description body (Markdown) |
| `{Task Breakdown}` | Spreadsheet expanded column | Description body — rendered as interactive checkboxes by Linear |
| `{Acceptance Criteria}` | Spreadsheet expanded column | Description body |
| `{Accountable (A)}` | Spreadsheet RACI column | Description body only — omit if same as Assignee |
| `{Sprint}` | Spreadsheet Sprint column | Issue `cycleId` (native) — text shown for human reference |
| `{Estimated hours}` | Spreadsheet hours column | Description body (reference only) |
| `{Estimate Points}` | Derived via conversion matrix | Issue `estimate` (native) |
| `{Dependencies}` | Spreadsheet dependencies column | Issue `blockedBy` relations (native) — text shown for human reference |
| `{MoSCoW label}` | Spreadsheet MoSCoW column | Issue Label from "MoSCoW" label group (native) |

---

## Design Rationale

Three decisions distinguish this template from the prior v1 draft:

**1. Cycles replace Start/End Dates.** Because Issues live within Cycles (Sprints), the Cycle provides the scheduling container. There is no Start Date or End Date in the Issue body. The Sprint name is shown in the metadata block for human readability, but the functional scheduling link is the native `cycleId` assignment.

**2. RACI is simplified to Accountable only.** The native Linear `Assignee` field carries the Responsible role. Only the Accountable person is noted in the description, and only when they differ from the Assignee. Consulted and Informed roles are not recorded at the Issue level; they belong at the Project level.

**3. Estimate appears in both native and human-readable form.** The native `estimate` field receives the converted points value (via the conversion matrix), enabling Linear's velocity tracking and project graphs. The original hours figure is retained in the description for reference and auditability.
