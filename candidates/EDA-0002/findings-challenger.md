# Challenger findings

**Actor:** `DeepSeek-C05-TIMING`, challenger, D05, EDA-0002. **Round 1.** Written 2026-10-13T11:23Z.
**Nature of this file:** resolved unknowns and source-level findings that are *not* objections. Objections live in `challenges.md` and require verifier adjudication before they block anything. Findings here are statements I can support from sources I inspected; they carry the same evidence burden as proposer claims (`docs/CHARTER.md` line 12).

---

## F-1. Kill criterion K1 is **not** triggered by SRC-012 (full text read)

**Question tested.** K1 as the proposer defined it: "A nearest-work full-text check (SRC-012 or another found source) shows per-scenario sound certification with exact refinement already exists" (`proposal.md` § Kill and stop criteria). The proposer flagged SRC-012 as the single most decision-critical item (U1) and could not open it (four timeouts; `sources.json` SRC-012).

**Source state.** I read the full text of the author-hosted DAC 2011 paper this round (records C-A01, C-A02; retrieval route and fidelity caveat in `search-log-challenger.md`).

**Evidence.**

1. **Setup is empirical coverage with a margin, not a certificate.** §2.2 defines dominance, coverage, dominant set and a *dominance margin* that explicitly relaxes exact worst-case capture. §5.1 supports the slow-corner practice by measurement: coverage of the two slow corners `CM = {c14, c15}` is 99.9% at a 30 ps margin, 97.9% at 10 ps, and the weakest circuit (T4) is 87.6% at 0 ps (Table 8). The claim is phrased as a reasoned expectation — worst-case setup slacks are "expected to occur" at the corners with the largest signal arrivals — and the paper reports results restricted to the top-25% worst-slack endpoints.
2. **Hold is an estimate with a published error term, not a bound.** The method runs full STA at an anchor corner and clock-network-only partial runs at the other corners, then estimates the slack change as the clock-skew change (Eqs. 8-10). The discarded terms are the datapath-delay change and the required-hold-time change (Eq. 11); usefulness requires `e_d > 0`; the estimate is optimistic when the datapath delay shrinks. Measured behaviour: coverage falls to 92.1% on T5 with SI (Table 12); conservatism mean about −1 to −2 ps with worst cases about −26 to −38 ps, described as "can be conservative by up to −40ps" (§6.2.3).
3. **No exact refinement anywhere.** No fallback to full analysis for uncertain endpoints or corners is described; the natural remedy — evaluating worst slacks from several startpoints at the anchor — is explicitly dismissed ("such a solution is not necessary", §6.1).
4. **Scope is explicitly weaker than the proposal's.** The method targets non-final STA runs and optimization iterations; at sign-off the authors say additional corners are added (§1, §7). The paper makes no exactness or guarantee claim; the word "guaranteed" appears only in the negative sense that any corner set guaranteed to bound hold slacks must be large.

**Reasoning bridge.** The proposal's claimed distinction has three parts: (i) a certificate computed from each scenario's own characterized tables and parasitics; (ii) soundness with respect to the reference calculator's semantics, with no parametric or monotonicity model; (iii) exact refinement of uncertified triples so the reported decisions equal full analysis. The evidence above shows SRC-012 satisfies none of the three: its setup screen is a margin-based empirical coverage claim, its hold screen is an estimator with a documented error term and documented misses, and it refines nothing. Its own reported numbers (92.1% coverage in one SI case; underestimation up to −40 ps) are direct evidence that it is not decision-exact relative to full multi-corner analysis.

**Conclusion.** On the inspected evidence, SRC-012 does **not** already contain per-scenario sound certification with exact refinement. K1 is not triggered by SRC-012. This resolves the proposer's U1 in the candidate's favour and removes the top-listed residual risk in `search-log.md` § Residual risk item 1.

**Confidence and limits.**
- High confidence that SRC-012 is not a decision-exact method: the paper's own error analysis and coverage percentages are inconsistent with exactness, and this reading does not depend on subtle wording.
- Medium-high confidence on exact quoted wording, because the read went through a text-extraction proxy plus question passes (C-A01 `access_caveat`). The verifier should confirm the two or three sentences that will carry weight in the final record against the original PDF or the publisher copy.
- **K1 remains open against other sources.** This finding covers SRC-012 only. The kill criterion names "SRC-012 or another found source", and my forward-citation and 2024+ searches are not complete. In particular, SRC-013 (the same authors' linear-time all-corners work) is still unread by me.
- This finding does **not** establish novelty. It removes one specific collapse condition; it says nothing about commercial internals, unpublished work, or the other nearest sources.

**Conditions that would reverse this finding.** (a) An extraction error that hides a sound-bound construction or a refinement step in the paper; (b) evidence that the "dominance margin" is applied adaptively as a certificate rather than as a relaxation; (c) the appearance of another source that supplies the same guarantee and refinement (would trigger K1 independently).

---

## F-2. Observations from the same read that bear on my planned objections

Recorded now because they will shape `OBJ-` entries; **none of these is yet an objection.**

1. **Support for the demand premise, at M = 0.** At zero margin, even the best classical slow-corner screen misses endpoints: T4 coverage is 87.6% at 0 ps (Table 8), and hold coverage with SI drops to 92.1% on T5 (Table 12). This is independent evidence (industrial 45nm, commercial flow) that estimated/dominance screens are not decision-exact — which is the proposal's L1 and CLM-002, and it is now sourced at full-text level instead of abstract level.
2. **A tension with high-margin usage.** The same paper argues that at a 30 ps margin the slow-corner screen is "more than adequate" for non-final runs (§5.1, §7). The proposal's primary evaluation is at M = 0, where this argument does not apply; its secondary margin (5% of the clock period, e.g. 50-200 ps in Table 5's clock periods) is *larger* than the margins at which SRC-012 claims adequacy. Worth watching: if the pilot's benefit is concentrated at large M, the utility case weakens, because prior practice already covers large margins.
3. **Cost premise for the clock pass gains a locator.** Partial clock-only runs took 9.0-25.3 s against full runs of 490.9-2466.6 s (Table 14), i.e. roughly 1-5% of a full run per corner in that industrial setting. This independently supports the proposal's mechanism step A (exact clock pass is cheap) — and, by contrast, sharpens the open question about the *data-network bound pass*, which has no analogue in SRC-012 and whose cost is my ρ concern.
4. **Benchmark-transfer limitation, in both directions.** SRC-012's corners are 3 device settings × 5 *interconnect* settings; RC and C variation is central to its findings. The packet's open scenario sets have exactly one RC corner per platform (`experiment-plan.md` § Datasets). So the industrial evidence that estimated screening misses violations transfers only partially to the pilot's corner sets, and the pilot's H3 safety-contrast result would not transfer back. This is a limitation of the *demonstration*, not of the mechanism.
5. **Boundary of the nearest work is now sharper.** SRC-012 reuses the clock-only partial run (an ingredient the proposal openly borrows) and states that the setup-side small-corner bound is empirical. That makes the proposal's distinction a *guarantee* distinction rather than an ingredient distinction — consistent with the proposal's own framing, but it also means the novelty rests on the soundness properties P2-P5 (the proposal's own central risk) and on exact refinement, not on the flow structure.

---

## F-3. SRC-013 (the parametric linear-time companion) is explicitly non-conservative end to end

**Source state.** Full-text-level read of the author-hosted TCAD 2008 paper (record C-A06); the proposer had it as metadata only.

**Evidence.** Delays, arrivals and slews are affine linear functions of normalized process parameters at ±1, reducing the space to 2^n discrete corners. The internal max operation is proven conservative by construction — a hyperplane ceiling intended never to underestimate the maximum delay or slew at any corner. But the authors state that the *linearized interconnect delay, slew and effective-capacitance inputs* are not conservative and may underestimate values at certain corners; accuracy is verified empirically afterwards on ISCAS '85 with a 90nm library (roughly 6-7x speedup over corner analysis). No slack formulation is developed, and there is no exact refinement or per-corner fallback; the minimum-overestimation hyperplane is rejected as exponentially expensive in favour of a linear-time heuristic.

**Consequences.**
1. The nearest *parametric-bound* prior art does not supply a sound certificate against the reference engine's semantics; it is structurally the same class the proposal distinguishes itself from, now with a full-text locator rather than an abstract-level guess. This disconfirms a lingering novelty risk (good for the proposal) and simultaneously gives the proposal's CLM-005/CLM-008 premises a stronger footing than the proposer could give them.
2. It also supplies a concrete, sourced counterpoint for any later claim that "model-based bounds are enough": in the closest published attempt, the authors themselves document underestimation.

**Limits.** Benchmarks are ISCAS '85 / 90nm; the load-bearing sentence is a short quote obtained through the extraction proxy and should be confirmed by the verifier.

---

## F-4. Dominance-based pruning is known practice with a cell-level "proof" — a missing baseline and a claim that needs qualification (not yet an objection)

**Lead evidence.**
- C-A08 (secondary, Chinese-language practitioner article, 2026-09-30): scenario A dominating B means no path is better at A than at B, so B may be dropped. Three evidence levels are given: (1) library delay monotonicity, checked by scripting a scan of Liberty delay tables and described as the strongest and cheapest test, treated as a mathematical proof *at the cell level*; (2) RC-pairing monotonicity (a comparability condition); (3) path-structure sampling, explicitly engineering confidence rather than proof. Temperature inversion and multi-voltage domains defeat (1). Reported practice: roughly 5:1 scenario reduction on a mid-size SoC in a commercial flow, with auditable pruning records and a protected full-corner re-run before tapeout.
- C-A07 (vendor white paper, Tetelbaum/Abelite, Feb 2014; same author as the proposer's SRC-019): warns that redundancy judgments made from one sub-path are unsafe, names SS + Fast-Metal (and FF + Vmax + Slow-Metal) as genuinely required corners for setup when sub-path dominance structures differ, states delay is not monotone in temperature, and says the corner-based approach does not guarantee against silicon failure. It recommends large derates/margins as the compensation.

**Why this matters to EDA-0002.**
1. **Baseline gap.** The baseline set (B0-B5, O in `experiment-plan.md`) has no entry for the cheapest sound-when-verified competitor: verify cell-level monotonicity between scenarios from the Liberty tables, drop dominated scenarios, and run the survivors exactly. Where the dominance relation holds at the level the decision needs, that composition yields exact decisions with no bound machinery, no certificates and no refinement — and it needs no new code, only B0 runs on a reduced scenario set. It is a natural candidate for the "strongest naive composition" slot and for ablation A5's neighbourhood.
2. **A claim that needs qualification.** CLM-002 states that accessed reduction methods carry "no formal guarantee". Under verified library monotonicity there is a checkable dominance argument, so the claim as worded is too broad unless it is qualified to the level at which the guarantee holds. The proposal's own A5 already leans on per-table monotonicity, so the qualification is available to it.
3. **The subtlety cuts both ways.** C-A07 shows cell-level dominance does not imply slack-level dominance, because the capture clock path can reverse the ranking (the same mechanism as the proposal's CLM-017 counterexample). So the dominance baseline is *not* a free win over the candidate; it is only sound where the dominance relation is established for the decision being made. This is exactly why it must be *tested*, not asserted.

**Status: candidate objection material, not an objection.** No primary source for the Liberty-scan dominance method has been found yet, and its effectiveness on the pilot's open scenario sets (ASAP7, SKY130) is unmeasured. Decisive test (cheap, needs no implementation): on each evaluated design and set, compute cell-level dominance between scenarios from the Liberty tables, compute slack-level dominance per endpoint from B0 data at M = 0, prune any scenario dominated for every endpoint, run the survivors exactly, and compare decisions and runtime against B0. This is folded into CA-3 in `first-pass-plan.md`.

**Amendment (sweep closure, 2026-10-13).** The primary-source search for an academic cell-level Liberty-monotonicity dominance *proof* returned nothing public (C-A29); per the plan recorded in the search log, the lead is **downgraded**. The practice remains anchored at method level by two primary sources — patent claim 1's dominant-corner selection (C-A22) and the MDPI paper's dominant-corner strategy (C-A17) — while the unsafety caveats rest on C-A07 (practitioner level). Items 1 (baseline gap) and 2 (CLM-002 qualification) stand unchanged; only the "proof" framing is withdrawn.

---

## F-5. Forward citations of SRC-012 do not trigger K1 (abstract-level sweep)

**Source state.** 23 citing works returned by the Semantic Scholar graph API (record C-A09) — a query the proposer could not run (HTTP 429 in their session).

**Evidence.** By title and abstract the citing set is dominated by learned/statistical corner prediction (One-for-All ICCAD 2024; FACT MLCAD 2024; Unobserved Corner DATE 2019; multi-corner macro modeling TCAD 2024; SI-aware wire timing prediction ASP-DAC 2025), parallelism (CPU-GPU STA, TCAD 2023), mode merging (DAC 2015), and library characterization (SetupKit ICCAD 2025). None presents sound per-scenario certification with exact refinement. Three items remain shortlisted for full-text checks: NIO (2014), the DAC 2015 mode-merging paper, and a 2011 thesis on performance verification under variability.

**Consequences.** K1's "or another found source" leg is not triggered at abstract level by the citing literature of SRC-012. This is a weaker form of evidence than F-1 (abstracts, not full texts) and is recorded as such.

---

---

## F-6. The contest gate is closed: TAU 2018 is path reporting, TAU 2019 is design optimization — neither is multi-corner screening (U8 resolved)

**Question tested.** The proposer's U8 and CLM-014 ("No ICCAD or TAU contest found addresses MCMM scenario reduction… TAU 2018 and 2019 topics unresolved (login wall)"), plus their contest-audit promotion precondition: "If TAU 2018 or 2019 turns out to concern multi-corner screening, this audit must be revised before promotion."

**Source state.** Both contest decks read at full text from local bytes whose SHA-256 equal the hashes in the human's `PROVENANCE.md` (records C-A11, C-A12). No login wall was involved for the decks themselves.

**Evidence.**
1. TAU 2018: "Timing Contest on Path Reporting". Problem = efficient top-N path reporting over a pre-built timing graph with from/through/to queries; benchmarks vga_lcd and leon3mp_iccad with constant-delay Liberty models "to reduce delay-calculation impact"; scoring accuracy/runtime/memory/documentation. Corners appear only as "Early and Late Libraries" inputs. There is no scenario-coverage or reduction objective.
2. TAU 2019: "Design Optimization Contest" (deck subtitle "A Parallel Closure"). Problem = an optimizer applying buffer insertion/deletion and buffer re-sizing, evaluated by OpenTimer for max clock frequency, power, area, runtime and memory. Inputs include Early and Late Libraries and SPEF; results tables split into fast-corner and typical-corner columns.

**Conclusion.** Neither contest poses multi-corner screening, corner reduction, or any soundness-of-screening question. The proposer's contest audit does **not** need revision on this ground, and CLM-014's "unresolved" qualifier can be closed (the TAU 2013 part of CLM-014 was already sourced from SRC-037 to SRC-040).

**Side-product worth carrying into EXP-001.** The TAU 2019 package is a public, multi-design (6 designs, 641 to 795K gates), Nangate45, SPEF-carrying benchmark set with early/late libraries — a candidate partial answer to CLM-013's dataset gap, which the proposer's plan currently treats as blocked. Caveat, stated to prevent over-reading: "early/late libraries" are the min/max analysis libraries for one corner, not two PVT scenarios; the deck does not state whether the fast/typical columns are two characterized corners. I record this as a lead for the tasklist, not as a claim.

**Limits.** Decks are terse; absence of a corner-screening *objective* in the deck is strong but is absence-of-evidence for any unpublished contest follow-up work.

---

## F-7. The proposer's pinned-code provenance and locators verify cleanly (all eight recorded hashes recomputed; locators accurate to ±1 line)

**What was checked.** The full OpenSTA tree at the pinned commit `e01d3f163f483f233db00410b6515a767a6ca03b` was downloaded and extracted (record C-A13), and each of the proposer's eight recorded file hashes recomputed.

**Result.** All eight MATCH the proposer's records: DmpCeff.cc `edfadea5…`, TableModel.cc `8326d308…`, Sta.cc `8da5e45c…`, DelayCalc.cc `42c6e651…`, Sdc.tcl `34677ea5…`, Corner.cc `68c644f0…`, GraphDelayCalc.cc `d939d1bb…`, Search.cc `0e848806…`. Line locators were spot-checked: all cited lines contain the claimed construct, with the largest offset being one line (a function name on the line after the cited start of a range). One citation is loose in form but right in substance (Sta.cc "lines 411 and 417" for the default-calculator fact; 417 is the GraphDelayCalc construction).

**Consequences.**
1. My earlier provenance-gap statement in `search-log-challenger.md` ("upstream file hashes could not be recomputed") is withdrawn: they have now been recomputed and they match.
2. CLM-006 and CLM-007 are reliable observations. This matters for the division of labour in this round: objections should target the proposal's *inferences* (P2-P5, CLM-009) and its *unqualified general statements*, not its code reading.
3. The verifier's confirmation burden on the code side is now small; the remaining confirmation burden is on the paper quotes (C-A10 closes those for SRC-012/SRC-013 too: the load-bearing sentences were re-read from the original bytes).

---

## F-8. CRPR *reduces* hold slack in the pinned engine; the proposal's "CRPR only adds slack" is false for hold (objection material → OBJ-001)

**Source state.** Pinned source tree, hash-verified (C-A13); exact lines in C-A15.

**Evidence.** `search/PathEnd.cc:691-710`: `commonClkPessimism()` returns `-crpr_` when the check's generic role is **hold** and `+crpr_` otherwise (setup); `requiredTime = requiredTimeNoCrpr + commonClkPessimism`. `sdc/Sdc.cc:226-229`: the Sdc constructor sets `analysis_type_ = AnalysisType::ocv` and `crpr_enabled_ = true`; `Sdc::crprActive()` (5474-5477) is true under those defaults. So, by default, the reference engine **subtracts** crpr from hold slack.

**Consequence.** The proposal's mechanism step B states: "**CRPR:** give no credit in the bound. This is conservative, because CRPR only adds slack." For setup this is right; for hold it is wrong in direction: omitting crpr *inflates* the hold lower bound by crpr, so a hold triple can be certified at M while the reference slack is M − crpr. CLM-009's "every violating triple is uncertified when M ≥ 0" then fails for hold, and the reported hold violation list and hold TNS can miss violations — the precise failure mode the candidate exists to prevent.

**Why this is fixable, and cheaply.** crpr is a function of the launch and capture clock paths at the check (the `CheckCrpr` machinery walks exactly those paths). The proposal's pass A computes both clock paths exactly, per scenario. So the hold certificate can carry the exact crpr (or a sound upper bound) with no additional delay calculation. I record this as a repair hypothesis, not a demand; adjudication belongs to the verifier.

**Limits.** Whether the defect materializes in the pilot depends on whether the evaluated flows leave the pinned defaults in place and whether any evaluated hold check has a shared clock path with crpr > 0. Both are checkable before any implementation work (OBJ-001 decisive test).

---

## F-9. The pinned wire delay is not always the single-pole crossing: `thresholdAdjust` can raise it, and ports use another formula (objection material → OBJ-002)

**Source state.** Pinned source tree, hash-verified (C-A13); exact lines in C-A16.

**Evidence.** `dcalc/DelayCalcBase.cc:126-153`: when the load pin's Liberty library differs from the driver's, the returned load delay is adjusted by `load_slew * (load_vth − drvr_vth)/(drvr_slew_upper − drvr_slew_lower)`, added on rises and subtracted on falls; `thresholdLibrary` (155-169) resolves top-level ports to the default (first-read) library, giving a second way for the two libraries to differ. The adjustment is applied to the wire delay at `dcalc/DmpDelayCalc.cc:96/121/276/343` and `dcalc/LumpedCapDelayCalc.cc:162`. Separately, `dcalc/DelayCalcBase.cc:107-124` (`dspfWireDelaySlew`) computes an input-port wire delay as `−elmore·log(1−vth)` — a third formula.

**Consequence.** CLM-007's summary ("Wire delay is a single-pole crossing with τ = Elmore delay, with Elmore fallbacks") is true of the `DmpAlg/DmpPi` path but incomplete as a statement of the *returned* quantity. The incompleteness is load-bearing exactly where the proposal needs precision: P4's bound is "the Elmore delay of the reduced model", and a positive threshold adjustment can exceed it. If any evaluated scenario reads more than one Liberty library per corner (stdcells plus macros or IO), the bound as specified is not sound at the affected pins.

**Also relevant to P4 from F-8's sibling read (C-A14).** The cited DAC 1995 theorem bounds the 50% delay of the *true RC tree response* under a monotone input whose derivative is unimodal and symmetric; the pinned calculator returns a crossing time of an internal pi-model waveform measured from the driver source's own crossing. These are different quantities; the theorem does not by itself transfer. This does not make the bound unachievable — it makes it a *modelling* proof obligation that the current plan assigns to P4 without an argument.

**Limits.** Static reading; magnitude unknown without a run. Both points are cheap to test (OBJ-002 decisive test).

---

## F-10. SRC-022 at full text: learned prediction that explicitly "replaces the STA tool on 12 corners" for hold, with a practical-equivalence claim and no guarantee (supports CLM-002; a natural H3 comparator)

**Source state.** Read through the extraction proxy (record C-A17); the proposer had SRC-022 at abstract level. A direct publisher-mirror byte fetch failed (empty body), so the byte-provenance route used for the other papers was not available here.

**Evidence.** "Machine-Learning-Based Multi-Corner Timing Prediction for Faster Timing Closure" (Electronics 11(10):1571, 2022) selects "dominant" corners by an iterative-increase strategy, runs exact STA there, and predicts slack at the rest with a Random Forest; median absolute error below 3 ps is argued to "be regarded as having the same effect as the STA tool in practical industrial applications", with a 10 ps threshold cited as the point where predictions are useful. The industrial case times 2 corners exactly and predicts 12; there is no uncertainty-triggered fallback and no stated bound. The data are 14 hold corners at 16nm on ITC'99 plus in-house blocks.

**Consequences.**
1. CLM-002/L1 gain a full-text instance in the *hold* domain: reducing corner count by prediction, with an explicit "replace the tool" framing and no certificate — exactly the practice the candidate distinguishes itself from, and one that a "strongest naive baseline" set should be able to represent (B-series).
2. It is a natural H3 (safety-contrast) comparator if the pilot's corner sets can support a prediction baseline at all — which CLM-013 currently says they cannot without new characterization. This tension is worth resolving in EXP-001 rather than assuming.
3. It also shows dominant-corner selection applied to *hold*, which broadens F-4's practitioner lead from setup-style dominance to the hold side.

**Limits.** Proxy read; not decisive for novelty; the paper's own error numbers are the authors' measurements on their designs.

---

## F-11. Broadened contest sweep: the TAU series ends in 2021 and no contest 2011-2026 poses multi-corner screening or a signoff-guarantee task (extends F-6; U8 audit needs one line of extension, not a revision)

**Source state.** Records C-A18 (TAU series, primary; 2021 deck downloaded and hashed), C-A19 (ICCAD CAD Contest 2025/2026), C-A20 (ISPD 2026, secondary and flagged), C-A21 (MLCAD 2025, secondary).

**What the sweep found.**
1. **TAU is the only contest series that ever posed timing-analysis problems, and it is over.** Complete list read from the 2021 contest page: 2011/2012 power grid simulation; 2013 variation aware timing; 2014 CPPR; 2015 incremental timing and CPPR; 2016/2017 timing macro-modeling; 2018 timing reports; 2019 design optimization; 2020 delay calculation using current models; 2021 delay calculation with current-source models from a single driver to multiple receivers (ASAP7 v1.7, CCS, RC-tree). The last contest on record is 2021; the site root still redirected to `/2021` in April 2024 (Wayback), and the TAU 2025 program has no contest session. **No contest in the series is a multi-corner screening, reduction or signoff-guarantee task**; the nearest historical items are the two CPPR contests (2014, 2015) and variation-aware timing (2013).
2. **ICCAD CAD Contest 2025/2026** (C-A19): timing appears only as optimization over organizer-fixed checks — 2025 Problem C (incremental placement, TNS/WNS on organizer-specified corners), multibit-FF optimization; 2026 Problem D "Timing Fixing by Useful Skew" (Realtek). No screening or soundness problem.
3. **ISPD 2026** (C-A20, secondary): post-placement buffering/sizing; reported timing setup is **setup-only, single PVT corner, ideal clock**, OpenSTA-based. The newest contest-adjacent flow therefore cannot exercise multi-scenario machinery at all.
4. **MLCAD 2025** (C-A21): ReSynthAI physical-aware logic resynthesis for timing optimization. Same shape.

**Consequences.**
- The proposer's U8 (TAU 2018/2019) is *correct as far as it goes* but incomplete as a series audit: the series list above should replace it (audit-completeness fix, not an error). CLM-014's TAU 2013 sourcing stands.
- No kill criterion is touched: nothing in 2011-2026 contests defines the candidate's task, so the "no prior contest" half of the novelty story survives the broadened sweep.
- OQ-4 (dataset): the TAU 2019 design-optimization package remains the only contest-adjacent dataset lead; ISPD 2026's single-corner/ideal-clock flow is *not* usable as an evaluated multi-corner flow, and the MLCAD 2025 flow is likewise single-setup.
- Context for OBJ-001: the industry devoted **two consecutive TAU contests (2014, 2015) to CPPR** — independent evidence that CRPR sign handling is a named risk area in this field, which supports the severity framing of the hold-certificate omission (context only; the objection's evidence remains the pinned code).

---

## F-12. The 2024-2026 SOTA sweep leaves K1 untriggered: the nearest disclosures are prediction-first, and the closest soundness language is description-level with explicitly approximate TNS

**Source state.** Records C-A22 (patent, primary claim-level read), C-A23 (nine works, mixed abstract/summary fidelity), C-A24 (exact-WDC line, snippet-level, not load-bearing). This is the "newest SOTA" pass the human asked for; fidelity caveats are stated per item in C-A23.

**The three nearest disclosures and what each lacks.**
1. **US 12,675,622 B1, Synopsys (priority 2022-04-25; granted 2026-07-07)** — the closest document to the candidate's *positioning*. Claims cover per-path corner-subset selection and **marking circuit objects with predicted corners** (claim 1/8/15), ML slack estimation with an error-threshold gate (claim 7), and an aggressiveness knob (claims 3/4). The signoff-safety sentence — "if no violations are reported ..., then no violations exist across all corners that are being considered" — appears **only in the Description**, and the same Description states the method *targets* a "consistent TNS error percentage" (worked example: 1% TNS difference) and hedges results as "acceptable differences in quality of results". Missing relative to the candidate: certified per-scenario margin, exact violation lists, exact TNS, exact refinement of a candidate set. The candidate's differentiator therefore must be stated as **exactness and refinement against the pinned engine**, not "corner marking" or "fallback", which the patent already claims.
2. **Multicorner TCAD 2024 (SRC-019 line)** — "Bayesian decision strategy ... accuracy close to 100% ... with little extra STA executions": the nearest *academic* fallback mechanism. It is statistical (a decision rule), reports accuracy rather than proving zero-miss coverage, and has no refinement step.
3. **Exact worst-delay-corner B&B (C-A24)** — exact, but in a different object (worst corner under affine/piecewise-affine models, exhaustive explore-or-prune). It is not a screening certificate over a pinned non-affine engine and produces no violation lists or TNS.

**The rest of 2024-2026** (ASAP TCAD 2026, FACT TODAES 2026, One-for-All ICCAD 2024, SetupKit ICCAD 2025, BLAST DAC 2025, flip-flop waiver TODAES 2025, UQ-GNN) is uniformly prediction-first from one seed corner or characterization-side, with average-accuracy metrics; none reports a zero-miss guarantee, an exact violation list, or exact refinement.

**K1 assessment at this fidelity.** No work found (2024 through October 2026, contests included) discloses per-scenario sound certification with exact refinement. K1 remains untriggered. **Fidelity caveat:** the four closed-access 2025-2026 items were read at abstract or summary level only; if the verifier or proposer obtains full texts (especially SetupKit and ASAP), this finding should be re-checked — the abstract of none promises soundness, but abstracts can omit a theorem.

**Consequence for the proposal.** The related-work section should place the patent line explicitly (soundness *claimed* at description level; TNS approximate) — it is the strongest available prior art and it sharpens, rather than weakens, the candidate's exactness claim, provided the proposal keeps "exact D_M(S)" precise and does not adopt the patent's own looser "good coverage" language (see S-4).

---

## F-13. Audit extensions and leads from the broadened sweep (no objection material)

- **U-series extension:** replace U8's two-item contest audit with the full TAU series (C-A18) plus the 2024-2026 contest picture (C-A19/C-A20/C-A21). Neither changes any claim's truth value; both close audit gaps a verifier would otherwise flag.
- **OBJ-002 / P4 framing context:** the 2020/2021 TAU contests show where the field invested in wire-delay modelling — current-source (CCS) models, multi-receiver RC trees — precisely the model class the pinned `dmp_ceff_elmore` calculator is *not*. The P4 proof obligation is therefore about the pinned model as it is, not about state-of-practice accuracy; the thresholdAdjust finding (F-9) lives in exactly this gap.
- **Leads (not pursued; not objection material):** TAU 2020 slide "belov_clustering_based_merging_v2.pdf" (Synopsys, cluster-based *merging* of corners/modes) and the 2019 MIS panel material are industry primary sources on reduction and on modelling-induced optimism; worth a bounded read if the verifier wants a practitioner-practice anchor beyond F-4's.

---

## F-14. Remaining verification items closed (sweep closure pass)

**Closed this pass, with records.**
1. **TAU 2013 contest (C-A25).** Results page read: variation-aware *parametric* timing analysis contest; 1st IITimer (IIT Madras), 2nd HWL timer (NTHU), 3rd iTimer (NCTU); organizers incl. Sinha (IBM), Guerra e Silva (INESC-ID), Shebaita (Synopsys). The proposer's CLM-014 anchor is now backed by the primary results page; the last open contest item from the U-series audit is closed.
2. **TAU 2019/2020 Synopsys merging deck (C-A26).** Read in full (hash recorded). Content: GBA-PBA gap; merging only where convergence holds ("No convergence => no merging => slacks are accurate"); partition chosen to minimize accuracy loss at a given merge factor; 16nm/0.545V/100K-endpoint industrial data point. Closes the F-13 lead; adjacent to, not overlapping, corner screening.
3. **ISPD 2026 primary confirmation (C-A27).** The contest repository's own scripts show a TT-only library set (`libworst`) and ideal clocks (`set_ideal_network [all_clocks]`; propagated clock commented out), with report_tns/report_wns metrics. C-A20's load-bearing claims are upgraded from search-index summary to primary confirmation. Fidelity note: the ISPD 2026 description PDF and the MLCAD 2025 problem statement both use subset fonts without usable ToUnicode maps; my extractor returns scrambled glyphs and they were not read — recorded as an extraction limitation, facts taken from README/scripts instead.
4. **C-A09 shortlist triage (C-A28).** (a) DAC 2015 mode merging (Sripada & Palla, Synopsys): paywalled, abstract-level only; closest "merging with validation" analogue ("inbuilt validation that merged constraints correctly model the intent") — watch item if a full text becomes reachable; (b) NIO ICSICT 2014: paywalled, no abstract, no OA copy — recorded as unobtainable in this session, not silently dropped; (c) **Onaissi 2011 U Toronto PhD thesis: obtained and read** (880,389 bytes, SHA-256 recorded). It is the same author as SRC-012/013: Ch. 4 is a block-based PSTA with an *Exact Algorithm* and a *Sufficient Condition* (a different object from engine-exact screening); Ch. 5 is the DAC 2011 anchor-corner method with an "Exact vs conservative approach" section and explicit conditional conservatism ("we must choose ... an anchor corner that leads to the smallest datapath delay"); the optimization chapter states outright that "there is no guarantee that X-hat would be the worst-case corner for the post-optimization expression". Net: F-1/F-5 (K1 not triggered) gain a fuller-text corroboration, and the exactness that exists in this line is parametric-PSTA exactness, not decision-set exactness.
5. **Open-access negative result (C-A28).** Properly formed arXiv queries return zero preprints for ASAP, SetupKit, BLAST, the uncertainty-aware GNN, and SI-Aware; One-for-All's ACM OA link 403s. F-12's fidelity caveat is therefore a *verified* negative: no open full text of the five closed 2025-26 works exists at the routes available to this role. The re-check remains a verifier/human action (institutional access).
6. **F-4 lead downgraded (C-A29),** as planned; amendment recorded in F-4.

**Consequence.** No challenger-side factual item from my own checklist remains open. What remains is outside my single-role authority or reach: verifier adjudication of OBJ-001/OBJ-002; the paywalled full texts; the joint task-list co-production (harness items 9-10) which requires the proposer and the adjudicated objections.

---

## F-15. OBJ-002 self-narrowing: the thresholdAdjust branch needs *differing threshold definitions*, not merely several libraries per corner

**Source state.** PDK check C-A30 (ASAP7 TT library headers) on top of the pinned-code facts C-A16 and the OBJ-002 filing.

**Evidence.** ASAP7's LVT, RVT and SLVT stdcell libraries declare identical threshold attributes (input/output 50%, slew 10/90) and identical nominal conditions; the ISPD 2026 evaluation flow reads several of them in one corner (C-A27). Under `thresholdAdjust` (`dcalc/DelayCalcBase.cc:126-153`) the additive term vanishes when the load and driver threshold values are equal, so the common mixed-VT pattern is inert. The adjustment is live only when a driver/load library *pair* has differing threshold definitions (some macro/IO libraries use different pct conventions), or through the separate input-port formula (`dspfWireDelaySlew`, `DelayCalcBase.cc:107-124`).

**Consequence for OBJ-002.** The "potentially major" branch is narrowed: its trigger is not "more than one Liberty library per corner" but "a library pair with differing threshold pct attributes inside the evaluated set (or input-port arcs)". The objection's other limbs are unaffected: CLM-007 is still incomplete as a description of the *returned* quantity, and P4 still needs its modelling argument. The decisive test in `challenges.md` is updated accordingly (static per-corner threshold-attribute scan first; unit test only if a mismatched pair exists).

**Honesty note.** This is a self-correction that weakens my own objection's severity branch; it is recorded because the harness requires conditions and tests to be accurate, not maximally threatening.

---

## Status

- Findings recorded: F-1 (K1 not triggered by SRC-012), F-2 (SRC-012 side observations), F-3 (SRC-013 non-conservative), F-4 (dominance-pruning baseline gap and CLM-002 qualification; proof-lead downgraded in the amendment), F-5 (forward-citation sweep), F-6 (contest gate closed; U8 resolved), F-7 (code provenance and locators verified), F-8 (CRPR hold direction), F-9 (thresholdAdjust and port wire delay), F-10 (SRC-022 at full text), F-11 (broadened contest sweep), F-12 (2024-2026 SOTA sweep; K1 untriggered at the recorded fidelity), F-13 (audit extensions and leads), F-14 (remaining verification items closed: TAU 2013, merging deck, ISPD 2026 primary, shortlist triage incl. the Onaissi thesis, OA negative result, F-4 downgrade), F-15 (OBJ-002 self-narrowing: differing threshold definitions, not library count, is the trigger).
- Objections recorded: **OBJ-001** (hold certificate omits CRPR; major, fixable) and **OBJ-002** (CLM-007 incompleteness bears on P4; minor, with the formerly "potentially major" branch narrowed by F-15/C-A30) — both in `challenges.md`, both awaiting verifier adjudication.
- Verifier action requested: (1) adjudicate OBJ-001/OBJ-002; (2) independently confirm `search/PathEnd.cc:691-710` and `dcalc/DelayCalcBase.cc:126-153` in the pinned tree; (3) if institutional access allows, re-check F-12 against the full texts of ASAP (TCAD 2026), SetupKit (ICCAD 2025), BLAST (DAC 2025), SI-Aware (ASP-DAC 2025) and the uncertainty-aware GNN — no open copy exists (C-A28); (4) optionally confirm the ISPD 2026 script reading (C-A27) and the paywalled DAC 2015 mode-merging abstract-level summary (C-A28).
- Next in the round: none on the challenger's own checklist — all factual items are closed (F-14). The remaining steps belong to the process: verifier adjudication, then the joint task-list co-production (harness items 9-10) with the challenger additions to `experiment-plan.md`/`tasklist.md` (the CA- series in `first-pass-plan.md`), the CRPR sign audit as a unit test, and S-4 (related-work framing) for the proposer.
