# EDA-0002 (D05) proposer first-pass plan

| Field | Value |
|---|---|
| Actor ID / call sign | `Claude-P05-TIMING` / `CLD-Origin-TIMING` (the call sign appears only in the launch prompt, not in the packet) |
| Role | proposer |
| Domain / topic | D05 Timing, extraction and signoff / `EDA-0002` (phase `research`, stage `initial`) |
| Actual model | `claude-opus-5-5` (Opus 5.5), reasoning effort `max`; host-reported. Requested: `claude-family:strongest-exposed` |
| Input commit | `d437c2f660906efe9351a90451905826d00b63e3` |
| Packet SHA-256 | `ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d` (recomputed; matches) |
| Listed-file hashes | 31 of 31 verified; 0 mismatched, 0 missing, 0 unlisted files |
| Written | 2026-10-12 (UTC); companion record: `readiness.json` |
| Status | Onboarding plan only. No search, experiment or topic selection has been performed. No novelty claim is made. |

## 1. Purpose and labels

This is the proposer plan required by `harness/ONBOARDING.md` step 4 (line 10) and listed as a first output in `domains/D05/brief.json` (lines 18-21). It does not propose a topic. The research round starts only with a later file packet or direct human request (`harness/ONBOARDING.md` line 13).

Statement labels:

- **[P]** Observation from a hash-verified packet file, with locator.
- **[I]** My inference from packet observations.
- **[H]** Hypothesis to investigate. Not yet searched or tested.
- **[L]** Lead from my pretrained background knowledge. Unverified, bibliographic details may be wrong, and never cited as evidence until confirmed in a primary source.

## 2. Isolation and unlisted context (summary)

Full records are in `readiness.json` (`isolation_observed`, `unlisted_context`).

- I make no OS-isolation claim for the session. The host applies a per-command macOS Seatbelt sandbox to Bash. Under it, reads are denied across the home directory except for this packet and this outbox, and other actors' packet and outbox directories are named in the deny list. Writes are limited to this outbox, the working directory and temp areas, and network egress goes through a filtering proxy. I have not established whether the file and web tools fall under the same restrictions, and I did not probe any denied path.
- All actors appear to share one host and one OS account. As far as I can observe, the strong-enforcement setup in `docs/ISOLATION.md` line 5 (separate containers or accounts, packet mounted read-only) is not met.
- The packet directory has no `.git` and no `.claude`, and its files are read-only by mode bits only.
- The context was fresh: no earlier turns, memory, CLAUDE.md, skills or MCP servers were present. No subagent or messaging tool is available.
- Unlisted context: the host system prompt and environment block, which include sandbox path names revealing other actors' directory patterns and a launch run ID `CLD-P05-LAUNCH-0001`; an operator-email reminder (value withheld, unused); a git-attribution reminder (unused); the `/model` command record; the call sign in the launch prompt; and my pretrained knowledge, used only for [L] leads and terminology.

## 3. Packet constraints on the research round

- [P] Scope: STA, multi-mode/multi-corner analysis, parasitic extraction, crosstalk/SI, timing closure, incremental analysis and ECO. Metrics: WNS/TNS, signoff fidelity, corner robustness, extraction error, runtime and closure effort (`domains/D05/brief.json` lines 5-6).
- [P] Boundary: distinguish training targets, surrogates and signoff oracles. Physical ECO spans D04, but D05 owns signoff validity (`domains/D05/brief.json` line 7).
- [P] At most one opportunity per proposer and one hypothesis per domain (`docs/PHYSICAL-PILOT.md` line 24; `domains/D05/brief.json` line 17).
- [P] Provisional D05 primary metric: wall time to obtain the same timing decisions as pinned full OpenSTA analysis, reporting maximum endpoint slack error and false-negative violating endpoints (`config/research-brief.json` line 71). Each topic preregisters its own endpoint (line 69).
- [P] Provisional minimum meaningful effect: at least 20% wall-time reduction, maximum absolute endpoint slack error of 0.005 ns or less, and zero missed violating endpoints on evaluated cases (line 77). Evidence requires at least 3 independently selected designs, at least 5 paired seeds per stochastic condition, confidence intervals and all failures. GCD alone cannot establish success. Thresholds are revised after baseline variance and practitioner input, before candidate evaluation (line 78).
- [P] Compute: 8 CPU-hours total, 2 CPUs and 4 GiB per job, one job at a time, no GPU, $0 API, two-week provisional horizon. These are coordinator-selected caps (`config/research-brief.json` lines 9-26).
- [P] Tools: OpenROAD/OpenSTA/OpenRCX at `b16bda7e82721d10566ff7e2b68f1ff0be9f9e38` in a digest-pinned OpenLane container; Yosys 0.68+post; KLayout/Magic present, but DRC/LVS not validated (lines 27-43).
- [P] Technology and designs: the Nangate45 research library at the typical corner only, and one design, `gcd_nangate45` (lines 44-61; `config/physical-resources.lock.json`). The GCD smoke gave setup WNS -0.054 ns and TNS -0.880 ns, so timing is not closed. Flow completion establishes only a reproducible tool path (`docs/PHYSICAL-PILOT.md` line 19).
- [P] No experiment authorization. Blockers: no accepted topic or agreed task list; representative designs, macro-rich cases, additional corners and a qualified signoff oracle are still incomplete (`config/launch-release.json` lines 71-75). Before any feasibility claim: at least 3 independent designs, additional corners, an explicitly qualified reference oracle for signoff claims, and the strongest accessible baselines under equal resources (`docs/PHYSICAL-PILOT.md` line 27).
- [P] Engineering user: physical-design and timing-closure engineer. Practitioner validation is pending (`config/research-brief.json` line 67).

[I] Consequences for planning:

1. Opportunities whose claims need multiple corners, SI analysis or a signoff-grade oracle are blocked until resources are acquired. Today the only unblocked class is single-corner questions referenced to pinned OpenSTA.
2. "Same decisions as pinned OpenSTA" is a claim of fidelity to a reference, not of signoff accuracy. The claim ledger must keep the two apart.
3. The 8 CPU-hours must cover parasitic generation for at least 3 designs plus repeated timing runs. That favours public designs that already ship with parasitics, subject to license checks.
4. On GCD-sized inputs, a 20% wall-time effect would be lost in run-to-run noise and fixed start-up cost. The designs must be large enough that the measured phase dominates the noise.

## 4. Open issues for the coordinator

Details and locators are in `readiness.json` `discrepancies_and_open_questions`.

1. **D05 role mismatch (DQ-01).** `domains/D05/brief.json` and `domains/D05/README.md` name Codex D05 proposer and challenger roles. `config/launch-release.json` and `ASSIGNMENT.json` assign `Claude-P05-TIMING` and `DeepSeek-C05-TIMING`. I follow the latter and edited nothing.
2. **Referenced files missing from the packet (DQ-02 to DQ-04):** `config/agents.json` (the onboarding pause check), `config/agents-claude.json` (the registry), `config/roles.json`, `scripts/project.py`, `templates/topic/` and `runs/PHYSICAL-PILOT-0001`. Without them I cannot run `validate` or `tasklist-digest`.
3. **Session registration and model confirmation (DQ-02, DQ-06).** The session is not yet registered. The model is host-reported only, and I cannot tell from inside the session whether it is the strongest one exposed.
4. **Measurement ruling (DQ-07).** May the proposer run small, non-confirmatory characterization while drafting, given `experiment_authorization: false`? An example would be OpenSTA phase profiling on public designs under a stated CPU-minute cap. Default until ruled: no local tool runs. Failure evidence will come from public sources or tight inference.
5. **Gaps in the provisional metric (DQ-08).** These are handled in section 10 and are not a criticism of the brief.

## 5. Candidate workflow slices and engineering decisions

| ID | Slice | Engineering decision supported | Decision reference (oracle) | Resource status now | Fit to provisional D05 metric |
|---|---|---|---|---|---|
| S1 | Incremental timing inside closure/ECO loops (sizing, buffering, Vt swap, hold fixing, what-if ECO) | Accept or reject a candidate move; which endpoints still violate | From-scratch OpenSTA on the post-move netlist/parasitics at the same commit | Unblocked: single typical corner suffices. [I] OpenROAD repair commands could generate realistic move sequences | Direct. The baseline must be OpenSTA's own incremental path, not from-scratch analysis |
| S2 | Scenario (corner x mode) reduction that preserves decisions | Which scenarios to analyze per iteration without missing violations | Full analysis of all scenarios | Blocked: typical corner only. Needs public multi-corner libraries and RC corners with acceptable licenses | Direct |
| S3 | Parasitics to delay calculation (RC reduction, delay-calculator choice, SPEF handling) | Which RC and delay-calculation fidelity leaves decisions unchanged | OpenSTA with full SPEF and its most accurate available delay calculator. Extraction accuracy itself needs a field-solver oracle, which is unavailable | Partly unblocked (STA-cost side only) | Direct for STA cost; extraction-accuracy claims are oracle-blocked |
| S4 | Pessimism handling: GBA vs PBA, CRPR/CPPR, derates | Whether GBA violators are real before spending ECO effort | A path-based recalculation engine; whether pinned OpenSTA has one is unknown | Unknown until the G1 source audit | Direct if a PBA reference exists |
| S5 | Crosstalk / SI-aware timing | Delta-delay and timing-window decisions | SI-capable signoff tool or SPICE: unavailable | Blocked | Awareness only |
| S6 | Hierarchical abstraction (ETM, ILM, timing macro models) | Top-level decisions with abstracted blocks | Flat OpenSTA analysis | Needs hierarchical designs and timing-model generation support (to verify) | Direct |
| S7 | Timing-closure decision support (agentic or AI): violation triage, SDC debugging, ECO recommendation | Which fix to apply; whether the constraints are right | Re-analysis after the fix. An oracle for constraint intent is hard to build | $0 API rules out reproducible LLM-agent runs | Weak; overlaps D04 for ECO |
| S8 | Learned timing surrogates (pre-route or post-route slack/delay prediction) | Early estimation or screening | A surrogate is not an oracle; decision equivalence needs an exact fallback | No GPU, few designs, and family-held-out training is hard | Only as a screening component |

Search order (not a selection): S1, S3 (STA-cost side), S4 (pending the oracle check), S2 (with a corner-acquisition check), S6, S8, S7, S5.

[I] The order rests only on fit to the provisional metric and on oracle availability under current resources. It is not a judgment of novelty or value, and it will change if the search shows saturation or missing demand.

All three tracks (traditional, AI and agentic) are searched in every slice, and no track is preferred for its own sake (`docs/CHARTER.md` line 5). Per `harness/PROPOSER.md` line 3, a narrower defensible question is preferred over a broad novelty claim.

## 6. Terminology and search expansions

| Concept | Variants to search | Pitfalls |
|---|---|---|
| Static timing analysis | STA, timing engine, timer, timing graph, levelization, arrival/required-time propagation, slack | "Timing-driven" placement or routing papers belong to D04; tag the overlap |
| Incremental timing | incremental STA, timing update, lazy/dirty propagation, what-if analysis, ECO timing, timing query | "Incremental" is also used for incremental placement and routing |
| GBA/PBA | graph-based analysis, path-based analysis, path recalculation/retiming, exhaustive PBA, pessimism removal | Vendor-specific mode names |
| CPPR/CRPR | common path pessimism removal, clock reconvergence pessimism removal, clock network pessimism | Interaction with hold analysis |
| Variation and derates | OCV, AOCV, POCV, SOCV, LVF, SSTA, timing derate | Corner-based vs statistical formulations |
| MCMM | multi-corner multi-mode, scenario, scenario reduction, dominant corner/scenario, corner pruning/merging/selection, missing-corner prediction | PVT corners vs RC corners (Cworst, RCworst, Cbest, RCbest, typical) |
| Parasitics and delay calculation | SPEF, RC extraction, parasitic reduction, model order reduction (AWE, PRIMA, TICER), effective capacitance (Ceff), driver model, NLDM/CCS/ECSM, Elmore, D2M, Arnoldi | Extraction, reduction and delay calculation are distinct stages with distinct oracles |
| Signal integrity | crosstalk, coupling capacitance, delta delay, timing windows, aggressor filtering, noise analysis | Usually needs SI-capable tools |
| Hierarchical timing | extracted timing model (ETM), interface logic model (ILM), timing macro model, block abstraction, hierarchical STA | Context-independent vs context-dependent models |
| ECO and closure | timing ECO, hold fixing, gate sizing, buffer insertion, Vt swap, useful skew, repair_timing | D04 owns physical ECO; D05 owns signoff validity |
| Learned or differentiable timing | GNN slack prediction, timing surrogate, learned delay model, differentiable STA, timer-to-timer correlation, GBA-to-PBA prediction | Regression accuracy is not decision accuracy |
| Acceleration | GPU STA, parallel/distributed STA, task-graph parallelism, multi-threaded timing | The 2-CPU job cap limits parallel-scaling claims |
| Guarantees | conservative/safe bound, interval or bounded STA, certified pruning, error-bounded approximation, false negatives, decision equivalence | "Zero misses on evaluated cases" is not a guarantee |

## 7. Search plan (research round; not started)

Rounds:

- **SR-0 Tool capability audit (source reading only).** Identify the OpenSTA commit that OpenROAD `b16bda7e...` references. Read the code paths and documentation for incremental update, multi-corner analysis, delay calculators, path-based recalculation, CRPR, derates, SI and timing-model writing. Output: a capability table with file/line locators.
- **SR-1 Scoping sweep across S1-S8 and all tracks (shallow).** Use the section 6 query families, covering roughly the last ten years plus classical foundations. Log every query.
- **SR-2 Contest audit.** TAU workshop contests (all available years), timing-related ICCAD CAD Contest problems, and ISPD contests on timing-driven sizing or ECO. Collect official rules, provided baselines and hints, winner reports and public code. Contest-provided ideas count as baseline knowledge, not novelty (`docs/PHYSICAL-PILOT.md` line 24).
- **SR-3 Open implementations.** OpenSTA, OpenROAD (resizer), OpenTimer, the iEDA timing engine, and other open CPU or GPU timers. Include repository issues and commits about runtime pain, incremental-update bugs and multi-corner cost.
- **SR-4 Public commercial capability.** Vendor documentation and whitepapers for STA, extraction and ECO products. These support advertised-capability statements only, not controlled comparisons (`docs/EVIDENCE.md` line 7).
- **SR-5 Deep nearest-work audit for 2-3 shortlisted slices.** At least the three nearest independent approaches each. Backward and forward citation expansion, author and lab neighbourhoods, patents for industrial mechanisms, and negative or failed results.
- **SR-6 Pre-submission novelty refresh** (`docs/EVIDENCE.md` line 13).

Indexes: DBLP, IEEE Xplore, ACM DL, arXiv (cs.AR, cs.LG), Semantic Scholar or Google Scholar for citation graphs (as access permits), OpenReview, GitHub, official contest sites, Google Patents and vendor sites. Each source records its access level (`full`, `abstract`, `metadata`). Abstract-only access never counts as method inspection.

Logging:

- For every query, `search-log.md` records the UTC date, engine/index, exact string, filters, results inspected, inclusion or exclusion with reason, and access limits.
- Every retained source goes into `sources.json` in the `docs/FORMATS.md` schema, with locator, claim IDs, limitations, version and license.

Stop rule: a round stops only after two documented expansions reveal no closer mechanism. Otherwise I report budget exhaustion and the residual risk. "Three nearest approaches" is a coverage minimum, not a certificate (`docs/EVIDENCE.md` line 13).

Search tools: the host WebSearch/WebFetch tools under the existing subscription. No paid API.

Seed leads [L] (all unverified; checked in SR-1 to SR-5 before any use):

1. OpenSTA, the timer used inside OpenROAD. It is the decision reference, and its incremental and multi-corner machinery is audited in SR-0.
2. OpenTimer and its second version (T.-W. Huang and co-authors), an open incremental timer with a reported TAU-contest lineage.
3. The iEDA project's STA engine. Scope and license to be verified.
4. GPU-accelerated STA (reportedly Guo, Huang and Lin, ICCAD 2020) and follow-ups.
5. A timing-engine-inspired GNN for pre-routing slack prediction (reportedly Guo et al., DAC 2022).
6. Machine-learning prediction of path-based slack from graph-based analysis (reportedly Kahng et al., ICCD 2018).
7. Learned estimation of SI-induced delay and transition (reportedly Kahng et al., SLIP 2015).
8. Prediction of timing at unanalyzed corners (Kahng group and others; titles unverified).
9. The TAU contest series: reportedly CPPR, then incremental timing with CPPR, then timing macro modeling, in the mid-2010s. Topics and years to be confirmed from official archives.
10. Clock-network pessimism-removal algorithms (for example a reported "UI-Timer").
11. Classical RC model-order reduction (AWE, PRIMA, TICER), Elmore and D2M delay metrics, and effective-capacitance driver modelling.
12. Differentiable or statistical timing engines from industrial research (a reported NVIDIA engine named "INSTA"; existence and details unverified).
13. Commercial public capability descriptions: Synopsys PrimeTime and StarRC, Cadence Tempus and Quantus. Relevant capabilities are multi-scenario, distributed, hierarchical, PBA and ECO.

[L] Industrial practice probably already includes slack-threshold filtering, such as running PBA only on GBA violators and filtering SI aggressors by timing window. Any margin-based pruning idea must therefore be searched as prior art first, not assumed novel.

## 8. Comparison dimensions for the nearest-work audit

The `prior-art.csv` columns are fixed: `source_id, task, mechanism, data, evaluation, assumptions, limitation, overlap, distinction`. Within them I will record:

- Workflow stage and the decision supported.
- Analysis mode: GBA/PBA/SSTA, setup/hold, and MCMM and SI coverage.
- Guarantee type: exact, bounded error with the stated bound, statistical, or none.
- Decision metrics (missed and false violations near the threshold) kept separate from regression metrics (MAE, R^2).
- The reference oracle and its qualification.
- Baseline strength: from-scratch, incremental or commercial.
- Designs: source, size, node, corners and family overlap between training and test.
- Hardware, threads, and whether the reported runtime is end-to-end.
- Preprocessing, characterization or training cost, and the amortization horizon.
- Implementation availability: repository, commit and license.
- Limitations as stated by the authors, kept separate from limitations I infer (labelled).

## 9. Failure mechanisms to investigate [H]

None of these is a claim. Each needs a counterexample, a reproducible observation or a tightly supported inference before it can enter the claim ledger (`harness/PROPOSER.md` line 13).

| ID | Suspected failure | Why it would matter | Evidence needed | Refuted if |
|---|---|---|---|---|
| FM-01 (S1) | After small ECO moves, incremental updates re-evaluate large fan-out cones even though most downstream changes cannot alter any endpoint decision | Wasted update work in closure loops, which make many timer calls | Source audit of the invalidation/propagation rules; counts of re-evaluated vertices vs vertices whose arrival or slew changed beyond a small tolerance | The engine already stops on unchanged or negligible deltas, or the avoidable work is below the 20% effect threshold |
| FM-02 (all) | End-to-end wall time is dominated by fixed phases (Liberty/SPEF/Verilog parsing, graph build, Tcl) or by delay calculation, not propagation | Determines which mechanism can reach a 20% end-to-end effect. Caching or serialization gains would be engineering, not research | A phase-level runtime profile on representative designs (needs the DQ-07 ruling) or published profiles | The targeted phase carries enough of the runtime for the effect threshold to be reachable |
| FM-03 (S1-S4, S8) | In closed or nearly closed designs, many endpoints sit within ±5 ps of zero slack (a "slack wall"), so certified-approximate screening falls back to exact analysis for most of them | Bounds the attainable speedup of any approximate decision-preserving mechanism (see section 10) | Endpoint slack distributions after optimization, from public reports or authorized runs | The ±5 ps band holds a small fraction of endpoints on representative closed designs |
| FM-04 (S2) | The dominant scenario differs by endpoint and path (cell- vs wire-dominated paths, setup vs hold, PVT vs RC corners), so scenario-level pruning either keeps most scenarios or risks misses | Determines whether endpoint-level certificates add anything beyond simple corner dominance | Per-endpoint worst-scenario distributions on multi-corner data (needs the G3 corners) | One scenario dominates all decisions on representative designs, or the available bounds are too loose to prune |
| FM-05 (S8; learned parts of S2/S4) | Learned estimators with good MAE or R^2 still misclassify near-threshold endpoints | Decision-preserving use needs an exact fallback whose size sets the speedup | Published error distributions near zero slack, with missed/false-violation reporting | Published held-out-family results show zero misses with errors of 5 ps or less near the threshold |
| FM-06 (S3) | RC-reduction and delay-calculation accuracy budgets are uniform per net rather than allocated by timing margin | Possible delay-calculation savings on high-margin nets | Source audit of the reduction controls; prior art on slack-driven tolerance | Prior art already allocates by margin, or delay calculation is a small runtime share (FM-02) |
| FM-07 (S6) | Timing abstractions characterized at nominal boundary conditions mispredict under different input slews, loads or clock latencies, flipping top-level decisions | Limits block reuse in hierarchical closure | TAU macro-modeling contest metrics and winner reports; flat vs abstracted comparisons | Reported errors are far below 5 ps at practical model sizes, i.e. the problem is saturated |
| FM-08 (S1-S4 hazard) | Bounds that are safe for late (setup) analysis are unsafe for early (hold) analysis or under CRPR | A correctness hazard for any pruning mechanism, not an opportunity | Construct counterexamples during mechanism design; test setup and hold separately | Not applicable; this is a mandatory correctness test |

## 10. Experimental endpoints (draft for preregistration; not frozen)

**Decision set.** For each scenario, timing endpoint, check type (setup, hold, recovery, removal) and clock/path group: the slack, and the violation flag (slack below zero, or below a preregistered margin). Whether design-rule checks (max slew, capacitance, fanout) are in scope is decided at preregistration. A numerical tie tolerance for "identical" results is also preregistered, because operation order can perturb floating-point slack.

| ID | Endpoint | Rule |
|---|---|---|
| EP-01 | Primary: end-to-end wall time to a decision set identical to the reference | Paired ratio per design against the strongest relevant baseline. Provisional threshold: at least 20% reduction |
| EP-02 | Missed violating endpoints (false negatives) | Must be 0. State whether this is certified by construction or only observed on evaluated cases |
| EP-03 | False alarms (false positives) | Proposed addition: a method that flags every endpoint already scores zero false negatives. Identical decisions require 0. Any relaxation is preregistered with its downstream ECO cost |
| EP-04 | Slack fidelity | Maximum absolute slack error of 5 ps or less over the preregistered endpoint population. Also p50/p99 error, and WNS/TNS per scenario and path group for setup and hold |
| EP-05 | Total cost | CPU time and peak RSS. All preprocessing, characterization and training are included end-to-end or amortized over a stated horizon, with the break-even point |
| EP-06 | Mechanism counters | Vertex and arc evaluations, delay-calculation calls, scenario x endpoint evaluations. Secondary and less noisy; used for causal ablation, never as the primary endpoint |
| EP-07 | Failure accounting | Crashes, timeouts and decision mismatches, reported per design |

[I] **Joint-constraint consequence.** Suppose a method's slack error is two-sided and bounded by e = 5 ps.

- Guaranteeing zero missed violations means flagging every endpoint whose approximate slack is below +e.
- Guaranteeing identical decisions also requires exact re-analysis of every endpoint whose approximate slack falls in [-e, +e).

The attainable speedup of any approximate mechanism is therefore bounded by the size of that band and the cost of re-analyzing it (FM-03). Exact accelerations avoid the band, but must still beat the strongest exact baseline.

**Baseline policy.**

- The reference is the pinned full OpenSTA analysis named in the brief.
- The comparison baseline is the strongest relevant configuration: OpenSTA's incremental update for incremental use, and its best multi-corner mode for multi-scenario use. It runs with equal threads and memory.
- Also included: a closest-prior-mechanism baseline, a naive-composition baseline, and an equal-budget or oracle bound where meaningful (`docs/EXPERIMENTS.md` line 15).

**Measurement protocol.**

- The same pinned container image and binaries are used for baseline and candidate, with the 2 CPU / 4 GiB limits and fixed thread counts.
- The cold- or warm-cache policy is declared. Warm-up runs are discarded, and A/B order is interleaved.
- Wall time, user and system CPU, and peak RSS are recorded, along with the host state (one experiment job at a time, per the brief).
- Phase-level times are reported alongside end-to-end times.

**Statistics.**

- Per-design paired ratios with bootstrap confidence intervals. Repetition counts come from pilot variance; three seeds is not automatically adequate (`docs/EXPERIMENTS.md` line 17).
- Correlated cases (one design family, one move sequence) are not treated as independent. Multiple comparisons are disclosed, and every per-design result and failure is reported.

**Claim scope.** Fidelity to pinned OpenSTA at the stated corner(s). No signoff-accuracy claim is made without a qualified oracle.

## 11. Feasibility gates before selecting an opportunity

- **G1 Tool capabilities.** Complete the SR-0 audit with source locators. Determine which mechanisms already exist in the pinned OpenSTA and which baselines are available.
- **G2 Designs.** At least 3 independent design families with verified redistribution and use rights, large enough for STA runtime to dominate noise. [L] Candidate pools to check: OpenROAD-flow-scripts designs for Nangate45, TAU-contest benchmark suites that ship with parasitics, and open-source cores (for example OpenTitan blocks). Synthesis-only suites (EPFL, ITC'99, ISCAS) would need mapping and P&R cost.
- **G3 Corners (S2 only).** Public multi-corner libraries plus RC corners. [L] Candidates to check: SKY130, GF180MCU, ASAP7, IHP SG13G2, and the original NanGate library corner set. Check licenses and OpenRCX rule availability.
- **G4 Oracle.** An operational definition of "full OpenSTA analysis" (commands, reports, endpoint dump format). Record that no signoff-grade oracle is available.
- **G5 Compute.** Estimated CPU-minutes for parasitic generation and repeated timing runs per design, fitting within 8 CPU-hours including pilot variance runs. This estimate comes from public data until DQ-07 is ruled.
- **G6 Rights.** A license record for every design, library and tool. No proprietary or restricted data.

Acquisition downloads and any tool execution happen only after coordinator or human authorization.

## 12. Opportunity selection procedure

Each shortlisted opportunity is assessed against these criteria, with evidence references:

- **C1 Demonstrated engineering demand:** papers with industrial motivation and data, tool documentation describing the capability or pain, public issue reports. Not a proxy alone (`docs/CHARTER.md` line 11).
- **C2 Distance to the nearest mechanism** after at least two documented expansions.
- **C3 Oracle availability and qualification** for the intended claim scope.
- **C4 Resource fit:** 8 CPU-hours, 2 CPUs, 4 GiB, no GPU, $0 API, and designs and corners obtainable with rights.
- **C5 Measurability:** the expected effect can be detected above run-to-run noise on accessible designs.
- **C6 Boundary:** the decision is owned by D05, with any D04 overlap explicit.
- **C7 Contest originality:** not merely a provided idea, a winner approach or an unfinished contest task (`docs/CHARTER.md` line 13).

The selection rules:

- Select exactly one opportunity.
- Record the runners-up and the reason each was rejected in `search-log.md`.
- An opportunity with an unmet C3 or C4 gate can be selected only if the plan contains the acquisition task, marked as a blocking dependency.
- If no opportunity survives, I report that with evidence rather than manufacturing a combination (`harness/PROPOSER.md` line 19).

## 13. Anchor and drift controls

Once an opportunity is selected, `direction-control.json` freezes the problem, engineering user, downstream need, causal mechanism, mechanism invariants and forbidden pivots before the challenge round (`docs/CHARTER.md` line 16).

The forbidden pivots are the three in the scaffold plus slice-specific ones such as:

- Dropping decision equivalence in favour of average-error metrics.
- Replacing the mechanism with parallelization or hardware scaling alone.
- Moving the objective from a D05 timing decision to a D04 placement or routing objective.

`combination_drift` and `demand_drift` start at 0 and are rescored on every substantive revision.

## 14. Research-round sequence and deliverables

1. **SR-0 to SR-4:** `search-log.md`, `sources.json`, a first `prior-art.csv`, `contest-audit.md` and `industry-gap.md`. The industry gap covers the persona, open implementations with versions, public commercial evidence, matched vs incomparable conditions, algorithm vs data/integration gap, and adoption cost.
2. **Shortlist, SR-5 and selection:** the nearest-work sections of `proposal.md` and the `direction-control.json` anchor.
3. **Failure evidence:** public evidence or an authorized minimal observation, written into the observed-limitation section of `proposal.md`.
4. **Plan documents:**
   - `experiment-plan.md`.
   - `tasklist.md`: EXP-001 to EXP-009, expanded with owner, dependencies, budget, procedure, artifact and pass/fail criterion.
   - `forecast.json`: nulls with resolution tasks where unknown.
   - `experiment-consensus.json`: left pending. I do not sign placeholders.
   - `dossier.json`: set to `submitted` only when complete.
5. **`responses.md`** stays untouched until adjudicated challenges are released.
6. **`role-output-manifest.json`** with output paths and SHA-256 hashes, plus run-manifest fields per `templates/run.json`.
7. **Structural validation** by the coordinator, unless `scripts/project.py` is included in the next packet.

No experiment is executed in the research round without the authorizations in `docs/EXPERIMENTS.md` lines 25-27.

## 15. Stop point

This turn ends after writing `first-pass-plan.md` and `readiness.json` to the outbox. No web survey, experiment, monitoring, inter-agent message, subordinate agent or self-generated follow-up was started.
