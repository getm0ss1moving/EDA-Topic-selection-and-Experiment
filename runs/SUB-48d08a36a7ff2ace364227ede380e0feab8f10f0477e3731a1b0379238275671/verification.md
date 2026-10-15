# Verification

| Input / identity | Value |
|---|---|
| Topic / revision | EDA-0002; SUB-798cbd734b7b9b36d5460af3487a6b0400e1c6e6b7aabb6c576d5a6ecdef0974 |
| Adjudicated challenger | SUB-d4efe5f9b29cc9ce2f4f5db2b7da7c3aa1931b9ccd604d15d77e97ef94bc18f3 |
| Verifier / input | ChatGPT-V05-TIMING; c411c94b-521d-48a9-b109-4489482b9cc6; commit a48f03d4bc254c0b0957d0fe0f265e072d6cf49a; packet c185aa8014f1936a775c86d3e418766e774100191d7c3658608e9790e9f5d7d2 |
| Dossier digest | a5a7f5f57b5a776db53d476412e8dc7e40901265182022a872edb1dd6424d563; supplied release scope including manifest, not integrated dossier |
| Independence | Distinct logical sessions and input manifest hashes checked; explicitly unblinded. Only own released handover and assigned shared files read. Historical R0 verdict is not verification of current R1b/GPT content. |
| Decision | revise; no new experiment authorized. Resolve evidence/specification/readiness gates below. |

| Claim / objection | Source ID and exact locator | Verdict | Blocks advancement? | Reason / required action |
|---|---|---|---|---|
| OBJ-001 | V-S01 section 4; V-S02 slides 18-23/28; plan B1 line 13 | valid | yes, before H2 | Freeze paired operation-level P/B1 delta; not a duplication verdict. |
| OBJ-002 | V-S04 sections 2.3/5.3 | valid | no | Add scoped ISPD2026 audit; current fixture is ideal-clock single-corner setup. |
| CLM-030 | V-S01 section 4; V-S03 section 3 | valid | no | Correction of universal safe-pruning/nonlinear absence is justified; novelty remains open. |
| CLM-032 | V-S05 setCeffAlgorithm/gateModelRd; V-S06 Table2::findValue | partially_valid | yes | Code supports implementation-sensitive obligations, not an all-cone certificate proof. Use function locators; web-extracted line numbering differs from source ledger. |
| CLM-033/034 | proposal conditional proof and WNS paragraph | valid | no, conditional only | Sound lower bounds plus equivalent refinement imply no missed below-margin slack; exact positive WNS needs incumbent refinement. Assumptions remain unproved. |
| CLM-031 | released historical record, not independently rerun | unresolved | yes for broad-waveform claims | Retain negative evidence and restriction; no current numerical verification or inherited R0 approval. |
| CLM-035/036/037 | V-S04; TAU2019 page reopened; other vendor/winner claims not rechecked | unresolved | yes for contest/industry clearance | No proprietary-absence or exhausted-contest-search inference. |
| CLM-038/039 | JOB/prompt; research-brief available_pdks/designs/compute | valid | yes | Brief establishes typical-only GCD fixture and provisional caps; no allocation or three-design/scenario bundle established. |
| CLM-041 | proposal union-of-cones argument | valid | no | High endpoint coverage need not remove shared-graph work; accounting identity is not measured speedup. |
| CLM-042/043 | tasklist TASK-02 through TASK-09; forecast labeled forecast_not_measurement | unresolved | yes | 20% and causal benefit remain hypotheses; no experiment performed. |
| Closest/new work | V-S02 slides 21/28; V-S07 DOI abstract; V-S08 DOI lead | unresolved | yes | BNB overlap checked; TCAD full PDF fetch timed out, recent primary full methods unavailable. No equivalence established. |

| Gate | Result | Evidence / missing prerequisite |
|---|---|---|
| Novelty | false | B1 delta and closest full-method overlap unresolved. |
| Mechanism | false | Conditional logic valid; arithmetic, interval classification and tag/search proof absent. |
| Engineering utility | false | Restricted-capability practitioner need and threshold calibration pending. |
| Contest originality | false | ISPD gap valid; final rules/winners and wider search not exhausted. |
| Headroom | false | Unique avoidable work and overhead unmeasured; no saturation theorem asserted. |
| Feasibility | false | Representative legal inputs, budget feasibility and allocation pending. |
| Direction integrity and penalties | false for acceptance | Combination drift 1, demand drift 0; mechanism and user preserved, but accepted topics require total zero. This is not a new pivot finding. |
| Experiment consensus | false | Task hash c082e16aa927e8fc7bb6c1ebcbb750004ed0ccbe4b71dd0f105cf58a75c789e1; no current proposer/challenger consents. |

| Reopened source | URL / access / limitation |
|---|---|
| V-S01: Efficient Block-based Parameterized Timing Analysis Covering All Potentially Critical Paths | [V-S01](https://www.eecg.utoronto.ca/~najm/papers/iccad08-khaled.pdf); full; Sections 4.1-4.2, PDF page 5; exact pruning and sufficient pruning. Affine hyperplane pruning is established. It does not by itself implement discrete-engine all-scenario reports. |
| V-S02: Unified MCMM STA engine presentation | [V-S02](https://www.aspdac.com/aspdac2010/Archive_Folder/pdf/8B-2.pdf); full; Slides 18-23 and 28, especially slide 21 incumbent Dcurrent pruning. Path/parameter branch-and-bound and an incumbent are explicit. No identity with current proposal established. |
| V-S03: Parameterized Timing Analysis with General Delay Models and Arbitrary Variation Sources | [V-S03](https://www.eecg.utoronto.ca/~najm/papers/dac08-khaled.pdf); full; Section 3 properties 1-3, PDF page 2. Nonlinear function-class bounds exist under closure, boundedness and efficient extrema assumptions; nonlinear terminology is insufficient novelty. |
| V-S04: Invited: Post-Placement Buffering and Sizing Contest | [V-S04](https://vlsicad.ucsd.edu/Publications/Conferences/421/c421.pdf); full; Section 2.3 PDF page 2; Section 5.3 PDF page 7. 2026 uses single-PVT setup and ideal clocks; MCMM, post-CTS and hold are future enhancements under consideration. Dataset lead is not ready evidence for this contract. |
| V-S05: OpenSTA pinned DmpCeff.cc | [V-S05](https://raw.githubusercontent.com/The-OpenROAD-Project/OpenSTA/e01d3f163f483f233db00410b6515a767a6ca03b/dcalc/DmpCeff.cc); full; DmpCeffDelayCalc::setCeffAlgorithm; gateModelRd; DmpCap::gateDelaySlew/loadDelaySlew. Branch selection uses gateModelRd and input slew; source corroborates need for interval-wide classification, not a completed proof. |
| V-S06: OpenSTA pinned TableModel.cc | [V-S06](https://raw.githubusercontent.com/The-OpenROAD-Project/OpenSTA/e01d3f163f483f233db00410b6515a767a6ca03b/liberty/TableModel.cc); full; Table2::findValue, bilinear expression and double intermediates. Actual arithmetic differs from an abstract float32-only allowance. Full scaling/cast/search enclosure remains unverified. |
| V-S07: Effective Corner-Based Techniques for Variation-Aware IC Timing Verification | [V-S07](https://algos.inesc-id.pt/projects/rav/Silva10.pdf); abstract; DOI 10.1109/TCAD.2009.2034343; indexed author-PDF abstract. Direct PDF reopened twice: fetch timeout. Indexed abstract claims exact worst-delay/slack; no full-method comparison or novelty clearance. |
| V-S08: Interpretable Cross-Corner Timing Prediction Based on XGBoost-SHAP Solution | [V-S08](https://api.crossref.org/works/10.1145/3816045); metadata; DOI lead; direct Crossref access failed. Search located metadata/secondary abstract only; no primary full-method entailment adopted. |

| Validation / next work | Evidence |
|---|---|
| Local validation | Both released manifests passed trusted verify; JSON and freeze checks used. Full repository validate deferred to coordinator because this standalone packet lacks checkout. No scientific build, property run or benchmark was executed. |
| Search/access record | 2026-10-15 web searches and actual access limits are in verification.json.run_record. Search budget ended with residual risk; absent results prove no novelty. |
| Next revision | Specify fair B1/P differential first; add ISPD scoped audit; close proof/data/demand prerequisites before consent. Do not interpret either objection as demonstrated duplication or joint abandonment. |
| Output record | release/verification.md, release/verification.json, release/workflow.json; frozen submission supplies immutable run identity. |
