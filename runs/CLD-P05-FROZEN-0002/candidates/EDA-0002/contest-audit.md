# Contest Audit

## Contest identity, year, and official rules

Among the contest records inspected, none has scenario reduction or screening for multi-corner STA with decision equivalence as its topic. This is a statement about the records checked, not a claim that no relevant contest exists. The table shows what was checked. Access levels follow `sources.json`.

| Contest | Topic | Evidence | Access |
|---|---|---|---|
| TAU 2013 | Variation-aware parametric timing analysis; parallelism encouraged | SRC-039 | Search metadata |
| TAU 2014 | Common path pessimism removal (CPPR) | SRC-039 | Search metadata |
| TAU 2015 | Incremental timing and incremental CPPR. Winners: iTimerC 2.0, UI-Timer 2.0, iitRACE | SRC-037, SRC-047 | Search metadata |
| TAU 2016 | Timing macro-modeling (hierarchical timing with black-box/gray-box models) | SRC-038 | Page fetched |
| TAU 2017 | Timing macro modeling | SRC-039 | Search metadata |
| TAU 2018 | Timing reports from an STA graph: top-N critical paths with from/through/to, graph-based analysis only | SRC-059 (GitHub, topic level), corroborated by SRC-053 and SRC-054 | Topic level; rules unread |
| TAU 2019 | Timing-driven optimization: buffer insertion, deletion and sizing, scored by timing, power and area | SRC-059 (GitHub, topic level), corroborated by SRC-055 and SRC-056 | Topic level; rules unread |
| TAU 2020, TAU 2021 | Delay calculation (2020 winner: current-source-model delay calculator) | SRC-039 | Search metadata |
| ICCAD CAD Contest 2014, 2015 | Incremental timing-driven placement (2015 provided OpenTimer as the timer) | SRC-040 | Search metadata |
| ICCAD CAD Contest 2018 | Timing-aware fill insertion | SRC-040 | Search metadata |
| ICCAD CAD Contest 2025 | Power and timing optimization using multibit flip-flops | SRC-040 | Search metadata |
| 2011 IC/CAD contest (Taiwan) | A3: multi-core (parallel) STA, not multi-corner | SRC-040 | Search metadata |

Official rule documents were not read for any of these contests. The table reflects topics, not rules.

## Provided ideas, hints, baselines, and constraints

- **Closest contest, TAU 2013.** It provided a *parametric* (variation-aware) timing formulation. Linear parametric delay forms, as used in SRC-013 and SRC-014, are therefore baseline knowledge. The proposal does not claim parametric timing as its contribution. It explicitly avoids a parametric model and compares against the parametric approaches as nearest work (`proposal.md` § Closest prior work).
- **TAU 2015.** Incremental timing and lazy propagation are baseline knowledge. They were used only to exclude slice S1 (`search-log.md` § Excluded results).
- **TAU 2016-2017.** Macro modeling is not used.

## Winner methods and public implementations

- **TAU 2015:** iTimerC 2.0 (lazy evaluation and propagation; SRC-047), and OpenTimer (SRC-048) as a public implementation in the contest lineage. Neither is a component of this candidate.
- **TAU 2013:** winner methods were not retrieved. Doing so is a follow-up task for the challenger or verifier, since parametric all-corner ideas are adjacent to SRC-012 and SRC-013.

## Unfinished tasks versus new research contribution

- [INF] This candidate does not implement a supplied contest baseline, an organizer hint, a known winner approach, or an unfinished contest task (`docs/CHARTER.md` line 13).
- The closest contest-provided idea is parametric corner coverage (TAU 2013). The proposal treats it as prior knowledge and makes a different claim: decision equivalence by construction, using per-scenario table-level bounds plus exact refinement.
- Round 1 (owner item U8): GitHub and arXiv were searched for primary records of TAU 2018 and 2019. The OpenTimer repository README (SRC-059), written by the contest golden timer's authors, names both topics. Neither topic is multi-corner screening. The topic pages and summary slides read in ADD-0001 (SRC-053 to SRC-056) agree.
- If the unread rules or winner reports show multi-corner screening, this audit must be revised before promotion.

## Evidence and unresolved access

**Unresolved**:

1. The TAU 2018 and 2019 rules, file formats and winner reports. The topics are known at topic level only. The round-0 statement that the pages sit behind a login wall was inaccurate (ADD-0001 erratum E4).
2. The TAU 2013 winner reports and the parametric formulation details.
3. The official rule PDFs for the TAU and ICCAD contests listed.

All three are listed as open items in `proposal.md` (U8) and in the `search-log.md` refresh plan.
