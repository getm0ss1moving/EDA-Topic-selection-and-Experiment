# Conditional experimental protocol — no execution allocation

Status: proposer research draft for EDA-0002, batch cycle 1. No current experiment is authorized, no readiness consent is signed, and all numerical effects are hypotheses. The current turn performs source reading, prose/JSON authoring and structural validation only (SRC-P01).

## Oracle and pinned dependencies

Reference: OpenSTA e01d3f163f483f233db00410b6515a767a6ca03b, dmp_ceff_elmore, one binary/compiler/environment and one SDC mode. Source SHA-256 values for DmpCeff.cc and TableModel.cc are in sources.json. Baseline scripts must create all declared corners in a common process, load the right Liberty and SPEF for each analysis point, then export engine-internal slack identities and report statistics. An unvalidated serial process loop cannot be called strongest B0. Reproduction of this configuration is TASK-04, not a completed result.

Three distinct designs and at least three genuinely characterized scenarios are required. Existing GCD/typical is a smoke fixture, not a confirmatory dataset. TASK-03 freezes actual source/tool/design/platform commits, licenses, Liberty-header voltage/temperature/process, RC provenance, SDC/netlist/SPEF hashes, generation-script/config hashes and intended reference endpoints. Arbitrarily scaled delay tables or RCs cannot count as independent characterized corners. Freeze deterministic source/generation procedures before execution and record actual output hashes afterward. If dependencies cannot be pinned within an explicit allocation, remain unresolved or park; do not replace representative data with a favorable fixture.

## Comparators and cost boundary

B0: common-process full scenario analysis; B1: generic interval bound, sound classification and exact fallback without the proposed specialization; B2: documented anchor/clock estimate, labeled heuristic; B3: aggregate endpoint certificates to scenario-level skipping; B4: no-clock-information conservative bounds; B5: full exact analysis with the same instrumentation/report adapter; B6: strongest pinned incremental exact update after edits. P: proposed R1 certificate with exact-WNS refinement. O: oracle upper-screen diagnostic using B0 labels, excluded from deployable speedup claims. A B1 implementation that is equivalent to P is an adverse novelty result, not an unfair baseline to weaken.

Charge parsing, graph building, scenario setup, all clock and bound passes, unique refinement work, exception classification, certificate/WNS logic and final reports. Log writing must be identical or charged; correctness audit runs are separately charged to evaluation cost and cannot be silently included only in B0. Report both normal run cost and audit cost. Count all failures, timeouts, data generation, builds and tuning against total research spend. GPU/API allocation is zero. No parallelism-based novelty; equal fixed core/memory limits and randomized interleaved run order.

## Falsification sequence

1. TASK-01 resolves closest-mechanism and contest overlap; no numerical work is needed.
2. TASK-02 establishes an executable soundness specification before any production skipping: complete slew-interval CPC classification, operation-aware outward arithmetic, exception/tag/clock semantics and dependency closure. Unknowns produce exact fallback. Finite tests can falsify but never prove this specification.
3. TASK-04 reproduces full B0 reports. TASK-05 instruments a diagnostic census: eligible triples, certified triples, exception exclusions, initial refinement-union arcs, whole-net expansion, WNS-only expansion, unique work removed and phase time. Endpoint counts alone do not pass the gate.
4. Implement P only if soundness and plausible net savings survive. Compare components and B1 under equal budgets; do not count known composition as novelty without an additional useful capability.
5. Confirmatory runs and independent reproduction occur only after matching proposer/challenger consents, verifier readiness check and actual resource allocation.

Mandatory adversarial cases: reconvergent fan-in; multi-driver and off-cone loads; DMP branch thresholds across input slew intervals; negative/nonmonotone/extrapolated NLDM tables; mixed library thresholds; degenerate table axes and overflow/NaN fallback; near-zero and near-M slacks; SDC false/max/min/multicycle setup and hold paths; generated clock and shared-clock CRPR; output delays; unsupported-check fallback; scenario ranking reversal; all-positive endpoints whose exact WNS is unknown; a high-certification graph with fully shared uncertified cones. Include the inherited P3-P5 counterexamples unchanged if licenses permit their fixture reuse. No new code experiment was run in this cycle.

## Metrics and decision rules

Primary: exact D_M equality and runtime ratio R=1-T_P/T_B0; provisional target R>=0.20 on each of at least three designs. Report sign identity, maximum slack error, exact WNS/TNS differences, all certificates against B0, complete refinement set and memory. Compare bit-level values from the same internal representation if feasible; if bit identity fails, declare failure of the strict contract and investigate accumulation order, not a post-hoc 5 ps waiver. TNS sums must use the reference ordering. The brief's <=5 ps diagnostic target does not relax exactness.

Deterministic timers use paired repeated runs to estimate timing noise, not fake design replicates. A variance pilot must preregister the repetition count (minimum five; prefer ten if the actual budget permits), CI procedure, cold/warm cache policy and outlier policy before candidate timing. Randomized methods need at least five paired seeds per design. Confidence intervals are within-design uncertainty; three designs do not establish universal generalization. No threshold adjustment after observing P.

H2 requires graph-union savings and equal-budget B1/Ablation comparison; no-clock fallback may be less informative but cannot be made unsound. Edit-loop B6 is measured for ten frozen batches with all input and constraint invalidations applied. A win only from scratch must be stated as such and cannot establish closure-loop benefit.

Stop on any unsound certificate/missed violation/report mismatch (K7), equivalent known mechanism with no useful distinction (K1/K5), exclusive removable cost insufficient after overhead (K3), or unavailable representative legal data/allocation (K4). Preserve all negative outcomes. No theorem of timing saturation is asserted. Follow tasklist.md for exact owners, prerequisites and outputs.
