<!--
TEST FIXTURE — Structured Artifacts Build, Session 4
Dummy project: "Launch a Community Tech Festival"
3 sub-projects, 10 tasks. Created by the build agent for validation purposes.

Sub-projects:
  SP01 — Venue & Logistics
  SP02 — Programme & Speakers
  SP03 — Marketing & Comms

RACI inheritance test cases included:
  - T02 inherits Owner (R) from SP01
  - T07 inherits Owner (R) and Accountable (A) from SP02
  - T09 has no dates but has a dependency (tests date calculation)
  - T10 has no dates and no dependencies (tests warning label)
-->

# Project Task Register

| Row Type | Task ID | Sub-project | Task name | Owner (R) | Accountable (A) | Consulted (C) | Informed (I) | Dependencies | Estimated hours | Start date | End date | % Complete | Status | Sprint |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PROJECT | P01 | Community Tech Festival | | Sarah Chen | Board | | All Stakeholders | | | | | | | |
| SUBPROJECT | SP01 | Venue & Logistics | | Marcus Webb | Sarah Chen | Facilities Team | | | | | | | | |
| TASK | T01 | Venue & Logistics | Shortlist and visit candidate venues | Marcus Webb | Sarah Chen | Facilities Team | Board | | 16 | 2026-04-07 | 2026-04-10 | 100 | Complete | Sprint 1 |
| TASK | T02 | Venue & Logistics | Negotiate and sign venue contract | | | | Board | T01 | 8 | 2026-04-13 | 2026-04-14 | 60 | In progress | Sprint 1 |
| TASK | T03 | Venue & Logistics | Arrange catering and AV equipment | Marcus Webb | Sarah Chen | Catering Co | | T02 | 12 | | | 0 | Not started | Sprint 2 |
| TASK | T04 | Venue & Logistics | Conduct venue risk assessment | Marcus Webb | Sarah Chen | H&S Advisor | Board | T02 | 4 | | | 0 | Not started | Sprint 2 |
| SUBPROJECT | SP02 | Programme & Speakers | | Priya Nair | Sarah Chen | Advisory Panel | | | | | | | | |
| TASK | T05 | Programme & Speakers | Define programme themes and session formats | Priya Nair | Sarah Chen | Advisory Panel | Board | | 8 | 2026-04-07 | 2026-04-09 | 100 | Complete | Sprint 1 |
| TASK | T06 | Programme & Speakers | Identify and invite keynote speakers | Priya Nair | Sarah Chen | Advisory Panel | | T05 | 16 | 2026-04-10 | 2026-04-17 | 50 | In progress | Sprint 1 |
| TASK | T07 | Programme & Speakers | Confirm full session schedule | | | | Board | T06 | 12 | | | 0 | Not started | Sprint 2 |
| SUBPROJECT | SP03 | Marketing & Comms | | Lena Frost | Sarah Chen | Design Agency | All Stakeholders | | | | | | | |
| TASK | T08 | Marketing & Comms | Develop brand identity and event website | Lena Frost | Sarah Chen | Design Agency | Board | T05 | 24 | 2026-04-10 | 2026-04-21 | 30 | In progress | Sprint 1 |
| TASK | T09 | Marketing & Comms | Launch social media campaign | Lena Frost | Sarah Chen | | All Stakeholders | T08 | 8 | | | 0 | Not started | Sprint 2 |
| TASK | T10 | Marketing & Comms | Print and distribute physical flyers | | | | | | 6 | | | 0 | Not started | Sprint 3 |
