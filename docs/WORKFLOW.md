# File-mediated automatic research workflow

Current owner policy, 2026-10-15: all new proposer, challenger and verifier work
uses ChatGPT/Codex. `docs/CODEX-AUTOMATION.md` defines the active runtime.
Historical Claude/DeepSeek runs remain evidence. They are never resumed by the
new coordinator and their signatures are not transferred to successor roles.

## Research cycle

1. The coordinator prepares three distinct logical role seats from a committed
   source snapshot. Every job receives common rules, its own harness, the bounded
   brief, its own previous released output and explicitly released shared files.
2. Proposer surveys papers, contests, open implementations and public industry
   capabilities. It writes the complete anchored proposal, evidence, forecast,
   experiment plan and executable task list, then self-freezes.
3. The coordinator automatically delivers the proposal and starts the challenger.
   Challenger reads the cited primary material and independently searches newer
   papers, formulations, contest editions, hints, baselines and winner reports.
   It records evidence-backed objections or an honest feasible/unresolved outcome,
   proposes task-list corrections and self-freezes. Codex review is unblinded;
   do not claim forecast blindness.
4. The coordinator starts the verifier on the matching frozen proposal/challenge
   pair. Verifier reopens evidence, adjudicates every objection, checks important
   positive claims and writes compact tables plus JSON. A challenge alone cannot
   veto or force a proposal revision.
5. Verifier self-freezes. Its ruling and exactly the challenges it adjudicated are
   delivered to the proposer. Each completed three-role round is queued for one
   automatic GitHub PR with exact releases, registrations and outcome. A GitHub
   outage leaves a durable retry queue and does not discard the research.
6. Proposer responds, revises and repeats. Keep the original anchor and two drift
   penalties. New scientific directions receive new IDs. Preserve negative results
   and explicitly supersede errors; never erase the original objection.
7. For a promising topic, proposer and challenger independently sign the same
   frozen proposal and exact experimental task-list hash. Consent collection is
   automatic and does not consume a substantive review round. Verifier checks
   evidence, all readiness criteria, both consents and the eight acceptance gates.
8. For exhausted novelty, applicable theoretical saturation, a documented dead end
   or no viable anchor-preserving direction, proposer and challenger independently
   sign the same abandonment target and digest. Verifier checks the grounds.
   Archive the complete record and start a successor under a new ID automatically.
9. After three substantive rounds without convergence, park with exact unresolved
   questions and start a fresh successor. Human arbitration is optional. Never
   convert lack of consensus into acceptance or joint abandonment.

## Decisions, promotion and experiments

The human owns priorities and actual resource allocations; proposer owns the
hypothesis, challenger owns objections, verifier owns evidence adjudication, and
the coordinator owns scheduling and transport. No role signs for another.

Formal acceptance requires the complete dossier under `topics/EDA-NNNN/` to pass
`project.py validate`: distinct sessions, evidence-backed gates, zero direction
drift and matching experiment consents. Runtime `selected_for_pilot` is recorded
with its evidence; it does not bypass canonical dossier validation or authorize
unallocated experiments. Parked/rejected/abandoned dossiers live under `archive/`.
A replacement has a new ID and repeats novelty search.

Bind consent to an earlier immutable `SUB-<sha256>` proposal or a full Git commit.
A consent file cannot reference the hash of its own containing release. Changes to
the science, task list or referenced dependencies invalidate consent.

## GitHub and human review

Every completed round and governance change uses a PR. The coordinator may merge
its transport PR after all required checks pass, without self-approval. Research
selection and abandonment do not require a human reminder, separate GitHub
account or approval. Human review of final topic/experiment reports is optional;
it can be explicitly re-enabled with the repository variable
`REQUIRE_HUMAN_FINAL_REPORTS=true`. The independent scientific verifier remains
mandatory regardless of this administrative setting. No GitHub approval is
fabricated or treated as scientific verification.

Scientific communication travels only in released files, never shared memories,
private conversations or direct scientific role messages. PR descriptions identify
paths, release IDs and scope; do not substitute chat/comments for evidence files.
Private logs, credentials, copyrighted full papers and restricted designs stay out
of public releases. Structural CI checks form and provenance, not scientific truth.
