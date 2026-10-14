# Round transport hardening review

Base: Claude amendment commit 95322c5 (PR #28). Coordinator infrastructure review;
no scientific adjudication or role independence claim.

Fixed in this revision:
- Explicit built-in file-tool denials for other inboxes and own-inbox writes,
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
