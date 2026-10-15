# EDA-0007 — Electrical-contrast covariance for selective replacement timing evaluation

Initial successor; owner D05 batch cycle 4/4, 2026-10-15. **Conditional hypothesis; novelty, utility and feasibility unresolved. Not experiment-ready.** Complete the scheduled independent challenge/verification and stop the batch. This proposer recommends no pilot or acceptance; no useful system delta is demonstrated.

Author ChatGPT-P05-TIMING-EDA-0007; logical session c807b92b-b6c4-48ea-b9cf-67682a012958; input commit f68c1492c05be3fac5622deac4bb479eabf957de; packet b134fc0b334c43b56e99a085e5f96a526a299dab89eeecebf8f3b781e3d5a9f6. Requested model is in JOB.json, without separate role-level attestation. Review is unblinded. Cutoff 2026-10-15 UTC. Only supplied released predecessor files and accessible independent external sources were read; no foreign private role material or withheld checkout was inspected.

## Problem and actual decision

A timing-optimization developer chooses a function-preserving cell replacement for one fixed critical driver from a finite ordered legal set at an immutable checkpoint. Decide which candidate to measure next, then which measured candidate to offer to the optimizer. Do not require a dense endpoint vector. Public OpenROAD source S02 provides a concrete consumer: its measured-VT candidate measures a local arrival difference under a temporary edit and restores the design. It does not establish workload size, bottleneck fraction, our complete adapter or global closure benefit.

The deployment endpoint is fully charged time to return a measured feasible replacement with low reference-local-score regret; downstream WNS/TNS and electrical violations must also be checked after a guarded commit. Local arrival improvement can worsen another endpoint. EXP-006 must validate the proxy-to-closure connection; local prediction accuracy alone cannot justify usefulness.

## Three-lens shortlist, before selection

| Lens and concrete candidate | Closest mechanisms and proposed interaction | Selection position |
|---|---|---|
| Cooperating algorithmic agents | Arrival agent proposes replacements; electrical agent supplies slew/cap objections on a versioned shared intervention record; one transaction evaluator resolves conflicts and invalidates stale reports. Observations/actions are restricted to the same checkpoint, tables, features and returned measurements. EDAid and AgenticPD already cover multi-agent/stage orchestration (S10/S11, abstract access). | Not selected: no supported reason role separation improves on deterministic estimate/measure/rollback. Fair alternatives would be one repeated-call controller, parallel search and a non-LLM state machine with equal information/EDA-call budget and charged communication. No runtime agents or LLM calls are added. |
| Bounded unified predictor | Replacement-conditioned joint local-arrival-gain and slew-margin predictor. PreRoutGNN already treats coupled timing quantities (S04); current analytical windows and learned capacitance models are strong alternatives (S03/S05). | Not a standalone contribution. Compare separate specialists plus fusion and a shared-trunk model using identical features, labels and fitting budget. Joint prediction is a component hypothesis below, not a novelty label. |
| Prediction plus analytical and scoped exact work | Model candidate contrasts using signed sensitivities to common electrical errors; a bundled exact observation updates the unmeasured alternatives. Generic correlated GPs and information acquisition are prior (S07/S08). | Selected: test whether intervention-dependent physical contrast structure offers a useful low-label cost/reliability tradeoff beyond current calibrated estimation and a faithful supplied-feature joint GP/controller. |

This is one new topic, not three live projects. Conventional alternatives include scalar incremental timing, calibrated analytical estimation, deterministic score ordering and classical sizing/calibration (S01–S03/S09). No source-based shortlist proves superiority.

## Scope, deployable information and output contract

Initial slice: acyclic combinational data paths, unchanged netlist and extracted-wire topology, NLDM, one library/scenario, ideal clocks and maximum/setup analysis. Replacements must be functionally equivalent and pin/geometrically legal; prefer same-footprint VT alternatives in the first adapter. Enough alternatives in lawful representative libraries are NOT established. Changed pin capacitances and upstream loading must propagate. Topology edits, new routing/buffering, SI, MCMM, OCV, CPPR, hold, latches, generated clocks and path exceptions require ordinary reference handling; no foundry-signoff claim follows.

Inputs available before querying: checkpoint/version hashes, candidate library identities/LUTs, existing base-state timing, parasitics, candidate-dependent loads and bounded analytical electrical-window features. Base timing and extraction costs are charged. Calibration labels are a missing dependency, not assumed available. Candidate-specific future reference outputs and post-selection labels are forbidden features.

For a fixed target driver v, g(c)=A_base(v)-A_c(v) using the pinned scalar engine, scene and max-rise/fall convention. m(c) is the minimum slew-limit margin over the declared affected pins; missing/unsupported limits remain explicit. Direct library/load/geometry checks supply capacitance and legality constraints where valid. The approximate predictor returns y_c=(g(c),m(c)). A query applies ORIGINAL c to the immutable base, performs valid incremental timing/parasitic updates, returns bundled outputs plus full global guard summaries, restores the base and verifies restoration. A local prediction window does not certify unchanged external endpoints.

Return only a measured candidate or unchanged base. The selected candidate receives full reference guards before commit. Engine-relative feasibility is limited to that evaluated candidate and declared model. **No exact best-candidate, same-decision, unconditional coverage or silicon-signoff claim.** An unqueried candidate may be better. Gaussian probabilities are model beliefs; calibration is empirical. Checking the returned choice cannot recover a missed optimum. Unsupported or changed-state cases take a valid, fully charged reference fallback.

## Mechanism and closest alternatives

S02 is an actual measured path; S03 already contains local-window estimation and STA slew bias. Generic predict/check, confidence gating, multitask learning, exact rollback and incremental timing are not new. S06 and S16 are forward leads requiring full-method audit, not claimed inferior baselines. S07 supplies correlated conditioning and the noiseless block-design transfer-cancellation warning. S08 supplies constrained information search.

Let y_hat be the strongest calibrated analytical mean. Build a candidate-by-output loading matrix W from the difference between each replacement's and base's analytical responses to the SAME signed boundary-slew/load perturbations. Shared axes identify the same electrical source. Candidate/output rows can have different signs and magnitudes. In normalized units the hypothesis is r=y-y_hat=Wz+epsilon, with z~N(0,Omega), epsilon~N(0,D), so K=W Omega W^T+D. W is pre-query observable; Omega/D need training-family calibration or an explicit unresolved cold start. Probe only valid table/model ranges. Non-smooth path switches, failed probes or missing physics expand residual uncertainty/trigger UNKNOWN, never a forced favorable sign.

This is a physically parameterized latent-factor GP, not new probability theory. It may be exactly expressible by an ordinary supplied-feature GP: that comparator is mandatory. The proposed system delta is only a useful parameterization/integration cost tradeoff if demonstrated under identical information, not the formula or generic query scheduling.

A common electrical-model error can cancel in the difference of two alternatives or amplify it when their signed responses differ. Therefore marginal confidence and RMSE need not reflect uncertainty of the engineer's comparison. Existing deterministic slew-bias correction might already remove the relevant error, leaving no headroom. Physical covariance could also be wrong and harmful.

## Controller and state interaction

1. Freeze target/base/candidate order/legality and available measurements. Compute analytical means and W without changing shared timing state.
2. Maintain one posterior over the finite candidate/output table. Queried entries become observed engine results; charge fitting and every label. Do not use held-out future candidates to refit for free.
3. The incumbent is the measured feasible candidate with greatest positive g under deterministic ties; unchanged base is always allowed. For acquisition, draw bounded joint hypothetical tables, estimate reduction in Bayes simple regret of this measured-only policy after each possible bundled observation, and divide by predicted full transaction time. Use the same capped fantasies/samples/controller in joint-kernel baselines. This is a finite approximate value-of-information rule, not an exact acquisition solver.
4. Stop at fixed query/time cap or a preregistered model-risk threshold. No guarantee attaches to early stopping. Full engine guards accept one measured candidate or retain base; independently scored replacements are not combined without recomputation.
5. Any base change invalidates state-specific predictions, factors and query results. Only permitted calibration transfers under a declared version/corner contract. Charge fallback, failures and invalidation.

## Analytical witness, observation versus inference

EXP-000 checked standard Gaussian arithmetic with exact rationals: two errors with variances 10 and covariance 9 have contrast variance 2; independent errors with the same marginals give 20; covariance -9 gives 38. After observing the first variable, the other's positive-case variance is 19/10. Thus equal marginals do not determine pairwise uncertainty. This is not an EDA witness, trained model, calibrated probability or speedup. Equal shared loadings cancel before a query; a large marginal-variance reduction alone need not improve ranking. Wrong-sign transfer is a mandatory negative control. Circuit realizability and useful error structure remain EXP-003 obligations.

A second constructed witness ties the signs to a bounded electrical intervention. Let the known base arrival be 12, and a locally monotone upstream response be D(C)=D0+k(C-C0), with positive but cheap-model-uncertain slope k. Two replacements change input load by +0.2 and -0.2; their remaining path constants give arrivals a_A(k)=9.8+0.2k and a_B(k)=10.2-0.2k. At k=0.5, arrivals are 9.9 and 10.1; at k=1.5, they are 10.1 and 9.9. Both primitive load responses are monotone, but candidate score-error loadings have opposite signs. At k=1 they tie. Exact base timing fixes D0, not an otherwise unidentified slope; if available cheap information already determines k exactly, this uncertainty and proposed benefit disappear. This is a synthetic affine electrical-model witness, not a real Liberty/RC network, an OpenSTA result or evidence of common deployment frequency. Here uncertainty is epistemic error of a cheap intervention response, not manufacturing variation. EXP-000 independently checked these rational inequalities; EXP-003 must establish whether any such residual exists after current bias calibration.

## Contribution attribution and falsifiers

Route: conditional useful combination/structural parameterization. Compare against current analytical estimation with STA slew bias, independent specialists/fusion, shared-trunk prediction, generic multi-output GP and a supplied-feature latent-factor GP with the SAME W/data/mean/controller. The latter may be equivalent; no artificial information handicap is allowed. A1 diagonal covariance; A2 remove cross-output factors; A3 shuffle W within targets; A4 same features/full GP; A5 strongest deterministic calibration; A6 opposite/zero sensitivities and path switching; A7 noiseless full-output block design; A8 cold versus amortized labeling. These test attribution without demanding a new theorem or super-additivity.

Kill H1 if contrast calibration fails, a faithful generic comparator eliminates useful delta, shared effects cancel, a scalar correction suffices, candidates are too few, or modeling overhead exceeds query savings. Kill utility if local improvements fail downstream guards or time savings require worse-than-tolerated regret. A transaction restore failure invalidates subsequent observations. Do not rescue failure by adding agents, labels, trials, full-flow models or MCMM under this ID.

## Claim ledger

| ID | Type / locator | Position |
|---|---|---|
| CLM-701 | Observation; S02 estimate/arrivalDelay/restoreEstimateJournal, S03 buildContext/estimate | Actual local replacement consumer; workload/adapter unresolved (EXP-001/002). |
| CLM-702 | Observation; S04 auxiliary timing tasks, S05 §§II–III, S12 §§2/5 | Coupled predictions and constrained sizing are prior; no broad unified novelty. |
| CLM-703 | Conditional hypothesis; W model/controller; S07 §§2/2.3, S08 §3 | Electrical contrast structure may aid query selection; EDA validity and useful novelty unresolved (EXP-003–006). |
| CLM-704 | Own finite arithmetic; EXP-000 | Equal marginals can mask different comparison uncertainty; no EDA transfer established. |
| CLM-705 | Utility hypothesis; S01/S02 integration and task list | Lower measured-selection cost at comparable regret/global outcome possible; magnitude unknown. |
| CLM-706 | Documentary; owner brief/JOB/S13 | No allocation, commercial absence, representative labels or scientific acceptance established. |
| CLM-707 | Released historical H01–H03 | EDA-0006 negative lessons retained; no inherited verification of this successor. |

## Headroom, feasibility and final position

No applicable lower bound, saturation or calibrated gain exists. T_total=T_base+T_features+T_fit+T_acquisition+sum(T_apply+T_update+T_report+T_restore)+T_final_guard+T_fallback. Compare current calibrated policy and full incremental enumeration, with cold and amortized labeling separately. Fully incremental queries may already be too cheap to improve.

Missing: compatible modern build, complete adapter/restore/read-set audit, representative lawful candidate sets, calibration labels, named implementer/reproducer, actual resource allocation, meaningful regret/downstream tolerances and matching task-list consents. Historic provisional CPU caps are not an owner allocation. No new EDA/full-flow/training/GPU/remote/paid-API execution occurred.

EDA-0006 remains parked; its generic execution distinction and full-vector demand are not resurrected. This new smaller-output probabilistic mechanism uses a new ID. Initial drift scores are zero for consistency, not merit. The cycle-4 result is a conditional source-mapped hypothesis and dormant dependency plan, not acceptance, joint abandonment, theoretical exhaustion or universal duplication. Future work after the scheduled independent reviews requires a separately authorized restart beyond this four-cycle batch.
