# EDA-0003 demand and industry-gap audit

## User and actual decision

Target user: detailed-router developer maintaining a fixed-layout pin-access engine. Decision: deploy a new solver representation only if actual full-routing latency improves at fixed correctness and downstream quality. Demand for pin access generally is established in the primary literature (P01/P02); evidence that this particular solver bottleneck is material in the allocated environment is absent. No practitioner interview was conducted. No email/message was sent. T02 validates useful latency and T05 measures the available share before candidate testing.

## Open implementations

P05 is a public BSD-3-Clause implementation containing route-conflict preparation, component analysis and incremental MiniSat solving. Exact code bytes and snapshot reference are in sources.json. Its readme limits supported rules to ISPD2018. P12 is the available pinned OpenROAD entry point; the inspected FlexPA.cpp dispatches preparation and serialization, not a full audit of its distributed implementation. P01's published local-state method must not be assumed unchanged in current OpenROAD. Neither codebase was built or benchmarked here. Third-party submodule and benchmark rights remain separate from the top-level source license.

## Commercial advertised capability

Cadence explicitly advertises instance-level pin-access planning and restriction-aware spacing (P10). Synopsys advertises routing-driven placement, manufacturing compliance and routing convergence (P11). These public statements contradict any broad claim that industry lacks pin-access awareness. They do not reveal the solver representation, conflict completeness, runtime, or whether residual state quotienting is already used internally. No matched commercial comparison or commercial feature deficit is claimed.

## Same-stage distinction and integration cost

The proposed software-only representation consumes the same candidate route graph as P05; it does not repair a missing graph extractor, produce new legal routes, move cells or change the PDK. Integration costs include export/serialization, consistent route identities, graph-key invalidation, independent checker coverage, query policy normalization, full key collision checking, memory caps, fallback accounting and deterministic witness selection. These can outweigh solver savings. A separate front-end extractor or more advanced rule support would be a new claim and cannot rescue this topic automatically.

## Practical headroom

CLM-009 bounds the benefit of changing only selection. Publicly reported short pin-access runtimes do not establish local host behavior, but they weaken the prior case that compiling another structure is valuable. No numerical end-to-end gap is measured here. The5% threshold is a proposer screening suggestion; absolute saved seconds and repeated-call workload remain unknown. P05 already reuses one SAT solver across assumption calls within a component. Artificially resetting that solver or adding thousands of duplicate calls would create false demand.

## Readiness verdict

Algorithmic novelty unresolved; candidate-specific demand unresolved; whole-flow headroom unresolved. The presently observed gap is a research-evidence/integration gap, not established missing commercial functionality. Existing GCD/Nangate45 smoke and provisional caps support neither pin-access prevalence nor a representative experiment. Full official contest evaluation invokes Innovus (P08/P09), and no license is established. Use an independently validated open rule subset only with explicit scope; do not call it official full contest or foundry signoff. All physical execution is gated by T02 and a later allocation.
