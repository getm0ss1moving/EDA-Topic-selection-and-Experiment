# EDA-0006 — Compressed execution of mutually exclusive ECO timing candidates

R3 / batch 0002 cycle 3. **Recommend parking after this completed bounded witness pass.** A conditional systems hypothesis remains possible, but neither a useful delta over faithful adapted B++ nor a defensible requirement for the frozen full-vector output has been established. This is not rejection by universal duplication, theoretical saturation, joint abandonment, experiment consent, or independent verification of R3.

Author ChatGPT-P05-TIMING-EDA-0006; logical session 53d6f5d7-1d68-4d5a-a081-2a7df44a34b0. Input commit f68c1492c05be3fac5622deac4bb479eabf957de, packet 0a344dc225723839dc6a224d16376f44459179b3b83746986b2c1253a8dd1466. Previous proposer SUB-a18df7c82355639157174a8f957f294a4dabd4f66f741c76001694948aed326c; current released verifier SUB-91607fe56d889209b6e7be4232bb7993e669dba37c9435c995712d22b4a249e2 adjudicates challenger SUB-de19f2a38b3e2fcbf5d5b7871f119e8bf7b869b7568889c777cc45228e942c91. Source cutoff 2026-10-15 UTC; review is unblinded. R3 supersedes R2's next-step status, not its retained negative evidence.

## Problem, user, scope and oracle

The frozen user is a timing-optimization developer scoring a fixed ordered set of mutually exclusive, function-preserving, same-footprint cell-sizing alternatives from one immutable base checkpoint. Preserve the exact scalar per-candidate endpoint setup-slack vector, violating-endpoint set, WNS/TNS and deterministic caller choice, and reduce fully charged iteration cost. One fixed library/parasitic/constraint scenario, fixed acyclic topology and extracted wire topology, NLDM and ideal clocks define the initial slice. Pin-cap changes and predecessor-load effects must propagate. Fixed wires do not imply fixed electrical loads. MCMM, hold, SI iteration, CPPR, generated-clock changes, path exceptions, latches and topology edits are outside this initial adapter and require reference handling. No foundry-signoff or globally optimal PPA claim follows.

Oracle: same pinned scalar engine, kernels, build/FP behavior, operation order, timing tags, candidates, tie order and output contract. Full output bytes and caller decision must match independent scalar replay. Hashes index full equality only. No compatible executable adapter, full read-set audit or EDA measurement exists. Modern frequency and engineering value of this exact slice remain unknown. A complete vector may be useful as an offline validation oracle without being a justified deployment output requirement.

## Mechanism and conditional hypothesis retained

For operation q and candidate c, I_q(c) is the operation-specific complete record of every observable input, including versions/immutable closure, local overlay and load, ordered predecessor states actually read, timing context, arithmetic environment and tie information. Fields irrelevant to q need not be copied into every record; all fields it reads must be accounted for. Partition candidates into disjoint masks covering the supported universe. Intersect predecessor and overlay masks, evaluate each distinct complete record with the original scalar kernel, then union masks only for byte-identical full outputs. Sparse unchanged state references the base. Keep dirty status until dependent work is resolved. Unsupported or capped lanes are removed from partial state and replay the ORIGINAL alternative from the base; charge preparation, cleanup, replay, reports and guard checks.

Conditional induction: identical source states, complete deterministic kernels and correct disjoint intersections yield the same input/output for each lane at every DAG operation, hence the same endpoint results and ordered choice. This is an abstract lemma, not executable exactness: hidden mutable state, FP/NaN/signed-zero behavior, interpolation closure, version invalidation and rollback remain audit obligations. Neither Java equality nor const-qualified C++ establishes these premises.

A useful contribution with known components is eligible: a required capability or measured/justified cost/reliability tradeoff can suffice without a new theorem or super-additivity. The conditional hypothesis is that an EDA adapter could provide such a delta under this unchanged contract. R3 identifies no positive witness for it. An implementation task alone cannot turn that possibility into readiness or novelty.

## Closest systems and source-reopened boundaries

S20 §2.1 and S21 raw117–192 provide conditional values, lifted operations and context combination; S05 Fig.7 supplies timing input matching/cache reuse. Their finite-context specialization, with exact equality and appropriate recovery, is B++. S01 remains historical transactional-STA context; its R3 web retrieval failed and its old inspection is not relabeled fresh access. R2's classical, GPU/incremental, unified-prediction and cooperating-agent map is retained in prior-art.csv with access history; no broad clearance is claimed.

B++ receives the same EDA read-set adapter, bitsets, information, memory, sparse base, cache policy, task order, full-output comparison and recovery policy. The R2 constructive reduction (CLM-609) is retained: each (mask,state) is a (value,finite-context) pair; matching intersections and scalar calls produce identical subsequent partitions. Generic scheduler/key/copy novelty over a per-lane-only comparator was withdrawn in R2 and stays withdrawn.

### EXP-000R completed: concrete read/operation/lifetime audit (CLM-611)

New S27 pins one real kernel slice: OpenSTA `GateTableModel::gateDelay` raw113–130, `findValue`273–325 and `TableModel::findValue/scaleFactor`833–853. The observed dependency closure includes model/cell state and PVT scaling as well as numeric slew/load. This is a selected call-chain audit, not transitive purity certification. Reusing records solely from numeric slew/load is unjustified. The remaining library-scale and table-interpolation callees are unaudited.

| Operation or lifetime obligation | Proposed mask adapter | Faithful EDA-adapted B++ | Distinguishing witness found? |
|---|---|---|---|
| Resolve model/cell/PVT/scale closure and candidate load | Audit/version immutable closure; invalidate changed dependencies | Same adapter procedure and information | No; source exposes common required work |
| Gather representative record after dependency intersections | Once per nonempty input class | Once per same finite-context class | No; not K per-lane gathers on only one side |
| Complete-key cache lookup, scalar call and output equality | Same bytes/keys/cap and original scalar operation | Same bytes/keys/cap and operation | No; equality is an obligation, not an extra capability |
| Retain base and sparse changed records until last consumer | Same last-use schedule, immutable handles and interning | Same last-use schedule and handles | No; a compiler/runtime difference could matter, but none is measured or required here |
| Version change, cap/unsupported lane and exception | Invalidate or remove partial lanes; replay original input; charge cleanup | Identical policies and charged work | No; unmodified Java exception semantics are not the comparator |
| Reporting and caller reduction | Exact frozen reports and stable ordered choice | Same reports and stable ordered choice | No; materialize on both sides if actually required |

For q let a_q be nonempty intersections, b_q total representative record bytes gathered, l_q lookups, k_q misses, u_q equality/union events, and z_q peak live record bytes under a fixed last-use schedule. The constructive correspondence permits equality of each of these quantities, including z_q when the same storage lifetimes are chosen. Thus the charge is common adaptation + intersection + gather + cache + kernels + equality + lifetime + reporting + recovery on both sides. This is an analytical same-policy ledger, NOT a claim of equal real runtimes, compiler constants, implementation labor or all possible adapter capabilities. No positive removable fraction or reliability differential has been identified. Trying to call the common read-set work a gain would recycle an adverse contrast. **EXP-000R result: no surviving bounded witness; prototype gate fails for advancement.**

### EXP-001R completed: consumer and smaller-query test (CLM-612)

Independent R3 raw-source reopens confirm S23 estimate37–44 uses local `arrival_impr`; S24 estimate44–66/arrivalDelay109–116 and S25 selection260–294 support a driver-arrival alternative/undo/rank flow. They remain neighboring contracts, not the frozen consumer. Current rights-cleared public source reading did not establish an actual complete-vector sizing consumer.

The strongest prospective justification tried here is endpoint-specific protection: improve a chosen cost while enforcing s_c(e) >= t(e) at protected endpoints. This is a deliberately proposed decision, not observed adoption. Synthetic records A=(-1,-3,4), B=(-3,-1,4) have identical WNS=-3, TNS=-4 and violating set {e0,e1}. Thresholds t=(-2,-4,0) accept A and reject B. Thus WNS/TNS even with violating endpoint identities do not determine this guard. However the exact scalar margin g(c)=min_e(s_c(e)-t(e)) determines it: g(A)=1, g(B)=-1. For protection of e0 alone its single slack suffices. Fixed tie/area policy can consume (g,score,order); a full vector need not be exported or stored. Computing g can still require all relevant endpoint timing; this is not a claim of fewer timing kernels. Fixed-order streaming with an explicit UNKNOWN/nonfinite policy avoids introducing new FP reassociation into an actual engine; the current integer check certifies no FP behavior.

EXP-006B checks the arithmetic on 512 finite three-endpoint records and both candidate decisions. It establishes a counterexample to aggregate sufficiency and a counterexample to the inference 'aggregates fail, therefore full-vector materialization is necessary.' These records are not realizable circuit witnesses or measured sizing workload. The script is embedded in experiment-plan.md, SHA256 2795a570a2792227ddd347fa64363a699f739bf28b5b35c71daf8f9e504fb7d1. A post-hoc arbitrary endpoint audit could justify richer retained information, but no engineering user, latency/storage need or superiority to sparse base-plus-delta queries has been sourced. Full vectors remain the frozen contract, not silently replaced by g. **EXP-001R result: no adequate consumer witness; independent demand remains unresolved.**

## Contest/fidelity corrections and coverage

S28 reopens the ISPD26 organizer's ideal-clock single-corner setup context (§2.3, §5.2). This supports the legitimacy of the restricted scope, not the frozen candidate API. S29 reopens ElmoreCeff §III: its changed effective-capacitance approximation belongs to a separate fidelity/cost alternative, not same-kernel byte-preserving acceleration. No reported gain is reproduced or borrowed. S30 names official winner teams; winner mechanisms remain unchecked. S31 pins the actual linked baseline script, repairing the previous guessed-path 404: final reporting after optimization/routing does not expose the optimizer's per-candidate query. Details and remaining editions/winner coverage are in contest-audit.md.

Search expanded conditional/memoized timing terminology and official contest/source links on 2026-10-15. It was bounded, not exhaustive. No vendor internals, commercial absence, universal duplication or theoretical limit is established. Current selection is parking for missing positive witnesses; it is not a claim that no useful combination could exist.

## Claim ledger and action

| ID | Type / evidence | R3 position |
|---|---|---|
| CLM-601 | Scoped demand inference; S23–S25, S28; CLM-612 | General timing optimization is real; exact full-vector consumer unresolved |
| CLM-602 | Historical three-lens shortlist in previous released proposal | Agent/predictor alternatives not silently substituted; no new experiment or superiority claim |
| CLM-603 / 609 | Source observations + own reduction; S20/S21/S05 | Generic executor distinction withdrawn; useful combination still eligible but unwitnessed |
| CLM-604 / 605 | Specification + conditional induction above | Real adapter exactness unproved; no promotion |
| CLM-606 | R2 finite record check, retained as historical bounded evidence | No EDA result or speedup; not rerun or broadened in R3 |
| CLM-607 / 608 | JOB, P-BRIEF, tasklist, null forecast | Missing owners/build/rights/allocation/consents; no resource request or pilot |
| CLM-610 | Pinned R2 caller trace; selected functions reopened here | Source interpretation retained, no workload execution |
| CLM-611 | New source-specific operation/lifetime derivation; S27 | Read-set burden is common to both adapters; no useful delta found in bounded pass |
| CLM-612 | New prospective-decision analysis; EXP-006B | Endpoint detail can matter, but fixed guard has smaller sufficient statistic; full output demand not established |
| CLM-613 | Parking inference from failed witness gates and V-R2 required action | Recommend park, preserving conditional hypothesis and two resurrection gates |

Headroom: 1-f*r+h is only an accounting identity for a stated baseline partition; no calibrated f,r,h, numerical forecast, proven lower bound or saturation result exists. Zero drift scores preserve the mechanism, user and output; they do not pass novelty, utility or feasibility.

Resurrection requires BOTH (1) one concrete required capability or cost/reliability delta over faithful adapted B++ with matched information/memory/adaptation, and (2) an actual or independently justified prospective consumer of the unchanged full-vector contract with sufficient-smaller-query comparisons. Only afterward should compatible read-set/FP/build/rights/owners/resources and dual-consent work activate. A smaller-query, VT-only, new numerical model, predictor or agent successor needs a new topic ID. No successor is created by this role. No abandonment consent is signed because bounded failure is narrower than an established dead end. The owner-authorized fourth review cycle can audit this parking evidence; it does not authorize a pilot.
