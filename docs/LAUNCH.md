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

## DeepSeek platform domain onboarding

The DeepSeek allocation in `docs/TEAM-DEEPSEEK.md` adds 21 actors over the shared `D01`-`D09` territories. Export one actor-scoped packet per actor at a frozen full SHA:

```sh
python3 scripts/project.py packet proposer  --domain D01 --actor DeepSeek-P01-ARCH  --ref FULL_SHA --out /absolute/external/DeepSeek-P01-ARCH
python3 scripts/project.py packet challenger --domain D01 --actor DeepSeek-C01-ARCH --ref FULL_SHA --out /absolute/external/DeepSeek-C01-ARCH
python3 scripts/project.py packet verifier  --domain D01 --actor DeepSeek-V01-DIGITAL --ref FULL_SHA --out /absolute/external/DeepSeek-V01-DIGITAL
```

The exporter reads the actor record from the frozen commit, not the working tree, and refuses an actor whose registered role or `domain_ids` do not match the requested domain. Each packet carries `ASSIGNMENT.json` and `PACKET.json`.

> You are `ACTOR_ID` (`CALL_SIGN`), the DeepSeek-platform ROLE for domain DOMAIN_ID. Your only project input is the frozen packet at PACKET_PATH, identified by the SHA-256 of its `PACKET.json`. Read `AGENTS.md`, `harness/ONBOARDING.md`, the common policy and `harness/ROLE.md`. Use English. Verify the hash of every listed file before relying on it, record your actor ID, role, domain, input commit, packet hash and any unlisted context you were exposed to, and write `readiness.json` plus `first-pass-plan.md` to OUTBOX_PATH. This turn is bounded onboarding only: do not begin a broad web survey, an expensive experiment, recurring monitoring, inter-agent conversation or a self-generated follow-up. Compute, tool, PDK and design access are unknown; record them as unknown rather than inventing them. Do not write into the packet, the shared checkout, another actor's outbox or repository governance. Do not approve or merge anything.

Challengers additionally plan nearest-work and contest-hint searches plus tests that could refute their own future objections. Verifiers plan claim/source/locator checks, triage order and escalation conditions, and report `waiting_for_evidence` until claims exist. A later direct human request or released file packet starts the research round.

## First research cycle

1. Human fills the brief's domain, user need, tools/data and resource limits.
2. Coordinator creates and commits a draft dossier with `python3 scripts/project.py init EDA-0001` on a research branch.
3. Export the proposer packet at that full commit and launch the first prompt.
4. After a complete proposal is committed, export a challenger initial packet; after its independent assessment, export a full packet.
5. Export the verifier packet with the released challenge; then release adjudicated feedback to the proposer.
6. Cycle and promote only under docs/WORKFLOW.md. The GitHub gate remains blocked if the independent identity is missing.
