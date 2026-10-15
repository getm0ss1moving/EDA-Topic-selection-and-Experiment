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
