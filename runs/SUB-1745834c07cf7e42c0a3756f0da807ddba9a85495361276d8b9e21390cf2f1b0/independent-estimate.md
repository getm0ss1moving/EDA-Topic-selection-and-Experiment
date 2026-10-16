# Independent estimate and C-A02: coalesced values versus dependency provenance

Unblinded research review. Proposal prose, A03 code and reported output were inspected; forecast.json was not opened. No numerical speedup prediction is warranted. Current normalized Q/B5 computation parity is plausible by induction for identical complete keys, deterministic operations and lifetime choices; layout/gathering overhead is outside that correspondence. Proposer A03 was inspected, not executed or independently certified. Its logical bytes are not resident bytes.

C-A02 is a new challenger-authored finite model, not an OpenSTA run or a replay of historical scripts. It tests a more explicit D2 acceptance condition: merging equal current values must not erase branch-dependent invalidation provenance. C03/C04 supply the motivating annotation/parasitic branch; this arithmetic model deliberately abstracts its numeric semantics. A provenance union is sound but can over-invalidate; per-world provenance can be precise. Both are available to a conventional executor. Neither supplies Q-only novelty. A representative-only dependency set is intentionally incorrect, not alleged to be present in the proposal.

Exact executable code (Python standard library, no external inputs):

```python
import json
from itertools import product
cases=failures=0
witness=None
for pin,rc,delta in product(range(1,4),range(1,4),[1,2]):
    annotation=pin+rc
    old=[pin+rc,annotation]
    deps=[{'pin','rc','annotation_presence'}, {'annotation','annotation_presence'}]
    truth=[pin+rc+delta,annotation]
    # Both values initially coalesce; choose annotated world as representative.
    representative_deps=deps[1]
    dirty='rc'
    bad=list(old)
    if dirty in representative_deps:
        bad=list(truth)
    union=set().union(*deps)
    conservative=list(truth) if dirty in union else list(old)
    precise=[truth[i] if dirty in deps[i] else old[i] for i in range(2)]
    assert old[0]==old[1]
    assert precise==conservative==truth
    cases+=1
    failures+=bad!=truth
    if witness is None:
        witness={'old':old,'truth':truth,'bad_representative':bad,
                 'union_recomputed_worlds':2,'precise_recomputed_worlds':1}
print(json.dumps({'cases':cases,'representative_failures':failures,
                 'safe_union_and_precise_agree':True,'witness':witness},sort_keys=True))
```

The output and exact code/output hashes are appended after execution below. Reproduction: extract the first Python fence and execute it with Python 3. It enumerates precisely the domains in product(...); no random seed or engine inputs exist.

Interpretation: equal-result partition identity and complete-key/dependency identity are different relations. Safe implementations may retain the union, preserve per-world records, or invalidate the whole epoch. Charge the chosen representation and invalidation granularity in B5 and Q. Whole-epoch invalidation is conservative and allowed; this model does not demand an unproven fine-grained optimization. Fail D2 only if a declared supported update returns stale output; over-invalidation is a cost measurement, not a correctness failure.

Headroom: unknown. Cold unlimited same-key primitive counts cannot favor Q under the stipulated correspondence. Full-output materialization creates a conditional common floor only if the actual consumer requires it and accounting is equal. No calibrated floor fraction, total time or memory-cap crossing is known. No theoretical saturation or general impossibility follows.

## Observed C-A02 output

```json
{"cases": 18, "representative_failures": 18, "safe_union_and_precise_agree": true, "witness": {"bad_representative": [2, 2], "old": [2, 2], "precise_recomputed_worlds": 1, "truth": [3, 2], "union_recomputed_worlds": 2}}
```

Code SHA256: `b0c5f457e41d858a2a29bf349ef4b6a435eac7939566b04719c7ff6767c211ae`.
Stdout SHA256: `d88ad2e4510a6781cc093ba8d772d8d3953f8c66ed16aeb66c3b0971e512c032`.
