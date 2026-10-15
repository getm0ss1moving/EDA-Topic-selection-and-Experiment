# Author check of the DeepSeek transport of the EDA-0002 round-0 dossier (PR #13)

| Field | Value |
|---|---|
| Checked by | `Claude-P05-TIMING`, content author of the transported files (proposer session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`), run `CLD-P05-ADDENDUM-0001` |
| Requested by | The human owner, asking the author to confirm DeepSeek's upload or propose changes |
| Repository | `getm0ss1moving/EDA-Topic-selection-and-Experiment` (public), read through the GitHub REST API and `raw.githubusercontent.com` |
| PR | #13 "Transport the Claude-P05-TIMING round-0 dossier for EDA-0002": head `9d5bd30e30238f611e30ad21f094db1e4df98b43`, base `21d6f7156709e45e430276fd82c3612328cca2bc`, merge commit `4b666c04b0eaa089934f736fab4db2309ce7d36a`, merged 2026-10-13T09:29:33Z |
| `main` at check time | `ed52e1ba693a23e4a3703ce774dfa1c5658271c0` |
| Checked at | 2026-10-13, about 10:38-10:40Z (true UTC) |

This is a transport-fidelity check by the author. It is not a scientific review, an approval or a confirmation. Nothing was pushed, commented on, reviewed or merged.

## Result

**DeepSeek's transport is correct. No change to the repository is requested.**

| # | Check | Outcome |
|---|---|---|
| T1 | Changed paths | 15 files: the 13 authored `candidates/EDA-0002/` files (modified over the scaffold) plus `runs/CLD-P05-RESEARCH-0001/manifest.json` and `runs/DSK-TRANSPORT-CLD-P05-0001/manifest.json` (added). No other paths. The host artifact `.claude/.cc-writes/` was not transported. |
| T2 | Byte identity, PR head | All 14 authored files match the outbox SHA-256 values (table below). |
| T3 | Byte identity, current `main` | The same 14 files are still identical on `main` `ed52e1ba…`; later merges did not alter them. |
| T4 | Transport manifest | Per-file hashes, the source session, run, input commit and packet hash all match the author's records. `source_role_output_manifest_sha256` `ed13d070…` equals the outbox `role-output-manifest.json`. |
| T5 | Dossier digest | Recomputed independently as `8d6bd047232a17a1ba985d156c831e76e3212772667309dffc9cdf1a934ff03b`, equal to the PR body and the transport manifest. The value came from a reimplementation of `digest()` in `scripts/project.py` (read at the head, lines 36-46, not executed), applied to all 16 files of `candidates/EDA-0002/` at the head. As the code specifies, it excludes `verification.json` and `verification.md`. The untouched `challenges.md` scaffold was hashed but not read. |
| T6 | `tasklist.md` digest | `d115fcc69b1b65610311aa0b95554f4fe26bdac8a966f606f30fb6c0ca7efd56` matches. |
| T7 | Checks at the head | `research-structure` succeeded. Two `verifier` check runs failed (09:25:20Z and 09:29:05Z) before the confirming review; the next one succeeded (09:29:19Z). The combined status `independent-verifier` is success. `M0nitor-EDA` reviewed `APPROVED` with body `CONFIRM 9d5bd30e30238f611e30ad21f094db1e4df98b43`. |
| T8 | PR body | Consistent with the files. The `dossier.json` state (`submitted`) and `proposer_session` are reported as the author wrote them. |

| File | SHA-256 (outbox = PR head = `main`) |
|---|---|
| `candidates/EDA-0002/contest-audit.md` | `fb416544b8e99eb61c4b7b6dda913d4a247f48a3352cbad0d16f1468ad4b5fc0` |
| `candidates/EDA-0002/direction-control.json` | `f9ee70159f3fa034a34077bcc9358b0c9fc07686889d47bff34407f4b2b1e50c` |
| `candidates/EDA-0002/dossier.json` | `5c29d0ca629745fdf8115c83027c2b6e23cd4b316f38c15a95561805e3726263` |
| `candidates/EDA-0002/experiment-consensus.json` | `366d7446fedcbc733de465a5de8725242e09a8d50630fefaa855a7dd504442a4` |
| `candidates/EDA-0002/experiment-plan.md` | `441933fab59195d3e5a9a38abe8324bb272b9095d79b269907e2ba4660648eac` |
| `candidates/EDA-0002/forecast.json` | `06d5e1dfc27373a42bd472a264f3df1fcb06a0d30d918430da9844001d06f7e8` |
| `candidates/EDA-0002/industry-gap.md` | `672c821feac7c77d9fbd2c9518552c7512099f8fb8496a675f67799ebc42e455` |
| `candidates/EDA-0002/prior-art.csv` | `ab3672ad4eaf9ff6e85b20dc95307fadd548c132ca2a9252aec71bcacaddbf3c` |
| `candidates/EDA-0002/proposal.md` | `18a2404e48fcb9ef68675d6854306d965b8a4fc2449edc33a3206ff04c12c5db` |
| `candidates/EDA-0002/responses.md` | `3db163c6afe4601470f4e30959e2e04af02e852b558a8ae9e1cd424adb5731e6` |
| `candidates/EDA-0002/search-log.md` | `1b222e874e73d8f6e6fcceba528f99f631e37b2026962b148537c2b46e55e5bd` |
| `candidates/EDA-0002/sources.json` | `4cc83ce23146ec2f867e8f98aca60440d3f22f5801d43ff8b38b207cb4afde57` |
| `candidates/EDA-0002/tasklist.md` | `d115fcc69b1b65610311aa0b95554f4fe26bdac8a966f606f30fb6c0ca7efd56` |
| `runs/CLD-P05-RESEARCH-0001/manifest.json` | `5eeb8b71f9df0486135455e4c4f6bd2cac70bbe7accc78686da9fa2f7201a707` |

## Non-blocking notes for the coordinator

1. **`role-output-manifest.json` is referenced but not in the repository.** The transport manifest records its hash, but the file was neither transported nor listed under `exclusions`, so the hash cannot be verified from the repository. Some author disclosures exist only in that file:
   - the blocked relative `rm` resolved against the packet directory, and the packet re-verification that followed;
   - the re-creation of `readiness.json` between turns;
   - the host working-directory moves;
   - the reasoning-effort observation.

   It contains no absolute local paths. Suggestion: transport it as `runs/CLD-P05-RESEARCH-0001/role-output-manifest.json` with the addendum, or list it under `exclusions` with a reason.
2. **Clock offset.** The transport manifest correctly flags that its own timestamp is about 15 h behind true UTC. The same host-clock offset affects every timestamp the author wrote in round 0. That is the author's erratum E1 (`evidence-addendum.md` § 4), not a transport defect: a verbatim transport must not alter it.
3. **PR checklist wording.** The ticked item "Critical sources checked in versioned files" should be read as "transported verbatim", as its parenthetical says. No source was re-checked in this transport.
4. **Not read by the author:**
   - the `chatgpt-codex-connector[bot]` review on PR #13 (state `COMMENTED` at the head). Only its first line was displayed, as API metadata;
   - every other PR in the repository (#1-#12 and #14-#16), seen by title only.

   GitHub comments are not admissible until copied into a file and checked (`docs/WORKFLOW.md` line 24), and the proposer must not read unreleased challenger material (`docs/ISOLATION.md` access matrix). If the bot review raises objections to the dossier, route them through `challenges.md` and `verification.md`.
