# Amendment AUTO-CIRCUIT-0001 for DeepSeek-V02-PHYSICAL

Issued on 2026-10-14 to `DeepSeek-V02-PHYSICAL`, the EDA-0002 verifier (session
`e6bc9983-e74b-4576-9c1d-3abc95ea3df9`), by the Claude platform coordinator at the owner's
request. It is a transport notice: no scientific content, finding or approval. It adds to
`COORDINATOR-REAL-ROLE-INBOX-0001`, which stays in force. The files under `files/` come from
commit `@SOURCE_COMMIT@` and replace that bundle's copies of the same paths.

It closes the gaps in your `gap-analysis.md`, so that the proposer and you can run rounds
automatically while the GPT challenger is at its usage limit.

## What changed for you

1. **G1 and G2, registration.** `config/roles.json` registers session
   `e6bc9983-e74b-4576-9c1d-3abc95ea3df9` as the EDA-0002 verifier, with input pair
   `27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88` and
   `db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78`. Freeze with exactly that
   identity.
2. **G3, assignments.** `domains/D05/brief.json` and its README now name you as the verifier and
   `Codex-C05-TIMING-R2` as the challenger, matching `config/launch-release.json`.
3. **G4, digest.** `files/scripts/project.py digest <DOSSIER-DIR>` computes `dossier_digest` for
   the dossier you adjudicated. It runs offline; full `validate` stays on the coordinator side.
4. **G6, the GPT challenge.** The GPT challenger's frozen round-1b review,
   `SUB-e81a3116230c993ef314885730e0e5202a2bbfeab70328f5bfcc8b35c0511c7f`, is in your inbox under
   `from-challenger`. The coordinator delivered it because that challenger has reached its usage
   limit. The proposer's frozen R1b release arrives under `from-proposer` once the proposer
   freezes it.
5. **Naming what you checked** (`harness/VERIFIER.md`, `docs/AUTO-ROUND.md`). Pass
   `--reviews <proposer release ID>` for the proposer release you checked, and
   `--adjudicates <challenger release IDs>` for every challenger release you ruled on. Name the
   same IDs in `verification.md` or `verification.json`. Rule on every objection in each
   included challenger release, if only as `unresolved`, because only adjudicated material may
   reach the proposer.
6. **Rounds without a challenger.** When only a proposer release arrives, review it directly and
   send with `--reviews` alone. The proposer receives your release with no challenger material.
7. **Waiting.** `wait` always takes `--seen-file`; a missing file means nothing has been handled
   yet. The `--after` cursor is gone.

## Procedure

1. Verify `AMENDMENT.json`. Then write `<OUTBOX>/receipts/AUTO-CIRCUIT-0001-receipt.json` with
   `amendment_id`, `session_id`, `amendment_sha256`, `files_verified`, `recorded_at_utc`,
   `rules_acknowledged` and `conflicts_or_questions`.
2. **Bootstrap round.** Your completed ruling on the round-0 dossier and the DeepSeek round-1
   challenge sits in `<OUTBOX>/release/`.
   - Set its `dossier_digest` with `project.py digest` over the dossier you adjudicated.
   - Freeze it with the registered identity.
   - Send it with neither `--reviews` nor `--adjudicates`. The proposer receives your verdicts as
     a `verification` delivery, without the challenger's raw files.
   - Keep this ruling separate from the round-1b work: the round-0 packet's content does not
     carry over to the GPT challenge.
3. Start the background wait. When the proposer's R1b release and the GPT challenge are both in
   your inbox, adjudicate the challenge against R1b, freeze, and send with
   `--reviews <R1b release ID> --adjudicates SUB-e81a3116…`.
4. After that, for each new proposer release, review it together with any challenger releases
   that arrived, then freeze and send. Acknowledge each delivery after you have processed it, and
   wait again. Never claim acceptance or authorize experiments.

## Commands

- `<BUNDLE>` is
  `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/DeepSeek-V02-PHYSICAL/COORDINATOR-AUTO-CIRCUIT-0001`.
- `<INBOX>` is `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/DeepSeek-V02-PHYSICAL`.
- `<OUTBOX>` is
  `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL`.

```sh
python3 -I <BUNDLE>/files/scripts/role_submission.py freeze --source <OUTBOX>/release \
  --queue <OUTBOX>/submissions --role verifier --actor DeepSeek-V02-PHYSICAL \
  --session e6bc9983-e74b-4576-9c1d-3abc95ea3df9 --topic EDA-0002 \
  --ref 27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88 \
  --packet db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78
python3 -I <BUNDLE>/files/scripts/round_transmit.py send \
  --config <BUNDLE>/files/config/round-transport.json --release <OUTBOX>/submissions/SUB-<hash> \
  [--reviews SUB-<proposer release>] [--adjudicates SUB-<challenger release> ...]
python3 -I <BUNDLE>/files/scripts/round_transmit.py wait \
  --config <BUNDLE>/files/config/round-transport.json --inbox <INBOX> \
  --seen-file <OUTBOX>/processed-deliveries.json --timeout 86400
python3 -I <BUNDLE>/files/scripts/round_transmit.py ack \
  --seen-file <OUTBOX>/processed-deliveries.json --delivery <DLV ID>
```

Run the wait as a background Bash command, so that the session wakes when it ends.
