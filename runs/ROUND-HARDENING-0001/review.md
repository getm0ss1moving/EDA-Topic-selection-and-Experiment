# Round transport hardening review

Base: Claude amendment commit 95322c5 (PR #28). Coordinator infrastructure review;
no scientific adjudication or role independence claim.

Fixed in this revision:
- Explicit built-in Read denials for other inboxes and own-inbox write denials,
  supplementing existing Bash filesystem rules without removing sender writes.
- Reject symlink delivery routes and folders, traversal/duplicate release IDs
  before opening payloads, and mismatched actor/session/descriptors.
- Invalid deliveries cannot wake a research consumer. Receipt-set cursors prevent
  same-second/lower-sorting deliveries from being skipped. Wait deadlines cap the
  final sleep. A real subprocess waiting for a synthetic atomic delivery is tested.

Validation before synthetic runtime test: 66 unit tests and project validation
passed. No live role private content was inspected. A single fresh synthetic
Claude isolation test is used; its JSON result is authoritative, not this prose.

Remaining: unknown online copies cannot be recognized by a repository keyword
hook. Shared-account protection is accidental-exposure protection. A returning
wait process does not establish Claude background turn wake-up. No production
session was resumed and no existing frozen policy bundle was modified. New code
must be delivered as a new hashed amendment and acknowledged before deployment;
launcher settings hash is updated in source only.

## First runtime result and repair

`isolation-smoke.json` is a failed full smoke, not a pass. Inbox read/write
protection and all canary checks passed. B16 transmission failed; five guard
probes were never attempted by the synthetic model, so guard runtime coverage is
incomplete. The installed guard did record one blocked call.

The sender-side symlink precheck conflicted with write-only destination grants:
metadata inspection itself requires a read. Removed that precheck at the sender;
coordinator-provisioned destinations remain trusted and receiver-side symlink
rejection remains enforced. A regression test prohibits sender metadata reads.
Added deterministic hook tests for direct, mirror and encoded known-project
requests, external reading and the explicitly uncovered renamed-mirror case.
All 70 unit tests pass. A second, sequential fresh synthetic smoke validates the
repair; no two test-role sessions ran concurrently.

## Runtime diagnosis and verified correction

The second full smoke also failed B16 and the same five unattempted guard probes;
its JSON is retained. A subsequent single-command synthetic diagnostic exposed
`Operation not permitted` at the destination `.pending-*` directory. The broad
foreign-inbox Write/Edit denials also blocked the intentional Bash write grant.
Removing those conflicting denials, while retaining explicit foreign Read denials
and own-inbox Write/Edit denials, allowed the same synthetic send to return two
`delivered` outcomes. Receiver-side validation confirms both packets are valid;
see `transport-diagnostic.json`. Sender metadata prechecks remain removed to
preserve write-only semantics.

Final validation: 70 unit tests and project validation passed. Both full smokes
remain FAILED records because they used the intermediate conflicting settings
and the model skipped guard probes. The targeted corrected-runtime transport
passed; it does not replace a future full deployment smoke. No real scientific
round or Claude automatic model-turn wake-up is claimed. Production launcher and
amendment installation remain gated on a complete deployment test.
