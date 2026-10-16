# Search log and public run record

## Identity, scope and stopping

Topic EDA-0012; D04 batch0004 cycle4/4. Actor/session/job/input commit/packet are copied exactly in compliance.json. Research date2026-10-16 UTC. Public evidence uses paper/source/contest reading and one tiny own finite model, not an EDA flow. Scope: fixed-placed ASIC CTS leaf sink partition and legal buffer footprints. No private role material, parent conversation, shared memory, checkout discovery or unallocated code execution was used.

The first tool read exactly assigned JOB.json and prompt.txt. Only afterwards rg --files policy was used to find common policy and the one proposer harness. Common rules, brief, templates, trusted scripts and only explicitly assigned predecessor files were inspected. Large combined text reads were partly tool-truncated; CODEX-AUTOMATION/SELF-SUBMISSION/batch policy and predecessor verifier JSON were reopened in targeted reads. No unlisted predecessor release or parent role note was read. The final source/own-check work is a research release, not scientific verification of itself.

## Queries and result decisions

Index: web search, unfiltered unless indicated. All below executed2026-10-16; source IDs denote originals inspected. No search absence is used as novelty proof.

| Expansion | Exact or faithfully grouped executed queries | Inspected / decision |
|---|---|---|
| Initial CTS need | clock tree synthesis obstacle aware sink clustering legalization buffering congestion OpenROAD TritonCTS paper; clock tree synthesis learning congestion obstacle aware clustering exact min cost flow paper; ISPD clock tree synthesis contest 2010 benchmark obstacles sink clustering winner | S01-S04,S11; broad displacement relevance; no primitive novelty. |
| Classical assignment | clock tree synthesis sink clustering buffer legalization min cost flow capacity obstacle; clock tree synthesis simultaneous clustering legal buffer location matching capacity flow; "clock tree" "Hall" legalization clustering; "TritonCTS" "legalization" "clustering" paper | iCTS S04 is close; generic exact assignment remains mandatory comparator. |
| Site/representation | "clock tree" "legalization" "capacity" buffer clustering; "clock tree synthesis" "Benders" OR "matching" OR "site"; site constrained clock buffer insertion simultaneous placement exact legality clustering cuts; "clock tree synthesis" "site capacity" ASIC; "clock buffer" "Hall" OR "Benders" OR "infeasible" clustering | No direct exclusive novelty conclusion; FPGA resource-capacity results excluded as different architecture unless transfer justified. |
| Current prediction and code | "CTS-Bench" github graph coarsening clock tree; "clock tree synthesis" "legalization" "learning" 2025 2026; "clock tree synthesis" "legal" "clustering" 2025 2026 paper; "CTS" "Wu" "2025" "clock" GNN prediction | S08/S09/S14, plus S05/S06 patent neighborhood; current unified and separate-head predictors already exist. Wu lead not fully checked; not a decision source. |
| Conventional decomposition | "logic based Benders" scheduling planning Hooker 2007 pdf | Author S07 opened; assignment/subproblem cut feedback acknowledged conventional. No scheduling speedup imported. |
| Commercial | site:cadence.com Innovus clock tree synthesis concurrent clock optimization placement legalization | Official S10 opened. Advertised capability only; inaccessible tutorial/support links not bypassed. |
| Contest/winner refresh | ISPD 2025 contest 2026 contest clock tree synthesis; "Algorithmic Tuning of Clock Trees" Contango Markov PDF | Official S11/S12/S13 checked; S-X01 open error; S-X02 index-only; exact winning source bridge unresolved. |

Backward/citation expansion: inspected iCTS's K-means/MCF and GH-tree discussion, CTS-Bench reference list/forward-future-work, patent citation neighborhood and official contest archive. This is bounded neighborhood work, not systematic forward citation enumeration or all proceedings coverage. No additional new full-method source establishes the proposed joint footprint feedback's novelty. Two expansions continued finding close mechanisms (patent learning and LBBD), so the evidence-standard saturation stop was NOT reached. Search stops by bounded final-turn budget and finite batch hard stop; residual novelty/contest risk is explicitly unresolved. Before any future promotion a new, separately authorized refresh must resolve these gaps; no automatic fifth cycle follows.

## Access, corrections and excluded material

sources.json records exact full/abstract/metadata access. Full means original content available and the stated section inspected, never an all-method audit. Raw OpenROAD byte files have exact one-based locators and hashes; web rendering line counts differ. Wrong guessed src/cts/src/README.md failed and was corrected to src/cts/README.md. Contango author-PDF direct browser open failed; indexed title/text is not reported as full method access. Historic result PDF browser title says2008 while official2010 link/content identifies the event; no inference rests on that title. Team/method diagram extraction loses alignment, so the winner algorithm is not reconstructed from it. CTS-Bench and SwiftCTS license/data/label/code audits remain pending. No copyright full text or source file copies are included in release.

Public source bytes were read by urllib into memory, selected ranges printed for inspection, and compact source hashes/line counts replayed below. No upstream Python/Tcl/C++ was executed, installed, compiled or imported. GitHub API resolved current heads to S09/S14 exact commits; README hashes are in sources.json. Those metadata reads are not model or benchmark execution.

## Analytical fixture: exact runnable code and parameters

Parameter domains and footprints are all literal below; Python standard library only, no random seed, files, network or solver. Run by saving the fenced block as /tmp/eda0012_finite.py and executing python3 /tmp/eda0012_finite.py, or extract/exec the block directly. It was run once for scientific model output during this job; mechanical replay may repeat the identical fixture. The third/fourth/fifth cases are negative controls. The finite solver deliberately uses exhaustive conventional search; no candidate advantage is implied. The alleged missing information applies only to independent nonempty-domain/origin abstractions, not an observed OpenROAD defect.

```python
from itertools import combinations, product
import json

def solve(domains):
    for choices in product(*(sorted(d) for d in domains)):
        if len(set(choices)) == len(choices):
            return list(choices)
    return None

def deficient(domains):
    for k in range(1, len(domains)+1):
        for ix in combinations(range(len(domains)), k):
            sites = set().union(*(domains[i] for i in ix))
            if len(sites) < len(ix):
                return {"clusters": list(ix), "sites": sorted(sites)}
    return None

cases = {"contended": [{"a"}, {"a"}],
         "regrouped": [{"a"}, {"b"}],
         "no_contention": [{"a", "b"}, {"a", "b"}]}
for name, ds in cases.items():
    print(json.dumps({"case": name, "each_nonempty": all(ds),
                      "assignment": solve(ds), "deficiency": deficient(ds)}, sort_keys=True))
# Distinct site origins are insufficient if cell footprints overlap.
origins = [{0}, {1}]
footprints = {0: {0, 1}, 1: {1, 2}}
choice = solve(origins)
print(json.dumps({"case": "overlapping_footprints", "origin_matching": choice,
                  "physical_nonoverlap": not bool(footprints[choice[0]] & footprints[choice[1]])}, sort_keys=True))
# Incomplete domains cannot certify infeasibility of the physical problem.
print(json.dumps({"case": "domain_expansion", "restricted": solve(cases["contended"]),
                  "expanded": solve([{"a", "b"}, {"a"}])}, sort_keys=True))
assert solve(cases["contended"]) is None
assert solve(cases["regrouped"]) == ["a", "b"]
assert choice == [0, 1] and footprints[0] & footprints[1]
```

Exact compact stdout:

```text
{"assignment": null, "case": "contended", "deficiency": {"clusters": [0, 1], "sites": ["a"]}, "each_nonempty": true}
{"assignment": ["a", "b"], "case": "regrouped", "deficiency": null, "each_nonempty": true}
{"assignment": ["a", "b"], "case": "no_contention", "deficiency": null, "each_nonempty": true}
{"case": "overlapping_footprints", "origin_matching": [0, 1], "physical_nonoverlap": false}
{"case": "domain_expansion", "expanded": ["b", "a"], "restricted": null}
```

Code SHA-256 (UTF-8 fenced content with final LF): `80d1fd91cd78444f24b278a0a28ce28a65bc84c1085b48eef686e0a4e78f89b4`.
Stdout SHA-256 (UTF-8 with final LF): `9e39aa7fd9989f74599e06c78f682cb54914ee232f8f44cd3d63367984da4591`.

Interpretation: local legal existence is insufficient for simultaneous assignment, full footprints matter for multi-site cells, and infeasible restricted options can become feasible after expansion. Regrouped domains are invented inputs, not generated from real sinks/rows or a proof an exchange realizes them. No timing, QoR, skew, runtime speedup, empirical prevalence, conventional superiority or physical headroom is measured.

## Reproducible compact source check

Exact source retrieval/check script (read only; no downloaded-code execution):

```python
import urllib.request, hashlib
base = "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD/b16bda7e82721d10566ff7e2b68f1ff0be9f9e38/src/cts/"
for name in ["README.md", "src/HTreeBuilder.cpp", "src/TreeBuilder.cpp"]:
    body = urllib.request.urlopen(base + name, timeout=30).read()
    print(name, len(body.decode().splitlines()), hashlib.sha256(body).hexdigest())
```

Exact stdout:

```text
README.md 167 0b463c00fe7c3bbbcdf9534d6378cf67ba42ebe7a19139fc6094336eb6a3fc83
src/HTreeBuilder.cpp 2140 2917f4b094da699f4ab83a278fb6659e74803e6a0090f1848969a6a7328bfcb4
src/TreeBuilder.cpp 311 52ab5e4f8f317ce9848d5795305c19bd776ec95f26a6b8165e1fd23363cbe6b4
```

Code SHA-256: `c0b6ac583c54438655d4b876da6e67c06c28627f3410d7ab0d7766b6d39f3ea9`.
Stdout SHA-256: `678f1064f8b284f78655a2566ddbbc9c7590613d243901908a7fedc46ff28af6`.

Network availability can fail on replay; that is an access limitation, not a different source version. Selected source conclusions use raw function/line locators in sources.json, not only names or these metadata counts. Hash checks establish identity of fetched bytes, not semantic correctness, whole-flow completeness or independence.

## Public run manifest and validation

Own outputs: release/proposal.md, sources.json, search-log.md, prior-art.csv, contest-audit.md, industry-gap.md, experiment-plan.md, forecast.json, tasklist.md, responses.md, direction-control.json, experiment-consent.json, workflow.json, compliance.json. Submission manifest will supply their exact SHA-256 values under submissions/SUB-<hash>/SUBMISSION.json. A mirror run descriptor is stored in the job's own runs/EDA-0012-proposer.json; publication is coordinator-owned and no PR/merge is performed by this role. Full repository validation is the coordinator duty under prompt.txt; local trusted freeze/verify and standalone validation results are appended below.

No complete production implementation or EDA runner exists in this release; future bounded procedures are dependencies with explicit missing command/image bindings, not invented runnable flows. Own tasklist is identified by hash in proposal.md, with no signature to the containing release and no other-role vote.

### Local validation record

Executed `python3 policy/scripts/project.py validate` in the assigned job root. Exit1: missing `policy/config/roles.json`. This standalone packet is not the full checkout; no checkout read/discovery was performed to repair it. Full-repository validation remains coordinator-owned. This is a disclosed local validation limitation, not a scientific pass.

Own mechanical check passed: JSON parse, exact embedded finite-code and stdout SHA-256 replay, task-list SHA-256 equality, and trusted role_compliance.validate_ledger against exact actual authorized SUB IDs. Task-list SHA-256: `1786f88ab4f09bbded99d69ecc1b26c58338bba2b05e416bfe3ed5ffe13db817`. Mechanical replay repeated the same five tiny finite cases and produced the same stdout hash; no new physical observation arose.

Trusted self-freeze is requested using the exact JOB/prompt identity/input/packet command; its immutable SUBMISSION.json and subsequent verify output provide the actual result. A successful freeze is submission integrity only, never scientific approval, resource permission or dual consent.
