# Isolation and access policy

## Trust boundary

A directory rule, `.gitignore`, read-only file bit or separate worktree is not a security boundary. A public repository cannot make committed files confidential. Isolation here means controlled input exposure and auditable independent execution. Strong enforcement requires separate containers/OS accounts with only the packet mounted read-only, an output directory mounted writable, no repository `.git`, no shared home/cache/memory, no other sessions, and scoped network credentials. This project supplies packet export and policy; it does not claim to sandbox an unrestricted desktop agent.

## Access matrix

| Actor | May read | May write | Must not read |
|---|---|---|---|
| Proposer | Common policy, own harness, brief, assigned dossier, released verified challenges and decisions, public sources | Proposal/evidence/plan/forecast/responses in own outbox | Unreleased challenger notes, verifier scratch, other sessions or memories |
| Challenger | Common policy, own harness, brief, frozen proposal/evidence/plan; forecasts only after independent assessment | Challenge and supporting evidence files in own outbox | Proposer scratch, verifier scratch, other role harnesses, unreleased responses |
| Verifier | Common policy, own harness, submitted dossier, published challenges/responses, public original sources, provenance manifests | Verification/adjudication files in own outbox | Private reasoning or transcripts of either other role |
| Coordinator/human | Public protocol, released output packets, run manifests and repository state | Packet manifests, transport commits, assignments | Private chain-of-thought; do not inject private cross-role context |

A challenger packet intentionally withholds `forecast.json` on first pass. Use `--stage full` after it has committed its independent estimates. Proposer first-pass packets withhold raw challenges and verifier material; `--stage full` releases only a round the coordinator has confirmed as adjudicated. The exporter filters file names, not the semantics of prose: the coordinator must check that released files contain no private notes or unadjudicated material.

## Session setup

Start a fresh, empty conversation for each role. Do not fork full history; do not preload summaries from another role. Prefer different models for diversity, but model diversity is not proof of independence. Disable cross-session memory retrieval, agent messaging and unrestricted task inspection. Never share raw chain-of-thought. All scientific claims and concise justifications must be explicit in artifacts.

Run `python3 scripts/project.py packet ROLE EDA-0001 --ref FULL_SHA --out /absolute/external/path` to export tracked allowlisted data only. The output includes checksums and origin commit; it excludes `.git`, other harnesses, untracked files and symlinks. For infrastructure review before dossiers exist use `--governance` instead of a topic ID. This explicit governance-review exception includes all public harnesses and templates for consistency checks, but excludes scientific dossiers and private notes. It does not assign the reviewer another scientific role. Supply the resulting packet as the role's entire working directory. Run the agent in an actual container or account if access restriction must be enforced.

## Contamination response

Stop the affected role, log the exposed artifact/session IDs (not private reasoning), discard its independence claim, start a clean replacement session and rerun the affected review. The human records an exception if continuing; an exception cannot be called independent confirmation.

Governance packets include the three tracked dossier-area README files so offline structural validation has the same empty-area scaffolding as a clean checkout. To release additional public audit evidence, append `--evidence-run RUN_ID` (repeatable, governance only); this exports only named committed run directories and still excludes other dossiers/runs. Check manifests and review the chosen run contents before export.
