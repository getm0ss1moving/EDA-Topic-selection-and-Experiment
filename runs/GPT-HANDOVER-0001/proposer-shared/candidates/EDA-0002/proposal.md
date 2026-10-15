# Proposal

**EDA-0002: Sound per-(endpoint, scenario) screening for multi-corner STA with exact refinement**

| Field | Value |
|---|---|
| Domain | D05 Timing, extraction and signoff (MCMM analysis, signoff fidelity, runtime) |
| Proposer | `Claude-P05-TIMING`, session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`, model `claude-opus-5-5` |
| Input | Packet `ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d`, input commit `d437c2f660906efe9351a90451905826d00b63e3` |
| Evidence window | Round 0: public sources retrieved 2026-10-13, 07:02-08:01 UTC. The round-0 files recorded 2026-10-12, 16:02-17:01 because the host clock ran 54,000 s behind UTC (`search-log.md` § Round 1, erratum E1). Round 1: GitHub and arXiv only, plus the owner-approved lab runner, 2026-10-14 UTC. |
| Revision | **Round 1 proposer revision before any challenge**, under owner decision CLD-LAB-0001 (`runs/CLD-P05-REVISION-0001/manifest.json`). The runner was used only for tooling, GitHub data and the P3-P5 property checks. No hypothesis, runtime, certifiable-fraction, band-width or real-design measurement was made. |
| Revision 1b | **Pre-freeze amendment, directed by the human owner on 2026-10-14** (`runs/CLD-P05-REVISION-0002/manifest.json`). It incorporates the challenger's independent first pass (`runs/CDX-C05-INDEPENDENT-0001/` at commit `b7822234`). That pass was written without the dossier and raises no objection to it, so nothing here responds to an adjudicated objection, and no verifier is assigned. The amendment adds:<br>- leads SRC-066 to SRC-068, which widen K1;<br>- an explicit list of preserved outputs;<br>- two soundness rules found while checking the challenger's priorities: timing exceptions (CLM-027) and float rounding (CLM-028);<br>- an incremental exact baseline and the ECO-loop question (CLM-029, CH8);<br>- certificate audits.<br>No experiment or runner job was run. |
| Status | **K2 is activated.** P3, P4 and P5 as stated in round 0 are falsified by reachable counterexamples (CLM-018 to CLM-020). The guarantee claim is narrowed to the capacitive-path certificate R1 (CLM-023), which is further restricted in 1b by the exception and rounding rules (P8, P9). Novelty is **not** established (CLM-015, CLM-026). Apart from the property-check counts, which are finite-test observations on synthetic fixtures, no claim below is a measurement. |

Labels: **[OBS]** sourced observation · **[INF]** my inference · **[HYP]** hypothesis to test · **[FCST]** forecast. Source IDs refer to `sources.json`; packet files are cited by path and line.

Property-status labels, as defined by the runner instructions:

| Label | Meaning |
|---|---|
| `proved` | Proved; nothing in this dossier currently carries this label |
| `code-argument-only` | A careful reading of the pinned code, not machine-checked |
| `finite-tests-pass` | Passed the stated finite fixtures only; not a proof |
| `falsified` | A counterexample exists |
| `unresolved` | None of the above |

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
- [OBS] The worst scenario differs by path, so removing "dominated" scenarios can miss violations (CLM-003). One source finds each path is worst at only 3-4 corners, and those corners differ by path; a cell-dominated launch path paired with a metal-dominated capture path needs SS combined with fast metal (SRC-019 pp. 7-8). SRC-012's abstract excerpt makes a similar statement about hold. Under owner decision U1 that excerpt is not relied on.
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

**Preserved and not preserved (round 1b).** The challenger's first pass asks that the preserved result be fixed in advance (`runs/CDX-C05-INDEPENDENT-0001/independent-estimate.md`, priority 1). The equality claim covers only the following.

| Output | Preserved exactly? |
|---|---|
| Violation flag of every (endpoint, scenario, check) triple, for setup, hold, recovery and removal checks, including output-delay endpoints | Yes |
| Slack of every triple with slack < M | Yes |
| WNS and TNS per scenario and check type, when negative | Yes |
| Slack of a triple with slack ≥ M | No. Reported as "certified ≥ M" with the logged bound, or exactly if the triple was refined |
| Path detail (`report_checks` paths) for certified triples | No |
| Inferred clock-gating checks, data-to-data checks (`set_data_check`), minimum pulse width, minimum period and maximum skew | No (v1) |
| Design-rule limits: maximum slew, capacitance and fanout | No (v1) |
| SI, POCV and the other out-of-scope effects listed above | Not modelled by the reference either |

These limits do not change the downstream need: D_M(S) has had this definition since round 0. B0 comparisons (G1-G4) use exactly the preserved rows.

**Use setting (round 1b).** P is a from-scratch analysis: after reading a new netlist or SPEF, for example after re-extraction in a closure iteration, and for a signoff run. Inside an ECO loop that edits a timed design without re-extraction, an incremental exact update is the natural competitor (CLM-029). This matches the round-0 exclusion of the repair-loop slice S1 (CLM-016), so the user and the need are unchanged. Whether P still pays off in such a loop is the open question CH8. It is measured as a secondary comparison and is not part of H1.

**Correctness oracle.** Full multi-corner analysis of S with the same pinned OpenSTA build, all scenarios in one run (`define_corners`, SRC-005; `Corners::makeAnalysisPts`, SRC-006). This is a *decision reference*, not a qualified signoff oracle: the packet makes no claim of silicon signoff or multi-corner coverage (`config/research-brief.json` line 65). Every claim here is therefore "fidelity to pinned OpenSTA".

## Claim ledger (ID, type, source, locator, uncertainty)

| ID | Type | Statement | Source and locator | Uncertainty |
|---|---|---|---|---|
| CLM-001 | OBS | Signoff scenario sets run from tens to hundreds of scenarios. | SRC-021 body; SRC-015 abstract; SRC-020 body; SRC-019 pp. 7-8 | Medium. Mostly vendor or practitioner sources; no controlled survey. |
| CLM-002 | OBS | Accessed reduction methods use estimated, empirical, learned or experience-based criteria with no formal guarantee against missed violations. | SRC-016 description; SRC-017 description; SRC-018 description; SRC-015 abstract; SRC-021 body; SRC-022 to SRC-025 (abstract-level) | Medium. Several sources were seen at abstract or metadata level only. |
| CLM-003 | OBS | The worst scenario differs by path or endpoint; dropping scenarios can miss violations; hold resists small-corner-set bounding. | SRC-019 pp. 7-9 | Medium. SRC-012's excerpt is not relied on (owner decision U1). |
| CLM-004 | OBS | Practice demands no missed failing endpoints and covers residual risk with extra hold uncertainty of 10-20 ps. | SRC-020; SRC-021 | Low for "stated practice"; unknown for prevalence. |
| CLM-005 | OBS | Parametric all-corner bounding and branch-and-bound engines model cell delays as linear functions of process or mode variables. | SRC-014 slides 14-15 (citing SRC-013) | Low for SRC-013 and SRC-014. **High for SRC-012, whose assumptions were not read.** Round 1b: SRC-068's title claims general delay models, so "linear" may not hold for the whole family (unread). |
| CLM-006 | OBS | Pinned OpenSTA times all corners in one run; its default calculator is `dmp_ceff_elmore`; seven calculators are registered. | SRC-005 lines 3663-3672; SRC-006 lines 88 and 174; SRC-003 lines 411 and 417; SRC-004 lines 37-43 | Low (code reading). |
| CLM-007 | OBS | In pinned `dmp_ceff_elmore`, the variant (`DmpCap`, `DmpZeroC2`, `DmpPi`) is chosen from the pi model and an input-slew-dependent Rd. On the `DmpPi` path, gate delay is a table lookup at a solved Ceff in [0, 1.01·(c1+c2)]: the last Newton step is unchecked. On that path the driver slew is measured on the pi-model waveform, not looked up. On the `DmpZeroC2` path the gate delay is also taken from the waveform. Wire delay and load slew are root-found crossings of a single-pole response to that waveform, with Elmore and driver-slew fallbacks and no upper clamp. NLDM tables are bilinear with edge-cell linear extrapolation, and slews are clipped at 0. *Round 1 correction of the round-0 statement.* | SRC-002 lines 479-489, 555-607, 915-949, 965-1025, 1222-1241, 1281-1312, 1545-1585; SRC-007 lines 104-135, 1012-1068, 1443-1463; SRC-060 | Low for the code facts (code-argument-only). |
| CLM-008 | INF | *Round-0 claim, now **falsified** as a general rule.* It claimed that table-box cell bounds plus Elmore wire bounds give sound per-scenario arrival and slew bounds for every net. P3-P5 fail on the DMP waveform path (CLM-018 to CLM-020). The surviving restricted form is CLM-023. | SRC-002; SRC-007; `runs/CLD-P05-REVISION-0001/p3-p5-record.md` § 5 | Resolved: falsified. |
| CLM-009 | INF | If the bounds are sound, restricting exact analysis to uncertified triples reproduces D_M(S) exactly. Every violating triple is uncertified when M ≥ 0, so violation lists, sub-margin slacks and TNS are exact. | Logic from the definitions; now depends on CLM-023 instead of CLM-008, and from round 1b on the exception and rounding rules (CLM-027, CLM-028) | Medium. Depends on correct cone extraction and global effects (CRPR, clock tags, multi-driver nets, timing exceptions; CLM-024, CLM-027); see CH5. |
| CLM-010 | HYP (H1) | On at least 3 independent designs and a multi-scenario set S, the screened analysis reproduces D_M(S) exactly and takes at least 20% less end-to-end wall time than the strongest full-MCMM baseline (B0) under equal resources. | To be tested (EXP-006, EXP-007); threshold from `config/research-brief.json` line 77 | Unknown. No measurement. |
| CLM-011 | HYP (H2) | The speedup comes from certifying non-dominant (endpoint, scenario) triples. Predicted signatures: higher certification in non-dominant scenarios; exact clock analysis materially raises certification (ablation A1); single-scenario use gains less than 20% (A3); endpoint-level beats scenario-level (A2). | To be tested (EXP-003, EXP-006) | Unknown. |
| CLM-012 | HYP (H3) | At least one estimated or heuristic screening baseline at comparable cost misses at least one violating triple on some evaluated configuration, while the proposed method misses none. | To be tested (EXP-006, EXP-007) | Unknown. CH3 may hold on small open corner sets. |
| CLM-013 | OBS | The packet lacks the required resources: only Nangate45 at the typical corner and GCD (`config/research-brief.json` lines 44-61). | SRC-028 to SRC-036, SRC-052 | Low for the listings; licenses partly unverified (see `experiment-plan.md`). |
| CLM-014 | OBS | Among the contest records inspected, no ICCAD or TAU contest topic concerns MCMM scenario reduction. TAU 2013 concerned variation-aware parametric timing. The TAU 2018 topic was timing reports from an STA graph, and TAU 2019 was timing-driven optimization (topic-level GitHub record SRC-059, corroborated by SRC-053 to SRC-056). This is not a claim that no relevant contest exists. | SRC-037 to SRC-040, SRC-053 to SRC-056, SRC-059 | Medium. TAU 2018 and 2019 rules, formats and winner reports were not inspected. |
| CLM-015 | INF | Novelty is not established. No accessed source describes per-scenario bounds that are sound with respect to the reference delay calculator, combined with exact refinement to reproduce full MCMM decisions. The nearest paper's assumptions (SRC-012) remain unresolved under owner decision U1: arXiv and GitHub hold no copy. A forward-citation screen of SRC-012 (ADD-0001; SRC-057, SRC-058) found only learned predictors, at title or abstract level. Round 1b adds three unread leads from the same research line: SRC-066 (certified path elimination), SRC-067 (exact worst-delay corner) and SRC-068 (general delay models). | `search-log.md`; SRC-057; SRC-058; SRC-066 to SRC-068 | **High.** Kill criterion K1 remains open and now covers SRC-066 to SRC-068. |
| CLM-016 | OBS | Excluded slice S1 (decision-guarded incremental STA in repair loops) is substantially covered by prior patents and timers, and OpenROAD's repair loop consumes exact non-critical slacks. | SRC-008, SRC-009, SRC-011, SRC-041 to SRC-050 | Medium. See `search-log.md` § Excluded results. |
| CLM-017 | INF | An anchor-slack cutoff screen can miss a violation when the capture clock path is wire-dominated and the RC corner changes (constructed example below). | Constructed from the qualitative example in SRC-019 p. 7 | The arithmetic is exact; whether such structures occur in the evaluated open designs is unknown (EXP-003). |
| CLM-018 | OBS | **P3 as stated is falsified.** The driver slew lies outside the table-slew box at the arc's own input slew on 3,553 of 19,600 driver arcs, all on the DMP waveform path. 896 of these come from SPEF RC trees with internally consistent tables (reachable). The worst value is 1.334 × the box maximum; the low side reaches 0.966 × the box minimum. | `runs/CLD-P05-REVISION-0001/p3-p5-record.md` § 5; SRC-002 lines 479-489, 915-949; SRC-063 | Finite-test observation on synthetic fixtures. |
| CLM-019 | OBS | **P4 as stated is falsified.** Wire delay exceeds the reduced-model Elmore delay on 100 of 52,088 wire arcs. 12 of these are reachable with consistent tables, the worst being +1.9% (+3.7 ps); the maximum over all fixtures is +15.9%. | `runs/CLD-P05-REVISION-0001/p3-p5-record.md` § 5; SRC-002 lines 555-607; SRC-060 | Finite-test observation. |
| CLM-020 | OBS | **P5 as stated is falsified.** Load slew exceeds driver slew plus the single-pole increment τ·ln((1−vl)/(1−vh))/k on 3,025 of 52,088 wire arcs. 1,543 of these are reachable with consistent tables; the worst is 1.907 × the bound, and the maximum is 2.14 ×. | `runs/CLD-P05-REVISION-0001/p3-p5-record.md` § 5; SRC-062 lines 108-124 | Finite-test observation. |
| CLM-021 | INF | **Capacitive path and lower bounds.** On the `DmpCap` path, and on nets without parasitics, driver slew = T(s, C), gate delay = D(s, C), wire delay = τ and load slew = driver slew, exactly. On every path, wire delay ≥ 0, load slew ≥ driver slew and driver slew ≥ 0, provided driver and loads share one library. | SRC-002 lines 555-607, 737-773, 1531-1542; SRC-007 lines 104-135; SRC-061; SRC-065 | code-argument-only + finite-tests-pass (603 driver and 1,613 wire arcs on the capacitive path; 52,088 wire arcs for the lower bounds; zero violations). |
| CLM-022 | INF | **Bracket bounds.** On the waveform path, root brackets bound driver slew, wire delay and load slew by dt + 2C'(Rd + Rpi) (+ 2τ for loads), divided by the slew derate where applicable. Rd and dt are DMP-internal. Bounding dt from the tables (assumption ADT) is not established by the code. | SRC-002 lines 479-489, 631-635, 1076-1080, 1269-1273; SRC-060 | code-argument-only + finite-tests-pass for the bounds. ADT is finite-tests-pass (maximum ratio 1.0077) but **unresolved** as a proof. |
| CLM-023 | INF | **Narrowed certificate R1.** Bounds are sound when every data net in an endpoint's fan-in cone at scenario s is on the capacitive path for every input slew in its interval. A certificate built only from such cones, with the remaining rules of § Mechanism, therefore never misses a violation. | CLM-021; P1 (SRC-007); P6 | code-argument-only. The share of cones it covers on real designs is unknown (owner item U4; deferred). |
| CLM-024 | OBS | **Code-level side effects for refinement and bounding.** Delay calculation for a multi-driver net uses all parallel drivers. The driver waveform depends on the whole net, not only the cone's loads. `thresholdAdjust` alters wire delay and slew when libraries differ. A pi model with less capacitance than its pin caps is ignored. | SRC-008 lines 940-967, 1255-1271; SRC-062 lines 127-153 | code-argument-only. These are recorded as threats with required falsification tests. |
| CLM-025 | OBS | **P2 as stated is falsified for the `DmpZeroC2` path.** There the gate delay is the waveform crossing, not a table value (2,171 of 2,258 arcs differ from the table at C1). It stayed within [D(s,0), D(s,C)] on all 2,258 arcs. | SRC-002 lines 1222-1241; `runs/CLD-P05-REVISION-0001/p3-p5-record.md` § 5 | Falsified as stated. The box membership is finite-tests-pass and **unresolved** as a proof. |
| CLM-026 | INF | *(Round 1b.)* **Certified elimination is not new in itself.** Classical parameterized timing removes paths that cannot be critical for any parameter value while preserving the timing envelope. It distinguishes sufficient pairwise pruning from exact feasibility-based pruning (SRC-066, as paraphrased by the challenger). Branch-and-bound engines prune with bounds (SRC-014), and exact worst-corner computation exists (SRC-067). The remaining distinction is narrower: soundness with respect to a reference engine's discrete-scenario semantics, with no parametric delay model, plus exact reproduction of per-(endpoint, scenario, check) decisions. R1 is a sufficient, incomplete test in this sense, and the oracle screen O plays the role of the exact feasibility test. | SRC-014 slides 7, 21 and 29; SRC-066 to SRC-068 (metadata) | **High.** SRC-066 to SRC-068 are unread. The distinction holds only if their full texts do not cover discrete characterized corners with reference-engine soundness (K1). |
| CLM-027 | OBS | *(Round 1b.)* **Timing exceptions can make an exception-blind bound unsound.** In pinned OpenSTA the multicycle adjustment is added to the target clock arrival. For a hold check under a multicycle path declared with `-setup` and multiplier N ≥ 2, it is (N − 1) × period. The hold requirement therefore moves later and hold slack falls, by an amount that depends on the path. A bound that used the default required time would overstate hold slack. [INF] Maximum and minimum delay exceptions also set the requirement per path (SDC semantics; this code was not traced). False paths only remove paths, so a bound that ignores them stays conservative. | SRC-069 lines 649-656; SRC-070 lines 624-633, 776-831 | code-argument-only for the multicycle case. Exception matching, tag handling and delay exceptions were not traced. |
| CLM-028 | OBS/INF | *(Round 1b.)* **Rounding.** Delays, slews, arrivals and slacks are 32-bit floats in the pinned build [OBS]. P1 puts table extremes at a finite point set in exact arithmetic, but a float evaluation at an interior slew can exceed the float maximum over that set by a few ulps [INF]. IEEE round-to-nearest addition and max are monotone, so a bound chain stays sound against B0's own float results if each table bound is raised by a derived rounding allowance [INF]. That allowance is computed from the format, not calibrated on data, so it is not an empirical safety margin under K2. | SRC-071 DelayFloat.hh line 27, Delay.hh lines 21-38; SRC-064 lines 399-400; SRC-007 | code-argument-only. The allowance's size and its sufficiency need the EXP-002b finite tests (P9). |
| CLM-029 | INF | *(Round 1b.)* **Incremental exact timing is the competitor in ECO loops.** The pinned engine updates delays, arrivals and required times incrementally after edits (SRC-001; challenger S05 for the upstream README). A certificate is valid only for the netlist and parasitics it was computed on, and an edit invalidates every certificate whose cone, or whose nets' loads, it touches (CLM-024). In a loop of small edits, B6 may therefore beat P even if P beats B0. | SRC-001; SRC-008 lines 588-589; CLM-016 | Unknown. Tested as CH8 (EXP-007). |

## Closest prior work and explicit distinction

Full rows are in `prior-art.csv`. The closest independent approaches are:

1. **Bounding across corners from a few corner runs, plus clock-only runs for hold** (Onaissi et al., SRC-012; earlier linear-time work SRC-013).
   - *Overlap:* very high. It bounds slack across corners without timing every corner, and the hybrid hold method uses clock-network-only runs, an ingredient this proposal reuses.
   - *Distinction (provisional):* the proposed certificate for scenario s comes only from s's own characterized tables and parasitics and is sound with respect to the reference calculator's semantics. It uses no delay model over PVT space and no monotonicity in P, V or T. Uncertified triples get exact refinement, so the output equals full analysis.
   - *Status:* **unresolved** (owner decision U1). The round-1 re-attempt through arXiv and GitHub found no copy, so SRC-012's assumptions are not inferred from excerpts.
     - A proposer reading of an Internet Archive capture exists in `addenda/EDA-0002/ADD-0001`. It was made before decision U1 and is held for the owner's admissibility ruling; this revision does not use it.
     - If SRC-012 already bounds each discrete scenario soundly against table-level semantics and refines exactly, this candidate collapses (K1).
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
8. **Certified elimination in parameterized timing, and exact worst-corner computation** (SRC-066, SRC-067, SRC-068; added in round 1b from the challenger's first pass and from SRC-014's reference list).
   - *Overlap:* potentially very high. These works soundly discard work that cannot change the timing envelope, or compute the exact worst corner, which is the same guarantee style (CLM-026).
   - *Distinction (provisional):* the proposal has no parametric delay model. Its scenarios are discrete characterized corners, its soundness is stated against the reference calculator's code, and its output is the per-triple decision set, not a worst delay.
   - *Status:* **unresolved.** None of the three has been read by the proposer. All are outside the GitHub and arXiv routes, and arXiv and GitHub hold no copy (`search-log.md` Q45, Q46). They join SRC-012 under K1.

[INF] **Every ingredient is individually known**: early/late (interval) propagation, Elmore upper bounds (SRC-026), Ceff ≤ C_total (resistive shielding, encoded in SRC-002 lines 969-974), clock-only partial runs (SRC-012, excerpt level), selective re-analysis (SRC-017, SRC-024) and, from round 1b, sound envelope-preserving elimination (SRC-066, unread; CLM-026). The candidate's claimed contribution is a *formulation and guarantee*: exact equality with full MCMM analysis by construction under audited properties, at a cost proportional to the decision-ambiguous triples.

[INF] Round 1 shows that the Elmore-type wire bound does **not** hold for the pinned calculator (CLM-019). The guarantee therefore rests on the narrower capacitive-path certificate (CLM-023), and its utility is untested.

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

- **A. Exact clock analysis at s.** Time only the clock network: arrivals and latencies at register clock pins, using the reference engine restricted to clock-network vertices. Clock networks are a small fraction of the graph. SRC-012's abstract describes clock-only partial runs; this is excerpt level only (owner decision U1).
- **B. Bound pass over the data network at s (round 1: narrowed rules R1).**
  - Propagate upper bounds on late arrival and slew (AU, SU) and lower bounds on early arrival and slew (AL, SL), with no Ceff iteration.
  - **Net classification.** A data net is *capacitive-path certain* (CPC) at s if the pinned variant selection (SRC-002 lines 1545-1585) chooses `DmpCap` for every input slew in its driver's interval [SL, SU]. Nets without parasitics also count, since they use the lumped table at the known load (SRC-065). Sufficient tests:
    - **Structural:** C1 = 0, Rpi = 0, or C1 < 1e-3·C2.
    - **Rd-interval:** Rd(s) is the same 1 fF finite difference of the delay table at C1+C2 as `gateModelRd` (lines 1630-1649). Over [SL, SU] it is piecewise linear, so it is evaluated at the interval ends and the slew grid points. The net is CPC if min Rd > 1000·Rpi, or max Rd < 1e-2 Ω, each with a float32 rounding allowance.
    - **v1 exclusions:** multi-driver nets and nets whose load library differs from the driver library are never CPC (CLM-024).
  - **CPC nets** (exact code paths, CLM-021):
    - gate delay ∈ [min, max] of D(s, C) over s ∈ [SL, SU], with C = C1 + C2 fixed;
    - driver slew ∈ [min, max] of T(s, C) over the same interval. Extremes lie at the interval ends and the slew grid points (P1);
    - wire delay = τ exactly (0 when the load has no Elmore entry);
    - load slew = the driver-slew interval.
  - **Non-CPC nets** get no bound. Any endpoint whose data fan-in cone at s contains a non-CPC net is uncertified at s. The round-0 rules (table box over [0, C1+C2], Elmore wire bound, P5 slew rule) are withdrawn because P3-P5 are falsified (CLM-018 to CLM-020).
  - **Derates and uncertainty:** apply them exactly as the reference does.
  - **CRPR:** give no credit in the bound. This is conservative, because CRPR only adds slack.
  - **Timing exceptions (round 1b, P8; CLM-027).** An endpoint is never certified, at any scenario, if a multicycle, maximum-delay or minimum-delay exception could match one of its paths. That is, the exception's `-from`, `-through` or `-to` objects (pins, instances or clocks) meet the endpoint, its data fan-in cone, or its launch or capture clocks. False paths and disabled arcs are ignored by the bound; this keeps it conservative, because it then bounds a superset of the constrained paths. Exact refinement applies the exceptions as the reference does.
  - **Rounding (round 1b, P9; CLM-028).** Every table bound is raised (for upper bounds) or lowered (for lower bounds) by a rounding allowance derived from the float32 format and the table's magnitude. Every sum and max in the bound pass is then an ordinary float operation, so the bounds stay ordered against B0's own float results.
- **C. Certify.**
  - Setup lower bound = exact capture-clock required time at s − AU(D) − (upper bound on setup time over the data-slew interval, at the exact clock slew).
  - Hold lower bound = AL(D) − exact hold required time at s − (upper bound on hold time).
  - A triple is *certified* if its lower bound is at least M, its data fan-in cone is entirely CPC, and no exception rule excludes its endpoint.
  - The certificate log records, per certified triple, the lower bound, its rounding allowance and the scenario, so that every certificate can be audited against B0 (guardrail G7 in `experiment-plan.md`).
- **D. Exact refinement.**
  - For the uncertified endpoints U_s, run the reference engine restricted to the union of their fan-in cones, data plus clock, closed over whole nets and over all drivers of multi-driver nets (CLM-024). Report exact slacks.
  - Certified triples are reported as "certified ≥ M" with the bound value logged.
  - If refinement fails or a cone cannot be isolated, fall back to full analysis of s.
- **Certificate validity (round 1b; CLM-029).** A certificate holds only for the netlist, SDC, libraries and parasitics it was computed on. Any edit invalidates the certificates of every endpoint whose data cone or capture clock path contains an edited cell or net, or a net whose load an edit changed. P v1 makes no attempt to maintain certificates: after an edit, it is re-run from scratch. The ECO-loop comparison (CH8) measures what that costs against incremental exact timing.

**Conditional variant R1-C (not part of the guarantee claim).** For DMP waveform-path nets, the root-bracket bounds of CLM-022 would give computable bounds only if the ramp-fit assumption ADT held. ADT is finite-tests-pass and unresolved as a proof. The bounds are also loose, spanning several RC time constants per net. R1-C may be studied only as a separately labelled conditional rule. It is never reported as sound, and it is never mixed into R1 certificates (forbidden pivot in `direction-control.json`).

**Soundness properties and round-1 status.** These are stated against pinned `e01d3f16`. The full record, with build, fixtures, commands, invariants and counterexamples, is `runs/CLD-P05-REVISION-0001/p3-p5-record.md`.

| ID | Property (round-0 statement, then round-1 narrowing) | Status |
|---|---|---|
| P1 | NLDM evaluation is piecewise bilinear with edge-cell linear extrapolation, and slews are clipped at 0, so interval and box extremes lie at a finite point set (SRC-007 lines 104-135, 1012-1068, 1443-1463) | **code-argument-only** for 2-D tables; the fixtures' table replication agrees. 3-D tables: **unresolved** (not inspected) |
| P2 | Gate delay is the table value at (s, Ceff) with Ceff ∈ [0, C1+C2] | `DmpPi`: **code-argument-only + finite-tests-pass** with Ceff ∈ [0, 1.01·(C1+C2)]; 16,739 arcs, Ceff ≤ C1+C2 in all. `DmpCap` and lumped: **code-argument-only + finite-tests-pass** (Ceff = C). `DmpZeroC2`: **falsified** as stated (CLM-025); its delay box membership is **unresolved** |
| P3 | Driver slew lies in the table-slew box over [0, C1+C2] | **falsified** (CLM-018). Narrowed: on CPC nets driver slew = T(s, C), and driver slew ≥ 0 everywhere: **code-argument-only + finite-tests-pass** (CLM-021) |
| P4 | Wire delay ≤ Elmore delay of the reduced model | **falsified** (CLM-019). Narrowed: on CPC nets wire delay = τ, and wire delay ≥ 0 everywhere: **code-argument-only + finite-tests-pass** |
| P5 | Load slew ≤ f(driver slew bound, Elmore); tested with OpenSTA's own single-pole increment | **falsified** (CLM-020). Narrowed: on CPC nets load slew = driver slew, and load slew ≥ driver slew everywhere: **code-argument-only + finite-tests-pass** |
| P6 | The bound pass and refinement use the same parasitic reduction and the same pinned code as the reference | Design invariant. The fixtures' independent reduction matches the pinned reducer to 2e-6 |
| P7 (new) | The CPC tests above imply the `DmpCap` branch for every slew in the interval | **code-argument-only**. Finite tests are still required (task list EXP-002b), including float32 rounding at the 1e-3 and 1e-2 Ω thresholds |
| P8 (round 1b) | Endpoints that no multicycle or delay exception can match have the default clock-derived requirement. Ignoring false paths and disabled arcs keeps the bounds conservative | **code-argument-only** for multicycle paths (CLM-027). Delay exceptions and exception matching: **unresolved** (not traced). Finite tests in EXP-002b |
| P9 (round 1b) | With the derived rounding allowance, every float bound in the pass is on the safe side of the reference's float value | **unresolved.** The argument is in CLM-028; the allowance's size and its sufficiency are tested in EXP-002b |

**K2 is activated.** P3-P5 cannot support the round-0 certificate without an empirical safety margin. The guarantee claim is therefore **revised**, not converted into a heuristic: zero missed violations is claimed only for certificates built from CPC cones (R1, CLM-023) on endpoints that the exception rule admits (P8), with the rounding allowance (P9). That claim is itself code-argument-only and needs verifier review and the EXP-002b tests. Every other triple is refined exactly.

**Causal hypothesis.**

- *Decision equivalence* follows by construction from the R1 bounds plus exact refinement (CLM-009, CLM-023).
- *The speedup*, if any, now needs five conditions together:
  - a large share of (endpoint, scenario) data fan-in cones is CPC;
  - few endpoints are excluded by the exception rule (round 1b; P8);
  - most such triples in *non-dominant* scenarios have slack margins larger than the bound band;
  - the bound pass and clock pass cost much less than exact delay calculation;
  - uncertified cones cover a small part of the graph per scenario.
- [INF] The first condition is new and may fail. A net is CPC only if its reduced Rpi is below about 1/1000 of the driver's Rd, which suggests that only very short nets qualify. That share has not been measured (owner item U4) and is the first check in EXP-003 (CH6, K3).

[INF] The effect is still predicted to concentrate where single-corner bound-then-refine fails. In a closed single-scenario design, many endpoints sit near zero slack, so bounds certify little. In MCMM, each endpoint is tight in only a few scenarios (SRC-019 p. 8).

**Cost model (for analysis, not a forecast).** Reduction ≈ 1 − mean over s of (b_s + r_s), where b_s is the cost of the clock and bound passes at s and r_s the cost of refinement at s, both relative to exact analysis of s. Shared fixed costs (parsing, graph build) dilute any gain (FM-02 in `first-pass-plan.md`), so they are measured separately in EXP-003.

**Accounting identity (round 1b, following the challenger's first pass).** Every comparison charges the whole flow:

T_P = T_fixed + T_classify + T_clock + T_bound + T_certify + T_refine + T_report (+ T_maintain in an edit loop).

- T_fixed covers parsing, linking, graph build and parasitic reduction.
- T_classify covers the CPC tests and the exception rule.
- In v1, T_maintain is a full re-run of P after each edit (§ Mechanism, certificate validity).

A gain counts only if T_P is below the matched exact baseline's time for identical preserved outputs: B0 from scratch, or B6 inside an edit loop.

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
| CH4 | P3-P5 fail for the pinned calculator. | **Confirmed in round 1** (CLM-018 to CLM-020). K2 is activated and the certificate is narrowed to R1. |
| CH6 | CPC cones are rare in real designs at the evaluated scenarios, so R1 certifies too few triples for a 20% gain. | H1 (via K3); tested first in EXP-003 |
| CH7 | The R1 code argument is wrong: a CPC-classified net takes a non-`DmpCap` path, or a `DmpCap` result differs from the exact table at C. | CLM-023 and the guarantee (K7) |
| CH5 | Restricted refinement does not reproduce full-analysis slacks, because of global effects such as clock tags, CRPR, generated clocks, timing exceptions or path-group interactions. | CLM-009, unless the mismatch is fixed by a corrected cone definition and re-verified |
| CH8 | (Round 1b.) In an edit loop without re-extraction, incremental exact timing of all scenarios (B6) is faster than re-running P, so P's gain is limited to from-scratch analyses. | Does not falsify H1, which is a from-scratch claim. It bounds the claim's scope, and the result is reported either way (EXP-007) |
| CH9 | (Round 1b.) Near the margin, rounding or tie handling makes a certified triple differ from B0: its B0 slack falls below its logged bound, or below M. | P9 and CLM-023 (K7) |

## Remaining headroom and assumptions

- **Upper bound on the gain:** the oracle screen (EXP-003).
- **Lower bound:** none. The fallback to full analysis guarantees correctness, not speed; overhead can make the method slower.
- **Theoretical limit:** none claimed. Headroom is empirical and depends on the scenario set, the design and M.

**Assumptions**: the declared S is the signoff scenario set; all scenarios share the netlist and SDC; scenarios differ only in library and parasitics; the reference calculator is `dmp_ceff_elmore`; there is no SI.

**Round-1 headroom caveat [INF].** Under R1, the attainable gain is bounded above by the share of triples with CPC fan-in cones. That share is unmeasured; measuring it on real designs is deferred by the owner (U4). A small share would make the oracle bound itself small, whatever the slack distribution.

**Residual risk.** A 3-corner set (ASAP7) may be too small to show a 20% gain. The 16-corner SKY130 set needs Liberty generation (EXP-001). No RC corners are available for either PDK (CLM-013).

## Resource and dependency feasibility

**Available in the packet**: pinned OpenROAD/OpenSTA in a digest-pinned container, Nangate45 at the typical corner, and GCD (`config/research-brief.json` lines 27-61). These are not sufficient on their own. Nangate45 has one corner, and the PHYSICAL-PILOT rules require at least three independent designs and additional corners (`docs/PHYSICAL-PILOT.md` line 27).

**Open prerequisites**, each with its license, listed in `experiment-plan.md` § Datasets and tracked in EXP-001:

- ASAP7 NLDM FF/SS/TT libraries (BSD-3-Clause upstream per SRC-032; ORFS copy provenance unverified);
- SKY130 hd multi-corner Liberty (16 PVT corners as `.lib.json`, SRC-030; skywater-pdk is Apache-2.0 per SRC-031, but the library repository's own license is unverified; conversion required);
- designs `aes`, `jpeg` (BSD-3-style, ASICs World Services) and `ibex_sv` (Apache-2.0), all ORFS master, to be pinned (SRC-034);
- RC corners: none available, since ORFS ships a single OpenRCX rules file per platform (SRC-035, SRC-036).

**Compute.**

- **Owner decision U6:** prerequisite P&R is not authorized in this round and has no pilot allocation. Its cost must be estimated and explicitly allocated in the jointly accepted task list.
- **Runner ceiling:** the owner-approved file-mediated runner has a 300 core-hour infrastructure ceiling, which is not a scientific allocation. This round used 0.45 core-hours (`runs/CLD-P05-REVISION-0001/evidence/runner-ledger.json`).
- Whether P&R plus repeated MCMM timing fits the pilot's 8 CPU-hours is **unknown**.
- No GPU or paid API is needed.

**Tooling now available (round 1).** Pinned OpenSTA `e01d3f16` is built on the runner from GitHub sources only, following its own build rules (SRC-064).

- **Toolchain:** CMake, flex, byacc, Tcl, SWIG and Eigen, with each repository's license recorded.
- **Deviation:** GNU bison was replaced by byacc through a CLI wrapper. The C++ sources and grammars are unmodified, but the generated parsers differ from a bison build.
- Details: `runs/CLD-P05-REVISION-0001/p3-p5-record.md` § 2.

**Implementation.** The mechanism is a C++ extension of the pinned OpenSTA behind a command flag: bound pass, clock-only search, and cone-restricted search predicates. Development effort is uncosted and is a real feasibility risk.

## Known unknowns and kill criteria

**Known unknowns** (each has a resolution task). Round-1 status follows owner decision CLD-LAB-0001:

| ID | Unknown | Round-1 status and resolution |
|---|---|---|
| U1 | SRC-012 full content and assumptions | **Unresolved.** arXiv and GitHub, the only permitted routes, hold no copy. The archived reading in ADD-0001 awaits the owner's admissibility ruling. Verifier full-text read required (K1). |
| U2 | Soundness of P3-P5 | **Resolved: falsified as stated.** K2 is activated, and the narrowed properties are labelled in § Mechanism. Open follow-ups: P7 finite tests (EXP-002b); 3-D tables (P1); `DmpZeroC2` delay box (P2). |
| U3 | OpenSTA MCMM runtime breakdown | **Deferred** by the owner. Preserved as a proposed EXP-003 measurement pending task-list consensus. |
| U4 | Oracle-certifiable fraction, CPC share and band widths on real designs | **Deferred** by the owner. Preserved and preregistered in EXP-003. |
| U5 | Licenses and provenance | Toolchain licenses are verified from each repository (`runs/CLD-P05-REVISION-0001/evidence/REQ-0003-licenses.txt`). Libraries and designs are still to be acquired only from GitHub or arXiv, with licenses verified in the repository itself. Any item with unclear license or provenance is excluded (EXP-001). |
| U6 | Compute fit, including P&R | P&R is **not authorized** in this round. Its cost is to be estimated and allocated in the jointly accepted task list. |
| U7 | Global side effects of cone-restricted search | Static findings are recorded as threats with required falsification tests (CLM-024; record § 7). The full experiment is deferred until consensus. |
| U8 | TAU 2018 and 2019 topics | **Topic level resolved** from a GitHub record (SRC-059). Rules, formats and winner reports are unresolved. No global "no relevant contest" claim is made (CLM-014). |
| U9 | Reporting margin M and the 20% threshold | Owner decision: M = 0 ps is primary; 5% of the clock period is only a labelled sensitivity analysis; the 20% threshold is **provisional**. Challenger or practitioner evidence may revise these before consensus. |
| U10 | Content of NIO (ICSICT 2014), a forward citation of SRC-012 | Unresolved: the abstract is withheld by the publisher, and the work is not on arXiv or GitHub. |
| U11 | (Round 1b.) Content of SRC-066, SRC-067 and SRC-068, and the unreferenced "[Heloue, DATE07]" on SRC-014 slide 7 | **Unresolved.** These are outside the GitHub and arXiv routes, with no copy on either (Q45, Q46). The challenger could not retrieve SRC-067's text either. Verifier full-text read required (K1). |
| U12 | (Round 1b.) How many endpoints the exception rule excludes in the evaluated SDCs | Unmeasured. Counted in the EXP-003 census, from the SDC files and B0's graph. |
| U13 | (Round 1b.) Whether P pays off inside an edit loop against incremental exact timing | Unmeasured. Tested as CH8 in EXP-007, with no threshold. |

**Kill and stop criteria**:

| ID | Trigger | Consequence |
|---|---|---|
| K1 | A nearest-work full-text check (SRC-012, SRC-066, SRC-067, SRC-068 or another found source) shows that per-scenario sound certification with exact refinement already exists for discrete characterized scenarios | Abandon this ID or propose joint abandonment; a successor needs a new ID. *Status: open; widened in round 1b.* |
| K2 | P2-P5 cannot be made sound without empirical safety margins | The guarantee claim fails for the affected paths. *Status: **activated in round 1** for the DMP waveform path. The claim is narrowed to R1 (CLM-023); no empirical margin is used anywhere.* |
| K3 | EXP-003, using the R1 rules: the oracle screen restricted to CPC cones, plus measured pass costs, predicts below 20% (provisional, U9) reduction on at least 2 of 3 designs for every available scenario set | Stop before implementation. *This now includes the CPC-share census; a small share stops the work early (CH6).* |
| K4 | Prerequisites (multi-corner libraries, designs, compute allocation) unobtainable within the pilot caps | Park with specific missing items |
| K5 | Any decision mismatch against B0 in EXP-006 not traced to a fixable implementation bug and re-verified | Stop |
| K6 | Combination or demand drift score of 2 or more on any revision | Stop under the charter's governance rule |
| K7 | (new) The verifier refutes the R1 code argument, or an EXP-002b test finds a CPC-classified arc whose results differ from the exact `DmpCap` values. From round 1b also: a P8 or P9 test, or the G7 audit, finds a certified triple whose B0 slack is below its logged bound and the cause cannot be fixed by a corrected rule without an empirical margin | Withdraw the remaining guarantee claim. Propose parking or joint abandonment; do not continue as a "sound" method. |

## Unresolved questions for the coordinator and human

1. **SRC-012 admissibility.** Should the full-text reading in `addenda/EDA-0002/ADD-0001` (Internet Archive capture, made before decision U1 on the human's instruction) be admitted, or must SRC-012 stay unresolved until a verifier reads it?
2. **Prerequisites and P&R.** Authorize, in the jointly accepted task list, the acquisition of multi-corner libraries and designs from GitHub only. Set the explicitly estimated P&R allocation (owner items U5 and U6).
3. **Practitioner input** on M = 0 ps versus M > 0 and on the provisional 20% threshold (owner item U9).
4. **Bison build.** Should a verifier-side bison build of OpenSTA be required to remove the parser-generator deviation (record § 2)?
5. **Utility given K2.** Is the narrowed R1 certificate worth an EXP-003 CPC-share census before any further investment, or should the human prefer parking now? The proposer recommends the census: it is cheap, decisive, and preregistered as K3.
6. **New nearest-work leads (round 1b).** SRC-066, SRC-067 and SRC-068 are hosted outside GitHub and arXiv. Should the proposer be allowed to open the author-hosted copies, or must they wait for the verifier (U11, K1)?
7. **Edit-loop comparison (round 1b).** Should the CH8 comparison with incremental exact timing (B6) stay in the pilot, inside the EXP-007 cap, or be deferred? The proposer recommends keeping it: it decides where the method is useful at all.
