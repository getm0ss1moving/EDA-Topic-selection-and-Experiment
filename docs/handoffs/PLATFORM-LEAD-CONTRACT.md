# EDA research project: platform lead contract

This handoff is for a platform coordinator, not for direct injection into every scientific actor. Give each actor only its common policies, its own role harness and its assigned frozen input packet. All research, objections, responses and verdicts must be written in English.

## What the project is trying to discover

The goal is to produce defensible EDA research questions with a clear engineering beneficiary, a specific unsolved mechanism, a credible novelty argument, and a reproducible experiment plan. Agentic EDA, AI for EDA and traditional EDA are alternative research approaches, not mandatory ingredients. An agent wrapper, a new neural architecture, or a combination of existing techniques is not automatically a contribution.

A good proposal explains: who encounters the problem; where existing methods fail; what is genuinely different in the proposed mechanism; why it should help; what would falsify it; and whether the improvement matters under realistic constraints. Review papers, official contest statements and winner reports, open-source implementations and publicly documented commercial capabilities. Separate inaccessible evidence from evidence of absence: lack of an open implementation does not prove commercial superiority or academic novelty.

Do not mechanically reject every combination. Reject a combination with no nontrivial mechanism or meaningful demonstrated benefit. A structural change is also insufficient without an engineering need. A theoretical-bound objection must identify the exact assumptions and metric; a result already tight in one setting may leave a different practical bottleneck open. A contest's supplied method is prior art even when a participant never finished implementing it.

## Current scope and cost limits

Only two survey territories are active:

| Territory | Responsibility | Boundary |
|---|---|---|
| D04 PHYSICAL | Floorplanning, macro/cell placement, legalization, CTS, global/detailed routing | Own physical interventions; evaluate downstream routed results, not HPWL alone |
| D05 TIMING | Extraction, STA, corner robustness, timing closure/ECO, signoff methodology | Own timing/reference validity; coordinate overlaps through released files |

The intended scientific configuration is two cross-platform topic teams with six logical actors. Codex proposes D04 and verifies D05; Claude proposes D05 and verifies D04; DeepSeek challenges both. Role creation is released only by `config/launch-release.json` and proceeds in workflow order. Do not recreate the former 21-actor wave, create one pair for every physical stage, spawn nested agents or start all roles with scientific inputs simultaneously. Archive old assignments without deleting their work. Do not start an unrestricted research loop or retry quota failures automatically.

Read `config/research-brief.json` and `docs/PHYSICAL-PILOT.md`. The local pilot has an observed 10-CPU/16-GiB host and a pinned OpenROAD container with public Nangate45/GCD fixtures. Coordinator-selected caps are eight CPU-hours total, one two-CPU/4-GiB experiment at a time, zero GPU and zero paid API budget. These are project-wide pilot caps, not an allowance for each platform. Request an allocation in a versioned run record before consuming the shared experiment budget; do not assume access to another host's files or Docker image.

The completed GCD smoke proves a tool/data execution path. Its negative setup slack means timing is not closed. It does not prove R1 feasibility, novelty, macro-floorplanning coverage, multi-corner validity, commercial parity, or foundry-certified signoff. The numerical improvement thresholds in the brief are provisional screening criteria; calibrate them using baseline variance and practitioner needs before candidate evaluation. Preserve unknowns and attach concrete resolution tasks.

## Construct independent roles

The platform lead is a transport and scheduling coordinator, not a fourth scientific voter. It must not write both sides of an argument, dictate a verdict, relay private impressions, or fill in missing evidence for an actor under that actor's name.

| Role | Required work | Prohibited shortcut |
|---|---|---|
| Proposer | Map a bounded area, audit nearest prior work, identify a mechanism/gap, propose an intervention, specify baselines, ablations, tasklist and uncertain forecasts; respond to verified objections | Presenting a search summary or unsupported model forecast as a novel feasible topic |
| Challenger | Independently search nearest work and reason about novelty, useful headroom, practical objectives, constraints, experimental confounds and failure conditions; cite each material objection | Treating speculation as a fatal flaw or vetoing a proposal by assertion |
| Verifier | Reopen original sources, verify claim-level entailment and applicability, adjudicate both sides, inspect experiment sufficiency and revise/park/reject/accept-for-pilot with reasons | Rubber-stamping citations, inventing inaccessible evidence, or treating a cheap model as an expert mathematical referee |

Use the strongest affordable model within your platform family for proposal synthesis, a medium-cost model for the challenger's search volume and critique, and a lightweight model for bounded verification. Record actual model ID, host and supported effort. These are workload allocations, not claims about measured EDA ability. Escalate uncertain technical judgments to a fresh independent expert/human, with a file-based question and evidence bundle. Never reuse a proposer as its own verifier.

## File access and independence

Create fresh conversations without history forks. Disable shared-memory retrieval and generation. Prefer separate containers/accounts with only a read-only packet and private writable outbox mounted. A worktree or prompt rule alone does not enforce read isolation; record the actual controls honestly.

- Proposer: common policy, own harness, assigned brief/dossier, public sources and subsequently released adjudicated challenges. No challenger/verifier scratch or raw unadjudicated objections.
- Challenger: common policy, own harness, assigned frozen proposal and sources. Commit its independent assessment before receiving the author's forecast. No proposer scratch, unreleased replies or verifier notes.
- Verifier: common policy, own harness, released proposal/challenges/responses and original public sources. No private conversations or hidden reasoning.
- Coordinator: registries, manifests and explicitly released outputs. No private transcripts, chain-of-thought or cross-role memory.

Never use agent-to-agent chat to exchange scientific claims. Scheduling messages may identify a packet path, actor and deadline; the research content must be in files. Include generated scientific assignment files in the packet hash inventory. Log contamination, discard affected independence claims and restart the affected review in a fresh session. Preserve historical packets unchanged.

## One bounded research cycle

1. Verify the reviewed governance revision and publish a frozen domain assignment. Create distinct role/session IDs and outboxes. Record the full input commit and SHA-256 of `PACKET.json`.
2. Ask each proposer for at most one candidate in its territory. Require the complete dossier: proposal, sources with precise locators, search log, prior-art comparison, contest audit, industry-gap analysis, experiment plan, forecast and tasklist. Use `templates/topic/` and `docs/FORMATS.md` as the actual schema, not prose examples from this handoff.
3. Freeze the submitted proposal. Challenger writes an independent estimate before seeing the proposal forecast, then submits claim-linked, evidence-backed objections and possible falsification tests.
4. Verifier checks the objections and original sources. Only then release adjudicated objections to the proposer. Unsupported criticism must be closed with reasons rather than allowed to steer the proposal as fact.
5. Proposer responds and revises while preserving the frozen problem, engineering need and causal mechanism. Record combination-drift and demand-drift penalties. A straightforward combination or demand-free replacement cannot be accepted under the original topic ID. Preserve prior revisions and objections; link superseding evidence. Verifier checks the response and the updated dossier.
6. If evidence shows exhausted novelty, applicable theoretical saturation, a dead end, or no anchor-preserving direction, proposer and challenger may jointly abandon the same frozen revision. Archive it with evidence and resurrection conditions. Any replacement uses a new topic ID and fresh novelty search. Otherwise limit to three rounds, then park or request human arbitration rather than manufacture agreement.
7. Topic confirmation and experiment start require proposer/challenger agreement on the final experiment task list. Both must sign the same `tasklist.md` SHA-256 and frozen revision; any amendment invalidates both signatures. The verifier checks readiness and identity but cannot replace either consent.
7. For pilot admission, require representative designs, reproducible strongest accessible baselines, matched resource budgets, meaningful endpoints, guardrails, failure accounting and uncertainty estimates. Separate observed facts, inference, hypotheses and forecasts. A forecast is never an experimental result.

Research may proceed while some experiment prerequisites are unresolved, but the corresponding feasibility gate must remain conditional. The outcome may legitimately be “park” or “reject”; the objective is research quality, not maximizing accepted topics.

## GitHub and review

Repository: https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment

Make a platform-specific branch/worktree and submit PRs for governance and scientific changes. Keep unaccepted dossiers in `candidates/`; promote to `topics/` only through a reviewed PR. Do not overwrite another platform's roster, private files or outputs. Claim a unique topic/run ID through the shared registry before creating conflicting paths.

Register real scientific sessions in `config/roles.json`; a platform roster or task title alone is not a scientific-session registration. Record model requested versus model used, packet hashes, operator and independence attestation. Do not invent a GitHub login for an AI actor.

`M0nitor-EDA` is the registered independent GitHub account, distinct from PR author `getm0ss1moving`. Its invitation was accepted and write access was verified on 2026-10-11; this is not an approval. Verify current status before use. The account must actually review the final files and submit an APPROVE review with exactly `CONFIRM <full current PR head SHA>`. Registration is not consent, account access, a scientific verdict or approval. Never impersonate the account or ask actors to share its credentials.

Both dossier-level scientific verification and the current-head GitHub confirmation are required. Every new PR head invalidates the old confirmation. PR #1 is governance, PR #3 is Codex allocation/pilot configuration, and PR #2 is DeepSeek allocation stacked on that work; inspect current bases and SHAs instead of assuming a pending draft is merged. Keep dependent PRs coherent and rerun checks after rebasing. Run:

```sh
python3 scripts/project.py validate
python3 -m unittest discover -s tests -v
```

The current `scripts/actor_packet.py` reads the Codex roster. Do not pass a DeepSeek/Claude identity and assume it will work. Use an appropriately reviewed platform exporter, or adapt the generic packet tooling in a governance PR. Verify allowlists and generated assignment hashes before dispatch.

## First return from each platform lead

Submit a versioned, English readiness report containing the platform's released actor IDs, actual model availability, session/isolation controls, frozen input revisions, output locations, cost allocation, current blocking prerequisites and the next bounded file exchange. Label planned sessions as planned. Do not claim tasks were launched or reviews completed merely because this handoff describes them.

Reviewer identity correction: the user corrected the earlier username to `M0nitor-EDA`. The invitation to the unrelated `M0nitor` account was revoked and that login removed from the allowlist. Separate GitHub accounts satisfy account separation only; independent scientific review still requires a distinct verifier session and evidence record, even when both accounts belong to the same human.
