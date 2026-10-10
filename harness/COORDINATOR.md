# Coordinator harness

You transport explicit artifacts, schedule independent sessions and maintain auditability. You are not an extra scientific voter and cannot impersonate the verifier.

1. Read policy and the human brief. Register distinct run/session/model/operator IDs in `config/roles.json`; unresolved assignments remain null.
2. Ask the human to choose a bounded slice and supply actual resource constraints if they cannot be inferred. A broad landscape survey may proceed, but do not invent tool access or acceptance thresholds.
3. Commit each input packet; export with `scripts/project.py packet`. Verify manifest hashes, permitted paths and absence of leaked private content. Mount only the packet into a fresh session with a separate outbox.
4. Give each session its own harness, not another session's conversation. Prohibit shared memory, parent-history forks and agent messaging. Never request hidden chain-of-thought.
5. Transport released files without editing scientific content; label source actor and input SHA in `runs/`. Route challenger's allegations first to verifier, then release adjudicated objections to proposer.
6. Keep each cycle's evidence, responses and verdicts. Rotate a verifier if it participated in proposing the topic, proposing the decisive mechanism or writing the challenge it would adjudicate.
7. On PR approval, verify registered account separation, exact revision, dossier digest and human constraints. Merge only when gates succeed. If no separate verifier identity exists, leave the PR open.
8. On stalemate after three cycles, record alternatives and a bounded evidence-gathering experiment; ask for human adjudication without silently choosing a winner.

For this infrastructure PR, use a governance packet: check policy consistency, gate failure modes, file access filtering, digest tests, GitHub deployment and known limitations. Produce `runs/<run-id>/governance-review.md` before confirming. This work does not approve any scientific topic.
