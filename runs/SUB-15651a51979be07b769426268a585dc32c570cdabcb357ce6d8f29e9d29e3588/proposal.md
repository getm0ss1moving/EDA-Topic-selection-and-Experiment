# EDA-0008: Order-sensitive resize/relocation prediction, revision 2

Batch 0003, D04 cycle 2/4. Research disposition: **revise; conditional hypothesis, not experiment ready**. This revision preserves the released EDA-0008 anchor, incorporates the current adjudicated OBJ-101/C-T01/C-T02, and independently obtains the previously unavailable R09 full paper. Historical contract repairs remain explicitly retained. Historical judgments concern historical bytes, not independent approval of this revision. No chip-tool build, EDA run or training is performed.

## Engineering problem and frozen boundary

A physical implementation engineer at a legal post-detailed-placement, pre-CTS, ideal-clock, single-PVT checkpoint must select KEEP, a singleton, or one order of a proposed width-changing resize and a distinct-cell relocation. Each edit includes deterministic incremental legalization; the first edit can change the geometry and feasibility of the second. The endpoint remains legal, equivalent, routable post-detailed-route quality per complete iteration cost. Narrow effect prevalence and economic importance remain unmeasured (CLM-010), despite general co-optimization demand. No hold, multi-corner, IR-aware or foundry-signoff guarantee is added.

Define state s by hashed ODB/netlist, all coordinates/masters, rows/sites, fixed objects, blockages, Liberty/LEF/SDC, RC model, tool/config versions, seeds and threads. Current whole-design GR/STA information is charged and available before decisions. Each branch now starts with a new executable process from the same immutable canonical checkpoint and initialization protocol; s includes that process-initialization contract. Intra-branch policy history after the first edit is intentionally part of the transition. Between-branch history is excluded. See the process-isolation contract below. The timing specialist emits at most K=4 resize intents a=(instance,new_master); the congestion specialist emits at most K=4 relocation intents b=(different_instance,absolute_target_site). Single-height, equivalent masters and supported orientations only. Intents are frozen at s. They are never regenerated inside a paired branch. Width changes apply at the branch's current location. Actual returned geometry changes to every instance, including unintended neighbors, are logged globally. A serial adaptive baseline may regenerate after each action, with its full extra cost reported separately.

T_a and T_b return a legal equivalent state or semantic FAIL. Prefix failure stops that order and discards its process; applying the other first in a separate clean process may still rescue the failed singleton. No shared-process rollback is used as the causal reference. An algorithmic time limit, unavailable report or process crash is UNKNOWN/censored, never proof of physical infeasibility. Tool-accepted results remain relative to the pinned oracle, not manufacturing signoff.

## Success, observability and numerical target contract: repair of OBJ-001

Let M=(A,B,AB,BA), where A and B denote successful singleton transitions, AB denotes T_b(T_a(s)), BA denotes T_a(T_b(s)). For deterministically resolved transitions AB<=A and BA<=B. The complete syntactic mask universe is below. It is not an assertion that every mask occurs in OpenROAD. Physical adapter invariants may eliminate masks only with recorded proof, never by deleting observations.

| M | Available successful final states | Numerical treatment and fallback |
|---|---|---|
| 0000 | KEEP | Classify resolved semantic failures; retain KEEP. |
| 0100 | b | b regression only; orders are failed. |
| 0101 | b, ba | Rescued resize: ba has its own outcome target; no singleton-a target. |
| 1000 | a | a regression only. |
| 1010 | a, ab | Rescued relocation: ab has its own outcome target; no singleton-b target. |
| 1100 | a,b | Singleton targets only; both orders failed. |
| 1101 | a,b,ba | ba direct branch target; no invented two-order contrast. |
| 1110 | a,b,ab | ab direct branch target; no invented two-order contrast. |
| 1111 | a,b,ab,ba | Common/contrast targets if both order metrics observed; singleton residual targets only if all required metrics observed. |

For each metric k independently define O_jk=1 only if the transition succeeded and a finite metric report exists. Thus O_jk<=M_j; baseline O_sk is also required for changes. There are 49 binary observation submasks for a fully resolved M across this syntactic universe for one metric; UNKNOWN transition bits are retained as partial observations, not assigned a nine-class label. This enumeration is an own analytic check, not observed physical incidence (CLM-016).

q=[WNS in ns, total GR overflow in the locked router's declared units]. WNS is maximized, overflow minimized. On complete observed labels define u_a=q_a-q_s, u_b=q_b-q_s, z=q_s+u_a+u_b, m=(q_ab+q_ba)/2-z, d=(q_ab-q_ba)/2. Reconstruct qhat_ab=zhat+mhat+dhat and qhat_ba=zhat+mhat-dhat, with zhat=q_s+uhat_a+uhat_b at deployment. All terms are metric vectors. d needs neither singleton label; c=(q_ab+q_ba)/2 and d exist when the final two reports exist, even if a singleton report is missing. m requires its full singleton reference. No FAIL, UNKNOWN or NaN is replaced by a fabricated numerical penalty label.

Use categorical prefix/conditional-transition heads p(A),p(B),p(B succeeds|a succeeded),p(A succeeds|b succeeded), or a nine-class mask model when a full mask is resolved. Conditional labels exist only on successful prefixes; unresolved executions are masked. Shared direct branch regressors learn every observed successful order, including rescue cases. They are the common fallback for every learned comparator. The candidate list always includes both orders, singletons and KEEP; predicted failure never deletes an order. A validation-fixed confidence gate chooses the residual predictor versus the shared direct fallback using initial-state features only. Its labels, architecture, validation tuning, abstention policy and cost are identical across comparisons. No numerical residual prediction is used outside its trained domain without falling back. This gating is empirical; misclassification costs and lost rescue opportunities must be reported.

Primary representation comparisons use the identical complete-record subset and identical raw labels in every arm. A separately reported availability ablation may expand c,d/direct training to additional both-order-observed records; it cannot be presented as a representation advantage from equal data. Every observed singleton supplies identical auxiliary supervision in all matched arms. The total-policy denominator is all frozen candidate pairs, including failure, rescue and censoring strata. Report per-mask counts, total attempted branches, failures/censoring, complete-stratum utility, overall utility and number/value of successful branches skipped by the budget or gate. Conditional regression error alone cannot demonstrate overall benefit.

## Transformed loss and actual proposed delta: repair of OBJ-002

For one normalized metric write e_c=chat-c, e_d=dhat-d, e_ab=e_c+e_d, e_ba=e_c-e_d. With nonnegative observable-branch weights w_ab,w_ba,

    L_order = w_ab(e_c+e_d)^2 + w_ba(e_c-e_d)^2
            = (w_ab+w_ba)(e_c^2+e_d^2) + 2(w_ab-w_ba)e_c e_d.

For equal two-success weights this is 2w(e_c^2+e_d^2). A mixed-success mask requires the cross term; treating it as diagonal contrast loss fabricates equivalence. For residual reconstruction e_c=(zhat-z)+(mhat-m). Merely penalizing mhat-m and dhat-d omits shared singleton error and generally changes the objective. Reconstruction loss is the primary loss, including derivative flow through zhat. Both facts were checked in a 500-case, 2,000 masked-loss own numerical algebra test, including gradients (CLM-017); no model was trained.

Normalize each physical metric once with a fixed training-only affine transform applied identically to both order outputs. Do not independently standardize c,m,d and call the result equivalent. Branch weights, complete/subset masks, singleton auxiliaries, failure losses, regularization, validation search, optimizer, minibatch ordering, seed and early stopping are fixed per comparison. Exact transformed control B3-T reuses the same latent parameters, output map, initialization, regularizer R(theta), data batches and optimizer state as the direct model. Its loss uses the full quadratic above, so predictions, gradients and decisions must agree to numerical tolerance. A failed identity check is a software defect, not a scientific win.

## Concrete parameter constraint: C-T02 repair and CLM-018/020

An unconstrained symmetrized residual network may be exactly a direct predictor. Revision 2 therefore tests a declared restricted instance of the existing residual mechanism, not a new coordinate system. For each metric and frozen resize candidate i / relocation candidate j define

    z_ij = q_s + u(s,a_i) + v(s,b_j)
    m_ij = U_m(s,a_i)^T V_m(s,b_j)
    d_ij = U_d(s,a_i)^T V_d(s,b_j)
    qhat_AB,ij = z_ij + m_ij + d_ij
    qhat_BA,ij = z_ij + m_ij - d_ij.

Primary factor rank r=1; r=2 is a prespecified sensitivity, never an automatic rescue. Each factor sees initial-state and its own typed intent only; no joint pair head, pair identifier memorization, outcome feature or cross-attention bypass. The shared state encoder is independent of order and pair index. Reversing the query exchanges output slots; typed resize/relocation roles remain fixed. WNS and overflow share the feature encoders but have separate outputs; separate encoders are an ablation. Success-mask, gate and direct fallback contracts above remain unchanged. Rank statements concern the B5 numerical core on a fixed candidate grid, not the mixed gated policy.

This is a falsifiable low-rank interaction prior: matrices M=[m_ij] and D=[d_ij] have rank at most r, while the additive singleton matrix is not forced to rank r. For a 3x3 grid, D=I_3 is an explicit counterexample to r<=2. A direct ReLU joint head can represent that abstract table with scalar action features x_i=i,y_j=j: d_ij=ReLU(x_i-y_j+1)-2ReLU(x_i-y_j)+ReLU(x_i-y_j-1). The rank-restricted core cannot. This is an abstract representability witness, not a claim that a physical checkpoint realizes I_3. Thus the restriction is identifiable, and it can be harmful. This own algebraic witness (CLM-020), not a physical observation, was checked without training. There is no reason yet to assume physical interaction matrices have low rank.

B3-M is the identical B5 graph expressed as direct branch outputs, with theta unchanged, the same raw reconstruction loss, regularizer and optimizer state. It must match B5; beating it is not an expected result. B3-T similarly remains the exact transformed B3 graph. A direct model imposing the same additive-plus-low-rank structure is an ordinary equivalent implementation, not independent evidence of representational novelty. Strong unrestricted direct prediction, generic low-rank direct modelling and B-CD controls are all required. Any useful contribution must be an evidenced EDA-specific information/cost/reliability tradeoff of this restriction under the full failure-aware policy, beyond these conventional alternatives. No new expressivity, lower sample complexity or original low-rank mathematics is claimed.

The exact proposed tensor graphs, budget frontier, masking and falsification rules are in experiment-plan.md. The new own 500-vector/2,000-weight-case check verifies reconstructed/transformed objective and analytic gradients, query swap, and rank witnesses; its largest loss discrepancy is 4.263256414560601e-14, analytic-gradient discrepancy 7.105427357601002e-15, finite-difference error 2.592404513279689e-09. These are scalar checker outputs, not trained-model identity validation, accuracy or EDA measurements.

## Process-isolated branch reference: OBJ-101 repair and CLM-019

Independently reopened R04 confirms retained accepted-instance history across rejected journals; R13 additionally declares a process-static summary. R14 exposes journal reinitialization and timing refresh but is not a proof of complete decision-state reset. Therefore a database hash or reconstructed Resizer object does not certify a clean branch. No broad OpenROAD bug claim is made: relevance to an adapter remains conditional.

The causal reference is now a fresh executable process per KEEP, singleton and ordered branch, loading identical canonical physical inputs, scripts, environment allowlist, tool/adapter binary hashes, seeds and thread count. A child must execute a fresh program image; fork-only reuse of live EDA memory and warmed mutable disk caches is forbidden. Both edits of an order run in that one process so genuine within-order state/geometry effects remain. Every return discards the process; selected physical output is serialized as the next epoch's checkpoint and all arms use the same canonical reload protocol. Models/arbiter retain declared decision history in the outer controller; it cannot alter engine initialization per arm. No adapter or process replay was executed here.

Source-only state inventory and exact process contract are embedded in experiment-plan.md for extraction into state-reset-contract.json. A future allocated preflight compares repeated clean branches under reversed/random prior visitation and shared-journal diagnostics, measuring decisions, feasibility, global geometry and reports. Any unexplained clean-reference difference fails preflight; a journal mismatch disqualifies that acceleration rather than becoming physical order evidence. Startup, loading, recomputation, serialization and discarded branches are charged to every arm. Native B0 retains its ordinary internal repair/retry capabilities inside its own fresh iteration process. This repairs the causal specification; runtime validation and the economics of losing journal reuse remain unresolved.

## Closest approaches and contribution boundary

R01 HyPAS, PDF pp.2-3 sections 2.2 and 3.1-3.4, is the closest co-optimization comparator: discrete physical repair and differentiable refinement with width-group safeguards and learned timing/power. R02 RL-LR, Introduction and section 3.2, already learns gate order/choice with incremental timing in a later IR-aware sizing setting. R03 AgenticPD v3, section section 3.1-3.4, already manages retained stage branches and history. R04 pinned OpenROAD MoveCommitter methods already provide nested reversible ECO journals and timing refresh. R05 ResizerAgent README specifies post-CTS feedback-driven sequence/fix plans. These are distinct comparison scopes; none of their reported gains is reproduced or transferred here. See prior-art.csv for actionable overlap and access limits.

R06 official ICCAD2025 Problem C directly covers sizing, buffering and relocation, so those operators and generic coordinated search are supplied context. R07 ISPD2026 formulation (PDF p.6 hard constraints, not just pp.2-3) imposes tighter physical constraints, including freezing cells not resized; it is not an unrestricted distinct-cell relocation benchmark. Its section 5.3 roadmap is future planning, not an already implemented 2027 feature set. R08 lists IRISLab/PTSD/HLFC winners; their original methods remain uninspected. R09 is now full-method accessible through its author's ordinary public session/download links. Its Algorithm 1 uses timing then power phases; sections 3.2-3.4 specify slack-partitioned GCN/PPO agents and sizing/VT/buffering actions, rather than the proposed fixed resize/relocation order-contrast predictor. Section 5 lists movement as future work. This narrows that particular overlap; it does not establish broad novelty. Its proprietary tool/technology setup is not available here. R15 FlowSynth is an older conventional simultaneous-transform/min-cost-flow lead with indexed abstract only. R18 independently retrieves the original Top-3 result archive: its 78 files are only DEF and ECO changelists, not method reports or code. Methodological winner coverage therefore remains unresolved, even though archive access is now resolved. Exact duplication and contest originality therefore remain open (CLM-014), not established absent. These are source gaps, not proof against the hypothesis.

## Hypothesis, decisions and falsification

H1/CLM-009: with equal complete costs, labels, deployable information and frozen candidates, B5's specified rank-restricted residual sharing improves useful checked sequence selection over B0 native repair, B1 adaptive serial greedy, B2 equal-cost lookahead, B3 strong direct/symmetry-matched prediction, the non-equivalent generic low-rank baseline and B-CD common/contrast without singleton output factorization. B3-T must match B3; B3-M, including the ordinary direct implementation of the same additive/bilinear graph, must match B5. These are identity controls and H1 never requires beating them. Test the common gate/fallback without counting it as novelty. H1 may fail because order effects are rare, residualization amplifies error, direct models learn the same function, or label/training costs erase savings.

Two algorithmic specialists exchange version-bound candidate IDs and predictions; a deterministic arbiter serializes database edits, tries budgeted branches, and accepts only whole-design checked improvements. One central controller with the same model and ties must produce the same actions (B7). Separate B6 gives a single repeated-call controller equal observations, tools, history and invocation allowance. No claim that multiple LLMs are necessary is made. All proposal, token, communication, rollback, fallback, model and final-route costs are charged; no agent is launched in this job.

Potential headroom is unquantified. A zero/noise-level order contrast or a dominating direct/lookahead baseline kills the proposed representation claim. No applicable global-optimum bound or saturation proof has been found. Let setup overhead C include labels/training and delta be per-decision saved cost at equal feasible quality; break-even requires delta>0 and N>C/delta. This is accounting, not a forecast. Final-route quality and owner-validated meaningful thresholds are unresolved; post-GR accuracy is diagnostic.

## Claim continuity and current disposition

| Claim | Status in revision 2 | Evidence and scope |
|---|---|---|
| CLM-001/002 | Historical contextual claims not relied on here | Old ChatEDA/EDAid readings not rechecked; generic orchestration novelty not asserted. |
| CLM-003/004/005/006 | Source observations, limited selected methods | R03/R04/R01/R02 as mapped above. |
| CLM-007 | General coupled physical need supported, narrow demand unresolved | R06/R07; no industrial prevalence estimate. |
| CLM-008 | Historical six-site toy only | Released predecessor witness; not rerun or inherited as physical evidence. |
| CLM-009/010 | Conditional hypothesis/inference | Analytic consistency repaired; all physical/learning gains unknown. |
| CLM-011 | Unused historical dataset lead | No CircuitNet action-order data claimed or acquired. |
| CLM-012 | Advertised public capability only | R11; no comparative vendor shortfall. |
| CLM-013 | Conditional algebraic equivalence | Transformed loss above, with masks and singleton-error qualifications. |
| CLM-014 | Partly advanced, still unresolved novelty/contest overlap | R09 full method now inspected; R06/R08 original winner reports still need full audit; R15 conventional lead. |
| CLM-015 | No new experiment authorization | JOB.json and policy/docs/INNOVATION-BATCH-0003.md. |
| CLM-016/017 | Own analytic enumeration/loss checks | Reproducible code and exact output in search-log.md. |
| CLM-018 | Narrowed candidate contribution | Rank-restricted residual sharing versus strong direct/conventional alternatives; no original low-rank algorithm claimed. |
| CLM-019 | Source observation plus reference-process design | R04/R13/R14; no empirical restore claim. |
| CLM-020 | Own algebraic restriction/witness | Rank-r factorization cannot represent I_3 contrast for r<=2; no physical low-rank claim. |
| CLM-021 | New original-method source observation | R09 PDF pp.3-6 and p.8; selected method mapping, not reproduced results. |
| CLM-022 | New official source payload observation | R18 archive directory: 78 output files, not reports or implementation methods. |

Zero combination and demand drift: process isolation and explicit residual factorization are repairs of the same physical interaction mechanism. The low-rank assumption is a new explicit falsifiable restriction within the retained mechanism, not an established physical fact. Do not silently pivot to generic tuning or HPWL. The revised pre-execution gate is EXP-000; every future build/baseline/incidence/training/full-flow task depends on it. Current consents are pending; rights/resources/environment/adapter/oracle/thresholds and remaining original-method gaps prevent pilot promotion. No independent approval of revision 2 is claimed. Research revision is complete as a file deliverable, while scientific gates remain unresolved. Independent challenge and verification must assess these new bytes.
