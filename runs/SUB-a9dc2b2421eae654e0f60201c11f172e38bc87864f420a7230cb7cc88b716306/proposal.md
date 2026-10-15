# EDA-0004: On-demand paired suffix differences for exact endpoint PBA

## Position, identity and scope of this final cycle

This is a new D05 candidate, not a renamed EDA-0002 revision. Proposer ChatGPT-P05-TIMING-EDA-0004; session 890f3b5f-a234-45ac-9b26-a39cc34133e7; input commit a48f03d4bc254c0b0957d0fe0f265e072d6cf49a; packet cd7f289283c0ef176125fcd266cd4fda9aba02467917228ec9fbc1ab20a30b0a. Domain batch cycle 4 of 4; initial scientific revision for this successor. Requested model is JOB.json's gpt-6.1-sol/high; no separate backend attestation is claimed.

**Final proposer position: a precisely specified mechanism-level successor is available for independent review, but genuine originality, net engineering benefit and implementation readiness remain unresolved. Do not select it for an experiment.** The new structure is a query-directed product graph over two slew states and the SAME suffix, with a fail-closed difference certificate. It is not a claim to have invented dominance, backward propagation, PBA, safe signal bounds or interval arithmetic. Especially important: DAC2004 already supplies a scalar backward suffix solution; its exact strengthened form is mandatory, and can be stronger than our certificate. The local construction below establishes a difference from coarse global bounds, not from all prior art. Source discovery has produced closer work rather than novelty closure.

No experiment, compilation, STA, fixture generation, paid service, data acquisition or new compute allocation occurred. All examples are analytical constructions, not observed Liberty distributions or benchmark results. No consent or scientific approval is inherited or signed. The four-cycle batch ends after the independent C/V jobs for this release; the task list is a conditional research specification, not a request to keep a loop alive.

## Preserved predecessor evidence (CLM-400)

Released predecessor.json identifies EDA-0002 as parked. The three permitted releases are proposer SUB-6658c76e5f7210390d0b56e6da5f52ab23356f257be6c1ca35fa9105ad9f2774, challenger SUB-bb62d5a576a0315b05064d88decbaf2a9d2ece6ffa724e45325903548470a101, and verifier SUB-1057c0a753d7e52927891b9cf2fbc91c3e965ce980795f3ece56d65206d5ea7e. They remain lineage evidence, not new-role approval.

Retain the conditional P-RANGE=B1+ transition/cost null (old CLM-047/OBJ-003), the withdrawn blanket linear-only/no-safe-pruning premise, adverse broad-waveform synthetic records P3 3553/19600, P4 100/52088 and P5 3025/52088 as unrerun historical reports, and the unproved arithmetic/tag/report adapters. Preserve the NUM-03 nonfinite-Rd analytical obligation, repaired producer DAG but missing locks, unvalidated CAP-only demand/20% target, absent representative multicorner inputs, and absent actual allocation/consents. Their raw historical experiments were not independently reopened here. The predecessor ruling checked that local-null argument; it did not prove universal saturation or authorize this successor. The source record H-P/H-C/H-V precisely locates these bytes. Responses.md retains each adjudicated issue separately.

Old mechanism: per-scenario own-table slack enclosure and certify/refine work elimination in full multi-corner GBA. New mechanism: comparing multiple path-specific prefix signals within a fixed scenario by a joint continuation relation for exact endpoint PBA. No CAP branch assumption, cross-corner reduction, predicted corner labels or predecessor numerical certificate is imported. New ID is necessary because both analysis objective and causal mechanism change. This is not an anchor-preserving rescue of EDA-0002.

## Problem and engineering decision (CLM-401)

User: timing-closure engineer considering whether a setup endpoint requires an ECO after graph analysis flags it. Need: obtain the actual worst path-specific setup slack for a declared endpoint set without silently truncating paths or incurring avoidable propagation work. Downstream metric: elapsed time to a complete endpoint verdict and identical worst slack, not number of pruned states. Endpoint PBA demand is directly documented in S04 slides 2/11 and S11 introduction; applicability to our narrow NLDM/fixed-load slice still needs T02 practitioner/workload evidence. No present-day industry-wide runtime ratio is inferred from older results.

Primary output for every declared endpoint/context is its minimum path-specific setup slack and violation flag, with WNS/TNS computed over that fixed endpoint set in reference order. It is not every path's slack, every internal-node slack or path-tie identity. Removing dominated prefixes is allowed only where all their suffixes are covered. If path identity is requested, preserve ties and predecessor metadata or disable this pruning. Engineer-facing completion must explicitly distinguish exact-for-declared-model, unsupported and incomplete; an exhausted resource cap cannot be labeled clean.

## Frozen model and oracle (CLM-402)

Initial model: a finite acyclic data timing graph; one declared SDC mode/scenario at a time, each rise/fall and launch/capture/context key separate; fixed net loads and fixed wire-transfer definition; single-input-switching NLDM-style cell delay/slew functions. Clocks and required times are fixed exact inputs for this slice. Include data-slew-dependent setup at the endpoint. No SI, waveform propagation, OCV/path-depth derates, latches, dynamic voltage, logical sensitization proof, generated-clock inference or cross-context merging is claimed. Unsupported domains remain in the request manifest and return UNSUPPORTED or use an independently validated exact fallback; never omit them from reported coverage.

The mathematical reference enumerates ALL admissible paths in this graph using the same transfer functions and endpoint check. OpenSTA's pinned table implementation S08 is a possible transfer adapter, not an assertion that OpenSTA report_checks is an exhaustive PBA oracle. A production adapter needs a separately authored exhaustive path retimer, independent enumeration, pinned operation order and validated clock/check semantics. A scalar toy oracle establishes only the toy model. Reference output fidelity to commercial signoff remains unknown; no licensed commercial oracle exists in this packet.

## Proposed mechanism: paired suffix-difference queries (CLM-403)

At node v, prefix signals A=(a,x,k) and B=(b,y,k) have arrivals a,b, slews x,y and identical compatibility key k. Require the same admissible suffix language P(v,e,k) to a particular endpoint e. Path legality/context differences invalidate the comparison. Let F_p(s) be remaining path delay PLUS endpoint setup time for suffix p, excluding the fixed required time. For a real-arithmetic model define

    Delta_v,e(x,y) = max over p in P(v,e,k) of [F_p(y)-F_p(x)].

If b-a+UpperDelta <= 0, A is no earlier in endpoint severity than B on every compatible suffix, so B can be removed for that endpoint. Strict inequality is used when a path representative/tie is requested. At an endpoint Delta(x,y)=setup(y)-setup(x). For edge q=(v,w), with delay d_q and slew g_q,

    Delta_v,e(x,y) = max_q {d_q(y)-d_q(x)
                          + Delta_w,e(g_q(x),g_q(y))}.

The two states must take the SAME edge q in each branch. Pairing is maintained through table-cell changes; independent maxima over the two paths are forbidden. Query-directed expansion constructs a product DAG keyed by (node, endpoint/context, slew pair, table/transfer version). Hash-cons identical pair subproblems. A bounded enclosure can terminate a query once its upper bound crosses the arrival-gap threshold; otherwise refine or return UNKNOWN. Do not infer bound validity from sampled points, typical monotonicity, or a derivative with unverified domain coverage. Nonfinite values, table extrapolation ambiguity, unsupported context or exhausted query budget return UNKNOWN and retain both prefixes.

Proposed causal effect: representing differences directly can cancel suffix-common delay terms before a maximum and avoid building accurate absolute suffix functions over irrelevant slews. Reuse of a relation across arrival gaps may amortize work. This is a hypothesis about representation/cost, not a capability theorem. Exact-state memoization, ordinary transfer reuse, demand-driven scalar suffix evaluation and early stop are also granted to the strengthened scalar baseline.

### Conditional soundness and floating-point boundary (CLM-404)

For exact real transfers and a sound UpperDelta, the inequality implies b+F_p(y)<=a+F_p(x) for every p. Every removed path therefore has a retained path to the same endpoint with at least as large severity. Keep a surviving representative per dominance chain and apply comparisons only among currently retained states, or preserve an acyclic replacement certificate. Endpoint minimum slack is unchanged. Different endpoint paths may require different retained representatives; global deletion needs the condition for every reachable requested endpoint. Endpoint setup must be included; arrival dominance alone is insufficient.

This is a conditional mathematical proof, not an engine floating-point proof. In pinned executable arithmetic, fl(a+d) is not translation invariant: a difference-only recurrence cannot silently cancel a and b. The exact specification is instead M_v,e(A,B)=max_p [severity(step_p(B))-severity(step_p(A))], including both arrivals and every actual rounding operation. Its recursive transition follows the same q on both full states; terminal checks use the executable's operations. A fast difference summary is usable only with an audited enclosure of this full-state M. If absolute arrivals must enter its key, hypothesized reuse may disappear. S08 Table2::findValue shows why input/return conversions and intermediate arithmetic cannot be ignored. Failure to supply this adapter blocks any exact-engine claim; it does not justify a 5ps certificate waiver.

## Analytical witness and the strongest adverse alternative (CLM-405/406)

Witness W1, real-valued units only: x=1, y=4; A=(11,1), B=(10.5,4). Let every suffix have F_p(s)=K_p+h(s), where h(s)=0.5(s-1) on [1,1.1] and h(s)=0.05+0.08(s-1.1) on [1.1,4], with constants K_p>=0. Then h(1)=0, h(4)=0.282, and B-A severity is -0.5+0.282=-0.218 for every p. A dominates B even though B has the slower slew. A coarse sensitivity upper bound rM=0.5 yields 1.5, insufficient against the 0.5 arrival gap. A paired exact residual proves dominance. Constants K_p cancel within each suffix, regardless of their spread.

This witness does NOT establish novelty. S01 section 4.2 already bounds slope-induced delay. S02 sections 3/5 allow sensitivity-based signal ordering; a sufficiently tightened secant bound can also certify W1. S03 already conditions selection on receiver behavior. S06 already computes backward delay-versus-slew functions. In fact, define D(s)=max_p F_p(s). For the single endpoint metric,

    D(y)-D(x) <= max_p [F_p(y)-F_p(x)] = Delta(x,y).

Thus exact scalar suffix functions can certify at least every endpoint elimination that this pairwise condition certifies, and sometimes more. This deduction is a critical adverse result, not hidden in an appendix. The proposed structure has no universal pruning-power advantage over exact S06-style analysis. Its only possible nontrivial contribution is a cheaper way to obtain certain certified comparisons WITHOUT building sufficient scalar information, on a demonstrable workload. Full-state floating-point scalar value functions strengthen the alternative further.

A previous linear form F_p=K_p+0.1s would be immediately handled by tightened S02 sensitivities and S06; it is discarded as a novelty witness. W1 only isolates coarse-bound loss and motivates a representation-cost test. There is currently NO matched-information net-work witness against unrestricted scalar B+. T01 must resolve that before implementation or benchmarking. If the paired recursion just repeats scalar evaluations or its result is a cheap scalar composition, stop this candidate; adding ML, corners or a more convenient proxy cannot repair it under this ID.

## Closest prior work and contribution boundary (CLM-407)

The exact comparison inventory is prior-art.csv. Three particularly close independent approaches are S02's slew-sensitive bounds, S06's backward suffix functions, and S05's staged multiple-signal PBA. S04 provides the multidimensional budget/accuracy context; it does not license a 2-D commercial-signoff extrapolation. S17 (2025 adaptive PBA) prevents treating current commercial practice as only old path peeling. S11/S12 document prediction alternatives, whose measured error objectives differ from an exact endpoint certificate. Source access is explicit in sources.json; no missing result counts as novelty.

Proposed structural delta is the paired continuation-query representation, not concatenating a GBA filter, a cache and a classic pruning rule. The same graph, transfer evaluations, memoization capacity, endpoint set and termination rules belong to P and B+. A required ablation replaces joint paired bounds by independently bounded scalar suffix values at the same resource cap; another grants B+ on-demand exact scalar recursion. If this removes the alleged advantage, the contribution is null. Mathematical recurrence novelty alone is not claimed; ordinary dynamic programming may already suffice.

## Headroom, hypotheses and kill rules (CLM-408/409)

H1: after all preprocessing, queries, validation and reporting are charged, paired queries reduce end-to-end time versus the strongest exact scalar/multiple-signal baseline while preserving every declared endpoint output. H0: exact scalar analysis, cache reuse or pair-state explosion makes the approach equal or slower. H2: a real licensed workload contains enough repeated slew relations and bounded residuals for useful amortization. H0b: transfers rarely repeat, context keys proliferate, or broad bounds remain UNKNOWN. Both hypotheses are unmeasured.

There is no applicable proof of saturation, no measured baseline plateau and no calibrated speedup interval. The exponential worst case of explicit path propagation under the model does not prove headroom for this candidate; S06 changes representation under a discretized-table cost model. Compare its accuracy assumptions before transferring complexity. A break-even ledger must satisfy saved forward/report work > pair construction + enclosure + lookup + extra memory + any fallback/replay overhead. Counting avoided calls without charging the calls performed inside the query is invalid.

The brief's 20% time reduction is a PROVISIONAL screening threshold, not owner-validated demand. Correctness target is zero endpoint differences in pinned model outputs and zero missed violations; diagnostic 5ps is reported but never grants acceptance. Threshold calibration and 3 independent design families precede candidate runs. Kill on valid originality-equivalence, no matched-information work delta, unsound adapter, absent practical scope demand, rights failure, all-overhead slowdown, unacceptable peak memory or unavailable allocation. None establishes universal abandonment by itself; this candidate has no joint abandonment consent.

## Resource and delivery feasibility (CLM-410)

No new compute is granted. Frozen research-brief.json lists only provisional 8 CPU-hour/4GB/2-CPU pilot caps and a typical-corner GCD fixture; those are not this candidate's allocation or representative PBA data. GCD is a parser/smoke candidate only. No source/build/compiler/container/input hashes for the required PBA adapter, no 3-family manifest, and no human effort estimate exist. Individual benchmark/cell/technology licenses must be checked; public contest repository licensing alone is insufficient. No paid PDK, commercial timer, GPU or API is assumed.

Tasklist.md specifies owners, producers, procedures, oracles, controls, stop criteria and conditional caps. It is deliberately NOT executable today: named source/lock/proof/demand/consent/allocation prerequisites block T05 onward. T00-T04 are documentation/proof/source tasks only. Self-freeze is structural submission, not topic acceptance. Independent C/V can reject or narrow this hypothesis from the complete candid dossier without infrastructure permission requests or another proposer cycle.

## Traceable claim ledger and current gates

| ID | Type | Evidence/locator | Present disposition |
|---|---|---|---|
| CLM-400 | Released historical observation | H-P CLM-047..049; H-C OBJ-003; H-V tables/JSON | Negative predecessor evidence retained; no inherited approval. |
| CLM-401 | Observation plus applicability inference | S04 slides 2/11; S11 pp.603-605; S16 Overview | General demand supported; restricted scope/threshold unresolved. |
| CLM-402 | Proposed model/specification | This proposal frozen model; S08/S09 only adapter evidence | Not a claim of ready full-engine oracle. |
| CLM-403 | New project hypothesis/specification | Paired recurrence above; compare S02/S05/S06 | Structural candidate defined; originality unresolved. |
| CLM-404 | Conditional deduction | Above inequality/full-state recurrence; S08 function locator | Real-model lemma only; executable enclosure unproved. |
| CLM-405 | Analytical witness | W1 above; S01 4.2; S02 3/5 | Separates coarse bound only; no novelty or net-cost witness. |
| CLM-406 | Adverse mathematical deduction | D(y)-D(x)<=Delta; S06 equations 2-4 | Exact scalar pruning at least as strong; central blocker. |
| CLM-407 | Bounded source observations | sources.json + prior-art.csv + contest-audit.md | Coverage/access limits explicit; no universal absence claim. |
| CLM-408 | Hypothesis/unknown headroom | H1/H0 and charged-work equation; S01/S06 model limits | No applicable saturation theorem or measured gain. |
| CLM-409 | Screening requirement/forecast | P-BRIEF; forecast.json | 20% provisional; numerical forecast null. |
| CLM-410 | Resource/rights observation | P-BRIEF; S08/S10/S15/S18; tasklist.md | No allocation, executable locks or representative data. |

Self-declared unresolved gates: novelty, nontrivial contribution, restricted utility, contest-method completeness, headroom, implementation feasibility and task consensus. Initial direction anchor is 0/0 (not independently cleared); this does not pass the other gates. No topic-confirmation or experiment consent is requested. The scientifically complete outcome of this finite job is a candid unresolved successor dossier with a specific strongest alternative and stop test.
