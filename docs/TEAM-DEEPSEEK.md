# DeepSeek research team

Platform allocation for the DeepSeek host. It covers the same nine `D01`-`D09` territories defined in `domains/` as the Codex allocation in `docs/TEAM.md`, with an independent proposer and challenger per territory and three shared verifiers: 21 tasks.

Two disjoint platforms surveying the same territory is deliberate. A territory is then investigated twice by two model families, and a proposal authored on one platform can be challenged and adjudicated on the other. Self-review inside a single platform family is weaker evidence than cross-platform review, even when sessions are technically separate.

This document records an allocation. Documenting a role does not assign it, does not constitute a scientific result and does not approve any topic.

## Identity and naming

Names use the stable platform prefix `DeepSeek`, role letter `P`/`C`/`V`, a two-digit identity and the domain suffix from `domains/`:

| Field | Pattern | Example |
|---|---|---|
| `actor_id` | `DeepSeek-<P\|C\|V><NN>-<SUFFIX>` | `DeepSeek-P01-ARCH` |
| `call_sign` | `DSK-<Spark\|Forge\|Ledger>-<SUFFIX>` | `DSK-Spark-ARCH` |

`actor_id` is the stable machine identity used in `config/agents-deepseek.json`, packets, commits and PR bodies. `call_sign` is a readable handle for dialogue logs and status reports. Role words are `Spark` (proposer), `Forge` (challenger) and `Ledger` (verifier).

The `Codex-*` identities in `docs/TEAM.md` and the `DeepSeek-*` identities here are disjoint namespaces. No platform may reuse another platform's prefix, and a platform must not silently operate under another platform's identity. Other platforms joining later pick their own prefix and add their own allocation file rather than extending this table.

These are identities, not credentials. An `actor_id` proves nothing about who actually ran the session.

## Model allocation

The host exposes exactly two DeepSeek model IDs, both confirmed present in the active profile configuration (`deepseek-official` default and the `deepseek-lab` provider entry): `deepseek-v4-pro` and `deepseek-flash` (DeepSeek-V41-Flash). Reasoning effort accepts `off`, `low`, `high` and `max`; there is no `medium` tier, so the middle of the ladder is expressed through the model choice rather than an effort label.

| Role | `model_requested` | `reasoning_requested` | Workload rationale |
|---|---|---|---|
| Proposer | `deepseek-v4-pro` | `max` | Strongest available model at deepest effort. Mechanism discovery, nearest-work synthesis and residual-headroom argumentation are the quality-critical path; `max` effort is spent only on the search and writing round. |
| Challenger | `deepseek-flash` | `max` | Critical depth is supplied by `max` effort and by the adversarial method in `harness/CHALLENGER.md`, while the cheaper per-token model makes large independent retrieval affordable. `deepseek-flash` also carries a 1M-token context window in this profile, which suits ingesting broad search corpora. |
| Verifier | `deepseek-flash` | `low` | Lightest tier for bounded source identity, locator and entailment checks. The verifier does not need deep generation; it needs cheap, repeatable checking over many sources. |

This is a three-tier cost ladder: strongest model at maximum effort for generation, cheap model at maximum effort for high-volume criticism, cheap model at minimum effort for checking.

Two consequences are binding:

- The lower tiers may not adjudicate difficult science. Per `harness/VERIFIER.md`, novel mathematical arguments, disputed impossibility claims, ambiguous mechanisms, conflicting source interpretation or a contested impossibility-of-improvement claim must return `needs_expert_review`. A fresh stronger verifier or a human then adjudicates. Escalation is the correct output, not a confident guess.
- Model IDs are recorded as requested, not as guaranteed. If a host does not expose the requested model, the operator records the actual model in `config/agents-deepseek.json` and the run manifest. Silent substitution is prohibited. These are workload choices, not measured EDA benchmark rankings or price guarantees.

A first onboarding wave was executed on the DeepSeek host as a bounded rehearsal. That runtime exposes no per-agent model override, so all 21 onboarding runs executed on the host default model `deepseek-flash` even though the registry requests `deepseek-v4-pro` at `max` for proposers. The actors detected and reported this themselves. `model_requested` therefore describes the intended independent launch, and the proposer tier remains unexercised: before any R1 proposal round is treated as a proposer-quality contribution, either the operator confirms the substitution in writing or the proposer sessions are launched on a host that actually exposes `deepseek-v4-pro`. This is recorded in `config/agents-deepseek.json` and in the onboarding run manifest.

Model diversity between proposer and challenger is intentional, but `docs/ISOLATION.md` is explicit that model diversity is not proof of independence.

## Assignment table

| Domain | Territory | Proposer | Challenger | Shared verifier |
|---|---|---|---|---|
| D01 | Architecture, specification and HLS | DeepSeek-P01-ARCH (`DSK-Spark-ARCH`) | DeepSeek-C01-ARCH (`DSK-Forge-ARCH`) | DeepSeek-V01-DIGITAL (`DSK-Ledger-DIGITAL`) |
| D02 | RTL, formal verification and test | DeepSeek-P02-VERIFY (`DSK-Spark-VERIFY`) | DeepSeek-C02-VERIFY (`DSK-Forge-VERIFY`) | DeepSeek-V01-DIGITAL (`DSK-Ledger-DIGITAL`) |
| D03 | Logic synthesis and technology mapping | DeepSeek-P03-SYNTH (`DSK-Spark-SYNTH`) | DeepSeek-C03-SYNTH (`DSK-Forge-SYNTH`) | DeepSeek-V01-DIGITAL (`DSK-Ledger-DIGITAL`) |
| D04 | Floorplanning, placement and routing | DeepSeek-P04-PHYSICAL (`DSK-Spark-PHYSICAL`) | DeepSeek-C04-PHYSICAL (`DSK-Forge-PHYSICAL`) | DeepSeek-V02-PHYSICAL (`DSK-Ledger-PHYSICAL`) |
| D05 | Timing, extraction and signoff | DeepSeek-P05-TIMING (`DSK-Spark-TIMING`) | DeepSeek-C05-TIMING (`DSK-Forge-TIMING`) | DeepSeek-V02-PHYSICAL (`DSK-Ledger-PHYSICAL`) |
| D06 | Power, reliability and manufacturability | DeepSeek-P06-RELIABILITY (`DSK-Spark-RELIABILITY`) | DeepSeek-C06-RELIABILITY (`DSK-Forge-RELIABILITY`) | DeepSeek-V03-SYSTEMS (`DSK-Ledger-SYSTEMS`; moved from V02 by run `DSK-ROLE-SUCCESSION-0001`) |
| D07 | Analog, RF and mixed-signal automation | DeepSeek-P07-ANALOG (`DSK-Spark-ANALOG`) | DeepSeek-C07-ANALOG (`DSK-Forge-ANALOG`) | DeepSeek-V03-SYSTEMS (`DSK-Ledger-SYSTEMS`) |
| D08 | Packaging, chiplets and 3D systems | DeepSeek-P08-CHIPLETS (`DSK-Spark-CHIPLETS`) | DeepSeek-C08-CHIPLETS (`DSK-Forge-CHIPLETS`) | DeepSeek-V03-SYSTEMS (`DSK-Ledger-SYSTEMS`) |
| D09 | Agentic EDA and flow orchestration | DeepSeek-P09-AGENTIC (`DSK-Spark-AGENTIC`) | DeepSeek-C09-AGENTIC (`DSK-Forge-AGENTIC`) | DeepSeek-V03-SYSTEMS (`DSK-Ledger-SYSTEMS`) |

Shared verifiers service three domain queues sequentially. They keep per-domain evidence ledgers and never transfer an unpublished claim from one queue to another. A verifier that participated in proposing a topic, proposing its decisive mechanism or writing a challenge it would adjudicate must be rotated out.

## Planned slice and current hold

The allocation above is the full nine-territory roster. Which part of it may run is a separate, explicitly recorded decision, because starting all 21 actors would spend budget without producing a bounded result. `config/agents-deepseek.json` carries an `activation` block; `scripts/project.py validate` checks that active and deferred actors partition the registry. An explicit `paused_governance` state permits zero active actors and forbids active domains.

The only planned post-release research slice is the physical-design and signoff slice, on the owner's budget directive:

| Domain | Column | Proposer | Challenger | Verifier | Topic container |
|---|---|---|---|---|---|
| D04 | Partitioning, floorplanning, macro and standard-cell placement, legalization, clock-tree synthesis, global and detailed routing | DeepSeek-P04-PHYSICAL | DeepSeek-C04-PHYSICAL | DeepSeek-V02-PHYSICAL | `EDA-0001` |
| D05 | STA, multi-mode/multi-corner analysis, extraction, crosstalk and signal integrity, timing closure and ECO, signoff fidelity | DeepSeek-P05-TIMING | DeepSeek-C05-TIMING | DeepSeek-V02-PHYSICAL | `EDA-0002` |

No scientific actor is currently active. The cross-platform release permits creation of only `DeepSeek-C04-PHYSICAL` and `DeepSeek-C05-TIMING`, both as challengers after their corresponding proposals are frozen. Every DeepSeek proposer and verifier remains deferred, as do all non-D04/D05 actors. The historical `DSK-R1-READY` records show that packets were prepared at an earlier revision; they do not authorize launch and are superseded by the current release matrix.

Budget deferral is a resourcing decision, not a scientific judgement: it says nothing about whether D01, D02, D03, D06, D07, D08 or D09 contain better problems. Deferred actors keep their identity, domain binding, packet and onboarding record, so releasing them later needs no reassignment and no new identity.

D04 and D05 are planned together on purpose. The two territories share a boundary that a single-territory survey tends to hide: a placement, CTS or routing objective is only meaningful against the timing model and signoff oracle that grade it, and a signoff study is only meaningful against the physical implementation it measures. `domains/D04/brief.json` and `domains/D05/brief.json` assign the boundary explicitly, and any cross-boundary claim must be carried through a released file rather than an agent message.

## Cross-platform review matrix

The strongest available review for a DeepSeek proposal is a Codex challenger, and vice versa. The coordinator should prefer the opposite platform whenever a suitable opposite-platform actor exists and has not touched the artifact:

| Artifact authored by | Preferred challenger | Preferred verifier |
|---|---|---|
| `DeepSeek-P*` | `Codex-C*` for the same domain | Any verifier from a third platform, or a non-authoring Codex verifier |
| `Codex-P*` | `DeepSeek-C*` for the same domain | Any verifier from a third platform, or a non-authoring DeepSeek verifier |

If only one platform is available, same-platform review may proceed but must be labelled single-platform review and cannot be presented as cross-platform confirmation. The GitHub confirmation gate is unchanged: only an account listed in `VERIFIER_LOGINS` may approve, and every actor in this allocation currently shares the owner's single GitHub account, so none of them can satisfy that gate alone. Merging therefore remains blocked until a genuinely separate identity is enrolled, exactly as described in `docs/GITHUB.md`.

## Dialogue protocol

Dialogue is file-mediated. Chat, agent messaging and shared memory are not admissible evidence; only committed files are. Each round has a fixed input packet and a fixed output contract.

| Round | Actor | Reads | Writes |
|---|---|---|---|
| R0 onboarding | every actor | own frozen packet: common policy, own harness, `harness/ONBOARDING.md`, own domain brief, own assignment | `readiness.json`, `first-pass-plan.md` in own outbox || R1 proposal | proposer | own R0 packet plus the released research brief | full dossier from `templates/topic/`; dossier state `submitted` |
| R2 challenge | challenger | frozen R1 proposal, prior-art evidence and experiment plan, with `forecast.json` withheld until its own headroom estimate is recorded | `challenges.md` with `OBJ-NNN` entries and evidence updates |
| R3 adjudication | verifier | submitted dossier plus published challenges; opens original sources independently | `verification.md` adjudicating every objection |
| R4 response | proposer | only adjudicated objections released by the coordinator | `responses.md`; mechanism, hypothesis, plan and forecast revised together |
| R5 re-verification | verifier | revised dossier and responses | `verification.json`, recomputed `dossier_digest`, decision |

Round order is not negotiable and no actor may skip to a later round on the strength of a chat summary. At most three cycles run by default. On stalemate the dossier is parked with explicit unresolved questions and referred to the human rather than resolved by consensus. Old objections are never deleted; they are superseded with links.

A challenger cannot veto by assertion and a verifier cannot silently rewrite a proposal. Per `docs/CHARTER.md`, the challenger bears the same evidence burden as the proposer.

## Independence limits on this host

The DeepSeek actors run on one desktop host with shared filesystem, shared cache and a single GitHub credential. Consequently:

- Worktree and outbox separation prevents write collisions and accidental cross-reads. It is not an operating-system security boundary.
- Agent Teams members share one host session. Their outputs are role drafts and are never independent verification of each other.
- Packet-based isolation is enforced by the exporter's allowlist (`scripts/project.py packet --domain`), not by filesystem permissions.
- No member of this allocation may approve a PR containing its own output.

A domain packet directory contains two files that are not part of the frozen git tree: `ASSIGNMENT.json`, which the exporter generates, and `PACKET.json`, which is the manifest itself. The exporter records the SHA-256 of `ASSIGNMENT.json` under the manifest's `generated` map so the envelope is hash-covered too; `PACKET.json` cannot list its own digest. An actor that finds any packet file absent from both maps must report it rather than assume it is legitimate.

Stronger isolation requires separate containers or accounts with only the packet mounted read-only, as described in `docs/ISOLATION.md`.

## Startup and cost control

Each task's first turn is bounded onboarding: verify every listed packet file hash, adopt the role, and write `readiness.json` plus a domain-specific `first-pass-plan.md`. Do not start 21 unbounded searches merely to instantiate the tasks. A later direct human request or released file packet starts a research round.

`config/research-brief.json` now records a measured local smoke path and provisional coordinator caps, metrics and thresholds. It does not establish representative publication designs, macro-floorplanning coverage, multi-corner signoff or practitioner-validated effect sizes. Actors must preserve those limitations and may not promote a topic or start experiments until the dossier-specific feasibility and consensus gates pass.

## Status

Governance hold. No DeepSeek actor has produced a survey, a proposal, a challenge or a verification. No topic is claimed. The D04/D05 topic containers are empty draft scaffolds, and their direction-control and experiment-consensus records remain pending. No R1 role may start until the governance stack is merged, the current head passes independent GitHub confirmation and the coordinator records an explicit release.

**Update 2026-10-13 (true UTC; 2026-10-14 local host date), per run `DSK-ROLE-SUCCESSION-0001`:** the owner moved the DeepSeek platform out of the challenger role and into the project's verification platform. `DeepSeek-C04-PHYSICAL` never ran and its seat passed to the Codex successor `Codex-C04-PHYSICAL-R2`; `DeepSeek-C05-TIMING` completed onboarding and a full round-1 challenge whose record is transported in `runs/DSK-C05-SESSION-0001`, and its seat continues with `Codex-C05-TIMING-R2`. `DeepSeek-V02-PHYSICAL` is released as the D04+D05 verifier (`deepseek-flash` at low effort for bounded source checks), and the D06 verifier binding moved to `DeepSeek-V03-SYSTEMS`. See `config/launch-release.json` `role_handoffs` for the owner-authorized records.
