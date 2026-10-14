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
   The verifier adds `--adjudicates SUB-<challenger release> ...` and must name the same IDs
   in `verification.md` or `verification.json`.
3. Wait for your next delivery as a background command, so waiting costs no model turns:
   `python3 round_transmit.py wait --config round-transport.json --inbox <YOUR INBOX> --after <LAST DLV ID> --timeout 86400`.
   When it returns, open a delivery only if `valid` is true. Never open an invalid delivery or
   a stray entry; report it in your output and wait again. Name the delivery IDs you used in
   your next release's own provenance text.

Routing is fixed in `scripts/round_transmit.py`. The proposer's release goes to the challenger
and the verifier, and the challenger's release goes to the verifier only. The verifier's
release goes to the proposer together with the challenger releases it adjudicated, as one
`verified-challenge` delivery, and to the challenger alone as a `verification` delivery.
While `challenger_stage` is `initial`, the challenger copy of a proposer release is held: the
coordinator performs the semantic forecast screen and delivers a redacted packet.

Each delivery is an immutable `DLV-<UTC>-<sender>-<release prefix>` folder holding exact copies
of the frozen releases and a `DELIVERY.json` record. The receiver re-verifies every byte, the
route and the configured identities. The sender's `transmissions.jsonl`, in its own outbox,
makes a repeated send a no-op.

## GitHub

Nothing is pushed during a round. After the round, the coordinator publishes each frozen
release with `role_submission.py publish`, together with the senders' transmission ledgers,
and merges the intermediate PRs after checks pass (`docs/WORKFLOW.md`). Within a round, a
release ID, not a Git commit, identifies what a role received. Final reports keep their human
approval.

## Limits

All roles share one OS account. Sandbox write and read grants are the boundary; delivery checks
catch misrouting and accidents, not a malicious actor. The transmitter runs only when a role
starts it: there is no daemon. A role's runtime must allow background commands for
inbox waiting; otherwise its operator resumes it when a delivery arrives.

## Reliable waiting and remaining runtime boundary

Prefer `wait --seen-file <OWN_OUTBOX>/processed-deliveries.json` instead of a
lexicographic `--after` cursor. Initialize that file to `[]`, then atomically
append each delivery ID only after processing its valid frozen packet. Never
write receipts into an inbox. On a restart, pass the same receipt file: an
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
