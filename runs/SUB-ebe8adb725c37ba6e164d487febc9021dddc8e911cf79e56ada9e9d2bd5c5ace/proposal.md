# EDA-0007: Electrical-contrast covariance for selective replacement evaluation

Additional batch 0003 cycle 2/4, revision R2, 2026-10-15. **Conditional hypothesis; revise; no pilot or experiment authorization.** Actor ChatGPT-P05-TIMING-B03-EDA-0007-REPLACEMENT-1-8154ee5a; logical session 5796edbb-fac9-477b-ab72-194c4cbfe34c; job e49aa3b5-4266-4966-ab60-b7455dfa7a9a; input commit b1bb69f62b089c3489eaf17dea34daae84af315c; packet a33750c8ec5badb03663cf317bd8b6ea96e6e5d9905fe82f0c50861adbbe46d9. Requested model gpt-6.1-sol/high is assignment metadata, not independent backend attestation. This fresh execution receives only frozen policy and released files; review is unblinded.

## Frozen problem, demand and reference contract

A timing-optimization developer selects which replacement of one critical driver to measure at an immutable checkpoint, then returns a measured candidate or base. The engineering hypothesis is lower fully charged selection time at justified local regret and global WNS/TNS/electrical tolerances. Useful candidate counts, bottleneck prevalence and tolerances remain unknown. N01 supplies an actual local consumer; N06 supports the broader physical/electrical task context, not a measurement of this proposed bottleneck. The local-to-global relationship must be tested, not assumed.

Scope remains acyclic combinational paths, NLDM, single library/scenario, ideal-clock maximum/setup analysis. Initially prefer lawful same-footprint VT alternatives, without asserting that a representative workload exists. Pin-capacitance effects must propagate upstream. No MCMM, hold, SI, OCV/CPPR, latches, topology changes or foundry-signoff guarantee is added. Unsupported cases use charged reference fallback.

For candidate c, g(c)=A_base(v)-A_c(v) under a pinned rise/fall/scenario convention; m(c)=min_p(L_p-s_p(c)) over declared affected pins with valid limits. Apply each candidate to the original base, update parasitics/timing, capture g,m and complete reference guards, restore and check database plus oracle state. Known replacement legality and capacitance checks are separate from m>=0. F_loc uses those known checks and local margin. F_full additionally requires the pinned global reference guards. Return only a measured F_full-passing candidate, otherwise base. A final guard certifies only the measured output under the pinned model, not an unmeasured optimum or silicon signoff.

New adapter clarification from N01 raw lines44-66: estimate's `legal` field includes `score > 0`, while raw non-improving scores are preserved. Consequently the adapter must record replacement_legal, query_succeeded, improves, F_loc and F_full separately. It must not treat this overloaded flag as the label for physical legality, discard negative scores or invent missing constraint observations. Current source returns an arrival score, not the proposed complete gain/margin/guard bundle. The feasibility of adding that bundle without invalidating restoration remains unresolved. This matters because an informative but non-improving probe must be queryable and charged if a lookahead test uses it.

## Evidence coverage and nearest approaches

Cutoff 2026-10-15 UTC. Current primary reopens N01/N02 identify a journaled consumer and load-dependent calibration; N03 supplies classical calibrated incremental/peephole sizing; N04 supplies established constrained lookahead; N05 supplies electrical directional guidance with multi-level calibration. These are strong competing mechanisms. N06/N07/N08 update official contest context; current winner algorithms remain incompletely audited. N09 supports advertised commercial ECO/ML capability only. Neither open-source absence nor unknown commercial internals proves scientific novelty.

The first search expansion covered current winner identities, bundled/noiseless constrained search and correlated outputs. The second expanded calibration/electrical covariance and official program/citation references. It found an additional contest primary paper and a noise/cancellation lead N11, with direct access failing for N11. Many electrical/optical/medical hits were irrelevant. No exhaustive novelty clearance is claimed; the bounded search budget is exhausted with explicit remaining winner and W-equivalence risks. Historical R07/R08/R14 leads remain in the inherited ledger but were not reopened in this job and carry no fresh verification.

## Anchored mechanism and same-feature equivalence

Keep the original signed candidate-minus-base electrical-response mechanism. Let h(c;u) be a cheap analytical map already using strong supported calibration and d(c;u) its contrast to base in gain and margin. Two shared epistemic axes at the target are log-normalized boundary slew and effective load, not process/manufacturing variation. Candidate pin-capacitance effects remain within h. Proposed feature:

W[c,o,j] = (d_o(c;u0+delta e_j)-d_o(c;u0-delta e_j))/(2 delta).

Screen delta=0.02, diagnose 0.01/0.04 without choosing on test labels. Four map calls per candidate and all shared/base work are charged. Out-of-range LUTs, active-min/max changes, inconsistent slopes or unavailable Ceff yield UNKNOWN/fallback. Thresholds/implementation are unresolved until EXP-001/002. No physical W was generated here.

Model deterministic discrepancy y-mu=Wz+epsilon, z~N(0,Omega), epsilon~N(0,D), K=W Omega W^T+D. Persistent epsilon is indexed by frozen candidate/output/checkpoint. It is not resampled query noise. Omega,D and normalization require training-family calibration. Exact observations condition both z and indexed epsilon, so observed entries have zero posterior covariance. For a supported observation block O, K_post=K-K[:,O] K[O,O]^-1 K[O,:]. Redundant observations require a support-aware solve or UNKNOWN; numerical jitter cannot silently redefine deterministic outputs as noisy.

An ordinary GP with identical mu,W,Omega,D, observations and controller is exactly the same predictive system. A different score against it is a bug or accounting mismatch. The possible contribution is the useful cost/quality tradeoff of physically constructing/calibrating W beyond equally informed strong calibration and generic electrical-feature models. GP form, covariance, electrical inputs and lookahead algorithms are not claimed new. N05 makes input/mean-calibration parity especially important. There is still no established useful EDA system delta.

## Controller, rank boundary and bounded Gaussian progress

With local measured incumbent b and fixed candidate set, R(H)=E[M_loc|H]-b obeys R(H)-E[R(H,Y_q)|H]=E[(g_q-b)_+ 1(F_loc(q))|H]. The default is joint CEI_local with exact posterior updates and deterministic ties. Same-candidate dependence forbids arbitrary EI-times-feasibility factorization. Cross-candidate covariance can affect later beliefs; it supplies no additional current one-step term at fixed candidate marginals. This earlier correction is preserved.

With two equal-cost queries, U2(q)=E[b'-b+max_r CEI_local(r|H,Y_q)]. This is an established bounded lookahead diagnostic (N04), not a new acquisition algorithm. Unequal costs require an explicit remaining-budget policy or a separately labeled heuristic; U2 divided by first cost is not called optimal. The local policy is not proved optimal for F_full.

Accept the adjudicated cycle-1 OBJ-001 (V1 below): if D=0, mu,W known, latent dimension two, and EVERY admissible first query bundles two outputs with invertible W_q, any query identifies z. With two equal-cost queries, the second can measure the best remaining locally feasible candidate. Both posterior-updated myopic CEI and optimal lookahead therefore reach the same local table optimum realization by realization. This conditional saturation boundary does not imply physical saturation or eliminate transfer versus an independent model.

EXP-000R2 executes exact rational checks for all three invertible blocks (determinants1,-2,5), all giving zero table covariance. For the fixed six-row W in the public script and D=rho I, after observing the first identity block, remaining trace is 14*rho/(1+rho)+4*rho: 0,451/2525,11,41800/101 at rho=0,0.01,1,100. Observed rows remain exactly zero. Persistent D prevents complete identification but does not itself prove useful lookahead. A separate rank-one redundant bundle leaves unobserved variances1,4.

A new jointly Gaussian, mixed-rank witness closes the prior non-Gaussian-only diagnostic gap. Let z1,z2 iid N(0,1), base gain0, exact (gain,margin) bundles Q=(z1-2,z2), A=(z1,1), B=(z2,1), C=(-z1-z2,1); all replacements queryable. D=0 and block ranks are (2,1,1,1). CEI(Q,A,B,C) is approximately (0.004245,0.398942,0.398942,0.564190), so myopic first queries C. Its second query is A/B tied because observing C reveals the sum and their conditional laws are symmetric; Q is pointwise dominated by A wherever Q is feasible. Q-first instead reveals both axes and then measures the best A/B/C, attaining max(0,z1,z2,-z1-z2). The myopic terminal value is max(0,z1,-z1-z2). Deterministic Gaussian angular quadrature gives expected values1.174157 versus0.927597, difference0.246560 in stipulated dimensionless units; conservative integration-error interval for the difference is [0.246390,0.246730]. See full proof, numerical bound and script in experiment-plan.md.

This does not contradict OBJ-001: three exploitation blocks are singular. The stipulated constant margins and known feature map are not a realizable Liberty circuit demonstration. Neither covariance nor lookahead is therefore an established deployment benefit. A matched independent-candidate law preserves every candidate's joint gain/margin marginal; Q then informs no other candidate. Its Q-first terminal expectation is bounded above by CEI(C)+CEI(Q)=0.568435. This is a transfer control for that Q-first policy, not a solved independent optimal-policy result. The identical W GP matches every correlated result. Real residual rank/conditioning, prevalence and charged utility remain unknown.

## Attribution, headroom and decisive falsification

Separate three questions: mean calibration, physical W information, and controller. B0 exhaustive reference; B1 calibrated local/offset ordering; B2 faithfully adapted N05 directional/calibrated ordering; B3 separate same-feature gain/slew specialists with fusion; B4 shared-trunk model; B5 generic raw-electrical-feature GP; B6 identical-W GP parity; P proposed W plus CEI. Every compatible model gets the same labels, features, policy sweep, bundles, candidate order, guards and charged budgets. Feature redistribution cannot manufacture contribution. EXP-003 records shared inputs/calibrated mean/W/covariance/policy row by row.

A11 explicitly separates all-full-rank D=0, mixed/rank-deficient D=0, and persistent D>0, including singular/ill-conditioned cases. A1 matched candidate marginals with cross-candidate dependence removed tests transfer; A10 same posterior myopic versus lookahead tests policy. Positive results in one comparison cannot support the other. No generic mathematical novelty or super-additivity requirement is imposed.

Kill or narrow claims on no residual benefit after strong calibration, no legal alternatives, failed restoration, rank saturation, wrong/miscalibrated transfer, overhead exceeding saved queries, or a poor local/full-guard relationship. No universal lower bound, calibrated success probability, applicable runtime floor or numerical EDA improvement forecast is established. Query/feature/label/fit/acquisition/apply/update/report/restore/guard/fallback time and memory are all charged, with cold-start and amortized costs distinct.

## Feasibility, direction and position

Both direction penalties remain zero: user, physical contrasts, deterministic bundled observations, measured-only return and global utility need are unchanged. Rank-aware falsification and adapter semantics repair the same anchor. Zero drift is not a merit score. No new agents, broadened corner scope or accuracy-only objective is introduced.

Readiness remains blocked by lawful representative workloads, complete generator/transaction/build/dependency locks, informative residual data, current winner-method closure, actual implementation/reproduction owners, justified endpoint thresholds, real experiment allocation and fresh matching P/C exact-task consents. No EDA build/run, label generation, fitting/training, GPU, remote compute or new paid API call occurred. Only tiny own arithmetic, trusted structural checks and public reading were run.

Position: submit R2 for independent review, keep the conditional physical hypothesis, and request no pilot. The new Gaussian witness removes one analytical gap without resolving physical novelty or feasibility. After three unsuccessful additional cycles follow the batch park/succession rule; four cycles total remains a hard stop. No abandonment consent or inherited historical approval is inferred.

## Stable claims

| ID | Type / locator | Status |
|---|---|---|
| CLM-701 | Observed source consumer/calibration, N01 raw44-66; N02 raw492-521 | Exists, but complete adapter and workload unverified. |
| CLM-702 | Prior mechanisms N03 section3.1; N04 sections2.3/3.2; N05 sections3.3/3.4 | Strong baselines; W-system distinction and winners unresolved. |
| CLM-703 | Hypothesis and algebra, anchored W/CEI/exact observation specification | Same-W GP equality; physical utility unresolved. |
| CLM-704 | Own checks A01/A02; experiment-plan reproduction | Prior exact fixtures rerun; new Gaussian/rank checks pass; no physical transfer established. |
| CLM-705 | Utility hypothesis, EXP-002/005/006 | Local/global link and meaningful total-cost savings unresolved. |
| CLM-706 | JOB and batch policy; N09 advertisement | Research-only resources, no commercial-absence or pilot claim. |
| CLM-707 | Released P1/C1/V1; responses | Current adjudicated repair integrated; predecessor findings remain historical. |
| CLM-708 | Own conditional lemma, V1 OBJ-001, A02 | Full-rank D=0 boundary accepted; mixed-rank Gaussian witness outside premises. |
| CLM-709 | N06 section4 Eq16 and section5.3; N07 winners; N08 README | Contest context updated; no winner algorithm clearance or MCMM pivot. |
| CLM-710 | Source observation N01 raw44-66; adapter inference | Improvement flag must not substitute physical-legality/observation semantics. |
