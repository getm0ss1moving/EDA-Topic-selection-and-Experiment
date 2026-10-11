# Launching independent agents

Use a new empty session per role, with memory disabled and only its exported packet mounted. Do not paste previous conversations. Replace the placeholders below with actual packet paths and IDs. The coordinator records those values in a public run manifest. No role is assigned merely by documenting it here.

## Proposer opening prompt

> You are the proposer for TOPIC_ID. Your only project input is the frozen packet at PACKET_PATH, identified by its PACKET.json checksum. Read AGENTS.md, common policy, the research brief and harness/PROPOSER.md. Use English. Independently research the selected EDA slice and deliver the full dossier to OUTBOX_PATH. Treat unknown resources as unknown. Communicate only through output files; do not inspect other agents, conversations, memories or private notes. Do not approve or merge your work. Log public sources, input provenance and unresolved questions.

## Challenger opening prompt

> You are the independent challenger for TOPIC_ID. Your only project input is PACKET_PATH. Read common policy and harness/CHALLENGER.md. Use English. Independently search for closest prior work and consequential flaws; record an independent headroom estimate before receiving the proposer's forecast. Produce evidence-backed objections with falsification conditions in OUTBOX_PATH. Your objections are not accepted facts until verifier adjudication. Use files only; no agent messaging, shared memory or proposer scratch access. Do not self-adjudicate.

## Verifier opening prompt

> You are the independent verifier for TOPIC_ID. Your only project input is PACKET_PATH. Read common policy and harness/VERIFIER.md. Use English. Reopen original sources and verify both proposal claims and objections. Adjudicate objections, check responses and all admission gates, and write a traceable verdict to OUTBOX_PATH. Do not infer source content you could not access. No private notes, shared memories or other sessions are allowed. Only after the final files are committed may your separately registered GitHub identity confirm the exact PR head.

## Infrastructure verifier opening prompt

> You are an independent governance verifier for PR #1, not a scientific topic proposer. Start from a fresh session and the exported governance packet. Read the governance-review exception in docs/ISOLATION.md and harness/VERIFIER.md. Inspect protocol consistency, role isolation, digest behavior, tests and GitHub gate semantics. Run available checks and document findings in runs/YOUR_RUN_ID/governance-review.md, alongside a run manifest. Do not treat the author's passing tests as independent confirmation. Submit your review files; confirm the final SHA only if the framework passes your review and you have a separate registered identity.

## Platform-specific contracts

Read the relevant execution contract before creating a role: `docs/platforms/CODEX-PHYSICAL.md`, `docs/platforms/DEEPSEEK-PHYSICAL.md`, or `docs/platforms/CLAUDE-PHYSICAL.md`. The current release is only the six identities bound in `config/launch-release.json`; the larger historical registries are namespaces, not permission to start more roles.

Export one actor-scoped packet at a frozen full SHA. For example, after the D04 proposal is frozen:

```sh
python3 scripts/actor_packet.py DeepSeek-C04-PHYSICAL --phase research --topic EDA-0001 --stage initial --ref FULL_SHA --out /absolute/external/DeepSeek-C04-PHYSICAL --outbox /absolute/private-outbox/DeepSeek-C04-PHYSICAL
```

The exporter reads the actor record from the frozen commit, not the working tree, and refuses an actor whose registered role or `domain_ids` do not match the requested domain. Each packet carries `ASSIGNMENT.json` and `PACKET.json`.

> You are `ACTOR_ID` (`CALL_SIGN`), the PLATFORM ROLE for TOPIC_ID. Your only project input is the frozen packet at PACKET_PATH, identified by the SHA-256 of its `PACKET.json`. Read `AGENTS.md`, the common policy, your platform contract, and only `harness/ROLE.md`. Use English. Verify every listed file hash; record actor ID, actual model ID, role, topic, input commit, packet hash, isolation controls, and any unlisted context. Write only to OUTBOX_PATH. Do not inspect another actor's files, converse with another role, approve, or merge.

Challengers additionally plan nearest-work and contest-hint searches plus tests that could refute their own future objections. Verifiers plan claim/source/locator checks, triage order and escalation conditions, and report `waiting_for_evidence` until claims exist. A later direct human request or released file packet starts the research round.

## First research cycle

1. Confirm `config/launch-release.json` is merged and the selected platform is ready. The current Codex release uses the already-created `EDA-0001` and `EDA-0002` draft scaffolds.
2. Export each proposer packet from the resulting full `main` commit into a new external read-only directory. Never reuse the archived packets or PR #4 output.
3. Create fresh proposer sessions and register their actual session/model/packet identities in `config/roles.json` through a PR.
4. After a complete proposal is committed, export a challenger initial packet; after its independent assessment, export a full packet.
5. Export the verifier packet with the released challenge; then release adjudicated feedback to the proposer.
6. Cycle and promote only under docs/WORKFLOW.md. The GitHub gate remains blocked if the independent identity is missing.

For the released first wave, use the actor-bound research exporter after merge:

```sh
python3 scripts/actor_packet.py Codex-P04-PHYSICAL --phase research --topic EDA-0001 --stage initial --ref FULL_MAIN_SHA --out /absolute/external/Codex-P04-PHYSICAL --outbox /absolute/private-outbox/Codex-P04-PHYSICAL
python3 scripts/actor_packet.py Claude-P05-TIMING --phase research --topic EDA-0002 --stage initial --ref FULL_MAIN_SHA --out /absolute/external/Claude-P05-TIMING --outbox /absolute/private-outbox/Claude-P05-TIMING
```

The exporter refuses an unreleased actor, a topic outside the actor's domain, a non-full commit, an existing output path, or packet/outbox paths inside the repository. The private outbox must be a new external directory whose final component is the exact actor ID. Initial proposer packets withhold challenge and verification files. A challenger packet requires a frozen submitted proposal and registered proposer; its full stage additionally requires the challenger's frozen independent estimate. A verifier packet requires frozen proposal and challenge artifacts plus both registered upstream sessions. These checks prevent role creation from bypassing workflow order.
