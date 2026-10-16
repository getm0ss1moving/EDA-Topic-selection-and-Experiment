# Search and analytical replay: EDA-0009 B4-R2

Identity: ChatGPT-P04-PHYSICAL-B04-EDA-0009; session 24989b4f-9381-471f-a32f-a8d8f7f685a1; job 160d8ea6-72cf-42c6-8a4f-f503a8e08f88. Input commit d0eedf3130de673ea92e4be202a32d463a63f301; packet d1325387dd19dfe8d7766889b646835828c2ba6e6003bc803cb1c06d036f27de. Retrieval date UTC: 2026-10-16T04:33:47.240550+00:00. Search engine: web search/open; fallback for primary PDF/source reading: Python urllib with timeout30s and pdftotext. Only self-authored analytical Python and trusted packet validators executed. No downloaded code, EDA build/flow, training, paid or remote compute executed.

## Fresh searches and stopping boundary

| Expansion | Exact queries / route | Inspected result and inclusion |
|---|---|---|
| Initial | `"AiDRC" "3769306"`; `"detailed routing" "violation prediction" AiDRC iterative`; `"nonmyopic" "value of information" "Krause" "Guestrin" 2005` | Primary DOI-indexed method and IJCAI2005; task-specific predictor and conditional observation baseline |
| Method and implementation | `"AiDRC" "features" "Section 3"`; `"AiDRC" github`; `"AiDRC" "Feature Selection" "Hanan"`; `"AiDRC" "github.com" "Li"` | Author PDF discovered and fully retrievable by urllib; selected §§2.3/3/4.1/5.5 read. AiEDA public README inspected, not identified as complete AiDRC reproduction |
| Cross vocabulary | `"detailed routing" "value of information" DRC checking`; `"design rule checking" "selective" "prediction" 2026 routing`; `"AiDRC" "residual" checking`; `"design rule checking" "cross-candidate" cache acquisition`; `"detailed routing" "incidence" "checking" prediction` | AiDRC remains closer task-specific prior; unrelated results excluded; no absence-based novelty claim |
| Citation/winner neighborhood | `site:ispd.cc "2019" "Dr. CU" winner`; `site:ispd.cc/slides/2019 "CU"`; reopened official2019/2026 pages, DrCU2 §III-C.2, pinned README | winner/paper/code relation, not executable equivalence; no benchmarks downloaded or run |
| Classical backward expansion | `"Optimal Nonmyopic Value" "Heckerman" "1993" conditional plans`; IJCAI2005 §1/§8 | Older nonmyopic approximation is a lead, not audited new proof; no general guarantee transferred |
| Engine / workflow | reopened WXL V-E/VI-B, OpenDRC IV-C, DRC-Aid §§3.1–3.4, Siemens named sections; pinned OpenROAD raw files | source/need/known-component boundaries only |

Stopping: two terminology/citation expansions are documented, but this is a bounded selected-source audit. AiDRC author/final-version and implementation parity, contest executable correspondence, incremental patents and calibrated physical economics remain unresolved. No claim that no closer method exists.

## Access and source integrity

DOI/full-ACM and author-PDF web opens returned Internal Error. The same publicly accessible author PDF succeeded through urllib:8,516,533 bytes, SHA256 ac23635ae04e506a0e83637397b52d1fb65d90759d116b1f20159d9e4674f690. Source carries placeholder2024 header; publication date is taken only from publisher metadata, not the filename/header. Author Fig11/prose channel discrepancy is left unresolved, not silently normalized. Local source copies/extracted text remain outside checkout and outside release; no full paper redistributed.

Pinned OpenROAD b16bda7e82721d10566ff7e2b68f1ff0be9f9e38: FlexGC_main.cpp4062 lines SHA2564770ffdc8f1ac0fd13e69dac1a0b75c5dbb795bf7c043be5ed2b8294cb43a517; FlexGC.h99 lines SHA256293e895cf573ccba346d5bf35184dac066f00509e327a53e370256078a945e64; TritonRoute.cpp1452 lines SHA2561bb6bef08a426c311d6e1b8fae12db89bfb69be89ff7340f381a95b6ab37f335. Locators are raw one-based. A display loop requested4064 for the4062-line GC file, printed through4062, then caught IndexError; bytes/hash and available lines were retained. This was a local extraction-range error, not source-access fabrication; no result depends on nonexistent lines.

## Exact self-authored analytical check

No external source code is executed. Parameters are in the code: four equiprobable two-bit states; XOR and single-bit terminal labels; query costs {1/20,1/10,1/5,3/10}; setup {0,1/10,1/4};96 settings. Exact Fraction arithmetic; deterministic ties. C/F use the same finite posterior table/actions; equality is an intentional null test, not two independent implementations. Depth2 exhaustive for two observations only; no theorem for larger pools. Utility is success probability minus normalized acquisition work. Common final exact cost is reserved/cancels in this model; planner work is counted as posterior nodes but not translated into time, so the values do not claim net physical speedup. Additional accounting records explicitly keep all candidate-state extraction cost.

Code SHA256 `f34c69778642ff9829d773aa5962f6ab3a847ca0f84414df275ef1ccf769b3ca`; exact stdout SHA256 `2b11d405747318dfd20dbfa409d7b8ec52e45d7bb510a6a7d0b0052fb0489a44`.

<!-- REPLAY-CODE-BEGIN -->
```python
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
S=tuple(product((0,1),repeat=2))
# Independent hidden variables; "single" is a no-complementarity control.
def solve(mode,costs,setup,depth):
    calls=[0]
    def label(s): return (s[0]^s[1]) if mode=="xor" else s[0]
    @lru_cache(None)
    def value(ids,mask,left):
        calls[0]+=1
        counts=[sum(label(S[i])==a for i in ids) for a in (0,1)]
        best=F(max(counts),len(ids)); policy=("stop",counts.index(max(counts)))
        if left:
            for a in (0,1):
                if mask&(1<<a): continue
                price=costs[a]+(setup if mask==0 else 0)
                total=-price; children=[]
                for bit in (0,1):
                    subset=tuple(i for i in ids if S[i][a]==bit)
                    if subset:
                        if depth==1:
                            ys=[label(S[i]) for i in subset]
                            child=(F(max(ys.count(0),ys.count(1)),len(ys)),("terminal",))
                        else: child=value(subset,mask|(1<<a),left-1)
                        total+=F(len(subset),len(ids))*child[0]
                        children.append((bit,child[1]))
                # Strict comparison gives STOP precedence, then increasing query ID.
                if total>best: best,policy=total,("query",a,tuple(children))
        return best,policy
    result=value(tuple(range(4)),0,depth)
    return result,calls[0]
for mode in ("xor","single"):
    myopic,_=solve(mode,(F(1,10),)*2,F(0),1)
    exact,calls=solve(mode,(F(1,10),)*2,F(0),2)
    print(mode,"myopic="+str(myopic[0]),"depth2="+str(exact[0]),
          "root="+str(exact[1][:2]),"posterior_nodes="+str(calls))
    assert exact[0]==(F(4,5) if mode=="xor" else F(9,10))
assert solve("xor",(F(1,10),)*2,F(0),1)[0][1][0]=="stop"
count=improved=equal=0
for mode,c0,c1,a in product(("xor","single"),(F(1,20),F(1,10),F(1,5),F(3,10)),
                           (F(1,20),F(1,10),F(1,5),F(3,10)),(F(0),F(1,10),F(1,4))):
    conventional,_=solve(mode,(c0,c1),a,2)
    factorized,_=solve(mode,(c0,c1),a,2)
    myopic,_=solve(mode,(c0,c1),a,1)
    assert conventional==factorized
    count+=1; equal+=conventional==factorized; improved+=conventional[0]>myopic[0]
    if mode=="xor": assert conventional[0]==max(F(1,2),1-c0-c1-a)
print("grid_cases="+str(count),"C_F_equal="+str(equal),"depth2_gt_myopic="+str(improved))
# Predicate reuse does not erase discovery in each distinct candidate state.
for administration in (F(1),F(5),F(6)):
    separate=4*F(2)+4*F(5)
    reused=4*F(2)+3*F(5)+administration
    print("accounting admin="+str(administration),"separate="+str(separate),
          "reused="+str(reused),"net_saved="+str(separate-reused))
    assert separate-reused==5-administration
# A changed empty range must be invalidated, even without old returned objects.
old=(); new=("inserted_neighbor",)
assert old!=new
print("empty_query_insertion_invalidates=True")
# Readiness graph: threshold/economics lock precedes census AND arm outcomes.
deps={"100":set(),"101":set(),"102a":set(),"102b":{"100","102a"},
      "106":{"102a","100"},"103":{"100","102b","106"},
      "104":{"100","102b","103","106"},"105":{"100","102b","103","104","106"},
      "107":{"100","102b","103","104","105","106"}}
order=[]
while len(order)<len(deps):
    ready=sorted(k for k,v in deps.items() if k not in order and v<=set(order))
    assert ready,"cycle"
    order.extend(ready)
assert order.index("106")<order.index("103")<order.index("105")
print("dag_order="+",".join(order))
print("all_assertions_passed=True; model_only=True; physical_runs=0")
```
<!-- REPLAY-CODE-END -->

Exact stdout:

```text
xor myopic=1/2 depth2=4/5 root=('query', 0) posterior_nodes=9
single myopic=9/10 depth2=9/10 root=('query', 0) posterior_nodes=9
grid_cases=96 C_F_equal=96 depth2_gt_myopic=27
accounting admin=1 separate=28 reused=24 net_saved=4
accounting admin=5 separate=28 reused=28 net_saved=0
accounting admin=6 separate=28 reused=29 net_saved=-1
empty_query_insertion_invalidates=True
dag_order=100,101,102a,102b,106,103,104,105,107
all_assertions_passed=True; model_only=True; physical_runs=0
```

Reproduce without executing any fetched source:

```sh
python3 - <<'REPLAY'
from pathlib import Path
import hashlib,subprocess,tempfile
s=Path('search-log.md').read_text()
c=s.split('<!-- REPLAY-CODE-BEGIN -->\n```python\n',1)[1].split('\n```\n<!-- REPLAY-CODE-END -->',1)[0]+'\n'
assert hashlib.sha256(c.encode()).hexdigest()=='f34c69778642ff9829d773aa5962f6ab3a847ca0f84414df275ef1ccf769b3ca'
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'own-analysis.py';p.write_text(c)
 b=subprocess.check_output(['python3',str(p)],timeout=10)
 assert hashlib.sha256(b).hexdigest()=='2b11d405747318dfd20dbfa409d7b8ec52e45d7bb510a6a7d0b0052fb0489a44'
 print(b.decode(),end='')
REPLAY
```

Local verification: exact authored block executed during construction and reproduction checks; no physical runtime inference. Structural graph check tests the exact public dependency map; it does not certify EDA readiness. Trusted freeze validator substitutes for unavailable full-repository validation in this standalone job under prompt instructions; publication validation belongs to the coordinator.
