# EDA-0007 — Electrical-contrast covariance for selective replacement timing evaluation

Batch 0003 additional cycle 1/4, research revision R1, 2026-10-15. **Conditional hypothesis; revise, not experiment-ready.** This release repairs the one-step acquisition and deterministic-observation contracts, supplies bounded analytical falsifiers, and reopens current source/contest material. It does not demonstrate a useful EDA gain or request a pilot.

Author: ChatGPT-P05-TIMING-B03-EDA-0007; logical session 5353d53c-1279-4e6e-8f34-409221f059aa; job 71796cdb-9158-417c-a464-60098bf7452a; input commit b1bb69f62b089c3489eaf17dea34daae84af315c; packet 8d27771f88c17fa1ac3ec3b3a02d3f7cd8f1b4d9e8572341d5ee8cc681d52632. Requested gpt-6.1-sol/high is assignment metadata, not independently attested backend identity. Review is unblinded. Historical proposer/challenger/verifier bytes are released inputs H01/H02/H03; their signatures and findings do not verify this revision. The owner has separately reopened four additional cycles, superseding historical stop instructions only for this bounded batch.

## Problem, demand and oracle

A timing-optimization developer chooses which legal replacement of one critical driver to measure next at an immutable checkpoint, then returns one measured replacement or the unchanged base. R01 is an actual temporary local-arrival-scoring consumer; R02 supplies a calibrated path-window alternative. The hypothesized useful endpoint is lower fully charged selection time at justified local regret and global WNS/TNS/electrical tolerances. Workload size, bottleneck prevalence and acceptable tolerances are unresolved, not established engineer requirements. See industry-gap.md and EXP-001/005/006.

Scope stays acyclic combinational paths, NLDM, one declared library/scenario, ideal clocks and maximum/setup analysis. Candidate cell functions and pin/geometry legality must be established; prefer same-footprint VT alternatives initially. Enough alternatives are not established. Pin-capacitance changes must propagate upstream. No topology changes, SI, MCMM, OCV/CPPR, hold, latches, generated clocks or path-exception guarantees are added. Unsupported inputs use fully charged reference handling. No silicon-signoff or globally optimal sizing claim follows.

Each query applies ORIGINAL candidate c to the same base, updates parasitics/timing, collects gain, affected-pin slew and complete reference guard summaries, rolls back, and checks restoration. g(c)=A_base(v)-A_c(v), pinned max rise/fall and scenario convention. m(c)=min_p(L_p-s_p(c)) over a declared pin set with valid slew limits. Missing limits are UNKNOWN. Known legality/capacitance checks are separate. Local modeled feasibility F_loc(c) combines those known checks and m(c)>=0. Final acceptance F_full additionally requires reference global guard conditions. Only measured candidates with F_full true may be returned; otherwise base. Local F_loc and global F_full are not interchangeable. The local acquisition below is a heuristic for the engineering endpoint until EXP-006 establishes its relationship to global closure.

## Coverage and nearest mechanisms

Search cutoff: 2026-10-15 UTC; deterministic replacement selection, timing calibration, covariance/transfer and bounded constrained search. sources.json and prior-art.csv distinguish reopened primary sections from abstract leads. R03 already supplies signoff-calibrated sizing; R04/R05 supply constrained/two-step acquisition; R06 supplies correlated GP machinery and its restricted cancellation case. R07 couples timing predictions and R08 learns an electrical subproblem. R09 was independently opened in full-text accessible form, especially §§3.3–3.4: discrete directional electrical guidance and multi-level calibration are now strong baselines. R10/R11/R12 update contest context; full current winner-method coverage remains incomplete. R13 supports only advertised commercial capabilities. R14 is a newly checked abstract lead for coordinated transformation loops.

Two search expansions found closer acquisition and calibration formulations. Therefore this round stops with documented search-budget exhaustion and residual novelty risk, not two negative expansions or exhaustive novelty clearance. Classical methods and straightforward calibrated estimation remain serious counter-hypotheses. Agent multiplicity is not justified for this local decision: no runtime LLM/agent system is added. Separate specialists/fusion, bounded joint prediction and a selective analytical/reference controller are competing baselines, not labels proving innovation.

## Physical feature construction hypothesis

The fixed anchor is signed candidate-versus-base electrical response structure, not a new GP or a generic predict/check loop. Given a baseline analytical map h(c;u) already using the strongest supported STA bias corrections, define d(c;u) as the predicted change relative to the base in (local gain, slew margin). Base timing is measured and charged. Define two shared normalized electrical axes at the target window: boundary input slew and boundary effective load. Candidate-specific pin-capacitance/loading effects remain inside h. Axes represent epistemic errors of this cheap response, not manufacturing variation. Candidate future engine results are never inputs.

For output o and axis j, use W[c,o,j]=[d_o(c;u0+delta e_j)-d_o(c;u0-delta e_j)]/(2 delta). This is a proposed bounded recipe, not a demonstrated implementation. A screening recipe would use delta=0.02 in log-normalized coordinates and diagnose delta=0.01/0.04 without choosing on held-out labels. Baseline d(base;u)=0 fixes the contrast origin. Range violations, left/right slope disagreement, active-min/max switches or unavailable Ceff produce a recorded UNKNOWN/fallback, not a favorable forced derivative. Probe tolerances and h implementation need EXP-001/002 approval before EDA execution. With two axes, feature cost includes four map evaluations per candidate plus base/shared work; no such EDA work was run here.

Let latent deterministic model discrepancy r=y-y_hat=Wz+epsilon, z~N(0,Omega), epsilon~N(0,D), K=W Omega W^T+D. Omega and D require declared training-family calibration; no labels or fitted values are available. Epsilon is indexed by frozen candidate/output/checkpoint. It is not freshly sampled query noise. An exact reference observation fixes BOTH the shared and per-index residual contribution at that observed entry. For queried index set O, posterior covariance is K-K[:,O] K[O,O]^-1 K[O,:], with no physical observation-noise addition. A numerical stabilization must preserve recorded exact observations and be reported, not redefine deterministic outputs as noisy. Singular cases need a tested support-aware solve or UNKNOWN.

An ordinary GP given the identical mean, W, Omega, D, labels and observation rule is exactly equivalent. This is retained negative evidence, now a required exact parity gate rather than a forecast of superiority over that same system. The possible contribution is constructing/calibrating physically useful W cheaply enough to improve the actual selection cost-quality tradeoff over equally informed conventional calibration and general raw-feature predictors. Generic GP notation, covariance alone, the two-step algorithm or the shared supplied features cannot be claimed new. R09 significantly narrows the feature/calibration distinction; no useful system delta is yet established.

## Repaired controller and one-step identity

Let b_loc be the best measured locally feasible gain including base. For the local model define M_loc as the best locally feasible gain in the fixed candidate set, and R(H)=E[M_loc|H]-b_loc. The historical one-step fantasy rule satisfies, by the tower property,

R(H)-E[R(H,Y_q)|H]=E[(g_q-b_loc)_+ 1{F_loc(q)}|H].

Thus its literal one-step rule is joint constrained EI (CEI), or CEI divided by a history-fixed estimated transaction cost. Cross-candidate covariance does not add a current one-step information term when same-candidate marginals are fixed. Gain/slew dependence remains relevant: CEI cannot generally factor into EI times feasibility probability. This repairs adjudicated OBJ-001 from H02/H03, and retires any previous one-step-information attribution. Complete hypothetical-table posterior simulations are unnecessary for this objective.

Default reference controller: direct joint CEI_local with exact posterior updates after each bundled measurement; measured-only terminal guard; deterministic ties. It is not asserted Bayes-optimal for F_full. All query guard outcomes are retained, and a measured local incumbent rejected globally cannot silently become an engineering success. Benchmarked output regret and guard failure use F_full as well as F_loc. Any stopping confidence is model-based, never an unconditional certificate.

A bounded two-query diagnostic is permitted as source/algebraic research, not a new acquisition contribution. For equal costs and exactly two remaining queries its local value is U2(q)=E[b_loc' - b_loc + max_r CEI_local(r|H,Y_q)]. This places the adaptive choice inside the expectation. One remaining query uses CEI. This is a finite restriction of established lookahead methods R04/R05. Heterogeneous-cost deployment requires an explicit remaining-budget Bellman rule or a separately labeled heuristic; dividing U2 by first-query cost is not claimed optimal. The experiment plan keeps equal-cost analytic checks separate from later fully charged deployment comparisons.

## Concrete analytical outcomes of this revision

EXP-000, fully reproduced in experiment-plan.md, contains two distinct checks:

1. Exact rational Gaussian conditioning on six arbitrary candidate/output rows: latent-factor and same-feature GP posterior means/covariances agree entry by entry, queried variances become zero, while incorrectly adding observation noise leaves variance 217/1048 at one queried entry. This establishes algebraic parity and semantics only.
2. A finite three-mode law for four measured candidates Q,B1,B2,B3: Q has gain -1 and margin 1,2,3 identifying the mode; B_i has gain 3 in mode i and -1 otherwise, margin 1. One-step CEI values are (0,1,1,1), identical to fantasy-regret reduction. Equal-cost two-query values are (3,2,2,2). Under an independent law with the same per-candidate marginals, they are (1,5/3,5/3,5/3). This demonstrates a possible later information effect and a switch in first-query preference. It is deliberately non-Gaussian, not a Gaussian timing model, a realizable Liberty circuit, a calibration experiment, evidence of deployment prevalence, or an EDA improvement. A separate same-candidate dependency check gives true CEI 0 where the invalid factorization gives 1/4.

The finite law is not promoted to the Gaussian physical hypothesis. Conversely, Gaussian parity is not performance validation. The tests separate a true one-step reduction, a logically surviving multi-step possibility and an exactly equivalent comparator.

## Attribution, headroom and falsifiers

Strong comparisons are current analytical calibration/window estimation; R09-inspired directional/calibrated guidance where faithfully adapted; exhaustive incremental enumeration; same raw features with separate specialists/fusion, shared-trunk predictor and a GP; and the identical W GP parity implementation. Each receives the same checkpoint, deployable inputs, allowed labels, candidate order, query cap and total resource ledger. Straightforward W plus CEI is the proposed implementation baseline itself; naming it differently creates no contribution. A learning architecture may lose to deterministic calibration.

Before any performance claim require: useful residual correlation after strong bias correction; held-out calibration/contrast ranking beyond scalar bias; sufficient legal alternatives; restored state correctness; saved charged work exceeding probes/fitting/acquisition/guards; and a justified local-to-global quality relationship. Kill the mechanism claim if these fail. If identical W GP diverges, debug implementation, never score the discrepancy as novelty. No universal lower bound, theoretical saturation, residual runtime fraction, calibrated effect size or success probability is established.

T_total=T_base+T_features+T_labels+T_fit+T_acquisition+sum(T_apply+T_update+T_report+T_restore)+T_final_guard+T_fallback. Report cold-start and amortized costs separately. Incremental queries or tiny candidate sets may already make learning pointless. Final measured guards certify only evaluated candidates under the pinned model; unmeasured candidates may be better.

## Direction, feasibility and position

The historical problem, user and contrast-covariance mechanism remain fixed in direction-control.json. Both drift scores are zero because the revision makes explicit already anchored W/observation/query assumptions; this is not a novelty or utility score. No agents, broader timing scope, extra labels or surrogate-only demand are introduced to escape criticism.

Current readiness blockers: complete lawful workload/candidate inventory and rights; compatible modern adapter/build and transitive rollback audit; physical residual/calibration data; current winner methods; actual implementation/reproduction owners; allocated EDA resources; justified quality/time thresholds; and matching P/C task-list consents. Historical GCD smoke and provisional caps do not resolve these. No EDA build/run, model fitting/training, GPU, remote compute or new paid API call occurred. Tiny own arithmetic and source reading are the only technical execution.

Position: retain a repaired conditional hypothesis for the next independent challenge. Do not accept for a pilot, infer abandonment consent, or convert remaining uncertainty into a universal duplication/dead-end claim. If three new substantive cycles do not converge, the batch policy parks the topic; a successor, if a cycle remains, must use a new ID and preserve these negatives. This proposer starts neither successor work nor experiments.

## Claim ledger

| ID | Type and trace | Current status |
|---|---|---|
| CLM-701 | Observation: R01 estimate/arrivalDelay/restore; R02 buildContext/estimate | Real local consumer and calibration baseline; transitive readiness/workload unverified. |
| CLM-702 | Observation: R03 §3.1; R07 method; R08 §II; R09 §§3.3–3.4; R10–R12 | Calibration, coupled prediction, electrical directional information and contests are prior; system novelty unresolved. |
| CLM-703 | Hypothesis plus own reduction: physical W, exact-observation conditioning and controller; R04–R06 | One-step information claim superseded; same-feature GP exactly equal; useful W/cost delta unresolved. |
| CLM-704 | Own algebra: EXP-000 and executable code | Stated finite/Gaussian checks passed; no EDA transfer or speed claim. |
| CLM-705 | Utility hypothesis: engineering endpoint and EXP-005/006 | Local/global quality relation and real savings unresolved. |
| CLM-706 | Documentary/limits: JOB, owner batch, resource brief, R13 | Research-only authorization; no commercial-absence or allocated-pilot claim. |
| CLM-707 | Historical record H01–H03, responses.md | Adjudicated OBJ-001/002 addressed; historical park/negative evidence preserved, no inherited approval. |
