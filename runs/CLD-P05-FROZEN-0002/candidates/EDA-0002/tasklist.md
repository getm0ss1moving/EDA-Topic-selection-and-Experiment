# Experiment task list

**Status:** proposer draft, **round 1, amendment 1b** (revised under owner decision CLD-LAB-0001, then amended before the freeze on the owner's instruction to incorporate the challenger's independent first pass). Not agreed and not signed. Any change to this file resets experiment consensus.

- The challenger must add the decisive falsification tests, fairness controls and missing dependencies (§ Challenger additions) before either role signs (`docs/CHARTER.md` line 28).
- No experiment task may start before promotion, task-list consensus and a human resource allocation. `experiment_authorization` is false.
- Owner decision CLD-LAB-0001 permitted, in this round, only tooling, GitHub and arXiv data, and the P3-P5 property checks. Their results are recorded under EXP-002.
- **CPU caps** below are proposed allocations from the pilot's 8 CPU-hour total (`config/research-brief.json` line 11). They are not estimates of need. Exceeding a cap triggers stop rule S1.
- **Runner ledger.** The owner's file-mediated runner has a 300 core-hour infrastructure ceiling (at most 8 cores and 12 hours per job), which is not a scientific allocation. Use is reported in `runs/CLD-P05-REVISION-0001/evidence/runner-ledger.json`. The proposer asks the owner to confirm that runner tooling and property-check use is not charged to the 8 CPU-hour pilot budget.
- **Owners:** P = proposer, C = challenger, V = verifier, H = human or coordinator.

- [ ] **EXP-001: Resolve tool, data and license access, and pin the environment.**
  - *Owner:* P executes; H authorizes the downloads and the compute allocation.
  - *Depends on:* promotion; human allocation.
  - *Status (round 1):* the tooling part is done. Pinned OpenSTA `e01d3f16` and its toolchain are built on the runner from GitHub sources, with licenses recorded (`runs/CLD-P05-REVISION-0001/p3-p5-record.md` § 2). Libraries, designs and P&R are not started.
  - *Budget:* ≤ 0.25 CPU-h for acquisition and conversion. **P&R:** a cap of ≤ 2.5 CPU-h is *proposed*. It is not allocated: owner decision U6 requires the P&R cost to be estimated (step 4) and allocated explicitly in the jointly accepted list. Wall ≤ 2 days.
  - *Procedure:*
    - (0) SRC-012. Re-attempted in round 1 through arXiv and GitHub only (U1): not available. It stays unresolved unless the owner admits the ADD-0001 reading or a verifier reads the full text. This feeds K1.
    - (1) Acquire tools and data only from GitHub or arXiv. Pin revisions and hashes, and verify every license from the repository itself. Exclude any item with unclear license or provenance (U5).
    - (2) Pin an ORFS commit. Record the license file of every design (`aes`, `jpeg`, `ibex_sv`) and platform at that commit.
    - (3) ASAP7: verify the provenance of the ORFS NLDM copies against the upstream BSD-3-Clause repositories, and read each corner's V/T from the library headers.
    - (4) SKY130 hd: verify the library repository's license, and identify and pin a reproducible `.lib.json`-to-Liberty generation path available from GitHub. Hash every generated `.lib`.
    - (5) Estimate per-design P&R CPU time from public ORFS metrics if available. Submit the estimate for joint allocation before any P&R run.
    - (6) After allocation only: implement `aes`, `jpeg`, `ibex` on each obtained platform with default ORFS settings at the pinned commit, and extract SPEF at the single available RC corner.
  - *Artifact:* `prereq-manifest.json` with URLs, commits, SHA-256 hashes, licenses, CPU-time log, and the netlist, SPEF and SDC hashes per design.
  - *Pass/fail:* pass if at least 3 designs on at least one scenario set with K ≥ 3 are available with verified licenses inside the allocation. Fail means park (K4).

- [x] **EXP-002: Audit soundness of the bounding rules against pinned `dmp_ceff_elmore`** (completed in round 1 on synthetic fixtures).
  - *Owner:* P derived and ran; V checks the derivation and the record; C may submit counterexamples.
  - *Done:* runner jobs REQ-0006 to REQ-0008 (0.01 core-h), using synthetic libraries and RC trees only. The record, with source revision, build commands, fixtures, check commands, invariants, counterexamples, code arguments and labels, is `runs/CLD-P05-REVISION-0001/p3-p5-record.md`.
  - *Result:*
    - P3, P4 and P5 as stated are **falsified** (CLM-018 to CLM-020), so **K2 is activated**.
    - The narrowed capacitive-path rules and the lower bounds are code-argument-only + finite-tests-pass (CLM-021).
    - The bracket bounds and assumption ADT: CLM-022.
    - P2 for the `DmpZeroC2` path is falsified as stated (CLM-025).
  - *Pass/fail as preregistered:* **fail** for P3-P5, which triggered K2. The certificate is narrowed to R1.

- [ ] **EXP-002b: Finite tests of the R1 classification (P7) and of the refinement side effects.**
  - *Owner:* P; V checks; C may add cases.
  - *Depends on:* task-list consensus (property-check category on the runner).
  - *Budget:* ≤ 0.25 CPU-h.
  - *Procedure:* synthetic fixtures only. Each step builds on the round-1 harness.
    - (1) For random and adversarial pi models and slew intervals, compare the R1 CPC classification with the variant actually selected at slews sampled densely in the interval, including both table extrapolation regions. Probe float32 rounding at the 1e-3·Rd and 1e-2 Ω thresholds.
    - (2) On every CPC-classified arc, confirm that gate delay, driver slew, wire delay and load slew equal the R1 values.
    - (3) Multi-driver net with a driver outside the fan-in cone.
    - (4) Net with cone and off-cone loads.
    - (5) Two-library net (`thresholdAdjust`).
    - (6) *(Round 1b, P9.)* Rounding: on random and adversarial tables, compare the float bound with its allowance against the pinned evaluator at densely sampled interior slews, and record the largest excess in ulps. Then build near-margin fixtures whose exact slack lies within a few ulps of M and of 0.
    - (7) *(Round 1b, P8.)* Exceptions, on small netlists: multicycle paths with `-setup` only, `-hold` only and both; maximum and minimum delay; false paths; and clock-to-clock exceptions. Confirm that the P8 rule leaves every exception-matched endpoint uncertified. Confirm against B0 that bounds ignoring false paths and disabled arcs stay conservative.
    - (8) *(Round 1b.)* Ranking reversals: two- and three-scenario fixtures in which the worst scenario differs by endpoint, including the CLM-017 capture-wire pattern for setup and a hold analogue.
    - (9) *(Round 1b.)* Clock effects: CRPR with shared clock segments, a generated clock, clock uncertainty and an output-delay endpoint.
  - *Artifact:* `p7-record.md` (covering P7 to P9) and per-case CSV.
  - *Pass/fail:* any CPC misclassification, value mismatch, bound below the pinned value in step (6), certified exception-matched endpoint in step (7), or certified triple whose B0 slack is below its bound in steps (6) to (9) triggers K7. Steps (3) to (5), (7) and (9) define required properties of the EXP-004 refinement.

- [ ] **EXP-003: Characterize headroom under R1 (mechanism pilot; no candidate implementation needed).**
  - *Owner:* P.
  - *Depends on:* EXP-001; EXP-002b pass.
  - *Budget:* ≤ 1.0 CPU-h.
  - *Procedure:*
    - (1) **CPC census, first.** Per design and scenario, record the share of data nets and of (endpoint, scenario, check) fan-in cones that are CPC under R1, computed from B0's reduced parasitics and the R1 tests. *(Round 1b.)* Also record the share of endpoints excluded by the exception rule P8, from the hashed SDC. Stop here if the predicted R bound from the CPC share and the exception exclusions alone is below the threshold (K3).
    - (2) Run B0 on each design and scenario set, recording phase-level time (parse, graph build, delay calculation, search, report) and per-scenario cost.
    - (3) From B0 reports, compute the oracle-certifiable fraction restricted to CPC cones, per scenario and check type; the per-endpoint worst-scenario distribution; and the slack distributions (slack wall).
    - (4) Using the R1 rules in a standalone script on B0 data, compute certified lower bounds and band widths, then the predicted certification rate.
    - (5) Plug the measured phase costs into the cost model and the accounting identity in `proposal.md`.
    - (6) Search for wire-dominated capture paths (the CLM-017 pattern) and count them.
  - *Artifact:* `headroom.md` and `headroom.csv`.
  - *Pass/fail:* fail (K3) if the predicted R is below 20% (provisional, U9) on at least 2 of 3 designs for every scenario set. Otherwise pass, and record the predicted R as a forecast input.

- [ ] **EXP-004: Implement the smallest mechanism and the naive-composition baselines.**
  - *Owner:* P; C reviews the baseline fairness.
  - *Depends on:* EXP-002b pass; EXP-003 pass.
  - *Budget:* ≤ 0.5 CPU-h (builds and unit tests).
  - *Procedure:* in a fork of OpenSTA `e01d3f16`:
    - (1) Add a clock-only search pass, the R1 bound pass and cone-restricted refinement behind a flag. Refinement cones are closed over whole nets and over all drivers of multi-driver nets. *(Round 1b.)* Include the exception rule P8, the rounding allowance P9 and the certificate log (bound, allowance, scenario).
    - (2) Check that with the flag off, outputs equal B0 bit for bit.
    - (3) Unit-test on hand-built netlists, including: a CLM-017-style capture-wire-dominated case; a hold case; the EXP-002b side-effect cases; *(round 1b)* a multicycle hold-shift case; and a near-margin case.
    - (4) Implement B2, B3, B4, B5 and O, plus the A1-A5 switches. *(Round 1b.)* Script B6 (incremental update after each edit batch) and the edit-sequence generator, with a fixed seed.
    - (5) Write `compare_decisions.py` (G1-G4).
  - *Artifact:* patch with commit hash; test log; baseline scripts.
  - *Pass/fail:* pass if:
    - the flag-off output is identical;
    - every unit test passes;
    - the CLM-017 case is reported as violating by P and as missed by a B2 configuration with cutoff 25 ps.

- [ ] **EXP-005: Estimate variance and preregister sample size and thresholds.**
  - *Owner:* P; C co-signs the frozen thresholds.
  - *Depends on:* EXP-004.
  - *Budget:* ≤ 0.5 CPU-h.
  - *Procedure:*
    - (1) 10 interleaved repetitions of B0 and P on one design and scenario set.
    - (2) Compute the coefficient of variation and choose N per `experiment-plan.md` § Pilot variance.
    - (3) Freeze N, M (primary 0 ps; 5% of the period as sensitivity), G5 and the success criterion in `experiment-plan.md` as a dated amendment, with practitioner input if available (U9).
  - *Artifact:* `pilot-variance.csv`; the amendment entry.
  - *Pass/fail:* pass if N fits the remaining budget. Otherwise the amendment records the wider CIs, or work stops.

- [ ] **EXP-006: Run the equal-budget paired evaluation and the required ablations.**
  - *Owner:* P runs; C may specify additional falsification cases before the run.
  - *Depends on:* EXP-005.
  - *Budget:* ≤ 2.0 CPU-h.
  - *Procedure:*
    - (1) For each design and scenario set, N interleaved runs of B0, P, B2-B5, O and A1-A5, under identical container limits.
    - (2) Compare decisions exactly against B0.
    - (3) Log every certificate, every CPC classification and every fallback.
    - (4) *(Round 1b.)* Audit every certificate against B0 (G7), and record each term of the accounting identity per run.
  - *Artifact:* raw logs, `results.csv`, decision diff reports, `certificate-audit.csv`.
  - *Pass/fail:* H1 succeeds per `experiment-plan.md`. Any G1-G4 or G7 failure triggers S2, and any G7 failure is assessed under K7. H2 and H3 are evaluated as preregistered, and negative results are reported.

- [ ] **EXP-007: Evaluate held-out families, other scenario sets, robustness and total cost.**
  - *Owner:* P.
  - *Depends on:* EXP-006.
  - *Budget:* ≤ 0.75 CPU-h.
  - *Procedure,* in this priority order within the cap:
    - (1) Run P and B0 on scenario set SET-B if it was not primary (otherwise SET-A).
    - (2) *(Round 1b; CH8.)* Run the edit-loop comparison of `experiment-plan.md` (B6, P and B0 after each of 10 preregistered edit batches) on every primary design and one scenario set.
    - (3) Run on 2 placement-seed variants per design (robustness only, not counted as independent).
    - (4) Run on held-out designs if licensed and affordable.
    - Report total cost, including EXP-001 generation, separately from per-analysis cost.
  - *Artifact:* `robustness.csv`; `edit-loop.csv`.
  - *Pass/fail:* decision equivalence (G1-G4) and the certificate audit (G7) hold everywhere, including after every edit batch. R is reported with CIs, with no new threshold. CH8 is reported as holding or not, with the cumulative wall times, and it limits the claim's scope rather than deciding H1.

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
  - *Procedure:* re-run B0 and P on one design and scenario set from the manifests alone, and compare decision files and median R. A verifier-side bison build of OpenSTA is recommended (`p3-p5-record.md` § 2).
  - *Artifact:* `reproduction.md`.
  - *Pass/fail:* identical decision files, and a reproduced R within the original 95% CI. The decision to proceed, revise or stop is recorded by the human, with reasons.

**Budget total (proposed):** 0.25 + 2.5 (P&R, unallocated until joint acceptance, U6) + 0.25 + 1.0 + 0.5 + 0.5 + 2.0 + 0.75 + 0 + 0.25 = **8.0 CPU-hours**. EXP-002 used 0.01 runner core-hours, outside this budget pending the owner's confirmation. If the P&R estimate exceeds 2.5 CPU-h, every later allocation must be renegotiated before continuing. Round 1b adds no allocation. Its new tests fit the EXP-002b cap, and the edit loop fits the EXP-007 cap through that task's priority order; if it does not fit, the held-out designs are dropped first.

## Challenger additions (pending)

Reserved for the challenger's required falsification tests, fairness controls and missing dependencies. The proposer will not sign until this section is complete and both roles agree on the exact text.

*Round-1b note.* On the human owner's instruction, the proposer adopted the five falsification priorities from the challenger's independent first pass (`runs/CDX-C05-INDEPENDENT-0001/independent-estimate.md` at commit `b7822234`) as proposer tasks: EXP-002b steps (6) to (9), the EXP-003 exception census, the EXP-004 additions, the EXP-006 audit and the EXP-007 edit loop. The challenger wrote those priorities without seeing this dossier, and they are not the challenger's dossier-specific additions. This section stays reserved for those additions after the dossier is released.
