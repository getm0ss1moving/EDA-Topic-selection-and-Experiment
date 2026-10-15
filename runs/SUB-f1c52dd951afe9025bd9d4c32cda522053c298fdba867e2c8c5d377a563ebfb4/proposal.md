# EDA-0008: Order-sensitive resize/relocation prediction, revision 1

Batch 0003, D04 cycle 1/4. Research disposition: **revise; conditional hypothesis, not experiment ready**. This revision preserves the released EDA-0008 anchor and repairs the adjudicated predecessor's three contract defects. Historical judgments concern historical bytes, not independent approval of this revision. No chip-tool build, EDA run or training is performed.

## Engineering problem and frozen boundary

A physical implementation engineer at a legal post-detailed-placement, pre-CTS, ideal-clock, single-PVT checkpoint must select KEEP, a singleton, or one order of a proposed width-changing resize and a distinct-cell relocation. Each edit includes deterministic incremental legalization; the first edit can change the geometry and feasibility of the second. The endpoint remains legal, equivalent, routable post-detailed-route quality per complete iteration cost. Narrow effect prevalence and economic importance remain unmeasured (CLM-010), despite general co-optimization demand. No hold, multi-corner, IR-aware or foundry-signoff guarantee is added.

Define state s by hashed ODB/netlist, all coordinates/masters, rows/sites, fixed objects, blockages, Liberty/LEF/SDC, RC model, tool/config versions, seeds and threads. Current whole-design GR/STA information is charged and available before decisions. The timing specialist emits at most K=4 resize intents a=(instance,new_master); the congestion specialist emits at most K=4 relocation intents b=(different_instance,absolute_target_site). Single-height, equivalent masters and supported orientations only. Intents are frozen at s. They are never regenerated inside a paired branch. Width changes apply at the branch's current location. Actual returned geometry changes to every instance, including unintended neighbors, are logged globally. A serial adaptive baseline may regenerate after each action, with its full extra cost reported separately.

T_a and T_b return a legal equivalent state or semantic FAIL. Prefix failure stops that order and restores s; applying the other first may still rescue the failed singleton. An algorithmic time limit, unavailable report or process crash is UNKNOWN/censored, never proof of physical infeasibility. Tool-accepted results remain relative to the pinned oracle, not manufacturing signoff.

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

The candidate B5 differs only in its explicit shared singleton/common-residual representation and exchange symmetry: g_m(s,a,b)=(h(s,a,b)+h(s,b,a))/2; g_d(s,a,b)=(k(s,a,b)-k(s,b,a))/2 under an order-query swap that retains typed intents. Swapping the query reverses order, not the physical edit types. Both successful branch outputs must exchange. A shared trunk across WNS/overflow is optional and ablated against separate heads plus fusion. B3 gets the same swap augmentation and an explicit symmetry-matched direct control. B5 is not guaranteed a smaller target, a better hypothesis class or lower sample complexity. If a direct symmetry-matched predictor is the identical function class and objective, the distinction may disappear entirely. A useful systems result would have to identify a finite-data sharing/conditioning or cost/reliability tradeoff beyond strong matched alternatives, then demonstrate downstream value. A theorem or super-additive gain is not required; a coordinate rename is insufficient (CLM-013/018).

## Closest approaches and contribution boundary

R01 HyPAS, section section 2.2 and 3.1-3.4, is the closest co-optimization comparator: discrete physical repair and differentiable refinement with width-group safeguards and learned timing/power. R02 RL-LR, Introduction and section 3.2, already learns gate order/choice with incremental timing in a later IR-aware sizing setting. R03 AgenticPD v3, section section 3.1-3.4, already manages retained stage branches and history. R04 pinned OpenROAD MoveCommitter methods already provide nested reversible ECO journals and timing refresh. R05 ResizerAgent README specifies post-CTS feedback-driven sequence/fix plans. These are distinct comparison scopes; none of their reported gains is reproduced or transferred here. See prior-art.csv for actionable overlap and access limits.

R06 official ICCAD2025 Problem C directly covers sizing, buffering and relocation, so those operators and generic coordinated search are supplied context. R07 ISPD2026 formulation imposes tighter physical constraints, including freezing cells not resized; it is not an unrestricted distinct-cell relocation benchmark. Its section 5.3 roadmap is future planning, not an already implemented 2027 feature set. R08 lists IRISLab/PTSD/HLFC winners; their original methods remain uninspected. R09's full 2024 multi-agent post-place method remains inaccessible through attempted lawful routes. Exact duplication and contest originality therefore remain open (CLM-014), not established absent. These are source gaps, not proof against the hypothesis.

## Hypothesis, decisions and falsification

H1/CLM-009: with equal complete costs, labels, deployable information and frozen candidates, B5's specific finite-data structure improves useful checked sequence selection over B0 native repair, B1 adaptive serial greedy, B2 equal-cost lookahead, B3 strong direct/symmetry-matched prediction, B3-T exact transformed identity, and B-CD common/contrast without singleton residualization. Test the common gate/fallback without counting it as novelty. H1 may fail because order effects are rare, residualization amplifies error, direct models learn the same function, or label/training costs erase savings.

Two algorithmic specialists exchange version-bound candidate IDs and predictions; a deterministic arbiter serializes database edits, tries budgeted branches, and accepts only whole-design checked improvements. One central controller with the same model and ties must produce the same actions (B7). Separate B6 gives a single repeated-call controller equal observations, tools, history and invocation allowance. No claim that multiple LLMs are necessary is made. All proposal, token, communication, rollback, fallback, model and final-route costs are charged; no agent is launched in this job.

Potential headroom is unquantified. A zero/noise-level order contrast or a dominating direct/lookahead baseline kills the proposed representation claim. No applicable global-optimum bound or saturation proof has been found. Let setup overhead C include labels/training and delta be per-decision saved cost at equal feasible quality; break-even requires delta>0 and N>C/delta. This is accounting, not a forecast. Final-route quality and owner-validated meaningful thresholds are unresolved; post-GR accuracy is diagnostic.

## Claim continuity and current disposition

| Claim | Status in revision 1 | Evidence and scope |
|---|---|---|
| CLM-001/002 | Historical contextual claims not relied on here | Old ChatEDA/EDAid readings not rechecked; generic orchestration novelty not asserted. |
| CLM-003/004/005/006 | Source observations, limited selected methods | R03/R04/R01/R02 as mapped above. |
| CLM-007 | General coupled physical need supported, narrow demand unresolved | R06/R07; no industrial prevalence estimate. |
| CLM-008 | Historical six-site toy only | Released predecessor witness; not rerun or inherited as physical evidence. |
| CLM-009/010 | Conditional hypothesis/inference | Analytic consistency repaired; all physical/learning gains unknown. |
| CLM-011 | Unused historical dataset lead | No CircuitNet action-order data claimed or acquired. |
| CLM-012 | Advertised public capability only | R11; no comparative vendor shortfall. |
| CLM-013 | Conditional algebraic equivalence | Transformed loss above, with masks and singleton-error qualifications. |
| CLM-014 | Unresolved novelty/contest overlap | R06/R08/R09 and EXP-001. |
| CLM-015 | No new experiment authorization | JOB.json and policy/docs/INNOVATION-BATCH-0003.md. |
| CLM-016/017 | Own analytic enumeration/loss checks | Reproducible code and exact output in search-log.md. |
| CLM-018 | Explicit remaining candidate contribution | Sharing/conditioning utility remains a testable hypothesis, not demonstrated novelty. |

Zero combination and demand drift: branch support and attribution are repairs of the same physical interaction mechanism. Do not silently pivot to generic tuning or HPWL. The revised pre-execution gate is EXP-000; every future build/baseline/incidence/training/full-flow task depends on it. Current consents are pending; rights/resources/environment/adapter/oracle/thresholds and nearest-method gaps prevent pilot promotion. Research revision is complete as a file deliverable, while scientific gates remain unresolved. Independent challenge and verification must assess these new bytes.
