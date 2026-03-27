<!--
INSTRUCTIONS FOR AGENTS (COACH)

This Dependency Structure Matrix (DSM) is used during the planning phase to analyze task relationships and optimize sequencing before generating the Gantt chart.

READING CONVENTION: "Row depends on Column"
- A mark ('X') in row T03, column T01 means that Task T03 depends on Task T01.
- In other words, T01 must be completed before T03 can start.
- The diagonal (where row ID equals column ID) should be marked with '-' to indicate a task cannot depend on itself.
- Marks below the diagonal indicate forward dependencies (normal sequence).
- Marks above the diagonal indicate backward dependencies (iterations or feedback loops), which should be minimized or resolved if possible.

Do not modify the structure of the matrix, only add rows/columns for new tasks and mark dependencies.
-->

# Dependency Structure Matrix (DSM)

| Task ID | T01 | T02 | T03 |
|---|---|---|---|
| **T01** | - | | |
| **T02** | X | - | |
| **T03** | | X | - |

*Example interpretation:*
* *T02 depends on T01 (T01 must finish before T02 starts).*
* *T03 depends on T02 (T02 must finish before T03 starts).*
