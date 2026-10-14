# Independent estimate before dossier release

Actor/session: Codex-C05-TIMING-R2 / /root/codex_c05_timing_r2. Input commit: 27977cb365dab9b3df5193fcd0c2e23804f840cf. Forecast exposure: none observed. Independence is qualified by ambient inherited workspace instructions and lack of hard sandbox; see readiness.json.

## Estimate

Numerical speedup, screening fraction, memory reduction, correctness failure rate, novelty and practical headroom: **unknown**. No benchmark data, target timing semantics, scenario distribution, baseline configuration or engineering threshold has been released. No numerical range is invented.

Observation: S01 supplies model-specific pruning semantics; S02 supplies an abstract-level bounded-search family; S05 documents an incremental baseline. These do not imply saturation of a different target model. S04 is only a prediction-method lead, not evidence of a safe elimination guarantee.

Hypothesis, not forecast: positive headroom is plausible when inexpensive conservative certificates eliminate sufficient exact work and remain valid after design changes. No improvement, or a slowdown, is equally plausible when bounds are loose, certificates are expensive, or most cases need refinement. This is conditional cost reasoning rather than a measured industry gap.

Assumed accounting identity for a future comparison: total screened-flow cost equals preprocessing plus certificate construction plus screening plus exact refinement plus update maintenance. Benefit requires this total to be lower than a matched exact baseline at identical outputs and tolerances. This identity provides no numerical bound or performance prediction.

## Proposed falsification priorities — not executed

1. Freeze which result is preserved: worst delay, endpoint slack, violating scenarios, or all reports. An exact oracle must use identical constraints, libraries, parasitics and timing features.
2. Audit every discard certificate and every unresolved case sent to exact refinement. Ranking prediction alone is not the proposed acceptance rule.
3. Include cross-scenario ranking changes, near-boundary cases, setup/hold semantics, clock effects and invalidation after edits where present in the frozen target model.
4. Compare exhaustive exact execution, incremental exact execution, naive screening plus fallback, and the nearest applicable certified method with equal resource accounting.
5. Report end-to-end costs and residual false exclusions; choose thresholds with the owner before execution.

No topic-specific objection or conclusion follows from these priorities. Dossier-specific estimates must wait for a screened frozen dossier; independence cannot be retroactively strengthened by this artifact.
