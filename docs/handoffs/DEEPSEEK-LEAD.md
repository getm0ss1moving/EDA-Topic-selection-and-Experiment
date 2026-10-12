# Handoff to the DeepSeek platform lead

You are the DeepSeek coordinator for the EDA Topic Selection and Experiment project. Read [the platform lead contract](PLATFORM-LEAD-CONTRACT.md), then `AGENTS.md`, `docs/CHARTER.md`, `docs/WORKFLOW.md`, `docs/EVIDENCE.md`, `docs/ISOLATION.md`, `docs/PHYSICAL-PILOT.md` and `harness/COORDINATOR.md`. Your job is to maintain independent, evidence-driven file exchanges—not to produce a simulated debate in one shared conversation.

## Your current team

Reuse these stable IDs from the existing DeepSeek roster:

| Actor | Role | Assignment |
|---|---|---|
| DeepSeek-P04-PHYSICAL | Proposer | D04: floorplan, placement, CTS, routing |
| DeepSeek-C04-PHYSICAL | Challenger | Independent D04 prior-art and failure analysis |
| DeepSeek-P05-TIMING | Proposer | D05: extraction, STA, signoff methodology |
| DeepSeek-C05-TIMING | Challenger | Independent D05 prior-art and validity analysis |
| DeepSeek-V02-PHYSICAL | Shared verifier | D04/D05 queues, sequentially |

Pause/archive every scientific assignment in your own runtime and registry while governance construction is active. Preserve their released files. Remove D06 from V02's future assignment without rewriting historical packet manifests. If a harness test is required, run only one synthetic role at a time and do not create a scientific verdict. Do not silently change Codex's or Claude's task state.

## Model policy clarification

The user has now specified platform families: all DeepSeek proposers, challengers and verifiers must use DeepSeek models. The prior unresolved request to approve Flash in place of V4 Pro is superseded by this family rule. If your host exposes only `deepseek-flash`, it is an allowed family member for all three roles; document the actual configuration and its limitations. Do not state that an output was produced by `deepseek-v4-pro` unless the runtime proves that it was.

Prefer your strongest affordable exposed DeepSeek option for proposers, medium-cost search/critique settings for challengers and lightweight bounded source checks for the verifier. Do not default every actor to maximum effort. If per-agent overrides do not exist, record that fact; do not invent a tier separation. Keep historical requested/actual model records intact and append the new policy resolution.

## Reconcile existing onboarding before R1

Your public PR #2 registry records the original 21-actor onboarding and a requested-versus-actual model discrepancy. Update its current allocation and policy through a PR. Do not retroactively relabel those runs as a stronger model or as completed research.

After DeepSeek's platform readiness block is cleared in a reviewed launch release, require the DeepSeek proposer and challenger to co-produce and separately sign the exact final experiment task list before any topic confirmation or experiment scheduling. A verifier checks this consensus but does not create it.

Inspect the released packet manifests for unlisted assignment content and any disclosed context exposure. Put future `ASSIGNMENT.json` content in the hashed input inventory. For any contaminated scientific review, create a clean replacement session; do not dismiss the issue because the source was another agent on the same platform.

Read the new research brief: resources are no longer wholly unspecified, but the GCD smoke is only infrastructure evidence. Macro-rich designs, representative benchmarks, additional corners and the relevant signoff oracle remain topic-dependent prerequisites. Replace historical onboarding packets with new immutable role-specific packets; do not mutate old packets in place.

## Next delivery

Create only `DeepSeek-C04-PHYSICAL` and `DeepSeek-C05-TIMING`, after the corresponding proposal is frozen. Before creating either session, work through [the challenger launch checklist](DEEPSEEK-CHALLENGER-CHECKLIST.md). Record the observed DeepSeek model ID, session state, packet hashes and isolation controls in an English run record and PR. These sessions are challengers: they must independently search prior art, estimate headroom before seeing the proposer forecast, and issue evidence-backed objections. Do not create DeepSeek proposers or verifiers, promote a topic, self-approve, or start a broad actor wave.

Coordinate across platforms only using released repository artifacts. Do not import Codex/Claude private conversations, imitate their hypotheses to manufacture agreement, or treat three platform votes as evidence. A cross-platform review still needs a new, independent verifier session with an explicit packet and claim-level source checks.
