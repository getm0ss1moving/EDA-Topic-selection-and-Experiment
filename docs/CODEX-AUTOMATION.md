# Current Codex operation

Follow [WORKFLOW.md](WORKFLOW.md) and `config/research-workflow.json`.
Active AI roles: searcher, challenger, verifier. The human authors ideas and
revisions. There is no AI proposer and no automatic AI successor proposal.

A job uses a fresh session, common rules, only its assigned harness, exact released
inputs, a full input commit and hashes, and its own scratch/outbox. Release files
through PRs; the coordinator may merge after required checks without self-approval.
Raw challenges reach verifier before delivery of adjudicated feedback to the human.
All jobs retain external-research access and cross-role privacy.

Searcher produces bounded literature batches (first ten, target 100).
Challenger/verifier wait for human-authored ideas and matching frozen inputs.
Do not resume historical seats or their memories. Model requests for continuing
review roles remain Astra low and GPT-6.1-Sol low; availability is not attested
until an actual launch. Searcher inherits the configured runtime model without
an invented model override.

`scripts/codex_loop.py` is a historical P/C/V implementation, retained for status
inspection and offline regression tests. Current-checkout execution commands are
disabled. Old `config/codex-*.json` files point to replay settings in `legacy/`.
No live service, automatic human-idea dispatcher or end-to-end new review loop is
claimed by this cleanup. Scientific outputs are produced only by assigned,
independent role jobs, never by a coordinator signing for them.
