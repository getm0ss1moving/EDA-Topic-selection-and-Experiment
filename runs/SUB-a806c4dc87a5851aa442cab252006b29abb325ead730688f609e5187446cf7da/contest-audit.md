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


## Cycle-2 ISPD2026 correction — OBJ-002

| Record | Direct inspection / locator | Scoped conclusion |
|---|---|---|
| SRC-R24 organizer paper, 2026 | Sections 2.3 and 5.3 | Current task uses one PVT, ideal-clock setup; MCMM/post-CTS/hold belong to a prospective roadmap. No multicorner certificate method is established by that roadmap. |
| SRC-R25 official description v2.2 | Section 2, page 3; section 3.3.1, pages 5-6 | Single-mode ideal-clock setup and TNS/runtime-based evaluation. This is an optimization task, not the present all-scenario report contract. Pinned PDF hash 530fd5bbdbcf927065373c6764cc36716604043acbdaebde8ca3a35b95c153c7. |
| SRC-R26 direct official contest index | Contest Winners | IRISLab, PTSD, HLFC listed first through third. This establishes organizer-reported winners only, not their algorithms or verified performance. |
| SRC-R27 organizer repository | Commit f7b29d242fc7d441f3b4eadc556f40099ccca067; README and LICENSE | Top-level BSD-3-Clause observed. Linked benchmark/platform files and external sources require their own provenance/license audit; repository label alone is not full dataset clearance. |
| SRC-R28 mutable program and linked slides | Contest Summary/Results entry; returned slide URLs | The program page is headed 2027 but body says 2026. Its contest-results link resolved to a 2025-path 122,920,554-byte PDF that the web tool refused as too large; closing slides actually show March 2025. Exclude these links as evidence for 2026 winner methods; no access workaround attempted. |

Read-only audit decision: **exclude the unmodified ISPD2026 fixture from representative propagated-clock multicorner setup/hold readiness.** It remains a possible input lead only if extra characterized corners, CTS/parasitic generation, per-asset rights and executable cost are separately pinned in TASK-03P. No new such fixture was generated. Detailed winning implementations remain unresolved, so contest originality is not cleared. Primary official sources correct the previous coverage omission without inventing a current feature from a future roadmap.

Searches for ISPD2026 IRISLab/PTSD algorithm reports returned the direct winner list, organizer material and a mirrored contest repository, not an inspected primary winning implementation. A mutable event program and search absence cannot demonstrate no overlap. Current rules/results were inspected; method-level access remains a named TASK-01S/01D question. TAU2018/2019 complete rule/code coverage and newer contest neighborhoods also remain incomplete.
