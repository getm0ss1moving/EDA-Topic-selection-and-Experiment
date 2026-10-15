# Independent protocol audit — D04 cycle 4

Exact inputs: challenger `SUB-9354b850df73175a5f4764f21dc5b5e8d9204f7741e9c50dce06953c34e9f984`, proposer `SUB-aeaba01af9a5b6128eec0673cea74b71dc559d2ba9bf7da096ebfaff8bdce21a`, verifier `SUB-2ff252d0046e7fc9825c2748ba4109878fee23295c7c2855ffd64435aa2a8f06`.

Disposition: **nonblocking_findings**. No supported conduct violation found within observable scope; no scientific vote.

N = no_violation_found_within_scope. All 27 entries below exactly match verification.json.

| Role | Inputs | Isolation | Writes | Evidence | Claims | Consent | Resources | Direction | Publication |
|---|---|---|---|---|---|---|---|---|---|
| challenger | N | N | N | N | N | N | N | N | N |
| proposer | N | N | N | N | N | N | N | N | N |
| verifier | N | N | N | N | N | N | N | N | N |

| Rule | Evidence and reason (release-relative locators apply to each exact role release above) |
|---|---|
| inputs | `compliance.json#/read_releases`; public `shared/job-descriptors/ROLE/JOB.json`; Declared actual inputs are within the public JOB allowlist; identity, job, commit and packet agree with descriptor/manifest. Predecessor originals are not supplied for re-audit. |
| isolation | `compliance.json#/activity`; public `shared/job-descriptors/ROLE/JOB.json`; All disclose checkout_access=none, no foreign private reads/messages/subagents. Unblinded exposure and backend/OS limits remain explicit. No contradictory released evidence; self-report is not complete trace. |
| writes | `compliance.json#/operations`; public `shared/job-descriptors/ROLE/JOB.json`; Own role release and job-local scratch writes disclosed. Hashes of every manifest-listed released file independently recomputed; no cross-role edit observed. |
| evidence | `compliance.json#/rules/evidence`; public `shared/job-descriptors/ROLE/JOB.json`; Sources/access limits and locators are explicit. Selected-full means selected passages rather than implementation audit. Failed patent/Magic/winner access remains limited, not represented as verified novelty evidence. |
| claims | `compliance.json#/rules/claims`; public `shared/job-descriptors/ROLE/JOB.json`; Synthetic set/geometry checks and conditional algebra remain separate from physical EDA measurements; forecasts are null, no demonstrated speedup or universal novelty asserted. |
| consent | `compliance.json#/rules/consent`; public `shared/job-descriptors/ROLE/JOB.json`; P pending with null target/hash; C revision_requested binds exact current P and recomputed task hash. These are not matching agreement. V explicitly keeps consensus false; challenger addenda are proposed changes, not current agreed tasks. |
| resources | `compliance.json#/activity`; public `shared/job-descriptors/ROLE/JOB.json`; Zero new EDA/training/paid runs disclosed; own tiny stdlib analytical work is allowed by batch policy. No new allocation or downloaded-code execution asserted. |
| direction | `workflow.json`; public `shared/job-descriptors/ROLE/JOB.json`; Fresh EDA-0009 preserves predecessor parking/negative evidence without inherited signatures. 0+0 drift is provenance, not merit. Unresolved mechanism/demand remains a scientific matter. |
| publication | `SUBMISSION.json`; public `shared/job-descriptors/ROLE/JOB.json`; Role self-freeze only, English released research prose, no private/copyrighted payload or claimed PR approval. Scientific V parks at fourth-cycle close; no fifth cycle/pilot/abandonment created. |

INC-001 (noncritical limitation; verifier evidence): incomplete source/adapter/physical-utility evidence remains candidly unresolved. Preserve disclosures; no misconduct or source-error allegation and no new scientific adjudication by this audit.

Manifest file hashes and descriptor bindings match. P task hash `3bebf6e0df640b3755ede2c770a9c8d8e782b7d989a311e5e73ef984e96a6744` matches C reviewed target and V. C addendum is separately hashed; P pending/C revision_requested are not consent. Toy results are synthetic; no physical experiment claim. Public ISPD2019, OpenDRC IV-C and Siemens region/HDB passages independently reopened; checks/URLs and access scope are in JSON.

Released bytes, public descriptors and self-authored ledgers only; no OS/network/tool-trace or backend-model attestation. No proof of absent undisclosed actions.

Historical predecessor disclosures retained as reported in current outputs; their original releases are outside this audit packet, and are not independently reverified.

Scientific weakness, unresolved novelty, unavailable primary text and honestly missing physical measurements are not conduct violations. This audit creates no scientific acceptance, rejection, abandonment, resource allocation or pilot authorization.

Three primary-source spot checks do not establish exhaustive source entailment or search coverage. No experiments, downloaded-code execution, private notes/transcripts/memory, checkout or role messaging used.
