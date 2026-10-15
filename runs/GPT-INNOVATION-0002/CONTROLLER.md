# Innovation batch controller

Owner request: two concurrent domains, four complete P/C/V cycles each, GitHub
publication each round and a Chinese owner topic report. See
docs/INNOVATION-BATCH-0002.md and config/codex-innovation-research.json.

This is a new batch, not a reset of GPT-FOUR-ROUNDS-0001. Do not read private
historical role conversations, scratch or runtime logs. Only explicitly released
same-domain predecessor files are supplied; no inherited approval.

Use scripts/codex_loop.py with --config config/codex-innovation-research.json
before the collect, dispatch and publish-pending subcommands. The active backend
is fresh app subagents with fork_turns=none, exact models/efforts from each JOB.
Proposer Sol6.1/high; challenger Astra/low; verifier Sol6.1/low. Native CLI model
fallback and old providers are not used. No unattended daemon is claimed.

After an app agent is successfully spawned, run controller.py --record-job PATH
--agent CANONICAL_TASK_NAME. controller.py alone checkpoints coordinator metadata,
public input descriptors and hash-verified released files. It never reads role
scratch or private transcripts. Keep state mutations sequential with publication;
the same CLI lock protects individual operations, but a long publication must
finish before collection. Mechanical corrections go to the same author with its
own retry-note path; do not rewrite science or invent consent.

Completed verifier output queues one round PR. Publish pending records, attach
every PR, inspect required checks and resolve actual mechanical findings. Merge
transport/governance PRs without self-approval or branch-protection bypass.
Preserve the exact source object with the public batch tag before dispatch.
Do not silently edit a frozen role packet when policy changes.

At four cycles per domain, do not start a fifth. After all eight PRs merge, run
controller.py --final to verify 24 release/job bindings, eight rounds and no pending
job. Read only the final released/adjudicated material for the Chinese owner
report. Publish the final audit/report by PR. Negative or unresolved results are
valid; no topic is accepted without real gates and dual consent. Historical
decisions, hypothetical thresholds and toy checks are never new EDA measurements.
