# EDA-0008: Order-contrast prediction for coordinating post-placement resizing and relocation

## Status, scope and predecessor

Fresh D04 successor, batch cycle 4/4, initial research release. **Position: retain a conditional hypothesis for independent review; novelty, representative demand and experiment readiness remain unresolved. At the batch limit, park rather than authorize experiments unless the independently reviewed gates actually pass.** This release neither accepts itself nor jointly abandons EDA-0005. No physical design run, training, GPU, remote compute or paid API experiment occurred.

The explicitly released EDA-0005 verifier parked a fixed-clock movement/hold-repair admission interface: its matched composition was stipulated operationally identical, and useful distinction, incidence and realization costs remained unknown. Preserve that negative lesson, not its scientific approval. EDA-0008 changes the mechanism and stage to **pre-CTS, ideal-clock post-detailed-placement sequencing of a width-changing resize and a relocation**. It is a new topic, not an anchor-preserving repair of EDA-0005. No hold-repair option tables or matching guarantee are inherited.

## Candidate comparison under the three required lenses

| Candidate | Concrete mechanism and engineer action | Closest methods and strongest alternative | Selection |
|---|---|---|---|
| A: cooperating optimizers | Timing specialist proposes width-changing resize; congestion specialist proposes relocation. Exchange a version-bound prediction of the two execution orders after legalization, then submit a selected order to real tools. | ChatEDA task execution (S01), EDAid candidate selection (S02), AgenticPD branch/context state (S03/S04), multi-agent post-place optimization (S08), native OpenROAD journals/policies (S05). A centralized repeated-call controller can perform the same coordination. | Pursue only the order-contrast representation below; agent names, messages, journals and checkpoint reuse are not contributions. |
| B: bounded unified prediction | From a placed design and a candidate resize/move, jointly predict post-GR WNS and total overflow, selecting a candidate before expensive checking. | HyPAS already uses learned timing/power with physical refinement (S06); CircuitNet supports congestion/timing tasks (S10). Independent heads plus nonlinear fusion and direct joint predictors are strong alternatives. | Do not pursue a general unified QoR model. Its coupled target set alone has no selected useful distinction; action labels/data are not presently possessed. |
| C: prediction plus scoped tool calculation | Learn the *difference between the outcomes of two action orders*, with common-mode interaction separated; invoke legalization, GR/RC/STA on chosen branches and retain only checked incumbents. | Sequential order/choice RL-LR sizing (S07), joint placement/sizing HyPAS (S06), nonlinear direct outcome models and exhaustive two-order rollout. | Select A+C with the two-output prediction of B only where necessary. Conditional finite-label/budget hypothesis, not a universal architectural advantage. |

## Problem and engineering decision

A physical implementation engineer has a legal pre-CTS placement with setup pressure and localized routing demand. The decision is whether to try a proposed resize followed by a proposed relocation, the reverse order, a singleton, or KEEP. Each primitive includes its own deterministic incremental legalization. A width change can shift cells; the next action then acts on the returned state. Consequently ordering can matter even when the *requested* cells are different. This is an inference and a model possibility, not a measured incidence finding. General coupled sizing/placement demand is evidenced by S06 §2.2 and S11 §§2.1–2.4; neither establishes the frequency or economic importance of this precise effect.

Downstream endpoints are legal, equivalent, routable post-DR outcomes, post-route WNS/TNS, power/area and total charged iteration cost. Post-GR WNS/overflow are decision feedback and training targets, not replacements for final routing. The workflow is deliberately restricted to one pair per decision, single declared PVT and ideal clocks. No multi-corner, post-CTS, hold, IR-drop or production signoff claim is made. Those would require new validation and cannot be silently added.

## Inputs, actions and deployment information

State s binds ODB/netlist, coordinates/masters, fixed objects, row/site geometry, placement/routing blockages, net graph, current GR demand/capacity, current STA slack/slew/load, Liberty/LEF/SDC, RC model, tool build, seeds and thread count by hashes. Current GR/STA acquisition is charged for every arm. Inputs are available at the decision boundary only after this acquisition; final-route reports and results from untried orders are forbidden model inputs.

A timing specialist observes critical-path/slack/load and library alternatives and emits at most K=4 deterministic ranked resize intents a=(instance,new_master). Initially only logically equivalent, single-height, supported orientation, width-changing master substitutions are allowed. A congestion specialist observes demand/capacity, local rows, connectivity and slack guards and emits at most K=4 ranked intents b=(different_instance,absolute_target_site). Candidate generation is common across controlled arms, with the same information and cap. K is a proposed experimental cap, not an observed optimum. The union includes KEEP and all singletons.

An action intent is frozen at s; it is not silently regenerated after the first action. T_a applies a to the current state, incrementally legalizes, records **all** resulting instance/master changes, validates legality/displacement and returns either a state or FAIL. T_b does the corresponding absolute-coordinate relocation and legalization. The two branches are s_ab=T_b(T_a(s)) and s_ba=T_a(T_b(s)). Width-change location is the current location on that branch. Master compatibility, legality and fixed objects are hard predicates, not learned scores. If an identifier, master or target is no longer admissible, the branch is FAIL. No assumption that requested and realized support coincide is allowed.

## Proposed causal mechanism

For an observed metric vector q(s)=[WNS(s), overflow(s)], define singleton changes u_a=q(T_a(s))-q(s), u_b=q(T_b(s))-q(s). For successful branches define residuals:

    r_ab = q(s_ab)-q(s)-u_a-u_b
    r_ba = q(s_ba)-q(s)-u_a-u_b
    m = (r_ab+r_ba)/2; d = (r_ab-r_ba)/2
    q_hat(s_ab) = q(s)+u_hat_a+u_hat_b+m_hat+d_hat
    q_hat(s_ba) = q(s)+u_hat_a+u_hat_b+m_hat-d_hat

The proposed predictor shares a bounded pair representation for the symmetric residual m and antisymmetric order contrast d across WNS and overflow. Inputs include the two intents, initial widths/locations, row whitespace, displacement radii, net/path overlap, current slack and demand. A mirrored order query must exchange outputs and negate d. This is an algebraic inductive bias, **not new mathematical expressivity**: a sufficiently flexible direct ordered-outcome model can represent the same function. Singletons are predicted at inference unless their measured outcomes already exist in the shared history; actual singleton measurements cannot be obtained for free. FAIL gets a separate classification target and no fabricated numerical q. Abstention is empirical and never a formal safety guarantee.

The timing and congestion specialists receive the same structured message `(state_hash, pair_ids, predicted_two_orders, abstain_flag, realized_checked_feedback)`. They can rank which *fixed* pair/order merits the next tool call. A deterministic arbiter enumerates the at-most-16 pairs, applies declared guard predictions only as ranking hints, and spends a fixed rollout budget on selected singletons/orders. Uncertain pairs may be tried, serialized under a conventional policy, or skipped according to a frozen stop rule shared by comparators. Every accepted incumbent is realized and freshly checked using whole-design GR/RC/STA; a final suffix runs DR and route-aware checks. Candidate failure restores the exact checkpoint. Termination is operation/time cap, no admissible proposal, or no checked improvement. No simultaneous database mutation by agents is permitted.

**H1 (CLM-009):** under finite common intervention labels and fixed complete decision cost, separating common interaction and order contrast improves selection of useful legal resize/relocation sequences compared with strong direct nonlinear outcome prediction, conventional order heuristics and sequential adaptive search. The hypothesized cause is easier learning of the smaller, order-sensitive residual on physically overlapping supports. It may fail because residuals are not smaller, ordering rarely matters, errors dominate or conventional methods already resolve it. Compare agent cooperation and central implementation separately; any representation gain does not demonstrate a need for multiple LLMs.

## What is and is not the proposed contribution

The candidate contribution is a tested label/representation and coordination interface for **realized, order-dependent legalization externalities of two specified physical edits**, with a measured finite-data quality/cost tradeoff. Components may be established. A useful systems result would need stronger evidence than a gain over isolated marginal addition. General sequential optimization, learning order, multi-agent objectives, nonlinear QoR, rollback and predict/check are already prior (S01–S09, S16).

The strongest immediate alternative is a symmetry-augmented nonlinear direct predictor trained on exactly the same five-state/pair records, plus the same arbiter and check budget. It may remove all advantage. A centralized implementation supplied with our same contrast model is an **equivalence control**, expected to select identical branches under identical ties and budgets; beating it is not a requirement or a credible claim. A central baseline without the representation but with all raw labels tests the representation, not “agents versus no agents.” If all useful benefit comes from extra physical labels, wider proposals, compute or a renamed implementation of existing work, the contribution fails. No theorem or super-additivity requirement is imposed.

## Analytical witness and its limits (CLM-008)

A lightweight deterministic row toy was executed; full code is in search-log.md. In a six-site row, A=(0,width1), B=(3,width1). Resize A to width2, keeping its current anchor; move B to site1. The active cell has priority and overlapping movable cells go to the nearest free legal site with deterministic ties. Resize-then-move returns A=(2,2),B=(1,1); reverse returns A=(0,2),B=(2,1). With deliberately dimensionless q=-(distance(A,5)+distance(B,0)), q(s)=-8, q(a)=-8, q(b)=-6, q(ab)=-4, q(ba)=-7. Marginal addition predicts -6 for both; residuals are +2 and -1, m=0.5,d=1.5. This proves a possible order-sensitive externality for this declared toy legalizer, not that OpenROAD behaves this way. Exhaustive rollout, an ordinary direct model and standard lookahead can also resolve it. It establishes neither novelty, representative incidence, trained performance nor PPA. Zero EDA calls were made.

## Claim ledger

| ID | Kind | Claim and locator | Limit / resolution |
|---|---|---|---|
| CLM-001 | observation | ChatEDA decomposes tasks, generates scripts, executes with feedback: S01 §III-A–C. | Not evidence about this order representation. |
| CLM-002 | observation | EDAid communicates plans/scripts and selects divergent candidates: S02 §3.1–3.3. | Code access not established; no gain transferred. |
| CLM-003 | observation | AgenticPD v3 branches over reusable stage states and stage contexts; GR selects incumbent, DR evaluates it: S03 §§2.1,3.1–3.4,Algorithm1; S04 selected functions. | v1 differs; v3 governs paper comparison, pinned code predates v3. |
| CLM-004 | observation | Native OpenROAD already has reversible nested batches and timing refresh: S05 MoveCommitter.cc 482–557; policy loop Optimizer.cc 157–196. | Selected code read only; no absence claim about all policies. |
| CLM-005 | observation | HyPAS combines constrained discrete repair, learned timing/power refinement and legalization: S06 §§2.2,3.2–3.7. | Does not establish final-DR performance here; no reported gain reproduced. |
| CLM-006 | observation | RL-LR sizing explicitly learns gate order and choice with incremental timing: S07 §§3.2–3.3. | Different IR-aware sizing problem; order learning itself is not new. |
| CLM-007 | observation | Contest optimization couples sizing, placement legality, timing/power and overflow: S11 §§2–4; S13 ProblemC. | General demand, not specific order-sensitive incidence. |
| CLM-008 | deduction + toy | Isolated marginals can fail to identify sequence outcome under our toy transitions. | Inline executed witness only, not a physical experiment. |
| CLM-009 | hypothesis | Joint symmetric/antisymmetric residual learning may improve finite-budget decision utility. | EXP-001–008; unmeasured, novelty unresolved. |
| CLM-010 | inference | Width-changing legalization can create relevant order externalities in this deployment slice. | Must measure with actual pinned adapter in EXP-003; potentially false/rare. |
| CLM-011 | observation | Current CircuitNet repository advertises multiple tasks and repaired feature files: S10 README changelog/tasks. | No paired interventions acquired; snapshot labels do not automatically supply them. |
| CLM-012 | observation | Commercial PPA search already advertised: S15 solution description. | No comparative commercial shortfall or unknown-internals claim. |
| CLM-013 | deduction | The representation is invertible for two successful outcomes and supplies no expressivity or optimality theorem. | Direct algebra; fair direct-model control mandatory. |
| CLM-014 | unresolved | Original winner implementations and full S08 method may eliminate the proposed distinction. | EXP-001; no search-absence novelty finding. |
| CLM-015 | governance | Batch grants research reading/derivation, no new physical/training allocation. | Frozen JOB and INNOVATION-BATCH-0002; future budgets are requests. |

## Counter-hypotheses, headroom and falsifiers

H0a: nearest prior work already specifies an equivalent useful representation/interface; inspect S08 and winner methods before pilot promotion. H0b: realized order contrast is zero or below repeat-run noise in representative inputs. H0c: the strongest direct predictor or conventional lookahead matches or dominates the proposed quality/cost curve. H0d: contrast is predictable only from unavailable future geometry. H0e: GR-selected improvements reverse after DR or violate constraints. H0f: data generation/training/proposal costs consume any deployment savings. H0g: a central implementation has identical decisions; this refutes multi-agent necessity but not by itself a separately evidenced representation contribution. Each has an explicit task below.

No theoretical physical saturation or optimum bound is asserted. The six-site example is not a lower bound on real PPA. If P paired oracle evaluations are avoided, average saved cost c is only an accounting approximation: savings require Pc > feature/model/communication/fallback overhead plus amortized training and label cost. Actual costs and deployment reuse count N are unknown. Report break-even N, or report no finite break-even if denominators are nonpositive. Low incidence bounds useful opportunity; measuring that is cheaper than training a large model.

## Feasibility, limits and final position

Public source reading, one abstract algebra/toy check and selected code audit are complete. Exact tool commits are identified in sources.json; they are **not compiled or compatibility-tested here**. No real checkpoint, rights-audited design/PDK bundle or paired dataset is allocated. The adapter and trained model are proposed work, not existing artifacts. Source access was improved by independently retrieving HyPAS, but S08 author downloads return an error page, and original winner code is unread. Two expansions found negative/prior evidence; the search stopped at a bounded research budget, not after two empty expansions.

Freeze this narrow anchor with zero initial drift. Acceptance, experiment consent and claims of demonstrated novelty/benefit are withheld. The conditional task list resolves prior-art overlap and real order incidence first, before any optional learned implementation. If no useful distinction survives, park with the negative record; no silent pivot to hold tables, stage orchestration, generic tuning or all-of-EDA models. Any new direction requires a new topic and ordinary independent review. No fifth batch cycle is requested or started.
