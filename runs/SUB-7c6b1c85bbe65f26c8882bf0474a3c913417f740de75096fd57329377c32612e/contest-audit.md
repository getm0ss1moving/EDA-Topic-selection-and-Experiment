# EDA-0003 contest and supplied-idea audit

Cutoff2026-10-15. Completing a contest task, following an organizer hint or substituting a solver is not by itself a contribution.

| Official source / edition | Inspected locator and supplied task | Overlap / implication |
|---|---|---|
| P08 ISPD2018 initial detailed routing | Abstract, Benchmarks, Evaluation Script, Contest Result, FAQ3/5/6/8 | Fixed placement/guides, pin/via rules and legal access are existing requirements. Organizers supply sample inputs, rules and evaluator. Pin-access handling is baseline work. Official1st TritonRoute,2nd Dr.CU; their later PAO/FastPass lines are central comparators. |
| P09 ISPD2019 initial detailed routing | Abstract, Evaluation Script, Final Contest Result, FAQ5/9/12/17 | More complex rules; winners Dr.CU1st, NTUidRoute2nd, Kim&Lee/TripleZ3rd. Published top-five final DEF/report files are outputs, not proof of solver internals. Full winner implementations were not all inspected. Official evaluator depends on Innovus; expired contest license notice is explicit. |
| P13 ISPD2025 performance-driven large-scale global routing | Official title/index | Different stage. It does not settle fixed-layout pin-access compilation novelty. Full winner core algorithms not audited, so no exhaustive exclusion. |
| P14 official previous-contest index | Redirected2026 page to2027 archive; lists2024 GPU/ML global routing and2026 post-placement buffering/sizing | Stage boundaries checked. The redirect is recorded rather than presented as a stable2026 rules page. Complete2026 problem/winner methods remain unread. |
| P16 ICCAD2025/2026 | Official contest problem titles |2025 incremental placement/sizing/buffering and2026 FloorSet are adjacent physical tasks, not this solver slice. A title check alone does not exclude a hidden subroutine overlap. Current2026 page schedules awards in November; no uninspected winner inferred. |

## Nearest published contest-related methods

P01 and P02 explicitly evaluate on the initial detailed-routing benchmark family; they are subsequent research papers, not interchangeable with the precise historical winner binaries. P05 is an enhanced Dr.CU implementation and contains more than a standalone SAT substitution. Preserve native code and compare exact constraints. General conflict-free selection and local pin-access analysis are not new because the dataset is old or a package is open source.

The current candidate claims no contest ranking, no score improvement, no unpublished winning approach and no permission to use a commercial evaluator. Its possible contribution would have to be a supported nontrivial state representation and meaningful whole-flow tradeoff beyond those comparators, not completion of pin access or implementation of an explicitly suggested higher-order-rule extension.

## Remaining audit work

T01 must inspect full journal2024 FastPass and older path-set branch-and-bound/flow/interval methods, current code neighborhoods and remaining winner method reports. P15's concurrent interval method is an inspected primary author PDF, but older original full methods found through P02 references have not all been reopened. No statement that the mechanism is absent from every contest/winner is supportable. The contest-originality gate remains unresolved. No input datasets, winner binaries or final DEF archives were downloaded or executed during this job.
