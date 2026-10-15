# Independent challenger review — EDA-0001 R1, batch round 1

Actor: ChatGPT-C04-PHYSICAL. Session: f29f2abb-ad12-4c6f-8446-e384bd6ae66d.
Input commit: a48f03d4bc254c0b0957d0fe0f265e072d6cf49a.
Reviewed proposal: SUB-4d1d28908e8092c441ca120da3acc52d46c0181575fb6cafc2b2230126c763dc.
Review is explicitly unblinded: proposal and experiment-plan disclose null effect forecasts and provisional thresholds. No historical verdict or approval is inherited. No routing, build, calibration or physical experiment was executed.

## Assessment

**revise**, with two major fixable concerns and one specification concern below. This is a recommendation for independent verification, not a verdict. The graph-selection subproblem has closer established analogues than the implemented comparator list currently captures. A very recent primary preprint also selects removals from graph frontiers. Neither observation proves equivalence of the complete physical method. The proposal correctly distinguishes its surrogate certificate from an RC timing bound and candidly leaves engineering readiness false. Continued research is reasonable; experiment consent is withheld pending the specified repairs and existing dependencies.

## OBJ-001 — The decisive comparator is missing the closest label-set search family

**Targets:** CLM-010/011, proposed mechanism steps 2–5, EXP-001 and EXP-002 arms B2/B3; T01/T05/T07.
**Severity:** major, fixable; potential blocker to a novelty/causal attribution claim, not proof that the idea is already fully published.
**Evidence:** C01, pp.4–6, Discrete MCR and Section 3.2, defines minimum removal using set-valued labels and an exact subset-state search. C02, pp.182–183, Figure 3 and Algorithm 1, distinguishes greedy, exact and bounded-length searches. C03, Sections II–III, especially Eq.(5)–(6) and GFS-1, uses bidirectional frontiers to construct removal sets and refines candidates on reduced graphs. These are primary methods, independently found beyond the proposal bibliography. C04, Sections III–VI, already supplies concurrent detailed-routing formulations with design-rule constraints; simultaneous reconstruction is not independently new.

**Reasoning bridge (our derivation):** take the proposal's already discretized, cost-expanded graph. Subdivide each transition into a vertex labelled with its complete disabling-owner set; retain direction and cost-state edges, remove hard-obstruction edges, and connect all valid terminal cost states to one sink. A target path's required release is the union of its labels. Minimizing its distinct owners is exactly a discrete constraint-removal subproblem on this transformed graph. This maps selection only: it does not solve legal reembedding of released nets, nor predict extracted timing. The physical coupling may still be valuable. However, defeating geometric release or lexicographic subset enumeration does not distinguish cut guidance from established label-set pruning plus the same reconstruction/oracle. T01 names related keywords but T05/T07 do not require an executable family member. C03 further makes a simple 'frontier-driven removal is new' characterization unsafe; its bidirectional heuristic is not asserted equivalent to this proposal's reachability-cut pruning.

**Uncertainty:** high confidence in the selection mapping; unresolved full-policy equivalence and practical performance. Published robotics timings are not transferred to VLSI. Directed cost-expanded graph applicability of each heuristic must be checked, not assumed.
**Reversal condition:** a source-pinned mapping demonstrates a genuine missing interaction/guarantee or the same-budget standard comparator fails precisely on a preregistered family the cut method handles, followed by downstream usefulness. Finding a relevant difference reverses an equivalence suspicion; it does not alone establish utility.
**Cheapest decisive test:** first write the reduction and policy table without execution. Then, only after allocation, implement exact subset-dominance MCR for tiny graph oracle checks and one bounded/greedy set-search comparator in the shared owner-pool/path-generator/joint-reconstruction harness. Compare complete owner-set traces and accepted embeddings under equal charged time; include repeated labels, overlapping labels and directed budget states. Adapt C03 only after documenting which assumptions survive. Use a simple MCR-selection + existing joint-routing composition as the direct alternative. Preserve the cut mechanism rather than pivoting to generic routing priority.

## OBJ-002 — Strict per-transaction WNS improvement excludes independent tied bottlenecks

**Targets:** mechanism steps 1, 6–7; CLM-010 applicability; T02/T05/T07.
**Severity:** major conditional applicability concern; no demonstrated prevalence and no claim of universal failure.
**Evidence:** P01, proposal mechanism step 7 requires whole-design worst setup slack improvement for each transaction; step 1 chooses one connection in a bounded clip. P01 experiment-plan EXP-001 does not explicitly include independent tied worst endpoints. Source is the frozen proposal itself; the following is an analytical counterexample, not a measurement.

Construct two independent cones outside each other's permitted clips, with endpoint slacks -0.10 ns and -0.10 ns, fixed clocks, no coupling and legal independent repair opportunities. Each local repair improves its own endpoint to -0.05 ns with no other change. The first repair leaves WNS at -0.10 ns, so strict step 7 rejects it. Neither repair can be committed, although applying both would reach WNS -0.05 ns. Owner-release cleverness cannot overcome this acceptance rule. Similar near-ties can limit the magnitude of accepted single-clip improvements. This does not contradict the narrow hypothesis that some instances benefit, and does not imply TNS should replace WNS.

**Confidence/uncertainty:** exact for the stated independent-cone model; physical incidence unknown. Tolerances and endpoint ties are not yet pinned.
**Reversal condition:** demonstrate that the declared eligible workload excludes this case for an engineering-supported reason, or provide an anchor-preserving atomic transaction specification that covers all tied bottlenecks within the existing caps. Any new multi-clip transaction must be explicitly costed and reviewed, not silently added.
**Cheapest decisive test:** add the two-cone counterexample and a unique-worst control to EXP-001; later record the number of tied/near-worst endpoints outside each clip before selecting repairs. Report all ineligible/plateau cases in the denominator. A useful positive outcome must survive the unchanged all-endpoint oracle. Numerical tie tolerance must be frozen from oracle resolution, not chosen after outcomes.

## OBJ-003 — Runtime screen has no fixed comparator denominator

**Targets:** EXP-002 provisional <=20% runtime regression, B0 no-op baseline, T03/T07/T08.
**Severity:** moderate specification defect; prevents a reproducible cost/utility decision, not evidence that the cap is infeasible.
**Evidence:** P01 experiment-plan EXP-002 defines B0 as incumbent plus no-op extraction/STA and also requires <=20% total runtime regression, without fixing the denominator or whether shared incumbent construction is included. P02 compute caps are expressly provisional.

**Reasoning:** improvement overhead divided by no-op STA time can be very different from overhead divided by the entire original routing flow. Equal search budgets for M and B2/B3 do not resolve this separate user-cost screen. A cap is not a measured runtime distribution. The proposal already correctly notes that 75 evaluations at 600 CPU seconds exceed eight CPU-hours; this review does not turn that illustrative calculation into a measurement.
**Reversal/test:** preregister both marginal repair cost and amortized full-flow cost; identify the one driving the 20% decision, its baseline, included operations and reuse policy. Give a worked symbolic ledger before allocating any run. Charge all selector preprocessing, rejected embeddings, full-oracle calls and rollback equally. Pass if every timed event has exactly one category and the decision can be reproduced from the ledger. No performance experiment is needed to repair the definition.

## Coverage and strongest favorable evidence

- **Duplicate/equivalent prior art:** unresolved for the complete method; supported overlap at selection and joint routing. C01–C04 add a concrete comparison absent from the executable arms. No exhausted-novelty ruling is warranted.
- **Mechanism/composition:** supported concern OBJ-001. The elementary cut proof is valid for an accurately constructed frozen graph; no new theorem or physical delay lower bound is established. Exact relation between cut pruning and existing frontier/set search remains open.
- **Engineering demand:** C05 Figure 1 supports routing-detour motivation. C13 Section 1 also documents interconnect/congestion constraints but concerns a different optimization stage. Neither establishes frequency of <=3-owner, local, DRC-clean post-route opportunities or validates +0.02 ns. T02 must measure an eligible-opportunity denominator when execution is authorized and obtain threshold rationale. Demand remains unresolved, not absent.
- **Commercial/open comparison:** C14 advertises routing/timing closure; internals and controlled comparisons remain unknown. Open-route experiments can establish an open-flow result, not commercial superiority. A small research technology/corner does not establish foundry signoff.
- **Headroom:** unknown numerical range. General constraint-removal computational difficulty is not an applicable saturation bound. The graph certificate only identifies a necessary release condition. No evidence supports either near-optimal timing or a +0.02 ns expected gain. OBJ-002 shows a specific neighborhood/acceptance restriction.
- **Contest-supplied ideas:** C05 already supplies detour motivation; C06 and C07 already supply blocker and region repair. C10 supplies 2025 GR rules/results, but winner algorithms were not recovered. C11/C13 confirm 2026 is post-placement buffering/sizing, outside the fixed-netlist anchor. C12 is a newer 2026 timing/global-routing abstract, not a fixed-route method. Contest novelty remains partially covered and unresolved at winner-method level. No claim of no newer relevant contest is made.
- **Experiment execution:** T01 reading is executable now. T02–T04 correctly identify missing design rights/pins, resources, commands, integration and oracle coverage. T05–T08 are conditional engineering work, not an executable frozen runner today. There is no consent while these remain unresolved. Shared state/candidate limits plus equal time are useful controls; clarify which resource terminates each arm and never compare capped incompleteness as infeasibility.
- **Cost/fairness:** rejected attempts and full oracle calls are already charged, designs/seeds are clustered, and criticality/geometric/cut-disabled ablations are useful. Add the stronger comparator and OBJ-003 ledger. No experiment was run to infer fit in the allocation.

## Direction and disposition

Combination drift **0/3**; demand drift **0/3** relative to the supplied initial anchor. Baseline additions and plateau/ledger tests preserve that anchor. These scores are not novelty or demand approval. Joint-abandonment position: **continue**. No supported ground establishes exhausted innovation, applicable saturation, a dead end or immutable direction failure. No signature for another role, scientific approval, merge or experiment consent is issued.

## Task-list contribution and provenance

See challenger tasklist.md for exact additions and consent conditions, independent-estimate.md for headroom, prior-art.csv for nearest mechanisms, sources.json for access levels, and search-log.md for dated queries and limits. Local run record is runs/challenger-round1.json; frozen SUBMISSION.json binds identity and bytes. Submission validation is structural only. Initial objection release; no withdrawals or adjudications yet.
