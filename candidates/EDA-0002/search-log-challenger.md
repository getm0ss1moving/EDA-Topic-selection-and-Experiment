# Challenger search log

**Actor:** `DeepSeek-C05-TIMING` (challenger, D05, EDA-0002). **Packet:** `e6c53f61…5332cf`, commit `4b666c04…`.
**Round:** 1 (began 2026-10-13 on direct human instruction). **Records written:** 2026-10-13T11:23Z.
**Scope of this log:** retrieval routes, queries, access failures and fidelity notes for everything I read. Objections and findings live in `challenges.md` and `findings-challenger.md`; source records in `sources-challenger.json`.

## Tool and access situation in this session (material to how my evidence must be judged)

| Channel | State | Consequence |
|---|---|---|
| Shell (`curl`) network | Fully filtered. Every host probed was denied at the proxy (`web.archive.org`, `www.eecg.utoronto.ca`, `eecg.toronto.edu`, `arxiv.org`, `ieeexplore.ieee.org`, `dl.acm.org`, `github.com`, `raw.githubusercontent.com`, `r.jina.ai`, `api.{crossref,openalex,semanticscholar}.org`, `scholar.archive.org`, `core.ac.uk`, `citeseerx.ist.psu.edu`, `www.tauworkshop.com`). | No local downloads, therefore no local hashing of upstream artifacts and no local PDF text extraction in this round. |
| Harness `WebFetch` | Works, including for the author-hosted PDF of SRC-012. | This is my retrieval channel of record for text sources. |
| Harness `WebSearch` | Works. | Discovery channel. |
| Files saved by `WebFetch` | Written by the harness into a session directory that my own permission settings deny me. | I cannot post-process fetched PDFs locally; text must come from an extraction service. Fidelity caveat recorded per source. |

**Fidelity rule I apply:** where a source was read through a third-party text-extraction service, I record that route explicitly, restrict myself to short bounded quotes, cite by section/table rather than by page image, and flag that exact character-level wording remains for the verifier to confirm against the original.

## Retrieval and query record

| # | UTC (approx.) | Channel | Target / query | Result |
|---|---|---|---|---|
| R-C01 | 2026-10-12 ~18:39Z | curl | `https://www.eecg.utoronto.ca/~najm/papers/dac11-sari.pdf` (SRC-012) | Denied at proxy (`deny network-outbound`). |
| R-C02 | 2026-10-12 ~18:40Z | curl | `archive.org` Wayback availability API for the same PDF | HTTP 429 from the archive endpoint; web.archive.org itself denied on both 80 and 443. |
| R-C03 | 2026-10-12 ~20:20Z | WebFetch | `https://www.eecg.utoronto.ca/~najm/papers/dac11-sari.pdf` | **Success**: 277.8 KB PDF retrieved; the fetch tool's own converter could not decode the Flate-compressed text layer. Direct PDF text extraction is not available in this session. |
| R-C04 | 2026-10-12 ~20:21Z | WebFetch | `https://www.aspdac.com/aspdac2010/Archive_Folder/pdf/8B-2.pdf` (SRC-014, control test) | Same structural failure: raw PDF bytes, no text extraction. Confirms a general PDF limitation, not a property of SRC-012. |
| Q-C01 | 2026-10-12 ~20:2xZ | WebSearch | `"A Fast Approach for Static Timing Analysis Covering All PVT Corners" Onaissi Najm DAC 2011 pdf` | Kept: venue/DOI/page metadata and the public abstract (see `sources-challenger.json` C-A03/C-A05). No open-access copy of record found on that pass. |
| R-C05 | 2026-10-12 ~20:3xZ | WebFetch | `https://r.jina.ai/https://www.eecg.utoronto.ca/~najm/papers/dac11-sari.pdf` | **Success**: full text of the author-hosted PDF extracted and returned by the extractor. Used for four targeted question passes (setup/dominance definitions; hold method; exactness-language audit; verbatim anchors + experimental setup). |
| R-C06 | 2026-10-12 ~20:4xZ | WebFetch | `https://dl.acm.org/doi/abs/10.1145/2024724.2024899` | HTTP 403. Publisher route unavailable; recorded, not bypassed. |
| R-C07 | 2026-10-12 ~20:4xZ | WebFetch | `https://ieeexplore.ieee.org/document/5981998` | Empty document returned (the proposer saw the same behaviour for a different IEEE record, SRC-024). Recorded. |

## What SRC-012 gave me (headline)

Full-text-level read of the DAC 2011 paper, including the definitions in §2.2, the setup-coverage results in §5.1, the hold anchor/partial-corner method in §6 with its error equation and conservatism statistics, and the conclusion in §7. The kill-criterion K1 assessment built on this read is in `findings-challenger.md` (F-1). Headline: **SRC-012 does not contain per-scenario sound certification with exact refinement**; it is an empirical/estimation method with documented margins and misses.

## Continued record (same round, later in the window)

| # | UTC (approx.) | Channel | Target / query | Result |
|---|---|---|---|---|
| Q-C02 | 2026-10-13 ~11:0xZ | WebSearch | `"A linear-time approach for static timing analysis covering all process corners" Onaissi Najm TCAD 2008 pdf` | Kept: venue metadata (ICCAD 2006 pp. 217-224; TCAD 27(7):1291-1304, DOI 10.1109/TCAD.2008.923635) and the abstract; located an open M.A.Sc. thesis version at the University of Toronto repository (scholaris item af017b56-...). |
| R-C08 | 2026-10-13 ~11:0xZ | WebFetch | `https://utoronto.scholaris.ca/items/af017b56-8be8-41df-af6f-d511840d41bd/full` | HTTP 500. Not pursued further because the author-hosted TCAD PDF route was available. |
| R-C09 | 2026-10-13 ~11:1xZ | WebFetch | `https://r.jina.ai/https://www.eecg.utoronto.ca/~najm/papers/tcad08-sari.pdf` | **Success**: full text of SRC-013 (record C-A06). |
| Q-C03 | 2026-10-13 ~11:1xZ | WebSearch | `multi-corner static timing analysis provably safe corner reduction guarantee zero missed violations exact refinement 2024 2025` | Kept as leads: US12675622B1 (already the proposer's SRC-017), FACT (MLCAD 2024 / IEEE 10740197), an NTHU 2025 deep-learning multi-corner prediction thesis (Taiwanese-language literature the proposer had not searched), and a Chinese-language MMMC corner-pruning article. |
| Q-C04 | 2026-10-13 ~11:2xZ | WebSearch | `"corner dominance" monotonicity Liberty library proof safe corner pruning signoff methodology primary source` | Kept: the same MMMC article; Tetelbaum's "Design for Variability and Signoff Tips" (Feb 2014, Abelite); Siemens/Solido white paper noting non-monotonic `.lib` data is a common undetected characterization defect; anysilicon "Signoff Tips" material on sub-path structure. |
| R-C10 | 2026-10-13 ~11:2xZ | WebFetch | `https://geek-doc.cn/eda/corner-pruning-mmmc-reduction` (direct) | Navigation shell only; article body not in the first 100k characters. |
| R-C11 | 2026-10-13 ~11:3xZ | WebFetch | `https://r.jina.ai/https://anysilicon.com/wp-content/uploads/2014/10/Signoff_Tips_paper_Feb_2014a.pdf` | **Success**: full text (record C-A07). |
| R-C12 | 2026-10-13 ~11:3xZ | WebFetch | `https://r.jina.ai/https://geek-doc.cn/eda/corner-pruning-mmmc-reduction` | **Success**: article body (record C-A08). Secondary source; treated as a lead only. |
| R-C13 | 2026-10-13 ~11:4xZ | WebFetch | Semantic Scholar graph API citations endpoint for SRC-012 | **Success**: 23 citing works (record C-A09). This closes part of the proposer's forward-citation gap (their session had HTTP 429). |

## Access-route notes for the verifier

- All publisher PDF reads earlier in the round went through the extraction proxy route of C-A02. No publisher route worked (ACM 403; IEEE empty; UofT repository 500). ACM/IEEE remain closed; they were not retried.

**Correction (same round, later window).** The statement that "upstream file hashes could not be recomputed" is **withdrawn**. Two capabilities were found in this session that were not visible earlier:

1. **Shell egress works when the host is named in the command's `allowed_domains`.** With that, `curl` retrieved `raw.githubusercontent.com` and `codeload.github.com` files, the author-hosted PDFs, both TAU contest decks, the UCI DAC-1995 PDF, and the full pinned OpenSTA tree. All eight proposer-recorded code hashes were recomputed and **match** (C-A13); all five downloaded PDFs hash-match the human's `PROVENANCE.md` (C-A10, C-A11, C-A12, C-A14). The human's local copies, the upstream files, and my reads are byte-identical.
2. **Local PDF text extraction is possible without system tools.** A dependency-free extractor was written for this session (Flate + PDF-LZW + TJ-kerning spacing) and used on every PDF above, replacing third-party extraction for these documents. Residual caveat: ligatures/symbols can drop and spacing can shift; wording was cross-checked across occurrences.

Two sandbox quirks that cost time, recorded so the verifier can reproduce: `$TMPDIR` (`/tmp/claude-501`) is writable but **read-denied**, so scratch files must go to `/tmp/claude/...`; and a Python process's stdout is silently dropped unless piped (for example `python3 … | head`).

| # | UTC (approx.) | Channel | Target | Result |
|---|---|---|---|---|
| R-C14 | 2026-10-13 ~11:35Z | curl | `tauworkshop.com/2019/slides/TAU 2019 Contest.pdf`, `…/2018/slides/TAU18_Contest.pdf` | Success; hashes equal PROVENANCE.md (`5df07bbd…`, `f043f706…`). Deck directory listings also retrieved (via the extraction proxy) to locate the 2019 file name. |
| R-C15 | 2026-10-13 ~11:35Z | curl | `eecg.utoronto.ca/~najm/papers/dac11-sari.pdf`, `tcad08-sari.pdf` | Success; `399a2461…`, `666cd07f…` equal PROVENANCE.md. |
| R-C16 | 2026-10-13 ~11:36Z | curl | `cecs.uci.edu/~papers/compendium94-03/papers/1995/dac95/pdffiles/21_2.pdf` (DAC 1995, SRC-026) | Success; `b7cf7a4c…` equals PROVENANCE.md. Text streams are LZW; extractor extended to decode them. |
| R-C17 | 2026-10-13 ~11:38Z | curl | `codeload.github.com/…/OpenSTA/tar.gz/e01d3f163…` (8.2 MB) | Success; tree extracted. |
| R-C18 | 2026-10-13 ~11:38Z | local | hash check of all eight proposer-cited files inside the tree | **All eight MATCH the proposer's recorded hashes** (C-A13). |
| R-C19 | 2026-10-13 ~11:39Z | local | line-locator spot check of every cited locator (CLM-006/CLM-007/CLM-016/S1) | All confirmed, ±1 line (F-7). |
| R-C20 | 2026-10-13 ~11:40Z | local | `search/PathEnd.cc`, `sdc/Sdc.cc`, `search/Crpr.cc`, `search/Search.cc` — CRPR sign and default activation | **Hold returns −crpr**; OCV + crpr enabled are the constructor defaults (C-A15, F-8, OBJ-001). |
| R-C21 | 2026-10-13 ~11:42Z | local | `dcalc/DelayCalcBase.cc`, `DmpCeff.cc`, `DmpDelayCalc.cc`, `LumpedCapDelayCalc.cc` — thresholdAdjust and port wire-delay formula | C-A16, F-9, OBJ-002. |
| R-C22 | 2026-10-13 ~11:44Z | proxy (WebFetch) | TAU 2019 slide directory listing; `tauworkshop.com/2019/` and `/2019/contest.html` | Used to locate the 2019 contest deck and the official contest description ("Design optimization … judged by final timing, area, and power"). |
| R-C23 | 2026-10-13 ~11:47Z | curl then proxy | `res.mdpi.com` direct path guess for Electronics 11(10):1571; then `r.jina.ai/https://www.mdpi.com/2079-9292/11/10/1571` | The direct mirror route returned an **empty body** (recorded as a failed route, not bypassed further); the proxy read succeeded and is recorded as C-A17 (SRC-022, now full-text-level with the proxy caveat). |

## Broadened sweep (human-directed extension: contests beyond the proposer's list + newest SOTA)

Records for the extension round. File writes stay in the outbox; scratch reads are in `/tmp/claude/dsk-c05-src012/work` (extractor now at `/tmp/claude/dsk-c05-src012/tools/pdftext2.py`; an earlier call in this window failed because it looked for `work/tools/`, corrected in place).

| # | UTC (approx.) | Channel | Target / query | Result |
|---|---|---|---|---|
| R-C24 | 2026-10-13 ~11:5xZ | curl | `tauworkshop.com/<year>/` probes, years 2019-2026 (root, `slides/`, `contest.html`, `agenda.html`) | `/2019/` and `/2020/slides/` live; `/2021/` root live with `speaker_slides/`; `/2022/`-`/2024/` and `/2026/` 404; `/2025/` root live (Hugo site). No contest page after 2021. |
| Q-C05 | 2026-10-13 ~11:5xZ | WebSearch | TAU 2024/2025 contest | No contest found; TAU 2025 logistics/topics only; one 2021 speaker-slide URL surfaced (`EvolutionSTAmodelingTau2021.pdf`). |
| Q-C06 | 2026-10-13 ~11:5xZ | WebSearch | ICCAD CAD contest 2025/2026 problem lists | 2026 problems identified (A-E); 2025 only Problem C confirmed at that pass. |
| R-C25 | 2026-10-13 ~12:0xZ | curl | `tauworkshop.com/2021/contest.shtml`, `tauworkshop.com/2012/contest_2012.html`, `tauworkshop.com/2025/post/program/` | Full prior-year contest list 2011-2021; TAU 2012 = power grid simulation (transient, parallel); TAU 2025 technical program (May 2025) has **no contest session**. |
| R-C26 | 2026-10-13 ~12:0xZ | curl + local | TAU 2021 contest deck download, hash, extraction | `TAU 2021 Contest - final.pdf` = `tau_contest.pdf`, SHA-256 `e67ab36167823ea9fd34646e00ee6185b9641fadd3bec73949929775ddbb3ccd`, 68 pages; text extracted locally (delay-calculation contest; single driver, multiple receivers, CCS, ASAP7 v1.7). |
| R-C27 | 2026-10-13 ~12:1xZ | curl | `iccad-contest.org/Problems.html`, `/tw/03_problems.html` | Live 2026 problem list read (A-E, organizers); 2025 titles partial. |
| Q-C07 | 2026-10-13 ~12:2xZ | WebSearch | ISPD 2026 contest / DAC 2026 MCMM | ISPD 2026 contest identified (buffering/sizing; single PVT corner, ideal clock per the invited-paper summary); nothing for DAC 2026. |
| Q-C08 | 2026-10-13 ~12:2xZ | WebSearch | ML timing worst-case bounds / conservative guarantees 2025-2026 | BLAST (DAC 2025), UQ-GNN, flip-flop waiver (TODAES 2025), and the patent's safety language surfaced; no 2026 soundness work. |
| R-C28 | 2026-10-13 ~12:3xZ | curl (API) | Crossref FACT; S2 ASAP / TCAD-2024 multicorner / flip-flop TODAES | Abstracts retrieved (FACT via Crossref because S2 has no record for that DOI yet; SI-Aware query hit HTTP 429 and was recorded as skipped). |
| R-C29 | 2026-10-13 ~12:3xZ | curl (API) | S2 citations of DAC 2011 (`10.1145/2024724.2024899`) | 7 citing works from 2022+ listed (SetupKit ICCAD 2025, SI-Aware ASP-DAC 2025, One-for-All ICCAD 2024, timing macro modeling TCAD 2024, FACT MLCAD 2024, CPU-GPU STA TCAD 2023, one unrelated 2026 item). TCAD-2008 DOI returned 404 at S2 (no record under that DOI form). |
| R-C30 | 2026-10-13 ~12:0xZ | WebFetch | `patents.google.com/patent/US12675622B1/en` | Full claim-level read (claims 1/3/4/5/7/8/15; Description safety sentence; 1% TNS example; bibliographic data). |
| Q-C09 | 2026-10-13 ~12:1xZ | WebSearch | One-for-All ICCAD 2024 | Framework described; no guarantee claim found. |
| Q-C10 | 2026-10-13 ~12:1xZ | WebSearch | ICCAD 2025 problem titles | Problem A (trojan detection) confirmed; overview mentions multibit-FF optimization; still no screening problem. |
| Q-C11 | 2026-10-13 ~12:3xZ | WebSearch | exact worst-corner B&B / complete coverage | INESC DATE 2007 and IC6 PDFs located (snippet-level content only after fetch failures). |
| R-C31 | 2026-10-13 ~12:3xZ | curl | `algos.inesc.pt/.../silva-date2007.pdf`; `algos.inesc-id.pt/projectos/powerplan/IC6.pdf` | Both **failed** (HTTP 502 and a TLS error respectively). Recorded as failed routes; no bypass attempted. |
| R-C32 | 2026-10-13 ~12:3xZ | curl | Wayback CDX (`tauworkshop.com`, 2022-2026) and root snapshot 2024-04-01 | No snapshots for `/2022/`-`/2024/`; the 2024-04 root still reads "Redirecting to ... /2021". |
| R-C33 | 2026-10-13 ~12:2xZ | curl | `sliponline.org/Publications/Conferences/421/c421.pdf` (ISPD 2026 invited paper) | **Failed**: 195-byte non-PDF body. ISPD 2026 details therefore rest on the search-index summary and are flagged in C-A20. |
| Q-C12 | 2026-10-13 ~12:3xZ | WebSearch | MLCAD 2024/2025 contest | MLCAD 2025 = ReSynthAI (ASU/NVIDIA; OpenROAD + CircuitOps; 12 benchmarks; September 2025). |
| Q-C13 | 2026-10-13 ~12:4xZ | WebSearch | 2026 certificate / proof / sound corner reduction | Nothing relevant; only practitioner corner-selection guidance (PnR vs signoff) and unrelated physics documents. Counts as a negative-result query for the K1 check. |

## Sweep-closure pass (remaining checklist items)

| # | UTC (approx.) | Channel | Target / query | Result |
|---|---|---|---|---|
| R-C34 | 2026-10-13 ~13:0xZ | curl | `sites.google.com/site/taucontest2013/`, `tauworkshop.com/2013/tau2013_program.pdf` | TAU 2013 results page read in full (winners, organizers, dates); program lists the contest committee. C-A25. |
| R-C35 | 2026-10-13 ~12:5xZ | curl + local | `tauworkshop.com/2020/slides/belov__clustering_based_merging_v2.pdf` | Downloaded (SHA-256 431b1330…), extracted; GBA-PBA gap and merge-only-when-converged framing read. C-A26. |
| R-C36 | 2026-10-13 ~12:5x-13:0xZ | curl | ISPD26-Contest repo: README, per-design `lib_setup.tcl`, `scripts/evaluation.tcl` (raw.githubusercontent) | TT-only `libworst` set and `set_ideal_network [all_clocks]` (propagated clock commented out); report_tns/report_wns. Primary confirmation of C-A20's claims. C-A27. |
| R-C37 | 2026-10-13 ~12:5xZ | curl | MLCAD25-Contest README + problem-statement PDF; ISPD26 description PDF | READMEs read (primary); both problem PDFs use subset fonts without usable ToUnicode and were **not** usable by the local extractor — recorded as an extraction limitation. C-A27 limitation note. |
| R-C38 | 2026-10-13 ~13:0xZ | curl (API) | S2 `openAccessPdf` for NIO / One-for-All / ASAP / TCAD-2024 / BLAST | Only One-for-All exposes an OA link (ACM; 403 later). NIO has title only, no abstract. C-A28. |
| R-C39 | 2026-10-13 ~13:0xZ | curl | arXiv API, properly formed queries for ASAP / SetupKit / BLAST / UQ-GNN / SI-Aware | **Zero hits** — no preprints exist. F-12's full-text caveat is now a verified negative. C-A28. |
| R-C40 | 2026-10-13 ~13:1xZ | curl | `dl.acm.org/doi/pdf/10.1145/3676536.3676656` (One-for-All OA link) | HTTP 403, 5.5 KB HTML body; no fallback attempted beyond the earlier proxy failures. C-A28. |
| R-C41 | 2026-10-13 ~13:1xZ | curl (API) + local | U Toronto scholaris DSpace REST (item → bundles → bitstreams); thesis PDF download; hash; extraction | Onaissi 2011 PhD thesis obtained (880,389 bytes, SHA-256 2233c14b…), 277 KB text extracted and keyword-scanned. C-A28. |
| R-C42 | 2026-10-13 ~13:1xZ | curl | ASAP7 TT library headers (LVT/RVT/SLVT, AO family) in the ISPD26 platform | Identical threshold attributes across variants → mixed-VT alone does not trigger `thresholdAdjust`. C-A30; OBJ-002 narrowed (F-15). |
| Q-C14 | 2026-10-13 ~13:0xZ | WebSearch | exact title of the 2011 thesis | Identified as Onaissi (U Toronto, advisor Najm) — same author as SRC-012/013. |
| Q-C15 | 2026-10-13 ~13:0xZ | WebSearch | "corner dominance" monotonicity liberty proof | No primary proof source exists publicly; F-4 lead downgraded. C-A29. |

**Boundary statements from this sweep (current as of this window).**
- Latest timing-specific contest on record: **TAU 2021** (delay calculation). Newest timing-adjacent contests: **ICCAD 2026 Problem D** (useful-skew timing fixing) and **MLCAD 2025** (ReSynthAI). No contest 2011-2026 poses multi-corner screening or a signoff guarantee (F-11).
- Latest SOTA reviewed: **ASAP (TCAD 45(1), 2026)**, **FACT (TODAES 31(4), 2026; online 2025-09-15)**, **SetupKit (ICCAD 2025)**, **US 12,675,622 B1 (granted 2026-07-07)**, plus the 2024-2025 items in C-A23. None discloses per-scenario sound certification with exact refinement at the fidelity read; K1 remains untriggered with the fidelity caveat in F-12.

## Planned next steps in this round (from `first-pass-plan.md` §10, updated)

1. ~~TAU 2018/2019 topic resolution~~ — **done** (F-6), and now **superseded by the full-series sweep** (F-11, C-A18): the TAU contest series runs 2011-2021 and none of it is multi-corner screening. TAU 2013 winner retrieval remains open (minor; CLM-014 is already sourced for 2013).
2. ~~Pinned-code re-verification of CLM-006/CLM-007 locators~~ — **done** (F-7; hashes recomputed, locators confirmed).
3. ~~Confirm the SRC-012/SRC-013 quoted sentences~~ — **done** for both (C-A10; originals read from hash-verified bytes).
4. ~~MDPI SRC-022 full text~~ — **done** (F-10, C-A17; proxy route, mirror route failed). Remaining: the three shortlisted citing works from C-A09 (NIO 2014; DAC 2015 mode merging; 2011 variability thesis).
5. A primary source for the Liberty-monotonicity dominance practice behind F-4, or downgrade that lead.
6. Promote the CRPR sign check to a unit test in the challenger additions, and refresh the `CA-` list in `first-pass-plan.md` with what this window produced (the OBJ-001 repair, the thresholdAdjust test, the TAU 2019 dataset lead).
7. Continue drafting `OBJ-` entries; OBJ-001 and OBJ-002 are filed in `challenges.md` and await verifier adjudication.
8. ~~Broadened sweep (human directive): contests and newest SOTA beyond the proposer's sources~~ — **done** (F-11, F-12, F-13; records C-A18 to C-A24; boundary statements above). Open sub-items: full texts of SetupKit (ICCAD 2025) and ASAP (TCAD 2026) for a F-12 re-check; primary confirmation of the two secondary contest summaries (C-A20, C-A21).
9. Apply the two audit extensions to the proposer-facing notes: U8's contest list (F-11) and the related-work framing S-4 (patent line; exactness differentiator) — to be folded into the `CA-` refresh of `first-pass-plan.md` next window.
10. ~~Three shortlisted C-A09 citing works; F-4 primary source; TAU 2020 merging deck~~ — **closed** in the sweep-closure pass (F-14): mode merging is paywalled at abstract level (watch item), NIO is unobtainable through available routes, the 2011 thesis was obtained and read (C-A28), the F-4 proof lead is downgraded (C-A29), and the merging deck was read (C-A26). Also closed: TAU 2013 results (C-A25), ISPD 2026 primary confirmation (C-A27), ASAP7 threshold check (C-A30).
11. **Challenger-side checklist status: empty.** Everything remaining is process or access: verifier adjudication of OBJ-001/OBJ-002; paywalled full texts (institutional access); joint task-list co-production (harness items 9-10) with the CA-series additions and the CRPR unit test.
