# Independent research and execution log

UTC retrieval date: 2026-10-16T04:18:05.624419+00:00. Exact input d0eedf3130de673ea92e4be202a32d463a63f301; role/session/job are recorded in compliance.json. Work occurred only in the assigned standalone job and external public sources. No checkout access, other-role private material or downloaded-code execution. Required common policy and only CHALLENGER harness read. Initial long tool output was truncated; automation/isolation and harness were reopened separately. Own forecast-independent numeric physical estimate remains unknown; review is explicitly unblinded and proposal forecast limitations were visible.

## Search expansions

1. Web search: `design rule checking incremental query caching active learning route repair value information`; `"design rule checking" "2026" incremental GPU`; `Pandora box problem correlated inspection costs value information shared observations`. Included AiDRC and costly value-estimation routing; excluded general networking/cache encyclopedia hits. Opened original papers rather than using secondary summaries as verdicts.
2. Web search: `"AiDRC" design rule checking pdf`; `ISPD 2026 2027 contest detailed routing winner`. Publisher-indexed primary methods available for AiDRC; direct DOI/full page and author PDF opens failed. Official2025/26/27 and2019 pages inspected. No claim that2027 lacks a contest; archive/title evidence alone is bounded.
3. Citation/terminology expansion: `"AiDRC" "incremental" checking`; `"OpenDRC" "incremental" 2025 2026`; `"Dr. CU" 2019 contest presentation pessimistic`. Inspected Dr.CU2 paper, source-linked slides search excerpts, FastPass public README, and IJCAI2005 backward VOI source. AiEDA/iPCL cited-by entries and FastPass cited papers are leads not full-method audits. Noise and secondary DeepWiki/ResearchGate were not used for decisive claims.

Stopping condition: bounded round budget, NOT two exhausted closer-work expansions. AiDRC full-method/code access, complete selective OpenROAD dependency audit, winner-binary correspondence, cited-by papers and CN122839978A remain unresolved. Google Patents primary opening failed again; no patent conclusions adopted. ISPD2019 result-PDF opening failed; official HTML remains accessible. No absence-of-result novelty claim.

## Source reading and local checks

Pinned raw OpenROAD source was fetched read-only in memory by Python urllib.request and printed with raw one-based line numbers; nothing downloaded was executed. SHA-256:
- FlexGC_main.cpp:4770ffdc8f1ac0fd13e69dac1a0b75c5dbb795bf7c043be5ed2b8294cb43a517;849–875,1516–1525,4021–4062.
- FlexGC.h:293e895cf573ccba346d5bf35184dac066f00509e327a53e370256078a945e64;45–81.
- TritonRoute.cpp:1bb6bef08a426c311d6e1b8fae12db89bfb69be89ff7340f381a95b6ab37f335;1089–1110.

URLs and applicability limits are in sources.json. These are selected reads, not all-path proof. No external source copies are published. Current proposal, tasklist, source records, experiment plan, direction-control, responses and consent were read, plus predecessor verifier verification.md; predecessor proposer files were only enumerated, not opened. No legacy output counts were independently attested.

## C-A01 exact own analytical replay

Purpose: test the one-step positive-value stopping rule under complementary information. Four equiprobable states; binary terminal decision; two distinct slot observations; cost0.1 each. Common exact-check cost is a reserved constant omitted equally. This does not model physical geometry, calibrated repair probabilities or real runtime. Only own tiny Python was executed, twice with identical stdout; no EDA/build/training run.

Replay: copy the exact block including final newline to a temporary .py file and run `python3 FILE.py`, or pass the exact string to `python3 -c`. Script SHA-256 `a4ccd79aa1efc4408d5f3a182edc81434361e16699784184c050f35be3a4e0f0`. Stdout SHA-256 `3431adaa0a9c2505bcde3b3b237b8f221a959b691942e4b217c86b0ee21f03e7`.

```python
from itertools import product
states=list(product((0,1),repeat=2))
def value(observed):
 groups={}
 for x in states:
  key=tuple(x[k] for k in observed)
  groups.setdefault(key,[]).append(x[0]^x[1])
 return sum(max(sum(v),len(v)-sum(v)) for v in groups.values())/len(states)
for observed in [(),(0,),(1,),(0,1)]:
 print(f'observe={observed} terminal={value(observed):.2f} net={value(observed)-0.1*len(observed):.2f}')
assert value(())==value((0,))==value((1,))==0.5
assert value((0,1))-0.2==0.8
```

Exact stdout:
```text
observe=() terminal=0.50 net=0.50
observe=(0,) terminal=0.50 net=0.40
observe=(1,) terminal=0.50 net=0.40
observe=(0, 1) terminal=1.00 net=0.80
```

## Submission checks

Own JSON parse and trusted standalone freeze are the local validation scope. Full-repository `scripts/project.py validate` is delegated to coordinator publication because this packet lacks the checkout and foreign harnesses. No checkout discovery was performed to satisfy it. Freeze is byte/provenance validation, not scientific approval. Complete result.json is written after successful freeze.
