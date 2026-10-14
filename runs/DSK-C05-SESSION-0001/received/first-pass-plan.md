# First-pass plan — challenger

**Actor:** `DeepSeek-C05-TIMING` (call sign `DSK-Forge-TIMING`), role challenger, domain D05 TIMING.
**Topic:** EDA-0002 — "Sound per-(endpoint, scenario) screening for multi-corner STA with exact refinement" (proposal by `Claude-P05-TIMING`).
**Input:** packet `e6c53f61ca815c2e69c1ab2f68cb2c667290f634cc49ea4ff5900d8e535332cf`, input commit `4b666c04b0eaa089934f736fab4db2309ce7d36a`, verified 2026-10-12T18:39:19Z with 30 of 30 listed hashes OK.
**Status:** onboarding turn. No web survey, no tool runs, no `forecast.json` exposure (withheld by `docs/ISOLATION.md` line 16). Everything below is a **plan**, an explicitly labeled **subjective prior**, or an **investigation target** — not a finding and not an objection.

Labels: **[PLAN]** planned action · **[FCST]** subjective prior · **[TGT]** investigation target, unverified · **[INF]** inference from packet content · **[OBS]** observation from packet content or from my own recomputation of stated numbers.

---

## 1. What I hold, and what I deliberately do not

**Held** [OBS]: the frozen dossier at round 0 — `proposal.md`, `sources.json` (SRC-001…SRC-052), `prior-art.csv`, `search-log.md`, `contest-audit.md`, `industry-gap.md`, `experiment-plan.md`, `tasklist.md` (proposer draft, "Challenger additions (pending)"), `direction-control.json` (penalties 0/0, initial anchor), `experiment-consensus.json` (status `pending`, all readiness checks false), `dossier.json` (status `submitted`, challenger and verifier sessions null), and `challenges.md` (title-only placeholder).

**Withheld or not yet produced** [OBS]: `forecast.json` is absent, so no proposer headroom estimate has been exposed to me. That is the condition under which §2 is written.

**Not read this turn** [OBS]: `docs/EXPERIMENTS.md`, `docs/FORMATS.md`, `docs/GITHUB.md`, `docs/PHYSICAL-PILOT.md`, `templates/run.json`, `config/physical-resources.lock.json` (hashes verified, contents not read). They are cited by the dossier but are not in the common-policy set named by `AGENTS.md` line 5. Flagged for the coordinator in §11.

**Method constraint** [OBS]: `config/launch-release.json` line 71 sets `experiment_authorization` false; no experiment may start before promotion and task-list consensus. My challenge work in the research round must therefore be source-based and analysis-based, with any experimental proposal expressed as task-list items for joint signature.

---

## 2. Independent headroom estimate before forecast exposure

Required by `harness/CHALLENGER.md` line 7 ("Before viewing proposer forecasts, independently estimate plausible headroom and record assumptions"). Recorded now, with no proposer numbers seen.

### 2.1 Cost decomposition I will use [INF]

Let K = |S|. Write the reference cost as

    T_B0  ≈  C_fix  +  K · ( c_search + c_dcalc )

where `C_fix` covers process start, netlist/SDC/SPEF read, graph build, levelization, library read of the K scenario libraries, and report writing; `c_search` is the per-scenario arrival/required propagation and search; `c_dcalc` is the per-scenario exact delay calculation (iterative Ceff solve plus table evaluation per arc).

The candidate's cost, if everything works as proposed, is

    T_P  ≈  C_fix  +  K · ( c_clock + c_bound )  +  Σ_s  c_refine( U_s )  +  c_lib

with `c_bound = ρ · c_dcalc` over the arcs in the bound pass, `U_s` the uncertified (endpoint, scenario) set, and `c_refine` chargeable only to the fan-in cones.

The oracle screen O (`experiment-plan.md` § Baselines) gives the ceiling:

    R_max(K)  =  1 − ( C_fix + K · ( c_clock + c_refine(below-M triples) ) ) / T_B0

### 2.2 Assumptions behind my prior (each one testable, none yet verified)

- **A1.** K-scenario OpenSTA runs share graph build and levelization, so `C_fix` is amortized over K; `C_fix/T_B0` falls as K grows and as the design grows. On a small fixture like the packet's GCD, I expect `C_fix` and library read to be a large share.
- **A2.** The bound pass costs a non-trivial fraction of exact delay calculation. Evaluating a table over a box requires the box corners, the in-box grid points and the edge crossings — for typical 7×7 or 8×8 NLDM tables that is many interpolated evaluations per arc, against one lookup plus a few Ceff iterations for the exact path. I treat ρ ∈ [0.2, 1.5] as the plausible range and regard ρ as the single most important unknown for the speed claim.
- **A3.** The certificate band accumulates along a path. Each stage contributes a per-stage band ε between the bound and the exact arrival, so a path of depth d carries roughly ε·d before any per-stage cancellation. Certification at margin M requires the true slack margin to exceed the accumulated band. Deep paths therefore certify less than shallow ones at equal per-stage tightness.
- **A4.** Clock-network band is removed by the exact clock pass (mechanism step A). Whether that is sufficient depends on the data-network band alone, which is the object of A3.
- **A5.** `c_refine` scales with the number of uncertified endpoints and the size of their fan-in cones, not with the full graph, which is the mechanism's core economy claim.

### 2.3 My estimate [FCST]

Subjective, no evidence, recorded before exposure:

| Quantity | Point | Plausible 80% interval |
|---|---|---|
| R at M = 0, K = 3, small fixture | 5–10% | 0% to 20% |
| R at M = 0, K = 3, larger designs (aes/jpeg/ibex scale) | 10–15% | 0% to 30% |
| R at M = 6–16, larger designs | 20–30% | 5% to 50% |
| ρ (bound-pass cost / exact delay-calc cost, per arc) | 0.6 | 0.2 to 1.5 |
| P(H1 as preregistered: R ≥ 20% on ≥ 3 designs per set, decisions exact) | 0.25–0.35 | 0.05 to 0.6 |

**Conditions that would move me up**: measured ρ < 0.3; a measured certification rate above ~80% per scenario at M = 0; `C_fix/T_B0` below ~20% on the evaluated designs; a measured per-stage band ε small relative to the slack distribution's mass near zero.
**Conditions that would move me down**: ρ close to or above 1; band growth with depth that consumes the margin mass; certification concentrated in scenarios that are already cheap; `C_fix` dominating on the available small designs; library read of K scenario libraries being a large irreducible block.

**Why this prior matters for the plan** [INF]: it makes two cheap measurements decisive *before* any implementation — the phase-decomposed B0 profile (§5, §7 CA-1) and the per-stage band ε with the path-depth distribution (§7 CA-2). If those two measurements predict R < 20% on the available sets, the topic stops at K3 without writing a line of the fork. I will state this prior, its assumptions and any later revision of it in my own files, and I will not revise it after seeing the proposer's forecast without recording the revision as post-exposure.

---

## 3. Nearest-work search strategy [PLAN]

Ordered by decision weight. Item 3.1 is the kill-criterion path (K1) and comes first.

### 3.1 Decision-critical reads

1. **SRC-012** — Onaissi, Taraporevala, Liu, Najm, "A Fast Approach for Static Timing Analysis Covering All PVT Corners" (DAC 2011 per filename and search metadata; DOI unverified). The proposer saw only excerpts; four fetch attempts failed (`sources.json` SRC-012; `search-log.md` § Access limitations). If this paper already bounds each discrete scenario soundly against table-level semantics and refines exactly, the candidate collapses under K1.
   Routes to try, in order: the author/institution copies on the two Toronto hosts already recorded; a Wayback Machine snapshot of the same URL; IEEE Xplore metadata and any open PDF; Unpaywall/OpenAlex/Semantic Scholar open-access copies; the Najm group publication list; citation-following from later papers that cite it (SRC-014's slide list is one such path).
   What I must extract: the delay model actually assumed, whether the bound is per discrete corner or over a parametric space, whether the bound is sound against characterized table semantics or against an analytic model, how hold is handled with clock-only runs, and whether any exact refinement of uncertified work exists.
2. **SRC-013** (Onaissi & Najm, linear-time all-corner, ICCAD 2006 / TCAD 2008) — same lineage, linear-parametric assumption.
3. **SRC-014** (Nian, Tsai, Huang, unified MCMM engine, ASP-DAC 2010 slides) — branch-and-bound exactness relative to a linear model; check chronologically and check its experimental section, which the proposer did not inspect.
4. **SRC-016** (IBM US7681157B2) — check the *actual* cutoff rule, because the proposal's constructed counterexample (CLM-017) attacks an anchor-relative slack cutoff; the patent describes per-parameter cutoffs estimated empirically. Whether the strawman matches the patent is a fairness question for baseline B2 (§5).
5. **Heloue DATE07 and Heloue TCAD12** — recorded as unfetched leads by the proposer (`search-log.md` § Excluded items). Parameterized timing covering all potentially critical paths is adjacent to the claimed distinction.
6. **Patents US11755807 and US11295057** — recorded as unfetched prediction patents; must be read before any "no formal guarantee in prior art" statement is accepted.
7. **The SSTA bounds-and-refinement lead** (`search-log.md` Q12, a Berkeley-hosted paper; not inspected). Bound-and-refine is a claimed novelty ingredient; the SSTA literature is where it most likely already exists in some form.

### 3.2 Contest-hint and prior-solution reads

See §4 for contest checks; they are listed separately because `docs/CHARTER.md` line 13 treats contest originality as an independent gate.

### 3.3 Query families and terminology variants

I will run each family on at least two independent engines and record query, engine, date, filters, inspected result and exclusion reason per `docs/EVIDENCE.md` lines 9-11.

- **Screening / reduction vocabulary:** multi-corner reduction, scenario reduction, view reduction, corner pruning, corner set minimization, dominant-corner selection, worst-case corner identification, corner ranking, sign-off safe reduction.
- **Soundness vocabulary:** certified, provable, guaranteed, sound bound, conservative bound, no missed violation, zero false negative, decision equivalence, exact refinement, bound-and-refine, lazy refinement, speculative analysis with fallback.
- **Model vocabulary:** interval bound, affine arithmetic, parametric timing, linear delay model across PVT, monotonicity assumptions, temperature inversion, non-monotone corner dominance.
- **Engine vocabulary:** static timing analysis acceleration, multicorner engine, block-based timing bound propagation, incremental timing, slack margin propagation.
- **Adversarial vocabulary my prior suggests:** "band accumulation", "bound width growth with logic depth", "over-conservative interval timing", papers that report *failure* of interval/parametric bounds.
- **Chronology filter:** 2024-01-01 to present for the refresh required before promotion (`search-log.md` § Pre-promotion novelty refresh items (c) and (d)).

### 3.4 Forward-citation expansion

The proposer could not run forward citations (Semantic Scholar HTTP 429, DBLP bot wall, Google Scholar not attempted — `search-log.md` § Access limitations). Forward citations of SRC-012, SRC-013, SRC-014, SRC-016 and SRC-017 are the highest-yield unrun search, because the claimed gap is a *guarantee* gap and any later paper that supplies the guarantee would be in those lists. I will attempt: OpenAlex, Semantic Scholar with backoff, Crossref cited-by, IEEE Xplore citation lists, and patent citation/reference sections (patents cite papers and later patents reliably).

### 3.5 Version, chronology and language checks

For every kept source: publication year and venue, any revised version, retractions or corrections, and whether a later version changes the mechanism. The proposer flagged that the Chinese- and Taiwanese-language thesis literature on MCMM was not searched (`search-log.md` § Residual risk item 4); I will add at least one documented attempt with the appropriate terminology, and report access limits honestly.

### 3.6 Stopping rule and records

Stop a search round only after two documented expansions reveal no closer mechanism, or on access exhaustion with the residual risk reported (`docs/EVIDENCE.md` line 13; the proposer used the second ground, which leaves the residual risk open and is exactly what I am here to close). New sources are appended to my own evidence file with stable IDs continuing the proposer's numbering; the proposer's records are never rewritten (`harness/CHALLENGER.md` line 16).

---

## 4. Contest-hint checks [PLAN]

- **TAU 2018 and 2019** — unresolved (login wall) and explicitly named in the proposal's U8 and in `contest-audit.md`. Routes: the tauworkshop.com archive, Wayback snapshots of the contest pages, ISPD/TAU slide decks, and any contest GitHub mirror. If either concerns multi-corner screening, the audit must be revised before promotion.
- **TAU 2013 winner methods** — `contest-audit.md` § Winner methods records that they were not retrieved. Parametric all-corner analysis is the contest-provided idea nearest to this candidate; I need the winner report to judge whether the anchor is a new limitation beyond the given idea or a re-derivation of it.
- **TAU 2015 / ICCAD contest baselines** — already excluded slice S1 by the proposer; I will re-check only that the exclusion still holds under the anchor as written.
- **Pinned-engine check** — independently repeat the proposer's repository check that the pinned OpenSTA at `e01d3f163f483f233db00410b6515a767a6ca03b` has no scenario-reduction, dominance or corner-pruning command, using my own query set over the Tcl command surface and the search/documentation tree. A found command would change both the novelty and the "integration gap" framing.
- **Gate to apply** (`docs/CHARTER.md` line 13): implementing a supplied baseline, an organizer hint or a known winner approach is not a research contribution by itself.

---

## 5. Critical baseline comparisons [PLAN]

The proposal's baseline table is B0 (pinned OpenSTA, all scenarios in one run), B1 (one run per scenario), B2-B4 (estimated/learned screens with exact fallback), B5 (naive dominance), O (oracle). My audit plan:

1. **Is B0 the strongest exact baseline at equal resources?** [TGT] Verify that B0 runs all scenarios in one process with shared graph build, that thread settings are identical across configurations, and that a per-scenario loop (B1) is genuinely slower. If B1 ≈ B0 on the available designs, the fixed-cost argument in A1 weakens and the whole speed claim changes shape. This is cheap to check with B0/B1 logs alone.
2. **Equal-budget rule direction** [TGT] `experiment-plan.md` § Baselines states that B2-B4 guards and cutoffs are chosen so each baseline's runtime is ≤ T_P on the calibration designs, and that false negatives are then compared at equal or lower cost. That construction makes the prior-art baselines *slower-equivalent but cost-capped*, which can understate a well-tuned prior screen. I intend to require a second, fairer comparison: tune B2/B3/B4 for **zero false negatives on the calibration designs** without a cost cap, then report their false negatives and cost on the test designs. H3 should survive that, or it is not established.
3. **Strongest naive composition** [TGT] The proposal names four naive compositions it beats, but the strongest realistic competitor may be missing: a *spread-based screen* that runs 2-3 anchor scenarios exactly, measures the observed cross-corner slack spread per endpoint, and refines exactly whenever the anchor slack is within a calibrated guard of the spread — a screen with exact fallback and no certificate. I intend to propose it as an added baseline (CA-3 below) because it is cheap, obvious, and directly tests whether *soundness* buys anything over *calibrated estimation with exact fallback*.
4. **Oracle bookkeeping** [TGT] O is intended as an upper bound on attainable R. Verify that O's cost includes the same clock pass, the same refinement machinery and the same report writing as P, otherwise O overstates the ceiling and K3 becomes unfalsifiable.
5. **Flag-off bit-identity** [TGT] `experiment-plan.md` requires the fork with the flag off to reproduce B0 bit for bit. That is a code-equivalence control, not a decision-equivalence control; both must be reported separately, and `compare_decisions.py` must be shown to *detect* a seeded mismatch before it is trusted (CA-6).
6. **Memory** [TGT] G5 caps peak RSS at 1.25× B0 (provisional). Per-(endpoint, scenario, check) certificates and bound arrays for K scenarios are a plausible RSS risk that the plan measures but does not bound analytically; I will ask for the certificate storage form and a worst-case estimate before the pilot.
7. **Cost accounting honesty** [TGT] EXP-001 generation cost (P&R, Liberty conversion) is planned to be reported separately from per-analysis cost, which is correct; I will additionally require the *amortization statement*: for how many closure iterations and how many scenario sets must the one-time cost be amortized before the total is a win.

---

## 6. Causal-mechanism attack plan [PLAN]

Targets, not objections. Each becomes an `OBJ-NNN` only when I can attach a source locator or an experimental result, per `harness/CHALLENGER.md` line 16 and `docs/EVIDENCE.md` lines 15-17.

- **A-1 Envelope soundness of P1/P2** [TGT] Re-read the pinned code myself (download and re-hash the same files the proposer hashed) and check the *complete* set of delay-calculation paths, not just the `DmpPi` path: `DmpCeff.cc` (`DmpPi`, `DmpCap`, `DmpZeroC2`, fallbacks), `LumpedCapDelayCalc.cc`, and the 3-D table path in `TableModel.cc` (the proposer's own limitation notes flag 3-D tables and the lumped-cap path as unread).
- **A-2 The slew question (P3)** [TGT] The highest-risk property. Check every source of the slew that the reference passes downstream: table value, waveform-model value, `slew_derate_from_library` or equivalent derating, and input/output threshold percentages in the library. If any of these can make the reference slew exceed a bound computed from slew tables alone, the certificate is unsound on that path. I want the audit to enumerate these sources explicitly and to record, per source, whether the bound covers it.
- **A-3 The Elmore claim (P4)** [TGT] The single-pole crossing in the pinned code is a numeric procedure with thresholds, iterations and fallbacks. Check whether the returned load delay is always ≤ the Elmore delay of the same reduced model, and whether the theorem's conditions (the input-waveform class in SRC-026, which the proposer read only at metadata level) cover the waveform shapes the engine actually produces.
- **A-4 Load-slew bound (P5)** [TGT] Same structure as A-2 for the downstream load slew.
- **A-5 Refinement exactness / global effects (CH5)** [TGT] Test whether restricting the reference engine to fan-in cones preserves exact slacks in the presence of clock tags, CRPR, generated clocks, path groups, `set_multicycle_path`, `set_false_path`, input/output delays at ports, unconstrained endpoints and the incremental machinery. The proposal lists CH5 as a counter-hypothesis; EXP-004 must contain adversarial unit netlists for each of these, not only the happy path.
- **A-6 Clock-pass economy and side effects** [TGT] Mechanism step A assumes a clock-only pass is cheap and isolable. Verify the clock network's runtime share on the evaluated designs and check that a clock-only search does not perturb CPPr or arrival state used by the refinement pass.
- **A-7 Bound-pass cost reality (ρ)** [TGT] See A2/§2. Require a *measured* ratio of bound-pass work to exact delay-calc work per arc and per scenario, plus the count of table evaluations per arc. A5 (monotone shortcut) probes part of this; I want the raw cost, not only the ablation delta.
- **A-8 Definitional edges of D_M(S)** [TGT] Check the hold and recovery/removal bound formulas for sign and threshold convention, check that "exact slack below M" plus "violation flag" is fully implied by the certified/refined split, and check the treatment of endpoints with no valid path, unconstrained clocks and `set_data_check`. Also confirm the M = 5% of period sensitivity is defined against the same clock for every scenario.
- **A-9 Boundary with D04** [TGT] The anchor claims ECO planning consumes exactly the decision set. `domains/D05/brief.json` line 7 puts physical ECO in D04 while D05 owns signoff validity. Whether the anchor's downstream-need statement overreaches into another domain is a framing question I will check in `responses`-adjacent analysis, not a mechanism attack.

**Recomputation already done this turn** [OBS]: I re-derived the CLM-017 counterexample arithmetic from `proposal.md` § L3. Anchor slack = 800 + 600 − 300 − 1000 − 50 = +50 ps; scenario s slack = 800 + 400 − 296 − 992 − 50 = −138 ps; the 25 ps cutoff rule skips the violating triple. The arithmetic is internally consistent. What it does *not* establish is that the rule it attacks is the one the cited prior art actually implements, and whether the wire-dominated capture structure occurs in the evaluated designs — both are §5/§6 targets.

---

## 7. Saturation and utility targets, with the tests that would refute my own concern [PLAN]

For each candidate concern I state the test that would show the concern is empty, so my objections stay falsifiable.

- **S-1 Fixed-cost ceiling.** Concern: on small designs and small K, `C_fix` plus the K-library read leaves less than 20% on the table regardless of mechanism quality.
  **Refuting test:** B0 phase profile shows per-scenario variable cost above ~60% of T_B0 at the evaluated K, and the oracle ceiling R_max(K) computes above 20% on at least 2 of 3 designs per set. Cheap, needs no implementation, and it is the K3 gate the plan already contains — I will require the phase decomposition to actually separate parse, graph build, library read, delay calc, search and report per scenario.
- **S-2 Band accumulation.** Concern: the certificate band grows with logic depth (A3), so certification at M = 0 is low exactly where slack margins are thin.
  **Refuting test:** measured per-stage band ε and the measured distribution of margins and depths give a predicted certification rate high enough to clear 20% on the evaluated designs; and a measured correlation between band width and depth that is weak or absent.
- **S-3 Non-dominance premise.** Concern: the benefit story assumes each endpoint is tight in only a few scenarios (SRC-019 p. 8 as quoted by the proposer). On the available open scenario sets — ASAP7 FF/SS/TT with one RC corner, SKY130 up to 16 PVT corners with one RC corner — the premise may hold for a different reason than in the cited industrial data (no RC-corner variation at all), which weakens transfer of the industrial evidence to this benchmark.
  **Refuting test:** B0 data show a per-endpoint worst-scenario distribution with real spread across scenarios, and the oracle-certifiable fraction is high in non-dominant scenarios; the benchmark's scenario diversity is then sufficient for the mechanism's premise.
- **S-4 Utility threshold.** Concern: the 20% threshold is declared provisional by the brief itself (`config/research-brief.json` line 77-78) and no practitioner input exists yet (U9); a pass at exactly 20% on a small fixture may not be a meaningful engineering improvement.
  **Refuting test:** practitioner input or a documented workflow argument tying wall-time reduction to closure iterations; and total-cost accounting (§5 item 7) that shows a net win including prerequisite generation.
- **S-5 Safety contrast (H3) may be vacuous.** Concern: on open corner sets, even a naive dominance rule may miss nothing (CH3 in the proposal), so H3 is untestable and the *purpose* of the guarantee is undemonstrated on the available data, while remaining real on industrial data that this pilot cannot access.
  **Refuting test:** a negative control (CA-5) in which at least one heuristic screen demonstrably misses a violation on an evaluated configuration, plus a count of CLM-017-style structures in the designs. If the refuting test fails, the honest outcome is a reported negative result, not a stronger claim.

---

## 8. Falsification tests and fairness controls I intend to propose for `tasklist.md` [PLAN]

`tasklist.md` reserves a "Challenger additions (pending)" section and `docs/CHARTER.md` line 28 makes my additions a precondition of consensus. Sketches below; final text, owners, artifacts and pass/fail criteria to be written into the task list and signed only after my source search.

| ID | Addition | Owner | Artifact | Pass/fail sketch |
|---|---|---|---|---|
| CA-1 | Oracle headroom gate from phase-decomposed B0 profiling only, before any implementation | C computes from P's B0 logs; P runs | `headroom-oracle.csv` | Fail (K3) if R_max < 20% on ≥ 2 of 3 designs for every available set |
| CA-2 | Band-accumulation probe: per-stage band ε vs. the margin/depth distribution, using the EXP-002 bound rules in a standalone script | C specifies; P runs | `band_depth.csv` | Concern S-2 stands unless predicted certification clears the required rate |
| CA-3 | Strongest naive composition: spread-based screen with exact refinement and calibrated zero-FN guard | C specifies; P implements | baseline script + results | H3 must hold against this baseline, not only against weaker ones |
| CA-4 | Fair prior-art tuning: B2/B3/B4 tuned for zero false negatives on calibration designs with no cost cap, cost reported | C specifies; P runs | `baselines-fair.csv` | If a tuned prior screen reaches zero FN at cost ≤ T_P, H3 fails as stated |
| CA-5 | Negative control: a fixed-cutoff screen and a dominant-corner screen must be *shown* to miss at least one violation somewhere, or H3 is reported as not demonstrated | C | `negative-control.csv` | Any screen with zero FN everywhere ⇒ negative result recorded, not silence |
| CA-6 | Decision-diff tool validation: seeded single-violation mismatch must be detected; checker audited independently of its author | C | `compare_decisions_selftest.log` | Tool must fail-closed on the seeded case |
| CA-7 | Slew-source audit: enumerate every slew source (table, waveform model, derate, threshold pct) and record bound coverage per source | P derives; C attacks | `slew_audit.csv` | Any uncovered source is a K2 candidate |
| CA-8 | Global-effect unit tests for cone-restricted refinement: generated clocks, CRPR, multicycle/false paths, port delays, unconstrained endpoints | P implements; C specifies cases | test log | Any mismatch triggers S2 |
| CA-9 | Hold-specific falsification configuration, given the prior-art statement that hold resists small corner-set bounding | C specifies | results row + negative-result record if no hold violation exists in the designs | Hold guarantee must be tested, not assumed |
| CA-10 | Equal-treatment audit from raw logs: identical container limits, threads, input hashes; run interleaving; no post-hoc threshold edits | C | `fairness-audit.md` | Any deviation recorded as a protocol violation |

Each item must end up with an owner, an executable procedure, an expected artifact and a pass/fail criterion before I sign (`harness/CHALLENGER.md` line 19).

---

## 9. Evidence discipline for my own objections [PLAN]

- Objections are `OBJ-NNN` with: targeted claim ID, severity, source IDs and locators, factual evidence, the inferential bridge, confidence, the conditions that would invalidate the objection, and the cheapest decisive test (`harness/CHALLENGER.md` line 16).
- Severity buckets to be used explicitly: fatal contradiction, major fixable, minor, open question (`harness/CHALLENGER.md` line 17).
- Facts, inference, hypothesis and forecast stay in separate labeled blocks (`docs/EVIDENCE.md` line 7). A vendor statement is evidence about advertised practice only. A patent is evidence about a described method, not about performance.
- Unavailable sources stay `unresolved`; I will not characterize the contents of anything I could not open.
- I will accept corrections to my own objections and record supersessions rather than deleting them (`harness/CHALLENGER.md` lines 22-23; `docs/WORKFLOW.md` line 18).
- I will score `combination_drift` and `demand_drift` on each substantive revision against the frozen anchor in `direction-control.json`, and I will not push the proposer toward a technique of my own preference (`harness/CHALLENGER.md` line 18).

---

## 10. Sequencing for the research round [PLAN]

1. K1 read of SRC-012 and its lineage (SRC-013, SRC-014, Heloue leads) — everything else is provisional until this lands.
2. Re-verify the packet's code claims against the pinned commit by fetching and re-hashing the same files; record my own locators.
3. Run the forward-citation and 2024+ refresh searches; append new source records.
4. Close or reopen the contest-audit gaps (TAU 2018/2019, TAU 2013 winners).
5. Draft `OBJ-NNN` entries only for concerns that survive steps 1-4, with locators and decisive tests.
6. Draft the `tasklist.md` additions (CA-1…CA-10) with owners, procedures, artifacts and pass/fail criteria.
7. Record my independent headroom prior revision *before* any forecast is viewed; escalate to the coordinator, not to the proposer.
8. Submit everything through my outbox as an output packet. No approval, no merge, no direct contact.

---

## 11. Boundaries honored this turn, and residual uncertainty

**Honored** [OBS]: only the frozen packet and my own outbox were read; no other actor's files, no repository checkout, no other role harness, no shared memory; no network request; no experiment; no messaging; writes confined to `readiness.json` and `first-pass-plan.md` in my outbox.

**Residual uncertainty in this plan**:

1. I have not seen the proposer's `forecast.json`; §2 is my pre-exposure prior and may be revised only with a dated post-exposure record.
2. All headroom numbers in §2 are subjective priors with unverified assumptions (A1-A5), stated so that the proposer and verifier can falsify them.
3. No source has been opened by me; every prior-art statement above is either quoted from the packet with a locator or explicitly marked as an unverified lead.
4. `docs/EXPERIMENTS.md`, `docs/FORMATS.md` and `docs/PHYSICAL-PILOT.md` were left unread pending a coordinator ruling on whether they belong to the common policy; the dossier cites them for consent, manifest and pilot rules that will matter at signature time.
5. Network access, compute and PDK/design access for the research round are unconfirmed; `domains/D05/brief.json` lines 43-45 state that this packet authorizes no broad research run, so §3-§8 are a bounded plan awaiting authorization rather than an executed search.
