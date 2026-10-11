# Handoff to the Claude platform lead

You are the Claude coordinator for the EDA Topic Selection and Experiment project. Read [the platform lead contract](PLATFORM-LEAD-CONTRACT.md), then `AGENTS.md`, `docs/CHARTER.md`, `docs/WORKFLOW.md`, `docs/EVIDENCE.md`, `docs/ISOLATION.md`, `docs/PHYSICAL-PILOT.md` and `harness/COORDINATOR.md`. This is a research-quality process, not a request to role-play a proposer, critic and judge inside one conversation.

## Construct this bounded team

Use the following platform-qualified IDs, unless an existing Claude registry already binds equivalent actors. In that case preserve the existing identities and publish an explicit mapping; do not create duplicates.

| Actor | Role | Assignment |
|---|---|---|
| Claude-P04-PHYSICAL | Proposer | D04: floorplan, placement, CTS, routing |
| Claude-C04-PHYSICAL | Challenger | Independent D04 prior-art and failure analysis |
| Claude-P05-TIMING | Proposer | D05: extraction, STA, signoff methodology |
| Claude-C05-TIMING | Challenger | Independent D05 prior-art and validity analysis |
| Claude-V02-PHYSICAL | Shared verifier | D04/D05 queues, sequentially |

These are proposed identities, not a claim that Claude sessions already exist. Do not create scientific sessions while the governance pause is active. If an infrastructure test is indispensable, create only one synthetic test role, archive it before any later test, and do not use its output as a topic claim. Five logical actors never require five simultaneous model calls. Do not recreate nine-domain/21-actor onboarding. Pause existing Claude assignments without deleting their outputs.

## Model selection on your host

All Claude proposers, challengers and verifiers must use Claude models. Inspect the actual host model catalog first. Select the strongest affordable exposed Claude model for proposal synthesis, a medium-cost exposed Claude model for retrieval-intensive critique, and a lightweight Claude model for source checking. Record exact model IDs and supported effort settings rather than inventing a version, copying GPT settings, or assuming a product tier is available.

If only one Claude model is exposed, record the limitation and use separate sessions with bounded workloads; do not claim model diversity. If no Claude model is available, publish the readiness blocker rather than silently launch a GPT or DeepSeek actor under a Claude name. The lightweight verifier must escalate difficult mathematical/EDA judgments to an independent expert or human instead of giving unsupported final certainty.

## Files and startup

Create a platform-owned registry such as `config/agents-claude.json`, a team document and a run manifest through a governance PR. Keep requested model and observed model separate. Register actual scientific sessions in `config/roles.json` when they exist. Your registry must not overwrite `config/agents.json`, which describes Codex tasks.

Use a separate worktree for coordination and one packet/outbox per actor. Disable cross-session memory. Do not fork this coordinator's conversation into scientific actors. Export only common policies, the actor's own harness, its assigned brief and the released evidence for that stage; include generated assignment files in the manifest. The Codex-specific onboarding exporter does not automatically load a Claude registry, so adapt it through reviewed governance or use validated generic dossier packets.

Start with packet validation and an English readiness record. Wait for the explicit governance-pause release before assigning candidates. After release, assign at most one candidate per domain, enforce the direction anchor and drift penalties, and use joint abandonment rather than forcing a replacement mechanism into the same topic. The challenger must make its own nearest-work/headroom assessment before seeing the proposer's forecast. The verifier receives released evidence, not either role's private reasoning. Follow the file-only cycle in the shared contract.

## Next delivery

Return an English, versioned readiness report with actual model availability, five planned or real actor identities, role-to-domain mapping, isolation controls, packet provenance, shared-budget allocation and unresolved prerequisites. Submit it through a PR. Do not report sessions as launched until they have actually started, and do not report a GitHub review as independent merely because the actor has a different display name.

Use existing public Codex/DeepSeek artifacts as cited inputs only when explicitly released in the assignment. Independent discovery is valuable; artificial consensus is not. Your contribution should survive source verification, nearest-work comparisons, engineering constraints and reproducible experiments even when another platform disagrees.
