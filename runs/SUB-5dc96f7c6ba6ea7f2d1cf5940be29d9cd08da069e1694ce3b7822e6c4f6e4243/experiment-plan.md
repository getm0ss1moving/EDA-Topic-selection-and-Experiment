# Conditional experimental plan — EDA-0005, round 1

## Status and preregistration

No physical execution or training is authorized by this release. The present evidence supports a hypothesis, not an experiment-ready topic. EXP identifiers correspond to tasklist.md. Before execution, freeze the exact source/PDK/design/SDC hashes, input-generation procedures, candidate generator, template grammar, budgets and stopping rules in an earlier immutable release; obtain both role consents and verifier readiness. No resource is inferred from the historical provisional cap.

H1 (CLM-009): for post-CTS datapath placement moves, incorporating jointly feasible hold-repair edits into selection yields a useful post-route timing/cost tradeoff over the strongest matched conventional composition. H0: same capability is prior; competition is rare; common repair options already suffice; or generation/checking cost destroys benefit. H2: observed benefit depends on explicit shared occupancy/connection constraints rather than extra candidates, calls or better features. H2 is falsified if the strongest ordinary composition matches the result at equal cost. No assumption of super-additivity is required.

## Primary metric and hard constraints

Primary: paired final extracted worst setup slack delta in ns, including positive slack, fixed die and SDC. Provisional screen from research-brief: +0.02 ns, no new hold-violating endpoint, <=2% cell-area/power-estimate regression and <=20% total-runtime increase. Also require no added final route DRC/connectivity/functional/ERC failure. Compare endpoint identities and full slack vectors, not only WNS. At already violating baselines require nonworsening hold WNS/TNS and endpoint violations, with closure rate reported separately; do not relabel an unclosed design as successful closure. Threshold and baseline variance must be resolved before candidate results.

Secondary: setup/hold TNS; number and area of new buffers; moved-cell displacement; rejected/invalid options; rework seconds; global overflow; final route failures; total wall and CPU time, memory, and absolute slack improvement. HPWL/GR scores cannot pass the primary gate. If meaningful runtime rather than WNS improvement becomes the primary objective, this must be reviewed and preregistered before runs; it cannot be selected after inspecting the more favorable metric.

## Versions, data rights and generation

Read-only current OpenROAD inspection: 8da6ac250b0349c346d1abed7c2c43107f4ff6f7. Historical packet executable: b16bda7e82721d10566ff7e2b68f1ff0be9f9e38, OpenLane image efabless/openlane@sha256:840fe28388494220dae9e2be6cf3c7cb2dadfa0eabae4144f0873b9ee949597f. These differ and must not be called the same baseline. Prefer pinning one reproducible release that builds on allocated hardware; if a different revision is required, compare native and candidate in that same revision and preserve old reference results as separate arms. This choice remains EXP-003, not an asserted successful build.

Nangate45/GCD is a pipeline fixture only. S15/S16 offer realistic blockages and a public baseline but are not a ready-made post-CTS hold dataset; generate CTS/initial-GR checkpoints under an explicitly pinned allowed flow, then audit real min/max constraints. Acquire at least three independent design families for eventual paired evaluation, grouping all synthesis/clock/placement variants of one design together. Document licenses of each input, cell library and tool, and output redistribution permissions. Do not publish proprietary netlists, licensed PDKs or paper copies. Original baseline and stressed inputs must both be retained. Artificially tightened hold uncertainty or site caps can be sensitivity tests only, with changed constraints explicitly labeled; they cannot establish typical engineering demand.

No learned model is required in selected C. If B is later evaluated as a comparator, use the same deployable post-CTS features and action representation for joint and separate models. Split by design family, charge label-generation/training costs, hold out tool/PDK transfers, and prohibit post-repair or final-route labels as inference features. Public-benchmark/LLM pretraining contamination remains unknown. A new training allocation would be needed.

## Controlled comparisons

| Arm | Procedure and purpose |
|---|---|
| B0 native | Unmodified pinned flow with its normal repair_timing, legalization and GR/DR policies; reference practical frontier. |
| B1 serial repeated repair | Same movement candidates, choose by immediate timing, run hold repair/legality/route and allow repeated reconsideration under the same budget. Not a one-shot straw baseline. |
| B2 coarse reservation | Equal whitespace allowance and identical movement generator; reserve regions based on total predicted repair demand; use the same repair library and oracle. Operationalization must be faithful to S14 rather than pretending to reproduce inaccessible commercial internals. |
| B3 ordinary joint composition | Same O(X), complete occupancy/connection predicates and finite/MILP solve, implemented as a conventional monolithic selector or eager rollout. This is the strongest direct overlap control; a win over B0 alone is insufficient. |
| B4 constrained buffer planning | Faithful bounded implementation/adaptation of S13 with the same placement perturbation allowance, then identical hold verification. Record formulation differences. |
| C selected | Full action-conditioned joint repair-option interface plus identical final oracle; no extra candidate generator. |
| A optional | AgenticPD v3/official-code-inspired controller, repeated-call single-agent and non-LLM controller with equal information/tools/tokens and EDA budgets. Not mandatory to prove C, since C makes no agent superiority claim. No actual API/model spending is currently approved. |

Use the strongest executable S11/S12/S22-related comparator where its assumptions match; inaccessible source or industrial designs preclude calling a partial imitation a reproduction. EXP-001 determines whether B2/B3/B4 are already enough to establish equivalence. If so, stop before physical runs unless a useful distinct tradeoff remains explicit.

## Mechanism tests and correctness

Ablate explicit inter-repair conflicts; replace action-specific options with total counts; suppress shared-buffer options; remove occupancy feedback while retaining expensive-call counts; use complete eager rollout over the same finite actions; and randomize ranking under equal budgets. The no-sharing ablation tests a modeling weakness, not a novelty claim. Include no-conflict controls and generous-whitespace cases. Report when an ablation improves outcomes.

Finite selector verification: enumerate every assignment in a *declared finite fixture suite*, not every graph up to an unrealistic size. Proposed suite: all 2^9 incidence matrices for three unit repair demands/three unit slots, crossed with all eight enabled-demand masks. Treat each demand as induced by its correspondingly enabled move. For each matrix/mask enumerate all 4^3 assignments (unassigned or slot1/2/3 per demand), enforce enabled coverage, allowed incidence and unit capacity, and compare optimum/feasibility with the selector. This is4096 matrix/mask cases and262144 raw assignment predicate checks; disabled demands must remain unassigned. Add ten individually specified shared-cover/net-split incompatibility cases with their own exact assignment counts frozen in the suite manifest. A correctly rejected restricted table is not a claim about all possible physical repairs. Bundle-dependent O(X) must be regenerated; no stale option or cross-checkpoint certificate.

Physical correctness: verify whole design state after compound edits, including rise/fall min/max timing, fanout and slews, cell legality, net connectivity and buffer equivalence. Full final routing/extraction checks the incumbent; no local sensitivity is treated as proof. On any false certificate, stop exactness claims and repair implementation before subsequent scientific runs. On timeouts, keep baseline/UNKNOWN and charge cost; never drop failure cases.

## Cost ledger and headroom

For every arm record candidate proposals, rejected subsets, option generation, legality, fresh STA/RC, all GR/DR calls, checkpoint copies, solver time, failed actions, fallback, training/LLM tokens if any, CPU time, wall time and memory. Report serial resource work separately from parallel elapsed time. Break down common work G, attributable rework R and interface cost K+V; test the proposal's conditional cost inequality. Compare at fixed wall/CPU budgets *and* equal counted expensive calls; if the rankings differ disclose both. New expensive labels are neither free nor shared only with the candidate.

Smallest prospective allocated witness: one existing legal post-CTS checkpoint, two relocation candidates, <=4 repair templates per bundle, complete physical guardrails; requested cap 2 CPU workers, 4 GiB and 1 wall hour, no GPU/API. Reuse an already acquired executable; compiling a new flow is a separate dependency. A cap miss returns UNKNOWN. This is a future request, not permission or a runtime prediction. Six-candidate exploration is a later scaling tier after this witness.

Eventual screening: three independently selected families, >=5 paired seeds where the flow is stochastic. Deterministic arms share exactly the same seed/checkpoint; duplicated deterministic runs do not create independent sample size. First estimate paired variance/cost on baseline-only inputs, preregister required sample size and request measured-runtime-based resources. Until those runtimes exist the total confirmatory CPU/memory requirement is unknown and no consent is reasonable. Do not claim the tiny witness fits a publication-scale design.

## Statistics, failures and stopping

Use design-family paired differences with family-level uncertainty; seeds are nested replications, not independent designs. Report per-family and pooled intervals, successful fractions, runtime tails and every failure. Choose minimum sample size/power calculation after variance and practitioner threshold, before evaluating C. Three families by five seeds is a screening floor, not a powered generalization claim.

Stop advancement if source-level equivalence defeats the interface delta; no lawful representative witness exists; physical repair competition has negligible incidence; B3 matches C at equal charged cost; proxy gains reverse after DR; or the meaningful primary/guardrail contract is not met. A template-cap failure says restricted coverage, not impossible timing closure. Preserve counterexamples, negatives and exact frozen inputs. Amendments invalidate consent. Current outcome is unresolved/readiness incomplete, not abandonment or acceptance.

## Reproduction artifacts

EXP-003 produces environment-lock.json and input-lock.json with hashes, build/container command, library/SDC/tool flags and license records. EXP-004 produces case.json, baseline.odb, move-options.json, repair-options.json, coverage/occupancy table and fresh oracle reports. EXP-005 produces the selector and comparator source/config hashes, finite-suite manifest and equality report. EXP-007 produces a paired run index, full per-call cost ledger, logs, DEF/Verilog/SPEF and final timing/DRC/equivalence reports. These are future producer artifacts, not files falsely claimed to exist now. Current executable analytical witness is printed with its reproduction code in search-log.md.
