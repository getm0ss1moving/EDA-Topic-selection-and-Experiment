# Codex research team

This allocation creates nine EDA survey territories, each with one proposer and one challenger, plus three shared verifiers: 21 independent tasks in total. Names use the stable platform prefix `Codex`, role letter `P`/`C`/`V`, numeric identity and domain suffix. These are identities, not credentials. Other AI platforms must use their own platform prefixes and must not reuse these IDs.

## Current paused allocation

The user narrowed the eventual research scope to floorplanning, placement, CTS, routing and signoff, then paused all scientific role conversations until governance tooling and constraints are reviewed. Codex-P04-PHYSICAL, Codex-C04-PHYSICAL, Codex-P05-TIMING, Codex-C05-TIMING and Codex-V02-PHYSICAL are the only planned assignments in that future scope, but all five are currently archived and inactive. Their released files remain historical records. Do not resume them or create replacements without an explicit pause release. During governance hardening, at most one synthetic test role may exist at a time; its output cannot be treated as scientific evidence.

Platform families are fixed: Codex uses GPT, DeepSeek uses DeepSeek, Claude uses Claude. Actual model IDs must be recorded. DeepSeek Flash is permitted under the user's family rule; it must never be reported as V4 Pro.

## Model allocation

- Proposer: `gpt-6-astra`, `high` reasoning (user-selected to conserve quota); strongest available host tier for mechanism discovery and difficult synthesis.
- Challenger: `gpt-6-sol`, `medium` reasoning; a balanced starting point for broad retrieval and critical comparison. The model name does not guarantee critical thinking; the challenger harness provides the adversarial method.
- Verifier: `gpt-6-luna`, `medium` reasoning; bounded source/locator/entailment checking. Novel mathematical arguments, disputed impossibility claims, ambiguous mechanisms or conflicting source interpretation must return `needs_expert_review`. A fresh stronger verifier or human then adjudicates; the proposer cannot verify its own claim.

These are workload choices, not measured EDA benchmark rankings or price guarantees. The desktop host exposes these model IDs. Current [OpenAI model selection guidance](https://developers.openai.com/api/docs/guides/model-selection) supports the quality/efficiency tradeoff, and [reasoning guidance](https://developers.openai.com/api/docs/guides/reasoning) explains effort selection. Record actual model settings in `config/agents.json`; never silently substitute an unavailable model.

## Assignment table

| Domain | Proposer | Challenger | Shared verifier |
|---|---|---|---|
| D01 Architecture, specification and HLS | Codex-P01-ARCH | Codex-C01-ARCH | Codex-V01-DIGITAL |
| D02 RTL, formal verification and test | Codex-P02-VERIFY | Codex-C02-VERIFY | Codex-V01-DIGITAL |
| D03 Logic synthesis and technology mapping | Codex-P03-SYNTH | Codex-C03-SYNTH | Codex-V01-DIGITAL |
| D04 Floorplanning, placement and routing | Codex-P04-PHYSICAL | Codex-C04-PHYSICAL | Codex-V02-PHYSICAL |
| D05 Timing, extraction and signoff | Codex-P05-TIMING | Codex-C05-TIMING | Codex-V02-PHYSICAL |
| D06 Power, reliability and manufacturability | Codex-P06-RELIABILITY | Codex-C06-RELIABILITY | Codex-V02-PHYSICAL |
| D07 Analog, RF and mixed-signal automation | Codex-P07-ANALOG | Codex-C07-ANALOG | Codex-V03-SYSTEMS |
| D08 Packaging, chiplets and 3D systems | Codex-P08-CHIPLETS | Codex-C08-CHIPLETS | Codex-V03-SYSTEMS |
| D09 Agentic EDA and flow orchestration | Codex-P09-AGENTIC | Codex-C09-AGENTIC | Codex-V03-SYSTEMS |

## Startup and cost control

Each task initially verifies its packet, adopts its role, and writes a readiness record and a domain-specific first-pass plan. Do not start 21 unbounded searches just to instantiate the tasks. Further research rounds use explicit bounded file assignments. Domain scoping is preliminary and may be split after evidence shows the bottlenecks.

First-pass plans cover established algorithms, recent primary papers, official contests/winner reports, open implementations and public commercial evidence. Proposers plan opportunity discovery; challengers plan independent nearest-work and failure-mode discovery. No pair sees the other's initial private notes or conversation. The initial plan is not a survey result or an accepted topic.

Shared verifiers service three domain queues sequentially. They keep per-domain evidence ledgers and never transfer unpublished claims between teams. Escalate uncertain scientific reasoning instead of converting a lightweight source check into a final novelty verdict. A verifier's rejection is subject to the same evidence rules as any objection.

## Communication and identity

Use fresh project worktrees and frozen actor packets. Do not fork conversations. A worktree prevents write collisions but does not enforce OS-level read isolation. Agents are instructed to read only their own packet and output directory; actual hard isolation remains an operator/container responsibility.

Tasks write only their own outbox and return paths. The coordinator transports released files, not chat summaries or hidden reasoning. Neither a task ID nor the user's shared GitHub credential constitutes an independent GitHub reviewer. `github_review_identity` stays null until separately enrolled; this does not prevent research onboarding, but still prevents approved merging.

Project governance is still under PR review. These tasks may use its frozen draft for onboarding; that is not acceptance of the draft or permission to merge scientific topics. The agents may flag governance issues in their own output files.
