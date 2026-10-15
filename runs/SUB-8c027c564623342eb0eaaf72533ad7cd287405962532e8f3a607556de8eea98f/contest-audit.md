# Current contest audit, cutoff 2026-10-15 UTC

## Newer rules repaired from released OBJ-002

R10: organizer repository commit faef83cacf70fa7923be07816d804ca9c1cef68e, README and ISPD27-Contest-Description.pdf. README links a public description and gives registration opening October5,2026. The official ISPD2027 contests page links this repository. Description text was actually downloaded via the ordinary public raw URL and extracted with pdftotext after the web PDF reader failed. No authentication or access-control bypass occurred. This corrects a parser/access gap; it does not produce benchmark results.

Description physical pages2–3 §2 specifies allowed transformations and fixed clock-tree constraints; pages4–5 §3.1 specifies initial functional BC/TC/WC scenarios and propagated setup/hold; §3.3.1 starts physical page5 with provisional scoring. A later scan mode is stated as future work. These broader conditions do not apply automatically to the proposal's ideal-clock single-scenario slice.

R11: evaluator README raw lines3–8,78–104,131–190; evaluation.tcl raw145–170 and245–267; metrics.py summarize; score.py validate_config; scoring_config.json status/weights/scenarios. Documentation/code provide reference mechanisms and multiple quality/runtime terms. Weights are explicitly provisional. Selected code was read as data, never imported or executed. Root LICENSE was read but benchmark/platform rights still require a per-file license audit. Sponsor resources are not an owner allocation.

No organizer statement in the inspected material establishes this physical-covariance selection recipe as supplied or absent. Implementing the supplied reference flow or contest transformations would not establish novelty. Compare the existing reference and current calibrated analytical alternatives under matched scope/cost if future resources permit.

## Prior edition and winners

R12: official 2026 contest page identifies IRISLab, PTSD and HLFC as first/second/third. The pinned 2026 README f7b29d242fc7d441f3b4eadc556f40099ccca067 supplies context, not an algorithm audit. Independent winner/name/technique searches did not locate an authenticated current winner algorithm report. An unofficial solution repository was a discovery hit and was not adopted as winner authority. Therefore winner-method novelty remains unresolved, not cleared.

The 2026 program request redirects to a 2027 URL displaying a 2026 contest session. Its linked contest-summary slide fetch failed. Another closing-slides link resolves to a 2025 deck: inspected metadata, excluded from 2026 winner evidence. No false report identity or algorithm was inferred. EXP-001 retains exact official winner/report provenance as a source task; no messages were sent to authors.

R09 compares its own sizing work to ICCAD2025 flows, a different contest. Its library-direction and calibration methods matter as primary prior art; its reported numerical gains/hardware are not our measurements and are not transposed into 2026/2027 winner claims.

## Locator convention

All raw GitHub line ranges here are 1-based physical newline counts in downloaded pinned bytes, including comments/blanks. Search-tool rendered lines may merge or omit lines and are not interchangeable. PDF references mean 1-based physical pages split by form-feed after pdftotext -layout; original section titles/equation numbers are preferred. The description was text-read, not visually inspected for figures. Hashes and access limitations appear in sources.json. No paper/PDF/netlist/PDK copy is included in the public release.
