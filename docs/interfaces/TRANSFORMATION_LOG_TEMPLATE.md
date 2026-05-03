# Transformation Log Template

**Status:** Commit-candidate draft; provisional pending controlled thin-slice handoff test  
**Author:** Manus AI  
**Intended repository location:** `docs/interfaces/TRANSFORMATION_LOG_TEMPLATE.md`  
**Adapter interface status:** revised draft candidate  
**Template status:** revised draft candidate  
**Document revision:** v0.3 housekeeping commit candidate  
**Revision file:** `TRANSFORMATION_LOG_TEMPLATE_v0_3_commit_candidate.md`  
**Related artefacts:** `docs/interfaces/ADAPTER_CONTRACT.md`; `docs/interfaces/DEPENDENCIES.md`

## 1. Purpose

This template records how preserved participant meaning is transformed into constitutional, legal, organisational, governance, software, or delivery-design propositions. It is designed for use by the constitutional/legal domain adapter after a Clean Language base output package has been created.

The template should be used whenever the adapter makes a substantive interpretive move. A substantive move is any step that could affect legal form, governance design, institutional purpose, role allocation, authority, accountability, software requirements, delivery commitments, or handoff readiness.

> **Operating discipline:** Do not allow professional categories to replace participant meaning invisibly. Record the source meaning, the base validation state, the adapter-readiness state, the adapter interpretation, the confidence level, the human validation state, and the downstream consequence.

## 2. Project-Level Log Header

Complete this section once for each project or repository instance. It establishes the dependency, source, and authority context for all later entries.

| Field | Entry |
|---|---|
| Project name |  |
| Project repository or workspace |  |
| Project stage | `propositional formation` / `lived-pattern formalisation` / `transition or growth` / `handoff to legal/build coach` / `other` |
| Clean Language source repository | `https://github.com/dilgreen/clean-language-base` |
| Clean Language base method version | `0.3` |
| Clean Language skill release version, if used | `0.1.0` |
| Clean Language manifest schema version | `0.1.0` |
| Clean Language release pin | `4dcf081035de23de10718d050afb8cbc892ae28a`; base release tag pending. |
| Source manifest file | `manifest.yaml` or project-specific source path. |
| Source validation review | `validation-review.md` or project-specific source path. |
| Source tree summary | `tree-summary.md` or project-specific source path. |
| Source node directory, if used | `nodes/` or project-specific source path. |
| Source known limitations | `known-limitations.md` or project-specific source path. |
| Constitutional/legal adapter contract | Revised draft candidate; proposed path `docs/interfaces/ADAPTER_CONTRACT.md`. |
| Transformation log template | Revised draft candidate; proposed path `docs/interfaces/TRANSFORMATION_LOG_TEMPLATE.md`. |
| Lead constitutional/legal coach |  |
| Participants or participant group |  |
| Validation route | `participant review session` / `written confirmation` / `not yet validated` / `other` |
| Legal/professional status note | This log records design interpretation unless separately reviewed and authorised as legal advice. |

## 3. Base Validation and Adapter-Readiness Fields

Each transformation entry should preserve the exact base package status fields where available. The adapter may add its own confidence and human-validation fields, but it should not replace or obscure the base status labels.

| Base field | Required values from base package | Adapter meaning |
|---|---|---|
| `validation_status` | `unreviewed`; `partially_validated`; `validated`; `needs_revision`; `rejected` | Indicates the validation state of the source material before adapter interpretation. |
| `adapter_readiness.status` | `not_ready`; `base_validated`; `adapter_handoff_prepared` | Indicates whether the source package is ready for domain interpretation or handoff. |
| `session_id` | Base-defined session identifier or equivalent locator | Allows the transformation entry to trace back to the relevant elicitation session. |
| Manifest item or node identifier | Base-defined item, node, or file identifier | Allows granular traceability from interpretation back to preserved meaning. |

If friendlier project labels are used in conversation with participants, they should be mapped back to the exact base labels in the log. The base labels are the audit trail; the friendlier labels are explanatory aids.

| Friendly label, if used | Base `validation_status` mapping | Notes |
|---|---|---|
| `raw` | `unreviewed` | Use only for material not yet participant-reviewed. |
| `partially validated` | `partially_validated` | Use where some but not all relevant meaning has been confirmed. |
| `validated` | `validated` | Use only where the base package marks the source material as validated. |
| `needs revision` | `needs_revision` | Use where participants or reviewers have indicated that the base material should be revised. |
| `rejected` or `contested beyond use` | `rejected` | Use where the source material should not be relied on as a basis for adapter interpretation. |

## 4. Adapter Confidence and Human Validation Scales

Use the following adapter-level labels consistently. These labels are distinct from base `validation_status`: they describe the adapter’s interpretation, not the validation state of the original elicited meaning.

| Adapter confidence status | Meaning | Suitable use |
|---|---|---|
| `confirmed` | The interpretation is strongly supported by source material and has been accepted by participants or authorised reviewers. | Material may be used in downstream drafting, subject to ordinary review. |
| `plausible` | The interpretation appears well-supported but has not yet been directly validated. | Material may be used for options, prompts, or provisional design. |
| `provisional` | The interpretation is useful but depends on incomplete, early-stage, or evolving material. | Material should be carried forward with caution and revisited. |
| `contested` | The interpretation is disputed by participants, sources, or reviewers. | Material should not be treated as settled. |
| `speculative` | The interpretation is exploratory and goes beyond the current source material. | Material should be used only as a prompt or hypothesis. |
| `rejected` | The interpretation has been rejected or superseded. | Material should be retained for audit but not used as an active design basis. |

| Human validation status | Meaning |
|---|---|
| `not yet reviewed` | Participants or authorised reviewers have not yet seen the adapter interpretation. |
| `reviewed - accepted` | The interpretation has been reviewed and accepted. |
| `reviewed - amended` | The interpretation has been reviewed and changed. The amendment should be recorded. |
| `reviewed - rejected` | The interpretation has been reviewed and rejected. |
| `requires further elicitation` | The interpretation has exposed a question that should return to the Clean Language elicitation process. |
| `requires professional review` | The interpretation raises legal, financial, regulatory, safeguarding, technical, or other professional issues. |

## 5. Transformation Entry Template

Copy this section for each interpretive move. Entries may be stored in a single cumulative log, one file per project phase, or one file per major handoff pack.

### Entry ID

| Field | Entry |
|---|---|
| Transformation ID | `TL-YYYYMMDD-001` |
| Date created |  |
| Created by |  |
| Last updated |  |
| Related project phase |  |
| Related lifecycle stage | `propositional formation` / `lived-pattern formalisation` / `transition or growth` / `handoff` / `other` |

### A. Source Package Reference

| Field | Entry |
|---|---|
| Clean Language source repository |  |
| Base method version |  |
| Skill release version, if used |  |
| Manifest schema version |  |
| Base release tag or commit hash |  |
| Source package path or repository location |  |
| Source manifest path |  |
| Source session ID |  |
| Source artefact | `manifest.yaml` / `validation-review.md` / `tree-summary.md` / `nodes/` / `known-limitations.md` / `other` |
| Source location within artefact | File path, heading, node ID, manifest item, transcript section, note ID, or other locator. |
| Source date |  |
| Source `validation_status` | `unreviewed` / `partially_validated` / `validated` / `needs_revision` / `rejected` |
| Source `adapter_readiness.status` | `not_ready` / `base_validated` / `adapter_handoff_prepared` |
| Related participant validation note |  |
| Related limitation or boundary warning |  |

### B. Preserved Meaning

Record the participant meaning before adapter interpretation. Use direct wording where available. If the meaning is summarised, say so. This section should be intelligible to participants and not only to professionals.

| Field | Entry |
|---|---|
| Participant wording or image |  |
| Participant distinction, metaphor, example, or pattern |  |
| What this appears to matter for, in participant terms |  |
| What should not be overwritten or collapsed |  |
| Ambiguities or fragile meanings |  |
| Does the source need further Clean Language elicitation? | `yes` / `no` / `uncertain` |

### C. Adapter Interpretation

Record the constitutional/legal interpretation as an interpretation, not as a fact. Distinguish clearly between participant language and adapter language.

| Field | Entry |
|---|---|
| Adapter interpretation |  |
| Interpretation type | `constitutional purpose` / `membership` / `authority` / `role` / `decision process` / `accountability` / `stewardship` / `asset or resource` / `conflict process` / `legal form inquiry` / `software or tooling implication` / `delivery implication` / `other` |
| Twigs–Trunk–Roots placement | `Twig` / `Trunk` / `Root` / `Tree` / `uncertain` / `not applicable` |
| Reason for placement |  |
| Alternative interpretations considered |  |
| Adapter assumptions introduced |  |
| Is any legal or professional category being introduced? | `yes` / `no` / `uncertain` |
| If yes, what category and why? |  |

### D. Confidence, Validation, and Authority

| Field | Entry |
|---|---|
| Adapter confidence status | `confirmed` / `plausible` / `provisional` / `contested` / `speculative` / `rejected` |
| Reason for confidence status |  |
| Human validation status | `not yet reviewed` / `reviewed - accepted` / `reviewed - amended` / `reviewed - rejected` / `requires further elicitation` / `requires professional review` |
| Who validated or challenged it |  |
| Date of validation or challenge |  |
| Authority status | `participant-authorised` / `coach-proposed` / `professional-review-needed` / `not authorised` / `unknown` |
| Validation notes |  |
| Does this override, amend, or qualify any prior interpretation? | `yes` / `no` / `uncertain` |
| Prior transformation IDs affected |  |

### E. Downstream Consequence

Record why the interpretation matters. If there is no meaningful downstream consequence, the entry may not be needed.

| Field | Entry |
|---|---|
| Affected downstream artefact | `constitutional options paper` / `handoff pack` / `legal drafting brief` / `governance protocol` / `software requirements` / `delivery plan` / `participant briefing` / `other` |
| Drafting or design consequence |  |
| Legal or professional consequence |  |
| Operational consequence |  |
| Software or tooling consequence |  |
| Human autonomy or consent consequence |  |
| Risk if misinterpreted |  |
| Reversibility | `easy to revise` / `moderate effort` / `hard to revise` / `legally consequential once adopted` |

### F. Open Questions and Return Loops

| Field | Entry |
|---|---|
| Open questions |  |
| Should this return to Clean Language elicitation? | `yes` / `no` / `uncertain` |
| Further elicitation prompt or focus |  |
| Should this go to constitutional/legal adapter review? | `yes` / `no` / `not yet` / `requires review` |
| Should this go to legal/build coach? | `yes` / `no` / `not yet` / `requires review` |
| Required next action |  |
| Owner of next action |  |
| Target review date |  |

### G. Change History

| Date | Change made | Reason | Made by |
|---|---|---|---|
|  |  |  |  |

## 6. Example Entry Skeleton

The following example is intentionally schematic. It shows the expected level of traceability without inventing project-specific content.

| Field | Example entry |
|---|---|
| Transformation ID | `TL-20260503-001` |
| Source repository | `https://github.com/dilgreen/clean-language-base` |
| Base method version | `0.3` |
| Skill release version | `0.1.0` |
| Manifest schema version | `0.1.0` |
| Base release tag or commit hash | `4dcf081035de23de10718d050afb8cbc892ae28a`; base release tag pending. |
| Source artefact | `tree-summary.md`, supported by `validation-review.md`. |
| Source session ID | `session-002` or equivalent source identifier. |
| Source `validation_status` | `partially_validated`. |
| Source `adapter_readiness.status` | `base_validated`. |
| Preserved meaning | Participant described the group as needing “a way to keep the work answerable to the people it affects.” |
| Adapter interpretation | This may imply an accountability or stewardship mechanism rather than only an internal management role. |
| Twigs–Trunk–Roots placement | `Root`, provisional. |
| Adapter confidence status | `plausible`. |
| Human validation status | `not yet reviewed`. |
| Downstream consequence | May affect governance protocol, membership rights, review process, or stakeholder voice mechanism. |
| Open question | Who are “the people it affects,” and what kind of answerability is meant? |
| Required next action | Return to participant review before drafting any accountability clause. |

## 7. Use in Handoff Packs

When a project moves from high-level constitutional coaching to legal drafting, organisational build, software build, or delivery coaching, the transformation log should be included in the handoff pack. It should not merely accompany the final conclusions; it should show how those conclusions were reached and where caution remains necessary.

| Handoff use | Required treatment |
|---|---|
| Legal drafting handoff | Include all entries that affect legal form, powers, duties, governance mechanisms, enforceability, and amendment. |
| Organisational design handoff | Include entries that affect roles, decision rights, accountability, culture, conflict, stewardship, and review cycles. |
| Software/build handoff | Include entries that affect workflow, permissions, data structures, audit trails, interfaces, and user autonomy. |
| Human-delivered project handoff | Include entries that affect programme design, facilitation duties, participant consent, evaluation, and adaptation. |
| Early-stage project continuation | Include entries marked provisional, speculative, or requiring further elicitation so that open meaning is not prematurely closed. |

## 8. Quality Check Before Use

Before an interpretation is relied on downstream, check that the entry answers the following questions in a way a participant or future reviewer could understand.

| Check | Question | Pass status |
|---|---|---|
| Source traceability | Can the interpretation be traced to a source repository, base package, manifest item, session, node, or explicit legal/professional requirement? |  |
| Base status preserved | Are exact `validation_status` and `adapter_readiness.status` fields recorded where available? |  |
| Meaning preservation | Is the participant’s wording, image, distinction, or pattern still visible? |  |
| Category transparency | Is it clear where adapter language begins? |  |
| Confidence honesty | Is the adapter confidence label justified by the evidence and validation state? |  |
| Human validation | Is it clear whether participants have reviewed the interpretation? |  |
| Downstream consequence | Is it clear what could change if the interpretation is wrong? |  |
| Reversibility | Is it clear how difficult the interpretation would be to unwind later? |  |
| Return loop | Is it clear whether the matter should return to elicitation, proceed to adapter review, proceed to handoff, or remain open? |  |

## 9. References

No external references are used in this draft. It is a project-internal template revised in response to Clean Language workstream commentary and the declared `clean-language-base` package versions.
