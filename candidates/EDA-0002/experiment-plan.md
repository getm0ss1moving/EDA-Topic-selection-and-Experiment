# Experiment Plan

**Status: draft preregistration, not frozen.**

- Experiments are not authorized: `experiment_authorization` is false (`config/launch-release.json` line 71), and none may start before promotion and task-list consensus (`docs/EXPERIMENTS.md` lines 25-27).
- Thresholds marked *provisional* are frozen only after the pilot variance task (EXP-005) and before any candidate evaluation (`config/research-brief.json` line 78).
- Every amendment is recorded in § Stopping rules and amendment procedure before the affected data are collected.

## Preregistered hypotheses and counter-hypotheses

- **H1 (primary; CLM-010).** For each of at least 3 independent designs and each evaluated scenario set S with K ≥ 3, the screened analysis P reproduces the decision set D_M(S) exactly (defined in § Primary metric), with relative end-to-end wall-time reduction R ≥ 20% against B0 under equal resources.
- **H2 (mechanism; CLM-011).** The reduction is mediated by certified triples in non-dominant scenarios. Predicted signatures:
  - (a) the certification rate is higher in scenarios that are not the per-endpoint worst;
  - (b) A1 (no exact clock pass) lowers the certification rate and R;
  - (c) A3 (single scenario) gives R < 20%;
  - (d) A2 (scenario-level) gives a lower R than endpoint-level.
- **H3 (safety contrast; CLM-012).** At least one estimated or heuristic screening baseline (B2-B4) at comparable or lower cost misses at least one violating triple on at least one evaluated configuration, while P misses none.
- **Counter-hypotheses** (CH1-CH5, `proposal.md`):
  - CH1: bound bands too wide;
  - CH2: fixed or shared phases dominate runtime;
  - CH3: simple dominance is already safe on open corner sets;
  - CH4: properties P3-P5 fail;
  - CH5: restricted refinement is inexact.
- **Distinction.** EXP-003 is a *mechanism pilot*: oracle analysis that does not require the candidate implementation. EXP-006 and EXP-007 are the *confirmatory evaluation*.

## Primary metric, units, direction, and meaningful effect

**Decision set D_M(S).** For every scenario s ∈ S, every timing endpoint e and every check c ∈ {setup, hold, recovery, removal} present:

- the violation flag, slack < 0;
- the exact slack whenever slack < M;
- WNS(s) and TNS(s) per check type, when negative.

**Primary metric:**

    R = (T_B0 - T_P) / T_B0 x 100

R is a relative percentage, and higher is better. T is end-to-end wall time from process start to the decision-set file being written. It includes reading the netlist, libraries, SPEF and SDC; all passes (clock, bound, refinement); and writing reports. Percentage points are never used for R.

**Meaningful effect (provisional, `config/research-brief.json` line 77).** R ≥ 20% per design, with decision equivalence holding.

**Reporting margins:** M = 0 ps (primary, matching the brief's "same timing decisions") and M = 5% of the clock period (secondary sensitivity). Both are preregistered here and subject to practitioner input (U9).

**Guardrails:**

| Guardrail | Rule |
|---|---|
| G1 | Missed violating triples (false negatives) = 0 on every evaluated case |
| G2 | False violations (false positives) = 0 |
| G3 | Slack equality for every reported triple: tie tolerance 1e-6 ns for "identical" results; outer bound 0.005 ns per the brief |
| G4 | WNS and TNS identical within 1e-6 ns |
| G5 | Peak RSS ≤ 1.25 × B0 (provisional) |
| G6 | No crash or timeout |

Any G1-G4 failure counts as a failure of H1 for that case, whatever the runtime.

**Secondary metrics:**

- certification rate per scenario;
- oracle-certifiable fraction, i.e. the fraction of triples with B0 slack ≥ M;
- bound band width = (exact slack − certified lower bound), as a distribution;
- CPU time and peak RSS;
- phase-level time: parse, graph build, clock pass, bound pass, refinement, report.

## Correctness and feasibility constraints

- The same netlist, SDC, libraries and SPEF are used for every compared configuration.
- B0 is the unmodified pinned OpenSTA. The candidate is a fork of the same commit with the new code behind a command flag. With the flag off, the fork must reproduce B0's reports bit for bit; this is a sanity test in EXP-004.
- The scope invariants in `proposal.md` (no latches, no SI, `dmp_ceff_elmore`) are checked per design. Any design that violates them is excluded **before** evaluation, and the exclusion is recorded.
- Every certificate is logged. Every certified triple is checked against B0 in every evaluated case, which makes the empirical soundness check exhaustive.

## Pinned baseline versions and reproduction

| Item | Value |
|---|---|
| Reference engine | OpenSTA `e01d3f163f483f233db00410b6515a767a6ca03b`, as built in OpenROAD `b16bda7e82721d10566ff7e2b68f1ff0be9f9e38` inside `efabless/openlane@sha256:840fe28388494220dae9e2be6cf3c7cb2dadfa0eabae4144f0873b9ee949597f` (`config/research-brief.json` lines 29-31) |
| Delay calculator | `dmp_ceff_elmore` (default, SRC-003) |
| Analysis | `define_corners` with all scenarios in one run (SRC-005) |
| Flow scripts for prerequisite generation | ORFS, pinned to a commit chosen in EXP-001 (master was `e5cc6e79…` at search time; SRC-052) |

**Reproduction.** Every script, input hash, container digest and command line is recorded in `runs/<run-id>/manifest.json` (`docs/FORMATS.md` line 50).

## Datasets, rights, family splits, and contamination audit

**Required designs** (open prerequisite; EXP-001). Three independent families, each implemented on each platform used:

| Design | License (as read; to re-verify at the pinned commit) | Source |
|---|---|---|
| `aes` | BSD-3-style (ASICs World Services; covers netlist and silicon forms) | SRC-034 |
| `jpeg` | BSD-3-style (ASICs World Services) | SRC-034 |
| `ibex` (`ibex_sv` sources) | Apache-2.0 | SRC-034 |

Optional held-out families, to be added only if licenses verify and budget allows: `riscv32i` and `microwatt` (sky130hd), and `swerv_wrapper` or `ethmac` (asap7). Their licenses are **unknown** and unchecked.

**Required libraries and corners** (open prerequisite):

| Library | Corners | License | Status |
|---|---|---|---|
| ASAP7 NLDM, ORFS copy (SRC-028) | FF, SS, TT | Upstream BSD-3-Clause (SRC-032) | Provenance of the ORFS copy unverified; corner V/T to be read from library headers |
| SKY130 `sky130_fd_sc_hd` | 16 PVT corners as `.lib.json` (SRC-030) | skywater-pdk umbrella repo Apache-2.0 (SRC-031); **library repository license unverified** | Conversion to Liberty required; method and tool to be identified in EXP-001 |
| Nangate45 (packet) | typical only | Research library (packet lock) | Not usable as a multi-scenario set |
| RC corners | none | n/a | ORFS ships one OpenRCX rules file per platform (SRC-036); rules are corner-specific (SRC-035). **No RC-corner claims will be made.** Synthetic RC scaling may appear only as a labeled sensitivity study, never as primary evidence. |

**Splits.** P has no learned component, so no training split exists for it. Baselines B2-B4 are calibrated or trained *leave-one-design-out*: calibrate on two families, test on the third. Placement-seed variants of one design are never counted as independent designs.

**Contamination audit:** no test design or scenario may be used to tune P's bounding rules or the cutoffs, regressions or thresholds of B2-B4.

**Rights:** no proprietary PDK, design or report. Upstream license notices are kept with downloaded files, and assets are not vendored into the repository (`docs/PHYSICAL-PILOT.md` line 17).

## Hardware, PDK, corners, tool and API budgets

- **Hardware:** local arm64 host; one 2-CPU, 4 GiB container job at a time (`config/research-brief.json` lines 10-26); the same thread setting for all configurations.
- **CPU budget:** 8 CPU-hours total, allocated per task in `tasklist.md`. Allocations are caps, not estimates of need. Exceeding a cap triggers a stop and an allocation request.
- **GPU and API:** none.
- **Scenario sets:**
  - SET-A: ASAP7 {FF, SS, TT} × 1 RC corner (K = 3);
  - SET-B: SKY130 hd up to 16 PVT corners × 1 RC corner (K ≤ 16), subject to EXP-001.
  - [INF] SET-A alone may be too small to show H1 or H3; SET-B is the main test if it is obtainable.

## Strong, naive-composition, and equal-budget baselines

| ID | Description | Role |
|---|---|---|
| B0 | Pinned OpenSTA, all scenarios in one run (`define_corners`), same threads | Strongest exact baseline and reference oracle |
| B1 | Pinned OpenSTA, one run per scenario, sequential | Context only (weaker) |
| B2 | Anchor-slack cutoff screen (IBM-style, SRC-016): exact analysis at the anchor scenario(s); skip (e, s) if anchor slack ≥ c; c calibrated leave-one-design-out for zero false negatives on the calibration designs | Closest-prior mechanism, estimated |
| B3 | Ratio-estimate screen (simplified SRC-017): estimate slack at s by scaling anchor component delays with per-cell library delay ratios at the anchor operating point; refine exactly if the estimate is below M + guard | Closest industrial-style estimated screen |
| B4 | Regression screen (SRC-015-style): linear regression from observed to unobserved scenarios, trained leave-one-design-out; exact refinement for predicted slack below M + guard | Learned screen with exact fallback (structure like SRC-024) |
| B5 | Naive dominance: "SS for setup, FF for hold" (or the platform's slowest and fastest) | Common heuristic |
| O | Oracle screen: refine exactly the triples whose B0 slack is below M; cost of the clock and refinement passes only | Upper bound on attainable R for any screen |

**Equal-budget rule.** B2-B4 guards and cutoffs are chosen so that each baseline's runtime is ≤ T_P on the calibration designs. False negatives are then compared at equal or lower cost (H3).

## Ablations and mechanism tests

| ID | Change | Prediction |
|---|---|---|
| A1 | Remove the exact clock pass; bound the clock network too | Certification rate and R drop (H2b) |
| A2 | Scenario-level certification only: skip s only if every endpoint at s certifies; otherwise run s in full | Lower R (H2d) |
| A3 | Apply P to a single scenario | R < 20% (H2c, slack-wall prediction) |
| A4 | M ∈ {0, 5% of period} | Lower R at larger M |
| A5 | Monotone-corner shortcut (valid only on verified-monotone tables) vs full extreme-point evaluation | Measures the cost of soundness |

**Mechanism test.** Plot the per-scenario certification rate against the scenario's rank in per-endpoint worst-slack order (H2a).

## Pilot variance, sample size, seeds, and statistics

**Determinism.** STA is deterministic, so "seeds" do not apply to the timing runs. Run-to-run variance comes from the host and container. Placement seeds create *design variants*, and those are used only in EXP-007 robustness checks.

**Pilot (EXP-005):** 10 interleaved repetitions of B0 and P per design on one scenario set. Estimate the coefficient of variation of wall time, then choose N repetitions so the 95% bootstrap CI half-width of R is ≤ 5 percentage points of R, within budget. If N does not fit the budget, report the wider CIs or stop (budget rule).

**Analysis:**

- per design, the median-of-N wall time for each configuration;
- paired run-order-matched ratios with a bootstrap 95% CI (10,000 resamples);
- across designs, a geometric-mean ratio, always with per-design results shown;
- no pooling across scenario sets or platforms;
- multiple comparisons (configurations × ablations) disclosed, with confirmatory claims limited to H1 on the preregistered designs.

**Success criterion for H1 (provisional):** for every design, decision equivalence (G1-G4) holds, the median R ≥ 20%, and the lower 95% CI bound of R is > 0.

## Failure accounting and Pareto tradeoffs

**Failure accounting.** Every run is logged, including crashes, timeouts, refinement fallbacks, bound-validity violations and decision mismatches. Failures are never dropped from denominators. Any G1-G4 failure triggers stop rule S2.

**Pareto reporting.** R against peak RSS; R against M; certification rate against bound-evaluation cost (A5); and per-scenario costs.

## Stopping rules and amendment procedure

**Stopping rules**, in addition to K1-K6 in `proposal.md`:

| ID | Trigger | Action |
|---|---|---|
| S1 | A task exceeds its CPU-hour cap | Stop that task and request allocation |
| S2 | Any decision mismatch or bound-validity violation | Stop evaluation, diagnose, fix with a regression test, and rerun all affected cases from scratch. A violation that cannot be repaired without empirical margin triggers K2. |
| S3 | EXP-003 oracle analysis predicts R < 20% on at least 2 of 3 designs for every available scenario set | Stop (K3) |
| S4 | Prerequisites not authorized or not obtainable | Park (K4) |

**Amendments.** Any change to H1-H3, the metrics, thresholds, baselines, designs, scenario sets or analysis is dated and recorded here before the affected data are collected. Any `tasklist.md` change invalidates experiment consensus (`docs/FORMATS.md` line 38).

## Reproduction commands and artifacts

**Planned artifacts** (none exist yet; owners per `tasklist.md`):

- `mcmm_screen/` OpenSTA patch, applied on top of `e01d3f16`, with flag `-screen` on a new command `report_mcmm_decisions`. The command name is provisional.
- `scripts/run_b0.tcl`, `scripts/run_p.tcl`, `scripts/run_baselines.tcl`.
- `scripts/compare_decisions.py`: exact comparison of D_M(S) files, with G1-G4 checks.
- `scripts/bound_audit.py`: arc-level bound-validity audit for EXP-002.
- `scripts/oracle_screen.py`: EXP-003 oracle analysis from B0 reports.
- Per-run manifests under `runs/`, including container digest, input hashes, command lines, host load notes, and raw timing logs.
