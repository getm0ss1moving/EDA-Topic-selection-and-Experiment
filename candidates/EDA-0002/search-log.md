# Search Log

Actor `Claude-P05-TIMING` (proposer), session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`. Packet `ff20816f…3574602d`; it was re-verified at 2026-10-12T16:02:57Z with 31 of 31 hashes OK.

## Scope, terminology, and search date

- **Date and window:** 2026-10-12, roughly 16:02-17:01 UTC (one session). Per-item times below are approximate, to within about 10 minutes.
- **Search tools:**
  - Host `WebSearch` in "standard" mode unless marked *extended*. It returns model-written summaries plus links, so a claim taken only from such a summary is recorded as `metadata` access.
  - Host `WebFetch`. A small model extracts the answer from the fetched page, so quotes are limited and locators should be re-verified.
  - `curl` downloads of public source files into session scratch, read with `grep` and `sed`.
  - A locally compiled PDFKit text extractor for two PDFs. It only reads text; no EDA tool was run.
- **Slice definition** (`first-pass-plan.md` §5): all slices S1-S8 were considered. Search order was S1, then S3, S4, S2, S6, S8, S7 and S5, but the deep audit ended up on S2 (MCMM).
- **Terminology** (see `first-pass-plan.md` §6): MCMM, scenario, view, corner (PVT, RC), dominant corner, corner reduction or pruning, unobserved-corner prediction, signoff-safe, slack cutoff, synthetic corner, clock-network partial analysis, effective capacitance (Ceff), Elmore bound, interval or early/late bounds.

## Queries, indexes, filters, and inspected results

No date or venue filters were applied unless stated. "Kept" means the result was recorded in `sources.json`.

| # | Approx. UTC | Engine | Query (exact) | Inspected / kept | Notes |
|---|---|---|---|---|---|
| Q01 | 16:10 | WebSearch | `incremental static timing analysis slack-based pruning propagation early termination` | 9 links; patents US9400864, US8056038, NYCU thesis | S1 scoping; led to SRC-044 |
| Q02 | 16:10 | WebSearch | `TAU 2015 timing contest incremental timing and CPPR analysis` | TAU 2015 site, iTimerC 2.0 record, theses | SRC-037, SRC-047 |
| Q03 | 16:11 | WebSearch | `"static timing analysis covering all" PVT corners Onaissi Najm` | Synopsys US12675622; Najm group PDFs (dac11, tcad08, iccad06, tcad12, iccad08) | SRC-012, SRC-013, SRC-017 |
| Q04 | 16:12 | WebSearch | `unobserved corner prediction reducing timing analysis effort Kahng DATE 2019` | DATE 2019 page, NSF PAR, MDPI 2022, IEEE 10419016, patent US11295057 | SRC-015, SRC-022, SRC-024 |
| Q05 | 16:20 | WebSearch | `incremental timing analysis patent stop propagation slack threshold "incremental timing" sufficient slack not recomputed` | US8046725, US10747925, US9280625, US9171122, US8056038, US7260801 | S1: SRC-043, SRC-044, SRC-045 |
| Q06 | 16:20 | WebSearch | `iTimerC 2.0 fast incremental timing CPPR lazy evaluation lazy propagation ICCAD 2015` | NYCU record, TAU 2015 site, ICCAD 2015 problem C | SRC-047 |
| Q07 | 16:20 | WebSearch | `gate sizing runtime dominated by incremental timing analysis Lagrangian relaxation percent of runtime timer` | TCAD 2020 multithreaded LR sizing (summary), Iowa State theses | S1 demand; not kept (secondary summary only) |
| Q08 | 16:20 | WebSearch | `OpenROAD repair_timing slow runtime issue incremental timing update github` | OpenROAD issue #5003, Antmicro blog | SRC-050 |
| Q09 | 16:16 | WebSearch | `"Multicorner Timing Analysis Acceleration for Iterative Physical Design" abstract` | IEEE 10419016 abstract summary | SRC-024 |
| Q10 | 16:33 | WebSearch | `incremental timing analysis patent level-limited lazy recalculation Abato Hathaway "incremental timing analysis" 5508937` | US5508937, US7111260, US8775988 | SRC-046 (S1) |
| Q11 | 16:33 | WebSearch | `OpenTimer v2 parallel incremental timing analysis engine lazy evaluation update_timing TCAD` | HKBU records, OpenTimer README | SRC-048 (S1) |
| Q12 | 16:34 | WebSearch *extended* | `interval bounds static timing analysis guaranteed slack bound refinement on demand incremental optimization` | Blaauw SSTA bounds paper (Berkeley host), US7404163, US7117466 | Bounds-and-refinement concept exists in SSTA; not kept (not inspected) |
| Q13 | 16:35 | WebSearch | `timing-driven optimization stale timing information bounded error incremental STA accuracy runtime tradeoff sizing buffering` | dt10 transactional timing, US8141017, INSTA DAC25, Tatum FPT18 | SRC-041, SRC-042, SRC-049 (S1) |
| Q14 | 16:37 | WebSearch | `"transactional" timing analysis physical synthesis incremental bottleneck Markov IBM Design Test 2010` | dt10 paper metadata, Papa dissertation link | SRC-041 |
| Q15 | 16:38 | WebSearch | `David Papa dissertation University of Michigan "bounded transactional timing analysis" deepblue` | none relevant | Excluded (not found) |
| Q16 | 16:39 | WebSearch | `INSTA ultra-fast differentiable statistical static timing analysis engine arXiv Yi-Chen Lu 2025` | NVIDIA page, HeteroSTA arXiv 2511.11660 | SRC-049; HeteroSTA not kept (GPU, S1) |
| Q17 | 16:43 | WebSearch *extended* | `corner pruning static timing analysis provably safe dominance bound multi-corner signoff missed violation guarantee` | DAC11 PDF (toronto.edu host), US12675622, Kahng NSF, MDPI, ASP-DAC 2010 unified MCMM engine, Tetelbaum 2014, embedded.com 40nm, EEJournal 2012, US9141742, US7681157 (via summary) | SRC-014, SRC-018, SRC-019, SRC-020, SRC-021 |
| Q18 | 16:43 | WebSearch | `temperature inversion worst-case corner selection static timing analysis FinFET corner dominance changes` | US8181144, US8645888, USC ISLPED14 paper, SemiEngineering | Evidence that corner dominance can change; not kept individually (SRC-019 p. 9 covers it) |
| Q19 | 16:55 | WebSearch | `TAU contest topics list 2013 2014 2015 2016 2017 2018 2019 timing analysis contest archive tauworkshop` | ISPD slides 2013/2014, TAU 2015 site | SRC-039 |
| Q20 | 16:55 | WebSearch | `TAU 2017 contest timing macro modeling OR "TAU 2018" contest OR "TAU 2019" contest timing analysis topic` | LibAbs, iTimerM references | SRC-039 |
| Q21 | 16:55 | WebSearch | `ICCAD CAD contest multi-corner timing problem OR "multi-corner" "CAD Contest" timing analysis problem statement` | iccad-contest.org pages, CEDA newsletter, NTU 2011 PDF | SRC-040 |
| Q22 | 16:59 | WebSearch | `"The Elmore delay as a bound for RC trees with generalized input signals" Gupta Tutuianu Pileggi IEEE TCAD 1997` | CMU page, Wikipedia, slides | SRC-026 |
| Q23 | 16:59 | WebSearch | `"Performance computation for precharacterized CMOS gates with RC loads" Dartu Menezes Pileggi effective capacitance` | CMU page, secondary descriptions | SRC-027 |
| Q24 | 16:59 | WebSearch | `hold time analysis minimum set of dominant corners dominance margin timing feasibility at all other corners` | DAC11 (excerpt), US12675622, AMD/Intel docs | Confirms hold limitation (SRC-012 excerpt) |
| Q25 | 17:00 | WebSearch | `multi-corner timing prediction partial matrix completion neural network 2024 STA corners` | MCSTA (BUAA), TOTAL (BUAA), US11755807 | SRC-023, SRC-025 |
| Q26 | 17:00 | WebSearch | `TOTAL multi-corners timing optimization transfer active learning DAC 2023 generalized linear model latent features Bayesian` | BUAA record, IEEE 10419016, SetupKit (different topic) | SRC-023 |
| Q27 | 17:00 | WebSearch | `OpenRCX define_process_corner extract_parasitics multiple corners corner_cnt write_spef corner OpenROAD documentation` | OpenROAD rcx docs (two versions) | SRC-035 |

**Direct fetches and downloads** (all kept items are in `sources.json`):

- **GitHub API:**
  - OpenROAD `src/sta` submodule at `b16bda7e` (SRC-010);
  - OpenSTA and OpenROAD commit metadata;
  - OpenSTA tree at `e01d3f16`;
  - ORFS platform, library and design listings (SRC-028, -029, -034, -036);
  - license API calls (SRC-031, -032);
  - ORFS master head (SRC-052).
- **Raw source files downloaded to scratch and hashed** (hashes in `sources.json`):
  - OpenSTA: `dcalc/{GraphDelayCalc.cc, DelayCalc.cc, DelayCalc.i, DelayCalc.tcl, DmpCeff.cc, DmpDelayCalc.cc, LumpedCapDelayCalc.cc, DelayCalcBase.cc}`, `search/{Search.cc, Sta.cc, Corner.cc, Crpr.cc, Levelize.cc, MakeTimingModel.cc}`, `liberty/TableModel.cc`, `parasitics/{ReduceParasitics.cc, Parasitics.tcl}`, `tcl/{Sta.tcl, Search.tcl, Variables.tcl, Sdc.tcl, Liberty.tcl, Network.tcl, CmdUtil.tcl, Util.tcl, Link.tcl, StaTcl.i}`, `include/sta/{Sta.hh, Search.hh}`, `doc/ChangeLog.txt`;
  - OpenROAD: `src/rsz/src/{RepairSetup.cc, RepairHold.cc, Resizer.cc, RepairDesign.cc}`, `src/rsz/README.md`, `LICENSE`.
- **Google Patents pages:** US12675622B1, US9280625B2, US10747925B1, US8056038B2, US8141017B2, US7681157B2, US9141742B2.
- **Web pages:** Antmicro blog (SRC-050), DATE 2019 page (SRC-015), TAU 2016 contest page (SRC-038), EEJournal (SRC-020), embedded.com (SRC-021), and ORFS README and license files.
- **PDFs downloaded and text-extracted:** ASP-DAC 2010 slides (SRC-014) and Tetelbaum 2014 (SRC-019).

## Backward and forward citation expansion

**Expansion 1 (backward, from the multi-corner seed SRC-012):**

- Onaissi ICCAD06/TCAD08 (SRC-013), via the same author page and the ASP-DAC 2010 slides' citation list.
- Heloue DATE07 branch-and-bound (cited in SRC-014, slide 7; not fetched).
- Heloue TCAD12 "parameterized timing analysis covering all potentially critical paths" (search hit; not fetched).
- The NTU unified MCMM engine (SRC-014).
- Patents found by topic: IBM US7681157 (SRC-016), Synopsys US9141742 (SRC-018) and US12675622 (SRC-017).

**Expansion 2 (forward and alternative formulations):**

- Learned prediction line: Kahng DATE19 (SRC-015), then MDPI 2022 (SRC-022), TOTAL DAC23 (SRC-023), IEEE 2024 (SRC-024), MCSTA 2024 (SRC-025), and patents US11755807 and US11295057 (search hits; not fetched).
- Industrial practice: Tetelbaum 2014 (SRC-019), embedded.com (SRC-021), EEJournal (SRC-020).

**Result.** Neither expansion surfaced a source describing per-scenario bounds that are sound against the reference engine's delay-calculation semantics, combined with exact refinement to reproduce full MCMM decisions. This is **absence of evidence under limited access**, not proof of novelty (`docs/CHARTER.md` line 9).

**Forward citations of SRC-012 could not be searched**: Semantic Scholar returned HTTP 429, DBLP served a bot wall, and Google Scholar was not attempted.

## Classical and alternative-formulation search

- **Parametric or linear-model all-corner STA:** SRC-013, SRC-014 (via SRC-012).
- **SSTA bounds with selective enumeration** (Blaauw et al., Berkeley-hosted PDF, Q12): a related bound-and-refine idea in statistical timing. Not inspected; recorded as a lead for the challenger.
- **Delay bounds:** Elmore as an upper bound (SRC-026); Ceff and resistive shielding (SRC-027 and the code in SRC-002).
- **Synthetic worst corners** (SRC-018) and **greedy coverage** (SRC-021) as non-learned alternatives.

## Contest, repository, and commercial search

- **Contests:** see `contest-audit.md`. TAU 2013-2017 and 2020-2021, plus ICCAD 2014/2015/2018/2025 and the 2011 IC/CAD contest. No MCMM scenario-reduction contest was found. TAU 2018-2019 are unresolved.
- **Repositories:**
  - pinned OpenSTA (`e01d3f16`): multi-corner analysis exists, and no scenario-reduction or dominance command was found in the Tcl command files inspected (`grep -i "dominan|scenario|corner_reduc|reduce_corner"` over the `tcl/*.tcl` files listed above returned nothing);
  - OpenROAD `b16bda7e` resizer (S1 assessment);
  - ORFS master: platform libraries, designs and licenses.
- **Commercial:** Synopsys patents (SRC-017, SRC-018), an IBM patent (SRC-016), a Cadence-related vendor article (SRC-020), and a vendor white paper (SRC-019). The internals of commercial timers remain unknown (`docs/EVIDENCE.md` line 23).

## Excluded results and reasons

**Excluded slices** (`first-pass-plan.md` §5), with the evidence that drove each decision:

- **S1 Decision-guarded incremental STA in repair loops.** Excluded for thin novelty and decision-consumer mismatch.
  1. OpenSTA already stops arrival propagation on unchanged arrivals (SRC-009, lines 1145-1163 and 1208-1235). It also offers a relative gate-delay tolerance (SRC-008, line 1070) that ignores slew change, but OpenROAD's resizer does not set it (grep of the `rsz` sources, SRC-011).
  2. Margin- and threshold-based skipping is covered by patents: Synopsys incremental slack-margin propagation (SRC-043), IBM's half-slack-margin test (SRC-044), IBM variable-accuracy sufficiency (SRC-045), IBM bounded transactional timing (SRC-042) and level-limited incremental timing (SRC-046). Lazy evaluation and propagation are in iTimerC 2.0 (SRC-047) and OpenTimer (SRC-048).
  3. OpenROAD's `RepairSetup` sorts fanouts by exact slack margins (SRC-011, lines ~703-740 and ~855-880). Any scheme leaving non-critical slacks stale would change the repair trace, so decision equivalence would need exact answers in exactly the regions where savings would come from.
  4. Demand evidence was strong (SRC-041, SRC-049, SRC-050) but did not overcome items 2-3.
- **S3 Multi-fidelity or bounded delay calculation for single-scenario STA.** Excluded because a near-identical concept is patented (US10747925, SRC-045), and because the slack-wall argument (FM-03) predicts small gains in closed single-scenario designs. That prediction is retained as ablation A3.
- **S4 GBA/PBA pessimism.** Excluded because no path-based recalculation engine was found in the pinned OpenSTA tree (SRC-001; file list of `search/`), so there is no reference oracle.
- **S5 SI/crosstalk.** Excluded because no SI module exists in the pinned OpenSTA tree and there is no signoff-grade SI oracle.
- **S6 Hierarchical timing models.** Excluded because the TAU 2016-2017 contests and their winners (SRC-038, SRC-039) cover it heavily; OpenSTA has `write_timing_model` (`search/MakeTimingModel.cc`).
- **S7 Agentic timing-closure support.** Excluded because the packet allows no API budget (`config/research-brief.json` line 14).
- **S8 Learned surrogates.** Excluded because there is no GPU, few designs are available, and the D05 boundary warns against treating surrogates as oracles (`domains/D05/brief.json` line 7).

**Excluded items within S2:**

- HeteroSTA, INSTA: GPU engines, outside the resource envelope.
- SetupKit: library characterization, a different task.
- US11755807, US11295057: prediction patents, not fetched; listed as leads.
- Heloue DATE07 and TCAD12: not fetched; leads.

## Access limitations and stopping rationale

**Access failures** (recorded, not bypassed):

| Target | Failure |
|---|---|
| SRC-012 (eecg.utoronto.ca and eecg.toronto.edu) | Fetch timed out 4 times; curl timed out after 120 s |
| SRC-041, Papa dissertation (web.eecs.umich.edu) | TLS certificate verification failed; not bypassed |
| SRC-022 (MDPI) | HTTP 403 |
| Semantic Scholar API | HTTP 429 |
| DBLP | Bot-protection wall |
| IEEE Xplore 10419016 | Empty page |
| INSTA PDF | Git LFS pointer instead of the file |
| TAU 2018 and 2019 sites | Google login wall |
| NSF PAR PDF 10539798 | TLS error on download; host-saved copy not readable under permissions; item unidentified and not used |

**Stopping rationale.** `docs/EVIDENCE.md` line 13 allows a round to stop after two documented expansions reveal no closer mechanism, or on budget/access exhaustion with the residual risk reported. Both expansions above were documented, but the round stops here **on access exhaustion with residual risk**, because the single most decision-critical paper (SRC-012) was seen only as an excerpt.

**Residual risk:**

1. SRC-012 may already contain the proposed mechanism (K1).
2. Commercial timers may already implement sound per-endpoint screening; their internals are unknown.
3. Forward citations of SRC-012, SRC-016 and SRC-017 were not searched.
4. The Chinese- and Taiwanese-language thesis literature on MCMM was not searched.

## Pre-promotion novelty refresh

Pending. Before promotion, in order:

- **(a)** Read SRC-012 in full and record its delay model, bound construction and hold method.
- **(b)** Run forward-citation searches of SRC-012, SRC-013, SRC-016 and SRC-017.
- **(c)** Re-run Q03, Q04, Q17, Q25 and Q26 with a date filter covering 2024 to the present.
- **(d)** Search the terms "certified corner pruning", "sound multi-corner timing", "provable corner dominance" and "scenario screening".

The search must be re-run after any substantive mechanism change.
