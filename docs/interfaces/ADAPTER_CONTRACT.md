# Constitutional/Legal Domain Adapter Contract

**Status:** Commit-candidate draft; provisional pending controlled thin-slice handoff test  
**Author:** Manus AI  
**Intended repository location:** `docs/interfaces/ADAPTER_CONTRACT.md`  
**Adapter interface status:** revised draft candidate  
**Document revision:** v0.3 housekeeping commit candidate  
**Revision file:** `constitutional_legal_adapter_contract_v0_3_commit_candidate.md`  
**Related documents:** `DEPENDENCIES_v0_3_commit_candidate.md`; `TRANSFORMATION_LOG_TEMPLATE_v0_3_commit_candidate.md`

## 1. Purpose

This document defines the contract between the **domain-agnostic Clean Language base package** and the **constitutional/legal design coaching repository**. Its purpose is to prevent two forms of drift. The first is **methodological drift**, where the constitutional/legal repository inadvertently becomes a second source of truth for Clean Language elicitation. The second is **semantic drift**, where participant meaning is silently converted into legal, constitutional, organisational, software, or delivery categories before it has been preserved and validated.

The constitutional/legal repository therefore operates as a **domain adapter repository**. It may interpret elicited material for constitutional, governance, legal, organisational, drafting, software, or project-delivery purposes, but it must do so downstream of the Clean Language base package and with a visible transformation record.

> **Core rule:** The Clean Language base preserves and organises participant meaning. The constitutional/legal adapter interprets that meaning for legal and governance design only after the base material has been captured, versioned, and traceably carried forward.

## 2. Architectural Position

The Clean Language base repository remains the canonical source for the elicitation method, base output templates, base manifest schema, release checklist, and Manus skill package. The constitutional/legal repository does not fork or edit that base. Instead, it declares a versioned dependency on the current Clean Language base release and supplies a domain-specific adapter that explains how elicited material is used in the legal and constitutional drafting process.

The current dependency declaration names the canonical base as `https://github.com/dilgreen/clean-language-base`, with `base_method_version: 0.3`, `skill_release_version: 0.1.0`, and `manifest_schema_version: 0.1.0`. No GitHub release tag was found during the housekeeping check, so this draft also records the current default-branch release pin as commit `4dcf081035de23de10718d050afb8cbc892ae28a`, labelled by its commit message as “Initial Clean Language base package release”. Compatibility remains **provisional pending a controlled thin-slice handoff test**, because the adapter has not yet been exercised against a complete base output package in a live or simulated project.

| Layer | Canonical owner | Main function | May change base meaning? | Output status |
|---|---|---|---|---|
| Clean Language base | Clean Language repository | Elicit, preserve, sequence, validate, and lightly structure participant meaning. | No. | Base output package and manifest. |
| Constitutional/legal adapter | Constitutional/legal repository | Interpret preserved material into constitutional design questions, legal framing options, governance mechanisms, and drafting or build pathways. | Yes, but only as explicit interpretation. | Adapter outputs with transformation records. |
| Project repository | Project-specific fork or instance | Hold participant records, validations, decisions, transformation logs, drafts, and handoff packs for one institutional project. | No silent changes; project decisions must be recorded. | Project record and deliverables. |

This separation allows the base method to remain portable across domains, while allowing the constitutional/legal repository to retain its specialised understanding of **Twigs, Trunk, Roots, Trees, lifecycle stage, legal form, governance design, stewardship, authority, enforceability, and institutional handoff**.

## 3. Base Inputs Expected by the Adapter

The adapter should not begin substantive legal or constitutional interpretation until a minimum Clean Language base output package exists. The constitutional/legal adapter currently expects the following base package artefacts, aligned with the Clean Language base package terminology.

| Base input | Expected current name or field | Adapter use |
|---|---|---|
| Base manifest | `manifest.yaml` using `manifest_schema_version: 0.1.0` | Provides the versioned source record, package metadata, session references, validation state, and adapter-readiness information. |
| Validation review | `validation-review.md` and manifest `validation_status` fields | Helps distinguish validated meaning from material that is unreviewed, partially validated, needs revision, or has been rejected. |
| Tree summary | `tree-summary.md` | Provides a neutral summary of the elicited tree-like meaning structure before domain-specific constitutional/legal translation. |
| Node records | Optional `nodes/` files or equivalent node-level records | Allows the adapter to trace particular interpretive moves to specific participant expressions, distinctions, examples, or patterns. |
| Known limitations | `known-limitations.md` or equivalent manifest notes | Warns the adapter against over-interpreting fragile, ambiguous, contested, or incomplete source material. |
| Adapter readiness | Manifest `adapter_readiness.status` | States whether the base package is `not_ready`, `base_validated`, or `adapter_handoff_prepared`. |

The adapter may proceed with partial inputs only where the project explicitly records that it is working in an early-stage, exploratory, or provisional mode. In that case, outputs must be labelled as provisional and the transformation log must make the limitation visible.

## 4. Validation and Adapter-Readiness Discipline

The adapter should read base validation and adapter-readiness fields before interpreting the material. These fields do not replace human judgement, but they prevent the adapter from treating every source item as equally settled.

| Base field | Expected values | Adapter consequence |
|---|---|---|
| `validation_status` | `unreviewed`; `partially_validated`; `validated`; `needs_revision`; `rejected` | Determines how confidently the adapter may rely on the source material. |
| `adapter_readiness.status` | `not_ready`; `base_validated`; `adapter_handoff_prepared` | Determines whether the material should remain in elicitation, proceed to cautious adapter interpretation, or be prepared for formal handoff. |
| `session_id` or source locator | Base-defined identifier | Allows each transformation-log entry to trace back to the exact source material. |
| Manifest item or node identifier | Base-defined identifier | Allows downstream reviewers to audit the interpretive chain. |

If a source item is `unreviewed`, `needs_revision`, `rejected`, or attached to `adapter_readiness.status: not_ready`, the adapter may still use it as a prompt for inquiry, but should not treat it as a drafting-ready constitutional or legal basis.

## 5. Permitted Adapter Moves

The constitutional/legal adapter may make domain-specific interpretive moves that the base Clean Language package should not make. These moves are legitimate because the adapter is expected to support constitutional and legal design, not merely elicitation.

| Adapter move | Description | Required discipline |
|---|---|---|
| Constitutional interpretation | Identify what elicited material may imply for purpose, authority, membership, stewardship, accountability, or institutional identity. | Cite the base artefact, manifest item, node, session, or validation note that prompted the interpretation. |
| Twigs–Trunk–Roots refinement | Revisit provisional placement of concrete activities, central commitments, and enabling structures in light of legal/governance design. | Distinguish participant language from adapter classification. |
| Lifecycle assessment | Assess whether the group is in propositional formation, lived-pattern formalisation, transition, dispute, growth, or codification mode. | Record uncertainty and avoid treating lifecycle placement as a legal conclusion. |
| Legal form inquiry | Identify questions relevant to company, trust, association, cooperative, contractual, charity, commons, software, or hybrid institutional structures. | Frame as inquiry or option unless and until legal advice is obtained where required. |
| Governance design translation | Translate meaning into candidate roles, rights, duties, consent processes, decision rules, conflict processes, review cycles, and amendment mechanisms. | Preserve an audit trail from participant meaning to proposed governance mechanism. |
| Handoff preparation | Prepare narrowed briefs for legal drafting, organisational design, software build, human-delivered project delivery, or other downstream work. | Include readiness criteria, transformation-log references, and unresolved questions. |

The adapter’s role is active and creative, but not unconstrained. It may translate, but only where the translation is **visible, contestable, and reversible**.

## 6. Prohibited Adapter Moves

Certain actions would compromise the integrity of the shared architecture and should be prohibited unless a project-specific human decision expressly overrides them and records why.

| Prohibited move | Reason |
|---|---|
| Editing the Clean Language base method inside the constitutional/legal repository | This would create competing master copies and undermine the Clean Language repository as canonical source. |
| Importing the Clean Language base by copying unmanaged files into the adapter repository | This creates version drift and makes it unclear which layer governs the method. |
| Treating provisional Twigs–Trunk–Roots placement as final constitutional design | Early placement is a sensemaking aid, not a completed design conclusion. |
| Converting participant language directly into legal clauses without a transformation record | This hides interpretive judgement and can give false authority to legal language. |
| Overwriting participant meaning with professional categories | The process exists to preserve human meaning, not to subordinate it to technical frames. |
| Presenting adapter outputs as legal advice where that is not authorised | The repository may support legal design and drafting, but professional legal advice remains a separate status and responsibility. |
| Ignoring base `validation_status` or `adapter_readiness.status` | This would allow the adapter to rely on material that the base layer has marked as not ready, unresolved, or rejected. |

## 7. Required Transformation Record

Every substantive adapter output should be accompanied by a transformation record. This does not need to be bureaucratic, but it should be sufficient to let a participant, coach, lawyer, drafter, software builder, delivery lead, or future agent understand how a conclusion emerged.

| Record field | Required content |
|---|---|
| Source reference | Link or identifier for the base artefact, `session_id`, manifest item, node, validation note, or prior project document. |
| Base validation status | Exact source `validation_status`, where available. |
| Base adapter-readiness status | Exact source `adapter_readiness.status`, where available. |
| Preserved meaning | The relevant participant wording, image, distinction, example, or pattern before domain translation. |
| Adapter interpretation | The constitutional, legal, organisational, software, delivery, or governance interpretation being proposed. |
| Confidence status | Whether the interpretation is confirmed, plausible, provisional, contested, speculative, or rejected. |
| Human validation status | Whether participants have reviewed, accepted, amended, rejected, or returned the interpretation for further elicitation. |
| Downstream consequence | What drafting, design, handoff, build, or decision work depends on this interpretation. |
| Open questions | What remains unresolved and should not be collapsed into premature form. |

This transformation record is the practical safeguard that allows the adapter to be domain-specific without becoming opaque.

## 8. Version and Dependency Rule

The constitutional/legal repository must declare its Clean Language dependency explicitly. At minimum, each project or repository release should record the Clean Language base repository, base method version, manifest schema version, release-checklist treatment, release tag or commit pin, Manus skill package version if used, adapter version, transformation-log template version, and compatibility status.

| Dependency | Current declaration for this draft candidate |
|---|---|
| Clean Language repository | `https://github.com/dilgreen/clean-language-base` |
| Clean Language base method version | `0.3` |
| Clean Language manifest schema version | `0.1.0` |
| Clean Language skill release version | `0.1.0` |
| Clean Language release checklist treatment | Included in the base package release `0.1.0`; no unsupported standalone checklist version is claimed. |
| Adapter contract | Revised draft candidate, document revision v0.3, proposed path `docs/interfaces/ADAPTER_CONTRACT.md`. |
| Transformation log template | Revised draft candidate, document revision v0.3, proposed path `docs/interfaces/TRANSFORMATION_LOG_TEMPLATE.md`. |
| Base release pin | No GitHub release tag found; current default-branch pin is commit `4dcf081035de23de10718d050afb8cbc892ae28a`. |
| Compatibility status | `provisional`, pending controlled thin-slice handoff test. |

The constitutional/legal repository may now declare a concrete dependency on the Clean Language base release. It should not yet claim full operational compatibility until the first controlled thin-slice handoff has confirmed that base outputs can be consumed, interpreted, logged, and reviewed without boundary confusion.

## 9. Human Autonomy and Validation

This adapter exists to support human participants in giving durable form to institutional meaning. It should therefore preserve the distinction between **what participants have said**, **what the coach has inferred**, **what the base package has validated**, **what the adapter has proposed**, **what legal drafting may require**, and **what the group has actually authorised**.

The adapter should actively protect participants from premature closure. Where a constitutional/legal form appears attractive, the adapter should still ask whether that form reflects the living pattern, emerging proposition, or human purpose being expressed. Where the material is early and propositional, the adapter should produce provisional scaffolding rather than false constitutional finality.

## 10. Minimum Compatibility Checklist

Before the constitutional/legal adapter is used in a project, the following checks should be satisfied.

| Check | Question | Status |
|---|---|---|
| Canonical source declared | Has the Clean Language base source and version been identified? | Required; currently declared in dependency document. |
| Base package fields available | Are `manifest.yaml`, `validation-review.md`, `tree-summary.md`, and any relevant `nodes/` or limitation files available? | Required for full handoff. |
| Adapter readiness checked | Has `adapter_readiness.status` been reviewed before adapter work begins? | Required. |
| Adapter boundary understood | Is it clear what the base layer does and what the adapter may add? | Required. |
| Transformation logging enabled | Is there a template or process for recording interpretive moves? | Required. |
| Participant validation route present | Is there a route for participants to confirm, amend, or reject interpretations? | Required. |
| Legal-status warning present | Is it clear when outputs are design material rather than legal advice? | Required. |
| Handoff readiness path present | Is there a way to decide when material is ready for legal drafting, project delivery, software build, or other downstream work? | Required. |

## 11. Open Questions for Review

The Clean Language base package now provides the base method version, skill release version, manifest schema version, and base-side handoff architecture required for the constitutional/legal adapter to declare a concrete dependency. The next unresolved issue is not whether the base package exists, but whether the constitutional/legal adapter has successfully consumed it in practice.

The first controlled test should therefore be a **thin-slice handoff**. A small Clean Language base output package should be passed into the constitutional/legal adapter, transformed into a limited constitutional design output, recorded in the transformation log, and then checked for traceability, boundary integrity, participant intelligibility, and practical usefulness for downstream drafting or build work.

A secondary question is whether the constitutional/legal repository should eventually include a machine-readable adapter manifest in addition to this human-readable contract. My recommendation remains to begin with this contract, the dependency declaration, and the transformation log template, then add a machine-readable schema only after the thin-slice test shows what needs to be standardised.

## Related Project Documents

The following internal project documents should be read alongside this contract when assembling the generic constitutional/legal repository.

| Document | Relevance |
|---|---|
| `clean_language_dependency_decision_record_for_constitutional_repository.md` | Records the cross-workstream decision that the Clean Language repository is canonical and the constitutional/legal repository is an adapter. |
| `clean_language_base_adapter_and_skill_source_of_truth_protocol_note.md` | Provides the earlier protocol note on base/adaptor separation and Manus skill source of truth. |
| `native_repository_structure_for_constitutional_drafting_process.md` | Locates this adapter contract within the proposed repository architecture. |
| `handoff_readiness_criteria_and_handoff_pack_specification.md` | Defines downstream readiness and handoff expectations. |
| `twigs_trunk_roots_constitutional_process_framing.md` | Provides the domain-specific pattern language that the adapter uses, without relocating it into the Clean Language base. |
| `ReviewofConstitutional_LegalAdapterInterfaceDocuments` | Provides the Clean Language task’s commentary that prompted this alignment pass. |

## References

No external references are used in this draft. It is a project-internal protocol document revised in response to Clean Language workstream commentary and the declared `clean-language-base` package versions.
