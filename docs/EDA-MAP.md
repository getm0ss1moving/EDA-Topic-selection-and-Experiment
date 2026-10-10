# EDA scoping map and investigation agenda

This is a coverage checklist, not a completed survey or a claim about current best results.

| Area | Candidate engineering objectives | Common evaluation traps |
|---|---|---|
| Specification, architecture, HLS | Functional correctness, throughput, energy, area, verifiability | Generated-code pass rate without synthesis or equivalence |
| RTL design and verification | Bug discovery, proof coverage, engineer time, regression cost | Test leakage, vacuous assertions, shallow simulation |
| Logic synthesis and technology mapping | PPA under libraries and timing constraints | Unrealistic libraries; cell count as a complete area proxy |
| Floorplanning, placement, routing | Routability, congestion, timing, wirelength, runtime, legality | HPWL improvements that disappear after detailed routing |
| Timing, signoff, extraction | WNS/TNS, corners, uncertainty, SI, extraction fidelity | Surrogate timing versus signoff; unfair corner selection |
| Power, reliability, physical verification | IR/EM, DRC/LVS, yield, aging, thermal limits | Missing power activity, impossible manufacturing assumptions |
| Analog, RF, mixed-signal | Spec satisfaction, robustness, yield, simulation budget | Typical-corner optima without Monte Carlo or parasitics |
| Packaging, chiplets, 3D | Interconnect, thermal, partition, integration costs | A single objective ignoring coupled constraints |
| Agentic EDA and flow orchestration | Correct completed tasks, wall time, cost, reproducibility | Agent verbosity or benchmark success without tool correctness |

For each chosen slice, map input/output artifacts, production decisions, correctness oracle, dominant cost, assumptions, accepted baselines and current pain points. Agentic studies must compare agent orchestration against scripts, simple search, non-agent LLM use and strong classical methods at equal total cost. AI studies must test distribution shift across designs, families, nodes and corners where feasible. Traditional studies must compare implementation quality as well as algorithmic novelty.

Use `contest-audit.md` to separate organizer-provided concepts, public baselines, competitor innovations, unresolved tasks and hidden constraints. Use `industry-gap.md` to distinguish missing features, missing integration, data/PDK advantage, engineering maturity and actual algorithmic gaps. Public evidence about commercial products cannot establish their undisclosed algorithms.

Prioritize a narrow slice only after the human brief fixes tool and data availability. Do not select a thesis topic solely from this checklist.
