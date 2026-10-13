# Research charter

## Objective

Identify a concrete EDA bottleneck; map the closest prior solutions; locate a demonstrable limitation; propose a causal mechanism; define a falsifiable hypothesis and a feasible experiment. Cover Agentic EDA, AI for EDA, and traditional algorithmic EDA without preferring an AI component for its own sake.

## Hard gates

- Novelty: identify the nearest papers, implementations, contest statements and winner solutions. Search terminology variants and citation neighborhoods. A missing search result is not proof of novelty.
- Nontrivial contribution: a combination must produce a new mechanism, interaction, formulation, guarantee, or demonstrated capability unavailable from a straightforward composition. Structural novelty also needs evidence and utility.
- Engineering utility: specify the user, workflow stage, decision, deployment constraints and meaningful improvement threshold. A proxy alone is insufficient without a measured relation to the downstream objective.
- Remaining headroom: distinguish a proven lower bound, a bound under restrictive assumptions, an empirical plateau and a compute-limited baseline. A claim of saturation needs its assumptions and residual gap. Challengers bear the same evidence burden as proposers.
- Contest originality: implementing a supplied baseline, organizer hint, known winner approach, or unfinished task is not by itself a research contribution. A new limitation beyond the given idea may qualify if explicitly demonstrated.
- Feasibility: baseline, data rights, tool access, compute budget and correctness oracle must be identified before accepting an experiment-ready topic.
- Evaluation integrity: no train/test leakage, cherry-picked designs, uncharged search budget, or inconsistent PDK/tool/corner conditions.
- Direction integrity: freeze the problem, engineering user, downstream need, causal mechanism and mechanism invariants before challenge response. A proposer may narrow or repair that mechanism, but cannot escape a valid objection by replacing it with a straightforward combination or an optimization with no demonstrated engineering demand under the same topic ID.

## Direction-drift penalty

Score two penalties independently on every substantive revision: `combination_drift` and `demand_drift`, each from 0 to 3. Zero preserves the anchor. One is a minor implementation-level drift that still preserves the causal mechanism and downstream need. Two means the proposed contribution has materially become a straightforward composition, or its objective has shifted to a weakly justified proxy/user need. Three means the original research question has effectively been replaced. Penalties are lexicographic governance constraints: reported PPA, runtime, model score, or search convenience cannot compensate for them. Any component at 2 or above, or total at 3 or above, blocks further experimental advancement until the original anchor is restored or a joint-abandonment review begins. Accepted topics require a total of zero.

## Joint abandonment

A topic may be abandoned when evidence supports at least one of four grounds: no innovative mechanism remains after verified prior-art challenges; relevant headroom is close to a theoretical limit under applicable assumptions; the causal approach is a documented dead end; or the anchored direction cannot change without becoming a different or demand-free topic. The proposer and challenger must independently agree on the same existing frozen commit and dossier digest and sign the same decision record. A registered verifier independently checks the cited evidence and process before archive validation. Abandonment is not failure concealment: archive the full dossier, objections, evidence, penalties and resurrection conditions. A replacement starts under a new topic ID and repeats novelty search; it cannot silently inherit acceptance or erase negative evidence. The verifier cannot force either scientific role to consent.

## Experiment task-list consensus

Topic confirmation and experiment authorization require proposer/challenger agreement on a final `tasklist.md`. The proposer owns the causal-test and implementation sequence; the challenger must add or require decisive falsification tests, fairness controls and missing dependencies. Both independently sign the same frozen revision and exact task-list SHA-256 in `experiment-consensus.json`. Agreement asserts that dependencies, resources, baselines, metrics, correctness oracle, stop rules, owners and procedures are reasonable and executable; it does not assert that the hypothesis or forecast is true. The verifier checks the two consents and readiness fields but cannot substitute its own consent. Any later task-list change invalidates the agreement and requires both roles to sign again.

Failure of an unsupported premise means revise or collect evidence, not automatic rejection. When the evidence instead establishes a dead end and both scientific roles agree, use joint abandonment. Acceptance authorizes a research plan; it does not establish novelty universally or promise publication.

## Decision rights

The human owns priorities, resources and exceptions. The proposer owns a hypothesis. The challenger owns independently researched objections. The verifier owns source checking and whether each objection is valid, overstated, unsupported, or unresolved. None may confirm their own output as independent evidence. A second verifier or a human adjudicator handles contested verifier conclusions through written files.

## Research incentives

Reward disconfirmation, corrected citations and useful negative results. Do not reward proposal count, objection count, impressive forecasts or forced consensus. Freeze evaluation criteria before results. Publish uncertainty and archive negative outcomes. Reopen decisions when new prior art or evidence appears.

Human GitHub approval is reserved for final topic and experiment reports, as specified in `docs/WORKFLOW.md`. Intermediate PRs use automated checks and role-specific AI verification without requiring a human approval review.
