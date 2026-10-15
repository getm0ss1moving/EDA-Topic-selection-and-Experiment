# Independent challenger review: EDA-0007 R2

Reviewed proposal: SUB-ebe8adb725c37ba6e164d487febc9021dddc8e911cf79e56ada9e9d2bd5c5ace. Input commit b1bb69f62b089c3489eaf17dea34daae84af315c; actor ChatGPT-C05-TIMING-B03-EDA-0007-REPLACEMENT-1-3f76bcf0; session a758be30-1627-4434-bc85-379554161f43; job 5e45854a-abda-4878-90f2-fd99030102e3. Additional batch0003 cycle2/4. Research review is explicitly unblinded. Prior released P1 and V1 were read for context; no prior signature or independent approval is inherited.

Assessment: **unresolved**, retain the conditional anchored hypothesis, no pilot consent. No supported fatal contradiction or newly supported blocking objection was found in the narrowed R2 claims. Physical usefulness and experiment readiness remain unresolved for the reasons R2 itself states. The analytical witness is valid; its robustness boundary deserves a sharper falsification task. This is a scientific review, not the separate protocol audit.

## Independent positive checks

CLM-703: The one-step reduction follows the tower property with a fixed table optimum and measured feasible incumbent. The same-W GP and latent representation have identical finite-dimensional Gaussian laws. Persistent indexed D differs from independent observation noise. These are algebraic statements under the proposal's explicit assumptions, not physical validation. S01 section2.3 assumes independent objective/constraint priors for its factorized EI; that assumption cannot be imported into R2's joint bundles.

CLM-704/708: The mixed-rank Gaussian witness works. Q reveals both latent coordinates; A dominates Q as a return candidate wherever Q is feasible. C-first leaves A/B conditionally exchangeable, with Q no better than A as the last measurement. I independently obtain exact expectations:

U_Q = (sqrt(2)+2 sqrt(5))/(2 sqrt(2 pi)) = 1.174156849850264.

U_myopic = (1+sqrt(5)+sqrt(2))/(2 sqrt(2 pi)) = 0.9275969610127873.

Gap = (sqrt(5)-1)/(2 sqrt(2 pi)) = 0.24655988883747648.

Derivation: write Z=R(cos theta,sin theta), E[R]=sqrt(pi/2). Each maximum is the support function of the convex hull of its coefficient vectors. Integrating the active sinusoid on each polygon normal interval yields its perimeter; multiply by E[R]/(2 pi). The full hull is the triangle (1,0),(0,1),(-1,-1), with the origin inside; the myopic hull is (0,0),(1,0),(-1,-1). Their perimeters give the formulas. Independently written 8192-bin angular sums match to <1e-6. These stipulated dimensionless results are neither EDA measurements nor a new acquisition contribution.

CLM-710: S04 raw lines44-66 independently confirms cap-preservation and replacement failure branches, journaled measurement, raw negative score retention, and an improvement-based legal flag. Separating query success, replacement legality and improvement is warranted. I did not inspect the complete restoration transitive closure or build anything. S05 confirms the selected slew-bias interpolation only.

## OBJ-001: clarify singular-witness robustness, a minor nonblocking analytical concern

Target: CLM-708 and EXP-004/A11, specifically extrapolating the mixed-rank witness toward physical information benefit. Evidence: R2 proposal/controller and experiment-plan Gaussian witness; A-C01 below; S01 section3.2 provides the established two-step objective, not this derived limit.

Construct an arbitrarily small coefficient perturbation with unchanged gains:
Q=(z1-2,z2), A=(z1,1+epsilon*z2), B=(z2,1+epsilon*z1), C=(-z1-z2,1+epsilon*z1).
For every nonzero epsilon, bundled W determinants in Q/A/B/C order are (1,epsilon,-epsilon,epsilon). With known coefficients, D=0 and exact full-bundle observations, every first query identifies z. With two equal-cost queries, any exact posterior-updated policy choosing the best feasible remaining candidate on its final query reaches the table optimum. In particular the optimized lookahead versus posterior-updated myopic terminal gap is zero. This remains true even though perturbed feasibility can differ in Gaussian tails; the conclusion concerns each perturbed problem's own feasible optimum.

At epsilon=0 the gap above is positive. Thus this idealized positive example has a discontinuous policy-value gap under an arbitrarily small rank-restoring perturbation. R2 already declares degeneracy; this does not refute its possibility claim or its broader physical-W hypothesis. It sharpens why numerical rank, persistent D and practical inference must be separated. Near singularity alone is not partial information under infinite-precision deterministic observation.

Severity: minor, nonblocking; confidence: high for exact known-W/D0/equal-cost premises; physical prevalence unknown. Reversal condition: explicit nonzero persistent discrepancy, unknown W/mean, incomplete bundles, limited observation resolution or unequal budgets invalidates the full-identification argument; those conditions need their own model and test rather than artificial query noise. Cheapest decisive test: exact determinant/support calculations on the four blocks followed by the full-identification lemma; tiny own rational checks at epsilon=1/10,1/1000,1/1000000 passed. Add the epsilon-versus-D robustness grid as a future allocated test, retaining exact-observation semantics. The verifier must adjudicate this OBJ before it becomes a proposer requirement.

## Coverage, novelty and task position

| Area | Status | Evidence and consequence |
|---|---|---|
| Duplicate/equivalent prior art | unresolved | S01 establishes constrained lookahead; S02 electrical directional guidance and calibration; S03 calibrated incremental/peephole sizing. No checked source establishes identical physical-W complete system. Absence of a match is not novelty. |
| Mechanism | supported algebra; physical claim unresolved | R2 coherent and same-W GP equivalence explicit. A-C01 supports possibility and a narrow robustness limit. |
| Useful composition | unresolved | Need cost/quality value from the electrical contrast construction after mean calibration, not covariance/GP names. Known components are eligible. |
| Engineering demand | unresolved | S04 is an actual consumer, but meaningful candidate multiplicity, query share and local/global utility are unmeasured. |
| Commercial/open comparability | unresolved | Selected open code is checked; no independent vendor-internals audit or superiority/absence assertion. |
| Headroom | unresolved physically | Exact full-rank/D0 saturation is conditional; no universal timing limit. Quantitative EDA gain remains unknown. |
| Contest-provided ideas | unresolved | S06/S07 identify current context; S08 reveals edition-mismatched closing-slide routing. Winner methods remain unauthenticated. |
| Experiments | unresolved readiness | Safe complete adapter, lawful workload, named implementers/reproducer and allocation still absent; do not execute dormant tasks. |
| Full cost | supported specification; amounts unknown | R2 charges probes/labels/fit/policy/restore/guards/failures, including cold and amortized costs. No measured savings. |

New expansion S09 identifies derivative-aware Bayesian analog sizing as an adjacent methodological lead. Its publisher-indexed abstract describes sensitivity information improving GP posteriors. This is not a full-method equivalence finding for deterministic digital replacement contrasts; direct source opening failed. Do not impose a complete analog-flow reproduction as a digital baseline without a justified mapping.

Both direction penalties are zero: the current user, electrical contrast, deterministic bundled measurement and guarded measured-only return remain anchored. Adding a rank robustness control does not change the mechanism. No joint abandonment is supported: uncertain physical value is not exhausted novelty or a demonstrated dead end. Current exact task hash is 0fb946b23dce8b14b97d3baf43cb04cecabbfc82f872947869668dfe82c5bda8; I request revision/readiness closure, not agreement. Preserve the batch three-cycle park/four-cycle hard stop.

## A-C01 reproducible own analytical check

The following script was authored and executed in this job, with output recorded in runs/analytical_check.json. No foreign experiment code, EDA tool, training or external compute was executed.

```python
from math import sqrt,pi,cos,sin
from fractions import Fraction as F
import json
# Independently derived perimeter formula for a planar isotropic Gaussian support function.
uq=(sqrt(2)+2*sqrt(5))/(2*sqrt(2*pi))
um=(1+sqrt(5)+sqrt(2))/(2*sqrt(2*pi))
diff=(sqrt(5)-1)/(2*sqrt(2*pi))
n=8192
quad=lambda full:sqrt(pi/2)*sum(max([0,cos((k+.5)*2*pi/n),-cos((k+.5)*2*pi/n)-sin((k+.5)*2*pi/n)]+([sin((k+.5)*2*pi/n)] if full else [])) for k in range(n))/n
assert abs(quad(True)-uq)<1e-6 and abs(quad(False)-um)<1e-6
rows=[]
for e in [F(1,10),F(1,1000),F(1,10**6)]:
    blocks=[[[F(1),F(0)],[F(0),F(1)]],[[F(1),F(0)],[F(0),e]],[[F(0),F(1)],[e,F(0)]],[[F(-1),F(-1)],[e,F(0)]]]
    dets=[a[0][0]*a[1][1]-a[0][1]*a[1][0] for a in blocks]
    assert all(d!=0 for d in dets)
    rows.append({'epsilon':str(e),'determinants':[str(d) for d in dets], 'exact_D0_two_query_policy_gap':'0 by full-identification lemma'})
print(json.dumps({'scope':'own tiny arithmetic; no EDA data, fit or deployment result','Q_first_closed_form':uq,'myopic_closed_form':um,'gap_closed_form':diff,'quadrature_8192':[quad(True),quad(False)],'perturbed_rank_checks':rows},indent=2))
```

Observed output:

```json
{
  "scope": "own tiny arithmetic; no EDA data, fit or deployment result",
  "Q_first_closed_form": 1.174156849850264,
  "myopic_closed_form": 0.9275969610127873,
  "gap_closed_form": 0.24655988883747648,
  "quadrature_8192": [
    1.17415681368716,
    0.9275969512778293
  ],
  "perturbed_rank_checks": [
    {
      "epsilon": "1/10",
      "determinants": [
        "1",
        "1/10",
        "-1/10",
        "1/10"
      ],
      "exact_D0_two_query_policy_gap": "0 by full-identification lemma"
    },
    {
      "epsilon": "1/1000",
      "determinants": [
        "1",
        "1/1000",
        "-1/1000",
        "1/1000"
      ],
      "exact_D0_two_query_policy_gap": "0 by full-identification lemma"
    },
    {
      "epsilon": "1/1000000",
      "determinants": [
        "1",
        "1/1000000",
        "-1/1000000",
        "1/1000000"
      ],
      "exact_D0_two_query_policy_gap": "0 by full-identification lemma"
    }
  ]
}
```

Local integrity: all payload SHA256 values matched for the three read released inputs. Byte hashing of other files in those releases does not imply semantic review of them. Trusted freeze/verify and ledger validation are structural checks only; full project.py validate belongs to coordinator publication because this standalone packet lacks the repository. No checkout was accessed.
