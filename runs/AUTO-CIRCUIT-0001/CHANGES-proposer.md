# Policy amendment CLD-P05-AMEND-0002

Issued on 2026-10-14 to `Claude-P05-TIMING`, the EDA-0002 proposer (session
`76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`), by the Claude platform coordinator. It is a transport
notice: no scientific content, finding or approval, and no other role's material. It adds to
CLD-P05-AMEND-0001, which stays in force. The files under `files/` come from commit
`@SOURCE_COMMIT@` and replace earlier copies of the same paths.

The owner asked for an automatic research circuit run by the proposer and the verifier while
the GPT challenger is at its usage limit, based on your `AUTO-RESEARCH-REQUIREMENTS.md` and the
verifier's gap analysis, and for constraints that block that circuit to be removed.

## Changed rules

1. **Rounds without a challenger** (`docs/AUTO-ROUND.md`). When no challenger release reaches
   the verifier, it reviews your release directly. You then receive a `verification` delivery:
   the verifier's release alone, with no challenger material. Respond to its verdicts exactly as
   you would to a `verified-challenge` delivery. Promotion and joint abandonment still need the
   challenger's own consent.
2. **Bootstrap; this replaces the freeze ban in owner decision 3** (`docs/AUTO-ROUND.md`,
   "Bootstrap"; answers your OD-02). Freeze R1b now, unchanged: your allowlisted round-1b files
   as they stand, with no self-initiated reading added. Then send it. All three roles then refer
   to one release ID. Self-initiated reading stays allowed, labelled as such, and goes into your
   next response, not into this release.
3. **Waiting.** `wait` now always takes `--seen-file`, and a missing file means nothing has been
   handled yet. The `--after` cursor is gone. Start a new background wait with this bundle's
   transmitter, which accepts `verification` deliveries. The wait started under
   CLD-P05-AMEND-0001 is harmless: it cannot return such a delivery and ends at its timeout. Do
   not restart that old wait.
4. **Validator** (your OD-05 and N-04). `files/scripts/project.py` runs offline:
   `digest <DOSSIER-DIR>` and `tasklist-digest <tasklist.md>`. Over your 13 R1b files plus the
   317-byte scaffold `challenges.md`, it gives the digest the coordinator confirmed,
   `291fb88515607ee0ac7a3c53c30ed9d84411b1274a222694a9c44d2a841db012`. Full `validate` stays on the
   coordinator side. The dossier templates are under `files/templates/topic/`.
5. **Experiment consent** (OD-06; your C-01 suggestion). `signed_revision` is the `SUB-` ID of the
   proposer release whose `tasklist.md` both roles accept, and `tasklist_sha256` is that file's
   `tasklist-digest`. An `agree` consent without both is rejected at freeze.
6. **Joint abandonment** (OD-08; your C-06 suggestion). You and the challenger may each release
   your own `abandonment-consent.json` with `session_id`, `decision` (`agree`, `decline` or
   `pending`), `grounds` (from `novelty_exhausted`, `theoretical_headroom_exhausted`, `dead_end`,
   `no_anchor_preserving_direction`), `signed_revision`, `signed_dossier_digest` and `rationale`.
7. **Assignments.** `domains/D05/brief.json` and its README now name the challenger
   `Codex-C05-TIMING-R2` and the verifier `DeepSeek-V02-PHYSICAL`, matching
   `config/launch-release.json`.
8. **Publication.** When a verifier delivery reaches you, the round is finished, and the
   coordinator's publisher pushes its frozen releases to GitHub as one PR. You need no GitHub
   access.
9. **Testing** (`docs/ISOLATION.md`). Synthetic tests use fresh sessions on throwaway fixtures,
   never a live role session.

## Still open with the owner; none blocks the circuit

- **OD-01:** the written reason for the round-1b exception.
- **OD-03, OD-04:** the PDF route and paywalled copies.
- **OD-09:** a distinct reviewer account for final promotion.
- **OD-10, OD-11:** runner allocation, the bison ruling, and binding by procedure versus P&R
  preparation.
- **OD-12:** an appeal adjudicator and arbitration after three rounds.
- **OD-13:** publication of run manifests. Until decided, summarize provenance in
  `search-log.md` and `responses.md`.
- **OD-16:** the open pilot questions.

## Commands

- `<BUNDLE>` is
  `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/Claude-P05-TIMING/COORDINATOR-AMENDMENT-0002`.
- `<INBOX>` is `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/Claude-P05-TIMING`.
- `<OUTBOX>` is
  `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING`.
- `<PACKET-SHA>` is the SHA-256 of `<BUNDLE>/AMENDMENT.json`. From now on, every release you
  freeze uses `--ref @SOURCE_COMMIT@ --packet <PACKET-SHA>`; the coordinator registers this
  pair.

```sh
python3 -I <BUNDLE>/files/scripts/role_submission.py freeze --source <OUTBOX>/release \
  --queue <OUTBOX>/submissions --role proposer --actor Claude-P05-TIMING \
  --session 76d0bf61-78f7-4b93-a557-7c29f1a2cbe8 --topic EDA-0002 \
  --ref @SOURCE_COMMIT@ --packet <PACKET-SHA>
python3 -I <BUNDLE>/files/scripts/round_transmit.py send \
  --config <BUNDLE>/files/config/round-transport.json --release <OUTBOX>/submissions/SUB-<hash>
python3 -I <BUNDLE>/files/scripts/round_transmit.py wait \
  --config <BUNDLE>/files/config/round-transport.json --inbox <INBOX> \
  --seen-file <OUTBOX>/processed-deliveries.json --timeout 86400
python3 -I <BUNDLE>/files/scripts/round_transmit.py ack \
  --seen-file <OUTBOX>/processed-deliveries.json --delivery <DLV ID>
```

Run the wait as a background Bash command, so that the session wakes when it ends.

## Receipt, then work

1. Write `<OUTBOX>/receipts/CLD-P05-AMEND-0002-receipt.json` with these keys:
   - `amendment_id`, `session_id` and `amendment_sha256`.
   - `files_verified` and `recorded_at_utc`.
   - `rules_acknowledged`: one entry per numbered rule.
   - `runtime_checks`: whether `project.py digest` reproduced `291fb885…`.
   - `bootstrap`: the R1b release ID and the delivery IDs reported by `send`.
   - `conflicts_or_questions`.
2. Then carry out rule 2, start the new background wait (rule 3), and end the turn.
3. From then on, handle each valid delivery as your harness and B-04 describe. After each
   delivery: freeze, send, `ack`, and wait again.
