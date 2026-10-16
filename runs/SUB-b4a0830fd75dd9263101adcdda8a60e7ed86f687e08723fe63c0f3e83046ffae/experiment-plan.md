# Experiment plan and public analytical evidence

## Baselines and exact endpoint

B0: isolated fresh/reference evaluation of every world. B1: existing journaled serial incrementality with the same output contract. B2: complete-key global memoizer. B3: B2 with conventional batching/coarsening and matched memory policies. B4: equally specialized conditional-value executor with flat value/context maps, early incompatible-context pruning and MTBDD alternatives, ported into the same language/runtime rather than handicapped by a JVM. B5: conventional sparse default-plus-exception join using the same kernel and available controller as Q. Q: operation-specific partition representation with support-sensitive dispatch and bounded retention. Full outputs/failures/ranking/commit/restore and final reference check identical for all. Strongest fair baseline selected as preregistered, never weak Cartesian-only performance attribution.

A kernel implementation identical in Q/B5 is a parity control. If no mechanism beyond it is specified or measured, no useful distinct contribution has been shown. No novel primitive-count reduction over B2/B4/B5 under equal pure keys and sufficient cold cache. Output-materialization counts and method-specific reporting/restore/fallback are charged. Include representation conversion, default support creation, membership bytes, full-key comparisons, all empty attempts, scheduling, failed tasks, model fitting/inference and communication.

Correctness proof scope: in a finite pure deterministic DAG, complete equal input/context tuples produce equal values; by topological induction each world's expanded values match independent evaluation. Default complement semantics preserve all worlds. Unsupported state is isolated fallback. This proves the model, not OpenSTA extraction or completeness. R05 source snapshot536061 differs from R04's pinned STA80fbbb; D1 must audit the actual chosen adapter and every transitive dependency before claiming engine-relative exactness.

Task dependencies, actual-null resources and phase-specific consents are specified in tasklist.md. No EDA code has been built or run. Model/cooperation arms are proposed only if a separate allocation and useful workload justify them. No current numerical runtime/accuracy forecast is calibrated.

## Cost and falsification

For input classes c_i and support exception maps E_i, a naive flat product considers prod(c_i) tuples; dense traversal gathers d*n inputs; sparse default traversal gathers d*|U| after support construction, with U=union support(E_i). These model different kinds of work: set/bitset cost, variable-order/MTBDD pruning, hash/equality and result coalescence constants differ. Building E_i densely can erase the advantage; measure its real producer work. Exact primitive count equals unique complete key count in all unlimited-cache variants. Finite caps change recomputation/schedule and must be logged, not attributed to representation without equal policy controls.

If a truly shared irreducible report/restore floor is f*T_baseline, even zero remaining work yields fractional time reduction <=1-f. A20% screen therefore needs f<=0.8 in that restricted model; f unknown. This is no empirical headroom claim or general lower bound on STA. Any mismatch kills exactness, no unique-key reduction exists under parity assumptions, absent full-output demand kills advancement under this anchor, and no total-time advantage over optimized B4/B5 kills a separate system-success claim.

## A02 public analytical replay

Executed by this proposer using own Python standard-library arithmetic only. Parameters: seed100104; random n in(1,2,8,32), arity in(1,2,4),64 trials per pair, values0..3; five named controls as in code. No runtime benchmark. Named counters are exact dimensionless counts. Support encoding cost is exposed as support_entries; its CPU time is not measured or free. The replay uses a dense input for encoding and full expansion, so it does not demonstrate sparse propagation economics. Conventional sparse join is deliberately the identical support_lift call; this is a negative equivalence control, not a competitor claimed beaten.

Reproduce from a frozen release directory (write replay files to your own scratch):

```sh
python3 - <<'PYREPLAY'
from pathlib import Path
import hashlib,re,subprocess,sys
p=Path('experiment-plan.md').read_text()
code=re.search(r'```python\n(.*?)```',p,re.S).group(1)
expected=re.search(r'```json\n(.*?)```',p,re.S).group(1)
Path('/tmp/eda0010-a02-replay.py').write_text(code)
actual=subprocess.check_output([sys.executable,'/tmp/eda0010-a02-replay.py'],text=True)
assert actual == expected
assert hashlib.sha256(code.encode()).hexdigest() == 'aabaa63e83e34e49939ea4b008afc84b75a394725e948acf0c043deb1f57d513'
assert hashlib.sha256(actual.encode()).hexdigest() == '1528c9f846499d39e8523c7c4388a9ef937ff826e80be8acf82abe82b8b7f90e'
print('A02 exact code/stdout hashes and replay verified')
PYREPLAY
```

Exact source (including final newline) SHA256:aabaa63e83e34e49939ea4b008afc84b75a394725e948acf0c043deb1f57d513.
Exact stdout (including final newline) SHA256:1528c9f846499d39e8523c7c4388a9ef937ff826e80be8acf82abe82b8b7f90e.

```python
import itertools, json, random, hashlib

def groups(xs):
    ans = {}
    for w, x in enumerate(xs):
        ans.setdefault(x, set()).add(w)
    return ans

def product_lift(cols, fn):
    n = len(cols[0]); gs = [groups(c) for c in cols]
    out = [None] * n; attempts = calls = 0
    for choices in itertools.product(*(list(g.items()) for g in gs)):
        attempts += 1
        live = set.intersection(*(s for _, s in choices))
        if live:
            calls += 1; v = fn(tuple(x for x, _ in choices))
            for w in live: out[w] = v
    return out, {'attempted_products': attempts, 'primitive_calls': calls}

def dense_memo(cols, fn):
    cache = {}; out = []
    for args in zip(*cols):
        if args not in cache: cache[args] = fn(args)
        out.append(cache[args])
    return out, {'tuple_probes': len(out), 'primitive_calls': len(cache)}

def encode(cols):
    # Base values are supplied, not predicted. World zero is an unchanged control.
    return [(c[0], {w: x for w, x in enumerate(c) if x != c[0]}) for c in cols]

def support_lift(n, encoded, fn):
    # This is ALSO the conventional sparse-join comparator. No unique algorithm claim.
    defaults = tuple(v for v, _ in encoded)
    support = set().union(*(set(e) for _, e in encoded))
    cache = {}; explicit = {}
    def evaluate(args):
        if args not in cache: cache[args] = fn(args)
        return cache[args]
    # Do not evaluate a default tuple for an empty complement.
    default = evaluate(defaults) if len(support) < n else None
    for w in sorted(support):
        args = tuple(e.get(w, v) for v, e in encoded)
        result = evaluate(args)
        if default is None or result != default: explicit[w] = result
    # Expansion is always charged; no output entry is dropped.
    out = [explicit.get(w, default) for w in range(n)]
    return out, {'support_entries': sum(len(e) for _, e in encoded),
                 'union_worlds': len(support),
                 'tuple_probes': len(support) + (len(support) < n),
                 'primitive_calls': len(cache), 'materialized_entries': n}

def check(cols, fn):
    ref = [fn(a) for a in zip(*cols)]
    p, pc = product_lift(cols, fn)
    m, mc = dense_memo(cols, fn)
    s, sc = support_lift(len(ref), encode(cols), fn)
    b, bc = support_lift(len(ref), encode(cols), fn)
    assert ref == p == m == s == b
    assert pc['primitive_calls'] == mc['primitive_calls'] == sc['primitive_calls']
    assert sc == bc
    return {'n': len(ref), 'arity': len(cols), 'classes': [len(groups(c)) for c in cols],
            'product': pc, 'dense': mc, 'support': sc,
            'conventional_sparse_join_equal': True}

fn = lambda a: max(a) + sum(a) % 3
cases = {}
n = 256
# Disjoint nonbase support, eight different nonbase values per parent.
cols = [[0]*n for _ in range(4)]
for j in range(4):
    for k in range(8): cols[j][1+8*j+k] = k+1
cases['disjoint_sparse'] = check(cols, fn)
# Few classes but dense changes: Cartesian intersection is a strong alternative.
cols = [[(w >> j) & 1 for w in range(n)] for j in range(4)]
cases['dense_binary'] = check(cols, fn)
# All worlds distinct per parent but only aligned tuples actually exist.
cols = [[w+j for w in range(16)] for j in range(4)]
cases['aligned_distinct'] = check(cols, fn)
cases['n1'] = check([[2], [3], [4], [5]], fn)
cases['full_coalescence'] = check([[0,1,2,3], [3,2,1,0]], lambda a: sum(a))
r = random.Random(100104)
count = 0
for n in (1, 2, 8, 32):
    for arity in (1, 2, 4):
        for _ in range(64):
            cols = [[r.randrange(4) for _ in range(n)] for _ in range(arity)]
            check(cols, fn); count += 1
# An explicit full output vector is n entries, even if all values coalesce.
assert cases['full_coalescence']['support']['materialized_entries'] == 4
# Incomplete electrical key and stale epoch witnesses.
arrival, slews = 5, [1, 2]
assert [arrival+s for s in slews] == [6, 7]
assert (1.0-0.999) > 0 and (1.0-1.001) < 0
assert round(0.999, 2) == round(1.001, 2)
assert (1, 5, 1) != (2, 5, 1)  # epoch must be part of a complete key
# Dependency DAG audit: source locks precede adapter, which precedes census.
deps = {'D0': [], 'D1': ['D0'], 'D2': ['D1'], 'D3': ['D2'],
        'D4': ['D3'], 'D5': ['D4'], 'D6': ['D5'], 'D7': ['D6'], 'D8': ['D7']}
seen = set()
for node, prerequisites in deps.items():
    assert set(prerequisites) <= seen; seen.add(node)
print(json.dumps({'seed':100104, 'random_cases':count, 'named_cases':cases,
    'same_key_primitive_parity':True, 'incomplete_key_controls':True,
    'dependency_dag_order':list(deps), 'EDA_runs':0,
    'runtime_gain_measured':False, 'support_encoding_cost_included_as_count_only':True},
    sort_keys=True, separators=(',', ':')))
```

Actual stdout:

```json
{"EDA_runs":0,"dependency_dag_order":["D0","D1","D2","D3","D4","D5","D6","D7","D8"],"incomplete_key_controls":true,"named_cases":{"aligned_distinct":{"arity":4,"classes":[16,16,16,16],"conventional_sparse_join_equal":true,"dense":{"primitive_calls":16,"tuple_probes":16},"n":16,"product":{"attempted_products":65536,"primitive_calls":16},"support":{"materialized_entries":16,"primitive_calls":16,"support_entries":60,"tuple_probes":16,"union_worlds":15}},"dense_binary":{"arity":4,"classes":[2,2,2,2],"conventional_sparse_join_equal":true,"dense":{"primitive_calls":16,"tuple_probes":256},"n":256,"product":{"attempted_products":16,"primitive_calls":16},"support":{"materialized_entries":256,"primitive_calls":16,"support_entries":512,"tuple_probes":241,"union_worlds":240}},"disjoint_sparse":{"arity":4,"classes":[9,9,9,9],"conventional_sparse_join_equal":true,"dense":{"primitive_calls":33,"tuple_probes":256},"n":256,"product":{"attempted_products":6561,"primitive_calls":33},"support":{"materialized_entries":256,"primitive_calls":33,"support_entries":32,"tuple_probes":33,"union_worlds":32}},"full_coalescence":{"arity":2,"classes":[4,4],"conventional_sparse_join_equal":true,"dense":{"primitive_calls":4,"tuple_probes":4},"n":4,"product":{"attempted_products":16,"primitive_calls":4},"support":{"materialized_entries":4,"primitive_calls":4,"support_entries":6,"tuple_probes":4,"union_worlds":3}},"n1":{"arity":4,"classes":[1,1,1,1],"conventional_sparse_join_equal":true,"dense":{"primitive_calls":1,"tuple_probes":1},"n":1,"product":{"attempted_products":1,"primitive_calls":1},"support":{"materialized_entries":1,"primitive_calls":1,"support_entries":0,"tuple_probes":1,"union_worlds":0}}},"random_cases":768,"runtime_gain_measured":false,"same_key_primitive_parity":true,"seed":100104,"support_encoding_cost_included_as_count_only":true}
```

Interpretation:768 random +5 named cases pass exact output/unique-key assertions; disjoint_sparse shows6561 naive product attempts versus33 sparse tuple probes/32 support entries, both33 primitive calls and256 output entries. Dense_binary shows16 product attempts versus241 support tuple probes/512 support entries. These are heterogeneous counts; neither establishes a time ratio. Aligned_distinct demonstrates empty-product blowup for the naive baseline only; optimized variable-order/BDD/sparse alternatives remain mandatory. Full_coalescence still materializes4 entries. n1 retains the no-multiplicity control. The electrical/rounding/epoch assertions are tiny witnesses, not complete engine invalidation tests. The DAG assertion checks only written ordering, not operational readiness. No empirical feasibility, memory peak or publication claim follows.
