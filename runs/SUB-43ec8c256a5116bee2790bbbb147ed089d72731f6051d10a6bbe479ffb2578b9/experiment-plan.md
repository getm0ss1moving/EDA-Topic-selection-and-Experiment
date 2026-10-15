# R3 experiment specification and completed tiny analytical diagnostic

Actor ChatGPT-P05-TIMING-B03-EDA-0007-REPLACEMENT-1-8154ee5a; session 5796edbb-fac9-477b-ab72-194c4cbfe34c; job 2d6a2a36-2080-4a78-ba1b-fad40c12219d; input b1bb69f62b089c3489eaf17dea34daae84af315c; packet a33750c8ec5badb03663cf317bd8b6ea96e6e5d9905fe82f0c50861adbbe46d9. Additional cycle3/4.

Only EXP-000R3 and public source reading were executed in this job. All EDA builds, label generation, training/fitting, full flows, remote compute and paid calls remain dormant. This plan is an independently reviewable proposal, not resource permission. Earlier scripts/results in P2 remain historical and were not rerun unless explicitly listed below. No actual implementation/reproduction owner is assigned by a role title.

## Reference transaction and correctness contract

Pin source OpenROAD3549d60529517dc82deb7f0ff769345e9a424911 only as a source candidate, together with compatible OpenSTA/OpenDB/build/config/library/SDC/parasitic/generator locks before building. This source snapshot is not a verified installed binary. T01/T02/T03/T04 show the immediate measurement/selection path; complete transitive invalidation and restore closure remain unknown.

Freeze the base checkpoint and deterministic ordered alternative list. For each query: validate replacement legality/cap requirements; apply from base; update parasitics/timing; capture g,m and all declared global guards BEFORE undo; restore; check database plus full oracle state. Keep separate replacement_legal, query_succeeded, improves, F_loc,F_full, UNKNOWN and failure reason. Missing margin is UNKNOWN. Do not lose non-improving labels because Estimate.legal is score-based. Measured-only return requires final full guards. Querying an identical frozen candidate twice reveals the same label, never an independent draw of eta. Unsupported domain/reference failure returns charged fallback or stops, never an invented feasible label.

First restoration mismatch invalidates the following labels and stops generation. Exactness is engine/model/checkpoint-relative only. No guarantee about all unqueried candidates, silicon signoff, global optimum or expanded corner scope.

## Data and ownership prerequisites

Future inventory must establish lawfully accessible checkpoint/library/PDK/design rights; actual n after source/config/physical filters; per-query timing; source-state/restoration hash scheme; cold/amortized baseline cost; representative families and independent owners. A single public GCD smoke in historical policy is not representative workload or current access validation. A pinned generation procedure can bind future data before consent: exact input/tool/config/script hashes, validation/oracle, cap and stop rule. Do not demand full experiments before consent and do not execute to fill those hashes without an allocation.

## Baseline and attribution contract

| Method | Information/model | Matched procedure |
|---|---|---|
| B0 | Exhaustive reference enumeration and full guards | Same ordered candidates/checkpoint; fully charged timing oracle |
| B1 | Strong supported T05/T06 local/offset/load calibration | Same raw inputs and reference label budget, calibration charged |
| B2 | Faithfully adapted T08 directional/multi-level calibration | Same compatible scope/input/label budget; do not claim whole author-flow reproduction |
| B3 | Separate gain/slew specialists plus ordinary fusion | Same electrical inputs, training families, query/fit budget |
| B4 | Bounded shared-trunk predictor | Same total fitting budget and held-out families; report negative transfer |
| B5 | Ordinary electrical-feature GP | Same raw features/mean and compatible CEI/lookahead sweep |
| B6 | EXACT proposed mu,W,Omega,D and observations | Predictive/action parity required with P under identical controller |
| P | Calibrated mean, proposed physical contrast W, indexed persistent D | Joint CEI default, separately bounded equal-cost two-query diagnostic |

Disclose four layers for every comparator: raw inputs, corrected mean, W/covariance, controller. No baseline loses deployable features or labels given to P. T08 requires especially strong input/mean calibration parity. DarBO is an adjacent lead only until a justified available-method mapping exists, not a compulsory incomparable analog experiment.

A1 removes cross-candidate dependence preserving each candidate's JOINT gain/margin marginal; A2 separately removes cross-output dependence with changed assumptions declared; A3 shuffles W signs/rows; A4 B6 exact parity; A5 strong mean/scalar calibration; A6 LUT/path/min/max and zero/opposite slopes; A7 noiseless separable block-design cancellation; A8 cold/amortized labels; A9 one-step fantasy equals joint CEI; A10 policy comparison under identical posterior; A11 epsilon/rank/D robustness below. Do not call A1 a lookahead attribution or A10 an isolated covariance attribution.

## Headroom and total cost before expensive implementation

Let n be actual legal/queryable alternatives, k measured alternatives and t equal full transaction time. With otherwise identical base/guards and added surrogate/controller overhead H, net time saving requires H<(n-k)t. For k2 and n<=2 the fixed two-query diagnostic cannot save calls. Real unequal-cost comparisons use measured sums and actual guard/fallback differences; the formula is a conditional accounting screen, not an optimal stopping theorem. Record candidate n and timing-share distribution, not only promising cases. Do not expand beyond the anchor to manufacture candidates.

Charge T_base+T_features+T_labels+T_fit+T_acquisition+sum(T_apply+T_update+T_report+T_restore)+T_guard+T_fallback, all failed/UNKNOWN/rejected queries, checkpoints/extraction and peak memory. Pair methods by frozen candidate table/order/seed/remaining budget. Family-level splits prevent variants/checkpoints leakage. Freeze meaningful endpoint tolerances/sample sizes before held-out outcomes, with practitioner/variance evidence. Prior provisional20%/5ps figures are not established requirements or this job's grant. No runtime LLM agents are proposed.

## EXP-000R3: epsilon/persistent-D scale diagnostic, completed

Use z~N(0,I2), persistent eta~N(0,rho I8), exact y=mu+Wz+eta. Row blocks are Q=[[1,0],[0,1]], A=[[1,0],[0,epsilon]], B=[[0,1],[epsilon,0]], C=[[-1,-1],[epsilon,0]]. Means follow the declared perturbed Gaussian witness; covariance diagnostics do not depend on those means. Epsilon/rho0 singular observation blocks are conditioned on independent row support, not regularized with artificial query noise.

For A and rho>0, posterior latent variance z2=rho/(epsilon²+rho), with z1=rho/(1+rho). Exact observed TABLE entries have zero covariance even when latent z remains uncertain. At epsilon=rho0 support conditioning gives latent diag(0,1). Along rho=c epsilon² the residual z2 fraction c/(1+c) remains finite; different limit orders give0 and1. The code verifies all stated formulas and queried-zero covariance for96 combinations over all four queries.

For fixed W and independent indexed D=rho I, unobserved prior variance grows with rho while its cross-transfer reduction C_UO(C_OO+rho I)^-1C_OU, where C=W Omega W^T decreases to0. This is why positive D is neither physical information evidence nor policy utility. Approximate numerical rank, unknown W, finite observation resolution and unequal budgets are separate untested models; do not use them to evade the exact lemma silently.

Observed selected output (rational fractions exact):

```json
{
  "scope": "own tiny exact rational analysis; no EDA labels, fitting, policy search or physical measurements",
  "grid_rows": 96,
  "selected_A_rows": [
    {
      "epsilon": "0",
      "rho": "0",
      "latent_z2_variance": "1",
      "observed_covariance_zero": true,
      "fractional_trace_reduction": "2/5"
    },
    {
      "epsilon": "1/1000",
      "rho": "0",
      "latent_z2_variance": "0",
      "observed_covariance_zero": true,
      "fractional_trace_reduction": "1"
    },
    {
      "epsilon": "1/1000",
      "rho": "1/1000000000000",
      "latent_z2_variance": "1/1000001",
      "observed_covariance_zero": true,
      "fractional_trace_reduction": "2500002000002500000000000000000/2500003500006500006500004000003"
    },
    {
      "epsilon": "1/1000",
      "rho": "1/1000000",
      "latent_z2_variance": "1/2",
      "observed_covariance_zero": true,
      "fractional_trace_reduction": "437500/625001"
    },
    {
      "epsilon": "1/1000",
      "rho": "1/100",
      "latent_z2_variance": "10000/10001",
      "observed_covariance_zero": true,
      "fractional_trace_reduction": "9903490100/25302540001"
    },
    {
      "epsilon": "1/1000",
      "rho": "100",
      "latent_z2_variance": "100000000/100000001",
      "observed_covariance_zero": true,
      "fractional_trace_reduction": "990101509901/30250000402500001"
    }
  ],
  "rho_over_epsilon_squared_paths": [
    {
      "epsilon": "1/10",
      "rho": "1/10000",
      "latent_z2_variance": "1/101"
    },
    {
      "epsilon": "1/10",
      "rho": "1/100",
      "latent_z2_variance": "1/2"
    },
    {
      "epsilon": "1/10",
      "rho": "1",
      "latent_z2_variance": "100/101"
    },
    {
      "epsilon": "1/1000",
      "rho": "1/100000000",
      "latent_z2_variance": "1/101"
    },
    {
      "epsilon": "1/1000",
      "rho": "1/1000000",
      "latent_z2_variance": "1/2"
    },
    {
      "epsilon": "1/1000",
      "rho": "1/10000",
      "latent_z2_variance": "100/101"
    },
    {
      "epsilon": "1/1000000",
      "rho": "1/100000000000000",
      "latent_z2_variance": "1/101"
    },
    {
      "epsilon": "1/1000000",
      "rho": "1/1000000000000",
      "latent_z2_variance": "1/2"
    },
    {
      "epsilon": "1/1000000",
      "rho": "1/10000000000",
      "latent_z2_variance": "100/101"
    }
  ],
  "policy_limits": {
    "singular_D0_Q_first": 1.174156849850264,
    "singular_D0_myopic": 0.9275969610127873,
    "singular_D0_gap": 0.2465598888374766,
    "all_full_rank_D0_gap_for_every_nonzero_epsilon": "0 by identification lemma; perturbed feasible set respected"
  }
}
```

The singular policy closed forms are (sqrt2+2sqrt5)/(2sqrt(2pi)) and(1+sqrt5+sqrt2)/(2sqrt(2pi)); their difference is(sqrt5-1)/(2sqrt(2pi)). These reproduce only stipulated mathematics, not a positive-D value function, calibration, timing measurement or EDA speedup. For nonzero epsilon/rho0, every bundle is invertible and the exact two-query policy gap is zero by identification, respecting each perturbed feasible set. Prior P2 matched-independent control0.568435 and earlier finite-law/GP fixtures remain preserved historical evidence, not new R3 executions.

Actual command: `python3 scratch/r3_robustness.py > runs/r3_robustness.json`. Script SHA256 `17b71ff8dde24a29674837bc9b5fbd52573b764203bc91132bd189e101afe0f7`; full96-row result SHA256 `fdec7b92563554def7eebdc43d2b3956991037e2ba915686278266e61bb5e03d`. The released reproduction below prints all rows using only the Python standard library. Save as r3_robustness.py and run `python3 r3_robustness.py`. No external code or data is executed.

```python
"""Own constant-size exact covariance test; not EDA, fitting, or physical data."""
from fractions import Fraction as F
from math import sqrt,pi
import json

def trans(a): return list(map(list,zip(*a)))
def mm(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def sub(a,b): return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def inv2(a):
    x,y=a[0]; z,t=a[1]; den=x*t-y*z
    assert den
    return [[t/den,-y/den],[-z/den,x/den]]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def block(e): return [[F(x) for x in r] for r in [(1,0),(0,1),(1,0),(0,e),(0,1),(e,0),(-1,-1),(e,0)]]
def check(e,rho,q):
    w=block(e);obs=[2*q,2*q+1];n=len(w)
    k=mm(w,trans(w));k=[[v+rho*(i==j) for j,v in enumerate(row)] for i,row in enumerate(k)]
    # At exact rho=0, choose a full-rank row support. Zero rows are deterministic.
    support=obs
    a,b=w[obs[0]],w[obs[1]]
    det=a[0]*b[1]-a[1]*b[0]
    if rho==0 and det==0:support=[obs[0]]
    koo=[[k[i][j] for j in support] for i in support]
    ik=inv2(koo) if len(support)==2 else [[1/koo[0][0]]]
    ko=[[k[i][j] for j in support] for i in range(n)]
    reduction=mm(mm(ko,ik),trans(ko));post=sub(k,reduction)
    assert all(post[i][j]==0 for i in obs for j in range(n))
    # Repeating an exact observation conditions no new random variable, hence no update.
    assert all(post[i][i]>=0 for i in range(n))
    wo=[w[i] for i in support]
    latent=sub(eye(2),mm(mm(trans(wo),ik),wo))
    unobs=[i for i in range(n) if i not in obs]
    rem=sum(post[i][i] for i in unobs)
    prior=sum(k[i][i] for i in unobs)
    transfer=sum(reduction[i][i] for i in unobs)
    assert rem+transfer==prior
    if rho==0 and det:assert rem==0 and latent==[[0,0],[0,0]]
    if q==1:
        expected=F(1) if e==rho==0 else rho/(e*e+rho)
        assert latent[1][1]==expected
    return {'epsilon':str(e),'rho':str(rho),'query':'QABC'[q], 'determinant':str(det),
      'observed_covariance_zero':True,'latent_trace':str(latent[0][0]+latent[1][1]),
      'latent_z2_variance':str(latent[1][1]),'unobserved_trace':str(rem),
      'unobserved_prior_trace':str(prior),'cross_transfer_trace_reduction':str(transfer),
      'fractional_trace_reduction':str(transfer/prior) if prior else None}
rows=[]
for e in [F(0),F(1,10),F(1,1000),F(1,10**6)]:
    for rho in sorted({F(0),F(1,10**12),F(1,10**6),F(1,100),F(1),F(100),e*e}):
        rows.extend(check(e,rho,q) for q in range(4))
# Positive gap and perturbation-zero gap: exact theorem values, not optimization simulation.
uq=(sqrt(2)+2*sqrt(5))/(2*sqrt(2*pi))
um=(1+sqrt(5)+sqrt(2))/(2*sqrt(2*pi))
assert uq>um
paths=[]
for e in [F(1,10),F(1,1000),F(1,10**6)]:
    for ratio in [F(1,100),F(1),F(100)]:
        r=check(e,ratio*e*e,1)
        assert F(r['latent_z2_variance'])==ratio/(1+ratio)
        paths.append({k:r[k] for k in ['epsilon','rho','latent_z2_variance']})
# Exact noncommuting limits: at epsilon!=0 rho->0 var z2=0; at rho>0 epsilon->0 var=1.
# High D is not a positive transfer claim; fixed W cross reduction ->0 as rho->infinity.
high=[check(F(1,1000),rho,1) for rho in [F(1),F(100),F(10**6)]]
assert all(F(a['cross_transfer_trace_reduction'])>F(b['cross_transfer_trace_reduction']) for a,b in zip(high,high[1:]))
out={'scope':'own tiny exact rational analysis; no EDA labels, fitting, policy search or physical measurements',
 'grid_rows':len(rows),'grid':rows,'rho_over_epsilon_squared_paths':paths,
 'known_exact_policy_values':{'singular_D0_Q_first':uq,'singular_D0_myopic':um,'singular_D0_gap':uq-um,
 'all_full_rank_D0_gap_for_every_nonzero_epsilon':'0 by identification lemma; perturbed feasible set respected'},
 'high_D_transfer':high,
 'limits':'Variance/transfer are diagnostics only, not downstream utility or positive persistent-D policy-value evidence. Known W/mu; exact bundles; indexed D; dimensionless stipulated coefficients.'}
print(json.dumps(out,indent=2))
```

## EXP-004/A11: future physical and policy boundary test, dormant

Before any positive physical-information claim, report calibrated W singular values and exact/numerical rank, normalization, held-out persistent-D scale and observation precision. Include all-invertible D0, mixed/singular D0, epsilon nonzero with rho below/comparable/above epsilon², and high-D/no-transfer controls. Retain exact output conditioning and observed-zero covariance. Support equations/pseudoinverse must have a declared rank/precision criterion; any approximation is labeled, charged and checked against the exact diagnostic. No repeated-query denoising of indexed discrepancy.

Policy evaluation must optimize or bound the same declared adaptive tree under a fixed budget, with integration/error tolerances frozen, strongest posterior-updated myopic comparator and identical observation bundles. Current A03 covariance trace is not a policy reward or proof of positive-D gap. For covariance comparisons preserve joint candidate marginals; for policy comparisons hold posterior fixed. No all-full-rank/D0 two-query gain and no identical-W GP advantage is allowed. If observed, stop and debug before reporting performance.

## Validation and stopping

Stop on invalid accepted output, restoration mismatch, missing allocation/consent, unavailable lawful input, leakage, invalid derivative, nonexistent candidate headroom or unjustified local/global utility. Withdraw physical-W contribution if strong mean/directional calibration explains all useful effect; equivalent GP disagreement is a bug. These checks can falsify the anchored approach; they are not mandatory performance promises. A new mechanism or user needs a new topic ID.

Trusted standalone freeze/verify and ledger validation are the local structural checks. The packet lacks the complete project; full project.py validate and PR/check publication belong to the coordinator. No checkout access is used to simulate them. A green freeze proves bytes/form, not independent scientific merit or absence of undisclosed actions.
