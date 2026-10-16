# Output-field to reader to engineering-decision map

Bounded current source walk R18: OpenROAD commit3549d60529517dc82deb7f0ff769345e9a424911; exact raw one-based locators below. This is an interface/caller audit, not whole-program reachability or a workload census.

| Promised/observed field | Producer | Actual reader and decision | What is established |
|---|---|---|---|
| Candidate legal flag | MeasuredVtSwapCandidate.cc46-47,54-56,63-66 | MeasuredVtSwapPolicy.cc274-276 skips illegal candidates | Explicit scalar legality; cap rejection and replace failure collapse to legal=false/score=0 in this interface. Not a complete violation/failure identity vector. |
| Arrival improvement score | Candidate.cc53,60,63;arrivalDelay109-116 | Policy.cc278-281 strict greater-than chooses best legal score | Per-candidate scalar arrival difference; not endpoint setup slack/WNS/TNS vector. Strict comparison retains first current best on equal score under this loop, not a universal tie policy. |
| Chosen applied edit | Candidate.cc69-101;Policy.cc288-295 | Commit acceptance, timing update and pending-move acceptance | Concrete commit path; no full-output consumer follows from it. |
| Restored base | Candidate.cc119-132 journal/undo/update | Next candidate estimate uses live state | Required correctness precondition; no published restore hash/test in this source walk. |
| Full endpoint setup-slack vector per candidate | Not a member of Estimate in OptimizerTypes.hh356-360 | No reader in audited type/candidate/policy path | Anchored demand NOT established. Other public consumers could exist. |
| Full pin slew/cap/violation/failure vector per candidate | Same type356-360 contains only legal,score | No reader in this bounded path | Internal updates/one cap guard do not establish full output demand. |

OptimizerTypes.hh391-399 additionally stores candidate/Estimate lists and best pointers for TargetEvaluation; it still supplies no missing full-vector field. Candidate.hh16-24 describes the measured swap as single-threaded live-STA work; comments are implementation intent, not independent performance measurements.

The anchored timing-engine developer remains the user. A legitimate natural full-output reader may support debug/regression/counterfactual decision auditing, but that is presently a hypothesis, not discovered demand. S2 must provide existing reader call sites or a documented research workflow, actual fields, candidate enumeration, decision consequences, failure handling and retention/materialization needs. A newly invented benchmark requirement or signature alone is insufficient. If only scalar selection is found, park this topic or use a separately governed new ID; do not rewrite the current contract to match a convenient caller.

No industrial exclusivity, commercial deficiency or matched runtime gap is claimed. Historical vendor R13/R14 claims are advertised capabilities only and were not reopened in this job. Generic memory/recomputation and variational representation are prior; a useful contribution must improve the actual complete consumer endpoint over equally informed specialized conventional execution. Current A03 has no Q-only storage gain and charges support creation. Natural multiplicity, maintenance cost, fallback, output/restore floor and total economics remain unmeasured.
