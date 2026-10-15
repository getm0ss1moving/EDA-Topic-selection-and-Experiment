# Conditional experiment plan, revision 3

EDA-0008, batch 0003 cycle 3/4. Research output only; EXP-000 is closed. No EDA executable, adapter, training or routed flow is run or claimed present. All execution tasks require future phase-specific exact allocation, distinct proposer/challenger consents and independent readiness checking. Proposed values below are design choices for review, not owner resource commitments or validated engineering targets.

## Physical endpoint and branch semantics

Retain legal post-detailed-placement / pre-CTS / ideal-clock / single-PVT state, equivalent single-height resize and distinct-cell absolute-site relocation, deterministic per-primitive legalization and global returned geometry diffs. Oracle: whole-design GR/RC/OpenSTA for intermediate metrics; separate legality, logic equivalence, electrical and routing checks. An identical preregistered CTS-if-required / DR / extraction / timing suffix evaluates every reported incumbent including KEEP. Unsupported cases are UNKNOWN, not manufactured infeasibility or numeric penalties. Nine masks, 49 syntactic observation submasks, rescue cases and all-candidate policy denominator remain mandatory. No final-route feature enters a pre-action model.

Primary endpoint is complete charged time to an owner-defined legal/equivalent post-DR quality target; caps produce right-censoring. Also report best feasible effective-period versus total-cost frontier, WNS/TNS, estimated power, cell area, DRC, ERC, route failures, RAM, loading and reset costs. Thresholds await explicit pre-execution validation; legacy +0.02ns/2%/20% screening values are provisional, not measured gains or established demand.

## Embedded state-reset-contract.json, version EDA8-R2-RESET-1

The following source-only contract is part of these scientific bytes. Extract and hash it during EXP-002; extraction may add actual implementation hashes only through a new frozen revision and renewed phase consent. This is a specification, not an implemented adapter.

```json
{
  "contract_id":"EDA8-R2-RESET-1",
  "reference":"fresh executable process for every KEEP/A/B/AB/BA attempt",
  "process_rule":"exec a new pinned program image; never fork-only or reuse a live EDA instance",
  "canonical_inputs":["ODB/netlist/coordinates/masters","LEF/Liberty/SDC/RC/rows/sites/blockages","pinned tool and adapter binaries","initialization/operation/report scripts","allowlisted environment, seeds and thread count"],
  "mutable_disk_state":"unique per-attempt working directory; no shared mutable route/policy/feature cache",
  "prefix_rule":"both primitives in one branch process; first edit history and geometry intentionally persist to second",
  "between_branches":"discard process; reload canonical input for next attempt",
  "accepted_epoch":"serialize accepted physical output; initialize all next-epoch processes by the same procedure",
  "external_controller":"declared incumbent/history/candidate records may persist; engine initialization is arm-independent",
  "failure":"semantic FAIL terminates branch; crash/timeout/report absence is UNKNOWN; never reuse crashed process",
  "cost":["process creation","load/init","full initial recomputation","both primitives/legalization","reports","serialization","discard/failures","final-route suffix"],
  "status":"source-level design only; physical validation not performed"
}
```

| Decision-relevant state | Source observation / locator | Reference treatment and future oracle |
|---|---|---|
| ODB/netlist/masters/placement plus fixed geometry | Assigned checkpoint contract; not an implemented adapter | Hash canonical inputs; record all returned global diffs; check equivalence/legality. |
| Pending/committed per-instance move sets and journal stack | R04 raw 61-81,374-401,482-599,668-673 | Fresh program image; no assumption that undoEco erases policy history. Compare next decisions, not only ODB hash. |
| Process-static summary | R13 MoveCommitter.hh raw 159-160; R04 raw 605-616 | Fresh executable resets C++ static lifetime. Decision influence not established; mere object reconstruction is insufficient as a general reset proof. |
| STA/RC caches and ordering | R14 raw 5622-5637; R04 restoreJournal timing refresh | Rebuild via deterministic initialization; compare metrics under declared tolerances. Cache equivalence remains a preflight obligation. |
| Legalizer/router RNG, ties, threads, environment and mutable files | Adapter-specific paths unknown | Fixed seeds/threads/config plus isolated working directory; source call-path inventory remains EXP-002. Clean repeated replay must detect residual nondeterminism. |
| Shared model/arbiter state | Proposed outer algorithm | Same declared initial history, ties and cache allowance across arms; no untried branch labels fed to decisions. |

C-T01 future differential protocol: at a capped training checkpoint, enumerate identical KEEP/A/B/AB/BA clean runs in forward, reverse and seeded random schedule; repeat a branch after unrelated failed/rejected branches. Also compare a diagnostic same-process journal path if implemented. Save branch-order-isolation.csv with canonical hashes, process provenance, semantic outcomes, global diffs, reports, decisions and cost. Require clean-reference semantic/geometry equality and preregistered report tolerances. A clean-reference failure halts incidence. A journal-only mismatch rejects journal reuse as an optimization; no contaminated labels enter learning. No call-path completeness or deterministic execution is asserted by this design document.

## Embedded comparator-contract: explicit computational graphs and tensors

Numerical features are acquired at the initial checkpoint, identically for all arms. Every scalar includes an availability bit; unavailable values use a training-fixed imputation and cannot alter candidate enumeration. Metric normalization uses one training-only affine scale per output metric, common to AB/BA. Full schema is fixed now as a reviewable proposed interface; unsupported extraction blocks EXP-002B until a new reviewed contract, rather than silent input substitution.

State vector x_s: 12 numerical fields (WNS ns; TNS ns; router-declared GR overflow; cell area; die area; instance count; net count; max-slew violation count; max-capacitance violation count; available-site fraction; maximum row utilization; mean row utilization), followed by 12 availability bits, dimension 24. Require baseline WNS/overflow to invoke the residual core. Each typed action has 16 numerical fields plus 16 availability bits: initial x/y in site/row units; old master width sites; requested master width sites (unchanged for relocation); height rows; target x/y (initial x/y for resize); output slack ns; output slew ns; input capacitance; fanout count; summed load capacitance; mean load Manhattan distance; current row utilization; free sites in the fixed initial row window; initial Manhattan distance to nearest fixed blockage. The row-window radius is a hashed EXP-002 parameter fixed before labels; missing blockage means availability=0. Master equivalence and legal intent enumeration are guards, not learned categorical IDs. x_a and x_b each dimension 32. Raw local timing/geometry values and acquisition cost are shared; future returned geometry is label/diagnostic only.

Primary B5 core per state/pair:

    h_s = ReLU(W_s x_s + b_s), width 16
    h_a,i = ReLU(W_a [h_s,x_a,i] + b_a), width 16
    h_b,j = ReLU(W_b [h_s,x_b,j] + b_b), width 16
    for each metric k:
      [u_i,U_m,i,U_d,i]_k = A_k h_a,i + alpha_k
      [v_j,V_m,j,V_d,j]_k = B_k h_b,j + beta_k
      c_ij,k = q_s,k + u_i,k + v_j,k + U_m,i,k dot V_m,j,k
      d_ij,k = U_d,i,k dot V_d,j,k
      output = [c+d,c-d].

For r=1, W_s shape [16,24], W_a/W_b [16,48], each with bias [16]; A_k/B_k [3,16] with bias [3]. Two metrics give 2,172 active core parameters; gate/direct fallback and success heads are identical additional charged modules for every learned arm. For r=2, A_k/B_k [5,16], total 2,308. The per-action singleton output cannot consume its counterpart intent. Shared metric encoders are the only cross-metric sharing; separate encoders are a budgeted ablation. Cross-pair information can enter the common initial state, but cannot remove the explicit rank-r output constraint on a fixed candidate grid.

Use raw reconstructed loss on every eligible observed branch, plus identical singleton auxiliary MSE, identical success losses and L2 penalty on actual trainable tensors. The primary equal-data representation comparison uses only records with all numerical references observed; direct fallback regressors use exactly the same expanded availability records in all arms. Rank diagnostics require a resolved grid or explicitly missing-data analysis, never treating missing branches as zeros. The optional expanded-label experiment is separate and cannot masquerade as a same-data advantage. All learned gating/abstention is initial-feature-only and shared; it never deletes a candidate merely from predicted failure.

| Arm | Graph / parameters and interpretation |
|---|---|
| B0 | Strong pinned native repair/retry and incremental physical baseline inside a fresh iteration process; no disabled native optimization to manufacture gain. |
| B1/B2 | Fixed and adaptive serial greedy with refreshed proposals (extra cost charged); equal-total-cost two-order/beam lookahead. Shared process isolation rule. |
| B3-U | Same encoders; concatenate [h_s,h_a,h_b] (48), ReLU joint layer width H, linear four outputs (two metrics x two orders). Same per-action singleton auxiliary heads. H=32 primary (3,736 active parameters); H=2 (2,146, near parameter match), H=16 and GBDT are prespecified strong-frontier alternatives. Do not claim a win solely against H=2 when H=32/GBDT dominates. Same input/label/cost cap; active counts and compute differ and are disclosed. |
| B3-T | Take B3-U's identical latent theta, compute c=(t_AB+t_BA)/2,d=(t_AB-t_BA)/2 and reconstruct loss with full masked quadratic. Identity map on theta, same regularizer, optimizer state and batch order. Expected identical predictions/gradients/decisions to B3-U. |
| B3-M | Take B5's identical latent theta and products, expose raw two-order outputs directly, use identical objective/regularizer/optimizer. Tensor map is the identity, not a new fit. Must equal B5; no performance-gap hypothesis. |
| B-CD-U | Same B3-U joint graph but four outputs interpreted as c,d; same singleton auxiliaries, raw reconstruction loss and explicit actual-parameter L2. This is an unrestricted no-singleton-output factorization comparison. An invertible final-layer coordinate map exists; ordinary L2 and Adam in different coordinates need not preserve the objective/trajectory. Report that optimization/regularization difference; pushforward-equivalent version is an identity control, not novel evidence. |
| B-LR | Generic joint bilinear prediction without additive singleton output: c=U_c^T V_c and d=U_d^T V_d, with the same state/action encoders and singleton auxiliary heads. Test r and r+2 where budget allows; disclose rank/parameter differences and do not attribute them to residualization. An ordinary direct additive-plus-bilinear model with the exact same factors as B5 is already the B3-M identity control, not an opponent B5 must defeat. |
| B4 | Separate per-metric models plus validation-tuned fusion, under the same cost/trial frontier. |
| B6/B7 | Single repeated-call controller with identical information/invocations; central deterministic B5/arbiter with identical ties, which must match multi-specialist actions. No LLM calls are allocated. |

Primary tensor coefficients above are an explicit candidate, not a claim that small tabular inputs suffice. A fairness frontier includes trainable encoder widths 16/32 and the direct H choices within a shared <=100k-parameter upper cap, CPU only, three seeds and at most 12 validation configurations per architecture including gate/rank choices. Width/rank trial counts, early stopping and tuning cost are charged, not ignored because only one network is retained. No arm gets additional labels/features/rollouts. Match active-parameter comparisons separately from same-total-cost comparisons; different active counts are not falsely described as exact matches. Model architecture selection is validation-only; no exploratory test-set search. All actual CPU/RAM/elapsed caps remain missing and prevent execution.

## Current diagnostic and conventional-comparator lock

CLM-024 in proposal.md supplies the exact margin/regret definitions and their assumptions. Add the following immutable diagnostic schema to EXP-002 metric-contract.json: policy_version/hash; utility type (affine/nonlinear/lexicographic); physical scales and coefficients; observed feasible set; hard guard tolerances; tie tolerance and AB/BA/candidate tie order; repeat-noise and meaningful regret thresholds; stratification bins fixed using training data only. No coefficient or threshold is supplied here as an engineering fact; unresolved owner validation keeps EXP-000 closed.

For EXP-003/005's same complete grids, compute each rank-r reconstruction, absolute c/d errors, singular residual, pairwise order margin, exact/predicted ties, order flip, selected pair/order, ranking regret and utility regret over the common observed feasible set. Also record omitted/infeasible/UNKNOWN alternatives and whether the conditional oracle excludes them. The oracle-set diagnostic uses current outcome labels only offline, never inference input. Report flat and margin-stratified tables, including zero-margin and noise-scale strata; no post-hoc deletion, extra acquisition, zero imputation or test-family threshold fitting. Report maximum absolute error separately from Frobenius relative error. A finite table bound using observed errors does not certify unseen candidates. For guard-sensitive alternatives evaluate exact locked guard/policy outcomes; the scalar lemma does not certify guard membership. EXP-007 total-policy evaluation remains decisive (the task identifier is EXP-007).

B8-J is now a mandatory conventional-comparator resolution task before promotion. Its status is NOT IMPLEMENTED. EXP-001 records the original-method comparison in proposal.md; EXP-004 must pin a faithful available implementation or an explicitly delimited adaptation with actual objective, option set, placement-cost evaluator, oracle, ties, available information and full resource accounting. Identify which assumptions transfer and which do not. Its predictions use only initial deployable information; real checks and failed-branch charges follow every other arm. Report B8-J separately from the original algorithm; an unrealized or weak adaptation cannot establish improvement over it. EXP-000 still precedes any implementation run. If no strong reproducible joint-selection comparator is available within actual resources, novelty/feasibility stays unresolved rather than replacing it with an easy claimed win.

R20 pinned organizer baseline is a source-only reference for B0 inventory. Preserve native capabilities and report any necessary stage/tool adaptation. Its script is not the proposed per-edit legalizer or evidence that the clean branch adapter exists. Use its raw physical lines and named commands, never web UI line numbers as raw code lines.

## Analytic restriction and possible failure

For fixed state, M=U_m V_m^T and D=U_d V_d^T have rank <=r. I_3 has determinant one and therefore cannot equal rank<=2 D; a three-ReLU triangular function of scalar action-feature differences represents it in the unrestricted direct head (proposal.md). This abstract witness is independent of training algorithm and does not establish physical reachability. For K=4 the primary r=1 output factors generate 24 scalars (eight singleton plus sixteen interaction factors) versus 32 unconstrained ordered outputs per metric. r=2 generates 40, so there is no universal output-count or parameter advantage. These are generated-array counts, not fitted parameter dimensions or a sample-complexity theorem. Matrix factors are nonidentifiable up to scaling/change of basis; interpret predictions/rank, not individual factors as physical causes.

The restriction is useful only if real legalization/order interactions share predictable structure at a decision-relevant scale, and savings beat labels/training/clean-start/suffix overhead. It can fail on highly local unrelated conflict pairs that produce a high-rank contrast matrix, on negative transfer, or when direct models already learn it. Before training, allocated EXP-003 (2x2 primary-rank screen) and EXP-005 (>=3x3 sensitivity screen) examine resolved contrast matrices against repeat-noise and prespecified rank residual and the locked margin/tie/flip/regret diagnostics. A rank statistic alone is neither a kill rule nor a downstream utility proof; apply preregistered noise/economic and downstream criteria. A failed low-rank prior cannot be rescued under this ID by adding unrestricted joint heads and calling them the same mechanism. Candidate rank=2 is the only preregistered sensitivity; further mechanism changes require a new reviewed direction or successor.

## Data generation, denominators and cost

A public historical result archive was retrieved solely for source inspection; no experimental input dataset is rights-locked and no flow is run. Future rights-audited six-family candidate pilot: split 3 train/1 validation/2 test by underlying RTL/design family before checkpoint generation, two checkpoints each. Variants/seeds stay together. K<=4+4 gives at most 41 unique KEEP/single/order outcomes and 72 primitive applications per checkpoint, hence 492 outcomes and 864 primitives across twelve checkpoints before repeat/failure/censoring/final suffix allowance. Clean-process replay recomputes prefixes; no invalid shared-prefix reuse reduces billed cost. Incidence begins at <=2 training checkpoints, K=2+2, <=13 unique outcomes each before separately capped repeats. Exact process count, load/report/repeat/censor caps must be frozen in each gate. No hidden/public benchmark or LLM pretraining contamination assurance is available.

Training/feature acquisition/gating, proposal/communication/tokens if later allocated, process startup/loading, canonicalization, all failed/rejected branches, suffix and fallback enter cold and amortized costs. C setup cost and delta per-decision savings imply break-even N>C/delta only for measured delta>0. No magnitude/probability forecast exists. Two held-out families support only feasibility screening, not population-wide significance.

## Decisive tests and stop rules

1. Retain all nine masks, partial UNKNOWN, per-metric availability, rescue and all-pair denominators.
2. EXP-002B must pass clean-process identity/noise and adapter/oracle checks before physical incidence. Any unexplained state dependence halts.
3. Test r=1/r=2 versus strong direct and generic low-rank alternatives; include zero/shuffled d, no-singleton-output, separate/shared metric encoders, disjoint-support controls and learning curves.
4. B3-T/B3-M/B7 equivalents must match numerical/gradient/decision tolerances fixed before training. Mismatch is a software/fairness failure.
5. Report total-policy value, complete-only error, success yield, gate/fallback error, missed rescues and censored failures. Better complete-only RMSE is insufficient.
6. Final-route reversals, native/direct/lookahead/applicable-conventional domination or nonpositive full-cost savings reject the utility claim. Do not add agents, labels, unbounded rank or larger budgets to conceal failure.
7. Independently audit exact original winner/full-method scope before promotion. Missing resources or unresolved novelty permits a conditional hypothesis, not an experiment-ready declaration or forced abandonment.
