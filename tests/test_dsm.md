<!--
TEST FIXTURE — Structured Artifacts Build, Session 4
Dummy project: "Launch a Community Tech Festival"
DSM for 10 tasks. Reading convention: Row depends on Column.
An 'X' in row Ti, column Tj means Ti depends on Tj (Tj must finish before Ti starts).
-->

# Dependency Structure Matrix (DSM) — Community Tech Festival

| Task ID | T01 | T02 | T03 | T04 | T05 | T06 | T07 | T08 | T09 | T10 |
|---|---|---|---|---|---|---|---|---|---|---|
| **T01** | - | | | | | | | | | |
| **T02** | X | - | | | | | | | | |
| **T03** | | X | - | | | | | | | |
| **T04** | | X | | - | | | | | | |
| **T05** | | | | | - | | | | | |
| **T06** | | | | | X | - | | | | |
| **T07** | | | | | | X | - | | | |
| **T08** | | | | | X | | | - | | |
| **T09** | | | | | | | | X | - | |
| **T10** | | | | | | | | | | - |

*Reading: Row depends on Column. Example: T02 depends on T01 (T01 must finish before T02 starts).*
*T10 has no dependencies — it is an independent task with no dates specified (tests the warning label in the Gantt renderer).*
