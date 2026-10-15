# Cycle-3 reproducible source/analytical audit

Actor ChatGPT-P04-PHYSICAL-EDA-0005, session07ec73dc-1bf7-4f5c-999f-b589460c1e5e. Input commit f68c1492c05be3fac5622deac4bb479eabf957de; packet b9b3d8bc704ac6b8b70e549417c704d5f4a0f3d966bdfe6c33bc9af9790bdef6. Exact cycle3 outputs are this job's release/ files and its immutable submissions/SUB-... directory; result.json is transport status. This is the public run record within the allowed dossier; coordinator stores it under runs/. No repository-wide validation is claimed.

## Input/provenance checks

All31 policy manifest entries rehashed,0 mismatches. Own previous12 files and released shared manifests (current verifier3,current challenger7, predecessor P12/C7/V3) rehashed with0 mismatches. Only assigned proposer/common policy and explicit released science were read. An initial checkout filename search and common docs/proposer-harness reads occurred before reading the job-local restriction; no foreign harness/science/private notes/transcripts/sessions/memory read. Thereafter packet/external-only. Procedural OS isolation, not adversarial confinement. No role messages sent, no scientific subagents. No inherited approval. Current verifier/challenger release IDs and exact reviewed proposer appear in responses.md.

## Searches on2026-10-15, web search/open, no date filter

| Expansion | Exact query / action | Included result / exclusion / access |
|---|---|---|
| A | `"HyPAS" "placement" OpenROAD`; `"HyPAS" "Hybrid Optimization" paper`; `"HyPAS" "github" "Liu"` | Official DAC program abstract reopened. CEDAR institutional abstract appears in search index; direct reader error. Abstract only, no numeric transfer. No usable method code established. |
| A | `"hold" "repair" "placement" "site" OpenROAD RepairHold`; `"hold repair" "joint" "placement" optimization sites`; `"hold repair" "candidate" "sites" placement EDA` | Pinned upstream RepairHold/Resizer chain inspected. Broad queries mostly generic or irrelevant; no source-backed positive delta. Unofficial/manual mirrors and unrelated medical/road repair hits excluded. |
| B | `"HyPAS" "pdf"`; `"HyPAS" "buffer" "placement" github`; `"HyPAS: A Hybrid Optimization Framework" filetype:pdf`; `"Fangzhou Liu" "HyPAS" code` | Found Wuqian Tang author page and first-author page. Opened author publication entry, followed actual PDF/Slides links; full7-page paper succeeded. Other HyPAS printer-platform hits excluded. Author page future-dated news not used. No complete original winner implementation established. |
| B | `site:github.com/The-OpenROAD-Project/OpenROAD "legalCellPos" "Point"` plus upstream Git tree API at immutable commit | Git tree identified src/dpl/src/Place.cpp. Opendp.cpp initially inspected but has no target function; Place.cpp contains legalCellPos1348-1373. No code executed. |
| Access repair | Tried `https://www.cse.cuhk.edu.hk/~byu/pubs.html` (HTTP404); `/publications/` reader failed; correct `/publications.html` opened | Correct author publications page and first-author page supplied metadata; full HyPAS fetched through coauthor PDF link instead. Broken guessed path is not novelty evidence. |

Two expansions found closer accessible evidence; they were NOT two empty novelty-search expansions. Stop due bounded round scope after full-method repair and concrete implementation contract, with no identified useful delta. Original contest-winning code, S12 full Algorithm3, exact S11 article and exhaustive forward citations remain incomplete. This is neither exhaustive novelty search nor universal duplication proof.

## Retrieval / source scope

Direct ordinary HTTPS via urllib.request,25s per source timeout; source/PDF bytes held in private external scratch only. Selected files: RepairHold.cc30075bytes SHA2565e5fd39774743e612f2337ca6e86af352bf50b07ce30870ba832b33eeee77f9f; Resizer.cc253499bytes SHA256ff3adf14a5f8f9059a293b7fbfbf39ce4138f008294c43fd86d6cc46c6024b85; Place.cpp44726bytes SHA256b8eaf11288695842a41ed9ca57ffc39a6d8476410dce81b5459fe52619659542; HyPAS1977926bytes SHA256d843ea04b2746e449c7ded65ab06bb5f5d9d11f969251962c6feec7bdb930ca0. Author HTML167967bytes SHA25660b74138e142f1336c9663b44b56641883e3e07565dbd077ff103b7fecfa7012. All exact URLs, locators and access qualifications in sources.json. Auxiliary pinned rsz README and Opendp.cpp read; API tree discovery read. Full related implementation not built/audited. Slides11-page PDF opened, but no slide-specific claim is relied on. A PDFp5 screenshot request was made; no visual-QA claim is relied on.

Representative source-read commands (source reading/text extraction only):

```python
from urllib.request import urlopen
from hashlib import sha256
commit = "8da6ac250b0349c346d1abed7c2c43107f4ff6f7"
base = f"https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD/{commit}/"
paths = ["src/rsz/src/RepairHold.cc", "src/rsz/src/Resizer.cc", "src/dpl/src/Place.cpp"]
for relative in paths:
    body = urlopen(base + relative, timeout=25).read()
    print(relative, len(body), sha256(body).hexdigest())
pdf = urlopen("https://wuqian-tang.github.io/files/papers/2026-dac-hypas.pdf", timeout=25).read()
print("HyPAS", len(pdf), sha256(pdf).hexdigest())
```

Actual text extraction: `/opt/homebrew/bin/pdftotext -layout <private-scratch>/hypas <private-scratch>/hypas.txt`; shell exit0,0.050s wall reported by command tool. `rg -n -i 'hold|clock|sign.off|3.2|3.7|4 Experimental|7200|training' <private-scratch>/hypas.txt` guided location reading; keyword absence is not proof of absent capability. Methods and evaluation were read at the explicit sections in S29. A source-line print briefly exceeded Place.cpp length and raised IndexError after printing its end; no scientific inference relies on that printing error.

## Cost and checks

No new EDA/full-flow/tool build/training/GPU/remote-host/paid-API calls. Costs were public source network requests, text extraction, JSON/hash checks and dossier writing on the existing desktop entitlement. Network latency is not an EDA runtime measurement. No new synthetic experiment was needed: the prior analytical equality remains explicitly historical. C3-T01 is source analysis/derivation, not a production bug reproduction.

A first dossier-write attempt copied the prior immutable files with preserved read-only mode, then write failed with PermissionError before any revision was written. Only the new job's release copies were made user-writable; originals unchanged. The revised files were then written and validated. Do not treat the mechanical retry as scientific execution.

Validation: all own JSON parses; allowed12 filenames; unique source IDs and source/CSV membership match; original anchor is identical; both penalties0; null forecasts; no consent invented. Trusted standalone freeze/verify below is the actual local submission gate; full project validation/publication belongs to coordinator under this packet. No browsing of checkout to satisfy legacy validation.

---

## Preserved round-2 search record and actual analytical code (historical, not newly executed)

# EDA-0005 round-2 search and analytical log

Identity: ChatGPT-P04-PHYSICAL-EDA-0005 / 07ec73dc-1bf7-4f5c-999f-b589460c1e5e. Input commit f68c1492c05be3fac5622deac4bb479eabf957de, packet b9b3d8bc704ac6b8b70e549417c704d5f4a0f3d966bdfe6c33bc9af9790bdef6. Date: 2026-10-15 UTC retrieval day. Own scratch outside checkout: /tmp/eda0005-p04-r2-q1be270u. No foreign-private material or role messages. Initial access departure: read common checkout governance and performed filename-only instruction listing before job prompt; no private/scientific material read. Subsequent work job-local and accessible external only.

## Research operations, searches and actual access

| Expansion / query or URL | Engine / action | Result and use |
|---|---|---|
| Global Interconnect Optimization resource sharing; supplied author PDF | Web open plus ordinary Python urllib HTTPS | Read §§2,3.4-3.5/3.9. PDF 747737 bytes, SHA-256 0448d6ab7cc506b9e15c6cbd18012e9973425f4390f9923fadfa381a955edc42; download 4.064 s. S22 source status repaired. No benchmark/result copied. |
| Novel Multi-Corner Delay Padding decomposition; official ASP-DAC PDF | Web reader Internal Error; ordinary urllib HTTPS succeeded | 5079213 bytes, SHA-256 97132d937fcaa6d568d28d6f53a6b8294a0edacddab18c69d2e6040bf51190d1; download 11.807 s. pdftotext extracted 23 slides; diagrams 13/14 rendered using pdftoppm and visually read. S23 now full selected original. |
| Same title, author-associated markdown lead | Web/raw URL S25 | Discovery-only expansion; full official PDF supersedes it. Numerical/detail differences mean no use as primary method evidence. |
| hold placement resource sharing timing buffer | Web search | Mostly irrelevant/secondary sources excluded. Public S14 reopened and Figure-2 feedback incorporated. |
| Routing-Aware Incremental Timing-Driven Placement pdf | Web search; IEEE abstract plus institutional thesis | S27 author thesis retrieved by normal HTTPS after web-reader failure: 4629496 bytes, SHA-256 e3fded3251150e17d7aeb8e0c3ef2219db08f2b6d83e335d0a99d92d6670c6e7; download 7.021 s. Title page and specified Chapter-5 sections read. Exact S11 publication remains abstract-only; do not conflate. |
| Power-aware hold optimization ASIC physical synthesis pdf | Web search publisher preview S12 | Abstract/introduction and algorithm summary available; general disturbances confirmed. Full Algorithm 3 inaccessible. No numerical gain transferred. |
| ICCAD2025 placement winner buffering relocation; yichen_iccad25_contest.pdf | Web searches; ordinary HTTPS | Official problem/winner indices inspected. NVIDIA endpoint returned 131-byte Git LFS pointer, not a PDF: pointer SHA-256 44bd8eed0165b324b423061080c7bf4e5303a3ff3f7ac220425c0925716b85b5; object OID 68119d848eb046c1a8935736558f62217723191a85744587b9b6b12861bce7e2 size 153803. pdftotext failed as expected. Not full-method access. |
| IRISLab ISPD26 buffering sizing algorithm; 2026 official problems | Web search and official S19/S26 open | Winner names and current tracks confirmed, complete method not found in bounded inspection. Not novelty evidence. |

Two expansions found closer/accessible negative evidence, not two no-result expansions. Search stopped on this bounded turn after materially resolving source access and operational comparison. Remaining exact full algorithms/winner methods stay unresolved. Source reading incurs no new paid API/GPU/remote allocation. Downloaded public copyrighted papers are scratch-only, never released. No downloaded code executed. URLs are in sources.json.

## C-T01 runnable analytical specification (CLM-016)

Reproduce by saving this exact Python block as trace_check.py outside the checkout, then run `/usr/bin/time -p python3 trace_check.py`. Standard library only. This is a deterministic mock; GR/STA operation labels do not invoke any EDA executable. No script files can be added to the trusted proposer freeze allowlist, so the complete runnable program is embedded here.

```python
import itertools as it,json,hashlib,time,platform
start=time.perf_counter()
weights={'A':30,'B':25,'C':20}
actions=sorted([tuple(x) for k in (1,2) for x in it.combinations(weights,k)],key=lambda x:(-sum(weights[a] for a in x),x))
def table(x,case):
    sites={'A':'s1','B':'s3' if case=='nonconflict' else 's1','C':'s2'}
    opts=[(a,tuple([a]),tuple([sites[a]]),1,tuple(['split'] if case=='net_split' and a in 'AC' else [])) for a in x]
    if case=='shared' and 'A' in x and 'B' in x:
        opts.append(('AB',('A','B'),('s1',),1,()))
    return opts

def admissible(x,z):
    cover=set();sites=[];splits=[]
    for _,cov,occ,_,con in z: cover.update(cov);sites.extend(occ);splits.extend(con)
    return set(x)<=cover and len(set(sites))==len(sites) and len(set(splits))==len(splits)
def key(z): return (sum(o[3] for o in z),tuple(o[0] for o in z))
def select_c(x,o):
    valid=[]
    for bits in it.product((0,1),repeat=len(o)):
        z=tuple(v for v,b in zip(o,bits) if b)
        if admissible(x,z): valid.append(z)
    return min(valid,key=key) if valid else None

def select_b3(x,o):
    valid=[]
    for k in range(len(o)+1):
        for ids in it.combinations(range(len(o)),k):
            z=tuple(o[i] for i in ids)
            if admissible(x,z):valid.append(z)
    return sorted(valid,key=key)[0] if valid else None

def transcript(case,selector):
    trace=[];incumbent=();best=0
    def emit(op,x,**kw):trace.append(dict(op=op,x=''.join(x),**kw))
    for x in actions:
        emit('RESTORE',x);emit('MOVE_LEGALIZE',x);emit('GR_RC_MINMAX',x)
        o=table(x,case);emit('GENERATE_OPTIONS',x,options=[v[0] for v in o])
        z=selector(x,o);emit('SELECT_TABLE',x,selected=None if z is None else [v[0] for v in z])
        if z is None:emit('TABLE_REJECT',x);continue
        # This deterministic mock is NOT OpenROAD or a physical timing/route oracle.
        passed=not(case=='realization_failure' and x==('A','C'))
        emit('COMPOUND_REALIZE_GR_STA',x,passed=passed)
        value=sum(weights[a] for a in x)
        if passed and value>best:incumbent=x;best=value
        emit('INCUMBENT',incumbent,value=best)
    return trace,dict(x=''.join(incumbent),value=best)
results={};prefix_checks=0
for case in ['conflict','shared','nonconflict','realization_failure','net_split']:
    a,ia=transcript(case,select_c);b,ib=transcript(case,select_b3)
    assert a==b and ia==ib
    # Unit operation credits test every termination boundary; they are not seconds.
    for cap in range(len(a)+2):
        assert a[:cap]==b[:cap];prefix_checks+=1
    results[case]={'events':len(a),'candidate_move_calls':sum(v['op']=='MOVE_LEGALIZE' for v in a),'option_generation_calls':sum(v['op']=='GENERATE_OPTIONS' for v in a),'compound_realization_calls':sum(v['op']=='COMPOUND_REALIZE_GR_STA' for v in a),'incumbent':ia,'trace_sha256':hashlib.sha256(json.dumps(a,sort_keys=True).encode()).hexdigest()}
# Small independent Hall-condition check, not a physical feasibility test.
matrices=masks=assignments=0
for incidence in range(512):
    matrices+=1
    for mask in range(8):
        masks+=1;enabled=[i for i in range(3) if mask>>i&1];feasible=False
        for a in it.product(range(4),repeat=3):
            assignments+=1
            ok=all((a[i]!=0)==(i in enabled) for i in range(3))
            if ok:ok=all((incidence>>(3*i+a[i]-1))&1 for i in enabled)
            if ok:ok=len({a[i] for i in enabled})==len(enabled)
            feasible|=ok
        hall=True
        for k in range(1,len(enabled)+1):
            for sub in it.combinations(enabled,k):
                nbr={j for i in sub for j in range(3) if incidence>>(3*i+j)&1}
                hall&=len(nbr)>=len(sub)
        assert feasible==hall
summary={'kind':'synthetic_analytical_check_not_EDA','cases':results,'budget_prefix_comparisons':prefix_checks,'trace_mismatches':0,'matching_cases':masks,'incidence_matrices':matrices,'raw_assignment_predicate_checks':assignments,'hall_mismatches':0,'physical_tool_calls':0,'elapsed_seconds':round(time.perf_counter()-start,6),'python':platform.python_version()}
print(json.dumps(summary,indent=2))
print('CONFLICT_TRACE='+json.dumps(transcript('conflict',select_c)[0],sort_keys=True))
```

Observed output from the exact executed block (local analytical evidence, not EDA measurements):

```text
{
  "kind": "synthetic_analytical_check_not_EDA",
  "cases": {
    "conflict": {
      "events": 41,
      "candidate_move_calls": 6,
      "option_generation_calls": 6,
      "compound_realization_calls": 5,
      "incumbent": {
        "x": "AC",
        "value": 50
      },
      "trace_sha256": "098c19fee8088f9c76be2572621ac7ef2866d1c172f910c6ae3c849f9a7d988c"
    },
    "shared": {
      "events": 42,
      "candidate_move_calls": 6,
      "option_generation_calls": 6,
      "compound_realization_calls": 6,
      "incumbent": {
        "x": "AB",
        "value": 55
      },
      "trace_sha256": "f84d43762bc741ddbfe31b41d3b27aa33f65bacd1e126ca5dec3042d73220ca5"
    },
    "nonconflict": {
      "events": 42,
      "candidate_move_calls": 6,
      "option_generation_calls": 6,
      "compound_realization_calls": 6,
      "incumbent": {
        "x": "AB",
        "value": 55
      },
      "trace_sha256": "6a36444337e60625044685831ac46300fdd9abb6a798fe2811c7b930ab8642a8"
    },
    "realization_failure": {
      "events": 41,
      "candidate_move_calls": 6,
      "option_generation_calls": 6,
      "compound_realization_calls": 5,
      "incumbent": {
        "x": "BC",
        "value": 45
      },
      "trace_sha256": "228a13c8bf3326c40e441d58d4be040a9eb8e49805dbdfadf2382f80f9a839e7"
    },
    "net_split": {
      "events": 40,
      "candidate_move_calls": 6,
      "option_generation_calls": 6,
      "compound_realization_calls": 4,
      "incumbent": {
        "x": "BC",
        "value": 45
      },
      "trace_sha256": "96451bb82319a0edf13755d69bbb2d85b2b66c035eb5d2c0aaba3767cc5b47bf"
    }
  },
  "budget_prefix_comparisons": 216,
  "trace_mismatches": 0,
  "matching_cases": 4096,
  "incidence_matrices": 512,
  "raw_assignment_predicate_checks": 262144,
  "hall_mismatches": 0,
  "physical_tool_calls": 0,
  "elapsed_seconds": 0.09657,
  "python": "3.9.6"
}
CONFLICT_TRACE=[{"op": "RESTORE", "x": "AB"}, {"op": "MOVE_LEGALIZE", "x": "AB"}, {"op": "GR_RC_MINMAX", "x": "AB"}, {"op": "GENERATE_OPTIONS", "options": ["A", "B"], "x": "AB"}, {"op": "SELECT_TABLE", "selected": null, "x": "AB"}, {"op": "TABLE_REJECT", "x": "AB"}, {"op": "RESTORE", "x": "AC"}, {"op": "MOVE_LEGALIZE", "x": "AC"}, {"op": "GR_RC_MINMAX", "x": "AC"}, {"op": "GENERATE_OPTIONS", "options": ["A", "C"], "x": "AC"}, {"op": "SELECT_TABLE", "selected": ["A", "C"], "x": "AC"}, {"op": "COMPOUND_REALIZE_GR_STA", "passed": true, "x": "AC"}, {"op": "INCUMBENT", "value": 50, "x": "AC"}, {"op": "RESTORE", "x": "BC"}, {"op": "MOVE_LEGALIZE", "x": "BC"}, {"op": "GR_RC_MINMAX", "x": "BC"}, {"op": "GENERATE_OPTIONS", "options": ["B", "C"], "x": "BC"}, {"op": "SELECT_TABLE", "selected": ["B", "C"], "x": "BC"}, {"op": "COMPOUND_REALIZE_GR_STA", "passed": true, "x": "BC"}, {"op": "INCUMBENT", "value": 50, "x": "AC"}, {"op": "RESTORE", "x": "A"}, {"op": "MOVE_LEGALIZE", "x": "A"}, {"op": "GR_RC_MINMAX", "x": "A"}, {"op": "GENERATE_OPTIONS", "options": ["A"], "x": "A"}, {"op": "SELECT_TABLE", "selected": ["A"], "x": "A"}, {"op": "COMPOUND_REALIZE_GR_STA", "passed": true, "x": "A"}, {"op": "INCUMBENT", "value": 50, "x": "AC"}, {"op": "RESTORE", "x": "B"}, {"op": "MOVE_LEGALIZE", "x": "B"}, {"op": "GR_RC_MINMAX", "x": "B"}, {"op": "GENERATE_OPTIONS", "options": ["B"], "x": "B"}, {"op": "SELECT_TABLE", "selected": ["B"], "x": "B"}, {"op": "COMPOUND_REALIZE_GR_STA", "passed": true, "x": "B"}, {"op": "INCUMBENT", "value": 50, "x": "AC"}, {"op": "RESTORE", "x": "C"}, {"op": "MOVE_LEGALIZE", "x": "C"}, {"op": "GR_RC_MINMAX", "x": "C"}, {"op": "GENERATE_OPTIONS", "options": ["C"], "x": "C"}, {"op": "SELECT_TABLE", "selected": ["C"], "x": "C"}, {"op": "COMPOUND_REALIZE_GR_STA", "passed": true, "x": "C"}, {"op": "INCUMBENT", "value": 50, "x": "AC"}]
```

Process timing: real 0.13 s, user 0.11 s, system 0.01 s. No memory benchmark or general runtime prediction. The program's internal elapsed time is one noisy local measurement of this toy. Its trace proof covers the declared deterministic table model and every operation-prefix cutoff; actual nonlinear physical realizations, option completeness, engine tie behavior and floating-point semantics are not validated. Hall/brute force is an independent mathematical oracle for unit-demand/unit-site matching only. Five shared/net-split tests are declared in the code; they do not satisfy the future ten-case production suite in EXP-005.

## Frozen-input and local structural checks

All 31 policy checksums match. Own prior 12 files and all five released shared manifests (12/3/7 historical and 7/3 current files) match their own manifests. Only common policy, own harness and explicitly released scientific files read. All release JSON/CSV/source references and task-list hash are checked before trusted freeze; full-repository validation is coordinator publication duty under this standalone job, not a falsely claimed local pass. Workflow contains exact paths/identity for runs transport.

## Previous own released log (historical record, not new execution)

# Search, access and analytical execution log

## Identity and scope

Actor ChatGPT-P04-PHYSICAL-EDA-0005; session07ec73dc-1bf7-4f5c-999f-b589460c1e5e; input f68c1492c05be3fac5622deac4bb479eabf957de; packet b9b3d8bc704ac6b8b70e549417c704d5f4a0f3d966bdfe6c33bc9af9790bdef6. Search/retrieval date2026-10-15 UTC. Work concerns post-CTS physical placement decisions and downstream hold repair, not a new timing-analysis algorithm. Scientific artifacts are English. No scientific messages, additional agents, source checkout access, private sessions/memory, physical runs, training or paid providers were used.

## Search expansion log

Index: web search tool, no domain or recency filter unless the literal query specifies one. Search results were discovery leads; only inspected primary sources support claims. The following are literal queries, grouped in execution order; exact source versions/access/locators are in sources.json.

| Pass | Literal queries | Inspected result and decision |
|---|---|---|
| 1 orientation | `ChatEDA EDAid AgenticPD physical design agent paper github`; `placement ECO timing congestion joint moves routing resource counterfactual interaction graph physical design`; `unified prediction physical design timing congestion multi task prediction 2025 2026` | S01–S04 and resource sharing lead. Generic stage agents not a contribution. Questionable journals/unclear chronology are not used as evidence. |
| 2 predictor and classical neighborhood | `AiEDA unified graph learning physical design prediction timing congestion 2025 github`; `routing-aware incremental timing-driven placement 2016 paper pdf`; `global interconnect optimization Daboul Held Natura Rotter pdf resource sharing 2023` | S09–S11/S22. A shared data library is not silently a unified predictive model. S11 full method unavailable. |
| 3 bounded repair | `"Divergent Thoughts toward One Goal" pdf`; `"setup" "hold" "congestion" "buffer" optimization post CTS placement paper`; `"clock" "data" "placement" "unified" "predict" physical design 2025`; `"hold" "repair" "reservation" buffer timing ECO placement` | S02/S05/S12. General repair side effects already known. |
| 4 methods and contests | `"Power-aware hold optimization for ASIC physical synthesis" doi`; `"A PUS based nets weighting" pdf`; `"Global Interconnect Optimization" "pdf" Held 3587044`; `"repair timing" "hold" "joint" placement optimization 2025 2026`; `"Drive Strength Aware Cell Movement" pdf`; `"hold" "buffer insertion" "placement" "simultaneous" optimization timing`; `"hold" "repair" "lookahead" placement`; `"ICCAD 2015" "timing driven placement" winner paper` | S12/S21/S22 and old cell-movement leads; recent contest material led to S15–S19. No claim of full paper access from metadata. |
| 5 current contests | `"2025 ICCAD" "Problem C" incremental placement optimization winners`; `"Post-Placement Buffering and Sizing Contest" 2026`; `"Drive strength aware cell movement techniques" Flach`; `"A PUS based" "sciencedirect"`; `"ISPD 2026" "contest" winners buffering sizing github` | Current official material and correction, public baseline. Winner wrappers unresolved. |
| 6 alternative formulation | `"hold repair" "Benders" placement`; `"hold" "buffer" "resource" "placement" "matching" timing optimization`; `physical design hold buffer placement simultaneous cell movement "integer"`; `"Benders" "placement" "timing" buffer`; `"hold" "buffer insertion" "minimum" "multiple" process corners 2016 pdf`; `"setup hold" "placement" "reservation" optimization EDA` | S13 and generic decomposition lead. No application of Benders is claimed as new; the selected algorithm need not use cuts. |
| 7 citation/forward expansion | `"Novel Multi-Corner Delay Padding"`; `"A CPS framework based perturbation constrained buffer planning approach" DOI`; `"hold" "buffer" "planning" "reservation" physical design placement 2026`; `"Repair" "closure" "placement" "hold" EDA` | Followed S12 references and newer padding/capacity terms. S13 full paper inspected; S23 recent presentation title/setup lead only, scientific method unresolved. |
| 8 patent and current-version refresh | `patent Synopsys "hold" "buffer" "2016-08-30" placement`; `"hold-time" "net ordering" "buffer allocation"`; `"hold time" "regions" "Synopsys" patent 2016`; `"Global Interconnect Optimization" "hold"`; `"Logic-Based Benders Decomposition" Hooker Ottosson 2003 pdf`; `"post CTS" "hold" "hypergraph" optimization buffer`; `"ChatEDA" "arxiv" 2023 autonomous agent`; `"hold buffer" "placement" "look-ahead" EDA`; `"hold fixing" "placement" "reservation" 2025 2026` | Public patent S14 defeats reservation novelty. S03 refreshed from v1 to v3 and official code corrected; S08 inspected for existing prediction-guided physical action. Generic LBBD author overview was opened as an alternative, not asserted as an exact EDA reduction. |

## Actual primary access and exclusions

Full accessible documents mean text was available; locators specify sections actually inspected. S01 framework §III and S02 §3 were read; S03's complete current methodology/Algorithm1 and current official implementation interfaces were inspected. S06's actual shared-load/rollback code was read, not inferred from its name. S13's ILP occupancy formulation was inspected. S15's current contest evaluation and announced roadmap were inspected separately.

Initial `https://aclanthology.org/2025.naacl-long.106/` was a wrong-title result and excluded immediately; EDAid evidence comes from its arXiv paper. AgenticPD v1 and the third-party Cheatnut repository were accessed before locating v3 and author-linked code; they are historical discovery, not the current baseline. The third-party commit was f4cf53a5526d3f941b3a25c6fea6a993c7514a02; README and search/stage_pipeline.py were read. No source instructions were executed.

The broad searches included unrelated network traffic, speculative journal hits, research social profiles and reposted proprietary manuals. These were not used as primary technical proof. Patent discovery used a secondary result only to identify the original public disclosure, which was then opened through Google Patents. Its existence establishes disclosed ideas, not enforceability or legal advice.

Full S11/S12/S22 methods remain incomplete. S12's publisher abstract/introduction/snippets were accessible through search even when direct opens returned Internal Error. ICCAD2025 Drive wrappers for problem PDF/top3 zip did not yield their contents; no login/bypass was attempted. ICCAD2015 winning slide link failed. ISPD2026 wrong URL without index initially failed; the official index succeeded. S23 PDF metadata/text extraction was partial and repeated section opens failed; no novelty claim relies on its full method. These are access facts, not evidence of absence.

## Versioned public code access

Used Python urllib against public GitHub APIs (`/repos/{owner}/{repo}/commits?per_page=1`, `/git/trees/{sha}?recursive=1`) to resolve and inspect relevant raw files; no downloaded code was executed. Four initial repositories were queried independently: OpenROAD, wuhy68/ChatEDA, Cheatnut/AgenticPD, OSCC-Project/AiEDA. Then author-linked Flians/AgenticPD and ABKGroup/ISPD26-Contest were inspected. Pinned source records include file hashes where content was read. ChatEDA current default commit02bb522a98f759595fbfce6bee33f64ef02ce3a5 and AiEDA788857fad4ce5e14cafd4c2ce55eebebdd45f50b were metadata checks, not a full-code audit.

Reproduce a source read without running its code:

```python
import hashlib, urllib.request
url = 'https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD/8da6ac250b0349c346d1abed7c2c43107f4ff6f7/src/rsz/src/RepairHold.cc'
body = urllib.request.urlopen(url, timeout=30).read()
assert hashlib.sha256(body).hexdigest() == '5e5fd39774743e612f2337ca6e86af352bf50b07ce30870ba832b33eeee77f9f'
lines = body.decode().splitlines()
print('\n'.join(f'{i+1}: {lines[i]}' for i in range(573,684)))
```

## Lightweight analytical check actually executed

Command: `python3 - <<'PY'` with the following standard-library code. This checks seven abstract assignments, not an EDA performance experiment. No physical delays are measured; scores are dimensionless constructed ranking values.

```python
import itertools
score = {'A':30,'B':25,'C':20}
slots = {'A':['s1'],'B':['s1'],'C':['s2']}
def feasible(moves):
    return any(len(a)==len(set(a))
               for a in itertools.product(*(slots[m] for m in moves)))
subsets = [s for k in range(3) for s in itertools.combinations(score,k)]
valid = [(sum(score[x] for x in s),s) for s in subsets if feasible(s)]
assert len(subsets)==7
assert not feasible(('A','B'))
assert max(valid)==(50,('A','C'))
print(len(subsets),max(valid),feasible(('A','C')))
```

Observed equivalent execution output: subsets_enumerated=7; unconstrained score55 for A+B, jointly_feasible=false; feasible_best=[50,[A,C]]; sequential_A_then_C_also_finds_best=true. Shared-option control was checked logically: a single allowed option covering both hA/hB at s1 makes A+B feasible. No claim that this is new or physically realized.

Packet check actually executed: SHA-256 over every policy/PACKET.json mapping returned31 files/0 mismatches. Supplied predecessor manifests returned3,7,12 files/0 mismatches. These hashes establish byte provenance only. The standalone trusted freeze validator is used for submission; full repository validation is delegated by the job contract to publication, not falsely claimed to pass locally.

## Stopping rationale and refresh

Two successive expansions found closer planning/reservation/contest evidence; they were not empty searches. This round stops at bounded documentary coverage with unresolved closest-method/winner gaps. Absence in searches does not establish novelty or impossibility. EXP-001 specifies the next exact uncertainty: same-assumption overlap and a faithful conventional joint interface. Refresh versions and all decision-critical new work before promotion or manuscript submission. No scientific approval, resource allocation or reviewer consent is inferred from source access or freezing.
