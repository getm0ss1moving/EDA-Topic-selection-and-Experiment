# Handoff: EDA-0002 proposer work, from `Claude-P05-TIMING`

| Field | Value |
|---|---|
| Outgoing actor | `Claude-P05-TIMING` (call sign `CLD-Origin-TIMING`), proposer, session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`, model `claude-opus-5-5` |
| Instruction | Human owner, in chat on 2026-10-15: "conclude your task and claim your project's critical file to let another model to keep on your work" |
| Concluded at | 2026-10-15T04:50Z (host clock, accurate to about 10 s) |
| Run record | `runs/CLD-P05-HANDOFF-0001/manifest.json`, which lists the SHA-256 of every outbox file |
| Dossier digest | `291fb88515607ee0ac7a3c53c30ed9d84411b1274a222694a9c44d2a841db012`. Recomputed at handoff over the 13 files in `candidates/EDA-0002/` plus the repository scaffold `challenges.md` (SHA-256 `8f59fa4f…`), excluding `verification.*`. The coordinator reported the same value for the PR #26 transport |

This file holds facts and file pointers only. It contains no private reasoning. Everything a successor needs is in this outbox, in the frozen packet and in the amendment bundle. My session scratch is **not** part of the handoff: another session must not read it, and nothing in it is needed.

## 1. Before a successor acts (owner and coordinator)

The proposer seat is identity-bound. Unless these steps are done, the successor's freezes, sends and consents will be rejected or will be invalid.

1. **Record the role handoff in writing.** Add it to `config/launch-release.json` → `role_handoffs` → `EDA-0002` → `proposer` (from `Claude-P05-TIMING` to the new actor ID, with the owner's reason), as was done for the challenger and verifier successions. Register the new session in `config/roles.json`. Per `docs/WORKFLOW.md`, session reassignment needs a written event and a fresh session.
2. **Update `config/round-transport.json`.**
   - `topics.EDA-0002.roles.proposer` must name the new `actor_id` and `session_id`.
   - The transmitter checks both on every release and every delivery: `checked_release` in `scripts/round_transmit.py` for sends, and `validate` for deliveries addressed to the proposer.
   - `role_submission.py` lets `experiment-consent.json` sign only for the releasing session.
3. **Start the successor fresh** (`docs/ISOLATION.md`, "Session setup").
   - Give it a new packet, the amendment bundle and read access to this outbox.
   - Do not fork this conversation and do not preload a summary of it.
   - Give it its own outbox, or write access to this one, and its own inbox grants.
4. **Stop this session's background wait first.** `docs/AUTO-ROUND.md` allows at most one consumer per role.
   - My wait (`round_transmit.py wait … --seen-file processed-deliveries.json --timeout 86400`, background task `bi86z6o18`, started 2026-10-14T10:29Z) may still be running.
   - The sandbox blocks `ps` and `pgrep`, so I could not stop it myself. End this Claude Code session, or stop the task from its background-task list, before the successor starts its own wait.
   - The seen-file is still `[]`. No delivery has arrived, and none has been acknowledged.
   - If this session is woken by a delivery after the handoff, I will not process it. I will only note that it arrived.
5. **Keep platform separation.** The challenger is Codex (`Codex-C05-TIMING-R2`) and the verifier is DeepSeek (`DeepSeek-V02-PHYSICAL`). `config/launch-release.json` justifies the verifier seat as "the third platform". A successor proposer from the Codex or DeepSeek platform would collapse that separation, so a Claude-family successor keeps it.
6. **Exposure travels with the dossier.**
   - The round-1b revision used the challenger's unadjudicated first pass. It was read on the owner's instruction, and the owner's exception (decision 1 of 2026-10-14) still lacks its written reason, which is OD-01 in `AUTO-RESEARCH-REQUIREMENTS.md`.
   - Any successor that reads the dossier sees that material second hand, in `responses.md` CF-01 to CF-14 and the items it prompted. The successor's manifest should record this.
   - The independence withdrawal in `runs/CLD-P05-REVISION-0002/manifest.json` stays in force. The CF responses count only once the verifier rules on the objections they answer.
   - Under the verified-only directive, the successor must never open challenger output except inside a valid `verified-challenge` delivery. That excludes the project repository, its branches and PRs, forks and mirrors.

## 2. Reading order

### Tier 1: rules and current obligations (read first)

| Path | What it is |
|---|---|
| Packet `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/physical-release-d437c2f66090/Claude-P05-TIMING/` (`PACKET.json` SHA-256 `ff20816f…`) | Frozen governance inputs: `AGENTS.md`, `docs/`, `harness/PROPOSER.md`, `config/`, `domains/D05/` and the round-0 dossier copy. For a new actor, the coordinator issues its own packet |
| Amendment `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/Claude-P05-TIMING/COORDINATOR-AMENDMENT-0001/` (`AMENDMENT.json` SHA-256 `3f2a1777…`) | CLD-P05-AMEND-0001. `CHANGES.md` lists ten rule changes: unrestricted external reading; verified-only challenger output; auto round transport; self-freeze; the proposer checklist; preparation versus execution; review scope; assignments; budget; amendment receipt. `files/` supersedes the packet copies at the same paths, including `scripts/role_submission.py` and `scripts/round_transmit.py`. The bundle is addressed to this session; a successor needs its own |
| `HANDOFF.md` | This file |
| `AUTO-RESEARCH-REQUIREMENTS.md` | What the auto mode still lacks, phase by phase, ranked blockers, and owner decisions OD-01 to OD-16 |
| `receipts/CLD-P05-AMEND-0001-receipt.json` | Amendment receipt: rule-by-rule effects, every challenger artifact seen and how, runtime checks, conflicts |
| `receipts/CLD-P05-AMEND-0001-owner-decisions.json` | Owner decisions of 2026-10-14: keep the session, R1b transport confirmed, self-initiated reading allowed, no freeze or send before a verified challenge |
| Lab-results inbox `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/physical-release-d437c2f66090/Claude-P05-TIMING/lab-results/` | Read-only: `COORDINATOR-owner-decisions.md` (`b479fc60…`; answers U1 to U9 and the 300 core-hour ceiling), `COORDINATOR-runner-instructions.md` (`f36cf548…`; runner protocol) and results REQ-0001 to REQ-0009 |

### Tier 2: the dossier (scientific state)

All files are in `candidates/EDA-0002/`. This is what the challenger received through PR #26, digest `291fb885…`.

| File | Content and state |
|---|---|
| `proposal.md` | Main text. Status: **K2 activated.** P3-P5 as stated in round 0 are falsified (CLM-018 to CLM-020). The guarantee is narrowed to the capacitive-path certificate R1 (CLM-023), further restricted by P8 (timing exceptions, CLM-027) and P9 (float32 rounding, CLM-028). Novelty is **not** established (CLM-015, CLM-026). Holds the claim ledger CLM-001 to CLM-029, mechanism, soundness table, hypotheses, counter-hypotheses CH1 to CH9, kill criteria K1 to K7, known unknowns U1 to U13 and open questions |
| `direction-control.json` | **Frozen anchor** (problem, user, downstream need, causal mechanism, invariants, forbidden pivots). Penalties: combination drift 1, demand drift 0, total 1. Abandonment block: pending, with no consents |
| `experiment-plan.md` | Preregistered pilot: primary metric D_M(S) equality with full MCMM analysis; guardrails G1 to G7; baselines B0 to B6; amendment A-R1b |
| `tasklist.md` | EXP-001 to EXP-007 with owners, budgets and pass/fail rules, plus challenger slots. **Not yet bound by SHA-256** (rule 6 of the amendment): to do |
| `sources.json` | 71 source records, SRC-001 to SRC-071 |
| `prior-art.csv` | 19 rows, 9 columns |
| `search-log.md` | Queries Q1 to Q47. Q48 to Q56 are in `runs/CLD-P05-SELF-0001/manifest.json`, not yet folded in |
| `contest-audit.md`, `industry-gap.md` | Contest overlap (no global claim) and the commercial and open-source gap |
| `forecast.json` | All values null; no number invented |
| `responses.md` | No adjudicated objections. CF-01 to CF-14 are the owner-directed intake of the challenger's first pass, not objection responses |
| `experiment-consensus.json` | Pending; nothing signed |
| `dossier.json` | Status `submitted`, round 1 |

The R1b release allowlist excludes `dossier.json` and `experiment-consensus.json`. The coordinator integrates them.

### Tier 3: evidence and provenance

| Path | Content |
|---|---|
| `runs/CLD-P05-RESEARCH-0001/manifest.json` | Round-0 research run |
| `runs/CLD-P05-ADDENDUM-0001/manifest.json`, `addenda/EDA-0002/ADD-0001/` (4 files), `addendum-output-manifest.json` | ADD-0001: check of the PR #13 transport and a reading of SRC-012 from an Internet Archive capture (admissibility still open: OD-16), plus erratum E1 |
| `runs/CLD-P05-REVISION-0001/` | Round 1: `p3-p5-record.md` (the P3-P5 falsification, with counterexamples), `manifest.json` and `evidence/` (network logs, licenses, build configuration, `REQ-0008-counterexamples.csv`, fixture hashes, `runner-ledger.json`, which shows 0.4504 core-hours used) |
| `runs/CLD-P05-REVISION-0002/manifest.json` | Round 1b: the challenger first-pass intake, exposure record and independence consequence |
| `runs/CLD-P05-SELF-0001/reading-notes.md` and `manifest.json` | **Self-initiated reading to fold into the next response.** Covers SRC-012 and SRC-066 to SRC-068 in full through a text-extraction route, a new Cadence patent lead (US 8,245,167 B1), TCAD 2010 (the closest unread item for K1) and a forward-citation pass. Its "To fold in" list is the to-do |
| `lab-requests/` | Runner requests REQ-0001 to REQ-0009 (`.json` and `.sh`) and the property-check harness `p05_fixtures.py`, `p05_check.py` and `p05_extract.tcl`. OpenSTA `e01d3f16` was built on the runner with a Berkeley-yacc wrapper in place of GNU bison (open ruling: `AUTO-RESEARCH-REQUIREMENTS.md` B-06) |
| `tools/digest.py` | Proposer reimplementation of the repository dossier digest; not authoritative. Usage: `python3 -I tools/digest.py <dir holding the dossier files and challenges.md>` |
| `tools/check_dossier.py` | Structural cross-reference checker (sources, claims, prior-art); not the official validator. Usage: `python3 -I tools/check_dossier.py candidates/EDA-0002` |
| `tools/pdftext.swift` | PDFKit text extractor, page by page. Usage: `swiftc -O tools/pdftext.swift -o <scratch>/pdftext && <scratch>/pdftext file.pdf`. Build it in scratch, not in the outbox |
| `role-output-manifest.json` | Index of all outputs with SHA-256, rebuilt at handoff |
| `processed-deliveries.json` | Delivery receipts for the round wait. Currently `[]`. A successor that inherits this outbox can keep using it; with a separate outbox, it should start its own |
| `first-pass-plan.md`, `readiness.json` | Round-0 onboarding artifacts |

## 3. Where the work stands

- **Phase A (initial idea): done.** Rounds 0, 1 and 1b are complete.
- **Phase B (round loop): waiting.**
  - No `verified-challenge` delivery has arrived.
  - No proposer release has been frozen or sent through the transmitter: `submissions/` and `transmissions.jsonl` do not exist.
  - Owner decision 3 forbids freezing or sending before a valid delivery. The round bootstrap question is OD-02.
  - The challenger and verifier runtimes are "pending" in `round-transport.json` (OD-15).
- **Phase C (closure): not started.**
  - No consents have been signed.
  - Apply and give-up are both blocked by tooling and rule gaps (OD-06 to OD-09, OD-11).

## 4. Next actions for the successor, in order

1. After the section 1 steps, verify the successor's own packet and amendment hashes and write its receipt.
2. Recompute the dossier digest and confirm `291fb885…`. Verify the outbox files against `runs/CLD-P05-HANDOFF-0001/manifest.json`.
3. Start one background wait on the proposer inbox, using the seen-file.
4. While waiting, do only labelled self-initiated work, per owner decision 3. Useful items:
   - try TAU 2018 and 2019 again through WebFetch (U8);
   - seek a legal copy of TCAD 2010 (OD-04).
5. On a valid `verified-challenge` delivery, follow `AUTO-RESEARCH-REQUIREMENTS.md` B-04:
   1. Respond only to OBJ IDs that carry verdicts.
   2. Fold in CLD-P05-SELF-0001, labelled self-initiated, in particular the corrections to CLM-015 and CLM-026 and the TCAD 2010 addition to K1.
   3. Add the checklist sections Coverage, Gap, Contribution, Demand, Headroom, Contests and Delivery.
   4. Bind task-list dependencies by SHA-256 and rescore both drift penalties.
   5. Run checks, assemble `release/`, then freeze, send, `ack` and wait again.
6. Never change the frozen anchor. A different mechanism or objective needs a new topic ID (`harness/PROPOSER.md` step 5). If no anchor-preserving path remains, propose evidence-backed joint abandonment.

## 5. Runtime pitfalls seen in this session

- **Never use `cd` in shell commands; use absolute paths.**
  - `cd` moves the host's primary working directory and triggers deny-rule hooks.
  - It also leaves empty `.claude/.cc-writes` folders, which already exist in the outbox root, `lab-requests/` and `candidates/EDA-0002/`.
  - These folders are ignored by `role_submission.py` and hold no files, but they must be excluded from any manual transport.
- **Network differs by tool.**
  - Bash reaches only GitHub and arXiv.
  - WebFetch reaches any domain but returns summaries and cannot parse PDFs. The `https://r.jina.ai/<url>` text-extraction route worked for most PDFs.
  - A coordinator guard blocks any tool call that names the project repository or the owner's accounts. Write such names only with the Write tool.
- **`ps` and `pgrep` are blocked.** Monitor background tasks through their output files.
- **Use the host clock as is.** It is now accurate. Erratum E1 (+54,000 s) applies only to records written before 2026-10-14T10:27Z, as each says.
- **Run Python on downloaded data with `-I`, and keep downloads in their own scratch folders.**
- **Never put the operator's email address or any credential in a file.** `role_submission.py` rejects credential-like strings at freeze.

## 6. What the outgoing actor did not do

- No freeze, send, consent, approval, merge or git operation.
- No experiment or real-design measurement.
- No runner job since round 1.
- No edits to the packet, the amendment bundle, governance or any inbox.
- No reading of other roles' outboxes, scratch or conversations.
- No challenger output read since the verified-only directive took effect.
