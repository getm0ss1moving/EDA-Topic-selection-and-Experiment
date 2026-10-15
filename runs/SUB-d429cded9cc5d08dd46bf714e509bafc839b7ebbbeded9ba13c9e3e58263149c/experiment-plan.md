# EDA-0006 R3 — completed witness pass and inactive experiment plan

## Hypotheses, metric and progression

H1 remains conditional: an unchanged-kernel complete-state candidate-mask adapter might provide a useful required capability or fully charged cost/reliability benefit beyond faithful adapted B++. H0: B++ supplies the same capability and operation/storage policies, and any measured difference is ordinary adaptation/constants. H2: the frozen full-vector output serves a decision not equally supported by a smaller exact query. H0-demand: required decision has a sufficient smaller query. R3 found no H1 witness; the tested prospective protection rule fails the full-materialization inference. Recommend park. These are research findings, not measured performance or readiness.

If resurrected, primary metric is total wall time in seconds to identical per-candidate endpoint results and unchanged caller decision; smaller is better, subject to correctness, peak memory and full legality/guard controls. A meaningful engineering threshold and variance must be justified by a real consumer before confirmatory work. No numeric benefit target or sample-size claim is adopted here. R2's provisional 20% is not validated demand. Forecast intervals remain null.

## EXP-000R completed source/analytical procedure

Read S21 selected functions, S20 §2.1/environment boundary, S05 Fig.7 and S27 kernel/closure chain. Construct the read/operation/lifetime matrix and a_q,b_q,l_q,k_q,u_q,z_q ledger in proposal.md. Match adapters, immutable identities, bitset/context encoding, scheduling, cache eviction, output report and recovery. Falsifier: one required operation/capability or live-state lifetime that the faithful adaptation cannot equally realize under the same resources, or an evidenced useful implementation tradeoff. None identified. This is a finite source audit, not a cost measurement or universal impossibility proof.

## EXP-001R / EXP-006B completed consumer analysis

Reopen S23–S25. Specify the prospective endpoint protection rule and test both aggregate insufficiency and scalar guard sufficiency. The complete self-authored stdlib check below has SHA256 `2795a570a2792227ddd347fa64363a699f739bf28b5b35c71daf8f9e504fb7d1`. Save the code fence as `check_r3.py` outside the checkout and run `python3 check_r3.py`. No source repository code is executed.

```python
from itertools import product
import json
A, B = (-1, -3, 4), (-3, -1, 4)
threshold = (-2, -4, 0)
def summary(s):
    return (min(s), sum(min(x, 0) for x in s),
            tuple(i for i, x in enumerate(s) if x < 0))
def vector_guard(s):
    return all(x >= t for x, t in zip(s, threshold))
def scalar_margin(s):
    return min(x-t for x, t in zip(s, threshold))
assert summary(A) == summary(B) == (-3, -4, (0, 1))
assert vector_guard(A) and not vector_guard(B)
assert (A[0] >= -2) and not (B[0] >= -2)
records = list(product(range(-3, 5), repeat=3))
for s in records:
    assert vector_guard(s) == (scalar_margin(s) >= 0)
candidates = [('A', A, 2), ('B', B, 1)]
def choose(guard):
    legal = [c for c in candidates if guard(c[1])]
    return min(legal, key=lambda c: (c[2], c[0]))[0] if legal else None
assert choose(vector_guard) == choose(lambda s: scalar_margin(s) >= 0) == 'A'
assert min(candidates, key=lambda c: (summary(c[1])[:2], c[2]))[0] == 'B'
print(json.dumps({'scope':'synthetic integer slack records; not circuit or timing execution',
    'same_summary':list(summary(A)[:2])+[list(summary(A)[2])],
    'vector_guard':[vector_guard(A),vector_guard(B)],
    'scalar_margin':[scalar_margin(A),scalar_margin(B)],
    'finite_guard_checks':len(records), 'guarded_choice':'A',
    'summary_area_choice':'B', 'full_vector_necessity_proved':False},sort_keys=True))
```

Observed output:

```json
{"finite_guard_checks": 512, "full_vector_necessity_proved": false, "guarded_choice": "A", "same_summary": [-3, -4, [0, 1]], "scalar_margin": [1, -1], "scope": "synthetic integer slack records; not circuit or timing execution", "summary_area_choice": "B", "vector_guard": [true, false]}
```

The calculation enumerates 512 integer slack records; time was not used as a metric. It does not validate circuits, physical realizability, model error, FP equality, scalar timing state, restoration, memory caps or real design performance. It grants no EDA allocation. The prospective guard is a demand probe, not a replacement output contract.

## Conditional future experiment, entirely inactive

After BOTH positive resurrection witnesses survive independent review, assign implementation owner I and independent reproducer R explicitly. First pin mutually compatible recursive OpenROAD/OpenSTA sources, compiler/FP/container/CPU, SDC/Liberty/SPEF hashes, reference-kernel mode, candidate generator and original order. Current source pins 8da6ac250b0349c346d1abed7c2c43107f4ff6f7 and 49b86c95b31c53ba9096b91ef384ae5406b3107c are audit versions, not proven compatible binaries. Complete transitive read-set/immutable closure, mutation/invalidation, exception and FP tests; unsupported cases replay from the original base and UNKNOWN never passes.

Use rights-cleared workload traces from at least three independent public design families, variants/checkpoints grouped together. Exact batch distribution, applicable slice fraction, provenance/license manifest and tool/PDK access remain unresolved. No learning or training labels are used; public benchmark familiarity can still bias tuning. Predefine held-out families, fixed candidate lists and correctness outputs before performance tuning.

Strong B++ = finite conditional execution + transaction/incremental STA + complete-key cache/output interning + same sparse lifetimes/tasks/recovery. B+ per-lane memoization is diagnostic only. Naive serial fresh and strong scalar incremental are context baselines. A faithful scalar loop with equal information is mandatory. Same kernels, hardware, memory/cache budget, candidate order, report materialization and guard. Separate common adapter construction/read-set work from any genuinely different work; charge load preparation, extraction, failed attempts, masks, key bytes, equality, output expansion, checkpointing, replay and full-context final checks. No handicapped Java-vs-optimized-C++ comparison.

Ablate only the surviving claimed delta and retain correctness. Report all cases, including no-reuse and orthogonal contexts, small batches, cap/fallback, hash collisions, signed zeros, NaNs, tags, reconvergence and dirty/base-equal boundaries. Predefine paired order/randomization and warm/cold cache procedures; choose repeat count from an allocated baseline-only variance pilot rather than inventing n now. Do not launch any full-flow, GPU, training, remote or paid API job. Resource requests and realistic executable commands belong to a later accepted environment lock/allocation, not placeholders represented as readiness.

Stop before implementation now. Future one false certified result stops exactness; absent witness stops advancement; later failure to meet justified downstream benefit records a negative result. Changes to task list/dependencies require fresh matching signatures on an earlier immutable release. No proposer or challenger agreement exists for this R3 plan.
