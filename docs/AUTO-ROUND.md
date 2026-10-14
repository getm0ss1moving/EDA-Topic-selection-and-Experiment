# Auto round transport

Owner directives, 2026-10-14: roles exchange a round's releases through local inboxes,
without updating GitHub during the round. The releasing role starts the transmitter itself.
A proposer sees challenger output only together with the verifier's adjudication
(`docs/ISOLATION.md`, "Verified-only challenger release to proposers").

## Inboxes

Each role of a topic has one inbox, listed in `config/round-transport.json`. The inbox has one
`from-<role>` folder for each role allowed to deliver to it:

| Inbox of | Folders | Written by |
|---|---|---|
| Proposer | `from-verifier` | verifier |
| Challenger | `from-proposer`, `from-verifier` | proposer, verifier |
| Verifier | `from-proposer`, `from-challenger` | proposer, challenger |

The proposer inbox has no challenger folder. Each platform coordinator configures its role's
sandbox to read only that role's own inbox and to write only the role's own `from-<role>`
folders in the inboxes it delivers to. An inbox is never writable by its owner. The coordinator
creates the folders and may place `COORDINATOR-*` notices at an inbox root.

## Round procedure

1. Freeze the completed release with `scripts/role_submission.py freeze`
   (`docs/SELF-SUBMISSION.md`).
2. Transmit it:
   `python3 round_transmit.py send --config round-transport.json --release <OUTBOX>/submissions/SUB-<hash>`.
   The verifier adds `--reviews SUB-<proposer release>` for the proposer release it checked and
   `--adjudicates SUB-<challenger release> ...` for every challenger release it ruled on, and
   names the same IDs in `verification.md` or `verification.json`. It rules on every objection
   in each challenger release it includes, if only as `unresolved`.
3. Wait for your next delivery as a background command, so waiting costs no model turns:
   `python3 round_transmit.py wait --config round-transport.json --inbox <YOUR INBOX> --seen-file <OUTBOX>/processed-deliveries.json --timeout 86400`.
   The CLI wakes the session when the command ends. Only valid deliveries end the wait; `check`
   lists invalid ones, which you never open. Name the delivery IDs you used in your next
   release's own provenance text.
4. After handling a delivery, record it so no later wait returns it again:
   `python3 round_transmit.py ack --seen-file <OUTBOX>/processed-deliveries.json --delivery <DLV ID>`.

Routing is fixed in `scripts/round_transmit.py`. The proposer's release goes to the challenger
and the verifier, and the challenger's release goes to the verifier only. The verifier's
release goes to the proposer together with the challenger releases it adjudicated, as one
`verified-challenge` delivery, or alone as a `verification` delivery when no challenger release
reached it this round; the challenger receives the verifier release alone.
While `challenger_stage` is `initial`, the challenger copy of a proposer release is held: the
coordinator performs the semantic forecast screen and delivers a redacted packet.

Each delivery is an immutable `DLV-<UTC>-<sender>-<release prefix>` folder holding exact copies
of the frozen releases and a `DELIVERY.json` record. The receiver re-verifies every byte, the
route and the configured identities. The sender's `transmissions.jsonl`, in its own outbox,
makes a repeated send a no-op.

## Rounds without a challenger

If no challenger release reaches the verifier, for example while the challenger seat is vacant
or its platform has reached a usage limit, the verifier reviews the proposer release directly
and sends without `--adjudicates`. The proposer then receives a `verification` delivery that
holds only the verifier release and carries no challenger material. The round completes and is
published as usual, and a later challenger release joins the next round. Promotion and joint
abandonment still need the challenger's own consent, so a topic cannot close without one.

## Bootstrap

A role whose current output never passed through the inboxes freezes it unchanged and sends it
before its first wait, so every role refers to the same release ID. A verifier ruling made on a
packet dossier, before any proposer release reached its inbox, may be frozen and sent without
`--reviews`; the publisher records that round without a proposer release.

## Consents and validation

- **Experiment consent:** `signed_revision` is the `SUB-` ID of the proposer release whose
  `tasklist.md` both roles accept, and `tasklist_sha256` is that file's digest
  (`project.py tasklist-digest`). Any task-list change creates a new release and resets both
  consents.
- **Joint abandonment:** each role releases its own `abandonment-consent.json` with
  `session_id`, `decision` (`agree`, `decline` or `pending`), `grounds`, `signed_revision`,
  `signed_dossier_digest` and `rationale`, signing the same release and its dossier digest
  (`project.py digest`). The coordinator copies both unchanged into `direction-control.json`,
  and the verifier checks them.
- **Validation:** role bundles include `scripts/project.py` and the topic templates, so each role
  computes the project's own digests offline. Full `validate` runs on the coordinator side.

## GitHub

Nothing is pushed during a round. A round is finished and frozen once the verifier's valid
`verified-challenge` delivery has reached the proposer. The coordinator's publisher then pushes
it, so roles need no GitHub credentials:

```sh
python3 scripts/round_publish.py watch --repo /path/to/checkout
```

Run it in Terminal.app with the coordinator's GitHub CLI login. For every completed round, it
opens one intermediate PR on branch `round/<topic>-<UTC>`. The PR holds the proposer release
the verifier last received before its ruling, the adjudicated challenger releases and the
verifier release, byte for byte under `runs/SUB-<hash>/`, plus `runs/ROUND-<topic>-<UTC>/round.json`
naming every delivery. A round whose sessions are not registered on main with the same input
pair is held and retried. `scan` lists rounds; `publish ROUND-ID --dry-run` builds and validates
the commit without pushing. The publisher never force-pushes or merges; the coordinator merges
after checks pass (`docs/WORKFLOW.md`). Within a round, a release ID, not a Git commit,
identifies what a role received. Final reports keep their human approval.

`runs/ROUND-CIRCUIT-0001/circuit_test.py` runs the whole proposer-challenger-verifier-proposer
circuit with three live sandboxed sessions and a publication dry run.

## Limits

All roles share one OS account. Sandbox write and read grants are the boundary; delivery checks
catch misrouting and accidents, not a malicious actor. The transmitter runs only when a role
starts it; the publisher is the only long-running process and acts after rounds, outside every
sandbox. A role's runtime must allow background commands for inbox waiting; otherwise its
operator resumes it when a delivery arrives.

## Reliable waiting and remaining runtime boundary

`wait` always takes the role's receipt file, `--seen-file <OWN_OUTBOX>/processed-deliveries.json`;
a missing file means nothing has been handled yet. Record each delivery with `ack`
only after processing its valid frozen packet. Never write receipts into an inbox. On a restart, pass the same receipt file: an
unacknowledged delivery is replayed rather than lost. If a turn fails between
output freeze and acknowledgement, use the immutable release ID to avoid a second
scientific revision. Each new wait reloads receipts; run at most one consumer per
role. Invalid deliveries do not wake research and remain visible through `check`.

The wait process returning is not proof that an LLM session wakes. A successful
Python delivery/wait test establishes transport only. Until the destination
runtime has acknowledged a real delivery, label model wake-up unverified. A
stopped CLI cannot be revived by its own background child. Resume the registered
session from its reviewed launcher when necessary, preserving its inbox and
receipt file; never launch a second session or blindly type into an active one.
A platform leader should record the delivery ID and role-authored receipt before
reporting successful end-to-end wake-up.

## Guard boundary

Explicit tool-level denials complement the existing home-denying Bash sandbox:
other roles' inboxes have explicit Read denials;
the own inbox cannot be edited/written. The transmitter's narrowly scoped Bash
write grants remain available. Keep these layers separate when testing.

A repository/account keyword guard cannot identify an arbitrary renamed public
copy. More keywords cannot close that gap. Readonly files under a shared OS user
also cannot authenticate a malicious sender. Strong isolation requires separate
OS users/VMs or containers, coordinator-controlled delivery and credentials, and
no shared writable policy. Even that does not eliminate unknown online copies
while unrestricted external reading is allowed. Therefore keep unadjudicated
material out of publicly indexed channels when confidentiality is required;
historical publication cannot be undone by an access-rule edit. Accidental
exposure must be recorded and scientific independence reassessed. Do not claim
these transport checks provide adversarial isolation.

Do not add broad foreign-inbox Write/Edit denial patterns on top of the scoped
Bash `allowWrite` grants: runtime testing showed those patterns also blocked the
transmitter's `.pending-*` creation. Keep explicit Read denial, own-inbox write
denial, outside-working-directory file-tool controls and narrowly provisioned
sender write grants. Test actual transmission whenever changing these layers.
