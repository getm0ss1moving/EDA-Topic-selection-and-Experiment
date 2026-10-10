# Evidence and search standard

## Source record

Every source has a stable `id`, title, URL/DOI or repository commit, source type, publication date (or `unknown`), UTC retrieval date, precise section/page/function/line locator, access level (`full`, `abstract`, `metadata`), supported claim IDs, and limitations. Record version and license/access constraints when relevant. A DOI's existence does not verify a claim. Do not cite abstract-only access as a full-method inspection.

Use original papers, supplements, official benchmark/contest rules, official winner reports, source code and reproducible experiments. Secondary summaries guide discovery and cannot alone decide novelty or impossibility. Vendor marketing supports a statement about advertised capability, not a controlled performance comparison. Label facts, inference, hypotheses and forecasts separately.

## Search protocol

Define the workflow stage and terminology first. Search primary venues and preprints, backward references, forward citations, contest archives and repository issues/commits. Record query, engine/index, date, filters, result inspected, inclusion/exclusion reason and access limits. Include classical non-AI methods, optimization theory, recent preprints, failed/negative results and closely related formulations with different vocabulary.

Maintain `prior-art.csv`: source ID, task/formulation, mechanism, data, evaluation, assumptions, limitation, overlap with proposal, and proposed distinction. Audit at least the nearest three independent approaches when they exist; a number is a minimum coverage prompt, never a certificate of exhaustiveness. Stop a search round only after two documented expansions reveal no closer mechanism, or report budget exhaustion and residual risk. Rerun novelty search before promotion and before submission; stale work is not automatically current.

## Claim and challenge discipline

Use stable IDs `CLM-001`, `OBJ-001`, `EXP-001`. A challenge identifies the exact claim, source locator, short paraphrase/quote, reasoning bridge, severity, uncertainty and a test that could refute the challenge. Distinguish refuted from unverified. Evidence that applies to another problem, node, corner, design family or cost model must explicitly justify transfer.

A verifier reopens each decision-critical original source, checks metadata and version, verifies the locator and entailment, then records `valid`, `partially_valid`, `unsupported`, `refuted`, or `unresolved`. Unavailable evidence remains unresolved; it is not fabricated as checked. Check favorable evidence as carefully as hostile evidence.

## Rights and provenance

Store bibliographic metadata, bounded excerpts, hashes and retrieval scripts rather than copyrighted full texts. Record data/design/PDK/tool licenses; do not upload restricted benchmarks, netlists or proprietary reports. Closed-source internals remain unknown unless public evidence establishes them. Record retractions, corrections, conflicts and version mismatches.
