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

## Decision coverage and objections

The verifier must trace every decision-critical positive claim and objection to checked evidence, including the strongest prior mechanism, engineering need, contest overlap, applicable bound and feasibility. A single checked source does not certify the dossier. Coverage and scientific entailment are semantic review duties; structural CI cannot establish them. Record unreviewed claim IDs as unresolved, and do not mark acceptance gates true while a decision-critical premise is unresolved. Scientific arguments from automated code reviewers also require file transport and adjudication before they can influence a research revision.

Search/download restrictions reduce accessible evidence; they do not establish novelty. Retain inaccessible sources in the search log and request a permitted, recorded source-access amendment if necessary. Never route around a domain restriction through a mirror or runner without authorization. Decisions about budgets, tools and thresholds must cite the human instruction or allocation file. Coordinator suggestions must be labelled suggestions, not invented owner answers.
