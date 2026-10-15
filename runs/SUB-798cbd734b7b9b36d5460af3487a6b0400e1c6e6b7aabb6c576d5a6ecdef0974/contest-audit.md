# Bounded contest originality audit

Research cutoff: 2026-10-15 UTC. CLM-035 is limited to the materials below.

| Official source | Inspected content and overlap | Missing evidence |
|---|---|---|
| TAU 2018, SRC-R12 | Topic: efficient timing-report generation after arrival/required-time updates. Report caching/search is adjacent and not novel by itself. | Detailed rules, complete winners and code not read. |
| TAU 2019, SRC-R13 | Design optimization and incremental/multithreaded engines; resource page lists rules v1.7 and team reports. | Full rule PDF, dataset license and implementation files remain unchecked. |
| iTimer, SRC-R14, slides 2/5/10 | Multicorner input; worst-corner-driven optimization; hold fixing iterates corners. | No certificate or output-equivalence conclusion can be inferred from slides alone. |
| TimeBoost, SRC-R15, slides 5-6 | Iterative optimization explicitly uses incremental timing updates. | Code and entire performance methodology not reproduced. |
| ParallelClosure, SRC-R16, slides 2/6/14-16 | MCMM optimization, per-corner slew targets and parallel graph processing. | Implementation and fairness not independently reproduced. |
| ICCAD 2025, SRC-R17 | Overview: Trojan detection, multibit-flop power/timing optimization, incremental placement optimization. | Detailed hints, complete final solutions and winner reports not exhausted. |
| ICCAD 2026, SRC-R18 | Overview: LLM netlist transformation, regression-failure bucketing and FloorSet. November ceremony is later than cutoff. | No future winners claimed; detailed subproblems remain unreviewed. |

The inherited uncertainty about TAU 2018/2019 high-level topics is reduced by fresh organizer and team sources. This does not certify that no contest has supplied the proposed mechanism. Reimplementing an organizer task, worst-corner selection, graph caching, parallel timing or a published team algorithm is not a research contribution. TASK-01 must compare any bound/refinement hint found in full rules and winning code to the exact report contract. Contest overlap remains unresolved until that check is complete.
