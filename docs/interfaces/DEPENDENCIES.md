# Dependency Declaration for the Constitutional/Legal Domain Adapter

**Status:** Commit-candidate draft; provisional pending controlled thin-slice handoff test  
**Author:** Manus AI  
**Intended repository location:** `docs/interfaces/DEPENDENCIES.md`  
**Adapter interface status:** revised draft candidate  
**Document revision:** v0.3 housekeeping commit candidate  
**Revision file:** `DEPENDENCIES_v0_3_commit_candidate.md`  
**Related artefacts:** `docs/interfaces/ADAPTER_CONTRACT.md`; `docs/interfaces/TRANSFORMATION_LOG_TEMPLATE.md`  
**Current dependency state:** Concrete base dependency declared; adapter compatibility provisional pending thin-slice handoff test

## 1. Purpose

This document declares the dependency relationship between the **constitutional/legal domain adapter repository** and the **Clean Language base repository**. It exists to prevent accidental forking of the base elicitation method, unmanaged copying of skill materials, or silent incompatibility between project records and the method release that produced them.

The constitutional/legal repository is not the canonical source for Clean Language elicitation. It is a domain adapter that consumes Clean Language outputs and transforms them into constitutional, legal, organisational, governance, software, or project-delivery design material only where those transformations are visible and reviewable.

> **Dependency principle:** The constitutional/legal repository should declare, not absorb, the Clean Language base. It should interpret base outputs through a versioned adapter rather than treating Clean Language materials as editable local content.

## 2. Current Dependency Ledger

The Clean Language task review confirms that the base package now exists as `clean-language-base`. This declaration therefore moves from a pre-release placeholder position to a concrete dependency declaration. The housekeeping check found no GitHub release tag for the base repository, so the declared release pin is the current default-branch commit `4dcf081035de23de10718d050afb8cbc892ae28a`, with the commit message “Initial Clean Language base package release”. Compatibility remains provisional because the constitutional/legal adapter has not yet completed a controlled thin-slice handoff test.

| Dependency | Current declaration | Status | Notes |
|---|---|---|---|
| Clean Language base repository | `https://github.com/dilgreen/clean-language-base` | Declared | Canonical source of the base elicitation method and release package. |
| Clean Language base method version | `0.3` | Declared | Base method version assumed by this adapter interface draft. |
| Clean Language manifest schema version | `0.1.0` | Declared | Schema version expected for incoming base output packages. |
| Clean Language skill release version | `0.1.0` | Declared | Operational skill release version identified by the Clean Language task review. |
| Clean Language release checklist treatment | Included in base package release `0.1.0` | Declared | No unsupported standalone release-checklist version is claimed. |
| Base release pin | `4dcf081035de23de10718d050afb8cbc892ae28a` | Declared | No GitHub release tag was found during the housekeeping check; this is the current default-branch release commit. |
| Manus Clean Language skill package | `clean-language-base`, `skill_release_version: 0.1.0` | Declared | Manus skill packages remain deployable releases derived from the canonical repository, not independent sources of truth. |
| Constitutional/legal adapter contract | `docs/interfaces/ADAPTER_CONTRACT.md`, revised draft candidate | Draft | Defines the adapter boundary, permitted moves, prohibited moves, base fields, and transformation record requirement. |
| Transformation log template | `docs/interfaces/TRANSFORMATION_LOG_TEMPLATE.md`, revised draft candidate | Draft | Provides a reusable project-level record for each interpretive move, aligned with base manifest fields. |
| Native repository structure | `native_repository_structure_for_constitutional_drafting_process.md` | Draft | Should later be updated to locate these adapter artefacts in the folder hierarchy. |
| Handoff readiness specification | `handoff_readiness_criteria_and_handoff_pack_specification.md` | Draft | Governs when material can move from constitutional coaching to legal/build coaching. |

## 3. Normative Hierarchy

If there is an inconsistency between artefacts, the following hierarchy should be applied. Each layer governs its own domain and should not silently override a higher layer.

| Priority | Artefact or layer | Governs | Consequence of conflict |
|---|---|---|---|
| 1 | Clean Language base method | Elicitation discipline, participant-meaning preservation, base validation, and base output categories. | The constitutional/legal adapter must not redefine the base method locally. |
| 2 | Clean Language release package | Deployable skill, templates, manifest schema, release checklist, and base-side handoff contract. | The adapter must update declared compatibility before relying on changed release behaviour. |
| 3 | Constitutional/legal adapter contract | Domain interpretation, Twigs–Trunk–Roots mapping, legalisation guardrails, and handoff obligations. | Project-level work must label deviations from the adapter contract. |
| 4 | Project repository overlay | Project-specific participant records, validation evidence, decisions, transformation history, and authority. | Project records may specialise the process but must not erase source meaning. |
| 5 | Draft legal or constitutional instruments | Operative clauses, governance commitments, rights, duties, procedures, and institutional form. | Drafts must be traceable to validated project decisions and reviewed under the relevant legal/professional standard. |

This hierarchy is intended to keep the base elicitation method clean, the adapter accountable, and the project record intelligible to participants and downstream professionals.

## 4. Compatibility Statement

The constitutional/legal adapter now declares a concrete dependency on the Clean Language base package identified above. That does not mean full operational compatibility has already been proven. The correct current status is **provisional pending thin-slice handoff test**.

| Compatibility question | Current answer | Required before stable use |
|---|---|---|
| Has the canonical Clean Language repository been identified? | Yes: `https://github.com/dilgreen/clean-language-base`. | Confirm repository URL at commit time. |
| Has the base method release been named? | Yes: `base_method_version: 0.3`. | Base release tag pending; current default-branch commit pin is `4dcf081035de23de10718d050afb8cbc892ae28a`. |
| Has the manifest schema been named? | Yes: `manifest_schema_version: 0.1.0`. | Check adapter intake fields against the actual schema. |
| Has the Manus skill package been linked to the base release? | Yes: `skill_release_version: 0.1.0`. | Confirm skill package provenance at commit or package-install time. |
| Has the adapter been tested against a base output? | Not yet. | Complete the planned controlled thin-slice handoff test. |
| Has the transformation log template been validated in use? | Not yet. | Use it in the thin-slice test and review for gaps. |

The adapter may therefore be used for repository structuring, review, and thin-slice preparation. It should not yet be marked `compatible`, `operationally_stable`, or `release_proven`.

## 5. Expected Base Package Inputs

The constitutional/legal adapter should expect the following Clean Language base package artefacts and fields. These are the concrete terms that should be used when checking source traceability and transformation records.

| Base package component | Expected name or field | Adapter relevance |
|---|---|---|
| Manifest | `manifest.yaml` | Primary package metadata and source-of-truth for version and status fields. |
| Base method version | `base_method_version: 0.3` | Declares which base method version produced or governs the output package. |
| Skill release version | `skill_release_version: 0.1.0` | Declares the deployable Clean Language skill release, if used operationally. |
| Manifest schema version | `manifest_schema_version: 0.1.0` | Declares the structure the adapter should expect when reading package metadata. |
| Session identifier | `session_id` or base-defined session locator | Allows source traceability from adapter interpretation back to elicitation material. |
| Validation status | `validation_status` | Indicates whether source material is `unreviewed`, `partially_validated`, `validated`, `needs_revision`, or `rejected`. |
| Adapter readiness | `adapter_readiness.status` | Indicates whether the package is `not_ready`, `base_validated`, or `adapter_handoff_prepared`. |
| Validation review | `validation-review.md` | Provides human-readable review and validation context. |
| Tree summary | `tree-summary.md` | Provides neutral tree-level summary before domain interpretation. |
| Node records | Optional `nodes/` files | Provide granular source records for particular participant expressions or patterns. |
| Known limitations | `known-limitations.md` | Warns the adapter against premature or overconfident interpretation. |

## 6. Dependency Update Procedure

The dependency declaration should be updated whenever any upstream or adapter-facing artefact changes in a way that could affect project interpretation. In practice, that means updating this file when the Clean Language workstream publishes a new base release, modifies the manifest schema, changes the release checklist, or packages a new Manus skill version.

The constitutional/legal repository should also update this declaration when the adapter contract changes, when the transformation log template changes materially, when a new project template is introduced, or when a thin-slice test exposes incompatibility between base outputs and legal/governance interpretation.

| Trigger | Required action | Review responsibility |
|---|---|---|
| New Clean Language base release | Record new version, release date, release tag or commit hash, and compatibility status. | Constitutional/legal repository maintainer, with Clean Language workstream confirmation where possible. |
| New Clean Language manifest schema | Check whether incoming fields are still sufficient for adapter interpretation and transformation logging. | Adapter maintainer and Clean Language workstream. |
| New Manus skill package | Confirm that the package is derived from the declared base repository release. | Skill packager or repository maintainer. |
| Adapter contract revision | Update adapter version and note compatibility implications. | Constitutional/legal workstream. |
| Transformation log revision | Update template version and note whether existing logs need migration. | Project maintainer or repository maintainer. |
| Thin-slice handoff test | Record observed compatibility, gaps, and required changes. | Joint review between Clean Language and constitutional/legal workstreams. |

## 7. Release-Ready Declaration Fields

Before this repository is treated as ready for repeatable project use, the following fields should be completed and reviewed. Some are now populated from the Clean Language review; others still require confirmation at commit time or after the thin-slice test.

| Field | Current value | Release-readiness note |
|---|---|---|
| `clean_language_repository` | `https://github.com/dilgreen/clean-language-base` | Confirm URL before commit. |
| `clean_language_base_method_version` | `0.3` | Confirm against release metadata. |
| `clean_language_manifest_schema_version` | `0.1.0` | Confirm against `manifest.yaml` schema file. |
| `clean_language_release_checklist_treatment` | Included in base package release `0.1.0` | No standalone checklist version is asserted. |
| `clean_language_release_pin` | `4dcf081035de23de10718d050afb8cbc892ae28a` | Base release tag pending; use this commit pin unless a tag is created before commit. |
| `manus_clean_language_skill_package` | `clean-language-base`, `skill_release_version: 0.1.0` | Confirm package provenance. |
| `constitutional_legal_adapter_contract_version` | Revised draft candidate; proposed path `docs/interfaces/ADAPTER_CONTRACT.md` | Pending user review and commit approval. |
| `transformation_log_template_version` | Revised draft candidate; proposed path `docs/interfaces/TRANSFORMATION_LOG_TEMPLATE.md` | Pending user review and thin-slice use. |
| `compatibility_status` | `provisional` | Do not change to `compatible` until a controlled handoff test succeeds. |
| `known_limitations` | No thin-slice handoff has yet been completed. | Update after test. |

## 8. Current Known Limitations

This dependency declaration is intentionally conservative. It no longer says that the Clean Language base package is unavailable, because the review confirms that it now exists. It does say that adapter compatibility remains unproven until the adapter has consumed a base output package and produced traceable domain outputs through the transformation log.

| Limitation | Practical implication | Proposed resolution |
|---|---|---|
| Thin-slice test not yet performed | The adapter has not been tested end-to-end against a concrete Clean Language output package. | Run a controlled thin-slice handoff using the declared base versions. |
| Base release tag pending | The repository has declared package versions, but no GitHub release tag was found during the housekeeping check. | Use the commit pin `4dcf081035de23de10718d050afb8cbc892ae28a` unless a tag is created before commit. |
| Transformation log template not yet used in practice | The aligned fields may still reveal usability issues when applied to real material. | Use the commit-candidate template in the first thin-slice test. |
| Legal/professional status varies by jurisdiction and project | Adapter outputs must not be overclaimed as legal advice. | Keep legal-status warnings and human/professional review steps visible. |
| Early-stage propositional groups may lack stable trunk material | The adapter may need to produce scaffolding rather than drafting-ready conclusions. | Use provisional status labels and avoid premature constitutional closure. |

## 9. Recommended Next Review

The next review of this dependency declaration should occur immediately before any adapter-side commit and again after the first controlled thin-slice handoff test. The pre-commit review should confirm that the declared Clean Language base repository and versions are accurate. The post-test review should decide whether compatibility can move from `provisional` to `compatible`, or whether adapter contract and transformation-log changes are needed.

## References

No external references are used in this draft. It is a project-internal dependency declaration revised in response to Clean Language workstream commentary and the declared `clean-language-base` package versions.
