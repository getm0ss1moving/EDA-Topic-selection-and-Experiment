# Independent search and public analytical record: B4-R2

All searches/retrievals: 2026-10-16 UTC, ordinary public web search/open and Python urllib; no downloaded code execution. Initial reads were exact JOB.json and prompt.txt, then job policy. Discovery stayed inside job policy/released shared inputs/own prior output or external research. No checkout/home discovery. Review is explicitly unblinded: proposal/plan thresholds and outcome descriptions were read; forecast.json was not opened. Current target is SUB-1995793c1627da4adba27cf9a355047e58ef3c0d8627137a33ff6fc81e76f89f. The earlier shared proposal was read as released history before the current revision; no historical finding is treated as current verification.

## Search ledger

| Expansion | Query / access | Result inspected and decision |
|---|---|---|
| Current nearest work | AiDRC iterative design rule violation prediction 3769306 | ACM indexed primary text; DOI open failed. Author PDF web fetch timed out; urllib succeeded, pdftotext in memory read PDF13/26. C2-S01. Retain exact-final-check prior and unresolved channel/version bridge. |
| New work | 2026 incremental design rule checking context reuse DRC prediction | EvoDRC and Rule2DRC primary HTML; C2-S05/06. Repair consumer evidence and adjacent candidate discrimination; neither establishes residual-obligation equivalence. |
| New contests | ISPD 2025 routing winner algorithm 2026 contest | Official2019/2025/2026 pages; C2-S07/08/09. Stage differences; no unsupported latest-work absence claim. |
| Terminology expansion | 2026 design rule incremental cache routing; DRC value of information routing | US20250232106A1 secondary lead; primary Google Patents failed. No patent conclusion. Many off-topic hits excluded. IJCAI2005 primary §§1–2 reopened. |
| Citation/implementation expansion | EvoDRC residual candidate reuse; references in EvoDRC §2.3 and repository | Author HTML §3.2–3.4 and public README inspected. Benchmark lead and trial provenance matter; no benchmark files/agent histories inspected. DRC-Aid §3.3–3.4 reopened. |
| Contest winner implementation | DrCU pinned README and GitHub recursive source tree API | README explicitly links ICCAD2019 paper; PoorViaMap.cpp raw1–44 inspected. This file search did not locate pessimistic-query routine. Paper §III-C.2 is method evidence; exact contest executable remains unresolved. |
| Exact checker | pinned OpenROAD FlexGC_main.cpp | Range query851–875, min-area1516–1525, main4021–4062. First print requested4065 and hit IndexError after valid4062; rerun clamped to actual length. No source changed or executed. |

Two expansions found additional adjacent methods, not an exhaustiveness certificate. Source budget ended with unresolved actual observation likelihood, AiDRC final config/code, complete checker interface, full winner executable correspondence and patent primary access. No physical measurement or prior performance number is adopted.

## C2-A01: independent repair check and off-support interface witness

Own authored Python, no imports beyond standard library, no external fixtures. Four equiprobable states, two actions, cost1/10, terminal binary decision utility. Common final checker reserve cancels. The first part checks the repaired depth2 mechanism independently; it does not rerun or attest the proposer's96-setting sweep. The second part is a hypothetical literal finite-payload conditioning interpretation, deliberately not attributed to an implemented proposer adapter. A returned payload outside the finite set has zero mass, so a posterior requires an observation model or explicit fallback. Two possible repairs differ; neither is asserted correct physically. Cache equality stays exact independently of approximate planning likelihood. No legal geometry frequency or measured speedup follows.

Exact runnable code (copy the block including its final newline and run python3):

```python
from fractions import Fraction as F
from itertools import product
states = tuple(product((0, 1), repeat=2))
def terminal(pool, mode):
    labels = [(x ^ y) if mode == "xor" else x for x, y in pool]
    return F(max(sum(labels), len(labels)-sum(labels)), len(labels))
def value(pool, unused, depth, mode):
    best = terminal(pool, mode)
    if depth:
        for a in unused:
            groups = [tuple(s for s in pool if s[a] == o) for o in (0, 1)]
            v = -F(1, 10)
            for g in groups:
                if g:
                    v += F(len(g), len(pool))*value(g, tuple(i for i in unused if i != a), depth-1, mode)
            best = max(best, v)
    return best
for mode in ("xor", "single"):
    print(mode, "depth1", value(states, (0,1), 1, mode), "depth2", value(states, (0,1), 2, mode))
assert value(states,(0,1),2,"xor") == F(4,5)
assert value(states,(0,1),1,"single") == value(states,(0,1),2,"single") == F(9,10)
# Hypothetical literal finite-payload conditioning, NOT a claimed implementation.
particles = (("payload-A",0,F(1,2)),("payload-B",1,F(1,2)))
obs = "payload-C"
mass = sum((w for payload,y,w in particles if payload == obs),F(0))
print("unseen_payload_mass", mass, "posterior_defined", mass > 0)
assert mass == 0
# Two explicitly different future off-support policies produce different choices.
for name, posterior in (("reset", F(1,2)),("likelihood_model",F(3,4))):
    action = "A" if posterior <= F(1,2) else "B"
    print(name, "P_B", posterior, "choice", action)
print("exact_cache_accepts_unseen_payload", any(p == obs for p,y,w in particles))
```

Exact stdout:

```text
xor depth1 1/2 depth2 4/5
single depth1 9/10 depth2 9/10
unseen_payload_mass 0 posterior_defined False
reset P_B 1/2 choice A
likelihood_model P_B 3/4 choice B
exact_cache_accepts_unseen_payload False
```

Code SHA256: f617c1c68b97bb95d0b8e6f3f9536283efaddbcc8c285e91dbddf64a23fe34f4
Stdout SHA256: 8fda38ef58125ec472b3d99cf94a62a159f9d1fb499bec3e4eb3c60b6a414401

Replay without private scratch: extract the sole python block from this file, verify the above code hash, execute it using Python's compile/exec with redirected stdout, compare to the text block/hash. All source and output bytes necessary for this analytical result are public here. No EDA/learning runs were made. Full-repository validate is delegated to publication because this packet is standalone; the supplied freeze validator is the local submission check.
