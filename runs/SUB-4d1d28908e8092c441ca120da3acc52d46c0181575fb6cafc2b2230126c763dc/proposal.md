# EDA-0001 / D04: Cut-guided blocker release for timing repair of DRC-clean routes

## Status and scope

Research candidate, revision R1, batch round 1 of 4. Novelty and physical feasibility are unresolved. No routing experiment, baseline reproduction, timing measurement or independent approval occurred in this turn. This release is a proposal for adversarial review, not a request to start compute. The shared-input directory is empty; no historical scientific claim or signature is inherited.

The workflow slice is incremental signal detailed routing after a legal placement and a completed detailed route. Netlist, placement, clock routing, die, library, SDC and corner remain fixed. The engineering decision is whether a small set of otherwise legal neighboring signal routes should relinquish resources together to repair a setup-critical detour. Timing analysis and extraction are external fixed oracles, not D05 methodological contributions. Macro placement, ML timing prediction, buffering, cell sizing, clock editing and global-router redesign are outside the anchor.

## Engineering need and primary endpoint

CLM-001 and CLM-002 establish a documented connection between routing detours and timing closure; they do not establish the prevalence of the proposed specific failure. The intended user is a physical-design engineer facing negative extracted worst setup slack after routing. Primary endpoint: the paired change in minimum setup slack over every constrained endpoint, in ns, after detailed routing and fixed extraction. An improvement of one selected path does not count when another path becomes worst. Report TNS, all endpoint slacks, hold violations, DRC, connectivity, runtime, memory, area and estimated power. Practitioner validation of the provisional +0.02 ns threshold remains T02; no market-wide unmet-need assertion is made.

## Claim ledger

| ID | Type | Claim and source locator | Limit |
| --- | --- | --- | --- |
| CLM-001 | Observation from source | ISPD18 explicitly illustrates a legal detour degrading a critical connection and asks that routing guidance be preserved. S01, Abstract and Figure 1. | This is an organizer-provided problem, not our contribution. |
| CLM-002 | Observation from source | Post-GR information can differ from final DR timing; the cited study assesses downstream timing optimization. S02, Sections 1, 2.1 and 5.2. | Does not show this candidate can repair a fixed routed design. |
| CLM-003 | Observation from source | WXL uses routing-order-aware aggressor/victim queue updates and incremental checking. S03, Section VI, Figures 14–15, Algorithms 11–12. | Generic blocker release and queueing are prior art. |
| CLM-004 | Observation from source | BonnRoute includes costly backup searches through wires and reservation discounts for incremental routing. S04, Sections 5.1–5.2. | The backup overlap is substantial; exact policy equivalence remains T01. |
| CLM-005 | Observation from source | Adaptive region removal handles restrictions imposed by retained paths. S05, Section 2.1, Figures 2–4. | Region enlargement and removing retained segments are not new. |
| CLM-006 | Observation from source | OpenROAD's pinned source contains separate net-sort and queue-sort paths; seed swaps appear in the former. S06, FlexDR_maze.cpp lines 1477–1539. | It is unverified which path a proposed fixture exercises; do not assume a seed flag changes the actual queue. |
| CLM-007 | Observation from source | Timing-driven rerouting with incremental extraction predates this candidate. S07, original proceedings abstract. | Full paper access failed; method-level distinction is unresolved. |
| CLM-008 | Observation from source | Recent offline RL changes detailed-routing cost schedules. S08, Sections III–V, version 2. | This candidate is not a claim that adaptive routing or learned schedules are absent. |
| CLM-009 | Observation from source | ISPD25 evaluates timing, power and overflow at global routing. S09, Introduction and Evaluation. | Contest score is not our post-DR endpoint. |
| CLM-010 | Hypothesis | A delay-budget surrogate cut can identify a smaller useful release set in DRC-clean timing failures than geometric or marker-driven release under equal total budget. | No empirical support; EXP-001 and EXP-002 are decisive. |
| CLM-011 | Inference | Published repair mechanisms do not by themselves establish that this particular cut-selection policy is equivalent or distinct. | No novelty conclusion follows from the inspected subset; T01 remains blocking. |
| CLM-012 | Feasibility limitation | The packet establishes only a GCD smoke fixture and provisional caps; no representative three-design allocation is established. S00, available_designs, compute and feasibility_status. | No execution readiness or resource commitment. |
| CLM-013 | Advertisement observation | Commercial tools advertise timing- and routing-driven closure. S10, About IC Compiler II. | Public descriptions do not expose internal release-set selection. |
| CLM-014 | Logical result | If every source-target path in a fixed surrogate graph crosses an edge disabled by retained ownership, no eligible path exists while those disabling owners remain. | Reachability statement only; not a physical timing lower bound. Proof below. |

## Nearest approaches and explicit proposed distinction

The nearest mechanisms are S03's queue, S04's incremental routing, S05's region repair and S07's timing-driven rerouting. S11 supplies an accessible Dr. CU baseline distribution. None is being dismissed as inadequate from its title or objective. The potentially distinct object is a reproducible cut witness in a cost-budget-expanded local routing graph, used to choose a bounded *owner set*, including DRC-clean blockers, before jointly rebuilding those owners and the timing target. This is a tentative distinction requiring source-level comparison, especially against older blocker-selection and multicommodity formulations.

A straightforward composition of criticality sorting, a large box and rip-up/reroute does not constitute this contribution. If that composition selects the same effective owner sets, or matches outcomes at the same end-to-end cost, the proposed interaction fails. Replacing it with a generic learned priority policy after such a result is prohibited.

## Analytic failure witness, not a measured circuit

Consider two legal connections A and B, two unit-capacity corridors x and y, and fixed terminals. A's route costs are x=1, y=10; B's are x=1, y=2. The incumbent assigns A to y and B to x. A has budget 2; B has budget 3. Rerouting A alone cannot use x while B remains. Joint reassignment A→x, B→y meets both budgets. There are no shorts in either assignment. This shows the insufficiency of an A-only move in this toy graph, and nothing more: established multi-net methods solve it, it does not distinguish our policy, and the scalar costs are not extracted RC timing. EXP-001 must include larger and adversarial families on which the complete prior policies are run.

## Proposed mechanism: bounded cut-guided owner release

1. Start from a DRC-clean incumbent. Select an actually constrained violating setup endpoint and one interconnect on its path; use source/sink pairs without altering pin access. Keep clock, power, fixed wires and geometry outside a predeclared clip immutable.
2. Build a layered local graph with explicit ownership on disabled track/via transitions and fixed hard obstructions. Record boundary stubs. Each disabled edge records **all** owners whose geometry or spacing footprint disables it; clearing just one of several owners is insufficient.
3. Attach fixed, nonnegative additive route-cost weights. Construct a budget-expanded graph with states (vertex, consumed integer cost), at most 128 cost bins and a declared rounding rule. This is a search surrogate. Its cost budget is calibrated only on development data, not claimed as a sound RC-delay bound.
4. Search for a source-target path under current retained ownership. If absent, retain the reachable-set frontier as a cut witness. In this frozen graph, every valid path crosses the frontier; a candidate release must enable at least one frontier edge by removing its complete disabling-owner set. Hard-obstruction-only frontiers indicate no local release within this abstraction.
5. Enumerate distinct owner subsets in increasing cardinality, bounded by three released blocker nets plus A, at most 32 exposed owners, 256 candidate sets and 50,000 expanded states. Use each new cut to prune sets that cannot open any frontier edge. Recompute reachability after release. Return 'cap exhausted' separately from 'infeasible in the fully enumerated bounded model'. No claim of global minimum release cardinality is allowed beyond completed exhaustive bounded search.
6. Rebuild A and the selected blockers jointly within the clip using the same bounded candidate-path enumeration and compatibility checks used by the geometric baseline. Freeze external stubs and preserve every pin connection. Commit atomically only after full-design connectivity, DRC, fixed extraction and full STA pass guardrails; otherwise restore the exact incumbent checkpoint.
7. Evaluate all endpoints after each tentative transaction. Require improvement in whole-design worst setup slack and no newly violating hold endpoint. Reject improvements that borrow hidden delay or create an off-clip violation. Charge search, rejected candidates, extraction, STA and checkpoint costs.

CLM-014 proof: let U be the source-reachable states in the enabled expanded graph. The target is outside U. Every source-target path in the graph with disabled transitions restored has a first edge from U to its complement. All such edges are disabled, otherwise their destination would be reachable. Keeping every disabling condition on the frontier therefore keeps the target unreachable. This elementary certificate does not prove existence after a release, correctness of joint reembedding, infeasibility outside the clip, completeness of the discretization or impossibility of physical timing improvement.

## Causal hypothesis, alternatives and falsification

H1 / CLM-010: targeting structural release obligations lets a fixed search budget spend more work on physically useful joint moves. Strong alternatives: (i) gains come entirely from trying more routes, (ii) larger regions explain all gains, (iii) a criticality-first queue suffices, (iv) the surrogate cut misidentifies physical bottlenecks, (v) rerouting moves the problem to another endpoint, (vi) the small-clip limits exclude useful moves.

EXP-001 compares owner-set policies under identical graph, path generator, state/candidate limits and operation counts. EXP-002 compares default router, target-only reroute, naive criticality+geometric-blocker repair, cut-disabled joint search, and full mechanism on identical checkpoints and equally charged wall/CPU budgets. The cut-disabled arm uses the same owner pool and joint engine but cardinality/lexicographic enumeration without witnesses. No random flag is treated as effective before branch tracing. Gain over default alone is insufficient.

Kill contribution if T01 finds an equivalent mechanism without a new defensible limitation; if cut guidance does not beat the strongest equal-budget policy; or if the useful difference is only an implementation speedup without measured downstream demand. Kill physical applicability if no eligible DRC-clean timing failure occurs in the independently selected fixtures, boundary rules prevent valid moves, or full-oracle cost exceeds the cap. A surrogate-only success cannot support publication utility.

## Headroom and feasibility

No applicable optimum or saturation bound for post-DR worst slack has been established. The toy shows a neighborhood restriction, not headroom in a physical design. Zero DRC is a legality endpoint, not proof of timing optimality. Published runtime improvements, contest scores and unrelated timing gains are not numerical forecasts here.

The pinned OpenROAD commit is from 2024; 2026 public documentation exposes newer behavior. Only pinned source claims are assumed for implementation. S06's README permits documented seed controls, but its separate queue path makes a seed-only control suspect. This is an explicit baseline-instrumentation dependency.

No new compute is authorized by this job. The inherited 8 CPU-hour / 4 GB / 2 CPU / 0 GPU envelope is explicitly provisional. Representative licensed designs, actual local clip APIs, extraction setup, full-run cost and engineering threshold remain unresolved T02–T04. A three-design, five-seed, five-arm physical comparison entails 75 complete evaluations before development/rejections; it is not declared to fit that envelope. Two weeks is a planning horizon, not evidence of completion.

## Direction integrity and decision position

Initial anchor is frozen in direction-control.json; combination_drift=0 and demand_drift=0 because this is the initial candidate, not because novelty or demand is confirmed. Preserve the graph-guided owner-set mechanism and fixed-design post-route endpoint. No challenge has yet been released or adjudicated. The proper next step is independent novelty and feasibility review. Experiment consent is pending; acceptance gates remain unresolved. Supported scientific abandonment would require matching proposer/challenger consent on an immutable revision and verifier review.
