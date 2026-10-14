# DeepSeek role succession: challengers out, verifier in (D04 + D05)

Run `DSK-ROLE-SUCCESSION-0001` executes the human owner's directive of 2026-10-13 (true UTC; 2026-10-14 local host date): the DeepSeek platform stops serving as challenger and serves as the project's verification platform for both queues. Coordinator: DeepSeek platform lead, session `04fe4881-0c22-4292-ac03-ab73f00eaf29`, operator `getm0ss1moving`. Base: `main` `22002d2`.

## What changes

| File | Change |
|---|---|
| `config/launch-release.json` | New matrix: `EDA-0001` challenger → `Codex-C04-PHYSICAL-R2`, verifiers for both topics → `DeepSeek-V02-PHYSICAL`; released set reduced to five actors; `role_handoffs` replaces `challenger_handoffs` with four owner-authorized records (both challenger handoffs and both verifier handoffs); `platform_readiness` roles updated; DeepSeek's readiness now carries a verifier model policy (`deepseek-flash` at low effort). |
| `config/agents-deepseek.json` | Top-level activation: `succession_directive` added; `released_actors` → `[DeepSeek-V02-PHYSICAL]`. `DeepSeek-C04-PHYSICAL` (never ran) and `DeepSeek-C05-TIMING` (completed onboarding and a full round-1 challenge; record transported in `runs/DSK-C05-SESSION-0001`) are marked `handed_off_by_succession` with successor pointers. `DeepSeek-V02-PHYSICAL` is released (`status` restored to `ready_for_fresh_session`, `active_scope` true, `fresh_session_required` true, `domain_ids` trimmed to D04/D05, verifier session-state note). `DeepSeek-V03-SYSTEMS` gains D06. |
| `config/agents.json` | `Codex-C04-PHYSICAL-R2` (`CDX-Skeptic-PHYSICAL`, `gpt-6-astra` at low effort, predecessor `DeepSeek-C04-PHYSICAL`, no inherited context) added on the owner's "Codex successor" choice; released count and scope policy updated. The Codex platform owns this identity's operation. |
| `scripts/project.py` | `validate_launch_release` now validates `role_handoffs` (per-topic, per-role `from`/`to`/`owner_authorized`/`reason` against the recorded succession), derives the five-actor released set and assignment matrix from the verified records, and requires the DeepSeek readiness model policy. |
| `tests/test_project.py` | Fixtures updated to the new matrix; the two succession tests are replaced by three handoff tests (owner record required; wrong successor rejected; registered successors accepted). 38 tests pass. |
| `domains/D06/brief.json` | DeepSeek verifier binding moved from V02 to `DeepSeek-V03-SYSTEMS` (`DSK-Ledger-SYSTEMS`), executing the standing instruction to remove D06 from V02's future assignment. |
| `docs/TEAM-DEEPSEEK.md` | D06 roster row updated; dated status update recording the succession. |

## What does not change

No scientific content, dossier, session record or experiment state is touched. No session is created: `DeepSeek-V02-PHYSICAL`'s session is gated by `config/launch-release.json` `research_sequence` on a frozen proposal plus released challenge material, and its packet will be exported from the then-current `main` commit when the verification stage arrives. The round-1 challenge already transported under `runs/DSK-C05-SESSION-0001` (PR #23) remains provisional; adjudication stays with the future verifier session, which will read only the released materials, never the retired challenger's private outbox beyond what was transported.

## Coordination note

This run and the challenge transport (`runs/DSK-C05-SESSION-0001`, PR #23) both touch the `DeepSeek-C05-TIMING` registry entry; whichever merges second is rebased so both records land intact. The succession is self-consistent on `main` `22002d2` without the transport.

## Validation

`python3 scripts/project.py validate` → structural checks passed. `python3 -m unittest discover -s tests` → 38 tests OK.

## Not authorized by this record

No topic, novelty, feasibility or experiment claim. The verifier release authorizes verification work when its packet is released; it approves no proposal and adjudicates no objection yet.
