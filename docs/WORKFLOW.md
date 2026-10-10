# File-mediated workflow

## State and storage

`draft -> submitted -> revision_requested -> submitted -> verified -> accepted`

A candidate may also become `parked` (missing feasible prerequisite) or `rejected` (validated fatal flaw). Store unaccepted work under `candidates/EDA-NNNN/`; promotion copies the complete reviewed dossier to `topics/EDA-NNNN/` and removes the candidate copy in the same PR. Rejected/parked dossiers may move to `archive/`; preserve history and resurrection criteria. `verified` is a candidate state, not permission to push directly to `main`.

## One review cycle

1. Human publishes a bounded research brief. Coordinator creates distinct role sessions and immutable packets at a full Git SHA.
2. Proposer searches and creates `proposal.md`, `sources.json`, `search-log.md`, `prior-art.csv`, `contest-audit.md`, `industry-gap.md`, `experiment-plan.md`, `forecast.json`, and `tasklist.md`. Mark dossier `submitted`; open a PR.
3. Coordinator freezes that proposal revision. Challenger independently searches before reading the author's forecasts; it then receives the full submitted dossier for detailed review. Record both packet SHAs. Write `challenges.md` with claim-level evidence and falsification tests.
4. Verifier opens the original sources and adjudicates every objection in `verification.md`. Until adjudicated, objections are allegations; the proposer must not treat them as established defects.
5. Coordinator releases the verified challenge packet. Proposer writes `responses.md`, resolving valid objections or disputing them with evidence. Revise the mechanism, hypothesis, plan and forecast together.
6. Verifier checks revised claims and responses, recalculates the content digest and writes `verification.json`. Only valid, unresolved, decision-critical objections block advancement. Unsupported challenges are closed with reasons.
7. Repeat up to three rounds by default. At the limit, park with specific unresolved questions or request human arbitration; do not manufacture consensus. Do not delete old objections; append supersession links.
8. For promotion, verifier confirms a dossier digest, the current PR commit and a decision of `accept_for_pilot`. The distinct registered verifier GitHub account submits `CONFIRM <full-head-sha>` as an approving review. The merge controller/human merges only after checks pass.
9. Execute the preregistered pilot. Update measured results by PR; revise, reject, or scale based on frozen thresholds. A forecast never becomes a measured result through acceptance.

## PR transport

Scientific communication exists in versioned files, including rebuttals, evidence corrections and decisions. PR bodies link these paths and identify scope; review bodies carry only confirmation metadata. Discussion in chat or GitHub comments is not admissible until copied into a file and independently checked. Do not use direct messages or shared agent memory.

Proposer/challenger/verifier each author their own output commits or submit an output packet to a transport-only human. Shared PR branches are permissible transport after packet collection, not shared live workspaces. A single coordinator account cannot impersonate independent review. Per-topic session IDs are immutable; session reassignment and contamination require a written event and a fresh session.

## Update and invalidation

Every content edit invalidates the dossier's previous content digest; every new PR head invalidates its review confirmation. Changes to scientific criteria, check scripts, harnesses or workflows are governance PRs and need independent review. Editing an accepted topic requires rechecking the affected evidence and experiments. New evidence may revoke acceptance through a PR, retaining the old decision in history.
