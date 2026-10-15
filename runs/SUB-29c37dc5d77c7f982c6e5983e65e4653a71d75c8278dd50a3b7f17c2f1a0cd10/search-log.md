# Independent search and execution log

Date: 2026-10-15 UTC. Actor/session and exact input are in workflow.json. Scientific prose English. Search engines: web tool search/open/find plus direct public urllib retrieval. No project checkout, other-role private output, session lookup, memory, contacts or subagents used. Sources and paths in sources.json identify released outputs; private retrieval scratch is /tmp/eda0006-c05-r1-review. No source copy is included in release.

## Search rounds

1. Initial independent terminology expansion: `static timing analysis simultaneous multi scenario incremental speculative gate sizing memoization canonical delay patent`; `variational execution sharing equivalent states bitset configurations scheduling timing analysis`; `ICCAD 2026 contest timing sizing winner ISPD 2027 contest`. This found variational execution, statistical-timing patents and current contest leads. Quantum/WCET/off-topic results excluded. Primary C01/C12 were opened, not accepted from snippets alone.
2. Follow-up: `Faster variational execution github VarexC conditional values`; `ISPD 2026 winner buffering sizing algorithm`; exact title `Reducing runtime and memory requirements of static timing analysis`. Found the 2018 author PDF, author code and the patent family. The B2 URL failed. Family result US20140298280A1 identified US8839167B1; the B1 primary full text opened successfully. This resolves proposer S05's access problem, while optional tolerances limit exactness inferences.
3. Citation/code neighborhood: inspected C01 code link, author's thesis and GitHub tree API. Pinned VarexC to 1221ef110e2b46951ab01319e97fa5d7dd84a724; inspected VImpl.java and VHashMap.java. The selected functions provide an explicit map/intersection/union reduction. No Java build or automated full-method equivalence test performed.
4. Broader later neighbors: `variational execution timing analysis ECO`; `simultaneous multi-scenario static noise 12518077`; `VarexC sharing 2025 2026`. Found C11 in 2026 and reopened its primary patent. Worst-case noise merging differs from retained exact candidate outputs, so excluded as a direct duplicate. Secondary discovery pages and irrelevant results are not evidence. Search budget ended with residual risk, not two no-closer expansions or a completeness certificate.
5. Contest/winner expansion: `IRISLab ISPD 2026 sizing winner algorithm`, `ISPD 2026 PTSD sizing` and broader winner query above. Official ISPD26 page verifies ranking, but no verified winner algorithm/code located. Read ISPD26 repository, current ISPD27 evaluator and ICCAD26 official topics. Newer edition coverage is partial; no claim that none exists or no winner uses this mechanism.
6. Reopened proposal-critical sources: OpenROAD exact Resizer pin directly; transactional paper author PDF; EDAid and PreRoutGNN full HTML selected methods. iTAP author PDF failed web opening and timed out on direct retrieval; not used to establish an objection. Transactional PDF web failure was repaired by direct legitimate author download, then pdftotext. No commercial internals inspected.

## Commands, provenance and costs

Direct retrieval used Python urllib.request.urlopen(url, timeout=20), writing only external scratch; independent URLs included the author transactional PDF, iTAP PDF, public VarexC tree API and exact Resizer source. Then:

```
pdftotext -layout /tmp/eda0006-c05-r1-review/transaction.pdf /tmp/eda0006-c05-r1-review/transaction.txt
rg -n -A 22 -B 5 'Case 2|Candidate selection|candidate selection' /tmp/eda0006-c05-r1-review/transaction.txt
sed -n '3220,3325p' /tmp/eda0006-c05-r1-review/resizer.cc
```

Retrieved hashes: transactional PDF fc65681fb41f2670b7dbbe963354d8a6819df68dbad8846a1855e435477efc6d; Resizer.cc ff3adf14a5f8f9059a293b7fbfbf39ce4138f008294c43fd86d6cc46c6024b85; VarexC tree JSON 95513bb88fe60be100faca08eeb9feb13417f4851df5692b5561911a40c28e6c. Function names are stable locators because browser-extracted line numbering differs from raw file numbering. No runtime timings, EDA run, training, experimental cost estimate or reproduced paper performance is claimed. Network retrieval and prose/check commands only; elapsed research effort was not precisely metered.

Outputs: release/challenges.md, release/tasklist.md, release/sources.json, release/prior-art.csv, release/workflow.json, release/experiment-consent.json and this log. The role script writes immutable submissions/SUB-<digest>; coordinator transport stores its provenance under runs/. No separate checkout writes made.

Validation: JSON parsing and trusted role_submission.py freeze/verify, followed by result.json schema-key/status check. Full repository `python3 scripts/project.py validate` is intentionally deferred to coordinator publication because this assigned standalone job excludes the repository and foreign harnesses. Freeze checks form/provenance, not scientific truth.
