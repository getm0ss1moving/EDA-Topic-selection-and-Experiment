# File-mediated workflow

## State and storage

`draft -> submitted -> revision_requested -> submitted -> verified -> accepted`

A candidate may also become `parked` (missing feasible prerequisite), `rejected` (validated fatal flaw), or `abandoned` (evidence-backed joint proposer/challenger decision). Store unaccepted work under `candidates/EDA-NNNN/`; promotion copies the complete reviewed dossier to `topics/EDA-NNNN/` and removes the candidate copy in the same PR. Rejected, parked and abandoned dossiers may move to `archive/`; preserve history and resurrection conditions. `verified` is a candidate state, not permission to push directly to `main`.

## One review cycle

1. Human publishes a bounded research brief. Coordinator creates distinct role sessions and immutable packets at a full Git SHA.
2. Proposer searches and creates `proposal.md`, `sources.json`, `search-log.md`, `prior-art.csv`, `contest-audit.md`, `industry-gap.md`, `experiment-plan.md`, `forecast.json`, `tasklist.md`, the initial `direction-control.json` anchor and pending `experiment-consensus.json`. Mark dossier `submitted`; open a PR.
3. Coordinator freezes that proposal revision. Challenger independently searches before reading the author's forecasts; it then receives the full submitted dossier for detailed review. Record both packet SHAs. Write `challenges.md` with claim-level evidence and falsification tests.
4. Verifier opens the original sources and adjudicates every objection in `verification.md`. Until adjudicated, objections are allegations; the proposer must not treat them as established defects.
5. Coordinator releases the verified challenge packet. Proposer writes `responses.md`, resolving valid objections or disputing them with evidence. Revise the anchored mechanism, hypothesis, plan, task list and forecast together. Update both direction-drift penalties. A new combination or different engineering objective that replaces the anchor must become a new topic rather than a revision.
6. Proposer and challenger jointly finish `tasklist.md`. The proposer supplies the implementation and causal-test sequence; the challenger supplies falsification tests, fairness controls and missing prerequisites. When both independently judge the exact plan reasonable, they sign the same frozen revision and task-list SHA-256 in `experiment-consensus.json`. A change to the task list resets consensus.
7. Verifier checks revised claims, responses, anchor preservation, penalty records and experiment-task-list consensus, recalculates the content digest and writes `verification.json`. Only valid, unresolved, decision-critical objections block advancement. Unsupported challenges are closed with reasons. The verifier cannot replace either task-list consent.
8. Repeat up to three rounds by default. If innovation is exhausted, the relevant theoretical headroom is exhausted, the approach is a dead end, or no anchor-preserving direction remains, proposer and challenger may sign a joint-abandonment decision on the same full revision. Move the dossier to `archive/` with status `abandoned`; preserve evidence, penalties and resurrection conditions. A successor uses a fresh ID. Otherwise park with specific unresolved questions or request human arbitration; do not manufacture consensus. Do not delete old objections; append supersession links.
9. For promotion, verifier confirms the experiment consensus, dossier digest, current PR commit and a decision of `accept_for_pilot`. The distinct registered verifier GitHub account submits `CONFIRM <full-head-sha>` as an approving review. The merge controller/human merges only after checks pass.
10. Execute the preregistered pilot only after promotion. Update measured results by PR; revise, reject, or scale based on frozen thresholds. A forecast never becomes a measured result through acceptance.

## PR transport

Scientific communication exists in versioned files, including rebuttals, evidence corrections and decisions. PR bodies link these paths and identify scope; review bodies carry only confirmation metadata. Discussion in chat or GitHub comments is not admissible until copied into a file and independently checked. Do not use direct messages or shared agent memory.

Proposer/challenger/verifier each author their own output commits or submit an output packet to a transport-only human. Shared PR branches are permissible transport after packet collection, not shared live workspaces. A single coordinator account cannot impersonate independent review. Per-topic session IDs are immutable; session reassignment and contamination require a written event and a fresh session.

## Update and invalidation

Every content edit invalidates the dossier's previous content digest; every new PR head invalidates its review confirmation. Changes to scientific criteria, check scripts, harnesses or workflows remain governance PRs with automated checks; human approval is not required for these intermediate updates. Editing an accepted topic requires rechecking the affected evidence and experiments. New evidence may revoke acceptance through a PR, retaining the old decision in history.


## Human review scope (owner decision, 2026-10-13)

Human confirmation is required only for final topic and experiment reports. Final topic dossiers and their revisions live under `topics/`; standalone final reports live under `reports/final/`. Any addition, modification, deletion or rename touching these paths requires an approving `CONFIRM <full-head-sha>` review by a registered human reviewer distinct from the PR author. README scaffolding is excluded. A draft report outside these paths is not an approved final deliverable.

Proposer/challenger exchanges, evidence, responses, AI verification records, candidate drafts, project JSON, tools, harnesses and governance updates require PRs and passing automated checks, but no human approval. The coordinator may merge these intermediate PRs after checks pass, without self-approving or claiming independent scientific verification. AI verifiers must still adjudicate evidence before objections become established findings. Proposer/challenger agreement on the exact experiment task list and AI verification remain prerequisites for promotion and experimental execution; human final-topic approval completes the promotion gate. Final experiment reports require human approval again.

Branch protection keeps both required status checks but sets its unconditional approving-review count to zero. The `independent-verifier` check classifies changed paths and enforces human approval only for final deliverables. Human resource decisions and unresolved factual questions are not inferred from this exemption.
