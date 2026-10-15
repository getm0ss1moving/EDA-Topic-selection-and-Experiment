# EDA-0003 experiment plan — conditional, not authorized

## Hypotheses and endpoint

CLM-010/H1 and CLM-008/009 in proposal.md are preregistration candidates. H0 includes generic-CSP equivalence, tiny native solving share, state explosion and geometry mismatch. Primary deployment endpoint is elapsed time from loaded fixed routing database to complete detailed-route output, including candidate/conflict generation, compilation, queries, fallbacks and all routing/validation. Report cold-start and single-invocation costs; any observed repeated-analysis workload is reported separately with its actual query count. No manually repeated queries count as demand.

A proposed 5% paired total-time reduction is only an initial screen. T02 must establish a useful absolute saved latency and confirm/fix this threshold before results. Full extracted WNS/TNS/hold, rule violations, connected pins, route geometry and flow failure rate are guardrails. This is a runtime topic; a pin-access time improvement or HPWL reduction alone cannot pass. The project D04 WNS default is recorded as a different provisional screen, not misreported as met.

## Arms and equality contract

N: unmodified P05 native FastPass, exact code snapshot recorded in sources.json.
B1: same FastPass candidate/conflict generator, incremental SAT on exported masks, common canonical final witness.
B2: generic exact variable elimination with fixed min-fill order and ordinary assignment states on the same finite graph, no geometry-specific quotient.
M: residual forbidden-domain quotient as precisely defined in proposal.md.
A: M without merging distinct assignment-frontier states whose future forbidden profiles coincide; same transitions/order/caps/oracle.

N is source-faithful deployment reference; it is not slowed artificially to provide a favorable comparator. B1/B2/M/A share complete candidate route identities, pair constraints, masks and canonical witness. Canonicalization is lexicographically first feasible route choice by fixed(pinID,routeID) order, implemented through successive feasibility decisions; every arm pays its own cost. FastPass's actual core-relaxation query sequence is captured before candidates are tested and supplied identically in diagnostic replay; its capture cost is charged once per actual invocation, and replay results cannot claim native-flow speedup. For a deployment integration, preserve the native outer enable policy with an explicit solver-independent tie/core-selection contract or fall back; do not assert that two solvers produce identical UNSAT cores. An absence of such a contract is a T04 stop, not an assumption of equivalence.

Comparison against generic B2 is decisive for nontriviality. If the only difference is hash-consing already present in standard decision-diagram compilation, report equivalence and stop the novelty claim. A speedup over PAO alone does not pass. Components trivial for native code retain their trivial path in every fair arm.

## Correctness

1. Compare full SAT/UNSAT tables to brute force on all graphs up to the predeclared bounded size, and randomized larger instances with a pinned generator only after allocation. Include empty domains, disconnected components coupled by same-pin choice, long-range conflicts, identical profiles, distinct profiles with equal recent history, mask relaxation, changed graph invalidation, intentional hash collisions, duplicate routes and cap exhaustion.
2. Compare B1/B2/M/A feasibility and canonical witnesses on **identical** graphs, not separately generated candidate sets. FastPass's at-least-one to exactly-one deletion equivalence is restricted to negative conflict constraints. Positive/connectivity/union-shape constraints invalidate that reduction.
3. Independent geometry checking must confirm emitted escape metals and fixed geometry, then full routing and independent connectivity/DRC on complete outputs. Shared checker agreement is insufficient to certify the extractor itself. Any omitted rule is listed by LEF type; no unsupported rule class becomes DRC-clean by declaration.
4. UNKNOWN/timeouts are censored failures with full cost. Never output UNSAT from a state/memory cap. Candidate fallback uses the same exact SAT reference, and wasted compilation is included.

## Data, licensing and splits

P08 ISPD2018 is the initially matched rule family for P05. Plan source-selected test1/test5/test10 for small/medium/larger opportunity strata, before any runtime outcomes; treat test7–10's related design family as correlated, not independent designs. This is an explicit weakness: three independently selected design families required for confirmatory claims are **not yet locked**. T02 must find, license and pin three separate families with meaningful pin-access workload; otherwise the plan remains ineligible for confirmation. Do not substitute three perturbations of one netlist.

ISPD2019 is external stress only after rule/oracle support is established. P05 README says its supported rules are ISPD2018; do not claim 2019 support from the presence of an evaluation directory. ASAP7 is a possible future public technology reading lead, not an acquired representative benchmark, foundry process or new allocation. GCD/Nangate45 is only a build fixture. Benchmark/LEF/DEF/SDC notices and download hashes, technology rules, tool/compiler versions and extraction corners need a lock before execution. No paper PDFs or restricted data enter the release.

## Cost, statistics and conditional commands

Current authorized experiment spend is zero: no run occurs in this batch. A possible later request would be bounded by the historical provisional8 CPU-hour,4 GiB,2 CPU/job envelope; it is not permission. Proposed decomposition is0.25 h model tests,0.75 h native reproduction/build smoke,1 h instrumentation/opportunity census,0.5 h integration parity, at most5.5 h paired physical tests. Five arms ×3 designs ×5 paired runs =75 complete runs. To fit the last envelope, mean **CPU** cost must be <=264 s/run inclusive of oracles, not264 s wall time on two CPUs. If it does not fit, stop and re-plan before results; never omit slow cases or uncharge build/search. Instrumentation/export, failed builds and rejected runs consume the cap. Public papers' reported machine timings are not estimates for this host.

Algorithms are deterministic on fixed inputs. Five repetitions measure timing noise; they are not five independent designs. If routing uses a genuine seed-bearing code path, pin and trace it before calling repetitions paired seeds. Use paired randomized execution order fixed before candidate outcomes, identical thread/affinity/memory/cold-cache policy, median and distribution of full latency, per-design ratios and bootstrap intervals only with the design-family clustering made explicit. With three families confidence is limited; no universal significance claim. Stop at the bounded pilot; confirmatory sample size and workloads need a separate allocation and preregistration informed by baseline variance.

Reproduction starts with the actual upstream commands in P05 README: `scripts/build.py -o release`, and its documented runner/evaluation examples. The local candidate, graph-export shim and normalized outer policy **do not exist yet**. T04 must deliver them, their hashes and exact CLI/config files before any task list can be signed. No invented `cepa` executable or successful build is claimed. Future procedure: pin the source snapshot and license; create an exporter around Helper::solveInstanceSAT; export domains/conflicts/masks/geometry IDs; implement independent reference and candidate; validate parity; benchmark only through the allocated runner. Full-repository validation remains the coordinator's publication duty; own trusted freeze is the available standalone structural check.

## Failure and stopping policy

T01 novelty failure stops engineering advancement. T02 invalid demand/insufficient families or missing oracle/license stops physical testing. T03 soundness mismatch stops all benefit claims. T05 bound S/T below the agreed threshold stops this solver-only latency direction. T06 no advantage over B2 or state-cap incidence dominating useful cases stops the structural claim; do not rename a hybrid as a rescue. T07 requires the stronger native/control reference to be beaten on full flow without correctness/timing regressions; otherwise report a negative result. Every change in scope, data, query policy, caps or tasklist invalidates prospective consents and requires a new immutable revision. No consent is present now.
