# DeepSeek verifier launch readiness: DeepSeek-V02-PHYSICAL (EDA-0002 / D05)

Run `DSK-V02-LAUNCH-0001` prepares the DeepSeek verifier launch for the frozen EDA-0002 revision and its transported round-1 challenge. It creates no session by itself: the operator starts it from their own Terminal.app with one command. Coordinator: DeepSeek platform lead, session `04fe4881-0c22-4292-ac03-ab73f00eaf29`, operator `getm0ss1moving`. Packet exported from `main` `27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88` (post-#25, including the self-submission protocol).

## What this verifies

The verifier adjudicates the frozen dossier (`4b666c0` content as transported) and the transported round-1 challenge (`runs/DSK-C05-SESSION-0001`): OBJ-001 (hold-CRPR certificate claim), OBJ-002 (wire-delay `thresholdAdjust`), plus claim-level entailment of decision-critical proposal claims, the eight gates in `templates/topic/verification.md` and the compact `verification.md` + `verification.json` output. An external automated review (recorded in `runs/DSK-C05-SESSION-0001/external-review-notes.md`) disputes OBJ-001's sign; adjudicating OBJ-001 against the pinned sources and the packet's decisive test settles that question as part of normal verification.

**Recorded limitation (owner-directed):** the challenge under adjudication was authored by `DeepSeek-C05-TIMING` — the same platform. The owner assigned DeepSeek as the D04/D05 verifier (PR #24 record), and the verifier session is fresh and did not write the challenge. This is a single-platform adjudication of the DeepSeek challenge and **must not be presented as cross-platform confirmation**; the limitation is recorded here for audit.

## Launch artifacts

| Item | Value |
|---|---|
| Session ID (pre-assigned) | `e6bc9983-e74b-4576-9c1d-3abc95ea3df9` |
| Packet | `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/verifier-release-20261014/DeepSeek-V02-PHYSICAL` |
| Packet SHA-256 | `db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78` (42 files, stage `full`, read-only 0555/0444) |
| Outbox | `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL` (empty, mode 0700) |
| Settings | `runs/DSK-C04C05-LAUNCH-0001/launch-settings-V02.json`, SHA-256 `48e9b241ce4edbda794a394d8b8e493289ff2f9a8e0b4e7639796485997f3d2f` (digest-pinned by the launcher) |
| Launcher | `runs/DSK-C04C05-LAUNCH-0001/launch.sh` (unchanged; per-actor binding read from `actor-launch.json`) |
| Model policy | `--model deepseek-flash`, `--effort low` (verifier tier, `docs/TEAM-DEEPSEEK.md`); host-reported model recorded at onboarding |

## Verifications performed

- **Packet**: 42/42 listed hashes re-verified after export; no extra file, no symlink; withheld check not applicable (stage `full`); `candidates/EDA-0002/forecast.json` present as expected for a verifier at stage `full`; the new protocol files are inside: `docs/SELF-SUBMISSION.md`, `scripts/role_submission.py`, `templates/topic/verification.md`; only `harness/VERIFIER.md` is present among role harnesses; `ASSIGNMENT.json` shows role `verifier`, stage `full`, model `deepseek-flash`, effort `low`, outbox path as above.
- **Isolation smoke**: `isolation-smoke-v02-readonly.json` — all 19 environment checks and all 26 step checks pass against the final digest-pinned settings: DeepSeek-only billing, `apiKeyHelper` auth with no `claude.ai` fallback, key unreachable from Bash, read-only packet unmodified, outbox writes only, deny rules cover the challenger and proposer trees.
- **Launcher preconditions**: `launch.sh --actor DeepSeek-V02-PHYSICAL --check` → all in order (CLI hash, settings digest, Keychain auth, packet digest and full file verification, empty 0700 outbox) → exit 0, nothing launched. Launch-record commit: `27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88`.

## Launch sequence

1. From the operator's own Terminal.app:
   `bash runs/DSK-C04C05-LAUNCH-0001/launch.sh --actor DeepSeek-V02-PHYSICAL --check`
   then the same command without `--check`.
2. Send the onboarding prompt below verbatim. The session writes `readiness.json` and `first-pass-plan.md` and stops.
3. The coordinator registers the session in `config/roles.json` (with output digests) and releases the research prompt below.
4. The verifier adjudicates, writes the compact `verification.md` + `verification.json`, and **self-freezes** per `docs/SELF-SUBMISSION.md` (assembles `release/` with exactly those two files; runs the packet's `scripts/role_submission.py freeze` into its own outbox queue).
5. The coordinator transports the frozen release with `scripts/role_submission.py publish`, attaches the PR, waits for checks and merges.

Onboarding prompt:

> You are `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`), the DeepSeek verifier for EDA-0002 (D05). Your only project input is the frozen packet in your working directory, identified by the SHA-256 of its `PACKET.json`: `db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78`. Read `AGENTS.md`, `ASSIGNMENT.json`, `PACKET.json`, the common policy and only `harness/ONBOARDING.md` and `harness/VERIFIER.md`. Use English. Verify every listed file hash. Record actor ID, actual model ID, role, topic, input commit, packet hash, the isolation controls you can observe and any unlisted context in `readiness.json` and `first-pass-plan.md` in your outbox `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL`. Write only to that outbox. Do not begin source adjudication in this turn. Do not inspect another actor's files, converse with another role, approve or merge. Finish the turn after writing both files.

Research prompt (to send verbatim after the registration merges):

> You are `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`), the verifier for EDA-0002 (D05), session `e6bc9983-e74b-4576-9c1d-3abc95ea3df9`. Your only project input is the frozen packet in your working directory, `PACKET.json` SHA-256 `db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78` (stage `full`). Read the common policy — including `docs/SELF-SUBMISSION.md`, `docs/EVIDENCE.md`, `docs/ISOLATION.md`, `templates/topic/verification.md` and the updated `harness/VERIFIER.md` — and use English. Reopen the original sources behind every decision-critical claim and objection in the released dossier and challenge; adjudicate OBJ-001 and OBJ-002 and any decision-critical claim-level entailment issues against versions and exact locators (`valid`, `partially_valid`, `unsupported`, `refuted` or `unresolved`). You have standing permission to read accessible external sources; unavailable evidence stays `unresolved`, never absent. Produce the compact `verification.md` (identity/input table, one row per decision-critical claim/objection with source ID, locator, verdict, whether it blocks advancement, and a short reason/action; then the eight-gate table) and the machine-readable `verification.json` consistent with it, in your outbox. Then self-freeze and submit per `docs/SELF-SUBMISSION.md`: assemble `release/` containing exactly `verification.md` and `verification.json`, and run `python3 <packet>/scripts/role_submission.py freeze --source <outbox>/release --queue <outbox>/submissions --role verifier --actor DeepSeek-V02-PHYSICAL --session e6bc9983-e74b-4576-9c1d-3abc95ea3df9 --topic EDA-0002 --ref 27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88 --packet db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78`. Record the release path in a status note in your outbox. `experiment_authorization` is false: make no tool runs and no experiments. Do not inspect another actor's material, do not sign for another actor, do not approve or merge your own work.
>
> Coordinator answers (administrative): the files `docs/EXPERIMENTS.md`, `docs/FORMATS.md`, `docs/GITHUB.md`, `docs/PHYSICAL-PILOT.md`, `docs/SELF-SUBMISSION.md`, `templates/run.json`, `templates/topic/verification.md`, `config/physical-resources.lock.json` and `scripts/role_submission.py` are part of the common input set this packet was exported with and may be read. `scripts/project.py validate` is deliberately absent from packets; the coordinator runs validation and transport. You are registered in `config/roles.json` as the EDA-0002 verifier; the frozen revision under review is `27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88` and the challenge under adjudication was transported in `runs/DSK-C05-SESSION-0001`.

## Not authorized by this record

No topic, novelty, feasibility or experiment claim; no approval of any proposal or objection. The record prepares a launch; the verdict belongs to the verifier session alone.
