# Frozen future task list: EDA-0009 B4-R1

This list is a conditional dependency DAG, not authorization to execute EDA or train. Actual CPU/GPU/remote/paid allocations: **null**. Existing research reading and the tiny own replay EXP-101 are the only work executed here. Owner batch policy adds four research cycles, not compute. The historical 8 CPU-hour screening cap in research-brief.json is explicitly provisional and is not adopted as allocation.

All future implementation owners below mean a later named, allocated implementation seat. P/C/V must independently review and sign the exact earlier frozen revision and this file hash before any experiment requiring consent. No current signature agrees. Preserve the fixed pool, common checkpoint, oracle, full cost accounting and every negative outcome. Do not alter generation to increase overlap after inspecting incidence.

## Dependency graph

EXP-100 (allocation/rights/consent; CLOSED) gates any build, instrumented physical replay, training or full-flow work. EXP-101 and source-only EXP-102a may precede it. The later execution order is:

    EXP-102a source/semantic inventory -> EXP-102b adapter correctness
    EXP-100 + EXP-102b -> EXP-103 candidate census and cost decomposition
    EXP-103 + EXP-104 preregistered estimator/baseline implementations -> EXP-105 pilot
    EXP-105 + EXP-106 threshold/family lock -> EXP-107 held-out evaluation

EXP-104 pure interface/algorithm specification can proceed as research, but its physical labels/training require EXP-100/103. EXP-106 must freeze thresholds before candidate-arm results, using separate calibration families. EXP-107 cannot run until both EXP-105 and EXP-106 finish.

## EXP-100 — authorization, exact inputs and fair-plan binding (CLOSED)

Owner: human resource owner supplies allocation/rights; scientific proposer and challenger sign only their own consent later; verifier checks. Inputs: this release, owner policy and no assumed external license. Procedure: record a named runner; real CPU time, memory, concurrency and storage limits; tool/container/config source hashes; every design/technology/SDC/library/checkpoint license and SHA-256; permitted use and redistribution; exact tasklist SHA-256 and earlier SUB revision signed by each role. Record cold/partial/complete-warm K0 construction procedure and costs for each arm. Do not equate a baseline marker report with Q0 certificates. Artifacts: allocation.json, inputs.lock.json, rights.md, two original consent files and verified consent report. Pass: actual non-null allocation, permitted data and matching exact-task independent agreement, all applicable eight gates checked. Fail: gate stays CLOSED, no execution. Request scope must separately identify source work, build, bounded adapter smoke, label generation, training and downstream evaluation. No number here spends a provisional cap.

## EXP-101 — public analytical witness (DONE in this role; tiny Python only)

Owner: this proposer, present research permission. Input: exact fenced Python block and parameters in search-log.md; script SHA-256 924393c7489f840ef9c530d7740f88ddd2ac4b7b8a0dacae62cd3231de5c5d25. Reproduce from released bytes in an own temporary directory:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, subprocess, tempfile
text=Path('search-log.md').read_text()
code=text.split('<!-- REPLAY-CODE-BEGIN -->\n```python\n',1)[1].split('\n```\n<!-- REPLAY-CODE-END -->',1)[0]+'\n'
assert hashlib.sha256(code.encode()).hexdigest()=='924393c7489f840ef9c530d7740f88ddd2ac4b7b8a0dacae62cd3231de5c5d25'
with tempfile.TemporaryDirectory() as t:
    p=Path(t)/'analysis.py';p.write_text(code)
    out=subprocess.check_output(['python3',str(p)])
    assert hashlib.sha256(out).hexdigest()=='e1f21ff654d703239071b42a1a8a050e20d442898445889b248133aab3521f1d'
    print(out.decode(),end='')
PY
```

Outputs: 1,500 support/residual-pair assertions, 500 common-kernel identity cases, sparse/positive/empty-query fixtures and exact stdout hash. Resource: subsecond own run observed; no timing performance claim. Oracle: direct full tuple/query enumeration in the script, not OpenROAD. Pass: exact hashes/stdout and no assertion failure. Fail: withdraw affected analytic claim; never repair by suppressing a generated counterexample. This does not validate 2D polygons, OpenROAD dependencies, real overlap or cost.

## EXP-102a — source-only novelty and coverage audit (partially DONE)

Owner: next authorized scientific research role, public reading only. Inputs pinned in sources.json: OpenROAD b16bda7e82721d10566ff7e2b68f1ff0be9f9e38 and source hashes; Dr. CU 3d81988d741da36d2612f3443165970e0125bccc; B4-S01–S16. Procedure: trace checkDRC -> getDRCMarkers -> worker init/main -> every applicable rule-family entrypoint and derived geometry/query dependency. Produce one row per rule with (entrypoint, global prerequisites, target-net scope, query geometry, negative result dependencies, complete output, safe support construction, fallback). Reopen clean-certificate and selective-dispatch paths; do not infer a public API from a header or ignore flag. Inspect min-area gates and other invocation-specific coverage, without declaring an engine bug from one branch. Complete forward/backward citations on Dr. CU pessimistic LUT, incremental hierarchy/dependencies and value-of-information/lazy baselines; seek original contest presentation/binary correspondence and original CN122839978A text legitimately accessible. Newer official 2025/26 contest pages must be reopened before promotion.

Artifacts: rule-coverage.csv, source-locators.json, baseline-reduction.md, rights additions. Pass for 102b: an explicit small rule subset admits a complete dependency/output model and independently runnable reference; no missing closure-critical output. Source unavailability remains unresolved. Fail: no spacing-only certification of all-rule cleanliness; reject adapter path if it cannot soundly isolate supported work. A source plan alone does not pass readiness.

## EXP-102b — implement and validate the selective interface (NOT EXECUTED)

Owner: future allocated implementation seat. Dependencies: 100,102a. Do not run downloaded source merely because it can be read. Generation procedure: start from the pinned engine commit; record patch/config hashes; implement an observer that records each supported anchor/rule/query slot, **all** query results including empty, canonical payload and marker provenance, plus an exact replay path with no shared mutable candidate state. Disable surgical mutation during pure checks or record all induced edits and recalculate supports. Add a baseline certificate extraction mode and coverage ledger; record enumeration/materialization/checking time separately. Implement marker deletion/regeneration and connectivity validation; full unaffected baseline markers persist.

Adversarial cases: insert into formerly empty halo, delete neighbor, move over boundary/grid, split/merge polygons, net relabel, via/master change, hierarchy transform, rule/config change, unsupported derived/global rule, source-ID renumber and hash collision. Each must invalidate dependent keys or return UNKNOWN/full fallback. One record per slot or explicit multiplicity bound is required for the support bound. Compare entire canonical marker/source tuples and connectivity partitions against a fresh full reference per candidate, not counts. Validate every recorded clean result as well as violating results. Freeze oracle invocation semantics and rule coverage. Artifacts: adapter patch, instrument config, replay command, small legal fixture generator, per-case inputs/output hashes, complete marker/connectivity diff, full fallback cost, dependency audit. Pass: zero false reused/certified output and exact named-oracle equality on all controls, with unsupported work properly charged. Fail immediately on one false certificate; no acceptance claim. Resource stop: exact allocated smoke timeout/memory ceiling from 100; if absent do not start.

## EXP-103 — baseline-relative incidence census before learning (NOT EXECUTED)

Owner: future implementation seat. Dependencies:100,102b. Use three or more independently selected legal design families if available; lack of representative cases is blocking. For each family freeze five or more checkpoint/seed variants before arm comparison, grouping all variants in one split. Candidate generator is a pinned deterministic same-net repair procedure, at most16 siblings per checkpoint, exact generation command/config/script hashes; record actual net/shape deltas, induced incidental edits and output hashes. Do not cherry-pick overlapping candidates or drop no-overlap/failed instances.

Execute cold, partial and complete-warm K0 as separate regimes with identical initial bytes in all arms. Charge construction once per actual pool and report whether/how amortized across repeated pools; no free warm-up. Record raw-common, baseline-common, novel-common, candidate-unique work and E-intersection bounds; measure canonicalization, serialization, query traversal, lookup/invalidation, predicate execution, fallback, memory and final check. Keys require byte equality; global state/candidate IDs cannot be included just to destroy reuse, nor excluded if semantically necessary. Artifacts: pool-manifest.jsonl, incidence.jsonl, full cost-ledger.csv, failure ledger and rights/versions. Pass for mechanistic economics: a representative residual saving distribution survives total discovery/fallback cost under a threshold preregistered without seeing arm outcomes. Fail/no-headroom regime: zero residual sharing or net-negative administration; preserve it. Do not turn a failed sampled regime into a universal impossibility theorem.

## EXP-104 — implement common kernel, acquisition arms and fairness locks (NOT EXECUTED)

Owner: future implementation seat; scientific approval remains P/C/V work. Dependencies for source-only interface specification:102a. For fitting/physical comparisons:100,102b,103. Implement common singleton/pair enumeration, deterministic ties/updates, deadline and reserved final-oracle work. Record arrays/observations and verify byte-identical choices when information is identical. Merge duplicate policies rather than counting their names as distinct baselines.

Freeze six acquisition/estimator arms: A eager payload discovery; B deterministic support-gated conventional lazy acquisition; C equally informed generic value-of-information/factorized controller with identical slot graph and query operations; D same-feature separate predictors plus fusion; E equal-budget shared-trunk/direct-set model; F proposed candidate-slot factorization and group acquisition. A centralized F gets the same data/tools as any specialist-agent wrapper. Compare B/C as strong baselines, not only A. Freeze encoder dimensions, optimizer/training steps, ensemble size, observation masks, calibration bins, family splits, random seeds, feature hashes and inference/query budget before outcomes. Proposed first audit configuration: a deterministic nonlearned controller without fitting; learned capacity is fixed only after real label costs are known. This is an unresolved specification prerequisite, not current agreement.

Controls: full K0 vs cold/partial; remove negative dependencies (must fail soundness fixture); raw-overlap vs residual features; no acquisition vs eager; same exact observed table across arms; no cache vs same cache; destroy cross-candidate association while keeping individual features; oracle incidence (diagnostic upper bound only, charged/excluded from deployable comparison); shuffled same-family labels forbidden across splits. Train from full reference labels generated under100; unobserved/censored labels never become negatives. Artifacts: implementation/config hashes, kernel-identity output, leakage audit and query trace schema. Pass: identical work budgets/information access and bounded complete-output interfaces; fail on oracle feature leakage, unequal cache or uncharged calls.

## EXP-105 — bounded end-to-end pilot (NOT EXECUTED)

Dependencies:100,102b,103,104. Owner: allocated runner seat. Execute each arm on exactly the same frozen candidate pools, with paired seeds, CPU/thread policy, memory cap and hard deadline. Count all failures/timeouts/partial work; never credit a partial candidate as checked. Report time to first fully checked target and best fully checked result at deadline, with right-censored failures and end-to-end cost. Include final chosen-state whole-design reference, independent connectivity and extracted setup/hold timing at fixed SDC/corner, area and estimated-power guards. An engine-empty report is named-engine/config scoped; foundry signoff is not claimed. Artifacts: complete invoke manifest/log hashes, canonical outputs, cost ledger, all failures. Stop at allocated limits. Pass only as a pilot if correctness holds and net cost is measured; pilot alone does not establish publication novelty or utility.

## EXP-106 — meaningful endpoint/threshold preregistration (NOT EXECUTED)

Owner: scientific proposer/challenger with practitioner evidence if available; verifier checks. Dependencies:102a and separate calibration data allowed by100; freeze before arm evaluation or held-out unmasking. Specify how a target is chosen when none of16 candidates closes the block; use time-to-checked-target survival analysis and deadline complete-result quality, not discarded failures. Fix the minimum useful wall-time/quality tradeoff, confidence interval method, family aggregation and timing/DRC/connectivity guardrails. Provisional brief values are not proven route-checking requirements. Record user evidence or label thresholds research-screening assumptions. No chosen-after-results threshold. Artifact: endpoint-lock.json with inputs/config/script hashes and hash timestamp. Fail: no confirmatory utility claim.

## EXP-107 — held-out test, replication and decision (NOT EXECUTED)

Dependencies:100–106 all passed with frozen exact-task consents. Owner: allocated runner; independent scientific review afterwards. Execute the same complete workflow on unseen design families and every preregistered checkpoint. Include paired bootstrap intervals by family, design-level tables and uncensored failures. Report setup/hold slack, route report coverage, connectivity, wire/via/area/power, elapsed/CPU time, bytes/memory and paid model/query overhead (zero only if genuinely none). No new design-generation, label or training budget can appear here without updating the task list and consents.

Mechanism falsification: if C (ordinary same-information acquisition) matches F within the frozen meaningful interval, the new-mechanism claim fails even if F beats A. If representation ablation does not change observations/decisions/cost, no attribution to incidence factorization. If residual sharing cannot cover administration/fallback, reject that economic regime. Exactness falsification: any false reused result, omitted violation or invalid connectivity is an immediate stop. A successful candidate requires independent source/novelty/utility review, all eight gates and no direction drift; it is not automatic from benchmark rank. Preserve negatives and unresolved limits; later park or joint abandonment must follow the distinct policy procedures.
