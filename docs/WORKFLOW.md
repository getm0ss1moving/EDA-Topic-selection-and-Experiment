# File-mediated workflow

## State and storage

`draft -> submitted -> revision_requested -> submitted -> verified -> accepted`

A candidate may also become `parked` (missing feasible prerequisite), `rejected` (validated fatal flaw), or `abandoned` (evidence-backed joint proposer/challenger decision). Store unaccepted work under `candidates/EDA-NNNN/`; promotion copies the complete reviewed dossier to `topics/EDA-NNNN/` and removes the candidate copy in the same PR. Rejected, parked and abandoned dossiers may move to `archive/`; preserve history and resurrection conditions. `verified` is a candidate state, not permission to push directly to `main`.

## One review cycle

1. Human publishes a bounded research brief. Coordinator creates distinct role sessions and immutable packets at a full Git SHA.
2. Proposer searches and creates `proposal.md`, `sources.json`, `search-log.md`, `prior-art.csv`, `contest-audit.md`, `industry-gap.md`, `experiment-plan.md`, `forecast.json`, `tasklist.md`, and the initial `direction-control.json` anchor. Mark dossier `submitted`; open a PR.
3. Coordinator freezes that proposal revision. Challenger independently searches before reading the author's forecasts; it then receives the full submitted dossier for detailed review. Record both packet SHAs. Write `challenges.md` with claim-level evidence and falsification tests.
4. Verifier opens the original sources and adjudicates every objection in `verification.md`. Until adjudicated, objections are allegations; the proposer must not treat them as established defects.
5. Coordinator releases the verified challenge packet. Proposer writes `responses.md`, resolving valid objections or disputing them with evidence. Revise the anchored mechanism, hypothesis, plan and forecast together. Update both direction-drift penalties. A new combination or different engineering objective that replaces the anchor must become a new topic rather than a revision.
6. Verifier checks revised claims, responses, anchor preservation and penalty records, recalculates the content digest and writes `verification.json`. Only valid, unresolved, decision-critical objections block advancement. Unsupported challenges are closed with reasons.
7. Repeat up to three rounds by default. If innovation is exhausted, the relevant theoretical headroom is exhausted, the approach is a dead end, or no anchor-preserving direction remains, proposer and challenger may sign a joint-abandonment decision on the same full revision. Move the dossier to `archive/` with status `abandoned`; preserve evidence, penalties and resurrection conditions. A successor uses a fresh ID. Otherwise park with specific unresolved questions or request human arbitration; do not manufacture consensus. Do not delete old objections; append supersession links.
8. For promotion, verifier confirms a dossier digest, the current PR commit and a decision of `accept_for_pilot`. The distinct registered verifier GitHub account submits `CONFIRM <full-head-sha>` as an approving review. The merge controller/human merges only after checks pass.
9. Execute the preregistered pilot. Update measured results by PR; revise, reject, or scale based on frozen thresholds. A forecast never becomes a measured result through acceptance.

## PR transport

Scientific communication exists in versioned files, including rebuttals, evidence corrections and decisions. PR bodies link these paths and identify scope; review bodies carry only confirmation metadata. Discussion in chat or GitHub comments is not admissible until copied into a file and independently checked. Do not use direct messages or shared agent memory.

Proposer/challenger/verifier each author their own output commits or submit an output packet to a transport-only human. Shared PR branches are permissible transport after packet collection, not shared live workspaces. A single coordinator account cannot impersonate independent review. Per-topic session IDs are immutable; session reassignment and contamination require a written event and a fresh session.

## Update and invalidation

Every content edit invalidates the dossier's previous content digest; every new PR head invalidates its review confirmation. Changes to scientific criteria, check scripts, harnesses or workflows are governance PRs and need independent review. Editing an accepted topic requires rechecking the affected evidence and experiments. New evidence may revoke acceptance through a PR, retaining the old decision in history.
