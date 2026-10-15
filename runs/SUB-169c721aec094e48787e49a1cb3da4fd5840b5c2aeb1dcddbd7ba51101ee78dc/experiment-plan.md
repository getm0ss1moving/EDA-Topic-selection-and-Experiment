# Experiment plan — hypotheses, oracles and conditional execution

## Scientific question and comparison

Test whether compressing candidate membership through complete timing-state equivalence classes improves total alternative-scoring latency beyond transactional lazy timing with complete-key caching/output interning and task clustering (B+). H0 is equivalent execution or extra mask cost. Candidate generation, batch composition, selected edit sequence, memory/cores, library/parasitic/corner, reporting and correctness semantics must match. Fresh scalar is the oracle, not the sole performance baseline. Fixed-lane vector execution isolates ordinary batching. Scope and invariants are fixed in proposal.md and direction-control.json.

No predictive model is required by the selected mechanism. Training cost is zero in this plan. Agent and unified-prediction candidates are documented alternatives, not implementations being silently added. If later prediction is introduced, its data/label/training/inference costs, family contamination, deployable-input audit and separate approximate/coverage contract require a new reviewed amendment preserving the anchor. Mere confidence gating is not a contribution.

## Endpoints and attribution

Primary: total wall time to obtain the identical requested per-candidate endpoint setup-slack outputs and deterministic ECO choice from the same base-ready batch. Report startup/build and reuse horizons separately. Charge all invalidation, load updates, mask refinement, keys/comparisons, queueing, copying, cache misses/hits/eviction, output expansion, failures and fresh reference replays; account for final context/commit guards. CPU time and RSS are co-primary cost diagnostics. Correctness requires byte-equivalent supported results and no missed violating endpoint; 5ps is a diagnostic only. WNS/TNS equality alone is insufficient. Final optimization quality, accepted moves, area/hold/legality and actual closure effort are downstream checks; no PPA improvement is forecast merely from scoring faster.

The 20% time reduction in P-BRIEF is provisional. EXP-005 freezes a practically meaningful threshold and sample size using baseline-only observations and documented integration cost before seeing candidate data. Five paired run-order seeds across >=3 independent families is an initial screening requirement, not a power calculation. Use family-level uncertainty, all failed cases and negative diverse-state cases; do not select designs based on method gain. Public benchmarks may have pretraining exposure if a learned/LLM method is later used. Keep variants of AES, JPEG, Ariane or other base designs together. No MCMM/PDK transfer conclusion from a typical-corner fixture.

## Conditional implementation and pins

Inspected OpenSTA 49b86c95b31c53ba9096b91ef384ae5406b3107c and OpenROAD 8da6ac250b0349c346d1abed7c2c43107f4ff6f7 are candidate source pins only. They are not a verified compatible build, not the historical container pin, and not a validated adapter. EXP-002 locks recursive dependencies and binaries. EXP-003 audits complete read sets, FP environment and exact scalar ordering. Legal replacements need unchanged topology/function/footprint and candidate pin caps; unsupported features must trigger scalar replay. The proof in proposal.md is conditional, not a completed program verification.

No new physical run or training resources are allocated by this batch. Proposed first conditional pilot: <=2 CPUh aggregate including checks/builds, 2 CPUs, 4GiB RSS, 600s per process, no GPU, remote host or paid API. It is executable only after all tasklist gates/actual owner acceptance and matching scientific consents. Representative/full-context evaluation may exceed that cap; then request a separate allocation and report that it remains undone. Restricted coverage and engineering demand are acceptance issues even if the abstract proof passes.

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
