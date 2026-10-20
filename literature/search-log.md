# Batch 001 discovery and access

Date: 2026-10-16. Coordinator-curated first literature batch; no independent
scientific review or fresh research-role session is claimed.

Search engine: web search. Queries used:

- site.arxiv.org 2026 physical design placement clock tree synthesis routing timing prediction EDA
- site.arxiv.org 2025 2026 static timing analysis timing optimization learning OpenROAD
- site.ispd.cc contests 26 2026 placement routing sizing
- site.arxiv.org 2026 placement routing "physical design" "agent"
- site.arxiv.org 2026 "routing" "VLSI"
- site.arxiv.org 2026 "static timing" "prediction"
- site.arxiv.org "PDAGENT-BENCH"
- site.arxiv.org "AlphaRoute" "Semantic"
- site.arxiv.org 2026 "IR drop" prediction
- site.arxiv.org 2026 "timing" "physical design" prediction
- "Hybrid ML for Lightweight Pre-Route" arxiv

Included primary arXiv/publisher entries are in catalog.json with exact inspected
versions and locators. Secondary search hits were discovery leads only and do not
support verdicts. Papers were selected for stage/method relevance and recent
availability, not by citation count or inferred quality. Current versions were
checked for PDAgent (v7), expert placement (v2) and LMM-IR (v2). Remaining v1
entries identify the inspected version without claiming no later version exists.

PDAgent v7 changed the title/author list and supplies a repository link; the old
search-index abstract saying code will open soon is superseded for this card.
LMM-IR remains one paper despite 2025 conference / 2026 arXiv update chronology.
ELBAGNN publisher abstract and a short method paragraph were visible; full-method
review and exact first-publication date are not claimed.

Access gaps/exclusions: IEEE DOI landing pages for multi-corner timing
10.1109/TCAD.2025.3646591 and MIMIC 10.1109/ASP-DAC66049.2026.11420406 returned
limited content; keep as discovery leads, excluded from this first ten. An attempted
ISPD25 repository URL returned 404; it is not evidence that the contest is absent.
The official ISPD archive identifies the 2025/2026 task names; only the 2026
organizer README was inspected in this batch. Hardware reverse-engineering clock
recovery was outside the current chip-design-method survey and was excluded.
A direct local urllib metadata fetch timed out at TLS; primary browser results,
not that failed fetch, support this catalog. No local paper download is claimed.

No full papers or tools were downloaded/run. No EDA experiments, paid resources,
novelty verdicts, human consents or independent scientific approvals were created.
Stop after ten; do not silently claim the remaining ninety are completed.


# Batch 002 discovery and access

Date: 2026-10-20. Ten additional papers, nine additional contest/project/module
entries. Coordinator-curated literature screening in the current session; no fresh
independent scientific actor or verifier is claimed. Existing batch001 records are
preserved. This batch stops at LIT-020, not at 100 completed papers.

Search engine: web search; follow-up primary GitHub REST retrieval through gh.
Query groups used (no exhaustive-search claim):

- site.arxiv.org 2026 "parasitic" "extraction" interconnect
- site.arxiv.org 2026 2025 "static timing analysis" GPU
- site.arxiv.org 2026 "electromigration" "IR" design
- site.arxiv.org 2026 "design rule" "layout" prediction
- site.arxiv.org electromigration 2025 2026 power grid physics informed
- site.arxiv.org 2026 "dynamic IR" prediction
- "Rule2DRC" paper github
- ICCAD 2026 CAD contest problems official
- "FloorSet" paper arxiv
- "Physical-Aware Multicorner Timing Prediction" IEEE "2025"
- "iRCX" "7135149" "10.2139"
- "iRCX" extraction github Yipei Xu Qing He
- "end-to-end" "parasitic extraction" arxiv 2025 2026
- site.ispd.cc 2025 "contest" "Performance"

Included papers were opened at their primary arXiv/SSRN/IEEE entries. Exact
inspected versions and locators are in catalog.json. Rational Krylov v2 was read
instead of counting v1 and v2 separately. Warp-STAR's linked conference DOI is an
alias, not another paper. Primary indexed SSRN/IEEE abstract text was readable for
iRCX/multicorner timing, while direct landing-page access was limited; neither is
a full-method read. No venue acceptance is inferred for SSRN or unlabeled
preprints. Title Open-Source does not verify an available code artifact.

The official ISPD2025 archive resolved the bad guessed repository URL from
batch001 to liangrj2014/ISPD25_contest. Official ICCAD pages identify Problem C,
submission closure and linked FloorSet repository. The original FloorSet paper
2405.05480 was consulted as a dataset/formulation lead and was not added as an
eleventh selected paper; the 2026 contest's relaxed protocol is distinct. Contest
winner implementations were not audited. ICCAD Problem A (netlist transformation)
and B (regression bucketing) were not prioritized for this backend-focused batch.
CADathlon problem statements are scheduled for November 1 and were not inspected.

Primary implementation checks: Rule2DRC eval_problem compilation/category-label
logic; FloorSet contest README hard/soft constraints, scoring and RuntimeFactor
policy; Trinity README and docs/evaluation.md raw/refined/legalized metrics and
refiner-only comparison; canonical OpenSTA README/license; OpenRCX command and
calibration docs; KLayout license and Netgen README. Full public text files were
retrieved to private scratch for inspection, never executed. The provenance run
contains source commit URLs, SHA-256/byte counts and failed retrievals, not copies
of those documents or copyrighted full papers.

Access gaps: iRCX code/license not verified; HeteroSTA binary/shared-library
availability not converted to a source-release claim; IEEE full text unavailable;
Netgen guessed COPYRIGHT path returned 404 and exact license remains unresolved.
Paper full texts, datasets, model weights, private PDKs, licensed tool runtimes and
advanced-node cases were not downloaded or executed. No paid API/training/EDA run,
new topic proposal, forecast measurement, approval or independent scientific verdict.
