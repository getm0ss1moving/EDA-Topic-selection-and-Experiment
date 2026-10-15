# EDA-0005: Selecting post-CTS placement moves through joint hold-repair options

## Decision and provenance

**Round 1 position: a bounded useful-combination hypothesis, with novelty and engineering advantage unresolved. Continue documentary and analytical review; do not select for a physical pilot yet.** Neither adding hold checks nor reserving whitespace is the proposed contribution. Both have direct prior art. The candidate is an action-specific interface that makes *joint physical repair feasibility* part of the placement-move decision, before committing those moves. It must outperform a faithful conventional composition using the same information and repair options to become a research contribution.

Actor: ChatGPT-P04-PHYSICAL-EDA-0005. Logical session: 07ec73dc-1bf7-4f5c-999f-b589460c1e5e. Input commit: f68c1492c05be3fac5622deac4bb479eabf957de. Packet: b9b3d8bc704ac6b8b70e549417c704d5f4a0f3d966bdfe6c33bc9af9790bdef6. All 31 packet file hashes and the three supplied predecessor manifests were checked successfully. Research was unblinded. Only supplied policy, own proposer harness and explicitly released historical files were used; no foreign private material, checkout, messages or scientific subagents were accessed.

EDA-0003's residual-domain pin-access compilation remains historical and parked. This proposal neither compiles its residual CSP nor inherits any signature, verdict or approval. Its scientific action is datapath placement plus compensating hold-buffer placement, rather than fixed-placement pin-access feasibility. Historical lessons about complete costs and representative endpoints remain methodological lessons only.

## Required three-lens comparison before selection

| Candidate | Concrete action, state and interaction | Closest work and strongest alternative | Choice |
|---|---|---|---|
| A: cooperating physical-repair agents | Placement and hold-repair agents propose movement/repair bundles against one immutable post-CTS database. A shared ledger records occupied sites, candidate net splits, rejected bundles and checkpoint identity. A deterministic arbiter resolves overlapping edits; termination is a fixed EDA/token budget or no admissible move. | ChatEDA already orchestrates tools (S01); EDAid already combines divergent proposals (S02). AgenticPD v3 has stage-conditioned search and knowledge retrieval (S03/S04). Compare a repeated-call single agent, independent parallel proposals and deterministic lookahead with exactly the same state. | Not selected: distinct prompts do not explain a capability beyond deterministic repair planning. Extra invocations are a cost, not a causal mechanism. |
| B: bounded unified action predictor | From a post-CTS state and a proposed cell relocation, jointly predict changes in setup slack, hold-repair buffer demand and local routing overflow. Choose which movement to try, using no future-route inputs. | PreRoutGNN supplies coupled timing representations (S09); AiEDA supplies common data interfaces (S10), not proof of this joint predictor. Compare separate heads plus fusion, a shared-trunk multitask model and analytical sensitivity ranking under identical labels. | Not selected: action-conditioned repair labels and cross-family data are missing; negative transfer and indirect repair costs could dominate. A training campaign is unjustified today. |
| C: analytical proposal ranking plus physical repair specialist and finite option selection | Rank a small movement neighborhood cheaply, then ask a specialist for explicit candidate hold repairs and their overlapping site/connection footprints. Select movements only together with a feasible repair bundle, and re-evaluate the complete edited design before retaining it. | Setup/hold-aware placement (S11), power-aware hold closure (S12), constrained buffer-hole planning (S13), resource reservation (S14), current OpenROAD (S05/S06), and resource sharing (S22) are strong conventional competitors. | **Selected for adversarial refinement:** no learned model or LLM is required. The scientific question is whether explicit shared repair options alter useful physical decisions at an acceptable total cost. |

Candidate A is a possible implementation of C, not a second selected mechanism. Candidate B is a competing architecture, not a required added component. Switching to autonomous script generation or to a general timing predictor would require a new topic.

## Problem, user and downstream need

User: an implementation engineer considering small, timing-driven datapath cell relocations after clock-tree synthesis and an initial global route. A movement that helps a late path can also change a short path; compensating buffers then need legal sites and routes that other repairs may need. The decision is which bounded movement bundle to accept *after accounting for its implementable hold repairs*, not which movement has the largest immediate slack estimate.

S12's abstract/introduction and S15's physical-constraint discussion support the general relevance of repair side effects. They do not establish this repository's incidence, seconds lost or willingness to integrate a new optimizer. Candidate-specific demand remains EXP-002. Public vendor capabilities already include concurrent optimization (S20); there is no claim that commercial tools lack this mechanism.

Primary endpoint: paired change in **post-detailed-route extracted worst setup slack, ns**, at fixed die, SDC, library, initial clock tree and technology. Guardrails: no new hold-violating endpoint, no added route DRC/connectivity failure, no worse ERC count, and <=2% cell-area and estimated-power regressions. Record setup/hold TNS, all failures, displacement, memory and total iteration cost. The brief's provisional +0.02 ns and <=20% runtime-regression screens are starting criteria, not demonstrated demand or forecasts. Validate or amend them before candidate runs, never after seeing a result. HPWL, predicted buffer count and global-route slack are diagnostic proxies.

## Stage boundary, inputs, outputs and oracle

Input is a legal, frozen **post-CTS/post-initial-GR checkpoint**, propagated clocks, complete min/max constraints, library tables, row/site geometry, fixed blockages, netlist and global-route state. The initial intended domain is single-clock, single declared mode/corner, combinational datapath cells with single-height legal sites. No clock-tree rewiring, register movement, retiming, logic restructuring or functional change is allowed. A cell relocation is the primary intervention. An allowed noninverting buffer chain and bounded neighboring legalization shifts form its repair intervention. Initial clock cells and their connectivity are fixed; data rerouting can still affect physical clock parasitics, so final analysis checks the entire design.

Output is an edited placement/netlist plus an auditable movement/repair manifest, or KEEP_BASELINE/UNKNOWN. An option is a *physical edit*, not a promise of a delay: inserted cell type(s), insertion edge/load set, legal site interval(s), moved-neighbor list, anticipated route-demand footprint, affected checks and generating checkpoint. Shared options can repair several endpoints; two independent insertions cannot silently claim the same site. Every option belongs to the full candidate placement bundle that generated it.

Oracles: (1) exhaustive finite-table enumeration for selector implementation; (2) pinned OpenROAD legality and full min/max OpenSTA after fresh GR parasitics for each retained in-loop bundle; (3) complete DR, connectivity, declared DRC, extraction and full min/max STA for final evaluation; (4) functional equivalence across buffer insertion. A table certificate is exact only for its table. GR feasibility is not DR routability, and neither is foundry signoff. An independent DRC/connectivity/equivalence configuration and representative post-CTS inputs remain unresolved dependencies.

## Mechanism and invariants

1. Freeze checkpoint x and enumerate at most six deterministic candidate cell relocations, grouped so alternative destinations for one cell are mutually exclusive. A cheap first-order delay/displacement score ranks them; it does not certify timing. Enumerate subsets X with at most two relocations for the first witness (22 subsets for six distinct cells), including the empty subset. This is a bounded neighborhood, not global placement optimality.
2. Apply X in an isolated child state, legalize within its declared movement budget, and recompute full-design GR parasitics/min-max STA. Newly violated or worsened hold checks define D(X); existing hold failures remain explicit guardrails rather than disappearing from the accounting.
3. Generate a capped set O(X) of concrete repair templates using the same library, connectivity and geometry in every comparator. Each template contains its complete sites, moved neighbors, load partitions and topology. The cap and truncation rate are recorded. Site coverage and shared insertion conflicts form an option hypergraph. Approximate route-demand and timing effects rank options only.
4. For fixed X, use binary option variables z_o. Require each d in D(X) to be covered by at least one selected applicable option; require nonoverlapping physical occupancies and compatible net splits. Shared-buffer options cover multiple checks. Minimize an explicit area/displacement/estimated-routing-work score lexicographically. A small enumeration or MILP solves this finite model; this is ordinary combinatorial optimization, not a new exact solver.
5. Apply the complete X plus selected repair options, reroute and recompute *full* min/max STA/legality/ERC. Independent option effects do not add soundly under slew, fanout and route changes. A failed realization removes that exact combination from the current search; never infer a general monotone no-good across other placements or checkpoints. With at most eight options and two placements per bundle, enumerating all 256 option subsets is a finite-model oracle, not permission to execute that many EDA calls.
6. Within a predeclared expensive-call/time budget, retain the best actually evaluated guardrail-satisfying bundle. On a cap, use UNKNOWN or retain baseline; count wasted work. Repeat from a new checkpoint only if the budget allows; invalidate old physical options. DR checks the reported incumbent against the baseline using the same final-flow procedure.

The changed interface is prospective, *jointly realizable repair edits* feeding back into placement selection. Standard rollback, a site reservation bitmap, a checker, a new MILP label, or a better predictor alone is not the claimed contribution. The interface may be an engineering composition already subsumed by earlier methods. That is an explicit null hypothesis.

## Claim ledger

| ID | Type | Claim and locator | Status |
|---|---|---|---|
| CLM-001 | Observation | Tool orchestration/multi-agent proposals are prior: S01 §III; S02 §§3.1–3.3. | Checked method descriptions; no performance transfer. |
| CLM-002 | Observation | AgenticPD v3 searches at GR and applies final DR to its incumbent: S03 §2.1 and Algorithm 1. | Version-specific; v1 differs. |
| CLM-003 | Observation | OpenROAD already aggregates violating loads and rolls back harmful hold fixes: S06 lines574–599 and633–684. | Source inspection; not a measured bug or inability. |
| CLM-004 | Observation | Repair side effects after legalization/routing are established: S12 abstract/introduction. | Publisher preview; full algorithm uninspected. |
| CLM-005 | Observation | Early allocation of hold-fixing placement/routing resources is prior: S14 Summary; claims1,4,6,9. | Public patent disclosure; no legal or production assertion. |
| CLM-006 | Observation | Simultaneous relocation/buffering/sizing is a contest task: S17 Problem C. | Completing that task is not novelty. |
| CLM-007 | Observation | Timing/placement/routing resource sharing is prior: S22 abstract and §3.2–3.3 snippets. | Full method access incomplete. |
| CLM-008 | Deduction | Independent feasibility of repair demands need not imply joint feasibility; shared repair can reverse this. | Finite witness below; no physical incidence claim. |
| CLM-009 | Hypothesis | Action-specific repair options improve post-route placement decisions beyond equally informed serial repair, reservation and eager rollout. | Unmeasured and scientifically unresolved. |
| CLM-010 | Unresolved | Representative incidence, useful effect, faithful strongest comparator and affordable overhead. | EXP-001/002/004–007. |
| CLM-011 | Deduction | Exhaustive option selection is exact for complete fixed table predicates only; template infeasibility does not imply physical impossibility. | Direct finite enumeration argument. |
| CLM-012 | Observation | Post-CTS, hold constraints and iterative ECO are already announced contest extensions: S15 §5.3. | Negative evidence against broad novelty. |
| CLM-013 | Governance | This batch grants reading/analytical checks, no new training/full-flow allocation. | JOB/prompt and INNOVATION-BATCH-0002. |
| CLM-014 | Observation | Prediction-guided post-GR physical optimization already exists: S08 abstract, §1 and optimization evaluation. | Does not establish this action interface. |
| CLM-015 | Observation | Small gate moves to create buffer holes are prior: S13 §3.1/Eq.3 and §3.2. | Generic whitespace planning is not new. |

## Analytical witness, negative control and cost bound

A deliberately abstract example has candidate moves A,B,C with ranking values30,25,20, at most two moves allowed. A induces repair hA with only site s1; B induces hB with only s1; C induces hC with only s2. Each site holds one buffer. Independent ranking chooses A+B (55), which has no joint assignment; A+C (50) is the best feasible subset. Enumeration checked all seven subsets of size<=2. **Ordinary capacity matching also solves this instance, and a serial A-then-C policy reaches the same answer.** Therefore this witness validates a modeling obligation and refutes neither a strong baseline nor existing tools.

Second negative control: if one shared buffer at s1 can repair both hA and hB without violating setup, A+B becomes feasible. A model demanding a distinct buffer for each endpoint would incorrectly reject it. Current OpenROAD's shared-load handling makes this control necessary. The analytic assignments are not a netlist, EDA run, learned-model result or measured slack gain.

Let G be common baseline work, R extra baseline rework attributable to avoidable repair conflicts, K option-generation/selection overhead and V any extra oracle work. Under *identical final physical outcomes and all other work*, a time-saving mechanism requires K+V<R and relative saving <=R/(G+R). R is unknown; a tiny conflict rate can eliminate practical headroom. If outcomes differ, compare final WNS/PPA and costs directly rather than applying this bound. No global optimum, polynomial physical solver or theoretical saturation is asserted.

## Nontrivial combination test and counter-hypotheses

The contribution route is a possible useful systems combination. The intended delta over coarse reservation is assigning scarce concrete repair alternatives jointly with the movement that causes them. The decisive baseline is **eager conventional lookahead using the identical option hypergraph**, plus native and serial methods. A faster implementation of the same computation without meaningful downstream value is insufficient.

H0a: published reservation/buffer-planning methods already establish this same capability. H0b: hold-repair competition rarely changes the chosen movement on legitimate inputs. H0c: equal-budget serial repair or complete rollout recovers the same frontier. H0d: full-route ranking changes erase GR benefits. H0e: option generation, omissions, invalidations and fallback exceed any saved rework. H0f: result differences come from a stronger candidate generator, privileged labels, extra EDA calls or a weakened hold/DRC contract.

EXP-001 must map the exact interface to S11–S15/S22 and recent winners. EXP-004 needs a legal physical witness and a nonconflict negative control. EXP-005/007 must charge every option/failed EDA call and preserve candidate universes. Reject the useful-contribution claim if no benefit survives these controls. A negative outcome is valid research; do not attach an LLM or change the engineering user to rescue it.

## Feasibility, search coverage and current position

Research reading and a tiny Python combinatorial sanity check were completed. No physical flow, solver benchmark, model training, new service or remote computation was run. Source metadata includes actual access limits; code was read, not built. The baseline toolkit is documented in the packet, but its old smoke and provisional caps are not an allocation or an observed readiness audit for this topic.

Known gaps: full S11/S12/S22 method comparison; complete ICCAD2025 and ISPD2026 winner methods; 2026 multi-corner padding lead; representative hold-stressed post-CTS families; independent physical oracle; practitioner threshold; full pinned environment and costs. Searches expanded from agents/predictors to constrained buffer planning/patents and then current contest roadmaps. They found closer negative evidence; the round ends with bounded-search exhaustion, not two empty expansions or a novelty certificate.

Tasklist defines documentary work now and resource-gated physical work later. Forecast numbers are null. No experiment consent is emitted. Request independent challenge and verification of this exact hypothesis and its admitted overlap; seek an anchor-preserving evidence refinement in the next round. Initial combination_drift=0 and demand_drift=0 do not imply novelty or readiness.
