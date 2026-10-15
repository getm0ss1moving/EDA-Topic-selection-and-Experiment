# EDA-0002 — Engine-relative certificates for exact multi-scenario timing decisions

Proposer: ChatGPT-P05-TIMING. Logical session: 6a1a1207-fcda-4f17-ab1e-c5d41539718b. Assigned model: gpt-6.1-sol, high; no provider fallback used. Input commit: a48f03d4bc254c0b0957d0fe0f265e072d6cf49a. Packet: bd4911a04b3d7666d4304e869c785e479bbb5b5d9434f6fc18e777a6d9fe0fcb. Batch cycle 1 of 4; research phase, not consent.

**Position:** revise the anchored mechanism. Novelty, certificate soundness, useful headroom and representative-data feasibility remain unresolved. This is a complete research dossier, not an experiment-ready recommendation. Total direction penalty remains 1. No acceptance, independent historical verification, consent or new experimental result is inherited.

## Provenance and coverage

The released seed and predecessor shared handover were read. Their R1b content contains earlier unadjudicated first-pass exposure; that exposure remains disclosed. No foreign role transcript, scratch, unreleased output, project checkout or session memory was inspected. There is no newly adjudicated challenge in this job. Changes are self-initiated source corrections and analysis, not answers to historical allegations. Primary-source reading cutoff is 2026-10-15 UTC. Source IDs below belong to this successor's ledger; SRC-H01/H02 explicitly identify historical proposer evidence.

Scope: single-mode, multi-corner NLDM STA with propagated clocks, one pinned reference calculator, exact setup/hold outcomes. Broader MCMM, variation models, SI, arbitrary calculators and manufacturing signoff are outside the first evaluated implementation. This is a restriction of the inherited v1, not a claim of broad signoff validity. Classical certified pruning, nonlinear bounds, corner estimation, learned prediction, incremental timers, patents, contests and vendor pages were searched. Two expansions produced closer classical and contest mechanisms, so the search is not declared exhausted. TCAD 2010 and recent predictor full methods remain material open leads.

## Problem, demand and preserved decision

The user is a timing-closure engineer who needs the reference result over every declared scenario S with less elapsed time. Define a triple as (endpoint, scenario, check); for multiple clock/path groups retain the reference engine's endpoint-check identity and minimize over legal paths exactly as it does. D_M(S) contains every triple with reference slack below M, with its exact reference slack, all violation identities, and reference WNS/TNS per scenario/check. M=0 is primary; equality at zero is nonviolating but still subject to WNS reporting. A positive-M sensitivity changes the reporting set, never the violation definition.

No skipped triple's slack is reported as exact. Negative WNS/TNS follow from exact negative slacks, but **positive WNS does not follow from knowing all skipped slacks are nonnegative**. Preserve the full WNS obligation: obtain an exact incumbent and refine any candidate whose lower bound is below it, iterating until no skipped endpoint can improve the minimum. If this cannot be implemented with engine-equivalent path semantics, refine the full scenario. Count this cost. If the reference instead defines a clipped WNS statistic, record that API convention explicitly; never silently use it to relax the contract. This is CLM-034, a logical output-completeness repair.

Published prior work and current vendor pages motivate timing turnaround, but the 20% threshold is a provisional project screening target (SRC-P01), not practitioner validation. There is no primary user-study evidence that this restricted CPC-only implementation saves engineering effort. Resolve that through TASK-03 and measured end-to-end outputs before promotion.

## Gap and closest mechanisms

CLM-030 [OBS/INF]: the historical assertion that existing reduction methods universally lack safe elimination is withdrawn. Certified pruning and exact search are established structures. The comparison is scoped as follows:

| Source | Checked overlap | Candidate distinction and remaining uncertainty |
|---|---|---|
| SRC-R02, DAC 2011, section 6.1 equations 9-11 | Anchor slack plus exact clock-only runs estimates other corners; conservatism depends on datapath differences. | Per-scenario engine-relative lower bounds could remove that approximation. The clock-only ingredient is prior art. |
| SRC-R03, ICCAD 2008, sections 2 and 4 | Affine parameterized timing has exact and sufficient pruning rules. | Discrete characterized-engine semantics and all-scenario decisions require separate demonstration. |
| SRC-R04, DAC 2008, section 3 | Nonlinear function classes admit guaranteed max bounds, distinct from least-squares approximation. | “Not linear” is insufficient novelty; show a changed capability and comparable cost. |
| SRC-R05, DATE 2007, sections 4-5 | Bound-based dynamic pruning plus exact search under supplied timing-graph models. | Generic bound/certify/refine is not new. |
| SRC-R09, claims 1-2, 16-17 and Figures 16A-B | Parameter-function bounds and setup/hold search were publicly described. | No inference about a shipped product or arbitrary Liberty-engine semantics. |
| SRC-R01, TCAD 2010 abstract | Exact worst-delay and worst-slack methods are claimed for sequential circuits. | Strongest unresolved overlap; full methods were not obtained. |
| SRC-R10/R11, 2026 publisher-deposited abstract/metadata | Cross-corner prediction and active neural-process leads. | Full methods unavailable; no claim that their guarantees are absent. |

These summaries do not establish novelty by differing implementation vocabulary. A certificate for a characterized engine is a candidate contribution only if its semantics, useful coverage and cheaper cost exceed a straightforward instantiation of known interval/pruning methods. Equal-budget naive composition and component ablations are mandatory. The ordinary exact fallback and the WNS repair are correctness obligations, not separate novelty claims.

## Mechanism and present soundness status

Keep the original sequence: exact clock pass per scenario, cheap data bounds using only that scenario's Liberty/SPEF, certify triples whose slack lower bound clears M, and exact refinement of the uncertified dependency cones. The oracle is OpenSTA e01d3f163f483f233db00410b6515a767a6ca03b with dmp_ceff_elmore, same binary/configuration/rounding environment for all methods. No cross-PVT monotonicity, training, fitted safety margin or changed delay calculator is allowed.

CLM-031 [historical OBS]: the released finite-test record reports P3 failures 3553/19600, P4 failures 100/52088 and P5 failures 3025/52088 (SRC-H01). These are inherited synthetic observations; no independent rerun occurred. Retain K2: the general waveform bounds are withdrawn. SRC-R06 freshly confirms DmpCap table calculation and Elmore load-delay branch structure. This motivates retaining the restricted R1/CPC candidate; it does not prove all-cone certificates sound.

CLM-032 [OBS/INF]: calculator selection depends on input slew through Rd (SRC-R06, setCeffAlgorithm). CPC classification must hold over the complete propagated interval, not a sampled slew. SRC-R08 uses double intermediates and float results; a generic float32 allowance does not itself enclose the actual operation graph. The inherited P9 allowance is **unresolved**, not an implemented proof. A validated outward enclosure must cover interpolation, extrapolation, scaling, cast, clipping and subsequent arithmetic; otherwise the triple falls back exactly. NaNs, infinities, malformed tables, unsupported axis forms and non-enclosed operations cannot certify.

Conservatively require whole-net/load and all-driver closure. Unknown exception matches, cross-library threshold adjustments, reconvergent clock tags, generated clocks, CRPR, unbounded startpoint slews, recovery/removal or unsupported graph features force exact evaluation of the affected report domain. Merely omitting these paths is forbidden. Explicit exception handling may later replace fallback only after an engine-relative audit. A clock-only pass must itself preserve every relevant tag and context; this remains a TASK-02 obligation.

CLM-033 [conditional logical proposition]: if each L(t) is a sound lower bound on the same reference slack sigma(t), all t with L(t)<M or no certificate are refined with reference-equivalent dependencies, and every report/WNS obligation is handled, then D_M(P)=D_M(B0). Proof: sigma(t)<M implies L(t)<=sigma(t)<M, so such t cannot be discarded; exact refinement supplies its slack. Exact negatives determine TNS with identical ordering. WNS additionally requires the incumbent refinement above. This proves only the reduction step under assumptions. It does not establish that the current calculator/search implementation supplies those assumptions.

## Headroom and causal test

CLM-041 [INF]: endpoint certification fraction is not an avoided-work fraction. Let U be the union of dependency-closed cones needed by uncertified triples and exact-WNS contenders, with full-net and context closure. A shared arc in U must still be evaluated even if many of its endpoints are certified. A design can certify most endpoints and still have U equal the full data graph. Count unique work by scenario and phase; never multiply an endpoint fraction by baseline time.

Use the accounting identity T_P = T_fixed + T_clock + T_bound + T_refine(U) + T_WNS + T_logging. Shared work must be charged once; keep WNS-only additions separate from U's initial closure to avoid double counting. T_B0 is the measured strongest full-analysis elapsed time including the same input and reporting boundary. The target requires avoided exact work to exceed 0.20*T_B0 plus new overhead. This is a measured cost model to test, not an architecture-independent lower bound. No saturation, Amdahl fraction, CPC prevalence or numerical forecast is known.

H1 [HYP, CLM-042]: after all proof/data/readiness gates, on three independently selected designs and at least three genuinely characterized scenarios, P preserves D_M exactly and reduces paired median end-to-end wall time by at least 20% under equal resources. Exactness is the scientific contract; <=5 ps diagnostic error in the brief cannot excuse missed violations or relax it.

H2 [HYP, CLM-043]: any benefit comes from the unique exact work removed by per-triple certification. At equal budgets P must outperform a generic known bound-plus-fallback composition, endpoint-to-scenario aggregation, and a no-clock-information variant; report all failures and total implementation/report overhead. Merely beating a naive cold serial launcher is insufficient.

Counter-hypotheses: CPC eligibility vanishes through deep cones; interval widths remove useful certificates; shared cones erase work savings; bound and WNS passes cost more than avoided work; incremental exact B6 wins the actual edit loop; known methods provide the same semantic guarantee. None is a measured finding. An oracle screen that uses B0 slacks is diagnostic only and its B0 cost can never be excluded from a deployable speedup.

## Contests, industry and delivery position

CLM-035/036/037 are bounded source observations detailed in contest-audit.md and industry-gap.md. TAU 2019 already supplied a multicorner optimization setting and teams used worst-corner or incremental approaches. Reimplementing them is not a contribution. Current product documentation does not establish proprietary algorithmic absence. The pinned engine supports incremental timing, making B6 mandatory for edit-loop comparisons.

CLM-038/039 [packet OBS]: only GCD/Nangate45-typical is established by the assigned brief; it cannot substantiate H1. The batch grants no experiment compute. Sources, methodology and feasible dependency ordering were advanced; no build, STA execution, data generation, property experiment or benchmark run occurred. Exact task-list agreement, representative licensed scenarios, demand calibration and current-role verification remain prerequisites. No scientific sign-off is requested this cycle.

Kill criteria: K1 duplicate/equivalent useful mechanism established from checked prior art; K2 inherited broad-waveform falsification retained; K3 uniquely avoidable work cannot meet the provisional threshold after overhead; K4 no representative licensed scenario/design bundle within an actually allocated budget; K5 naive composition gives the same guarantee/tradeoff; K6 no justified user benefit; K7 any unsound certificate, missed violation or report mismatch. K2 already activated the R1 restriction. Other criteria remain unresolved. A supported dead end may justify proposer abandonment consideration, but there is no joint consent or unilateral archive here.

## Historical claim disposition

The original ledger remains at SRC-H02; none is erased or treated as adjudicated.

| Legacy ID | Successor disposition |
|---|---|
| CLM-001 | Scenario-growth examples retained only as historical citations; numerical examples not reasserted. |
| CLM-002 | Universal no-guarantee formulation withdrawn; CLM-030 supersedes it. |
| CLM-003 | Scenario-dependence remains a hypothesis-relevant observation, not a new measured frequency. |
| CLM-004 | Historical practice claims not generalized to all practitioners. |
| CLM-005 | Linear-only family characterization corrected by SRC-R04. |
| CLM-006 | Pinned configuration must be reproduced; no all-corner benchmark inferred from README. |
| CLM-007 | Restricted DmpCap branch freshly inspected; full numerical behavior not independently rerun. |
| CLM-008 | Retain falsified status. |
| CLM-009 | Replace unconditional reading by conditional CLM-033 plus WNS obligation. |
| CLM-010 | H1 remains unmeasured as CLM-042. |
| CLM-011 | H2 strengthened with graph-union accounting, CLM-041/043. |
| CLM-012 | Heuristic failure is not a prerequisite for contribution; no failure-rate forecast. |
| CLM-013 | Resource deficit remains, CLM-038/039. |
| CLM-014 | Update bounded contest review, CLM-035; no exhaustive originality assertion. |
| CLM-015 | Novelty unresolved; refreshed closest work replaces stale access restrictions. |
| CLM-016 | Preserve incremental-loop exclusion from main novelty; B6 retained as comparator. |
| CLM-017 | Historical hypothetical example only; not experimental evidence of frequency. |
| CLM-018 | Inherited finite-test negative retained, SRC-H01. |
| CLM-019 | Inherited finite-test negative retained, SRC-H01. |
| CLM-020 | Inherited finite-test negative retained, SRC-H01. |
| CLM-021 | Code-level restriction supported; no general proof inherited. |
| CLM-022 | ADT/bracket extension excluded from certificate; unresolved. |
| CLM-023 | R1 candidate conditional pending classification/arithmetic/search audit. |
| CLM-024 | Full-net/all-driver dependencies retained as required controls. |
| CLM-025 | Inherited DmpZeroC2 mismatch retained; no table-only certificate there. |
| CLM-026 | Generic certified elimination/refinement explicitly prior art, CLM-030. |
| CLM-027 | Exception-matched or unknown contexts fall back exactly; full audit pending. |
| CLM-028 | Float32-only reasoning insufficient; CLM-032 and TASK-02 supersede it. |
| CLM-029 | Incremental exact competition retained; no outcome predicted. |
