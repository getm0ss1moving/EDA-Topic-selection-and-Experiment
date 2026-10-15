# Reproducible source search and access log — P05 succession cycle 1

Actor ChatGPT-P05-TIMING; session 6a1a1207-fcda-4f17-ab1e-c5d41539718b. Input a48f03d4bc254c0b0957d0fe0f265e072d6cf49a; packet bd4911a04b3d7666d4304e869c785e479bbb5b5d9434f6fc18e777a6d9fe0fcb. All searches/access below occurred 2026-10-15 UTC. No per-source approval was sought. No project checkout, Git branches, other role outputs or sessions were searched. Only supplied released proposer material was inherited. No old verification or signature is adopted.

Workflow slice: discrete characterized-corner setup/hold STA; engine-relative slack bounds, certified elimination, exact selective refinement, output-equivalent reports. Terminology expansions: parameterized timing, worst-delay/worst-slack corner, branch and bound, hyperplane redundancy, general nonlinear delay, clock-only correction, cross-corner prediction, active learning, incremental timing, report caching, contest optimization. The inherited bibliography is a discovery aid rather than independent source validation.

## Actual query and retrieval record

| ID | Engine/index and literal query or direct route | Result inspected; inclusion/exclusion and limits |
|---|---|---|
| Q-R01 | Web search: `"Effective Corner-Based Techniques for Variation-Aware IC Timing Verification" pdf` | Original author-host PDF abstract indexed; DBLP metadata used only to confirm DOI/title, not method. Important TCAD2010 lead retained. |
| Q-R02 | Web search: `"multi corner" "static timing" certified 2025 2026` | Recent timing/characterization results and current vendor page; adjacent cell-characterization work is not automatically all-scenario report equivalence. No novelty inference from search absence. |
| Q-R03 | Web search: `"TAU 2025" contest timing "TAU 2026"` | Mostly unrelated tau/marathon/physics hits excluded. Poor precision explicitly retained; not evidence that timing contests do not exist. |
| Q-R04 | Direct primary author PDFs: `dac11-sari.pdf`, `iccad08-khaled.pdf`, `dac08-khaled.pdf`; official DATE2007 `11.4_3.PDF` | Four downloaded PDFs hashed in source records, converted with `pdftotext -layout` in external temporary scratch. Read relevant sections from exact text. Browser ICCAD2008 failed but direct fetch succeeded. Classical pruning/general-bound overlap confirmed. |
| Q-R05 | Direct `https://algos.inesc-id.pt/projects/rav/Silva10.pdf` | Browser internal error; shell HTTPS SSL EOF. Alternate same-host HTTP closed connection and www-host HTTPS SSL EOF. No bytes/full-text hash obtained. Abstract remains all that was accessed. |
| Q-R06 | Web search: `"cross-corner" "2026" timing XGBoost SHAP` | DOI 10.1145/3816045 discovered; third-party index used for discovery only. Publisher endpoint failed; Crossref publisher-deposited abstract read directly. No precise performance claim adopted. |
| Q-R07 | Web search: `"TAU" "2025" "contest" timing analysis EDA` | Official contest sources located; unrelated TAU hits excluded. |
| Q-R08 | Web search: `"ICCAD 2025" contest problems timing` | Official ICCAD2025 overview; team repositories/secondary claims not used as evidence of winners or correctness. |
| Q-R09 | Direct DOI `10.1109/TCAD.2025.3581474`; web search `"ASAP" "3581474" timing`, later `"3581474"` | DOI browser failure; broad numeric search yielded irrelevant results excluded. Crossref direct metadata confirms title and January 2026 issue publication; no method access. |
| Q-R10 | Web searches `"TAU 2018" contest timing graph`, `"TAU 2019" contest timing optimization` | Reopened organizer statements and linked resource index. Official team reports read; see SRC-R12-R16. Secondary thesis/search summaries excluded from claims. |
| Q-R11 | Web searches `"3816045" site:dl.acm.org`, `"Effective Corner-Based" "Silva10.pdf"` | No full-method recovery. DOI/index existence did not count as method verification. |
| Q-R12 | Direct current `iccad-contest.org/2025/` and `/2026/`, `tauworkshop.com/2018/contest.html`, `/2019/contest.html` | Current bounded contest inventory; full rule/hint/winner implementation audit unfinished. ICCAD2026 ceremony listed after cutoff; no future winner report claimed. |
| Q-R13 | Direct TAU2019 official slides: iTimer, TimeBoost, ParallelClosure | Checked worst-corner, incremental and MCMM graph/optimization ingredients. Full implementation comparison remains open. PDF metadata title for iTimer is misleading; slide text identifies team. |
| Q-R14 | Direct pinned OpenSTA raw DmpCeff.cc, README.md, TableModel.cc | Hashes in sources.json; checked DmpCap selection, table evaluator and mixed double/float operations. No downloaded code executed. Current OpenSTA overview read separately; no latest-head audit claimed. |
| Q-R15 | Direct public patent US8245167B1, claims 1-2/16-17 and Figures 16A-B | Branch-and-bound, setup/hold and parameter-model overlap. Claims do not establish product shipment; legal scope not adjudicated. |
| Q-R16 | Direct Synopsys PrimeTime and Cadence Tempus official product pages | Advertised signoff and scale capabilities; no performance comparison or proprietary absence inferred. |
| Q-R17 | Direct `https://api.crossref.org/works/10.1145/3816045` and `/10.1109/TCAD.2025.3581474` | Exact deposited metadata saved/hashed in external scratch. R10 has publisher abstract; R11 metadata only. DOI year is not automatically issue year. |

## Expansion and stopping assessment

Expansion A reopens the classical branch-and-bound and pruning lineage from the released proposer handover (SRC-R03/R05/R09), including nonlinear max bounds (SRC-R04) and TCAD2010 (SRC-R01). It reveals stronger overlap than the inherited broad novelty language. Expansion B uses clock-only/corner-estimation vocabulary, current predictor metadata and TAU official team reports; it reveals established multicorner/incremental ingredients and newly dated predictor records. These are substantive expansions, but they did not yield two clean no-closer-mechanism passes: several closer items were found and TCAD2010 remains unread. This search round stops at a bounded research release with residual risk, not an exhaustion certificate. Forward-citation completeness, full newer predictors and complete contest hints/winners remain TASK-01.

## Access, compute and provenance

The original four primary PDFs were read from downloaded bytes and exact text extraction. Only metadata, hashes, bounded method summaries and locators are released; no full copyrighted paper or restricted data is included. TCAD2010 direct routes failed; this is a source-access limitation, not an infrastructure-permission block. No authentication bypass, paid service, foreign private file, tool build, property run, STA execution, PDK acquisition or design generation occurred. The historical P3-P5 counts are explicitly inherited proposer evidence.

Current source descriptions use source IDs SRC-Rxx; no hidden retained bibliography is needed to trace the current claims. SRC-H01/H02 point to exactly released inputs and distinguish historical evidence from fresh reads. Source-method limitations are recorded in sources.json. Same-scenario bound soundness, useful coverage and cost remain hypotheses/inferences.

Local verification: required role-file presence, UTF-8/JSON/CSV parse, claim/source cross-reference and task hash consistency are checked locally; trusted role_submission.py freeze and verify validate the release. Full `scripts/project.py validate` is deferred to coordinator publication by prompt.txt because this packet excludes the full repository; the checkout was not read to satisfy a legacy rule. Structural validation is not scientific verification.


## Batch cycle 2 — independent source work, 2026-10-15 UTC

Input commit a48f03d4bc254c0b0957d0fe0f265e072d6cf49a; packet bd4911a04b3d7666d4304e869c785e479bbb5b5d9434f6fc18e777a6d9fe0fcb. Only own released prior/handover and the assigned adjudicated shared pair were inspected. Unblinded review; no inherited independence or acceptance. No foreign private material or checkout access. No experiment compute used.

| Query / route | Engine and filters | Inspected result / disposition |
|---|---|---|
| ISPD2026 buffering contest results winners; ISPD2026 IRISLab/PTSD algorithm variants | web search, primary organizer results followed | Official direct winners page and organizer GitHub/readme/rules v2.2; scoped current timing assumptions; winners named but full methods not obtained. Mirrored contest repository excluded as method evidence. |
| Efficient MCMM 2010 branch bound STA engine; A unified multi-corner multi-mode PDF Nian Tsai | web search then official ASP-DAC archive/institutional metadata | Official 30-slide presentation and program/abstract inspected, downloaded PDF hashed. Incumbent and linear-model BNB overlap; no full six-page paper or runtime adoption. |
| Effective Corner-Based Techniques Silva timing verification PDF | web search, original author PDF | Indexed abstract/intro available; web PDF retry timed out and direct HTTPS returned SSL EOF. Still no full-method comparison. |
| Multi-corner timing certificate pruning 2025 2026; timing analysis interval certified pruning Liberty | web search, no date exclusion | Results noisy; public sta-si implementation lead surfaced but method not inspected and not relied on. No novelty inference from absent closer results. |
| Interpretable Cross-Corner Timing Prediction full text | web search plus official ACM DOI | Secondary discovery abstract not used for method claims; primary ACM fetch failed. Full-method guarantee/fairness remains open. |
| Backward mechanism check from current BNB lead | official ASP-DAC slides references; reopen SRC-R03/R04/R09 | Read affine exact/sufficient pruning, nonlinear closure/boundedness/extrema conditions, and public patent text; no claim that these implement PS-02 reports. |
| Direct pinned DmpCeff.cc and TableModel.cc reads | public raw upstream GitHub, exact commit | Downloaded/hash-matched sources; read DmpCap, setCeffAlgorithm, gateModelRd and Table2::findValue; whole IEEE/scaling/tag proof explicitly not supplied. |
| Current ISPD program/results links | official mutable page and outgoing links | 2027 header/2026 body; contest link returned 2025 path and oversized PDF failure; closing slides explicitly2025. Do not silently relabel as2026 winning method evidence. |
| Organizer snapshot/rights | public GitHub API/raw exact commit after discovery | Main resolved f7b29d242fc7d441f3b4eadc556f40099ccca067 (commit timestamp2026-05-03); pinned README/LICENSE/PDF downloaded, hashes in sources. Per-asset licenses not audited and no data generated. |

Two substantive expansions (classical BNB/nonlinear neighborhood and current contest/winner/data neighborhood) added relevant overlap and a dataset exclusion; they did not establish search closure. Search stopped at the bounded role-turn evidence budget with explicit remaining TCAD2010, recent full methods, winning-code and current-implementation gaps. This is budget exhaustion, not an exhaustive novelty certificate.

All downloaded copyrighted paper/code originals remained in private external scratch; release contains metadata, hashes, bounded paraphrases and our analytical derivation. No credentials, proprietary designs, restricted PDKs or full copyrighted papers are released. No access restriction was bypassed.

Analytical work: PS-02/TR-02 computes equal-information bounds and shows P/B1+ conditional equivalence by induction. No STA/Liberty fixture was run; numerical examples are stipulated exact rational values for the proof. Source read/metadata retrieval and structural Python validation do not imply experiment allocation.
