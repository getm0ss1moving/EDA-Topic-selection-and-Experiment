# Experiment plan and completed own analytical check

## Position and hypotheses

H1: candidate-relative shared-boundary enclosures can avoid enough exact local refreshes to reduce complete time while preserving a pinned full-refresh LR winner/guard/score contract. H0a: cheap precise boundary updates/caches dominate. H0b: generic affine/branch-bound transplantation captures all benefit. H0c: sound enclosures are too loose or costly. H0d: omitted context or floating details make certificates unsound. No H1 experiment is executed or allocated; T01-T08 remain dormant.

Primary future metric: total wall time per reference-equivalent decision sequence and completed closure, including all failures/fallbacks; lower is better. Correctness: exact candidate/tie/guard/acceptance agreement under pinned arithmetic semantics, zero unsupported certified outcomes. Final WNS/TNS, electrical limits, leakage/area and failure counts are downstream guardrails. Meaningful-effect threshold and statistical power are null pending T04/T05. No toy count is a speedup or engineer threshold.

B0 cached exact reference, B1 heuristic low-criticality pruning, B2 independent absolute bounds, B3 strongest generic validated affine/branch-bound transplant, B4 exact-boundary conventional task/cache controller, candidate and optional identical-checker learned composition receive identical candidate sets, operations, dependencies, memory limits and information. Any exact bound kernel or representation improvement is offered to B3. B1 is approximate and must be labelled as a distinct cost/quality point. Same R choices under identical deterministic commit semantics should yield the same later trajectory; external placement/routing changes require final fresh checks, not a theoretical guarantee.

Prospective data: independently selected public design families with verified individual licenses and reproducible NLDM/SDC/RC pins; no new design files downloaded here. Group all variants/checkpoints/ECO traces from one base family. Features cannot contain later exact survivor costs or future route information. For optional learned refinements, hold out entire families and declared library/corner groups; charge exact labeling and training and disclose public-corpus/LLM contamination uncertainty. At present neither a training set nor a real workload census exists. No commercial license or foundry-signoff authority is asserted.

## A01: own finite analytical check, actually executed

Purpose: exhibit the interval dependency problem in candidate comparisons, a stale weighted-term rank reversal, and a strong conventional negative control. All costs are rational affine functions of one shared scalar x; feasibility is fixed true, no circuit graph, NLDM, real dependency recorder or elapsed-time benchmark is present. This is algebraic research only. It neither establishes a useful EDA mechanism nor validates float/guard handling.

Parameters are embedded below:9 affine functions from slopes/intercepts{-2,0,2},81 ordered function pairs,5 x values{-2,-1,0,1,2},domain[-2,2]; lexicographic tie keeps alternative0. Each certified relation requires strict sign, otherwise exact fallback. Independent absolute intervals, paired coefficient differences and a separately written ordinary affine-form transplant receive identical inputs. Each of405 pair/x cases is compared to exact rational selection. No random seed, imports beyond Python standard library or external code execution.

To replay, copy exactly this code block into a UTF-8 file with LF and final newline, and run `python3 check.py`. Code SHA-256 `07a1bff92cd3fbd3fe36dd12ac4dc52ac88199a5910a8cb474128d593f84fd26`. Compact stdout SHA-256 `3748e862515f2192aa6ef1df243fab8642be6e0eee0733699aeefc169ace2775`. The author executed the identical source as own-check.py in this assigned job; it is embedded here because arbitrary .py files are not release-allowlisted. Public artifact is this file, not a private scratch locator.

```python
from fractions import Fraction as F
from itertools import product
import json

def val(f,x):
    return f[0]*x+f[1]

def hull(f,lo,hi):
    return min(val(f,lo),val(f,hi)),max(val(f,lo),val(f,hi))

def separate(a,b,lo,hi):
    al,au=hull(a,lo,hi); bl,bu=hull(b,lo,hi)
    return al-bu,au-bl

def paired(a,b,lo,hi):
    return hull((a[0]-b[0],a[1]-b[1]),lo,hi)

def aa_transplant(a,b,lo,hi):
    mid=(lo+hi)/2; radius=(hi-lo)/2
    center=val(a,mid)-val(b,mid)
    err=abs((a[0]-b[0])*radius)
    return center-err,center+err

def choice(a,b,x):
    return 0 if val(a,x)<=val(b,x) else 1

def certified(a,b,lo,hi,x,method):
    low,up=method(a,b,lo,hi)
    if up<0: return 0,False
    if low>0: return 1,False
    return choice(a,b,x),True

fs=list(product(map(F,[-2,0,2]),repeat=2))
xs=list(map(F,[-2,-1,0,1,2]))
rows=0; sep_fallback=0; pair_fallback=0; aa_fallback=0
for a,b,x in product(fs,fs,xs):
    oracle=choice(a,b,x)
    for method in (separate,paired,aa_transplant):
        got,fallback=certified(a,b,F(-2),F(2),x,method)
        assert got==oracle
        if method==separate: sep_fallback+=fallback
        if method==paired: pair_fallback+=fallback
        if method==aa_transplant: aa_fallback+=fallback
    assert paired(a,b,F(-2),F(2))==aa_transplant(a,b,F(-2),F(2))
    rows+=1
print(json.dumps({'cases':rows,'mismatches':0,'separate_fallback_cases':sep_fallback,'paired_fallback_cases':pair_fallback,'aa_transplant_fallback_cases':aa_fallback},sort_keys=True))
a=(F(100),F(3)); b=(F(100),F(4))
print('common_mode',str(separate(a,b,F(0),F(10))),str(paired(a,b,F(0),F(10))))
stale=(F(0),F(1)); fresh=(F(0)+F(1,100)*F(200),F(1))
print('low_weight_stale_choice',min(range(2),key=lambda i:(stale[i],i)),'fresh_choice',min(range(2),key=lambda i:(fresh[i],i)))
print('all_guards_true; exact_rational_affine_model; no_STA_or_time_measurement')
```

Exact stdout:

```text
{"aa_transplant_fallback_cases": 315, "cases": 405, "mismatches": 0, "paired_fallback_cases": 315, "separate_fallback_cases": 375}
common_mode (Fraction(-1001, 1), Fraction(999, 1)) (Fraction(-1, 1), Fraction(-1, 1))
low_weight_stale_choice 0 fresh_choice 1
all_guards_true; exact_rational_affine_model; no_STA_or_time_measurement
```

Interpretation: no mismatches in this finite model. Paired and generic affine bounds coincide throughout; their315 fallback cases versus independent-interval375 are not independent-call or primitive counts and include repeated x tests for the same pair. The common-mode difference is[-1,-1] rather than[-1001,999]. The small-weight fixture reverses stale choice0 to fresh1. There are no measured saved seconds, process bytes or physical timing values. Arithmetic cancellation is fully transplantable here. A01 exposes the strongest alternative explanation instead of certifying novelty.

## Future proof/implementation requirements

Pin the same scalar reference first; full neighborhood and upstream-load/slew effects cannot be omitted. A current box Z must contain actual context under every supported operation; cheapness and containment both require testing. NLDM region overlays and affine remainders must include branch changes and rounding. Guard UNKNOWN/NaN/extrapolation use full fallback. Test restoration and changed provenance even if current values remain equal. Support-building/census dependency ordering is T02 before T04, not circular.

Net cost = setup + complete-dependency recorder/bounds + paired/absolute/affine construction and conversion + scheduler + exact survivors/guards/winner + invalidation/restoration + final oracle + optional feature/training/communication. Failure/timeout costs remain in totals. Model-relative exactness never means globally optimal PPA, foundry signoff or arbitrary MCMM correctness. Resources, sample sizes, precision-adapter proof and implementation pins remain unresolved as task-list prerequisites.

## Local verification performed / deferred

Executed only own A01, source retrieval/hash inspection, output JSON/hash checks and trusted release freeze/verify. No EDA build/flow/training/downloaded code/paid API/GPU/remote experiment. Full `project.py validate` is not meaningful on this standalone role packet and was not used as pretext to inspect checkout; coordinator runs full-repository validation at publication. Freeze/JSON validity is mechanical, not independent scientific verification.
