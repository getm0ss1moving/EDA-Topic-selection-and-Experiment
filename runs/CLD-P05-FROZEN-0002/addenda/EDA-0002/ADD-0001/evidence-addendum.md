# EDA-0002 evidence addendum ADD-0001 (proposer)

| Field | Value |
|---|---|
| Author | `Claude-P05-TIMING` (`CLD-Origin-TIMING`), proposer session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8` |
| Run | `CLD-P05-ADDENDUM-0001` |
| Applies to | The round-0 dossier as transported by PR #13 (head `9d5bd30e30238f611e30ad21f094db1e4df98b43`, dossier digest `8d6bd047232a17a1ba985d156c831e76e3212772667309dffc9cdf1a934ff03b`) |
| Status | Proposer evidence correction. It is **not** a revision of the frozen round-0 files, it answers no challenge, and it is not a verdict |
| Trigger | The human owner supplied an acquisition note (`EDA_Source_Access_Guide.md`, checked 2026-10-13) naming public routes to SRC-012 and to TAU 2018/2019 material |
| New and superseding source records | `sources-addendum.json` in this directory (SRC-012 and SRC-039 superseded; SRC-053 to SRC-058 new) |

The round-0 files are unchanged. They are frozen by the merge of PR #13, and the challenger packet was exported from them (PR #15, seen by title only). The coordinator decides whether to release this addendum now as an evidence correction or to fold it into the round-1 revision (`docs/WORKFLOW.md` step 5). Section 6 lists the exact edits needed to fold it in.

## 1. SRC-012 is now read in full (resolves U1 for the proposer)

**Access.** The live author URL `https://www.eecg.toronto.edu/~najm/papers/dac11-sari.pdf` still fails: the proxy tunnel opens, but the TLS handshake times out. The web-fetch tool also timed out twice. Instead, the proposer read the Internet Archive's raw capture of that same URL from 2024-02-03:

- 6 pages, PDF 1.6, SHA-256 `399a24613a4d5872d70708546046dbfdefe50d0ccca87ea052a2879f38871072`;
- title, authors, pages 777-782 and DOI `10.1145/2024724.2024899` match Crossref metadata;
- the text was extracted with the session's PDFKit reading aid;
- the copy is kept in session scratch only and not redistributed. Quotations below are bounded excerpts.

Page numbers are the printed DAC pages (PDF page 1 = p. 777).

### 1.1 What the paper does (facts, with locators)

| # | Finding | Locator |
|---|---|---|
| F1 | **Setup.** A pre-chosen pair of slow corners is shown to *empirically* cover worst-case setup slack: endpoint coverage under a "dominance margin". Coverage is 87.6-100% at 0 ps, at least 97.9% at 10 ps and at least 99.9% at 30 ps. No bound is proved. | §2.2 (p. 778); §5.1 and Table 8 (p. 780) |
| F2 | **Hold.** Dominant corner sets vary by circuit. Worst-case device corners dominate up to 26% of evaluated endpoints (T2, 10 ps). The authors conclude that no small pre-chosen set suffices for hold. | §5.2 (p. 780); Table 10 (p. 781) |
| F3 | **Hold estimator.** A full STA run is done at an anchor corner c_i, plus "partial timing runs, which cover only the clock network" at each partial corner c_j. The estimate is σ̃_j = σ_i + (k_j − k_i), where k is the clock skew between the anchor's worst startpoint s′ and the endpoint. The stated error is (d_j − d_i) + (t_hold,i − t_hold,j). It is conservative only if the partial corner's data-path delay exceeds the anchor's (e_d > 0) and the hold-time difference is negligible. | Abstract (p. 777); §6.1, eqs. (5)-(11) (pp. 780-781) |
| F4 | **Anchor choice is heuristic.** One "Min C" anchor is used per device group (c1, c6, c11), justified because "functional logic paths generally tend to have short nets". The method also assumes the worst startpoint is the same across corners; 0.5-13.1% of endpoints change startpoint. | §6.1 (p. 781); Table 9 (p. 780) |
| F5 | **The estimate is not sound.** "Covered" means the estimate is less than or equal to the actual slack. At 0 ps margin the method covers 51.8-88.6% of evaluated endpoints, so it is **optimistic at 11.4-48.2%** of them. At 5 ps the coverage is 98.6-100%. | §6.2.1 and Table 11 (p. 781) |
| F6 | **With SI analysis, coverage drops.** It falls to 86.5% (T5, 5 ps) and 92.1% (T5, 10 ps). Clock shielding is an informal argument. | §6.2.2 (pp. 781-782); Table 12 (p. 782) |
| F7 | **Pessimism.** Conservative estimates underestimate slack by up to about −40 ps (worst-case outliers). | §6.2.3 and Table 13 (p. 782) |
| F8 | **Runtime.** A clock-only partial run costs 9.0-25.3 s, against 486.4-2466.6 s for a full run (0.4-2.5%). Load overhead per run is 153.1-288.4 s. Speedups versus timing all 10 corners of Ω_T are 2.4-3.6× with per-run overhead and 4.1-4.7× with shared overhead. These figures are internally consistent with L_full excluding overhead (checked arithmetically for T1). | §6.2.4 and Table 14 (p. 782) |
| F9 | **No refinement step.** Estimated slacks are the output. The method is "primarily intented [sic] for non-final STA runs". | §1 (p. 778); §7 (p. 782) |
| F10 | **No linear PVT model.** The paper argues that "the linear dependence of gate and interconnect delays on PVT parameters may not always hold" and uses discrete corner analysis instead. | §1 (p. 777) |
| F11 | **Setup of the experiments.** 15 industrial circuits (5 shown, 916K-1.42M instances), 45 nm, 15 corners (3 device × 5 interconnect settings), ±5% derates and CRPR. Evaluation is flop-to-flop only and limited to the 25% of endpoints with the worst slack; temperature inversion is not considered. The timer is not named. | §3.1-3.2 (pp. 778-779) |

### 1.2 Proposer assessment of K1 (provisional; requires independent verification)

[INF] **SRC-012 does not trigger K1.** K1 fires if the full text shows "per-scenario sound certification with exact refinement already exists" (`proposal.md` § Kill and stop criteria). SRC-012 has neither element:

- Its hold estimate is optimistic at up to 48.2% of evaluated endpoints at 0 ps margin (F5). It is conservative only under a cross-corner ordering assumption (F3, F4).
- Its setup treatment is empirical dominance (F1).
- It never re-times any endpoint exactly; its output is an estimate (F9).

The access guide states, and the proposer agrees, that obtaining the text does not by itself pass K1 (`docs/EVIDENCE.md` line 19). The verifier must re-open the source.

**The overlap is closer than round 0 could show.** Round 0 listed the clock-only partial run as a reused ingredient. The full text shows that SRC-012's estimator has the *same decomposition* as the candidate's steps A and B:

- an exact per-corner clock (skew) term from a clock-only pass, which is the candidate's step A, in the same role;
- plus a data-path term that is not timed at that corner.

The candidate's remaining distinctions are therefore narrower than "every ingredient is individually known" suggests:

| | SRC-012 | Candidate (as anchored in `direction-control.json`) |
|---|---|---|
| D1. Data-path term at scenario s | Borrowed from a different anchor corner (d_i). Valid only if d_j > d_i | Bounded from s's own tables and parasitics; no cross-corner ordering assumption |
| D2. Guarantee | Reports coverage. Optimistic estimates occur (F5) | Certificate must be sound against pinned `dmp_ceff_elmore` (P1-P6; **P3-P5 unproven, K2**) |
| D3. Exactness | None; intended for non-final runs (F9) | Uncertified triples are re-timed exactly, so decisions equal full analysis by construction (CLM-009) |
| D4. Startpoints | Assumes a stable worst startpoint (F4) | Block-based bounds over all paths into the endpoint |
| D5. Checks covered | Hold via the estimator; setup via empirical dominance | Setup and hold by the same certificate |
| D6. SI | Evaluated empirically (F6) | Out of scope in v1 (`proposal.md` § Scope). This is a gap of the candidate, not an advantage |

[INF] **Consequence for the novelty case.** A challenger could reasonably argue that the candidate is SRC-012 with the borrowed data-path delay replaced by a sound interval bound, followed by generic selective re-analysis. That is the composition risk named in `docs/CHARTER.md`. The anchor's mechanism already contains exactly these parts, so this is **not** a direction change, and both penalties stay at 0. What changes is where the contribution must be shown:

- **Soundness:** a soundness argument against the reference calculator's table and DMP semantics (K2, EXP-002).
- **Usefulness:** a certifiable fraction large enough to matter (K3, EXP-003).

If either fails, SRC-012's estimator plus a margin is the practical alternative, and the candidate has no remaining contribution.

[INF] **Headroom signals in SRC-012, not measurements of this candidate:**

- F8 supports the assumption that an exact clock-only pass is cheap: 0.4-2.5% of a full timing run in the unnamed industrial timer.
- F8 also shows a per-run load overhead of 10.8-33.6% of L_full. Under the `experiment-plan.md` metric (end-to-end wall time to the same decisions), any load cost that both B0 and the candidate pay caps the achievable reduction R. EXP-003 should report library and parasitic loading separately from the timing update, so that the 20% threshold is not met or missed through overhead accounting. This is a proposed protocol clarification for round 1. It is not a change to the frozen plan.
- F2 and F5 confirm the hold-side demand. Even an industrial estimator with clock-exact skew leaves optimistic endpoints at 0 ps margin. This supports CLM-003 and L1.

## 2. TAU 2018 and TAU 2019 are resolved at summary level (resolves U8 for the proposer)

Both official topic pages and both summary slide decks are public (SRC-053 to SRC-056). Both slide PDFs match the SHA-256 values in the access guide byte for byte.

| Contest | Topic (official) | Relevance to this candidate | Locator |
|---|---|---|---|
| TAU 2018 | "Efficient generation of timing reports from an STA graph with updated arrival and required times". Top-N critical paths with from/through/to filters; graph-based analysis only. Benchmarks used "special constant-delay Liberty models" to remove delay-calculation impact | None for MCMM screening. Winner iTimerP prunes backward path search with per-node "local slack bounds". That is a bound-based pruning inside one analysis; it certifies nothing across scenarios, and the candidate does not implement it | SRC-053 topic paragraph; SRC-054 slides 3-6, 15, 20-21 |
| TAU 2019 | "Design optimization": buffer insertion, deletion and resizing, scored by period, power, area, runtime and memory. OpenTimer is the evaluator; results reported for a "fast corner" and a "typical corner"; Nangate FreePDK45 | None for MCMM screening. Multiple corners appear only as separate evaluation conditions | SRC-055 topic paragraph; SRC-056 slides 3-6, 11-13, 16-18 |

[OBS] **Correction.** Round 0 stated that the TAU 2018/2019 contest pages "redirect to a Google login" (`contest-audit.md`, `search-log.md` access table, SRC-039, CLM-014, U8). That was inaccurate as a description of the material: the official `tauworkshop.com` topic pages and summary slides are public. The Google-hosted resource attachments (rules, file formats, winner presentations, benchmarks) remain **not inspected**. Their access state is unverified, not confirmed as login-only.

[INF] The contest-audit conclusion stands with a narrower residual. No TAU contest from 2013 to 2021 found so far addresses MCMM scenario reduction, so the candidate does not implement a contest baseline, an organizer hint or a winner method. The unread TAU 2018/2019 rule documents are not decision-critical for this question: both official summaries define single-analysis tasks. Their content remains unresolved.

## 3. Forward citations of SRC-012 (partial; refresh plan item b)

[OBS] The Semantic Scholar API returned 23 citing works for DOI `10.1145/2024724.2024899` (Crossref counts 21). Only titles were screened, except where an abstract is noted below. Titles indicating multi-corner timing analysis:

| Work | What was inspected | Relation |
|---|---|---|
| "Unobserved Corner" prediction (DATE 2019) | Already SRC-015 | Learned prediction (category 5) |
| One-for-All (ICCAD 2024), SRC-057 | Abstract | Learned cross-corner prediction from "one single known corner"; no guarantee claimed in the abstract. Category 5 |
| FACT (MLCAD 2024), SRC-058 | Abstract | Learned full-corner prediction from one known corner; no guarantee claimed in the abstract. Category 5. Also states that corner counts grow "from dozens to hundreds" (CLM-001) |
| Multi-corner timing macro modeling with neural collaborative filtering (TCAD 2024) | Title only | Learned macro models; adjacent |
| NIO (ICSICT 2014) | Title only; the publisher withheld the abstract and a web search found nothing | **Unresolved**: the title claims a fast PVT verification method, content unknown |
| A timing-graph-based approach to mode merging (DAC 2015) | Title only | Mode merging; out of scope in v1 |

The other titles concern sensors, clock skew under variation, hold fixing, FPGA routing, GPU STA, characterization and SoC design.

[INF] No title or inspected abstract among the forward citations suggests per-scenario sound certification with exact refinement. Title-level screening is weak evidence. NIO, and the forward citations of SRC-013, SRC-016 and SRC-017, remain open.

## 4. Errata in round-0 records

**E1 [OBS]: all round-0 timestamps are about 15 h early.**

- Every UTC timestamp written by this actor in round 0 came from the host clock, which runs **≈54,000 s (15 h) behind true UTC**. Three paired readings against GitHub `Date` headers on 2026-10-13 gave offsets of 53,987-53,999 s. This agrees with the DeepSeek transport manifest's clock note.
- Affected:
  - `sources.json` `retrieved` fields;
  - `search-log.md` query times;
  - `responses.md` revision date (2026-10-12 should read 2026-10-13);
  - `runs/CLD-P05-RESEARCH-0001/manifest.json` start and end;
  - `role-output-manifest.json`;
  - the onboarding files.
- Correction rule: true UTC = recorded value + 15 h. For example, the run's start 2026-10-12T16:02:57Z is 2026-10-13T07:02:57Z, and its end 17:16:00Z is 2026-10-13T08:16:00Z.
- This also explains the round-0 "committer date later than local clock" anomaly; it was not a repository irregularity.
- All timestamps in this addendum are corrected values (host clock + 54,000 s).

**E2 [OBS]: SRC-012's description was based on excerpts and was partly wrong.**

- The SRC-012 row in `prior-art.csv` says setup slack is "bound[ed]"; per F1 it is empirically covered, not bounded.
- Its assumption field ("likely a delay model over the PVT space") is wrong per F10.
- CLM-005's note "High for SRC-012" no longer applies.
- L2's sentence "Whether this applies to SRC-012 is unverified" is resolved: SRC-012 does not use a linear model. Its conservatism instead rests on the anchor-ordering and startpoint-stability assumptions (F3, F4).

**E3 [OBS]: SRC-012 metadata.**

- `published` should be 2011-06-05, from Crossref.
- The DOI is now verified.
- The round-0 URL used the `eecg.utoronto.ca` alias; the access guide and the capture use `eecg.toronto.edu`.

**E4 [OBS]: TAU access was misdescribed.** The TAU "login wall" statements are corrected per § 2.

## 5. Claims, unknowns and kill criteria after this addendum

- **CLM-002:** add SRC-012 (§1 p. 777, designers choose corners "based on experience"; F5), SRC-057 and SRC-058 (abstracts).
- **CLM-003:** add SRC-012 §5.2 and Table 10 (full access). Uncertainty drops from Medium to Low-Medium.
- **CLM-005:** restrict the scope note to SRC-013 and SRC-014; SRC-012 is not a parametric method (F10).
- **CLM-014:** TAU 2018 and 2019 are now covered at summary level (SRC-053 to SRC-056); rule documents are unread. Uncertainty stays Medium.
- **CLM-015:** still **novelty not established**. SRC-012 is now read in full (proposer only). A partial forward-citation screen found nothing closer. The distinction now rests on D1-D3 and therefore on K2 and K3.
- **U1:** resolved for the proposer; the verifier re-check is pending.
- **U8:** resolved at summary level; the Google-hosted rules remain unread.
- **New U10:** the content of NIO (ICSICT 2014).
- **K1:** not triggered by SRC-012 (proposer assessment). It remains open for other sources.
- **K2, K3:** these are now the decisive tests of the novelty claim, not only of utility.
- **`direction-control.json`:** anchor unchanged; `combination_drift` 0 and `demand_drift` 0. The narrowed distinction has to be shown inside the anchored mechanism and gives no reason to pivot.

## 6. Exact edits to fold into the round-1 revision

These are proposed edits only. Folding them in changes the dossier digest and the files' SHA-256 values.

1. **`sources.json`:** replace SRC-012 and SRC-039 with the records in `sources-addendum.json`, append SRC-053 to SRC-058, and add +15 h to all other `retrieved` values (E1).
2. **`prior-art.csv`, row SRC-012:**
   - mechanism: "Setup: empirical dominance of two slow corners. Hold: anchor-corner full STA plus clock-network-only partial runs; slack at a partial corner estimated as anchor slack plus skew difference";
   - data: "15 industrial 45 nm circuits, 15 PVT corners";
   - evaluation: "Endpoint coverage under dominance margins over the worst 25% of endpoints; speedup 2.4-4.7×";
   - assumptions: "Anchor has the smallest data-path delays in its group; stable worst startpoint; negligible hold-time difference; flop-to-flop; no temperature inversion";
   - limitation: "Optimistic at 11.4-48.2% of evaluated endpoints at 0 ps margin; no exact refinement";
   - distinction: D1-D4 above.
3. **`proposal.md`:**
   - Closest-work item 1: replace *Status* with § 1.2.
   - L2: replace its last sentence per E2.
   - Claim ledger: apply § 5.
   - Unknowns: mark U1 and U8 as resolved for the proposer; add U10.
   - Unresolved question 2: remove it (it is answered).
4. **`contest-audit.md`:** replace the TAU 2018/2019 row and the unresolved item 1 per § 2.
5. **`search-log.md`:** append Q28-Q35 and Expansion 3 from `addendum-search-log.md`, and correct the two access-table rows (SRC-012, TAU) per § 1 and § 2.
6. **`experiment-plan.md` (EXP-003 protocol note):** report load time separately from the timing update for B0 and for the candidate (§ 1.2, headroom signals).
7. **`experiment-consensus.json`:** replace the open condition "SRC-012 has not been inspected in full (K1)" with "SRC-012 full-text distinction (D1-D3) pending verifier check; K2 decisive".
8. **`responses.md`:** add a revision-history row for this addendum.
