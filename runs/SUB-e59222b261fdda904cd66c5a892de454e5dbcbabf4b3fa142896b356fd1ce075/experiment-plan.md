# Mechanism, provenance costs and conditional future experiment

## Equal-information controls

B0: isolated fresh reference for every requested candidate; B1: conventional journal/incremental reference with verified restore; B2: complete-key memoization; B3: ordinary scheduling/cache/lifetime policies; B4: strongest applicable variational formula-map/MTBDD execution, including canonical DAG application and sparse joining; B5: equally specialized conventional executor receiving Q's same support/index/controller kernels, keys, information, lifetime policy and cap. Q retains operation-specific exact partitions/split/re-coalescence. These are future definitions, not built engines. Match arithmetic, full values/statuses, declared phases, inputs, available features, actual byte cap, complete output demand and fallback. Adapt B4 equality for floating bit/status identity; audit candidate-universe restrictions and maxInteractionDegree instead of silently pruning requested worlds. B0/B1 remain full-output references; R28's scalar local scoring is context and a component comparator, not an interchangeable oracle.

The previous normalized correspondence and A03 lifetime result remain historical author evidence in SUB-017839... experiment-plan.md. No old code was rerun. Same-key primitive parity under pure complete keys/adequate cold cache is retained; neither index nor lifetime rename creates extra primitive savings.

## S1 maintenance/action map

| Action/state | Q | Strong conventional transplant | Required cost |
|---|---|---|---|
| Exact current value classes | membership->full value/status | identical value map/MTBDD | compare/coalesce and membership encoding |
| Future validity | dependency/negative-query incidence retained independently of value equality | identical per-world provenance or inverse index | recording reads, annotation existence, epochs, reverse edges |
| Changed dependency | look up affected memberships, reevaluate invalidated records, re-coalesce | same index, same dirty sets and actions | index construction/probe/update/removal, result output |
| Conservative alternative | union provenance across equal-value class | allowed in both | extra invalidated work plus lower/different metadata cost |
| Lifetime/cap | last-use release, declared eviction/recompute | same cap/policy/available history | metadata, checkpoint/recompute and output lifetime |

This map supplies no Q-only action. Complete dependencies, purity and restored state still need engine extraction. Conservative whole-epoch invalidation can be correct; its extra work is an economic issue. Do not present selective invalidation as necessary for correctness when union/epoch fallback is sound. Future cache state must remain consistent with new dependency provenance after a value-preserving branch switch, not merely emit the right present value; R29/R30 inform this requirement, without importing their proofs.

## A04 public analytical replay

Own Python standard-library integer fixture; no EDA, training, downloaded-code execution, model calls or paid resources. Parameters: n=1..6, every n-bit annotation-presence mask, initial RC=2/pin=3/present annotation=5; three sequential updates RC=3, toggle annotation0, pin=4. Named control n=8/mask240 with RC update only. Every update checks all requested outputs. Mutations are between batches; they do not loosen immutable candidate-base semantics. No floating, tags, electrical model, restoration journal or complete timing extraction is certified.

Counts are world-record reevaluations, not distinct pure-key calls. A shared pure evaluator could further coalesce them in both treatments. Index edges are logical membership records, not process bytes. Allocation/scanning/hash/set costs and data layout are uncalibrated. Indexed Q and indexed B5 use the identical index implementation deliberately as a transplant control; Flat provides a separately coded dirty-set scan. This does not compare independent production implementations or prove optimality.

Extract/run from the released experiment-plan.md in a fresh directory:

```sh
python3 - <<'EXTRACT'
from pathlib import Path
import hashlib, subprocess
s=Path('experiment-plan.md').read_text()
code=s.split('```python\n',1)[1].split('```',1)[0]
expected=s.split('```json\n',1)[1].split('```',1)[0]
Path('a04.py').write_text(code)
result=subprocess.check_output(['python3','a04.py'])
assert result.decode()==expected
print('code_sha256',hashlib.sha256(code.encode()).hexdigest())
print('stdout_sha256',hashlib.sha256(result).hexdigest())
print(result.decode(),end='')
EXTRACT
```

```python
import json

# Own finite integer model. Counts are world-record reevaluations, not
# shared pure-key primitive calls, engine runtime, process bytes, or STA work.
def read_world(state, world):
    deps = {f'ann:{world}'}  # includes existence/absence of the annotation
    annotation = state['ann'][world]
    if annotation is not None:
        return annotation, deps
    deps.update(('rc', 'pin'))
    return state['rc'] + state['pin'], deps


def fresh(state):
    return [read_world(state, w)[0] for w in range(len(state['ann']))]


class Flat:
    def __init__(self, state):
        pairs = [read_world(state, w) for w in range(len(state['ann']))]
        self.values = [p[0] for p in pairs]
        self.deps = [p[1] for p in pairs]

    def update(self, state, changed):
        dirty = {w for w, deps in enumerate(self.deps) if deps & changed}
        for w in sorted(dirty):
            self.values[w], self.deps[w] = read_world(state, w)
        return dirty


class Indexed:
    def __init__(self, state):
        self.values = []
        self.deps = []
        self.index = {}
        self.edge_inserts = self.edge_deletes = 0
        for w in range(len(state['ann'])):
            value, deps = read_world(state, w)
            self.values.append(value)
            self.deps.append(deps)
            self.add(w, deps)
        self.initial_edge_inserts = self.edge_inserts

    def add(self, w, deps):
        for dep in deps:
            self.index.setdefault(dep, set()).add(w)
            self.edge_inserts += 1

    def update(self, state, changed):
        dirty = set()
        for dep in changed:
            dirty.update(self.index.get(dep, ()))
        for w in sorted(dirty):
            for dep in self.deps[w]:
                self.index[dep].remove(w)
                self.edge_deletes += 1
                if not self.index[dep]:
                    del self.index[dep]
            self.values[w], self.deps[w] = read_world(state, w)
            self.add(w, self.deps[w])
        return dirty


def union_update(cache, state, changed):
    # Conservative value-class union; recompute every member of an affected
    # current value class. Correct but can over-invalidate.
    groups = {}
    for w, value in enumerate(cache.values):
        groups.setdefault(value, []).append(w)
    dirty = set()
    for worlds in groups.values():
        deps = set().union(*(cache.deps[w] for w in worlds))
        if deps & changed:
            dirty.update(worlds)
    for w in sorted(dirty):
        cache.values[w], cache.deps[w] = read_world(state, w)
    return dirty


def initial(n, mask):
    return {'rc': 2, 'pin': 3,
            'ann': [5 if (mask >> w) & 1 else None for w in range(n)]}


def run():
    fixtures = events = stale_events = 0
    for n in range(1, 7):
        for mask in range(1 << n):
            state = initial(n, mask)
            b5, q, b5_indexed, union = Flat(state), Indexed(state), Indexed(state), Flat(state)
            old_values = b5.values.copy()
            assert set(old_values) == {5}
            fixtures += 1
            for event in range(3):
                if event == 0:
                    state['rc'] = 3
                    changed = {'rc'}
                elif event == 1:
                    state['ann'][0] = None if state['ann'][0] is not None else 5
                    changed = {'ann:0'}
                else:
                    state['pin'] = 4
                    changed = {'pin'}
                d_flat = b5.update(state, changed)
                d_q = q.update(state, changed)
                d_transplant = b5_indexed.update(state, changed)
                d_union = union_update(union, state, changed)
                oracle = fresh(state)
                assert d_flat == d_q == d_transplant
                assert d_q <= d_union
                assert b5.values == q.values == b5_indexed.values == union.values == oracle
                assert q.index == b5_indexed.index
                stale_events += int(old_values != oracle)
                events += 1
    state = initial(8, 0b11110000)
    flat, q, transplant, union = Flat(state), Indexed(state), Indexed(state), Flat(state)
    before_classes = len(set(flat.values))
    state['rc'] = 3
    dirty = flat.update(state, {'rc'})
    q_dirty = q.update(state, {'rc'})
    t_dirty = transplant.update(state, {'rc'})
    u_dirty = union_update(union, state, {'rc'})
    assert dirty == q_dirty == t_dirty
    result = {'fixtures': fixtures, 'update_events': events,
              'stale_events_if_initial_values_never_invalidated': stale_events,
              'all_oracle_and_dirty_set_assertions': True,
              'named': {'worlds': 8, 'annotation_mask': 240,
                        'old_value_classes': before_classes,
                        'new_value_classes': len(set(q.values)),
                        'dirty_worlds_flat': sorted(dirty),
                        'dirty_worlds_q': sorted(q_dirty),
                        'dirty_worlds_indexed_b5': sorted(t_dirty),
                        'dirty_worlds_value_union': sorted(u_dirty),
                        'index_initial_edge_inserts': q.initial_edge_inserts,
                        'index_update_edge_deletes': q.edge_deletes,
                        'index_update_edge_inserts': q.edge_inserts-q.initial_edge_inserts,
                        'full_output_entries': len(q.values),
                        'output': q.values}}
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    run()
```

Exact stdout:

```json
{"all_oracle_and_dirty_set_assertions":true,"fixtures":126,"named":{"annotation_mask":240,"dirty_worlds_flat":[0,1,2,3],"dirty_worlds_indexed_b5":[0,1,2,3],"dirty_worlds_q":[0,1,2,3],"dirty_worlds_value_union":[0,1,2,3,4,5,6,7],"full_output_entries":8,"index_initial_edge_inserts":16,"index_update_edge_deletes":12,"index_update_edge_inserts":12,"new_value_classes":2,"old_value_classes":1,"output":[6,6,6,6,5,5,5,5],"worlds":8},"stale_events_if_initial_values_never_invalidated":360,"update_events":378}
```

Code SHA-256: `d01f95746244e24b4cde2e168c4ea446f6bdadf25bfa64cdf45781ebb8405529`. Stdout SHA-256 (including trailing LF): `17248346f6f06b0b0febaecad0d8d2a3557ac5f0069130e358db1f9c9f6171c3`.

Interpretation: retained dependency incidence avoids stale initial values. Selective invalidation reduces extra record work relative to a conservative value-class union in the named case, but the entire intervention transfers to B5. Building/maintaining that index costs work in the same model. No winner, byte or runtime gain is established. This is a new own observation requiring independent scientific review, not a reconstruction or validation of historical unpublished replays.

## Future correctness/dependency and cost oracle

D1/D2 in tasklist.md remain unexecuted. Extract actual transitive reads of Liberty/RC/SDC/context, annotation existence, driver input-cap/load, arrival/slew, required/check phases, exceptions/tags, floating/interpolation, base restoration and mutable calculator state. Exact current results may share storage, but retain separate validity provenance or conservatively invalidate their union/epoch. Unknown state forces charged isolated reference fallback. Add real coalescence-then-mutation cases for RC, annotation existence/value, output-equal branch switch followed by a second dependency edit, wrong epoch and return to prior base. Compare every endpoint/electrical/failure/ranking output and restore hash against fresh reference. A04 is only a test specification witness, not this engine test.

The topological procedure is source S1/S2 -> D0 actual scoped resources/rights/consent -> D1 recorder -> D2 correctness -> separately granted D3 baseline census and observer calibration -> D4 meaningful threshold/preregistration -> D5 matched implementations -> D6 new exact-target agreement -> D7 full paired evaluation -> D8 independent recheck. Current park blocks experimental construction. Source-only plans can be judged without first executing the future census; a diagnostic grant does not include Q evaluation.

Preregister costs separately for support construction/conversion, comparisons/key hashing/full equality, value and provenance classes, index edge construction/probe/removal/update, scheduling/communication, exact/recomputed work, peak resident and mechanism bytes, unsupported cases/reference fallback, report/read/restoration and final checking. Charge baseline-only observer perturbation before interpreting headroom. Any learned guide additionally charges labels/features/training/invocations/failures. Unified/shared-trunk versus separate specialists+fusion, simple rules/no-model and conventional adaptive controllers must share deployable information and family splits. Single-controller repeated-call and ordinary parallel controls precede cooperative-agent claims. No new training/cooperation is specified as the current intervention.

Current practical threshold, allocation, measured variance/cost fractions and all performance forecasts are null. No numerical speed target, universal lower bound or simulated STA gain follows from A04. Correctness stops on one mismatch; useful-system claims stop on complete transplant equivalence without a residual useful cost interaction, lack of natural full-output reader, resource exhaustion or unsupported rights. Acceptance and abandonment require their own independent exact bindings; park is neither.
