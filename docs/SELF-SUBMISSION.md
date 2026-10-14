# Self-submission and frozen role releases

The owner authorizes proposer, challenger and verifier self-submission and self-freeze.
This replaces earlier instructions to wait for the owner/coordinator to freeze a
dossier. The verifier submits a compact table and matching machine record.
Human approval is still required for final topic and experiment reports.

## Actor procedure

1. In your own outbox, assemble a `release/` directory containing only completed
   role-owned files. Do not include private scratch, another actor's files,
   credentials, copyrighted papers, or licensed data. The file allowlist is in
   `scripts/role_submission.py`. Proposer releases contain proposal, evidence,
   plan, forecast, task list and direction control; challenger releases contain
   challenges and their own evidence/search records, optionally a task-list
   revision and independent estimate; verifier releases contain the two
   verification files. Shared names such as `sources.json` remain separate in
   each release. Never overwrite another role's evidence ledger. A proposer or
   challenger may add `experiment-consent.json` containing only its own consent
   block (`session_id`, `decision`, `signed_revision`, `tasklist_sha256`,
   `rationale`); the session must be the releasing session and the decision one of
   `pending`, `agree` or `revision_requested`. Host artifacts named `.DS_Store` or
   `.claude` are ignored and never released.
2. Use the trusted script supplied in your packet/amendment:

```sh
python3 /trusted/role_submission.py freeze \
  --source /assigned/outbox/release --queue /assigned/outbox/submissions \
  --role challenger --actor REGISTERED_ACTOR --session REGISTERED_SESSION \
  --topic EDA-0002 --ref FULL_INPUT_COMMIT --packet INPUT_PACKET_SHA256
```

3. Successful completion creates `submissions/SUB-<sha256>/` atomically. Its
   `SUBMISSION.json` binds identity, input provenance and every output byte.
   This directory is both the frozen release and submission request; no second
   permission or human freeze action is needed. Repeat submission of identical
   content is idempotent. Revisions produce a new ID; never edit an old release.
4. Record the release path in your output status. Missing resources or sources
   must remain explicit; freezing does not assert feasibility or completeness of
   scientific evidence. Finish the assigned phase without inventing signatures.

Readonly permissions are accidental-edit protection, not a security boundary.
The transporter rehashes content. The script rejects symlinks, unlisted files,
empty files, files over 8 MiB, bundles over 32 MiB, text that is not UTF-8,
malformed JSON and credential-like strings (API keys, tokens, private keys).
Releases are published to a public repository without human review, so these
checks run at freeze and again at publish. These limits apply to published research
text, not access to your own saved experimental outputs.

## Coordinator transport

```sh
python3 scripts/role_submission.py verify /assigned/outbox/submissions/SUB-HASH
python3 scripts/role_submission.py publish /assigned/outbox/submissions/SUB-HASH \
  --repo /path/to/EDA-Topic-selection-and-Experiment
```

`publish` checks current main's session registry, topic, role and input packet;
uses a temporary clone; preserves the frozen files under `runs/SUB-HASH/`;
runs project validation; pushes a dedicated `submit/HASH` branch and creates one
intermediate PR. When integrating a release, copy a submitted
`experiment-consent.json` unchanged into that role's `consents` entry of the
candidate's `experiment-consensus.json`; never write a consent for an actor. Retry finds an existing PR. It never executes actor code, changes final
reports, grants credentials to the actor, approves or merges a PR. The
coordinator attaches the PR, checks CI, merges and records the resulting commit.
If a push succeeds but PR creation fails, retry retains the remote branch; no
force push is permitted. Resolve a divergent remote branch explicitly.

The source commit identifies actor inputs, the release hash identifies actor
outputs, and the transport commit identifies repository storage. Do not confuse
these with the exact revision required by experiment-consensus signatures.

Integrating the release into the candidate and preparing the next role's packet
remain coordinator operations, requiring no human freeze confirmation. Preserve
role ownership and source-ID provenance, reset stale consent after a task-list
or dependency change, and route allegations to the verifier before the proposer.
First-pass forecast masking still requires semantic inspection; a filesystem
watcher cannot establish scientific readiness or independence.

Inside a round, `scripts/round_transmit.py` moves releases between local role inboxes
without GitHub (`docs/AUTO-ROUND.md`); the publication above then happens after the round.

This command-based transport is available now. It does not install a daemon or
claim that queues are continuously watched. An unattended deployment must pin
registered actor queue roots and provide a transport-only service identity;
never accept arbitrary paths or role registration supplied by a submission.

## Compact verification

Use `templates/topic/verification.md`: identity/input table, one row per critical
claim/objection, and the eight-gate table. Cite source ID plus exact locator,
verdict, whether blocking, and a short reason/action. No long narrative is
required. Retain `verification.json` for structural gates and digest binding.
Unavailable evidence is unresolved; a concise table cannot conceal missing
verification. Task-list dual consent and final human approval remain unchanged.
