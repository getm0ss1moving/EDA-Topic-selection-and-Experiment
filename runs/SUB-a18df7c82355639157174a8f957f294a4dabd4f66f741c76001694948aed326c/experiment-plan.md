# Experiment plan — hypotheses, oracles and conditional execution

## R2 control: current scientific position

R1's generic mask-scheduler advantage is superseded by CLM-609's B++ reduction. Current question is whether a specific, caller-required engine-adapter capability or cost/reliability delta survives **that same adapted composition**. No such witness is supplied, so implementation and performance tasks remain inactive. tasklist.md is the live R2 dependency list; its source-only EXP-000/001/006A observations are completed, EXP-000R/001R are explicit witness gates. R1's proposed 2 CPUh pilot below is retained for history only and is unallocated/inactive; it cannot be inferred as an executable request.

Actual queries and validation must be separated. S22/S23 prepared sizing candidates consume local `arrival_impr`; S24/S25 measured alternatives consume one driver arrival. This is not evidence for changing the frozen full-vector contract. Full vectors can serve as offline oracle, but synthetic expansion cannot create a deployment benefit. Any final study must report deployment-required scoring, necessary full-context guard, and research-only reference validation separately, with their summed budget visible. Unknown guard semantics block deployment readiness.

The strengthened comparator B++ implements finite conditional contexts, full-state caching, sparse base overlays, joins, output interning and bounded replay with the same bitsets/task order/cache policy. EXP-004 grants it every identical optimization; comparing only against per-lane B+ is insufficient. The equation `T_new/T_B++ = 1-f*r+h` is an accounting identity under the declared removable-work partition. No f/r/h is measured. No numerical gain or success forecast is offered.

## Scientific question and comparison (R1 conditional protocol; B++ now mandatory)

Historical R1 question: whether compressed candidate membership lowers scoring latency against B+. R2 withdraws that generic distinction unless a caller-required adapter delta also beats faithful B++ lifted contexts with identical masks/cache/replay. H0 is equivalent execution or extra mask cost. Candidate generation, batch composition, selected edit sequence, memory/cores, library/parasitic/corner, reporting and correctness semantics must match. Fresh scalar is the oracle, not the sole performance baseline. Fixed-lane vector execution isolates ordinary batching. Scope and invariants are fixed in proposal.md and direction-control.json.

No predictive model is required by the selected mechanism. Training cost is zero in this plan. Agent and unified-prediction candidates are documented alternatives, not implementations being silently added. If later prediction is introduced, its data/label/training/inference costs, family contamination, deployable-input audit and separate approximate/coverage contract require a new reviewed amendment preserving the anchor. Mere confidence gating is not a contribution.

## Endpoints and attribution

Primary: total wall time to obtain the identical requested per-candidate endpoint setup-slack outputs and deterministic ECO choice from the same base-ready batch. Report startup/build and reuse horizons separately. Charge all invalidation, load updates, mask refinement, keys/comparisons, queueing, copying, cache misses/hits/eviction, output expansion, failures and fresh reference replays; account for final context/commit guards. CPU time and RSS are co-primary cost diagnostics. Correctness requires byte-equivalent supported results and no missed violating endpoint; 5ps is a diagnostic only. WNS/TNS equality alone is insufficient. Final optimization quality, accepted moves, area/hold/legality and actual closure effort are downstream checks; no PPA improvement is forecast merely from scoring faster.

The 20% time reduction in P-BRIEF is provisional. EXP-005 freezes a practically meaningful threshold and sample size using baseline-only observations and documented integration cost before seeing candidate data. Five paired run-order seeds across >=3 independent families is an initial screening requirement, not a power calculation. Use family-level uncertainty, all failed cases and negative diverse-state cases; do not select designs based on method gain. Public benchmarks may have pretraining exposure if a learned/LLM method is later used. Keep variants of AES, JPEG, Ariane or other base designs together. No MCMM/PDK transfer conclusion from a typical-corner fixture.

## Conditional implementation and pins

Inspected OpenSTA 49b86c95b31c53ba9096b91ef384ae5406b3107c and OpenROAD 8da6ac250b0349c346d1abed7c2c43107f4ff6f7 are candidate source pins only. They are not a verified compatible build, not the historical container pin, and not a validated adapter. EXP-002 locks recursive dependencies and binaries. EXP-003 audits complete read sets, FP environment and exact scalar ordering. Legal replacements need unchanged topology/function/footprint and candidate pin caps; unsupported features must trigger scalar replay. The proof in proposal.md is conditional, not a completed program verification.

No new physical run or training resources are allocated by this batch. Historical inactive R1 pilot estimate: <=2 CPUh aggregate including checks/builds, 2 CPUs, 4GiB RSS, 600s per process, no GPU, remote host or paid API. R2 withdraws any live request pending source witnesses; actual allocation, owner acceptance and matching consents would still be required. Representative/full-context evaluation may exceed that cap; then request a separate allocation and report that it remains undone. Restricted coverage and engineering demand are acceptance issues even if the abstract proof passes.

## Completed analytical sanity check: exact script and outcome

Command: `python3 toy_check.py` after copying the following self-contained source into an external scratch directory. This job executed the identical source at `/tmp/eda0006-p05-r1-research/toy_check.py`; this path is ephemeral and not a required experiment input. The embedded bytes are the portable artifact. Python 3 stdlib only. Runtime was below the shell tool's 0.1-second resolution; no meaningful performance timing was measured. Source reading/parsing is excluded from this script. It constructs 64 states and 12 transitions, not EDA designs.

```python
import json,struct

def bits(s):
    return struct.pack('>ddq',*s)

def step(s):
    a,x,t=s
    return (a+0.125*x,x*0.5+0.25,t)

def run(groups,depth=12,n=64):
    values=[(float(i%groups),float(i%groups+1),0) for i in range(n)]
    plain=values[:];cached=values[:];classes={}; cache={}
    for i,x in enumerate(values):
        k=bits(x)
        if k not in classes: classes[k]=[0,x]
        classes[k][0]|=1<<i
    misses=lookups=transitions=0
    for level in range(depth):
        plain=[step(x) for x in plain]
        nxt=[]
        for x in cached:
            lookups+=1;k=(level,bits(x))
            if k not in cache:cache[k]=step(x);misses+=1
            nxt.append(cache[k])
        cached=nxt;out={}
        for mask,x in classes.values():
            transitions+=1;y=step(x);k=bits(y)
            if k not in out:out[k]=[0,y]
            out[k][0]|=mask
        classes=out
    reconstructed=[None]*n
    for mask,x in classes.values():
        for i in range(n):
            if mask&(1<<i):reconstructed[i]=x
    assert list(map(bits,plain))==list(map(bits,cached))==list(map(bits,reconstructed))
    return dict(lanes=n,depth=depth,groups=groups,plain_evals=n*depth,cache_lookups=lookups,cache_misses=misses,quotient_transitions=transitions,initial_lane_insertions=n,final_lane_materializations=n,final_groups=len(classes))

# Reconvergent partitions: two orthogonal 8-way lane partitions.
a=[sum(1<<i for i in range(64) if i//8==j) for j in range(8)]
b=[sum(1<<i for i in range(64) if i%8==j) for j in range(8)]
assert sum(bool(x&y) for x in a for y in b)==64
assert (1.0,2.0,0)!=(1.0,2.0,1)
assert 0.0==-0.0 and struct.pack('>d',0.0)!=struct.pack('>d',-0.0)
print(json.dumps({'scope':'analytical toy; not EDA timing or performance benchmark','cases':[run(4),run(64)],'orthogonal_join':{'mask_intersections':64,'nonempty_classes':64},'tag_collision_rejected':True,'signed_zero_byte_distinction':True},indent=2))
```

Observed counts: four states → 768 uncached evaluations, 768 cached lookups, 48 cache misses, 48 representative transitions; initial insertions=64, final materializations=64. Sixty-four states → 768 lookups, 768 misses, 768 representative transitions plus mask overhead. An orthogonal 8×8 join has 64 attempted and 64 nonempty intersections. All reconstructed output bytes match the scalar synthetic reference; distinct tags and signed-zero bytes remain distinct.

These counts omit real key widths, word-level bitset cost, memory locality, incremental early stopping and interconnect kernels. They establish only that the specified representations behave as stated on this tiny example. They do not establish net time savings, novelty, actual context repetition, sound Liberty/OpenSTA behavior or industry utility. The strongest cached baseline already matches numerical evaluation count; this adverse result is central to EXP-000. Orthogonal partitions and high diversity are mandatory failure cases, not optional robustness embellishments.

## Final-hash and exposure controls

EXP-004 creates final code; EXP-006 validates its resulting binary/config/generator hashes, and EXP-007 consumes those exact hashes. No substantive edit occurs between validation and measurement without affected-suite revalidation. Baseline-only EXP-005 can run independently of candidate code, and its calibration exposure log must precede candidate/ablation results. Rebuilds, changed locks, aborts and invalidated results stay in the cost/event ledger. After any candidate-result exposure, amendments are exploratory until a new held-out preregistration. Independent reproduction is pending, not claimed by local self-checks.

## Completed R2 analytical reduction and boundary check (CLM-609)

Command actually run: `python3 /tmp/eda0006-p-r2-qq7eiws0/check_r2.py`. Python stdlib only, eight synthetic byte records, one synthetic join and an orthogonal partition case. Runtime below the shell's 0.1-second reporting resolution; this is not an EDA or timing benchmark. Sources were read but downloaded code was never executed. The following is the complete self-authored check; it tests the specification on finite fixtures and does not prove engine read sets.

```python
import json, struct
from itertools import product
N=8; U=(1<<N)-1

def val(x, tag=0): return struct.pack('>dq', x, tag)
def decode(b): return struct.unpack('>dq', b)
def part(xs):
    p={}
    for i,x in enumerate(xs): p[x]=p.get(x,0)|(1<<i)
    return p

def dense(p):
    xs=[None]*N; cover=0
    for x,m in p.items():
        assert m and not cover&m
        cover|=m
        for c in range(N):
            if m>>c&1: xs[c]=x
    assert cover==U
    return xs

# All records are synthetic; tag is observable, bytes distinguish signed zero.
a=[val(0)]*N; b=[val(0)]*N
a[1]=val(0);a[2]=val(0,1);a[3]=val(-0.0);a[4]=val(2)
b[1]=val(3);b[2]=val(3);b[5]=val(1);b[6]=val(2)
da=sum(1<<i for i in [1,2,3,4]);db=sum(1<<i for i in [1,2,5,6])

def join(x,y):
    ax,at=decode(x);by,bt=decode(y)
    return val(ax+by, at*10+bt)

def lift(left,right,active):
    # Prior composition: conditional values, intersections, full-record cache.
    out={};cache={}; ctr={'intersections':0,'nonempty':0,'lookups':0,'kernels':0,'unions':0}
    for x,mx in left.items():
        for y,my in right.items():
            ctr['intersections']+=1;m=mx&my&active
            if not m: continue
            ctr['nonempty']+=1;ctr['lookups']+=1;k=(x,y)
            if k not in cache: cache[k]=join(x,y);ctr['kernels']+=1
            z=cache[k];out[z]=out.get(z,0)|m;ctr['unions']+=1
    return out,ctr

def quotient(left,right,active):
    # Proposal: refine the same partitions, then representative scalar evaluation.
    refined=[]; ctr={'intersections':0,'nonempty':0,'lookups':0,'kernels':0,'unions':0}
    for (x,mx),(y,my) in product(left.items(),right.items()):
        ctr['intersections']+=1;m=mx&my&active
        if m: refined.append((m,x,y));ctr['nonempty']+=1
    out={};cache={}
    for m,x,y in refined:
        ctr['lookups']+=1;k=(x,y)
        if k not in cache: cache[k]=join(x,y);ctr['kernels']+=1
        z=cache[k];out[z]=out.get(z,0)|m;ctr['unions']+=1
    return out,ctr

active=da|db
lp,lc=lift(part(a),part(b),active);qp,qc=quotient(part(a),part(b),active)
# Dirty and equal-base is computed, then safely coalesces with inherited base.
base=join(val(0),val(0));untouched=U^active
for p in [lp,qp]: p[base]=p.get(base,0)|untouched
reference=[join(x,y) for x,y in zip(a,b)]
assert dense(lp)==dense(qp)==reference and lc==qc
assert a[1]==a[0] and da&(1<<1) and not da&1
assert a[0]!=a[2] and a[0]!=a[3]
# Distinct dirty input can also evaluate to exact base bytes.
x,y=val(1),val(-1);assert join(x,y)==base
# Orthogonal predecessor contexts force all 4*2 intersections nonempty.
ox=part([val(i//2) for i in range(N)]);oy=part([val(i%2) for i in range(N)])
ol,oc=lift(ox,oy,U);oq,oqc=quotient(ox,oy,U)
assert dense(ol)==dense(oq) and oc==oqc and oc['nonempty']==8
# Simulated cap event after partial work: revoke fallback lanes' partial state,
# then replay each ORIGINAL candidate from its initial a,b values exactly once.
fallback=(1<<2)|(1<<5);partial=dense(lp);replay_count=0
for c in range(N):
    if fallback>>c&1:
        partial[c]=None
        partial[c]=join(a[c],b[c]);replay_count+=1
assert partial==reference and replay_count==2
assert len(partial)==N
print(json.dumps({'scope':'synthetic byte-record accounting, not EDA benchmark',
'primary_ledger':lc,'orthogonal_ledger':oc,'fallback_original_replays':replay_count,
'checks':['partition_cover','inherited_vs_dirty_equal_base','dirty_output_equal_base','tags','signed_zero','reconvergent_join','partial_fallback_reset'],
'outputs_match':True,'same_abstract_ledger':True},indent=2))
```

Observed result: both implementations match the dense scalar byte reference. Both ledgers count 16 attempted intersections, six nonempty active classes, six cache lookups, six scalar calls and six output unions. The orthogonal fixture has eight of each; fallback replay count is two, from original inputs. All seven named boundary checks pass. Counted intersections bundle the AND operations shown in the script; they are abstract events, not CPU instructions, bitset-word timing, memory traffic or wall-time savings. Both sides also share input partition construction and output materialization; those omitted common costs cannot justify a performance claim. `quotient` even materializes an intermediate list while `lift` streams; this intentional simple implementation does not support any constant-factor advantage. The negative conclusion is that equivalent event counts are constructible, not that production implementations must have identical timing.

For cap recovery, the test clears both partially computed fallback values and recomputes original inputs exactly once. Engine implementation still needs to remove fallback masks from ALL intermediate overlays, revoke partial reports/cached context if invalid, restore base/context and replay full supported operations. The toy does not exercise OpenDB journaling, Liberty, setup constraints, FP environment changes, memory pressure, races or actual cap enforcement. These remain EXP-003/006 obligations rather than observed correctness.
