# EDA-0002 R1b challenger review

Actor: Codex-C05-TIMING-R2 / CDX-Skeptic-TIMING. Session: /root/codex_c05_timing_r2. Input commit: 24ea3f3223f6f5171e96711a4df90204e4f2248c. Packet SHA-256: 6d77b6e3cc08db57c84c0335ca1c40a029be50290c2bac7d7266016a28a89003.

Status: one substantive review completed; allegations submitted for independent verification. No scientific approval, experiment authorization, consent signature or abandonment agreement. Initial assessment remains unchanged. The proposer saw that assessment before R1b; its amendments are not independent rediscoveries. Forecasts are now intentionally exposed under the full-stage assignment. Requested model/effort remains gpt-6-astra/low; actual selection is not independently observable. Policy amendment receipt and all 63 verified payload hashes are recorded in the local readiness record. Shared-host isolation remains policy-only.

## Review outcome

Three concrete fixable objections require adjudication. No supported fatal novelty or saturation objection is established. The candidate appropriately withdraws P3–P5, distinguishes finite tests from proof, exposes feasibility gaps and withholds numerical forecasts. Those disclosures do not establish the remaining certificate. The existing P7–P9 and refinement obligations still need resolution.

Packet locators below are relative to shared-proposer-output/candidates/EDA-0002 unless specified. C05-S01–S04 are this review's own external source IDs; C05-P01–P03 identify frozen dossier evidence, not independent corroboration.

## OBJ-001 — CPC resistance minimum omits interior absolute-value breakpoints

- **Targets:** CLM-023, P7; proposal.md § Proposed mechanism, B / Rd-interval; tasklist.md EXP-002b.
- **Severity:** major, fixable soundness defect in the stated sufficient test; confidence high for the mathematical omission, unresolved for occurrence in the intended libraries.
- **Observation:** pinned DmpCeff.cc computes Rd from the absolute difference of two table delays, then tests low Rd or Rpi small relative to Rd (C05-S01, gateModelRd lines 1640–1648; setCeffAlgorithm lines 1561–1571). The proposal samples slew ends and table grid points to establish its minimum.
- **Reasoning:** even with ideal piecewise-linear table evaluation, the absolute difference can have an interior zero within a grid cell. Its minimum need not occur at a sampled end. This is independent of float-rounding error.
- **Analytic witness, not an executed fixture:** within one normalized slew cell x in [0,1], let the signed finite difference, after its positive scale factor, equal 2−4x ohms. Thus Rd=|2−4x|. Choose Rpi=0.001 ohm and C1=C2>0. Both sampled ends give Rd=2>1000 Rpi, so the written minimum test accepts CPC. At x=0.25, Rd=1 and the strict branch Rpi<Rd·1e-3 fails; Rd<0.01 also fails, as do the structural tests. The reference therefore selects the noncapacitive Pi branch. Positive table delays can realize this signed difference by adding a sufficiently large common offset. No assumption of monotonic load delay is stated that rules it out.
- **Consequence:** a net admitted by the written test can violate the branch premise on which R1 bounds rely. This disproves that test as a general sufficient rule, not a measured violation on a real design or an indictment of every CPC route.
- **Refutation/repair test:** show a frozen enforced admissibility condition excluding sign changes of the signed finite difference, or include interior roots and sound float interval bounds in the minimum calculation. Construct the two-load-column fixture above with physical units, inspect interior branch selections, and test adjacent representable values. Pass only if the classifier rejects unsafe intervals or proves every admitted slew selects DmpCap. Finite sampling supplements, rather than replaces, the universal argument. Preserve structural CPC paths; no mechanism pivot is requested.

## OBJ-002 — Endpoint fraction is not a runtime upper bound

- **Targets:** forecast.json assumption 2; proposal.md § Remaining headroom and oracle claims; tasklist.md EXP-003 step 1 / K3; CLM-010 feasibility gate.
- **Severity:** major, fixable evaluation/stop-rule defect; confidence high for the counting argument.
- **Evidence:** C05-P01 forecast states that attainable R is bounded by the CPC share of endpoint/scenario cones. C05-P02 EXP-003 permits stopping from that share and exception exclusions before phase measurements. Cone union and phase costs appear elsewhere, but no theorem links unweighted endpoint count to saved runtime.
- **Reasoning:** one certifiable endpoint can own a large expensive exclusive cone while many uncertifiable endpoints share a tiny cone. Conversely, many certifiable endpoints can share almost all work with one uncertifiable endpoint. Endpoint fraction therefore supplies neither a general upper bound nor a reliable runtime forecast. This is an analytic graph-work counterexample, not a measured design.
- **Consequence:** K3 can incorrectly terminate a useful direction or overstate headroom. An oracle screen is an upper bound only within a stated implementation/cost model with omitted oracle costs and retained work defined; its measured wall time alone is not a universal ceiling over all algorithms.
- **Refutation/repair test:** replace count-only stopping with a justified optimistic bound on removable exclusive graph work, accounting for shared clock/fixed work and required cone unions. Until available, census is descriptive and cannot trigger K3 alone. Validate the estimator on two synthetic graph families with opposite sharing patterns when experiments are authorized. Pass if no impossible count-to-cost implication is used and oracle assumptions are explicit.

## OBJ-003 — Exact output contract and tolerance-based success disagree

- **Targets:** CLM-009, CLM-010; proposal.md preserved-output table; experiment-plan.md G3/G4, G7 and H1; tasklist.md EXP-006.
- **Severity:** major, fixable verification-contract defect; high confidence.
- **Evidence:** C05-P03 promises exact sub-margin slack and WNS/TNS, but G3/G4 accept differences within 1e-6 ns; G3 also names an outer 0.005 ns bound. G7 requires exact comparisons for certificate lower bounds but sends refined slack equality back to G3.
- **Reasoning:** a nonzero refined-slack difference inside tolerance can pass H1 while violating the stated exact-equality contract. Zero missed violations is a separate condition and does not resolve this discrepancy.
- **Refutation/repair test:** define a canonical numerical output contract, serialization precision, zero/NaN policy, aggregation order and exact comparator for the preserved quantities. Use tolerance only as a separately named diagnostic, or explicitly narrow the equality claim and reassess the anchor. A comparator fixture with unequal same-sign negative values less than 1e-6 ns apart must fail an exact contract. No such fixture was executed here.

## Source-driven novelty and demand update

C05-S02 (DAC 2011, §6.1, equations 8–11 and discussion on printed pp. 780–781) uses full anchor timing plus clock-only runs to estimate other-corner hold slack. It explicitly discusses neglected data-delay/hold differences and startpoint stability. This supports structural overlap, but does not establish R1's code-level certificate or exact-refinement equivalence. Its industrial setup (§3) is historical evidence of the workflow, not current OpenSTA performance. K1 is not triggered merely by this paper.

C05-S03 (DAC 2008, §§2–3, equations 4–12) gives bounds for a class of nonlinear parameterized delay models. A blanket linear-only characterization of that family is inaccurate. It does not demonstrate discrete NLDM/DMP semantics plus the required decision set. CLM-005/L2 should remain scoped to specific linear papers, retaining this distinction. The dossier already flagged this uncertainty; no fatal novelty allegation is inferred.

An independently discovered source outside the supplied ledger, C05-S04 (IBM author publication abstract, On the signal bounding problem in timing analysis), studies slew-dependent bounding signals and warns about latest-arrival slew selection. Abstract access makes this a comparison lead, not evidence that R1 is unsound or duplicated. Compare its bounding semantics before claiming structural novelty.

## Remaining conditions and coverage

| Area | Assessment |
|---|---|
| Duplicate/equivalent prior work | Unresolved; newly read nearby methods do not establish duplication. Broader citation/contest coverage incomplete. |
| Nontrivial contribution / naive composition | Unresolved pending sound certificate, applicable prior-work comparison and ablations. A guarantee relative to a pinned implementation could matter; its utility is not established. |
| Demand | Historical sourced motivation plausible. Present user validation and utility of the deliberately limited D_M output remain unresolved. No claim of commercial signoff equivalence. |
| Theoretical headroom | No saturation result established. OBJ-002 concerns a false counting inference, not exhausted headroom. |
| Contest originality | Supplied topic summaries acknowledged; official rules/winner methods not independently checked this round. Unresolved, not proof of overlap. |
| Feasibility | Libraries/rights, pinned generation recipe, allocated prerequisite budget and executable commands remain pending as disclosed. Released synthetic logs were inspected as proposer evidence, not independently rerun or verified. |
| Full cost | Accounting categories and incremental comparator are useful. Charge diagnostic/certificate output consistently; retain cone-sharing costs and separate oracle privileges. |
| P8/P9 / refinement | Unresolved as admitted. No explicit rounding formula, operation-order proof or full exception matcher is yet supplied. Passing finite fixtures alone must not relabel these proved. |

Direction assessment against the supplied frozen anchor only: combination_drift=1, demand_drift=0, total=1 provisionally, consistent with narrowing rather than replacement. No score ≥2 is supported by this review. A score of 1 is not acceptance (charter requires zero at acceptance). The original round-0 file is not independently available, so historical preservation is not fully audited. Required repairs retain certificates and exact refinement; no combination-only pivot or unsupported-demand substitution is requested.

## Required task-list amendments and consent

1. EXP-002b: add OBJ-001 root/branch fixture and a universal classifier argument, with non-finite/division-denominator handling. Owner P; C reviews, V adjudicates. Artifact: classifier proof and branch records. Pass: all admitted domains meet branch premise.
2. EXP-003: remove count-only K3 stop; supply the cost-bound assumptions and union-work accounting in OBJ-002. Owner P, C reviews estimator. Pass: defensible cost model or no ceiling-based termination.
3. EXP-004/006: exact comparator and comparator regression required by OBJ-003. Owner P. Pass: exact contract and comparator agree, certificate audit retained.
4. EXP-002b: freeze P9 allowance formula and reference operation ordering, exceptional-value policy and P8 matcher semantics before testing. Missing derivation remains unresolved even if finite tests pass. Owner P; V checks entailment.
5. EXP-005/006: resolve one-design versus per-design pilot discrepancy; state whether success concerns an estimated 20% reduction or a lower-confidence-bound 20% reduction. Freeze unchanged primary metrics before seeing confirmatory results. Fix margins before calibration; charge all pilot/tuning costs.
6. Bind tasklist to exact hashes of experiment-plan.md, scope/algorithm specification and resource/input lock; fill prerequisites before consent. No experiment launched by this review.

Consent withheld for this exact task-list SHA-256 bb1f2e6c4ee63273b45b78041a921bbc77fca09e6a4263b48cec27150905d0ef pending adjudication and repair. This is not a veto or verifier ruling. No abandonment grounds jointly established. Proposed next disposition: revision/clarification after independent verification.
