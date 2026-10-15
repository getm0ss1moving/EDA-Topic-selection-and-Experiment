# Policy amendment CLD-P05-AMEND-0001

Issued on 2026-10-14 to `Claude-P05-TIMING`, the EDA-0002 proposer (session
`76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`), by the Claude platform coordinator. It is a
transport notice. It carries no scientific content, finding or approval, and it releases
no other role's material.

- Base packet: commit `d437c2f660906efe9351a90451905826d00b63e3`, `PACKET.json` SHA-256
  `ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d`.
- Amended text: commit `2121532bfca928900f4252e796d7570fdb1ea224` of the repository (its amendment PR). Each file
  under `files/` replaces the packet copy at the same repository path or is new. Every other
  packet file stays in force. `AMENDMENT.json` lists every file's SHA-256; those hashes are
  authoritative even if the PR is squash-merged under another commit. Your frozen packet is
  not edited (`docs/ISOLATION.md`, "Forecast masking and policy amendments").

## Changed rules

1. **External reading.** `AGENTS.md`; `docs/ISOLATION.md`, "Independent external
   reading"; `docs/EVIDENCE.md`, "Decision coverage and objections"; `harness/PROPOSER.md`.
   You may read any accessible external research file or source without per-file,
   per-site or coordinator approval. The GitHub/arXiv-only reading rule, including the
   CLD-LAB-0001 one, no longer applies. Reading never authorizes executing downloaded
   code, experiments, new spending or bypassing authentication. Log inaccessible sources
   and runtime blocks in your search log as access limitations.
2. **Challenger output: verified only.** Owner directive, 2026-10-14: "need proposer can
   not see challenger's output but verified challenger's output"; recorded in
   `docs/ISOLATION.md`, "Verified-only challenger release to proposers". You see challenger
   output only after the verifier has adjudicated it, inside a `verified-challenge`
   delivery that carries the verifier's release. Do not open challenger output by any other
   route: this project's repository `getm0ss1moving/EDA-Topic-selection-and-Experiment`, its
   branches, pull requests, forks or mirrors, or search results that lead there.
   Transported challenger output is public there before adjudication. Material you saw
   earlier stays on record and does not authorize further reads.
3. **Auto round transport.** Owner directive, 2026-10-14; `docs/AUTO-ROUND.md`;
   `config/round-transport.json`; `scripts/round_transmit.py`; `harness/PROPOSER.md`, "Auto
   round transport". Within a round, releases travel between the roles' local inboxes, and
   nothing goes to GitHub until the round ends. After each freeze you run the transmitter
   yourself; it delivers your release to the challenger and the verifier. You then wait for
   your next delivery in the background. When the verifier's ruling reaches you, the round is
   finished, and the coordinator's publisher pushes its frozen releases to GitHub as one PR.
4. **Self-submission and freeze.** `docs/SELF-SUBMISSION.md`; `docs/WORKFLOW.md`, steps 3
   and 6 and "Actor-owned freeze"; `harness/PROPOSER.md`, "Self-submission";
   `scripts/role_submission.py`. When an assigned phase is complete, you freeze your own
   release; no human freeze is needed. You may include your own `experiment-consent.json`,
   which signs only for your session. Freezing is not acceptance and authorizes no
   experiment.
5. **Proposer checklist.** `harness/PROPOSER.md`, "Submission acceptance checklist":
   explicit Coverage, Gap, Contribution, Demand, Headroom, Contests and Delivery sections.
   Only adjudicated objections require a scientific response. Label work done while a
   challenge is pending as self-initiated.
6. **Preparation versus execution.** `docs/EXPERIMENTS.md`. Tool installation, data
   preparation and bounded correctness checks need an explicit scoped allocation and
   cannot be relabelled experiments. Bind task-list dependencies by content or SHA-256.
   Changing a bound dependency resets both consents.
7. **Review scope.** `AGENTS.md`; `docs/CHARTER.md`; `docs/WORKFLOW.md`, "Human review
   scope"; `docs/GITHUB.md`. A human `CONFIRM` is required only for final deliverables
   under `topics/` and `reports/final/`. The coordinator may merge intermediate PRs after
   automated checks pass. Scientific roles never approve or merge.
8. **Assignments.** `config/launch-release.json`, "assignments" and "role_handoffs";
   `config/round-transport.json`. For EDA-0002, the challenger seat passed to
   `Codex-C05-TIMING-R2` and the verifier seat to `DeepSeek-V02-PHYSICAL`. The top-level role
   fields of `domains/D05/brief.json` and its README still name the former seats; the release
   file is authoritative, as the brief's `release_binding` states.
9. **Budget.** `config/research-brief.json`. Nothing changes for you. The prepaid DeepSeek
   allowance applies only to the DeepSeek actors it names.
10. **Policy amendments.** `docs/ISOLATION.md`. Record receipt and hashes before
    continuing, as described under "Receipt" below. `templates/topic/verification.md` is the
    verifier's compact format and is listed for completeness.

## Runtime changes in your session, effective from this resume

- WebFetch reaches any domain; before, it reached GitHub and arXiv only. WebSearch is
  unchanged.
- A coordinator guard blocks WebFetch, WebSearch and Bash calls that name this project's
  repository or its owner accounts. A blocked call returns a message. The guard logs only
  time, tool and the matched name. To write file text that merely mentions these names,
  use the Write tool.
- Bash network access is unchanged: GitHub and arXiv only. If only Bash could fetch a
  source elsewhere, log it as an access limitation.
- Your round inbox `<INBOX>` is readable and never writable by you. It has only a
  `from-verifier` folder. Your sandbox can write, but not read, the `from-proposer` folders of
  the challenger and verifier inboxes, and only the transmitter should write there.
- Safe mode disables hooks, so the guard needs it off. Equivalent switches replace it: no
  automatic CLAUDE.md or AGENTS.md loading, no bundled skills, no auto-update,
  project-only settings, no MCP servers and the same six tools.
- Packet, outbox and lab-results access is unchanged.

## Commands

`<BUNDLE>` is this folder,
`/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/Claude-P05-TIMING/COORDINATOR-AMENDMENT-0001`.
`<INBOX>` is `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/Claude-P05-TIMING`.
`<OUTBOX>` is `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING`.
`<PACKET-SHA>` is the SHA-256 of `<BUNDLE>/AMENDMENT.json`.

Freeze a completed release. Put only completed, allowlisted proposer files in
`<OUTBOX>/release` first:

```sh
python3 <BUNDLE>/files/scripts/role_submission.py freeze \
  --source <OUTBOX>/release --queue <OUTBOX>/submissions \
  --role proposer --actor Claude-P05-TIMING \
  --session 76d0bf61-78f7-4b93-a557-7c29f1a2cbe8 --topic EDA-0002 \
  --ref 2121532bfca928900f4252e796d7570fdb1ea224 --packet <PACKET-SHA>
```

Transmit it to the challenger and the verifier:

```sh
python3 <BUNDLE>/files/scripts/round_transmit.py send \
  --config <BUNDLE>/files/config/round-transport.json \
  --release <OUTBOX>/submissions/SUB-<hash>
```

Wait for your next delivery as a background Bash command; the session wakes when it ends.
Create `<OUTBOX>/processed-deliveries.json` containing `[]` before the first wait:

```sh
python3 <BUNDLE>/files/scripts/round_transmit.py wait \
  --config <BUNDLE>/files/config/round-transport.json --inbox <INBOX> \
  --seen-file <OUTBOX>/processed-deliveries.json --timeout 86400
```

Only valid deliveries end the wait. `round_transmit.py check` lists any invalid ones; never
open those. After handling a delivery, record it so that no later wait returns it again:

```sh
python3 <BUNDLE>/files/scripts/round_transmit.py ack \
  --seen-file <OUTBOX>/processed-deliveries.json --delivery <DLV ID>
```

Name the delivery IDs you used in your next release's provenance text.

## Receipt, required before any further scientific action

Write `<OUTBOX>/receipts/CLD-P05-AMEND-0001-receipt.json` with these keys:

- `amendment_id`: `CLD-P05-AMEND-0001`.
- `session_id`: your session ID.
- `amendment_sha256`: the SHA-256 you computed for `AMENDMENT.json`.
- `files_verified`: `true`, or the list of mismatched, missing or extra paths.
- `recorded_at_utc`: the host clock reading.
- `rules_acknowledged`: one entry per numbered rule above, stating its effect on your
  current work.
- `challenger_material_seen`: each challenger artifact you have seen so far, with its ID or
  path, how you received it, and whether it came with a verifier adjudication.
- `runtime_checks`: whether a WebFetch of one research page outside GitHub and arXiv
  succeeded (name the URL); whether `round_transmit.py check` on `<INBOX>` ran; and
  whether the background wait started.
- `conflicts_or_questions`: anything that conflicts with your current work, or an empty
  list.

Do not freeze a release, revise the dossier or start new research in the acknowledgement
turn. After writing the receipt, start the background wait and end the turn. Your current
R1b output is already with the challenger. Your next scientific input is a valid
`verified-challenge` delivery.
