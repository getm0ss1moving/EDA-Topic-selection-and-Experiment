# Verification — EDA-0002, batch cycle 2

| Input / identity | Value |
|---|---|
| Exact proposal | SUB-a806c4dc87a5851aa442cab252006b29abb325ead730688f609e5187446cf7da |
| Exact adjudicated challenge | SUB-74e2057df298eb5622da2f9b9ac90aab34b6bc351ab27f9e0c717e80ef60d6c6 |
| Commit; packet; verifier | a48f03d4bc254c0b0957d0fe0f265e072d6cf49a; c185aa8014f1936a775c86d3e418766e774100191d7c3658608e9790e9f5d7d2; ChatGPT-V05-TIMING / c411c94b-521d-48a9-b109-4489482b9cc6 |
| Dossier digest; task SHA-256 | c2ee50b06224fe87b3db7f43b387bf2e9a3e43cf57a5ee9080bd4d3a1a628b3a; b166cb871081bc3241c6885036263eae45858d3f453d85f73e44279c2cb6e572 |
| Scope / independence | Unblinded, distinct logical seats per verified manifests. Own released predecessor/handover only; R0 findings are not current verification. No foreign private material, checkout, messaging or subagents. Physical backend/registry not independently attested. |
| Decision | **revise**. No experiment selection, allocation, consent or abandonment. Cycle 2 is not the three-round parking boundary. |

| Claim / objection | Source and locator | Verdict | Blocking | Reason / action |
|---|---|---|---|---|
| CLM-044 / PS-02 | proposal PS-02 items 1-10 and sole delta | valid | no | Paired operational specification is materially repaired; requirements are not an implemented soundness proof. |
| CLM-045 / TR-02 | V2-S01/02; proposal TR-02 | valid | no | Independent real algebra yields f(u)=3+u, range [3,4], natural enclosure [0,7]; stated lower bounds follow under stipulated eta/setup assumptions. Not engine or runtime measurement. |
| CLM-043 / H2 | PS-02 B1+ and conditional induction | unsupported | yes | No nontrivial algorithmic advantage remains for submitted P-RANGE versus B1+; do not weaken strengthened baseline. |
| CLM-042 / H1 and exact reports | V2-S01/02; PS-02 UNKNOWN/fallback/WNS rules | unresolved | yes | 20% is a conditional screening target; full numeric/clock/tag/report/closure proof and measurements absent. |
| CLM-030 / closest prior art | V2-S03/04/05/09/10 | partially_valid | yes | Broad absence-of-safe-pruning premise correctly withdrawn. Full report-semantic equivalence and recent closest-method search remain unresolved. |
| CLM-035 / contest readiness | V2-S06/07/08/11 | partially_valid | yes | ISPD repair verified; exhaustive winner overlap and linked asset licenses remain unverified. |
| Utility / industry gap | industry-gap.md; V2-S09 | unresolved | yes | Turnaround objective plausible; restricted CPC demand, threshold calibration and comparable commercial gap not established. |
| Headroom / cost / forecasts | forecast.json; tasklist; independent-estimate.md | unresolved | yes | Unique union and overhead determine savings; eight hours sum correctly but are neither allocation nor feasible measured estimate. No saturation theorem. |
| Readiness / consent / abandonment | tasklist TASK-00; direction-control abandonment | unresolved | yes | Three-family/three-corner inputs, proof, DAG and allocation absent. No dual experiment or abandonment consents; local null is insufficient for universal abandonment. |
| OBJ-001 | V2-S01, V2-S02 | valid | no; resolved | Original missing paired specification is repaired by PS-02 common operations 1-10 and TR-02. This closes the documentation concern, not engine proof or contribution gates. Retain paired specification and conditional negative result. |
| OBJ-002 | V2-S06, V2-S07, V2-S08 | valid | no; resolved | Original ISPD audit omission is repaired; current scope is correctly excluded. Winner method coverage and per-asset rights remain separate unresolved gates. Retain scoped contest exclusion; finish wider winner/rights audit before readiness. |
| OBJ-003 | V2-S02, V2-S03, V2-S04, V2-S05 | valid | yes | P-RANGE sole changed primitive relative to B1-NAT is shared with B1+ by definition. Equal initial states, transfer functions and deterministic refinement imply identical eligibility and exact-work union. H2 attribution fails locally; no universal historical duplication/dead-end is established. Before coding, supply a genuinely additional anchor-preserving delta and equal-information witness, or retain null and park at the prescribed boundary. |
| OBJ-004 | tasklist TASK-02P/02E/04/06 | valid | yes: readiness only | TASK-02E consumes a pinned executable operation adapter after TASK-00, while TASK-02P only authors proof/fixtures; reference build appears later in TASK-04 and implementation later in TASK-06. No earlier executable provenance/producer is supplied. This blocks executable readiness only. Add explicit allocated bounded reference/primitive-adapter producers before TASK-02E, or pin a verified existing executable; rehash task list and recollect consent. No build now.  |

| Gate | Result | Evidence / missing prerequisite |
|---|---|---|
| Novelty | open | Closest full methods and winner overlap unresolved; submitted local distinction null. |
| Mechanism | open | Shared real-range operator is coherent; sound numerical/report adapters unproved. |
| Engineering utility | open | CPC-only need and meaningful threshold uncalibrated. |
| Contest originality | open | ISPD scope repair verified; winner methods and newer coverage unfinished. |
| Headroom | open | No useful unique-work/overhead measurements or applicable saturation proof. |
| Feasibility | open | Inputs, rights, DAG, proof and allocation absent. |
| Direction integrity | not accepted | Combination=1, demand=0, total=1. Preserves anchor diagnostically; no automatic clearing; acceptance requires zero. |
| Experiment consensus | absent | Distinct P/C seats, but neither signs current revision/task hash; no abandonment votes either. |

| Reopened source | Exact locator / access | Checked entailment / limit |
|---|---|---|
| V2-S01 [Pinned OpenSTA DmpCeff](https://raw.githubusercontent.com/The-OpenROAD-Project/OpenSTA/e01d3f163f483f233db00410b6515a767a6ca03b/dcalc/DmpCeff.cc) | DmpCap::init/gateDelaySlew/loadDelaySlew; setCeffAlgorithm; full | CAP total load and local delay/slew behavior match schematic trace; zero rpi selects CAP. Whole-engine enclosure remains unproved. |
| V2-S02 [Pinned OpenSTA TableModel](https://raw.githubusercontent.com/The-OpenROAD-Project/OpenSTA/e01d3f163f483f233db00410b6515a767a6ca03b/liberty/TableModel.cc) | Table2::findValue, two-axis branch and return; full | Four-term bilinear expression uses double intermediates with float inputs and return. Real range algebra alone does not prove numerical enclosure. |
| V2-S03 [Unified MCMM STA engine](https://www.aspdac.com/aspdac2010/Archive_Folder/pdf/8B-2.pdf) | slides 18-23; slide 21 Dcurrent; full | Incumbent bound pruning predates proposal; different parameterized objective prevents full equivalence inference. |
| V2-S04 [Efficient Block-based Parameterized Timing Analysis](https://www.eecg.utoronto.ca/~najm/papers/iccad08-khaled.pdf) | sections 4.1-4.2, PDF page 5; full | Affine exact/sufficient pruning supplies close context; not the full submitted report semantics. |
| V2-S05 [Parameterized Timing Analysis with General Delay Models](https://www.eecg.utoronto.ca/~najm/papers/dac08-khaled.pdf) | section 3, properties 1-3, PDF page 2; full | General function-class bounds have assumptions; nonlinear language alone is not novelty. |
| V2-S06 [ISPD26 rules v2.2](https://www.ispd.cc/contests/26/ISPD26_contest_description.pdf) | section 2, PDF page 3; full | Setup, single mode and ideal clock; unsuitable unchanged for declared representative target. |
| V2-S07 [Post-Placement Buffering and Sizing Contest](https://vlsicad.ucsd.edu/Publications/Conferences/421/c421.pdf) | sections 2.3 and 5.3, PDF pages 2 and 7; full | Single PVT current scope and prospective MCMM/hold/post-CTS distinction corroborated. |
| V2-S08 [Official ISPD26 results](https://www.ispd.cc/contests/26/index.html) | Contest Winners and Resources; full | Direct rankings are present; algorithms and all linked asset rights remain unverified. |
| V2-S09 [Multi-mode multi-corner physical optimization patent](https://patents.google.com/patent/US10133842B1/en) | claims 1,4,6-9; full | Timing characterization followed by local violating/worst/propagated view selection is described. This is neither proof of deployed capability nor own-table pre-analysis certificate equivalence. |
| V2-S10 [Effective Corner-Based Techniques for Variation-Aware IC Timing Verification](https://algos.inesc-id.pt/projects/rav/Silva10.pdf) | original PDF; DOI 10.1109/TCAD.2009.2034343; metadata | Direct reopen returned internal error; indexed author-PDF and bibliographic metadata only. Full-method novelty comparison unresolved. |
| V2-S11 [MLCAD26 contest](https://asu-vda-lab.github.io/MLCAD26-Contest/) | Overview and Final Results; full | Timing optimization contest and rankings are accessible; no winner algorithm or exact certificate equivalence established. |

| Run / next step | Record |
|---|---|
| Validation | Both trusted input manifests verified; digest and task hash recomputed; JSON parsed; trusted freeze validates output. Full repository validation is coordinator publication duty under standalone prompt exception. |
| Sources and limits | Sources reopened on 2026-10-15; URLs/access/locators in JSON. Bounded searches for exact multicorner timing pruning certificates and DOI 10.1109/TCAD.2009.2034343 did not close novelty. Unreviewed decision-critical claims stay unresolved. No paper copies redistributed. |
| Experiments | No build, STA, property test, data generation or benchmark; algebra is analytical, not measured. Eight CPU-hours are proposed caps only. |
| Reversal / parking | First resolve named nontrivial delta, proof, demand, input rights, DAG and allocation; then matching same-revision consent. If still nonconvergent after three substantive rounds, park with these questions. A local composition null cannot supply missing joint-abandonment signatures. |
