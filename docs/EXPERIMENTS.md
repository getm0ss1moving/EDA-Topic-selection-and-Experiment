# Experimental contract

## Preregistration

Before evaluating the proposed method, freeze hypotheses, primary metric/direction, constraints, meaningful effect threshold, baseline versions, tuning budget, splits, repetitions, statistical method and stop rules in a reviewed plan. Distinguish a mechanism pilot from a confirmatory evaluation. Record amendments before collecting the affected results.

## EDA controls

Pin tool commits/versions, scripts, PDK/library/design/corner versions, SDC constraints, extraction settings, hardware, threads, memory limits and seeds. Validate equivalence, legal placement/routing, DRC/LVS or specification correctness as appropriate. Report failures and infeasible runs, not just successful designs. Compare complete flow endpoints and disclose any unavailable signoff oracle.

Measure downstream PPA/quality together with wall time, peak memory, engineering effort where measurable, and all optimization costs. For AI include data generation, training, fine-tuning, inference, API cost, tool calls, retry count and amortization horizon. For agents, count unsuccessful trajectories and require verifiable artifacts rather than narrative success.

## Baselines and statistics

Use a strong reproducible baseline and a closest-prior mechanism baseline. Add simple composition, component removal, equal-budget search and oracle/upper-bound studies when meaningful. Tune competitors comparably. Hold out design families rather than random near-duplicate fragments. Audit contamination, generator overlap and optimization on the test set.

Choose repeated seeds and sample sizes from pilot variance and an effect-size/power argument; three seeds is not automatically adequate. Report per-design results and uncertainty, pair comparisons when designs match, disclose multiple comparisons, avoid treating correlated designs as independent. Report Pareto tradeoffs and constraints rather than hiding regressions behind aggregate scores.

## Forecasts and stopping

Forecasts contain pessimistic/base/optimistic effect estimates, units, baseline reference, assumptions, confidence, and reasons for each range. Unknown values remain null with an evidence-collection task; never present them as measured improvements. Calibrate previous forecasts against measured results using the same metric and budget.

Stop or revise when correctness fails, meaningful effect is below threshold, claimed novelty collapses, compute exceeds budget, or dependencies remain inaccessible. Negative results are valid artifacts. The task list must include dependency order, owner role, budget, command or procedure, output and pass/fail criterion for every experiment.

No experiment may begin while either direction-drift penalty is 2 or above, their total is 3 or above, or `direction_integrity` is false. These are governance blockers and cannot be traded against forecast PPA, runtime, benchmark or model improvements. Restore the frozen anchor or complete the joint-abandonment process first.

No experiment may begin until proposer and challenger have jointly completed the final task list and independently signed the same task-list SHA-256 and frozen revision in `experiment-consensus.json`. All readiness checks must be true, the verifier must validate the consensus gate, and the topic must be promoted through the normal review gate. Any task-list amendment invalidates the old consensus and pauses execution until both roles sign the new version.

## Preparation versus research execution

Literature review and static analysis may proceed under the assigned brief. Tool installation, data preparation and bounded correctness/property checks require an explicit scoped allocation (purpose, host, network policy, CPU/memory/time/storage limits and output provenance). A runner category string is not scientific authorization. These checks cannot be relabelled speedup, real-design headroom or QoR experiments to bypass consensus. Record failed checks and do not infer a universal theorem from finite tests. A machine safety ceiling is not a spending allocation.

Bind plan dependencies in `tasklist.md` by content or SHA-256 (baseline versions, metrics, thresholds, budgets, data splits, oracle and stop rules). The verifier checks these against the current files before acceptance. Changes to any bound dependency invalidate both consents; the coordinator pauses execution. Report timeouts, missing runs, negative results and total cost. Final experiment reports identify the frozen plan and all deviations and receive human review under `reports/final/` or the accepted topic directory.
