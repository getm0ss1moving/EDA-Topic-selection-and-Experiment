# Independent headroom and reproducible check

Headroom, success probability and calibrated speedup range: unknown. Exact rank saturation is not a physical runtime bound. For N candidate transactions of equal cost t, m queried candidates and extra feature/model overhead H, the simplified necessary savings condition is H < (N-m)t, before differential guard/fallback effects. This is an accounting identity, not measured values. Four map probes per candidate may dominate a small candidate set; the proposal already charges them. Source snippets do not determine N, t or H.

Own execution: Python standard-library Fraction arithmetic, six rows, three inversions of 2x2 matrices. No EDA, build, labels, training, GPU or paid API use. The following reproduces A01:

```python
from fractions import Fraction as F
W=[[F(x) for x in r] for r in [[1,0],[0,1],[1,1],[1,-1],[2,1],[-1,2]]]
K=[[sum(x*y for x,y in zip(a,b)) for b in W] for a in W]
for q in range(3):
    o=[2*q,2*q+1]
    a,b=K[o[0]][o[0]],K[o[0]][o[1]]
    c,d=K[o[1]][o[0]],K[o[1]][o[1]]
    det=a*d-b*c
    inv=[[d/det,-b/det],[-c/det,a/det]]
    post=[[K[i][j]-sum(K[i][o[u]]*inv[u][v]*K[o[v]][j] for u in range(2) for v in range(2)) for j in range(6)] for i in range(6)]
    assert all(x==0 for r in post for x in r)
    print(q,det,"all posterior covariance entries zero")
```

Observed determinants: 1,4,25; all assertions passed. Full latent recovery follows from invertibility, not from a fitted GP score. No Gaussian-sampling or physical timing experiment was executed. Proposal EXP-000 was read, not independently rerun; its numerical results remain author-reported in this review.
