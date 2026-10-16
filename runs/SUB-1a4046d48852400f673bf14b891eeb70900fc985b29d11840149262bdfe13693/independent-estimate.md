# Independent estimate and analytical boundary check

No calibrated runtime, memory or success-probability forecast is available. Review is explicitly unblinded: proposal/plan numeric analytical counts and thresholds were read; forecast.json was not opened. No real timing run was performed and no predecessor measurement is inherited.

For equal complete pure keys and unlimited cold caches, distinct requested keys fix primitive work. Finite-capacity gains depend on schedule, eviction and representation cost. These assumptions do not establish a bound on general STA or on an implementation with hidden dependencies. The shared irreducible-output floor argument is algebraically sound only when the floor is genuinely common and irreducible. Its fraction is unknown. No positive numerical headroom interval is justified.

## C-A01: arbitrary base, absent complement and re-coalescence

This independently authored standard-library fixture checks a boundary omitted from the proposer's A02 generator: the immutable base need not be a requested candidate. A02 always uses world zero as base; its complement is therefore nonempty. This is a coverage limitation, not a discovered error in the proposal's algorithm. Here all binary inputs for two columns and three requested worlds are enumerated, with base (0,0) supplied separately. The same input set is also evaluated with a constant-output primitive. Exact output and requested-key parity hold. No source/EDA code is executed; this is a finite integer model, not a test of floating-point timing, the real adapter, scheduling, memory or speed.

Replay: extract the Python fence below and run with Python 3. No package dependencies or external input.

```python
import itertools, json

def evaluate(cols, base, fn):
    n = len(cols[0])
    exceptions = [{w:v for w,v in enumerate(col) if v != b}
                  for col,b in zip(cols,base)]
    support = set().union(*(set(e) for e in exceptions))
    cache = {}
    def call(key):
        if key not in cache:
            cache[key] = fn(key)
        return cache[key]
    has_default = len(support) < n
    default = call(base) if has_default else None
    explicit = {}
    for w in sorted(support):
        key = tuple(e.get(w,b) for e,b in zip(exceptions,base))
        value = call(key)
        if not has_default or value != default:
            explicit[w] = value
    output = [explicit.get(w,default) for w in range(n)]
    keys = set(zip(*cols))
    assert output == [fn(k) for k in zip(*cols)]
    assert set(cache) == keys
    assert len(output) == n
    return not has_default, len(set(output)) == 1

checks = empty = coalesced_empty = 0
for bits in itertools.product((0,1), repeat=6):
    cols = (bits[:3], bits[3:])
    for fn in (lambda x:sum(x), lambda x:7):
        absent, coalesced = evaluate(cols,(0,0),fn)
        checks += 1
        empty += absent
        coalesced_empty += absent and coalesced
print(json.dumps({'checks':checks,'empty_complement_checks':empty,
                  'coalesced_empty_complement_checks':coalesced_empty,
                  'output_and_requested_key_parity':True,'eda_runs':0},sort_keys=True))
```

Actual stdout:

```json
{"checks": 128, "coalesced_empty_complement_checks": 36, "eda_runs": 0, "empty_complement_checks": 54, "output_and_requested_key_parity": true}
```

Code SHA-256: 2f39bf4c6f674cda4d1f8b5049ffa05d6ac289bb6adcc6efa937a8b8e4a7c00b.

Stdout SHA-256: 24fd01f2ce673814e583845a9b93c93a51fc0050a6e4146bf73b8490b702b0f4.
