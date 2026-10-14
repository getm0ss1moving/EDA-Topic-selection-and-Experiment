# Actor-owned submission and freeze

Scope: owner-requested proposer/challenger self-freeze and submission; compact
verifier presentation. Coordinator-authored infrastructure, not independent
scientific verification.

Decisions:
- Replace the owner/coordinator freeze permission with actor-owned immutable
  releases. Keep a separate transport Git commit and scientific admission gates.
- No broad GitHub credentials or repository access in role sessions. The transport
  command verifies registry identity and packet provenance and opens a PR from an
  isolated temporary clone, preserving role outputs under a content-addressed run.
- Compact verifier tables retain source locators, uncertainty, blocking status,
  eight gates and matching machine-readable verdict. No long essay requirement.
- Existing actor packets are not silently changed. New exports include the new
  procedure/tool. Existing sessions need a hashed policy amendment before use.

Validation: 44 unit tests and repository structural validation passed before
submission. Added seven local freeze tests for roundtrip/revision/idempotence,
content tamper, forbidden ownership, symlinks, missing files, size cap and extra
snapshot entries. No scientific actor was launched for these tests.

Limits: no continuously running queue watcher was installed; GitHub publication
of a real actor release has not been exercised in this change. Readonly bits are
not adversarial isolation. Semantic forecast masking and evidence adjudication
remain explicit coordinator/verifier duties. Actor output transport is not an
accepted topic or experiment authorization. No verifier was invented.

## Owner clarification: independent external reading

All proposers, challengers and verifiers have standing permission to read any
accessible external research source/file without per-file or per-domain approval.
Updated AGENTS, isolation/evidence policy and all role harnesses. Supersedes the
historical GitHub/arXiv-only research-reading restriction. Cross-role material
remains prohibited unless explicitly released as shared output for the receiver's
stage, regardless of external location. Source quality requirements still govern
claims. Offline compute, execution and budget limits are unchanged.

Validation rerun: project validation and all 44 tests passed. Existing sessions'
live permissions have not been changed; this PR supplies policy, not evidence of
runtime deployment. Historical frozen records remain intact.
