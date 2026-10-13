# Proposal

**EDA-0002: Sound per-(endpoint, scenario) screening for multi-corner STA with exact refinement**

| Field | Value |
|---|---|
| Domain | D05 Timing, extraction and signoff (MCMM analysis, signoff fidelity, runtime) |
| Proposer | `Claude-P05-TIMING`, session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`, model `claude-opus-5-5` |
| Input | Packet `ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d`, input commit `d437c2f660906efe9351a90451905826d00b63e3` |
| Evidence window | Public sources retrieved 2026-10-12, 16:02-17:01 UTC. No local tool runs: `experiment_authorization` is false (`config/launch-release.json` line 71), and the coordinator confirmed this under DQ-07. |
| Status | Initial submission (round 0). No claim below is a measurement. Novelty is **not** established (CLM-015). |

Labels: **[OBS]** sourced observation · **[INF]** my inference · **[HYP]** hypothesis to test · **[FCST]** forecast. Source IDs refer to `sources.json`; packet files are cited by path and line.

## Problem and engineering decision

**Workflow slice.** Multi-mode/multi-corner (MCMM) static timing analysis during timing closure and pre-signoff checking. This sits inside D05's scope of multi-mode/multi-corner analysis and signoff fidelity, with corner robustness and runtime as engineering metrics (`domains/D05/brief.json` lines 5-6).

**Engineering user.** A timing-closure or signoff engineer, or the owner of a closure flow, who must time a design at every scenario in a declared scenario set S. Here a scenario is a characterized cell-library corner combined with an RC corner; v1 is single-mode.

**Decision supported.** After each closure iteration and before the signoff go/no-go, the user needs the decision set D_M(S):

- every (endpoint, scenario, check) triple that violates;
- the exact slack of every triple whose slack is below a reporting margin M ≥ 0;
- WNS and TNS per scenario.

ECO planning and the signoff decision consume exactly these values.

**Pain**:

- [OBS] Scenario counts are large and growing. 16 signoff corners at 40 nm (SRC-021). 58 PVT corners on a foundry-16nm design (10 observed plus 48 predicted, SRC-015). More than 250 views at 28 nm with eight modes, cut to about 100 "depending on your tolerance for risk" (SRC-020, vendor). 135-495 basic corners in a methodology analysis (SRC-019 pp. 7-8, vendor white paper). (CLM-001)
- [OBS] Published and patented reductions skip scenarios using estimates, empirical cutoffs, learned models or experience, and none offers a formal guarantee (CLM-002). Examples:
  - empirical slack cutoffs (SRC-016);
  - dominant-corner ratio estimation plus ML, "designed to be sign-off safe" but without a proof (SRC-017);
  - synthetic max-over-corners, described by the patent itself as approximate (SRC-018);
  - regression or Bayesian prediction (SRC-015, SRC-022 to SRC-025);
  - greedy corner selection reaching 97.3% hold-path coverage, with 10-20 ps of added hold uncertainty to cover the rest (SRC-021).
- [OBS] The worst scenario differs by path, so removing "dominated" scenarios can miss violations (CLM-003). One source finds each path is worst at only 3-4 corners, and those corners differ by path; a cell-dominated launch path paired with a metal-dominated capture path needs SS combined with fast metal (SRC-019 pp. 7-8). Hold cannot be bounded by a small corner set (SRC-012, excerpt only).
- [OBS] Vendors and practitioners require that reduction must not miss failing endpoints (SRC-020), and they pay for residual risk with extra margin (SRC-021). (CLM-004)

**Downstream need.** Lower MCMM turnaround with **zero** missed violations, measured against full analysis of the declared scenario set S.

## Scope, inputs, outputs, and correctness oracle

**In scope (v1)**:

- flip-flop-based synchronous designs;
- one SDC mode;
- scenarios formed from characterized NLDM library sets and the available SPEF RC corners;
- setup and hold checks, plus recovery/removal if present;
- propagated clocks;
- pinned OpenSTA `e01d3f163f483f233db00410b6515a767a6ca03b`, which is the `src/sta` submodule of the packet's OpenROAD `b16bda7e…` (SRC-010), using its default `dmp_ceff_elmore` calculator (SRC-003, lines 411 and 417).

**Out of scope (v1)**:

- latches and time borrowing;
- SI/crosstalk;
- POCV, LVF and AOCV tables;
- CCS delay calculation;
- mode merging;
- operating points outside the declared set S. Tetelbaum's warning about intermediate temperatures (SRC-019 p. 9) concerns how S is defined, which is a separate problem.

**Inputs**: netlist, SDC, one Liberty set per scenario, one SPEF per RC corner, and the margin M.

**Outputs**:

- the decision set D_M(S) as defined above;
- a certificate log recording the bound used for every certified triple;
- a run log covering every pass, its cost, and any fallbacks.

**Correctness oracle.** Full multi-corner analysis of S with the same pinned OpenSTA build, all scenarios in one run (`define_corners`, SRC-005; `Corners::makeAnalysisPts`, SRC-006). This is a *decision reference*, not a qualified signoff oracle: the packet makes no claim of silicon signoff or multi-corner coverage (`config/research-brief.json` line 65). Every claim here is therefore "fidelity to pinned OpenSTA".

## Claim ledger (ID, type, source, locator, uncertainty)

| ID | Type | Statement | Source and locator | Uncertainty |
|---|---|---|---|---|
| CLM-001 | OBS | Signoff scenario sets run from tens to hundreds of scenarios. | SRC-021 body; SRC-015 abstract; SRC-020 body; SRC-019 pp. 7-8 | Medium. Mostly vendor or practitioner sources; no controlled survey. |
| CLM-002 | OBS | Accessed reduction methods use estimated, empirical, learned or experience-based criteria with no formal guarantee against missed violations. | SRC-016 description; SRC-017 description; SRC-018 description; SRC-015 abstract; SRC-021 body; SRC-022 to SRC-025 (abstract-level) | Medium. Several sources were seen at abstract or metadata level only. |
| CLM-003 | OBS | The worst scenario differs by path or endpoint; dropping scenarios can miss violations; hold resists small-corner-set bounding. | SRC-019 pp. 7-9; SRC-012 (excerpt) | Medium. SRC-012 not inspected. |
| CLM-004 | OBS | Practice demands no missed failing endpoints and covers residual risk with extra hold uncertainty of 10-20 ps. | SRC-020; SRC-021 | Low for "stated practice"; unknown for prevalence. |
| CLM-005 | OBS | Parametric all-corner bounding and branch-and-bound engines model cell delays as linear functions of process or mode variables. | SRC-014 slides 14-15 (citing SRC-013) | Low for SRC-013 and SRC-014. **High for SRC-012, whose assumptions were not read.** |
| CLM-006 | OBS | Pinned OpenSTA times all corners in one run; its default calculator is `dmp_ceff_elmore`; seven calculators are registered. | SRC-005 lines 3663-3672; SRC-006 lines 88 and 174; SRC-003 lines 411 and 417; SRC-004 lines 37-43 | Low (code reading). |
| CLM-007 | OBS | In pinned `dmp_ceff_elmore`, gate delay is a table lookup at a solved Ceff constrained to [0, c1+c2], falling back to c1+c2. Wire delay is a single-pole crossing with τ = Elmore delay, with Elmore fallbacks, and load slew is at least driver slew. NLDM tables are bilinear, with linear extrapolation from the edge cell. | SRC-002 lines 555-605, 915-948, 969-974; SRC-007 lines 1012-1060, 1443-1463 | Low for the code facts; their implications are CLM-008. |
| CLM-008 | INF | A per-scenario upper bound on late arrival, and a lower bound on early arrival, can be computed without iterating on Ceff. Each arc's table is evaluated over the box (slew bounds) × [0, c1+c2] at that box's finite set of bilinear extreme points. Soundness against the pinned calculator also needs properties P3-P5, which are **not yet established**. | SRC-002; SRC-007; SRC-026 (Elmore bound, metadata) | **High.** Central technical risk (EXP-002). |
| CLM-009 | INF | If the bounds are sound, restricting exact analysis to uncertified triples reproduces D_M(S) exactly. Every violating triple is uncertified when M ≥ 0, so violation lists, sub-margin slacks and TNS are exact. | Logic from the definitions; depends on CLM-008 | Medium. Depends on correct cone extraction and global effects (CRPR, clock tags); see CH5. |
| CLM-010 | HYP (H1) | On at least 3 independent designs and a multi-scenario set S, the screened analysis reproduces D_M(S) exactly and takes at least 20% less end-to-end wall time than the strongest full-MCMM baseline (B0) under equal resources. | To be tested (EXP-006, EXP-007); threshold from `config/research-brief.json` line 77 | Unknown. No measurement. |
| CLM-011 | HYP (H2) | The speedup comes from certifying non-dominant (endpoint, scenario) triples. Predicted signatures: higher certification in non-dominant scenarios; exact clock analysis materially raises certification (ablation A1); single-scenario use gains less than 20% (A3); endpoint-level beats scenario-level (A2). | To be tested (EXP-003, EXP-006) | Unknown. |
| CLM-012 | HYP (H3) | At least one estimated or heuristic screening baseline at comparable cost misses at least one violating triple on some evaluated configuration, while the proposed method misses none. | To be tested (EXP-006, EXP-007) | Unknown. CH3 may hold on small open corner sets. |
| CLM-013 | OBS | The packet lacks the required resources: only Nangate45 at the typical corner and GCD (`config/research-brief.json` lines 44-61). | SRC-028 to SRC-036, SRC-052 | Low for the listings; licenses partly unverified (see `experiment-plan.md`). |
| CLM-014 | OBS | No ICCAD or TAU contest found addresses MCMM scenario reduction. TAU 2013 addressed variation-aware parametric timing. | SRC-037 to SRC-040 | Medium. TAU 2018 and 2019 topics unresolved (login wall). |
| CLM-015 | INF | Novelty is not established. No accessed source describes per-scenario bounds that are sound with respect to the reference delay calculator, combined with exact refinement to reproduce full MCMM decisions. The nearest paper (SRC-012) was not inspected in full, and no forward-citation search was possible. | `search-log.md` | **High.** Kill criterion K1. |
| CLM-016 | OBS | Excluded slice S1 (decision-guarded incremental STA in repair loops) is substantially covered by prior patents and timers, and OpenROAD's repair loop consumes exact non-critical slacks. | SRC-008, SRC-009, SRC-011, SRC-041 to SRC-050 | Medium. See `search-log.md` § Excluded results. |
| CLM-017 | INF | An anchor-slack cutoff screen can miss a violation when the capture clock path is wire-dominated and the RC corner changes (constructed example below). | Constructed from the qualitative example in SRC-019 p. 7 | The arithmetic is exact; whether such structures occur in the evaluated open designs is unknown (EXP-003). |

## Closest prior work and explicit distinction

Full rows are in `prior-art.csv`. The closest independent approaches are:

1. **Bounding across corners from a few corner runs, plus clock-only runs for hold** (Onaissi et al., SRC-012; earlier linear-time work SRC-013).
   - *Overlap:* very high. It bounds slack across corners without timing every corner, and the hybrid hold method uses clock-network-only runs, an ingredient this proposal reuses.
   - *Distinction (provisional):* the proposed certificate for scenario s comes only from s's own characterized tables and parasitics and is sound with respect to the reference calculator's semantics. It uses no delay model over PVT space and no monotonicity in P, V or T. Uncertified triples get exact refinement, so the output equals full analysis.
   - *Status:* **unverified**, because SRC-012's assumptions were not read. If SRC-012 already bounds each discrete scenario soundly against table-level semantics and refines exactly, this candidate collapses (K1).
2. **Branch-and-bound exact worst corner under a linear delay model** (SRC-014).
   - *Distinction:* its exactness is relative to a linear parametric model; the proposal is exact relative to the reference engine on characterized libraries, and also delivers hold and per-endpoint slacks.
3. **Empirical slack-cutoff screening across parameter subspaces** (IBM, SRC-016).
   - *Overlap:* high in structure, since it bypasses paths whose slack exceeds a cutoff.
   - *Distinction:* the cutoffs are explicitly empirical estimates ("estimating an upper bound"); the proposal replaces them with a computed sound bound per triple.
4. **Dominant corner plus path-library ratio estimation, ML error classification and object marking** (Synopsys, SRC-017).
   - *Overlap:* high. It marks circuit objects with the corners in which they must be timed, which is close to the proposed cone-restricted refinement.
   - *Distinction:* marking is driven by estimates and ML rather than certificates; its own text gives no proof.
5. **Prediction with selective re-analysis** (TOTAL and the 2024 IEEE extension, SRC-023 and SRC-024; MCSTA, SRC-025; Kahng et al., SRC-015; MDPI 2022, SRC-022).
   - *Overlap:* structural. SRC-024's Bayesian strategy re-runs STA on uncertain predictions, a screen with exact fallback.
   - *Distinction:* their screen is statistical, a confidence about a learned predictor; the proposal's screen is a hard bound with no training data.
6. **Synthetic worst corners** (Synopsys, SRC-018).
   - *Distinction:* it makes analysis pessimistic, so decisions change; the proposal reproduces exact decisions.
7. **Industrial greedy selection plus margin** (SRC-021).
   - *Distinction:* it gives no coverage guarantee and pays margin; the proposal needs no margin.

[INF] **Every ingredient is individually known**: early/late (interval) propagation, Elmore upper bounds (SRC-026), Ceff ≤ C_total (resistive shielding, encoded in SRC-002 lines 969-974), clock-only partial runs (SRC-012) and selective re-analysis (SRC-017, SRC-024). The candidate's claimed contribution is a *formulation and guarantee*: exact equality with full MCMM analysis by construction under audited properties, at a cost proportional to the decision-ambiguous triples. Its utility is untested.

## Observed limitation and counterexample

**L1 [OBS].** Every accessed screening method selects what to skip using an estimate, empirical threshold, learned model or experience, without a certificate (CLM-002). The industrial response is extra margin (CLM-004).

**L2 [OBS/INF].** Accessed parametric bounding methods rest on a linear delay model over process and mode variables (CLM-005). Discrete multi-voltage and multi-temperature corners can be non-monotonic, for example under temperature inversion (SRC-019 p. 9). A model-based bound is therefore only as sound as the model. Whether this applies to SRC-012 is unverified.

**L3 [INF], constructed counterexample (CLM-017).** The numbers are hypothetical and chosen to instantiate the qualitative case in SRC-019 p. 7. Same netlist and cell library; two RC scenarios differ only in wire delay.

- Anchor scenario a (slow metal):
  - clock period T = 800 ps; setup time 50 ps;
  - launch clock latency 300 ps (cell 290, wire 10);
  - data path 1000 ps (cell 980, wire 20);
  - capture clock latency 600 ps (cell 100, wire 500).
  - Setup slack = 800 + 600 - 300 - 1000 - 50 = **+50 ps**.
- Scenario s (fast metal, every wire delay × 0.6):
  - launch 296 ps, data 992 ps, capture 400 ps.
  - Setup slack = 800 + 400 - 296 - 992 - 50 = **-138 ps**.

A screen that skips (endpoint, s) whenever the anchor slack is at least a cutoff of 25 ps (an SRC-016-style rule) misses this violation. The proposed method never uses a's slack to judge s. It bounds s directly, and here the certified lower bound at s is below 0, so the triple is refined exactly and reported. Whether wire-dominated capture paths of this kind occur in the evaluated open designs is measured in EXP-003; this example only shows the failure mode of anchor-relative screening, not its frequency.

**Why current methods don't address it.** Estimated and learned screens carry no certificate, and model-based bounds inherit the model's validity. Exhaustive analysis is safe but costs about one full pass per scenario.

**Why engineers care.** Vendors and practitioners state the no-miss requirement directly (SRC-020) and pay margin when they cannot meet it (SRC-021).

## Proposed mechanism and causal hypothesis

**Mechanism: certify, then refine.** For each scenario s in S, independently:

- **A. Exact clock analysis at s.** Time only the clock network: arrivals and latencies at register clock pins, using the reference engine restricted to clock-network vertices. Clock networks are a small fraction of the graph, and the hold method in SRC-012 uses the same ingredient.
- **B. Bound pass over the data network at s.**
  - Propagate upper bounds on late arrival and slew (AU, SU) and lower bounds on early arrival and slew (AL, SL), with no Ceff iteration.
  - **Cell arcs:** take the max or min of the arc's delay and slew tables over the box [SL, SU] × [C_lo, C_tot]. Here C_tot = c1 + c2 of the reduced net model; C_lo = 0 unless a tighter proven lower bound is established. Evaluate at the box corners, the table grid points inside the box, and the points where the box edges cross grid lines. This set is exact for piecewise-bilinear tables with edge-cell extrapolation (P1). If a table is verified monotone, a corner lookup suffices.
  - **Wire arcs:** upper bound = Elmore delay of the same reduced model the reference uses (P4); lower bound = 0. Load slew upper bound per P5; load slew lower bound = driver slew lower bound (the code enforces load slew ≥ driver slew within `DmpAlg::loadDelaySlew`, SRC-002 lines 555-605).
  - **Derates and uncertainty:** apply them exactly as the reference does.
  - **CRPR:** give no credit in the bound. This is conservative, because CRPR only adds slack.
- **C. Certify.**
  - Setup lower bound = exact capture-clock required time at s − AU(D) − (upper bound on setup time over the slew box).
  - Hold lower bound = AL(D) − exact hold required time at s − (upper bound on hold time).
  - A triple is *certified* if its lower bound is at least M.
- **D. Exact refinement.**
  - For the uncertified endpoints U_s, run the reference engine restricted to the union of their fan-in cones, data plus clock. Report exact slacks.
  - Certified triples are reported as "certified ≥ M" with the bound value logged.
  - If refinement fails or a cone cannot be isolated, fall back to full analysis of s.

**Soundness properties to establish.** These are stated against the pinned code; all are checked in EXP-002.

- **P1.** OpenSTA's NLDM evaluation is piecewise bilinear with edge-cell linear extrapolation (SRC-007), so box extremes lie on the finite set above. *Status: supported by code reading of the 2-D path; 3-D tables not inspected.*
- **P2.** Gate delay is the table value at (input slew, Ceff) with Ceff ∈ [0, c1+c2], including the failure fallback Ceff = c1+c2 (SRC-002 lines 915-948, 969-974). *Status: supported by code reading of the `DmpPi` path; the `DmpCap` and `DmpZeroC2` paths and the no-parasitic `LumpedCapDelayCalc` path still need checking.*
- **P3.** The driver slew passed downstream, taken from the waveform model when valid (SRC-002 line ~934), lies within a computable bound from the slew tables over the same box. *Status: not established; this is the highest-risk property.*
- **P4.** The load delay returned by the single-pole crossing (SRC-002 lines 555-605) is at most the Elmore delay of the reduced model. This is backed by SRC-026 for inputs with unimodal derivatives, but the numeric root-finding and threshold adjustment must be audited. *Status: not established.*
- **P5.** Load slew is at most a computable function of the driver slew bound and the Elmore delay. *Status: not established.*
- **P6.** The bound pass and the refinement use the same parasitic reduction and the same pinned code as the reference. *Status: a design invariant.*

If any of P2-P5 fails and cannot be repaired with a provable bound, the guarantee claim is withdrawn (K2).

**Causal hypothesis.**

- *Decision equivalence* follows by construction from sound bounds plus exact refinement (CLM-009).
- *The speedup*, if any, comes from three conditions together. Most (endpoint, scenario) triples in *non-dominant* scenarios have slack margins larger than the bound band. The bound pass and clock pass cost much less than exact delay calculation. Uncertified cones cover a small part of the graph per scenario.

[INF] This predicts the effect is concentrated where single-corner bound-then-refine fails. In a closed single-scenario design, many endpoints sit near zero slack, so bounds certify little. In MCMM, each endpoint is tight in only a few scenarios (SRC-019 p. 8).

**Cost model (for analysis, not a forecast).** Reduction ≈ 1 − mean over s of (b_s + r_s), where b_s is the cost of the clock and bound passes at s and r_s the cost of refinement at s, both relative to exact analysis of s. Shared fixed costs (parsing, graph build) dilute any gain (FM-02 in `first-pass-plan.md`), so they are measured separately in EXP-003.

## Structural or nontrivial combination contribution

**What naive compositions miss**:

1. *Bounds alone* cannot produce exact slacks, TNS or ECO lists for the violators that engineers act on.
2. *Refinement alone* is full analysis.
3. *Anchor-relative estimated cutoffs* are cheap but unsafe (L3).
4. *Bounding the clock network together with the data network* subtracts two loose quantities, so the slack band roughly doubles. [INF] Exact clock analysis per scenario is what keeps the band narrow enough to certify.
5. *Scenario-level certification*, which skips a whole scenario only if all its endpoints certify, discards most of the benefit when each scenario is tight for some endpoints.

**Ablations that test the interaction** (`experiment-plan.md`):

| Ablation | What changes |
|---|---|
| A1 | No exact clock pass; clock bounded too |
| A2 | Scenario-level instead of endpoint-level certification |
| A3 | Same mechanism applied to a single scenario |
| A4 | Vary the reporting margin M |
| A5 | Monotone-corner shortcut vs full extreme-point evaluation; tests the cost of soundness |

An oracle screen, which refines exactly the triples with reference slack below M, bounds the attainable gain from above.

## Counter-hypotheses and falsification criteria

| ID | Counter-hypothesis | Falsifies |
|---|---|---|
| CH1 | Bound bands are too wide relative to slack margins in non-dominant scenarios, so the certification rate is too low for a 20% gain. | H1 |
| CH2 | OpenSTA MCMM runtime is dominated by shared fixed phases (parsing, graph build, levelization) or by search rather than delay calculation, so per-scenario savings cannot reach 20% end to end. | H1 (via FM-02) |
| CH3 | On the available open corner sets (ASAP7 FF/SS/TT; SKY130 PVT corners with a single RC corner), simple dominance rules ("SS for setup, FF for hold") already miss no violations. | Shows H3 not demonstrated on this benchmark; does not falsify the guarantee. Reported as a negative result. |
| CH4 | P3-P5 fail for the pinned calculator. | The certificate (K2) |
| CH5 | Restricted refinement does not reproduce full-analysis slacks, because of global effects such as clock tags, CRPR, generated clocks or path-group interactions. | CLM-009, unless the mismatch is fixed by a corrected cone definition and re-verified |

## Remaining headroom and assumptions

- **Upper bound on the gain:** the oracle screen (EXP-003).
- **Lower bound:** none. The fallback to full analysis guarantees correctness, not speed; overhead can make the method slower.
- **Theoretical limit:** none claimed. Headroom is empirical and depends on the scenario set, the design and M.

**Assumptions**: the declared S is the signoff scenario set; all scenarios share the netlist and SDC; scenarios differ only in library and parasitics; the reference calculator is `dmp_ceff_elmore`; there is no SI.

**Residual risk.** A 3-corner set (ASAP7) may be too small to show a 20% gain. The 16-corner SKY130 set needs Liberty generation (EXP-001). No RC corners are available for either PDK (CLM-013).

## Resource and dependency feasibility

**Available in the packet**: pinned OpenROAD/OpenSTA in a digest-pinned container, Nangate45 at the typical corner, and GCD (`config/research-brief.json` lines 27-61). These are not sufficient on their own. Nangate45 has one corner, and the PHYSICAL-PILOT rules require at least three independent designs and additional corners (`docs/PHYSICAL-PILOT.md` line 27).

**Open prerequisites**, each with its license, listed in `experiment-plan.md` § Datasets and tracked in EXP-001:

- ASAP7 NLDM FF/SS/TT libraries (BSD-3-Clause upstream per SRC-032; ORFS copy provenance unverified);
- SKY130 hd multi-corner Liberty (16 PVT corners as `.lib.json`, SRC-030; skywater-pdk is Apache-2.0 per SRC-031, but the library repository's own license is unverified; conversion required);
- designs `aes`, `jpeg` (BSD-3-style, ASICs World Services) and `ibex_sv` (Apache-2.0), all ORFS master, to be pinned (SRC-034);
- RC corners: none available, since ORFS ships a single OpenRCX rules file per platform (SRC-035, SRC-036).

**Compute.** Whether P&R for 3 designs on 2 platforms plus repeated MCMM timing fits in 8 CPU-hours at 2 CPUs and 4 GiB per job is **unknown** (EXP-001 estimates it before any run). No GPU or paid API is needed.

**Implementation.** The mechanism is a C++ extension of the pinned OpenSTA behind a command flag: bound pass, clock-only search, and cone-restricted search predicates. Development effort is uncosted and is a real feasibility risk.

## Known unknowns and kill criteria

**Known unknowns** (each has a resolution task):

| ID | Unknown | Resolved by |
|---|---|---|
| U1 | SRC-012 full content and assumptions | Verifier/challenger full-text read; proposer re-attempt (EXP-001 step 0) |
| U2 | Soundness properties P3-P5 | EXP-002 |
| U3 | OpenSTA MCMM runtime breakdown | EXP-003 |
| U4 | Oracle-certifiable fraction and band widths on real designs | EXP-003 |
| U5 | Licenses: SKY130 hd library repository, ORFS ASAP7 copy provenance, design licenses at the pinned commit | EXP-001 |
| U6 | Compute fit | EXP-001 |
| U7 | Whether OpenSTA's search can be restricted to cones without global side effects | EXP-004 |
| U8 | TAU 2018 and 2019 contest topics | Contest audit follow-up |
| U9 | Practitioner validation of M and the 20% threshold | Human, per `config/research-brief.json` line 78 |

**Kill and stop criteria**:

| ID | Trigger | Consequence |
|---|---|---|
| K1 | A nearest-work full-text check (SRC-012 or another found source) shows per-scenario sound certification with exact refinement already exists | Abandon this ID or propose joint abandonment; a successor needs a new ID |
| K2 | P2-P5 cannot be made sound without empirical safety margins | The guarantee claim fails; do not continue as a "sound" method |
| K3 | EXP-003: the oracle screen plus measured pass costs gives below 20% predicted reduction on at least 2 of 3 designs for every available scenario set | Stop before implementation |
| K4 | Prerequisites (multi-corner libraries, designs, compute allocation) unobtainable within the pilot caps | Park with specific missing items |
| K5 | Any decision mismatch against B0 in EXP-006 not traced to a fixable implementation bug and re-verified | Stop |
| K6 | Combination or demand drift score of 2 or more on any revision | Stop under the charter's governance rule |

## Unresolved questions for the coordinator and human

1. Authorize the acquisition and conversion of the listed libraries and designs (EXP-001), and decide whether P&R for prerequisite generation counts against the 8 CPU-hour pilot cap.
2. Confirm whether the TAU 2018 and 2019 contest topics can be obtained (login wall).
3. Ask practitioners whether exact slacks are needed only for violators (M = 0) or also for near-critical lists (M > 0).
