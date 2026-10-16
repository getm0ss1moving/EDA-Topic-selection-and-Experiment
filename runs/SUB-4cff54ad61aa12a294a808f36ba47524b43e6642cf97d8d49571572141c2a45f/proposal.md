# EDA-0012: Shared-site feasibility feedback for leaf-clock clustering

## Position and provenance

D04 batch 0004 cycle 4/4, initial successor proposal. This is a concrete research candidate, **unresolved and not experiment-ready**. It does not inherit EDA-0009 acceptance, signatures, measurements or resources. Its predecessor is parked, not disproved or jointly abandoned. Exact actor/session/input/packet bindings are in compliance.json. Final scientific adjudication belongs to the new independent verifier; this proposer recommends retaining a parked research hypothesis after the finite batch unless the remaining gates are actually satisfied. No fifth cycle is requested.

## Problem, user and decision

A physical-design engineer, between placed standard cells and complete clock routing, must choose leaf sink groups and corresponding buffer locations. Fix the data-cell placement, clock domain, buffer master, fanout/capacitance constraints, technology, SDC and downstream flow. Study a bounded local neighborhood of at most 32 sinks and at most 8 leaf buffers. Clock gates, multi-height masters, multiple voltage domains and data-cell displacement are initially outside the mechanism's supported domain; encountering them requests ordinary CTS fallback, not a fabricated feasibility verdict.

Question: **Does retaining and feeding back shared legal-footprint competition across proposed sink groups reduce final closure cost or improve post-route setup slack, compared with equally informed integrated/conventional optimization and ordinary prediction-plus-legalization?** The exact footprint assignment is the object of physical construction, not a timing-methodology contribution to D05. Final extracted setup/hold timing remains a fixed oracle.

CLM-1201 (source observation): the pinned OpenROAD CTS documentation connects obstruction-aware buffering to reduced legalizer displacement and possible latency/skew/timing changes [S01 raw README line 87]. This establishes a publicly documented engineering connection, not measured prevalence or a meaningful threshold. CLM-1202: selected pinned source first obtains a clustering solution and then calls legalizeOneBuffer on each non-singleton cluster center; the helper already considers blockages and occupied locations [S02 raw 184-244; S03 raw 157-225]. Thus neither obstacle avoidance, occupancy awareness nor cluster/legalization interaction in general is claimed new. Whole-flow behavior, downstream detailed placement and all callers were not audited.

## Inputs, representation and output

For each enumerated sink subset c and permitted buffer placement p, store its sink bitmap, master/orientation, complete site-footprint bitmap, fixed-placement legality result, estimated electrical features, and model provenance. A leaf option is a hyperedge (sink subset, occupied sites), not merely a centroid and a scalar capacity. Two selected options conflict if sink coverage overlaps or physical footprints overlap. Every sink must occur exactly once; selected leaves obey the fixed number/cap/fanout contract. The finite model is a weighted exact-cover/set-packing problem. Finite-domain exactness is elementary and is not a new optimization theorem.

Candidate locations are finite and explicitly enumerated from legal rows within a displacement window locked before evaluation. A valid assignment is a constructive certificate for this declared geometry model; it is not routing, skew, DRC, electrical or global CTS certification. An infeasible restricted domain means only NO_ASSIGNMENT_IN_THIS_ENUMERATION. Search must expand the domain under the common charged schedule or fall back. It must never conclude physical impossibility from missing candidates. Source/database changes invalidate footprints, electrical scores and cuts; no unproved cache reuse is needed by this topic.

## Proposed causal mechanism

The candidate mechanism is **footprint-conflict feedback from buffer assignment to local sink repartition**, with optional learned amortization of the counterfactual cost of conflicts. Start from the same ordinary CTS grouping. Enumerate the common leaf options. A joint assignment checker returns either a feasible footprint-disjoint option set or an explicit finite unsatisfied core. Feed the core back to a bounded regrouping master: it may exchange sinks only within the frozen neighborhood, while the buffer count and all physical constraints remain fixed. A full cluster-combination no-good is always safe for exactly the same option domain. A generalized core cut is permitted only with its scope/dependencies proved; changing domains or the buffer master invalidates it. Core shrinking is paid work.

At each of at most 8 iterations, prioritize at most 16 permitted sink exchanges using deployable features: sink coordinates/caps, rows/occupied cells/blockages, full candidate footprints, current upstream latency estimates and already-paid core identities. No post-route result is a deployable feature. A deterministic central arbiter commits one complete state; workers never edit the database simultaneously. Terminate at the bound, no improving feasible candidate, or fallback; final full flow evaluates the selected construction. Retain the baseline if no fully checked improvement survives.

CLM-1203 (own finite observation): nonempty individual legal domains do not imply a joint assignment; distinct origins do not imply nonoverlapping multi-site cells. Complete runnable finite examples, hashes and stdout are in search-log.md. They demonstrate the information that an independent scalar/centroid abstraction can omit. They are not a failure reproduction of OpenROAD, a proof of empirical headroom, an agent result, or novelty over integrated solvers.

## Nearest prior and contribution burden

CLM-1204 (source observations): S04 iCTS section 3 already combines balanced K-means, min-cost flow, partition optimization, topology and buffering. S05 is a public disclosure of ML-guided clock clustering with subsequent timing checks. S06 describes clustered CTS and coupled learning for relocation/buffer changes. These negate broad claims that joint objectives, prediction plus checking, or collaborative clock optimization are new. S07 supplies generic logic-based Benders assignment/subproblem feedback. The obvious no-good/cut loop here is an application of that conventional decomposition. S08/S09 supply current CTS multi-target predictors; their outputs are approximate, not certificates.

The candidate contribution route is a useful physical representation/amortization tradeoff: preserve exact shared-footprint interactions while predicting which *repartition repairs the conflict at acceptable electrical cost*, rather than independently scoring groups and repairing after selection. The putative benefit is reduced failed regrouping/electrical/full-flow evaluations at equal total cost. **This delta is not yet established.** A conventional integrated set-packing/MIP/CP solver and LBBD controller receive every footprint, core, predictor estimate, warm start and enumeration action. A deterministic candidate controller that uses identical state, scores and ties to that conventional solver is the same algorithm and must be merged, not presented as a new arm. A learned ranker must beat an equally expressive conventional model with the same training labels, features and tuning budget; novel labels are not presumed.

Strongest alternative explanation: all gain over stock CTS comes from adding the ordinary joint placement model or spending extra candidates/labels, while any learned/agent wrapper contributes no useful cost-quality change. EXP-1204 and EXP-1206 explicitly test that explanation. Finding a conventional equivalence is a useful negative outcome, not a reason to rename the same algorithm.

## Unified, specialist and cooperative alternatives

D: separate electrical-displacement and conflict-cost predictors plus ordinary fusion. U: a shared encoder with separate heads for these same targets. H: either predictor ranks exchanges, exact assignment validates geometry, and the full flow validates the result. The finite exact checker never accepts an option because a predicted score is favorable. Prediction errors influence efficiency/selection only. No probabilistic coverage, global optimality, foundry signoff or exact timing claim is made. Training architecture/label availability are dependency tasks, not completed implementation.

Algorithmic cooperation can consist of a partition worker proposing exchanges, a geometry worker returning exact domain-specific cores, and an electrical worker scoring fixed proposed trees, sharing versioned state with one arbiter. Their observations/actions and synchronous message boundaries are above; only the arbiter writes. Compare to one centralized non-LLM controller with identical state, calls, parallelism and termination, and to a single agent with the same repeated-call/token/tool budget if an LLM arm is eventually allocated. Worker labels provide no novelty. Drop an agent wrapper if the centralized implementation matches it. No algorithmic workers, subagents, training or paid API calls were launched here.

## Demand, endpoint and headroom

Primary endpoint: paired post-route extracted worst setup slack in ns at fixed clock target, SDC, library, die area and flow, with hold, complete clock/data connectivity, routed DRC, clock power estimate, total cell area and wall-time guards. A secondary endpoint is all-cost time to a complete feasible tree meeting a locked skew/electrical contract. Report illegal/failed/timed-out cases; do not turn missing reports into zero skew. Buffer displacement and core frequency are explanatory metrics, never publication endpoints on their own.

Demand for preventing clock relocation damage is source-backed broadly (S01/S04). Frequency and materiality of *joint scarce-site leaf competition* in representative ASIC blocks remain unmeasured. EXP-1202 requires a census before mechanism outcomes. The brief's +0.02 ns/+2%/+20% screening numbers are provisional, not practitioner-validated requirements or predictions. They remain unadopted until the census, baseline variance and engineer endpoint review lock a threshold. No real headroom amount, confidence interval or success probability is defensible now. Matching can solve the special disjoint-slot model; general footprint conflicts need exact cover/packing. No applicable theorem establishes saturation of post-route QoR.

## Scope and final readiness

Preserve fixed placement, real legal footprint capacity, feedback to grouping, the same available information and final route/timing endpoint. Pure skew prediction, general flow agents, data-placement changes, repair-validation caching and increasing buffer count to escape competition require a new anchor or explicit separate baseline. Drift scores are initially zero because this is a new ID; zero says nothing about merit.

Actual experiment allocation, rights-cleared representative CTS checkpoints, site/row legality adapter, baseline reproduction, electrical cost labels, model configuration, exact task-list dual consent and materiality lock are absent. The small GCD fixture in the brief cannot establish constrained-CTS utility. No physical experiment, upstream code execution or training is reported. Stop the candidate if the census finds no material shared-footprint bottleneck; if equal-information integrated/LBBD alternatives erase its useful delta; or if overhead/route/timing regressions dominate. A failed approximation/cut certificate stops the corresponding exactness claim immediately. Absence of allocation blocks readiness, not the conditional hypothesis. No sufficient evidence or matching signatures support joint abandonment. This final-round dossier is submitted for independent review with an explicitly pending task list.

## Draft consensus metadata (not a signature)

The standalone proposer allowlist excludes a separate consensus file. The coordinator may later assemble canonical consensus from independent role-owned votes; this block records the present draft without inventing either vote.

```json
{
  "consents": {
    "challenger": {
      "decision": "pending",
      "rationale": "No current independent consent received.",
      "session_id": null,
      "signed_revision": null,
      "tasklist_sha256": null
    },
    "proposer": {
      "decision": "pending",
      "rationale": "Unallocated tasks, physical adapter, demand/threshold and conventional distinction unresolved; hash identifies draft only.",
      "session_id": "de22ba11-269c-4f5c-8aae-f697dff1e2bc",
      "signed_revision": null,
      "tasklist_sha256": null
    }
  },
  "open_conditions": [
    "EXP-1200 actual allocation and rights.",
    "EXP-1202 narrow engineering demand/materiality.",
    "EXP-1203 complete finite legality adapter/global caps.",
    "EXP-1204 strong same-information baseline/delta.",
    "EXP-1205 actual threshold and complete flow scripts.",
    "EXP-1206 distinct model/label/config costs.",
    "Exact same frozen task-list P/C agreement."
  ],
  "readiness_checks": {
    "baselines": false,
    "correctness_oracle": false,
    "dependencies": false,
    "metrics": false,
    "owners": false,
    "reproducible_procedures": false,
    "resources": false,
    "stop_rules": false
  },
  "status": "pending",
  "tasklist_sha256": "1786f88ab4f09bbded99d69ecc1b26c58338bba2b05e416bfe3ed5ffe13db817"
}
```

## Claim ledger

| ID | Type | Evidence / locator | Uncertainty |
|---|---|---|---|
| CLM-1201 | Source observation | S01 raw87 | Broad possible engineering connection, narrow demand unknown. |
| CLM-1202 | Selected source observation | S02 raw184-244; S03 raw157-225 | Existing occupancy-aware implementation acknowledged; no whole-flow defect. |
| CLM-1203 | Own finite analytical observation | search-log.md exact code/stdout/hashes | Invented domains only; no physical/novelty inference. |
| CLM-1204 | Prior mechanism mapping | S04 section3; S05 Definitions140-163; S06 S1-S6; S07 Introduction; S08 section3; S09 README | Selected access; full-system duplication and residual useful delta unresolved. |
| CLM-1205 | Advertised capability | S10 CCOpt body paragraph | No measured commercial gap or internals claim. |
| CLM-1206 | Contest context | S11 official page; S12 physical p26/p36; S13 archive list | Winner code/method bridge and exact contemporary overlap unresolved. |
| CLM-1207 | Dataset suitability limit | S08 sections2.1/5; S14 README | No representative footprint payload/rights audit. |
| CLM-1208 | Hypothesis | Proposed causal mechanism and EXP-1202/1204/1207 | Material demand and same-information benefit unmeasured. |
| CLM-1209 | Resource/provenance observation | JOB.json; common batch policy; compliance.json | No new EDA/training/allocation; audit cannot see unseen actions. |

No physical performance measurements or numerical forecasts are asserted. Every physical gain mentioned in source metadata remains an unadopted author claim.
