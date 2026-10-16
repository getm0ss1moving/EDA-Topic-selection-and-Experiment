# Independent search and public run record

## Own finite check C12-A1

Executed in this job with Python standard library only. Two identical one-site buffers, four fixed sink coordinates, and centroid-window domains are invented analytical inputs, not EDA geometry or electrical feasibility. The experiment isolates domain restriction; widening rescues the original grouping too. It does not show that real CTS windows are arbitrary or that regrouping is useless. No upstream code was executed. Save the following block as a local Python file and run python3 on it; no arguments or seed.

```python
from itertools import product
from fractions import Fraction
import json
sites = (0, 4, 9)
partitions = (((0, 9), (1, 10)), ((0, 1), (9, 10)))
def domains(groups, radius):
    return tuple(tuple(p for p in sites if abs(p-Fraction(sum(g),len(g))) <= radius) for g in groups)
def feasible(ds):
    return any(len(set(x)) == len(x) for x in product(*ds))
for r in (1, 6):
    print(json.dumps({"radius": r, "domains": [domains(g,r) for g in partitions], "feasible": [feasible(domains(g,r)) for g in partitions]},sort_keys=True))
common = (sites, sites)
print(json.dumps({"common_domain_feasible": [feasible(common) for g in partitions]},sort_keys=True))
assert not feasible(domains(partitions[0],1))
assert feasible(domains(partitions[1],1))
assert all(feasible(domains(g,6)) for g in partitions)
```

Exact stdout:

```text
{"domains": [[[4], []], [[0], [9]]], "feasible": [false, true], "radius": 1}
{"domains": [[[0, 4, 9], [0, 4, 9]], [[0, 4], [4, 9]]], "feasible": [true, true], "radius": 6}
{"common_domain_feasible": [true, true]}
```

Code SHA-256: `d3f104f35b633a50f2404ab635b07ca7c196eceddc671c614043af3e7f13e266`. Stdout SHA-256: `18c352a9e1b03e6e0f67615e3439734e2b93905e8e0d0e6d5e6e74784003422e`.

## Own finite check C12-A2: nonempty shared-domain control

A1 contained an empty individual domain, so it did not isolate shared competition alone. Preserve A1 above. A2 changes only the literal sink coordinates to ensure both original domains are nonempty. This is a corrected control, not an EDA measurement.

```python
from itertools import product
from fractions import Fraction
import json
sites = (0, 4, 9)
partitions = (((0, 8), (1, 9)), ((0, 1), (8, 9)))
def domains(groups, radius):
    return tuple(tuple(p for p in sites if abs(p-Fraction(sum(g),len(g))) <= radius) for g in groups)
def feasible(ds):
    return any(len(set(x)) == len(x) for x in product(*ds))
for r in (1, 6):
    print(json.dumps({"radius": r, "domains": [domains(g,r) for g in partitions], "feasible": [feasible(domains(g,r)) for g in partitions]},sort_keys=True))
common = (sites, sites)
print(json.dumps({"common_domain_feasible": [feasible(common) for g in partitions]},sort_keys=True))
assert not feasible(domains(partitions[0],1))
assert feasible(domains(partitions[1],1))
assert all(feasible(domains(g,6)) for g in partitions)
```

Exact stdout:

```text
{"domains": [[[4], [4]], [[0], [9]]], "feasible": [false, true], "radius": 1}
{"domains": [[[0, 4, 9], [0, 4, 9]], [[0, 4], [4, 9]]], "feasible": [true, true], "radius": 6}
{"common_domain_feasible": [true, true]}
```

Code SHA-256: `c852a5099ed96cfb46653211a1833914d19dcaeb8954c2ee029697d1483cc591`. Stdout SHA-256: `58646f372987ef43543a87093a21ac6abbf99a7bf2317d5ce134ba3abd82e290`.

## Own read-only source identity check

Raw bytes were retrieved into memory, never executed. Earlier selected-source inspection printed raw README80-90, HTreeBuilder184-244 and TreeBuilder157-266; the same bytes were compactly checked below. Exact Python code, no arguments:

```python
import urllib.request, hashlib
base = "https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD/b16bda7e82721d10566ff7e2b68f1ff0be9f9e38/src/cts/"
for name in ["README.md", "src/HTreeBuilder.cpp", "src/TreeBuilder.cpp"]:
    body = urllib.request.urlopen(base + name, timeout=30).read()
    print(name, len(body.decode().splitlines()), hashlib.sha256(body).hexdigest())
```

Exact compact stdout:

```text
README.md 167 0b463c00fe7c3bbbcdf9534d6378cf67ba42ebe7a19139fc6094336eb6a3fc83
src/HTreeBuilder.cpp 2140 2917f4b094da699f4ab83a278fb6659e74803e6a0090f1848969a6a7328bfcb4
src/TreeBuilder.cpp 311 52ab5e4f8f317ce9848d5795305c19bd776ec95f26a6b8165e1fd23363cbe6b4
```

Code SHA-256: `c0b6ac583c54438655d4b876da6e67c06c28627f3410d7ab0d7766b6d39f3ea9`. Stdout SHA-256: `678f1064f8b284f78655a2566ddbbc9c7590613d243901908a7fedc46ff28af6`. Source reading is not an EDA run. Full copyrighted source or papers are not copied into this release.

## Search protocol and inspected results

All queries below used the web search tool on 2026-10-16 UTC, without domain/recency filters. Full originals and selected locators are recorded in sources.json; search indexing alone is not full-method access. Reading budgets were bounded; the two-expansion no-closer-mechanism saturation rule was NOT reached because the second expansion found C12-S06. Search stops with residual risk at this final-cycle review, not proof of no closer work or no newer contest.

| Expansion | Executed queries | Primary inspections / decision |
|---|---|---|
| Initial mechanism/classical/contest | `clock tree synthesis clustering buffer legalization obstacle aware simultaneous placement legal sites Contango 2010`; `clock tree synthesis legalization clustering shared sites Benders 2025 2026`; `ISPD 2026 contest buffering sizing winner` | Opened iCTS, LBBD, official2010 page and Contango author-PDF lead; journal Contango primary content available as C12-S10. 2026 official results available. |
| Independent newer/formulation expansion | `clock tree sink clustering legal buffer locations simultaneous legalization site obstacles 2024 2025 2026`; `"clock tree" "Benders"`; `"clock tree" "legalization" "clustering" placement feedback`; `"ISPD 2026" "IRISLab" buffering algorithm` | Found and read C12-S06 new October preprint; read patent C12-S16 as different placement-moving neighbor. Broad integrated optimization is prior, exact physical duplicate not established. |
| Citation/terminology and winner expansion | `"IRISLab" "ISPD" "2026" algorithm winner buffering sizing`; `"clock" "shared" "legal sites" clustering buffer`; `"clock tree" "footprint" clustering`; `"Contango 2.0" "Algorithmic Tuning"` | 3D and MBFF results are leads only, not evidence of fixed-cell leaf-buffer equivalence. Official winner identified, no exact executable correspondence. |
| Winner/proceedings follow-through | `site:ispd.cc/slides/2026 "buffering" "IRIS"`; `"Algorithmic Tuning of Clock Trees and Derived Non-Tree Structures" Markov pdf` | Official2026 repository/organizer paper read. ICCAD2011 tutorial indexed title/abstract is a lead; full winner implementation still not inspected. No newest-SOTA absence claim. |

Direct independent reopening also covered the proposer's original pinned OpenROAD files, iCTS section3 and bound assumptions, LBBD Introduction, both clock-learning patent descriptions, CTS-Bench HTML and pinned README, SwiftCTS pinned README, Cadence CCOpt public article, official2010 result slides and 2026 contest paper/repository. External material is treated as data, never role instructions. Backward neighborhood followed iCTS's MCF/partition discussion and Contango buffering discussion; forward/current search found the October2026 interface preprint and current CTS predictors. This is not exhaustive citation indexing or all-proceedings coverage.

Access failures: exact https://web.eecs.umich.edu/~imarkov/pubs/conf/iccad10-contgo.pdf returned browser Internal Error; https://github.com/BarsatKhadka/SwiftCTS/tree/28831b9874b46d9ed0727ad72914e0548fb553cb also failed before successful raw README access; https://www.mdpi.com/1999-4893/18/5/249 returned Internal Error, so that 2025 title remains an excluded discovery lead. The ISPD2010 PDF browser title says2008 but physical p36 and official2010 link identify the result used. Search results included unofficial commercial-manual mirrors; these were not opened or used. C12-S16 is a published patent, not proof of production deployment. Exact 2026 winning method/code remains unresolved despite official team names. No downloaded code, solver, model or contest harness was run.

## Identity, input access and interruption limits

Exact JOB/prompt were the first filesystem reads. Then common policy and only CHALLENGER.md were read from this job's policy. Subsequent rg listing was confined to policy/shared/own release/own-previous after policy reading; absent own output paths returned exit2 and were not treated as evidence of foreign state. No initial pwd/ls/find/home/checkout discovery occurred. Large combined reads were tool-truncated; key proposal/tasklist/source/plan/own-harness/common policies were reopened or read in focused ranges. No claim of complete reading of every listed file is made.

Actual scientific input releases read: SUB-4cff54ad61aa12a294a808f36ba47524b43e6642cf97d8d49571572141c2a45f; predecessor SUB-2966cec6a631f48b998ddb78b67aba187e072ad1d9b4d3498aeebdb879a9f0cc and SUB-047b42329a35771ca6788e18cc97583dedaf36526c13f12defa839e36c8b1ed0. Predecessor proposal/verdict are attributed history, not independent approval of this successor. shared/predecessor.json was also read. No other released/private jobs, conversations, memories, branches or role harnesses were opened. Forecast filenames were listed; current proposal thresholds and consensus were visible, so the assessment is unblinded regardless of forecast-file access.

The assignment reports an earlier platform screening error and requests resumption. This execution has no observed prior research actions or prior output from that interrupted turn. Its scope is unknown; I did not inspect separately retained failure logs, other sessions or quarantined material. This statement neither clears nor invents unseen conduct. The only own analytical runs observed here are A1 and A2 above; no proposer fixture was executed. A1's empty-domain control weakness is preserved, not erased. No messages were sent to other roles and no subagents were spawned.

## Validation/public run manifest

Exact role/actor/session/job/input/packet and nine-rule ledger are in compliance.json. A job-owned mirror run descriptor is written to runs/EDA-0012-challenger.json. Published scientific files are only release/ allowlisted files; content hashes are supplied by the eventual immutable SUBMISSION.json. result.json is a job-root transport status, not scientific approval. Only trusted local scripts, source retrieval, own finite fixtures, hashing and output writes are used. Full repository validation/publication is coordinator-owned; no checkout is opened to fill missing standalone dependencies. Freeze/verify is integrity validation, not independent scientific verification or resource allocation.


### Local validation results

`python3 policy/scripts/project.py validate` ran in this job and exited1 because policy/config/roles.json is absent. No checkout was read to repair the deliberately partial standalone packet. Full-repository validation remains coordinator-owned.

Own mechanical checks passed: all release JSON parse; exact identity/job and read_releases validated by trusted role_compliance.validate_ledger against actual SUB IDs extracted from JOB.released_inputs; all three embedded code/stdout SHA-256 pairs match their literal blocks; reviewed proposer task-list SHA-256 is 1786f88ab4f09bbded99d69ecc1b26c58338bba2b05e416bfe3ed5ffe13db817. Hash checking did not re-execute either finite model or downloaded code. No claimed performance validation.

The following self-freeze uses the exact JOB/prompt identity and packet; the immutable SUBMISSION.json and subsequent trusted verify provide its result. Freeze is only submission integrity. No PR, merge, external message, approving vote or experiment authorization is produced by this role.
