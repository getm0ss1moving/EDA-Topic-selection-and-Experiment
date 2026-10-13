# Experiment task list

**Status:** proposer draft, round 0. Not agreed and not signed.

- The challenger must add the decisive falsification tests, fairness controls and missing dependencies (§ Challenger additions) before either role signs (`docs/CHARTER.md` line 28).
- No task may start before promotion, task-list consensus and a human resource allocation. `experiment_authorization` is currently false.
- **CPU caps** below are allocations from the pilot's 8 CPU-hour total (`config/research-brief.json` line 11). They are not estimates of need. Exceeding a cap triggers stop rule S1.
- **Owners:** P = proposer, C = challenger, V = verifier, H = human or coordinator.

- [ ] **EXP-001: Resolve tool, data and license access, and pin the environment.**
  - *Owner:* P executes; H authorizes the downloads and the compute allocation.
  - *Depends on:* promotion; human allocation.
  - *Budget:* ≤ 2.5 CPU-h (P&R for prerequisite generation), wall ≤ 2 days.
  - *Procedure:*
    - (0) Re-attempt a full-text read of SRC-012. If it is still inaccessible, ask V or C for a copy route; this is step one of K1.
    - (1) Pin an ORFS commit. Record the license file of every design (`aes`, `jpeg`, `ibex_sv`) and platform at that commit.
    - (2) ASAP7: verify the provenance of the ORFS NLDM copies against the upstream BSD-3-Clause repositories, and read each corner's V/T from the library headers.
    - (3) SKY130 hd: verify the library repository's license, and identify and pin a reproducible `.lib.json`-to-Liberty generation path (for example the PDK build scripts or open_pdks). Hash every generated `.lib`.
    - (4) Estimate per-design P&R CPU time from public ORFS metrics if available. Otherwise run one design first and extrapolate. Stop if the projection exceeds the cap.
    - (5) Implement `aes`, `jpeg`, `ibex` on each obtained platform with default ORFS settings at the pinned commit, and record the implementation corner.
    - (6) Extract SPEF at the single available RC corner.
  - *Artifact:* `prereq-manifest.json` with URLs, commits, SHA-256 hashes, licenses, CPU-time log, and the netlist, SPEF and SDC hashes per design.
  - *Pass/fail:* pass if at least 3 designs on at least one scenario set with K ≥ 3 are available with verified licenses inside the cap. Fail means park (K4).

- [ ] **EXP-002: Derive and audit soundness of the bounding rules against pinned `dmp_ceff_elmore`.**
  - *Owner:* P derives; V checks the derivation; C may submit counterexamples.
  - *Depends on:* EXP-001 (libraries and SPEF for the audit).
  - *Budget:* ≤ 0.5 CPU-h.
  - *Procedure:*
    - (1) Write the bound rules and the proof sketch for P1-P6, citing exact code lines of `e01d3f16`: `DmpCeff.cc`, `TableModel.cc` (including 3-D tables), `LumpedCapDelayCalc.cc`, `ReduceParasitics.cc`.
    - (2) Instrument the fork, output only, to dump for every arc and scenario the reference gate delay, wire delay, driver slew and load slew next to the computed bounds.
    - (3) Run on all EXP-001 designs and scenarios.
    - (4) Count violations of each property.
  - *Artifact:* `soundness.md` (derivations with locators), and `bound_audit.csv` listing per property the count of evaluated arcs and of violations.
  - *Pass/fail:* pass only if there are zero violations for every property, and P3-P5 have either a proof or a documented code-level argument accepted by V. Any unrepairable violation triggers K2.

- [ ] **EXP-003: Characterize headroom (mechanism pilot; no candidate implementation needed).**
  - *Owner:* P.
  - *Depends on:* EXP-001; EXP-002 rules, for band widths.
  - *Budget:* ≤ 1.0 CPU-h.
  - *Procedure:*
    - (1) Run B0 on each design and scenario set, recording phase-level time (parse, graph build, delay calculation, search, report) and per-scenario cost.
    - (2) From B0 reports compute the oracle-certifiable fraction per scenario and check type, the per-endpoint worst-scenario distribution, and the slack distributions (slack wall).
    - (3) Using the EXP-002 bound rules in a standalone script on B0 data, compute certified lower bounds and band widths, then the predicted certification rate.
    - (4) Plug the measured phase costs into the cost model in `proposal.md`.
    - (5) Search for wire-dominated capture paths (the CLM-017 pattern) and count them.
  - *Artifact:* `headroom.md` and `headroom.csv`.
  - *Pass/fail:* fail (K3) if the predicted R is below 20% on at least 2 of 3 designs for every scenario set. Otherwise pass, and record the predicted R as a forecast input.

- [ ] **EXP-004: Implement the smallest mechanism and the naive-composition baselines.**
  - *Owner:* P; C reviews the baseline fairness.
  - *Depends on:* EXP-002 pass; EXP-003 pass.
  - *Budget:* ≤ 0.5 CPU-h (builds and unit tests).
  - *Procedure:* in a fork of OpenSTA `e01d3f16`:
    - (1) Add a clock-only search pass, a bound pass and cone-restricted refinement behind a flag.
    - (2) Check that with the flag off, outputs equal B0 bit for bit.
    - (3) Unit-test on hand-built netlists, including a CLM-017-style capture-wire-dominated case and a hold case.
    - (4) Implement B2, B3, B4, B5 and O, plus the A1-A5 switches.
    - (5) Write `compare_decisions.py` (G1-G4).
  - *Artifact:* patch with commit hash; test log; baseline scripts.
  - *Pass/fail:* pass if the flag-off output is identical, every unit test passes, and the CLM-017 case is reported as violating by P and as missed by a B2 configuration with cutoff 25 ps.

- [ ] **EXP-005: Estimate variance and preregister sample size and thresholds.**
  - *Owner:* P; C co-signs the frozen thresholds.
  - *Depends on:* EXP-004.
  - *Budget:* ≤ 0.5 CPU-h.
  - *Procedure:*
    - (1) 10 interleaved repetitions of B0 and P on one design and scenario set.
    - (2) Compute the coefficient of variation and choose N per `experiment-plan.md` § Pilot variance.
    - (3) Freeze N, M, G5 and the success criterion in `experiment-plan.md` as a dated amendment, with practitioner input if available (U9).
  - *Artifact:* `pilot-variance.csv`; the amendment entry.
  - *Pass/fail:* pass if N fits the remaining budget. Otherwise the amendment records the wider CIs, or work stops.

- [ ] **EXP-006: Run the equal-budget paired evaluation and the required ablations.**
  - *Owner:* P runs; C may specify additional falsification cases before the run.
  - *Depends on:* EXP-005.
  - *Budget:* ≤ 2.0 CPU-h.
  - *Procedure:*
    - (1) For each design and scenario set, N interleaved runs of B0, P, B2-B5, O and A1-A5, under identical container limits.
    - (2) Compare decisions exactly against B0.
    - (3) Log every certificate and every fallback.
  - *Artifact:* raw logs, `results.csv`, decision diff reports.
  - *Pass/fail:* H1 succeeds per `experiment-plan.md`. Any G1-G4 failure triggers S2. H2 and H3 are evaluated as preregistered, and negative results are reported.

- [ ] **EXP-007: Evaluate held-out families, other scenario sets, robustness and total cost.**
  - *Owner:* P.
  - *Depends on:* EXP-006.
  - *Budget:* ≤ 0.75 CPU-h.
  - *Procedure:* run P and B0 on scenario set SET-B if it was not primary (otherwise SET-A); on held-out designs if licensed and affordable; and on 2 placement-seed variants per design (robustness only, not counted as independent). Report total cost, including EXP-001 generation, separately from per-analysis cost.
  - *Artifact:* `robustness.csv`.
  - *Pass/fail:* decision equivalence holds everywhere. R is reported with CIs, with no new threshold.

- [ ] **EXP-008: Analyze uncertainty, failed runs, negative results and forecast calibration.**
  - *Owner:* P; V checks.
  - *Depends on:* EXP-006, EXP-007.
  - *Budget:* ≈ 0 CPU-h (analysis only).
  - *Procedure:* per-design results and CIs; Pareto plots; the failure table; comparison of measured R with the `forecast.json` ranges set after EXP-003; documentation of every deviation.
  - *Artifact:* `analysis.md`.
  - *Pass/fail:* complete accounting, with no omitted run.

- [ ] **EXP-009: Independent reproduction and proceed/revise/stop decision.**
  - *Owner:* V, or an independent session designated by H.
  - *Depends on:* EXP-008.
  - *Budget:* ≤ 0.25 CPU-h.
  - *Procedure:* re-run B0 and P on one design and scenario set from the manifests alone, and compare decision files and median R.
  - *Artifact:* `reproduction.md`.
  - *Pass/fail:* identical decision files, and a reproduced R within the original 95% CI. The decision to proceed, revise or stop is recorded by the human, with reasons.

**Budget total:** 2.5 + 0.5 + 1.0 + 0.5 + 0.5 + 2.0 + 0.75 + 0 + 0.25 = **8.0 CPU-hours**. If EXP-001 alone exceeds 2.5 CPU-h, every later allocation must be renegotiated before continuing.

## Challenger additions (pending)

Reserved for the challenger's required falsification tests, fairness controls and missing dependencies. The proposer will not sign until this section is complete and both roles agree on the exact text.
