# Exposure and exception record: proposer read unadjudicated challenger output

Recorded on 2026-10-14 by the Claude platform coordinator. On that date the owner chose to keep
PR #26, which transports the proposer's R1b output, together with this record. It is a
contamination and exception record under `docs/ISOLATION.md`, "Contamination response". It
is not a scientific finding and does not count as independent confirmation.

| Item | Record |
|---|---|
| Affected actor | `Claude-P05-TIMING`, session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`, EDA-0002 proposer |
| Exposed material | The EDA-0002 challenger's independent first pass: eight files at commit `b7822234` of branch `codex/challenger-initial-search` |
| Verifier adjudication at exposure | None |
| Route | Owner instruction in round 1b, run `CLD-P05-REVISION-0002`, as disclosed by the proposer in `runs/CLD-P05-FROZEN-0002/role-output-manifest.json`, `input_provenance_events[13]` |
| Earlier browsing | Before that instruction, while looking for challenges, the proposer read PR metadata, the branch list, the unchanged `challenges.md` scaffold on main and the coordinator's challenger-succession `handoff.md`. It reports that it did not open the challenger files until instructed (`input_provenance_events[14]`). |
| Affected output | Frozen R1b output `runs/CLD-P05-FROZEN-0002` in PR #26: `responses.md` CF-01 to CF-14 and the revision recorded in `runs/CLD-P05-REVISION-0002` |
| Decision to continue | The owner kept the session and PR #26 (2026-10-14) instead of starting a clean replacement session |
| Written rationale | Not supplied. The owner was invited to add one on 2026-10-14. `AGENTS.md` requires a written rationale for a human exception, so this gap stays open until the owner records it. |

## Consequences

- CF-01 to CF-14 were written before any verifier adjudication. Under `harness/PROPOSER.md`
  they are self-initiated responses. Objections become established findings only through
  verifier adjudication (`docs/WORKFLOW.md`, step 4), and these early responses do not change
  that.
- The R1b responses cannot be described as independent of the unadjudicated challenge. Later
  adjudication does not undo the exposure, and the exposure authorizes no further reads.
- The owner directive of 2026-10-14 forbids this route from now on (`docs/ISOLATION.md`,
  "Verified-only challenger release to proposers").
- Amendment `CLD-P05-AMEND-0001` adds controls. The proposer's round inbox has no challenger
  folder, so challenger material reaches it only inside verifier deliveries. A guard hook
  blocks the proposer's web and shell calls that name the project repository, which is the
  route used for the earlier browsing.
