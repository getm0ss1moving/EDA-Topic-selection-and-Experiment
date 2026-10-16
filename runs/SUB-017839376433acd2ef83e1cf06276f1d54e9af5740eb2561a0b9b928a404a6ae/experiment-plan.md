# Mechanism-delta map, source dependency tests and experimental plan

## State/transition/lifetime contrast required by OBJ-1201

All records below are engine-relative complete keys, exact values/statuses and exhaustive requested-world memberships. Q and conventional B5 use the same declared DAG, immutable base/epoch, deterministic operation order, full-output readers, available features and lifetime policy. Same primitives and output equality are a fair common oracle, not independent scientific verification.

| State/action | Q specification | Strong conventional B5/transplant | Identifiable Q-only action? |
|---|---|---|---|
| Base/default | Explicit valid bit and exact base per operation | Same base and valid bit | No |
| Tuple gathering | Default plus world-indexed exact exceptions; charge support creation/conversion | Specialized conditional value map/MTBDD or identical sparse join; dense traversal also eligible | Only representation/gather administration can differ; no exclusive kernel |
| Operation invocation | Once per canonical complete requested key; base work separately charged | Same keys and cold-cache opportunity | No primitive-count difference |
| Coalescence | Exact value/status identity -> membership set | Conventional equal-result union -> same membership | No |
| Consumer/lifetime | Declared DAG consumers plus complete output consumers; decrement at use | Same remaining consumer count and last-use release | No |
| Retention/admission | Policy uses declared current information | Identical policy/features/cap and transplant | No specified difference |
| Invalid default | Dense/reference fallback, no assumed base hit | Same fallback | No |
| Output | Materialize/retain every requested output entry | Same entries and consumer endpoint | No |

Let F map Q(v,key,membership,value,status,remaining-users,epoch) to the identical B5 record. Equal initial base/input state and common operation order give a conditional bisimulation of normalized eval/coalesce/materialize/free events: a matching key invokes the same pure function; its full result yields the same class; identical user decrements permit identical release. This argument applies only to these stated semantics. It does not imply two different representations take equal gathering time or process memory, nor prove a general STA equivalence theorem. A future intervention must change a named transition/information/maintenance cost and survive its best conventional transplant. Present Q has no such demonstrated exclusive intervention.

## A03 public analytical replay

Own standard-library code only. No downloaded code, author implementation, EDA engine, training or external allocation executed. Extract the exact Python fence and run it; result JSON is the exact stdout fence. Commands:

```sh
python3 - <<'EXTRACT'
from pathlib import Path
s=Path('experiment-plan.md').read_text()
code=s.split('```python\n',1)[1].split('```',1)[0]
Path('/tmp/eda0010-a03-replay.py').write_text(code)
EXTRACT
python3 /tmp/eda0010-a03-replay.py > /tmp/eda0010-a03-stdout.json
shasum -a 256 /tmp/eda0010-a03-replay.py /tmp/eda0010-a03-stdout.json
```

Exact code SHA256 `261f1837df618fab028bf0c21359daf65e49cbb1ff4585d8a69426f7ce0c7773`; exact stdout SHA256 `cfafe14f1fdb83656ff536d3114ab933d83126fdfe403342d4609abe31cb8be5`. Final model seed20261016; 480 random operation cases, four named controls and one five-operation reconvergent DAG. The arithmetic annotation-presence witness is source-derived test design, not engine execution.

```python
import hashlib, json, random
from collections import Counter

def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'))

def val(x, status='OK'):
    return (x, status)

def primitive(op, args):
    errors = tuple((i, p[1]) for i, p in enumerate(args) if p[1] != 'OK')
    if errors:
        return (None, canon(errors))
    xs = [p[0] for p in args]
    if op == 'a': return val(2 * xs[0])
    if op == 'b': return val(xs[0] + 3)
    if op == 'c': return val(xs[0] * 5)
    if op == 'd': return val(xs[0] + xs[1])
    if op == 'e': return val(xs[0] - xs[1])
    if op == 'zero': return val(0)
    raise AssertionError(op)

def evaluate(op, columns, bases, mode, default_valid=True):
    n = len(columns[0]); assert n > 0
    buckets = {}; probes = 0; support_entries = 0
    effective_mode = mode if default_valid else 'B5'
    if effective_mode == 'Q':
        supports = [{w:p for w,p in enumerate(col) if p != base}
                    for col,base in zip(columns,bases)]
        support_entries = sum(map(len,supports))
        union = set().union(*(set(s) for s in supports))
        complement = sorted(set(range(n)) - union)
        if complement:
            buckets[tuple(bases)] = complement
        for w in sorted(union):
            key = tuple(s.get(w,base) for s,base in zip(supports,bases))
            buckets.setdefault(key,[]).append(w); probes += len(columns)
    elif effective_mode == 'B5':
        for w in range(n):
            key = tuple(col[w] for col in columns)
            buckets.setdefault(key,[]).append(w); probes += len(columns)
    else: raise AssertionError(mode)
    out = [None]*n; events=[]
    for args,worlds in sorted(buckets.items(),key=lambda kv:canon(kv[0])):
        result = primitive(op,args)
        worlds = sorted(worlds)
        events.append(['eval',op,args,worlds,result])
        for w in worlds: out[w]=result
    classes={}
    for w,p in enumerate(out): classes.setdefault(p,[]).append(w)
    normalized=sorted([[p,ws] for p,ws in classes.items()],key=canon)
    assert out == [primitive(op,tuple(c[w] for c in columns)) for w in range(n)]
    # Output default may differ from every requested world. It is computed and
    # charged separately here as a base prerequisite; never a requested-world hit.
    base_out = primitive(op,tuple(bases)) if default_valid else val(None,'UNKNOWN_DEFAULT')
    requested_base = tuple(bases) in buckets
    if default_valid:
        events.append(['base_eval',op,tuple(bases),base_out])
    else:
        events.append(['default_invalid_dense_fallback',op])
    events.append(['partition',op,normalized])
    return out,base_out,events,{'requested_keys':len(buckets), 'base_calls':int(default_valid), 'default_valid':default_valid,
        'empty_complement':not requested_base, 'coalesced_classes':len(classes),
        'tuple_reads':probes, 'support_entries':support_entries,
        # Constructing supports above scans dense input. It is charged explicitly.
        'support_build_reads':n*len(columns) if effective_mode=='Q' else 0}

DAG=[('a',['x']),('b',['a']),('c',['a']),('d',['b','c']),('e',['b','c'])]
OUTPUTS=['d','e']

def run_dag(xs,base,mode,retain):
    n=len(xs); live={'x':xs}; bases={'x':base}; ref=Counter(p for _,ps in DAG for p in ps)
    events=[]; metrics=[]; full_output={}; peak=0; output_bytes=0
    def size(p):
        # Declared logical encoding: one 16-byte payload/status handle per class,
        # one 8-byte membership id per world, plus 16-byte table header.
        return 16+16*len(set(p))+8*len(p)
    def sample():
        return sum(size(p) for p in live.values())+output_bytes
    peak=max(peak,sample())
    for op,parents in DAG:
        ys,b,es,m=evaluate(op,[live[p] for p in parents],[bases[p] for p in parents],mode)
        live[op]=ys; bases[op]=b; events+=es; metrics.append(m)
        peak=max(peak,sample())
        if op in OUTPUTS:
            full_output[op]=list(ys); output_bytes+=16*n
            events.append(['materialize',op,n]); peak=max(peak,sample())
        for p in parents:
            ref[p]-=1
            if not retain and ref[p]==0:
                del live[p];events.append(['free',p])
        if not retain and ref[op]==0:
            del live[op];events.append(['free',op])
    assert set(full_output)==set(OUTPUTS)
    return {'events':events,'outputs':full_output,'peak_model_bytes':peak,
            'output_model_bytes':output_bytes,'metrics':metrics}

rng=random.Random(20261016); count=0; empty=0; coalesce=0
for n in [1,2,3,8,17]:
    for repetition in range(32):
        bases=[val(rng.randrange(-2,3)),val(rng.randrange(-2,3))]
        cols=[[val(rng.randrange(-3,4),rng.choice(['OK','OK','E_A','E_B'])) for _ in range(n)] for _ in bases]
        for op in ['d','e','zero']:
            q=evaluate(op,cols,bases,'Q'); b=evaluate(op,cols,bases,'B5')
            assert q[:3]==b[:3]
            count+=1;empty+=q[3]['empty_complement'];coalesce+=q[3]['coalesced_classes']==1
# Fully disjoint requested states; baseline is never world zero.
q=evaluate('zero',[[val(1),val(2)]],[val(99)],'Q')
assert q[3]['empty_complement'] and q[3]['requested_keys']==2 and q[3]['coalesced_classes']==1
# Non-value status identities remain distinct under full equality.
s=evaluate('a',[[val(1,'E_A'),val(1,'E_B')]],[val(1)],'Q')
assert s[3]['coalesced_classes']==2
u=evaluate('a',[[val(5),val(6)]],[val(999)],'Q',False)
v=evaluate('a',[[val(5),val(6)]],[val(999)],'B5',False)
assert u[:3]==v[:3] and u[3]['base_calls']==0 and not u[3]['default_valid']
xs=[val(0),val(1),val(0),val(2),val(0),val(1),val(0),val(3)]
q=run_dag(xs,val(0),'Q',False);b=run_dag(xs,val(0),'B5',False)
retain=run_dag(xs,val(0),'B5',True)
assert q['events']==b['events'] and q['outputs']==b['outputs']
assert q['peak_model_bytes']==b['peak_model_bytes']
assert retain['outputs']==q['outputs']
def cap_model(pin, rc_wire, annotation, subtract_pin=False):
    return (0 if annotation is not None and subtract_pin else pin) + (rc_wire if annotation is None else annotation)
presence = {'before_absent':cap_model(2,3,None),
            'before_present':cap_model(2,3,5,True),
            'after_rc_change_absent':cap_model(2,4,None),
            'after_rc_change_present':cap_model(2,4,5,True)}
assert presence['before_absent']==presence['before_present']==5
assert presence['after_rc_change_absent']==6 and presence['after_rc_change_present']==5
result={'seed':20261016,'random_operation_cases':count,
 'empty_complement_cases':empty,'single_output_class_cases':coalesce,
 'named_controls':['absent_requested_base','all_outputs_recoalesce','distinct_error_statuses','invalid_default_dense_fallback'],
 'dag':['a=2*x','b=a+3','c=5*a','d=b+c','e=b-c'],
 'annotation_presence_witness':presence,
 'world_values':[p[0] for p in xs],'base_value':0,
 'Q_B5_normalized_transition_trace_equal':True,
 'transition_trace_sha256':hashlib.sha256(canon(q['events']).encode()).hexdigest(),
 'trace':q['events'],
 'requested_primitive_calls':sum(m['requested_keys'] for m in q['metrics']),
 'extra_base_primitive_calls':sum(m['base_calls'] for m in q['metrics']),
 'output_entries':sum(map(len,q['outputs'].values())),
 'full_outputs':q['outputs'],
 'peak_model_bytes':{'Q_last_use':q['peak_model_bytes'],'B5_last_use':b['peak_model_bytes'],'B5_retain':retain['peak_model_bytes']},
 'full_output_bytes_charged':q['output_model_bytes'],
 'administration_counts':{name:{k:sum(m[k] for m in r['metrics']) for k in ['tuple_reads','support_entries','support_build_reads']} for name,r in [('Q',q),('B5',b)]},
 'limitations':'Finite typed integer pure-DAG model. Logical bytes exclude Python/engine structures and global base/keys/graph metadata. No byte cap/eviction or rematerialization implemented. Dense-to-support construction explicitly charged. Trace normalization excludes unequal gathering administration. No STA/runtime/novelty measurement.'}
print(json.dumps(result,sort_keys=True,indent=2))
```

Exact stdout:

```json
{
  "Q_B5_normalized_transition_trace_equal": true,
  "administration_counts": {
    "B5": {
      "support_build_reads": 0,
      "support_entries": 0,
      "tuple_reads": 56
    },
    "Q": {
      "support_build_reads": 56,
      "support_entries": 28,
      "tuple_reads": 28
    }
  },
  "annotation_presence_witness": {
    "after_rc_change_absent": 6,
    "after_rc_change_present": 5,
    "before_absent": 5,
    "before_present": 5
  },
  "base_value": 0,
  "dag": [
    "a=2*x",
    "b=a+3",
    "c=5*a",
    "d=b+c",
    "e=b-c"
  ],
  "empty_complement_cases": 459,
  "extra_base_primitive_calls": 5,
  "full_output_bytes_charged": 256,
  "full_outputs": {
    "d": [
      [
        3,
        "OK"
      ],
      [
        15,
        "OK"
      ],
      [
        3,
        "OK"
      ],
      [
        27,
        "OK"
      ],
      [
        3,
        "OK"
      ],
      [
        15,
        "OK"
      ],
      [
        3,
        "OK"
      ],
      [
        39,
        "OK"
      ]
    ],
    "e": [
      [
        3,
        "OK"
      ],
      [
        -5,
        "OK"
      ],
      [
        3,
        "OK"
      ],
      [
        -13,
        "OK"
      ],
      [
        3,
        "OK"
      ],
      [
        -5,
        "OK"
      ],
      [
        3,
        "OK"
      ],
      [
        -21,
        "OK"
      ]
    ]
  },
  "limitations": "Finite typed integer pure-DAG model. Logical bytes exclude Python/engine structures and global base/keys/graph metadata. No byte cap/eviction or rematerialization implemented. Dense-to-support construction explicitly charged. Trace normalization excludes unequal gathering administration. No STA/runtime/novelty measurement.",
  "named_controls": [
    "absent_requested_base",
    "all_outputs_recoalesce",
    "distinct_error_statuses",
    "invalid_default_dense_fallback"
  ],
  "output_entries": 16,
  "peak_model_bytes": {
    "B5_last_use": 688,
    "B5_retain": 1120,
    "Q_last_use": 688
  },
  "random_operation_cases": 480,
  "requested_primitive_calls": 20,
  "seed": 20261016,
  "single_output_class_cases": 109,
  "trace": [
    [
      "eval",
      "a",
      [
        [
          0,
          "OK"
        ]
      ],
      [
        0,
        2,
        4,
        6
      ],
      [
        0,
        "OK"
      ]
    ],
    [
      "eval",
      "a",
      [
        [
          1,
          "OK"
        ]
      ],
      [
        1,
        5
      ],
      [
        2,
        "OK"
      ]
    ],
    [
      "eval",
      "a",
      [
        [
          2,
          "OK"
        ]
      ],
      [
        3
      ],
      [
        4,
        "OK"
      ]
    ],
    [
      "eval",
      "a",
      [
        [
          3,
          "OK"
        ]
      ],
      [
        7
      ],
      [
        6,
        "OK"
      ]
    ],
    [
      "base_eval",
      "a",
      [
        [
          0,
          "OK"
        ]
      ],
      [
        0,
        "OK"
      ]
    ],
    [
      "partition",
      "a",
      [
        [
          [
            0,
            "OK"
          ],
          [
            0,
            2,
            4,
            6
          ]
        ],
        [
          [
            2,
            "OK"
          ],
          [
            1,
            5
          ]
        ],
        [
          [
            4,
            "OK"
          ],
          [
            3
          ]
        ],
        [
          [
            6,
            "OK"
          ],
          [
            7
          ]
        ]
      ]
    ],
    [
      "free",
      "x"
    ],
    [
      "eval",
      "b",
      [
        [
          0,
          "OK"
        ]
      ],
      [
        0,
        2,
        4,
        6
      ],
      [
        3,
        "OK"
      ]
    ],
    [
      "eval",
      "b",
      [
        [
          2,
          "OK"
        ]
      ],
      [
        1,
        5
      ],
      [
        5,
        "OK"
      ]
    ],
    [
      "eval",
      "b",
      [
        [
          4,
          "OK"
        ]
      ],
      [
        3
      ],
      [
        7,
        "OK"
      ]
    ],
    [
      "eval",
      "b",
      [
        [
          6,
          "OK"
        ]
      ],
      [
        7
      ],
      [
        9,
        "OK"
      ]
    ],
    [
      "base_eval",
      "b",
      [
        [
          0,
          "OK"
        ]
      ],
      [
        3,
        "OK"
      ]
    ],
    [
      "partition",
      "b",
      [
        [
          [
            3,
            "OK"
          ],
          [
            0,
            2,
            4,
            6
          ]
        ],
        [
          [
            5,
            "OK"
          ],
          [
            1,
            5
          ]
        ],
        [
          [
            7,
            "OK"
          ],
          [
            3
          ]
        ],
        [
          [
            9,
            "OK"
          ],
          [
            7
          ]
        ]
      ]
    ],
    [
      "eval",
      "c",
      [
        [
          0,
          "OK"
        ]
      ],
      [
        0,
        2,
        4,
        6
      ],
      [
        0,
        "OK"
      ]
    ],
    [
      "eval",
      "c",
      [
        [
          2,
          "OK"
        ]
      ],
      [
        1,
        5
      ],
      [
        10,
        "OK"
      ]
    ],
    [
      "eval",
      "c",
      [
        [
          4,
          "OK"
        ]
      ],
      [
        3
      ],
      [
        20,
        "OK"
      ]
    ],
    [
      "eval",
      "c",
      [
        [
          6,
          "OK"
        ]
      ],
      [
        7
      ],
      [
        30,
        "OK"
      ]
    ],
    [
      "base_eval",
      "c",
      [
        [
          0,
          "OK"
        ]
      ],
      [
        0,
        "OK"
      ]
    ],
    [
      "partition",
      "c",
      [
        [
          [
            0,
            "OK"
          ],
          [
            0,
            2,
            4,
            6
          ]
        ],
        [
          [
            10,
            "OK"
          ],
          [
            1,
            5
          ]
        ],
        [
          [
            20,
            "OK"
          ],
          [
            3
          ]
        ],
        [
          [
            30,
            "OK"
          ],
          [
            7
          ]
        ]
      ]
    ],
    [
      "free",
      "a"
    ],
    [
      "eval",
      "d",
      [
        [
          3,
          "OK"
        ],
        [
          0,
          "OK"
        ]
      ],
      [
        0,
        2,
        4,
        6
      ],
      [
        3,
        "OK"
      ]
    ],
    [
      "eval",
      "d",
      [
        [
          5,
          "OK"
        ],
        [
          10,
          "OK"
        ]
      ],
      [
        1,
        5
      ],
      [
        15,
        "OK"
      ]
    ],
    [
      "eval",
      "d",
      [
        [
          7,
          "OK"
        ],
        [
          20,
          "OK"
        ]
      ],
      [
        3
      ],
      [
        27,
        "OK"
      ]
    ],
    [
      "eval",
      "d",
      [
        [
          9,
          "OK"
        ],
        [
          30,
          "OK"
        ]
      ],
      [
        7
      ],
      [
        39,
        "OK"
      ]
    ],
    [
      "base_eval",
      "d",
      [
        [
          3,
          "OK"
        ],
        [
          0,
          "OK"
        ]
      ],
      [
        3,
        "OK"
      ]
    ],
    [
      "partition",
      "d",
      [
        [
          [
            15,
            "OK"
          ],
          [
            1,
            5
          ]
        ],
        [
          [
            27,
            "OK"
          ],
          [
            3
          ]
        ],
        [
          [
            3,
            "OK"
          ],
          [
            0,
            2,
            4,
            6
          ]
        ],
        [
          [
            39,
            "OK"
          ],
          [
            7
          ]
        ]
      ]
    ],
    [
      "materialize",
      "d",
      8
    ],
    [
      "free",
      "d"
    ],
    [
      "eval",
      "e",
      [
        [
          3,
          "OK"
        ],
        [
          0,
          "OK"
        ]
      ],
      [
        0,
        2,
        4,
        6
      ],
      [
        3,
        "OK"
      ]
    ],
    [
      "eval",
      "e",
      [
        [
          5,
          "OK"
        ],
        [
          10,
          "OK"
        ]
      ],
      [
        1,
        5
      ],
      [
        -5,
        "OK"
      ]
    ],
    [
      "eval",
      "e",
      [
        [
          7,
          "OK"
        ],
        [
          20,
          "OK"
        ]
      ],
      [
        3
      ],
      [
        -13,
        "OK"
      ]
    ],
    [
      "eval",
      "e",
      [
        [
          9,
          "OK"
        ],
        [
          30,
          "OK"
        ]
      ],
      [
        7
      ],
      [
        -21,
        "OK"
      ]
    ],
    [
      "base_eval",
      "e",
      [
        [
          3,
          "OK"
        ],
        [
          0,
          "OK"
        ]
      ],
      [
        3,
        "OK"
      ]
    ],
    [
      "partition",
      "e",
      [
        [
          [
            -13,
            "OK"
          ],
          [
            3
          ]
        ],
        [
          [
            -21,
            "OK"
          ],
          [
            7
          ]
        ],
        [
          [
            -5,
            "OK"
          ],
          [
            1,
            5
          ]
        ],
        [
          [
            3,
            "OK"
          ],
          [
            0,
            2,
            4,
            6
          ]
        ]
      ]
    ],
    [
      "materialize",
      "e",
      8
    ],
    [
      "free",
      "b"
    ],
    [
      "free",
      "c"
    ],
    [
      "free",
      "e"
    ]
  ],
  "transition_trace_sha256": "00f36350fb0f94e02418b7faf030dd473ea22ba850458ccb58195bf006fcfae7",
  "world_values": [
    0,
    1,
    0,
    2,
    0,
    1,
    0,
    3
  ]
}
```

Interpretation: the normalized Q/B5 DAG traces and their declared logical peak bytes agree. Ordinary last-use release improves B5 itself. Dense-to-sparse rebuilding has extra reads; no weighting turns heterogeneous counts into runtime. Both methods charge the same extra base prerequisite evaluations and full outputs. Logical partition bytes assume header16 + payload/status-handle16 per result class + membership-ID8 per world; full output16 per entry is additionally charged. These figures are not real allocator/RSS bytes and exclude graph, base, complete key, map/hash/controller and temporary allocation metadata. No cap/eviction/recomputation policy is implemented. Shared primitive and trace serialization deliberately equalize oracle and event convention; independent tuple-gather paths test only the stated finite model. Random seed coverage is not a proof or independent verifier outcome.

## Pinned dependency boundary and executable future tests

Source pin: OpenROAD3549d60529517dc82deb7f0ff769345e9a424911 with OpenSTA80fbbb2945fee2702a84e711a95a0a3bb7050f22. Source files read, not built or executed. All line numbers below are raw one-based, not web-rendered positions. R19/R20 store exact hashes and source URLs.

| Dependency | Concrete source | Consequence and future falsification |
|---|---|---|
| Annotation absence/presence and subtraction flag | Sdc.cc3124-3140 drvrPinWireCap;3142-3155 setNetWireCap;3167-3185 connectedCap | Record successful AND absent map reads; toggle absent/present equal-total annotation then alter RC. A numeric-total-only cache must be rejected; complete invalidation must match reference. |
| Connected load pins/library context | Sdc.cc3253-3269 netCaps;3273-3330 pinCaps/portCapacitance | Include connected pin set, cell/port capacitances, scene, min/max and operating context. Swap a receiving input capacitance while arrival is unchanged. |
| Parasitic override precedence | GraphDelayCalc.cc1440-1473 parasiticLoad;1497-1516 netCaps | Annotation suppresses a parasitic branch; present-zero differs from absent. Track dependency changes even when current numeric result coalesces. |
| Gate call and phase lifetime | GraphDelayCalc.cc1072-1116 findDriverArcDelays | Input slew/load/parasitic plus multi-driver path, pin mapping, scene/minmax and finishDrvrPin boundary matter. No purity assumption for finishDrvrPin; audit or fallback. |
| Checks after both endpoint slews | GraphDelayCalc.cc346-374 findDelays | Explicit phase/check operation; equal arrival is insufficient. Force equal arrival/unequal slew and compare complete check outputs. |
| Requireds/TNS/endpoint state | Search.cc918-929 requiredInvalid;3288-3317 findRequireds/seedRequireds | Distinct reverse-phase dependency and invalidation, not reuse of forward-arrival keys. Change required constraint with equal arrival and test all slack/violation/ranking outputs. |

These are partial transitive obligations; helpers, tags, exceptions, reports, parasitic/library behavior, floating arithmetic and restoration remain unaudited. Unknown reads require conservative isolated reference fallback. Public code access does not grant data, PDK, builds or experiments.

## Baselines and future decisive comparisons

B0: isolated reference evaluation of every requested candidate and output. B1: the same engine's serial incremental/journal evaluation with complete output adapter. B2: complete-key memoization with equal storage/accounting and negative-query invalidation. B3: conventional incremental/coarsened task administration. B4: strong specialized variational execution with compatible contexts, formula-map/MTBDD, pruning and representation choices. B5: identical support-join/controller/lifetime specialization, plus ordinary dense joins when cheaper. A flat Cartesian loop or slow foreign-language port is not the strongest comparator. Q requires a future named contrast; the current local Q is B5 in normalized semantics and is not a separately novel treatment.

Matched compiler/language/arithmetic/key equality, same information and declared byte cap; all preprocessing, support production/conversion, hashing/equality, reports/readers, base analysis, fallback, restore/final checks and failed work charged. Report unlimited-key primitive parity as negative control. At finite memory report actual allocation peaks, eviction/recomputation traces and total time, not just retained values. Offline-optimal retention on the frozen tiny graph can bound that model; no learned guide may see future reuse at deployment.

S1/S2 gates precede any build. If both pass and actual diagnostic resources/consents exist, D1-D2 construct reference and recorder, D3 separately evaluates baseline-only demand/headroom including observer perturbation, D4 freezes practical threshold and held-out split, D5 builds fair alternatives/attributions, D6 collects fresh exact-target consent, and D7-D8 run/reproduce within actual grants. Tasklist gives precise owners, output procedures and stop rules. No numerical time/byte effect target is asserted without calibration. Optional prediction or cooperating workers requires a separate actual allocation and equal-information nonmodel/centralized/specialist/ordinary-parallel comparisons; correctness remains exact-engine responsibility.
