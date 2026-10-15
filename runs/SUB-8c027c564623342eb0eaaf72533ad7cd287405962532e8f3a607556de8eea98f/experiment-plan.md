# Experiment plan — EDA-0007 R1

## Current authorization and completed work

Owner batch0003 authorizes research/source reading and tiny own analytical checks only. This release ran the constant-size standard-library EXP-000 below and read primary sources. No OpenROAD/OpenSTA invocation, EDA build/full-flow, label generation, model fitting/training, GPU, remote or new paid-API call occurred. Historic provisional8 CPUh/4GB/0 GPU caps are not an actual allocation for this revision. Future diagnostic caps below are requests, not grants.

## Preregistered hypotheses and counter-hypotheses

H1: signed contrast W, constructed from shared electrical perturbations, captures useful held-out residual structure after strongest supported calibration. Counter: calibrated mean/scalar bias or equally informed raw electrical features explain it all. No distinct-model advantage over the identical W GP is possible.

H2: sequential bundled measurements change later marginal beliefs usefully. Counter: same-output/noiseless block cancellation, negligible errors, wrong-sign transfer, path switching or small candidate counts remove benefit. The literal one-step local regret rule equals joint CEI and is not a new information policy.

H3: the local decision policy saves total selection time without unacceptable full-guard/global quality loss. Counter: prediction overhead, label cold start, incremental timing speed, guard failures or local/global mismatch erase utility. Final measured acceptance cannot prove an unmeasured optimum was not missed.

## Primary endpoint, correctness and feasibility

Endpoint: total wall seconds per measured fully guarded selection at a preregistered allowed regret, compared with exhaustive measured enumeration and strong current cheap ordering. Report local gain regret, full-guard feasible gain regret and returned global WNS/TNS, electrical limits, area and available power estimates. Keep raw precision/units, minimum and sum slack definitions and all failed/UNKNOWN cases. No inherited approximate full-vector endpoint-error or20% screen is treated as validated demand. EXP-005 must freeze meaningful thresholds using actual workload variation and engineering rationale before candidate evaluation; it is currently unresolved.

Reference oracle: pinned OpenROAD source version3549d60529517dc82deb7f0ff769345e9a424911 and its declared compatible OpenSTA/build/dependency/FP configuration, immutable base and exact candidate order. This is an intended source target, not a verified installed binary. R01/R02 alone are insufficient to certify the transaction adapter. Each candidate starts at original checkpoint; update pin loading/parasitics/timing; capture g,m plus full reference guard summaries; rollback; compare checkpoint/database and reference outputs. Any mismatch invalidates later observations and stops the batch. Commit only a measured full-guard passing candidate or return base. No dense global-vector computation requirement is imposed on the approximate model, but reference validation must cover affected global consequences.

F_loc uses measured/predicted local slew and preknown legality; F_full uses reference global checks. The CEI_local surrogate is not asserted equivalent to immediate engineering improvement if these differ. Rejected global choices remain failures/costs in the final endpoint. Baselines use the identical final guard contract. Final guards do not provide a mathematical certificate about unmeasured candidates, foundry signoff or globally optimal PPA.

## Data, resource and contamination dependencies

No representative replacement dataset is supplied. EXP-001 must identify lawfully usable designs/libraries with enough legal alternatives, preserve each license, and pin generated-input procedures before any execution request. R10/R11 are source context; their ASAP7 listing/reference files are not project-ready rights, workload or compute. Historic Nangate45 GCD smoke is not a representative calibration set or modern API compatibility proof.

Group checkpoints, variants and candidate tables by original design family. Split training/tuning/held-out families before label/model selection; fit Omega/D only on training data. Freeze tool/library/scenario versions and normalization; no future candidate results or post-selection full-flow outputs in deployed features. Public benchmark/pretraining contamination remains uncertain, although this method uses no LLM. Evaluate cold start including all labels, and any amortization with declared reuse/transfer domain and training cost. Corner/library/design changes do not inherit validity automatically.

EXP-002 requests at most64 candidates from one lawful tiny checkpoint,10 wall minutes and2GB only as a future diagnostic; no grant exists. EDA builds need separate time/memory/source authorization too. Confirmatory design count, labels, model budget and replication cannot be honestly supplied before inventory/variance and actual allocation. A planning screen of at least3 independent families and5 paired stochastic seeds is not a completed power analysis or sufficient universal sample size. Missing actual implementer/reproducer identities block consent.

## Baselines and attribution

| ID | Procedure and fairness requirement |
|---|---|
| B0 | Exact incremental enumeration of every ordered legal candidate from original base, complete guards/restoration. Also use as offline regret oracle with its cost explicitly labeled; policy-time versus assessment-only costs reported separately. |
| B1 | Current strongest calibrated analytical/window estimate from R02, including supported STA bias, direct cheap ordering plus measured guards. Match probing/calibration information if available. |
| B2 | Strong directional/calibrated conventional alternative guided by R03/R09, faithfully bounded to this consumer; no claim of complete source reproduction without code/locks. |
| B3 | Separate gain/slew specialists with ordinary fusion; same raw electrical information, training labels and tuning/fit budget. |
| B4 | Shared-trunk bounded joint predictor; same inputs/labels and total budget. Negative transfer is reported. |
| B5 | Generic GP with raw deployable electrical features and calibrated mean; same label/acquisition/guard cost. Kernel/hyperparameter choices frozen on training only. |
| B6 | GP with exactly the supplied W, Omega, D, mean, observation semantics and controller. Must match the latent-factor implementation. This is a parity/implementation control, not a target expected to lose. |
| P | Physically constructed W with exact-observation updates and direct joint CEI_local. Two-step lookahead is a separate bounded policy ablation using the same posterior/information and charged work for every compatible model. |

No agent communication or token cost is hidden: the deployed algorithm has no LLM agents. Generic single/multi-agent orchestration does not answer this small timing decision without separate motivation. The scientific roles remain independent and are not components of the algorithm.

A1 diagonalize cross-candidate covariance while preserving initial per-candidate marginals. A2 remove cross-output transfer, while keeping same-candidate dependence appropriately recorded. A3 shuffle signed W across candidates within a target. A4 exactly equivalent B6. A5 scalar bias/strongest calibration. A6 zero/opposite sensitivities, LUT edges and min/max path switches. A7 separable noiseless full-output block-design cancellation. A8 cold versus honestly amortized labels. A9 direct one-step CEI versus fantasy-regret equality before any EDA measurement. A10 equal-cost two-step transfer versus myopic posterior-updated CEI and same-information lookahead. Do not count Monte Carlo errors, mismatched data or equivalent code paths as a scientific effect.

## Cost, statistics, failures and stop rules

Charge checkpoint/extraction, candidate generation, shared and per-candidate probes, every training label, fitting, tuning/acquisition, apply/update/report/restore, rejected actions, final guard, invalidation, fallback, memory and elapsed/CPU. Reuse must be disclosed and given to compatible baselines. Clock/parallelism limits match. Report policy-time and full research data-production cost separately, then cold/amortized totals; no free oracle data.

Pair runs by checkpoint/candidate order/budget/seed. Aggregate by independent design family; include confidence intervals with cluster-respecting uncertainty and every failure. Freeze sample size using pilot variance before held-out comparisons. Do not select best seeds, discard slow/failing cases or tune on target outcomes. Averages alone cannot conceal tail regressions. Report the time/regret/guard-failure Pareto curve and preregistered operating point.

Stop on one invalid accepted choice, restore mismatch, hidden label/feature leakage, exhausted allocation, missing consent, unsupported derivatives, or failure of stated domain assumptions. UNKNOWN invokes valid reference fallback with cost charged; frequent fallback may kill usefulness. Stop predictive-system novelty if equivalent B6 or calibrated alternatives explain the entire claimed effect; equivalence is not itself evidence of a dead end for useful W construction. A new mechanism/user/scope needs a new topic ID and new review. Any task/dependency change requires a new frozen revision and renewed exact-task consents.

## EXP-000: actual bounded analytical results

Command actually executed in this job: `python3 scratch/analytical.py > runs/analytical.json`. The complete source below is also frozen so a reviewer need not access scratch. Save that single Python block as analytical.py and run `python3 analytical.py`. It imports only fractions/itertools/json, makes no network or EDA calls, reads no benchmark and fits no model. Source SHA256925560e2221339bb89ba376f8b2c9448fa52924020220b6ffa0ece3bce46f09e.

The six-row Gaussian algebra and the four-candidate finite law are separate mathematical fixtures. The latter is explicitly non-Gaussian; its exact policy values do not verify the proposed Gaussian electrical model. Both are synthetic, not measurements of circuit residuals or runtime gains. All finite-law candidates are feasible, so local/full feasibility coincide only inside this fixture. In real EDA, that coincidence is an untested assumption.

The finite witness has a diagnostic limitation: its query Q is stipulated to reveal a latent mode through a bundled margin. It shows the logical possibility of an information-bearing, non-improving query. It does not establish that a lawful cell replacement provides such an observation, that three such alternatives exist, or that physical W/GP approximations recover the law. EXP-003 must test those missing premises if authorized.

Reported exact output:

```json
{
  "scope": "constant-size exact rational algebra, not EDA data or calibration",
  "one_step_joint_CEI": [
    "0",
    "1",
    "1",
    "1"
  ],
  "two_step_correlated": [
    "3",
    "2",
    "2",
    "2"
  ],
  "two_step_independent_same_marginals": [
    "1",
    "5/3",
    "5/3",
    "5/3"
  ],
  "GP_latent_posterior_parity": "all means and covariance entries exactly equal",
  "queried_variances": [
    "0",
    "0"
  ],
  "incorrect_observation_noise_queried_variance": "217/1048",
  "correlated_constraint_CEI": "0; invalid factorization gives 1/4",
  "limits": "Finite law is non-Gaussian and not a Liberty circuit; it proves logical multi-step possibility only. GP parity is a separate Gaussian algebraic identity."
}
```

## Complete reproduction script

```python
"""Constant-size algebraic checks; no EDA calls, fitting, or external inputs."""
from fractions import Fraction as F
from itertools import product
import json

def T(a): return list(map(list, zip(*a)))
def mul(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def add(a,b,sign=1): return [[x+sign*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def inverse(a):
    n=len(a);v=[list(r)+s for r,s in zip(a,eye(n))]
    for i in range(n):
        p=next(k for k in range(i,n) if v[k][i]);v[i],v[p]=v[p],v[i]
        d=v[i][i];v[i]=[x/d for x in v[i]]
        for k in range(n):
            if k!=i:
                d=v[k][i];v[k]=[x-d*y for x,y in zip(v[k],v[i])]
    return [r[n:] for r in v]

def cond(K,obs,ys):
    ko=[[K[i][j] for j in obs] for i in range(len(K))]
    oo=[[K[i][j] for j in obs] for i in obs]
    gain=mul(ko,inverse(oo))
    return mul(gain,[[y] for y in ys]),add(K,mul(gain,T(ko)),-1)

W=[[F(x) for x in row] for row in [[1,0],[0,1],[-1,1],[1,1],[1,-1],[-1,-1]]]
Omega=[[F(1),F(1,3)],[F(1,3),F(2)]]
D=[[F(i==j,4) for j in range(6)] for i in range(6)]
K=add(mul(mul(W,Omega),T(W)),D)
# GP on index rows with exactly the same W, Omega, D.
mu_gp,cov_gp=cond(K,[0,1],[F(1),F(-1,2)])
# Bayesian linear latent state includes per-index deterministic discrepancy.
A=[r+e for r,e in zip(W,eye(6))]
S=[[F(0) for j in range(8)] for i in range(8)]
for i in range(2):
    for j in range(2): S[i][j]=Omega[i][j]
for i in range(6): S[i+2][i+2]=F(1,4)
B=[A[0],A[1]]
G=mul(mul(S,T(B)),inverse(mul(mul(B,S),T(B))))
mu_lat=mul(A,mul(G,[[F(1)],[F(-1,2)]]))
cov_lat=mul(mul(A,add(S,mul(mul(G,B),S),-1)),T(A))
assert mu_lat==mu_gp and cov_lat==cov_gp
assert all(cov_gp[i][j]==0 for i in [0,1] for j in range(6))
assert mu_gp[0][0]==1 and mu_gp[1][0]==F(-1,2)
# Wrong semantics: an added observation-noise D leaves queried latent labels uncertain.
ko=[[K[i][j] for j in [0,1]] for i in range(6)]
oo=[[K[i][j]+F(i==j,4) for j in [0,1]] for i in [0,1]]
wrong=add(K,mul(mul(ko,inverse(oo)),T(ko)),-1)
assert wrong[0][0]>0

# law: list of (probability, complete candidate table); each entry=(gain, margin)
def incumbent(table,obs): return max([F(0)]+[table[q][0] for q in obs if table[q][1]>=0])
def e(law,fun): return sum(p*fun(t) for p,t in law)
def posterior_groups(law,q):
    groups={}
    for p,t in law: groups.setdefault(t[q],[]).append((p,t))
    return [(sum(p for p,t in group),[(p/sum(p for p,t in group),t) for p,t in group]) for group in groups.values()]
def cei(law,q,obs):
    return e(law,lambda t:incumbent(t,obs+[q])-incumbent(t,obs))
def regret(law,obs):
    return e(law,lambda t:incumbent(t,list(range(len(t))))-incumbent(t,obs))
def fantasy_reduction(law,q,obs):
    return regret(law,obs)-sum(p*regret(post,obs+[q]) for p,post in posterior_groups(law,q))
def two_value(law,q):
    return sum(p*max(e(post,lambda t:incumbent(t,[q,r])) for r in range(len(post[0][1])) if r!=q) for p,post in posterior_groups(law,q))

# Q is a non-improving measured candidate whose bundled margin identifies one of three modes.
law=[]
for z in range(3):
    table=[(F(-1),F(z+1))]+[(F(3 if z==i else -1),F(1)) for i in range(3)]
    law.append((F(1,3),table))
for q in range(4): assert cei(law,q,[])==fantasy_reduction(law,q,[])
# Equality remains true after every possible first observation, with nonzero incumbents.
for first in range(4):
    for p,post in posterior_groups(law,first):
        for q in range(4):
            if q!=first: assert cei(post,q,[first])==fantasy_reduction(post,q,[first])
assert [cei(law,q,[]) for q in range(4)]==[F(0),F(1),F(1),F(1)]
assert [two_value(law,q) for q in range(4)]==[F(3),F(2),F(2),F(2)]
# Independent same-candidate marginals: Q cannot inform any target.
ind=[]
for z,b1,b2,b3 in product(range(3),repeat=4):
    t=[(F(-1),F(z+1))]+[(F(3 if b==0 else -1),F(1)) for b in [b1,b2,b3]]
    ind.append((F(1,81),t))
assert [cei(ind,q,[]) for q in range(4)]==[F(0),F(1),F(1),F(1)]
assert [two_value(ind,q) for q in range(4)]==[F(1),F(5,3),F(5,3),F(5,3)]
# Same-candidate feasibility dependence: EI * P(feasible) is incorrect.
coupled=[(F(1,2),[(F(1),F(-1))]),(F(1,2),[(F(-1),F(1))])]
assert cei(coupled,0,[])==0
assert e(coupled,lambda t:max(F(0),t[0][0]))*e(coupled,lambda t:F(t[0][1]>=0))==F(1,4)
result={
 'scope':'constant-size exact rational algebra, not EDA data or calibration',
 'one_step_joint_CEI':[str(cei(law,q,[])) for q in range(4)],
 'two_step_correlated':[str(two_value(law,q)) for q in range(4)],
 'two_step_independent_same_marginals':[str(two_value(ind,q)) for q in range(4)],
 'GP_latent_posterior_parity':'all means and covariance entries exactly equal',
 'queried_variances':[str(cov_gp[i][i]) for i in [0,1]],
 'incorrect_observation_noise_queried_variance':str(wrong[0][0]),
 'correlated_constraint_CEI':'0; invalid factorization gives 1/4',
 'limits':'Finite law is non-Gaussian and not a Liberty circuit; it proves logical multi-step possibility only. GP parity is a separate Gaussian algebraic identity.'}
print(json.dumps(result,indent=2))
```


## Submission checks and publication boundary

Current local checks: all frozen policy-file and released-input payload hashes matched; own analytical assertions passed. The role release uses trusted role_submission.py freeze/verify and the supplied compliance validator. Full-repository project.py validate is a coordinator publication check because the standalone job lacks the entire repository and foreign harnesses. No checkout access is used to simulate that check. Freeze validates bytes/provenance, not scientific truth or pilot readiness. Source copies and local runs remain private to this job; public reproduction code/results are only the bounded own arithmetic above.
