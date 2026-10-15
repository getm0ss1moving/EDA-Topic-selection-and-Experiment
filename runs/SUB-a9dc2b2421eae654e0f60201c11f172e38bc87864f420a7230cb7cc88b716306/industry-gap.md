# Engineering need, industry context and limits

## User and decision

Timing-closure engineer deciding whether a flagged setup endpoint needs an ECO or can be cleared by full path-specific timing under declared assumptions. Output is worst endpoint slack, flags, WNS/TNS and coverage status. The metric is time to that decision; state counts are diagnostic. S11 introduction motivates avoiding over-fixing, and S04 slides 2/11 ties PBA coverage to signoff/ECO. These are primary published demand signals, not validation of our restricted fixed-load NLDM workflow or its effect threshold.

## Open implementations

S08 pins OpenSTA e01d3f163f483f233db00410b6515a767a6ca03b table code. S09 pins its API documentation; S10 is the current OpenTimer README, not a locked build. Both are potential integration aids. Neither inspected document is evidence of absent paired internals or a ready exhaustive path-slew oracle. No open baseline was built. OpenSTA distribution requires its license obligations (GPLv3/public or separate commercial terms per S18 README); third-party libraries retain their notices. No source is executed in this reading job.

## Public commercial capability

S16 official Tempus datasheet Overview/Key Features advertises integrated timing/ECO, SI, variation and concurrent-view capability. S05 and S17 are patent disclosures of staged and adaptive PBA, not evidence that an exact patented implementation is shipped or available to us. Their advertised/disclosed breadth makes a general industry feature-gap claim indefensible. No controlled comparison, current commercial runtime or internal absence is claimed. S03's receiver selection is older close disclosure.

## Comparable contract and adoption cost

Fair scientific comparison holds endpoint set, compatible suffix language, clock/required-time inputs, library/RC, contexts, arithmetic and requested outputs fixed. A pessimistic cluster result, bounded-depth path result or learned slack estimate is not the exact endpoint oracle. Commercial CCS/SI/OCV and our 2-D NLDM slice are incomparable without separate transfer evidence. A faster custom model is not faster commercial signoff.

Costs include path/context export, full-state rounding proof, independent path enumeration, graph/version invalidation, memory for pair states, replay logs and tool integration. Endpoint subsets must be chosen independently of candidate results and insufficient coverage must remain visible. No PPA improvement is inferred from a runtime hypothesis. A separate future closure study would hold ECO policy fixed and compare avoidable fixes/time at identical exact timing verdicts; it is outside current authorization.

## Unresolved practical gap

T02 must document actual time/coverage bottlenecks on licensed representative NLDM workloads and whether pair sharing survives complete tags. A source-backed general need exists; restricted-slice adoption and 20% utility threshold remain unresolved. An open-source implementation deficit or a new cache layout alone is not a research contribution. No primary source asserts that this proposed representation is missing from deployed tools.
