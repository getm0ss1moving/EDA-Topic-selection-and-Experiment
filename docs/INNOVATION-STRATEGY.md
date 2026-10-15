# Innovation strategy: useful combinations and structural contributions

Owner clarification, 2026-10-15: seek high-quality combinations and, where
supported, structural innovations for chip EDA. Multiple agents, learned models,
traditional algorithms and exact analysis may be combined. Explore both
fragmented-to-unified prediction and unified-to-specialized/hybrid analysis.
Neither more agents nor a larger unified model is an objective by itself.

This policy clarifies contribution evaluation and direction penalties for future
packets. It does not revise frozen verdicts, accept a candidate, reopen the
completed four-round batch, or allocate experiments, GPU time or API spending.

## What qualifies

Both routes are eligible:

- **Useful combination:** known components provide an identifiable new
  interaction, formulation, reliability/cost tradeoff, guarantee or practically
  useful capability not established by the strongest applicable prior systems
  or their straightforward composition under comparable conditions.
- **Structural contribution:** a changed representation, information flow,
  optimization problem, decomposition or invariant explains a new capability or
  tradeoff. A changed diagram alone establishes neither novelty nor value.

Not every component must be new. Mathematical novelty and super-additive gains
are not mandatory for a systems contribution. Conversely, a new benchmark win,
more samples, extra agents, better inputs or extra compute do not by themselves
identify a research contribution. State what is new at the system level and test
the claimed distinction. Ablations identify causality; they are not a requirement
that every component independently improve every metric.

The combination_drift field measures degradation or replacement of the frozen
contribution, not the number or origin of components. Adding AI, reusing a known
solver, or starting with a well-motivated combination is not automatically drift.
An anchor-preserving implementation repair can score zero. A genuinely different
mechanism starts a new topic, keeping the predecessor's negative evidence.

Distinguish a research-worthy hypothesis, experiment-ready plan and demonstrated
publication claim. Discovery may propose a plausible mechanism plus a decisive
test while results remain unknown. Missing measurements or unallocated hardware
block readiness or performance claims, not legitimate source reading or idea
formation. Do not demand a completed full-flow result before allowing a
hypothesis, or treat an unresolved premise as an established impossibility.

## Two kinds of agents

Scientific proposer, challenger and verifier remain independent and exchange only
their explicitly released outputs. In contrast, agents inside a proposed EDA
algorithm may coordinate, share a declared design state and exchange algorithmic
messages. That communication is part of the method to specify and evaluate.
It does not authorize access to another scientific role's private material.

Specify each algorithmic agent's observations, actions, shared state, feedback,
conflict resolution, termination and invocation cost. A role name is not a
specialization mechanism. Compare collaboration to a strong single agent with
the same information/tools and repeated-call budget, ordinary parallel search
and an appropriate non-LLM controller. Charge tokens, EDA calls, failed actions,
communication, checkpoint work and total elapsed/compute cost.

## Discovery directions, not approved topics

| Direction | Engineering question and candidate mechanism | Decisive comparison / failure condition |
|---|---|---|
| Fragmented to unified prediction | Can a shared circuit/physical-state representation capture a specific timing, congestion, clock or power interaction that separate predictors and ordinary fusion miss? Select a bounded subset and a real downstream decision first. | Separate specialists plus fusion, shared-trunk multitask baseline and strongest task-specific methods under the same labels/features/training budget. Stop the universal-model claim if negative transfer or downstream decisions are worse. |
| Unified to specialized/hybrid analysis | Can a controller choose when to use a cheap predictor, a specialist, an incremental computation or a declared exact engine from the actual decision risk and value of information? | Strong multi-fidelity/adaptive baselines, fixed scheduling and the full reference flow, all with charged overhead and fallback. Merely adding uncertainty or a checker is not new by itself. |
| Cross-stage cooperating agents | Can explicit propagation of a stage decision's downstream consequences improve closure over stage-local tuning without conflicting edits or repeated expensive reruns? | Stage-aware agent systems, single-agent repeated calls, conventional search and checkpoint reuse. Attribute benefit to coordination/state/credit assignment rather than extra trials. |
| Prediction-guided exact work | Can learning rank or schedule expensive subproblems while a justified invariant/checker preserves a precisely stated correctness property? | Strong exact heuristics and the same learned-plus-checker composition, with all proof/check/fallback costs. Stop an exactness claim on one invalid certified decision. |

For each discovery candidate, name one bottleneck and user action, the closest
mechanisms, the proposed information/interaction delta, the strongest alternative
explanation, a cheapest decisive test and its expected resource request. These
are search lenses, not evidence that the combinations are novel.

## Prediction and exactness contracts

Use distinct claims:

1. **Approximate prediction:** specify target, units, error distribution, tails,
   calibration and out-of-distribution limits. Better RMSE need not improve ECO
   selection, timing closure, route legality or the final PPA frontier.
2. **Probabilistic guarantee:** state assumptions, coverage event, confidence and
   scope. Calibration on evaluated data is not an unconditional exact guarantee.
3. **Engine-relative exact result:** identify the pinned engine/model/domain,
   operations, report semantics and oracle. A learned guide may propose work;
   sound decisions require the stated correctness argument and validated
   implementation. Unsupported cases must be explicit UNKNOWN or use a valid
   fallback, with all work charged. Domain-restricted exactness is not foundry
   signoff or proof of globally optimal PPA.

Unified prediction is a hypothesis, not a preferred architecture. Specialists,
analytical methods and selective exact computation remain eligible. Separate
training-time privileged labels from deployable inputs; final-route information
cannot silently enter an earlier-stage prediction. Split by independent design
families and group variants/checkpoints of the same underlying design. State
PDK/tool/corner coverage and any public-benchmark or LLM pretraining contamination
uncertainty. Treat offline accuracy and closed-loop decision quality separately.

## Evidence and progression

Use a staged evidence ladder: source mapping and analytic witnesses first;
bounded synthetic/source-level checks or small prototypes when allocated; then
representative held-out full-flow evaluation after dependencies and matching
task-list consents are satisfied. An unsuccessful cheap test is useful evidence.
No universal numerical target or success probability is supplied by this policy.

The challenger must identify the exact allegedly routine reduction, missing
capability or unfair comparison. "Uses known methods" is not sufficient evidence
against a useful system contribution. The verifier checks the claimed system
delta and the objection equally, separating a valid conditional lemma, a plausible
engineering hypothesis and demonstrated useful novelty. Existing novelty,
demand, headroom, cost and consent gates remain in force.

## Initial prior-art leads

Retrieved 2026-10-15 by the coordinator for policy orientation only. These are not
an independent topic verification or an exhaustive search. Paper access here is
limited to the author-supplied abstract/metadata; full-method and code audits
remain tasks for future assigned roles. No reported speedups were reproduced.

| ID | Primary source / version | Inspected locator and limited implication |
|---|---|---|
| STRAT-S01 | [ChatEDA](https://arxiv.org/abs/2308.10204v4), v4, 2024-09-21; first submitted 2023-08-20 | Abstract: task decomposition, script generation and execution with an LLM and EDA tools already exist. This is not an audit of its full method or performance. |
| STRAT-S02 | [EDAid](https://arxiv.org/abs/2502.10857v1), 2025-02-15 | Abstract: multi-agent collaboration for EDA flow automation is prior. Agent count alone is not a new mechanism. |
| STRAT-S03 | [AgenticPD](https://arxiv.org/abs/2607.04758v3), v3, 2026-10-04; first submitted 2026-07-06 | Abstract: stage-aware orchestration, stage agents and structured execution history are close prior leads. Do not claim these generic features are new or adopt its advertised gains as measurements here. |
| STRAT-S04 | [OpenROAD DSE documentation](https://openroad.readthedocs.io/en/latest/contrib/DesignSpaceExploration.html), current page, revision/date unspecified | Full page, especially sections 2, 3 and 6: cheap estimates, full-flow signals and multi-fidelity search already have established context. Dynamic documentation must be version-locked before an experimental comparison. |
| STRAT-S05 | [GR/DR timing consistency](https://arxiv.org/abs/2305.06917v1), 2023-05-11 | Abstract: learned post-GR prediction informing post-DR timing outcomes is an existing direction. No reproduced result, unified-model theorem or contemporary superiority follows. |

Orientation queries covered ChatEDA/multi-agent EDA, unified physical-design
prediction and OpenROAD tuning. Primary sources above were opened; secondary and
off-topic search hits do not support claims. Future roles must expand terminology,
citations, task-specific exact/hybrid methods and current contest/winner material,
then record source versions and actual access. Do not infer novelty from this
short list or merely rename these systems.
