# Actor-owned submission and freeze

Scope: owner-requested proposer, challenger and verifier self-freeze and
submission; compact verifier presentation. Coordinator-authored infrastructure, not independent
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

## Review by the Claude platform coordinator (2026-10-14)

The owner asked the Claude coordinator to check and fix this PR. Defects found and fixed:

- **Gate regression.** The compact `verification.md` template used `Pending` placeholders. `scripts/project.py` rejects unfilled review files only by matching `TBD`, so an untouched template could pass the verified/accepted check. The template uses `TBD` again; a new test proves that an untouched template blocks acceptance.
- **Unattended publication.** `publish` pushed actor text to a public repository with no content screening. Freeze and publish now reject credential-like strings, non-UTF-8 text and malformed JSON.
- **Brittle freeze.** A macOS `.DS_Store` or Claude Code's `.claude` staging folder inside a release directory made freeze fail with an unnamed error. These two host artifacts are now ignored, and errors name the missing, extra or irregular files.
- **Consent gap.** Neither role could submit a task-list consent, which blocked automatic experiment consensus. Proposers and challengers may now release an `experiment-consent.json` that signs only for the releasing session; the coordinator copies it unchanged.
- **Malformed manifests** raised `TypeError` instead of `ValueError`, so they escaped verify's rejection path.
- **Platform attribution.** Every submission branch used a `codex/` prefix. It is now the platform-neutral `submit/`.
- **Consistency.** `SELF-SUBMISSION.md` and this record covered only the proposer and challenger, while the verifier harness and allowlist include the verifier. Both now cover all three roles, and `docs/WORKFLOW.md` says how the verifier freezes and how consents travel.

Validation after the fixes: project validation and all 50 tests pass, including 6 new tests. Still not exercised: a real GitHub publication, and the runtime amendments existing sessions need, such as the Claude proposer's GitHub/arXiv-only reading settings.
