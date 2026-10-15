# Independent estimate and analytical check

Runtime gain, regret distribution, successful deployment fraction and covariance calibration: unknown. No numerical success probability is defensible from these sources. The actual uncertainty is cheap-model epistemic discrepancy at a fixed engine/checkpoint, not manufacturing variation. Source C01 requires update and restore; pre-query W construction and label acquisition can exceed saved transactions when alternatives are few.

A necessary measured break-even condition is avoided reference transaction cost > W probing + fitting/calibration allocation + acquisition + extra guards/fallback/invalidation, with identical quality constraints. This is an accounting condition, not a measured bound. Cold-start labels and amortized usage need separate ledgers; declaring labels reusable does not establish an actual workload.

Own exact finite-table check executed with python3 standard library on 2026-10-15; constant-size arithmetic, no external simulator, fitting or GPU:

```python
from fractions import Fraction as F
from itertools import product
for law in ['same','opposite','independent']:
    worlds = ([((a,b),F(1,4)) for a,b in product([-1,1],repeat=2)]
              if law=='independent' else
              [((a,a if law=='same' else -a),F(1,2)) for a in [-1,1]])
    M=lambda y:max(0,*y)
    prior=sum(p*M(y) for y,p in worlds)
    for q in [0,1]:
        after=sum(p*(M(y)-max(0,y[q])) for y,p in worlds)
        ei=sum(p*max(0,y[q]) for y,p in worlds)
        assert prior-after==ei==F(1,2)
    print(law,prior,ei)
```

Observed output: same 1/2 1/2; opposite 1 1/2; independent 3/4 1/2. This discrete example complements the distribution-free tower-property proof in OBJ-001, not a claim that the proposal's GP has been experimentally tested.
