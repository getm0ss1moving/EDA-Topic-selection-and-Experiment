# What the proposer needs to run the automatic research mode end to end

| Field | Value |
|---|---|
| Author | `Claude-P05-TIMING`, proposer for EDA-0002, session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8` |
| Requested by | The human owner, in chat on 2026-10-14 |
| Written | 2026-10-14, host clock (checked against a GitHub Date header at 10:27Z) |
| Basis | Amendment CLD-P05-AMEND-0001 (`AMENDMENT.json` SHA-256 `3f2a1777…`), the frozen packet `ff20816f…`, and what this session observed while working (each item cites its evidence) |
| Nature | A requirements and gap list for the owner and the coordinators. It is not scientific content, does not change the dossier, and authorizes nothing. Suggestions are labelled as suggestions; the decisions stay with the owner |

## 0. The goal, in three phases

1. **Phase A: initial idea.** Read papers, contest material, open implementations and public commercial evidence; then write a complete, sourced dossier. EDA-0002 has done this already (rounds 0, 1 and 1b). A successor topic would repeat it.
2. **Phase B: round loop.** Freeze a release and transmit it. Wait for a `verified-challenge` delivery, respond to the adjudicated objections, freeze again and transmit again. Repeat for up to three rounds (`config/research-brief.json`, `max_review_rounds: 3`).
3. **Phase C: closure.** Either **apply** (both roles sign the same task list, the verifier passes the gate, a human confirms promotion, and the pilot runs) or **give up** (a joint abandonment signed by both roles and checked by the verifier, then the dossier is archived).

Status codes used below:

- **OK**: observed working in this session.
- **PARTIAL**: works, with a limitation.
- **MISSING**: absent or blocked.
- **UNTESTED**: configured but never exercised.
- **DECISION**: needs an owner ruling.

## 1. Top blockers, ranked

| # | Blocker | Phase | Status | Who can resolve it |
|---|---|---|---|---|
| 1 | The challenger and verifier sessions are not running with inbox access. `round-transport.json` lists both runtimes as "pending", so no `verified-challenge` delivery can reach me, and my wait will only time out | B | MISSING | Codex and DeepSeek coordinators |
| 2 | Round bootstrap. R1b reached the challenger through PR #26, not through the transmitter. I have no `submissions/` folder and no `transmissions.jsonl`, so no content-addressed proposer release ID exists for the verifier to cite | B | DECISION | Owner (see B-02) |
| 3 | `signed_revision` in `experiment-consent.json` has no defined value in auto mode, and the obvious one (the ID of the release that contains it) is circular | C (apply) | DECISION | Owner and coordinator (see C-01) |
| 4 | Joint abandonment cannot be signed by the challenger. No abandonment-consent file is in its release allowlist, and it cannot edit my `direction-control.json` | C (give up) | MISSING | Coordinator (tool change) |
| 5 | Final promotion needs a `CONFIRM` from a registered human reviewer on a GitHub account distinct from the PR author (`docs/GITHUB.md`). If `VERIFIER_LOGINS` is empty, promotion is blocked | C (apply) | DECISION | Owner |
| 6 | Task-list co-authoring is slow by design. Challenger task-list revisions reach me only inside verifier deliveries, so every iteration costs a full verifier pass | C | DECISION | Owner (see C-02) |
| 7 | No official validator. My packet has no `scripts/project.py` and no `templates/topic/`, yet `AGENTS.md` requires `python3 scripts/project.py validate` before submission. I use my own reimplementation of the digest function, which is not authoritative | B, C | MISSING | Coordinator (amendment bundle) |
| 8 | PDF reading is indirect and unhashable. WebFetch does not extract PDF text; Bash cannot download from paper hosts; no local PDF tools exist | A, B | PARTIAL | Owner and coordinator (see A-01) |
| 9 | Paywalled sources. The closest unread item for K1 is Guerra e Silva, Phillips and Silveira, IEEE TCAD 29(1), 2010 (DOI 10.1109/TCAD.2009.2034343), which is not open access | A, B | MISSING | Owner (supply a copy) or verifier |
| 10 | Session continuity. The background wait lives only while this CLI session is open. A usage-limit stop or a closed terminal ends it, and a stopped CLI cannot be revived by its own background child (`docs/AUTO-ROUND.md`) | all | PARTIAL | Operator |

## 2. Cross-cutting runtime needs

### N-01 Session continuity and wake-up (PARTIAL)

- **Need:** the session stays alive during a round, wakes when a delivery arrives, and can be resumed with the same session ID after an interruption.
- **Evidence:**
  - The wait `round_transmit.py wait --seen-file … --timeout 86400` started as a background task at 10:29Z and was still running at 10:54Z (its output file was empty).
  - Earlier, the session stopped at a claude.ai usage limit and resumed only when the owner typed "continue".
  - `docs/AUTO-ROUND.md` treats model wake-up as unverified until a real delivery is acknowledged.
- **Needed from the operator:**
  1. Keep the machine awake and the CLI open during a round.
  2. Resume only this session (ID above) from its reviewed launcher (`runs/CLD-P05-LAUNCH-0001`), never a second session.
  3. After any interruption, ask me to restart the wait. The seen-file `processed-deliveries.json` ensures a delivery that arrived while I was away is replayed, not lost.
  4. Expect a wake-up about every 24 h even without a delivery, when the wait times out; I restart it each time.
- **Test:** the first real delivery. I record its ID, the wake-up time and the `ack` in my next run manifest.

### N-02 Unattended permissions (UNTESTED)

- **Need:** the round's commands must run without approval prompts while nobody is watching, or a round stalls silently.
- **Evidence:**
  - A deny-rule hook blocked one compound command containing `cd` (round 1b).
  - Shell `cd` moves the host's primary working directory, and the host then creates empty `.claude/.cc-writes` folders, as it did once inside the dossier.
  - I now avoid `cd` and use absolute paths only.
- **Suggestion:** pre-allow exactly these command shapes, with the bundle path fixed:
  - `python3 -I <BUNDLE>/files/scripts/role_submission.py freeze --source <OUTBOX>/release --queue <OUTBOX>/submissions …`
  - `python3 -I <BUNDLE>/files/scripts/round_transmit.py {send|wait|check|ack} …`
  - Write and Edit inside `<OUTBOX>` only.
  - Nothing else needs widening.
- **Test:** the synthetic round in section 6.

### N-03 Process visibility (PARTIAL; acceptable)

- `pgrep` fails inside the sandbox ("sysmond service not found"), so I cannot list processes.
- I rely on the background-task notification and its output file instead. No change is required. If wanted, allow `ps` for the current user only.

### N-04 Official validator and templates (MISSING)

- **Need:** run the project's own structural validation and digest on my release before freezing, as `AGENTS.md` and `docs/WORKFLOW.md` step 7 require.
- **Evidence:** the packet holds only `templates/run.json`. My digest reimplementation reproduced the earlier value `29b9ab53…`, but only the coordinator's validator is authoritative.
- **Suggestion:** add hashed copies of `scripts/project.py`, `templates/topic/*` and any schema it reads to an amendment bundle, with a note that it runs offline on a scratch copy and needs no git or network.
- **Test:** validate a scratch copy of the R1b files and compare the result with the coordinator's `291fb885…`.

### N-05 Clock (OK)

- The host clock now agrees with server time. Erratum E1 (+54,000 s) applies only to earlier records. Nothing is needed.

### N-06 Durable state across context compaction (OK, on my side)

- Long rounds compress my context. All state that matters is kept in files:
  - `processed-deliveries.json`;
  - receipts under `receipts/`;
  - run manifests under `runs/`;
  - `role-output-manifest.json`;
  - the self-initiated reading plan in `runs/CLD-P05-SELF-0001/reading-notes.md`.
- Nothing is needed from the owner.

### N-07 Repository keyword guard (OK; side effect noted)

- WebFetch, WebSearch and Bash calls that name the project repository or the owner's accounts are blocked. I write such names only with the Write tool and never fetch them.
- A paper or tool whose name happens to match a guarded keyword would also be blocked. If that happens, I log it as an access limitation.

## 3. Phase A: reading papers and contests, then forming the idea

### A-01 Reading PDF full text (PARTIAL)

- **Observed:**
  1. WebFetch on a PDF returned compressed binary with no text. The tool saved a copy under `~/.claude/projects/…/tool-results/`, which the file tools are denied.
  2. Bash network is GitHub and arXiv only. `curl` to `www.eecg.utoronto.ca` was refused by the proxy ("host is not on the allow list").
  3. No standard PDF tooling: `pdftotext`, `pdfinfo`, `mutool`, `qpdf`, `gs` and `tesseract` are absent, and Python 3.9.6 has no `pypdf`, `PyPDF2`, `fitz` or `pdfminer`. *(Correction, 2026-10-15: local extraction does exist. `swiftc` is present, and the small PDFKit extractor `tools/pdftext.swift`, used in ADD-0001, prints a PDF's text page by page. So the remaining gap is getting PDF bytes onto disk, not extracting them.)*
  4. **Workaround used in CLD-P05-SELF-0001:** WebFetch through the public text-extraction service `r.jina.ai`. It worked for four papers and failed for one host (HTTP 422).
- **Limits of the workaround:**
  - Every answer passes through WebFetch's summarizing model, which refuses long verbatim quotes (about 125 characters).
  - Page numbers are sometimes lost.
  - No PDF hash can be recorded, so the verifier must reopen every original.
- **Options, from smallest change to largest (owner's choice):**
  1. **Allow the Read tool on this session's WebFetch `tool-results/` folder only.** Read parses PDFs page by page, so I would get real text, exact page locators and, through Bash on the same file, a SHA-256. The folder holds only tool outputs of this session, but it sits next to transcripts, so the grant should name the exact subfolder.
  2. **A library fetcher.**
     - I write a URL list to a request file in my outbox.
     - A coordinator process, or the networked runner `lab231` with its allowlist extended to scholarly hosts, downloads each PDF to a read-only `library/` folder, records SHA-256, URL and time, and runs `pdftotext`.
     - I read the text files.
     - Copies stay out of every release, because copyrighted full texts must not be published (`docs/EVIDENCE.md`).
  3. **Widen Bash network to named scholarly hosts and install poppler or pypdf** in a pinned environment. This has the largest surface and is the least preferred.
- **Test:** read page 3 of SRC-067 (DATE 2007, `past.date-conference.com/…/11.4_3.PDF`) verbatim with its printed page number, and record its SHA-256.

### A-02 Paywalled and fee-licensed sources (MISSING)

- I have no institutional credentials and will not bypass authentication (`docs/ISOLATION.md`). The current list, in K1 priority order:

| Priority | Item | Why it matters | Access seen |
|---|---|---|---|
| 1 | Guerra e Silva, Phillips, Silveira, "Effective Corner-Based Techniques for Variation-Aware IC Timing Verification", IEEE TCAD 29(1):157-162, DOI 10.1109/TCAD.2009.2034343 | The abstract claims exact worst-slack for sequential circuits: the closest unread item for K1 | OpenAlex abstract only, not open access |
| 2 | Nien, "A Unified Multi-Corner Multi-Mode Static Timing Analysis Engine", NTU master's thesis 2009 (handle 123456789/42970) | The thesis behind SRC-014; its contents list "Exact MCMM STA" and "Extension to Hold Time Check" | Catalogue only, fee-licensed |
| 3 | SRC-024 (IEEE TCAD 2024, Xplore 10419016) and SRC-025 (ISEDA 2024) | Recent MCMM acceleration; currently metadata only | Metadata |

- **Suggestion:** the owner places lawfully obtained copies in a read-only folder that my sandbox can read, with a provenance note naming who obtained each, from where and when, as `EDA_Source_Access_Guide.md` did earlier. I record hashes and short excerpts only. Alternatively, the items go to the verifier as "verifier full-text read required".

### A-03 Contest material (PARTIAL)

- **Need:** contest statements, rules, benchmarks, organizer baselines and winner reports. For D05 these are mainly the TAU contests (2013-2019 timing, CPPR, incremental and macro-modelling) and ICCAD CAD contest timing problems.
- **Observed:**
  - Pages on `tauworkshop.com` and Google Sites were read in earlier rounds.
  - TAU 2018 and 2019 were left open under the old GitHub/arXiv-only rule (U8). Rule 1 now permits other sites, so I can retry them by WebFetch at the next response.
  - Benchmark archives are usually zip or tar files on Google Drive, Dropbox or university servers. Neither WebFetch nor Bash can fetch and unpack those today.
- **Needed:** the library fetcher from A-01 option 2, extended to archives, for contest benchmarks if a topic needs them. EDA-0002's pilot uses OpenROAD-flow-scripts designs from GitHub instead, so this is not blocking now.

### A-04 Search and citation tooling (OK, with a reproducibility gap)

- WebSearch works but returns summaries. The OpenAlex API through WebFetch worked for forward citations (31 citing works in CLD-P05-SELF-0001).
- Because WebFetch summarizes, I cannot store the exact JSON response or its hash.
- **Suggestion:** add `api.openalex.org`, `api.crossref.org` and `dblp.org` to the Bash network allowlist, read-only GET. Search records would then hold exact responses and hashes, as `docs/EVIDENCE.md` asks for reproducible searches.

### A-05 Source code and tools (OK for reading; runner for execution)

- Reading source from GitHub through Bash works; for example, the OpenSTA files at `e01d3f16` were fetched and hashed in round 1b.
- **Running** tools happens only on the lab runner, through `lab-requests/` and `lab-results/`, under a written scoped allocation (`docs/EXPERIMENTS.md`). The local host has no Docker and no `gh`.

### A-06 Starting a successor topic (DECISION, only if EDA-0002 is abandoned)

- A successor needs a new topic ID, a new packet with a full template set, and a fresh challenger first pass with forecast screening.
- While `challenger_stage` is `initial`, the transmitter holds my release for the coordinator's semantic forecast screen, so the coordinator must be available promptly.

## 4. Phase B: the round loop

### B-01 Live counterpart seats (MISSING; blocker 1)

- `config/round-transport.json` names the challenger `Codex-C05-TIMING-R2` and the verifier `DeepSeek-V02-PHYSICAL`. Both runtime fields are "pending":
  - the challenger's inbox read grant and its write grant into the verifier's `from-challenger` folder;
  - the verifier session itself, planned from `runs/DSK-V02-LAUNCH-0001`, and its write grants into the proposer and challenger `from-verifier` folders.
- **Needed:** both sessions running, with those grants, and confirmed by a test delivery (section 6).

### B-02 Round bootstrap (DECISION; blocker 2)

- **Facts:**
  - R1b (dossier digest `291fb885…`) reached the challenger through PR #26.
  - I have never run `freeze` or `send`: `<OUTBOX>/submissions/` and `<OUTBOX>/transmissions.jsonl` do not exist.
  - Owner decision 3 forbids freezing or sending before a valid `verified-challenge` delivery arrives.
- **Problems:**
  - The verifier's ruling, and my later response, should refer to one immutable proposer release ID. Today that ID does not exist.
  - The verifier's inbox `from-proposer` folder most likely holds nothing from me, though I cannot read it.
- **Options:**
  1. Let me freeze R1b **unchanged** (its 11 release-allowlisted files; `dossier.json` and `experiment-consensus.json` are excluded by design) and send it now. This creates `SUB-<hash>` for R1b. No content changes, and the self-initiated reading stays out of it.
  2. Keep decision 3 as it stands, and have the coordinator confirm that the verifier adjudicates against dossier digest `291fb885…` delivered by packet. The verifier's `verification.json` should then name that digest, so that I can match it.
- **Suggestion:** option 1, because it gives all three roles the same byte-identical reference. Either way, the choice needs your ruling.

### B-03 What a usable `verified-challenge` delivery must contain (UNTESTED)

The transmitter enforces the structure: one verifier release listed first, plus exactly the challenger releases named in `--adjudicates`. To respond, I need these inside it:

1. `verification.md` and `verification.json` that give, for **every** OBJ ID in the included challenger releases:
   - the verdict (`valid`, `partially_valid`, `unsupported`, `refuted` or `unresolved`);
   - whether it blocks advancement;
   - the required action;
   - the source locators checked.
2. Verdicts on my own decision-critical claims, especially:
   - the R1 code argument and the P8 and P9 rules (CLM-023, CLM-027, CLM-028);
   - the novelty claims CLM-015 and CLM-026;
   - the falsified P3-P5 (CLM-018 to CLM-020).
3. The dossier digest or proposer release ID the verifier adjudicated against.
4. The challenger's `challenges.md`, its `sources.json` and `search-log.md`, and any challenger `tasklist.md` revision.

**Rule I will follow:** I respond only to OBJ IDs that carry a verdict. Any objection in an included release without a verdict is treated as an allegation and gets no scientific response (`docs/WORKFLOW.md` step 4).

**Suggestion:** the verifier rules on every objection in each release it includes, even if only as `unresolved`, so that nothing unadjudicated reaches the proposer inside an adjudicated release. This keeps the verified-only directive clean.

### B-04 My procedure on each delivery (UNTESTED end to end)

1. The wait returns `{"status": "delivered", …}`. I run `check` and open only deliveries marked `valid`.
2. I verify the delivery. The transmitter re-verifies every byte; I also record the `DLV-…` ID and each `SUB-…` ID.
3. I write `responses.md` point by point: accept and revise, dispute with evidence, defer to a named test, or propose abandonment. The self-initiated reading (CLD-P05-SELF-0001), labelled as such, goes in at this step.
4. I revise the proposal, sources, search log, prior art, industry gap, plan, task list and forecast together, then rescore both drift penalties in `direction-control.json`.
5. I add the explicit Coverage, Gap, Contribution, Demand, Headroom, Contests and Delivery sections required by `harness/PROPOSER.md`, and bind task-list dependencies by SHA-256 (`docs/EXPERIMENTS.md`).
6. I run structural checks (official ones once N-04 is met), assemble `<OUTBOX>/release/` with allowlisted files only, freeze, `send`, then `ack` the delivery, and restart the wait.
7. I write a run manifest naming the delivery IDs, the release ID and the exposures.

### B-05 Provenance that cannot travel in a release (DECISION)

- The proposer allowlist in `role_submission.py` does not include run manifests, receipts or `role-output-manifest.json`. `AGENTS.md` asks for run records under `runs/`, and the round publisher pushes only frozen releases.
- **Question:** should the coordinator publish my `runs/CLD-P05-*` records separately, or should I summarize provenance inside `search-log.md` and `responses.md`? Without a ruling I will do the second and keep the full manifests in my outbox.

### B-06 Lab-runner work prompted by objections (DECISION)

- Verified objections may require new bounded checks, such as finite tests of P8 and P9 (EXP-002b steps 6-9) or the exception census.
- The runner exists, and requests REQ-0001 to REQ-0007 ran in round 1. But allocation CLD-LAB-0001 was scoped to the P3-P5 checks of round 1.
- **Needed:**
  1. a written, scoped allocation for round-2 property checks (purpose, host, network false, CPU, time and storage limits);
  2. a ruling on whether runner use counts against the 8 CPU-hour pilot budget (`config/research-brief.json`); the ledger stands at 0.4504 core-hours;
  3. a ruling on the parser-generator deviation: OpenSTA was built with a Berkeley-yacc wrapper because GNU bison has no GitHub release with clear provenance, so the generated parsers differ from a bison build. Does the verifier need a bison build?

### B-07 Round limits and disputes (DECISION)

- At most three review rounds. The owner or coordinator should state who declares a round finished. Per `docs/AUTO-ROUND.md`, the verifier's delivery to me ends the round, and the publisher then opens one PR per round.
- If I dispute a verifier conclusion, the appeal is a file with a precise counter-source. It can travel in my next release, which goes to the verifier and the challenger. `docs/CHARTER.md` assigns contested verifier conclusions to "a second verifier or a human adjudicator", and no such seat is configured. **Needed:** name it.

## 5. Phase C: closure, apply or give up

### C-01 Experiment consent mechanics (DECISION; blocker 3)

- `experiment-consent.json` must have exactly `session_id`, `decision` (`pending`, `agree` or `revision_requested`), `signed_revision`, `tasklist_sha256` and `rationale`.
- **Problem:** both roles must sign "the same frozen revision". If `signed_revision` were the ID of the release that contains the consent, the ID would depend on its own content.
- **Suggested rule:**
  1. I freeze a release `R_final` whose `tasklist.md` has SHA-256 `t` and which contains no consent.
  2. The challenger and I each release an `experiment-consent.json` with `signed_revision` set to `"SUB-<R_final>"` and `tasklist_sha256` set to `t`. My consent release carries the same `tasklist.md` bytes, unchanged.
  3. The coordinator copies both into `experiment-consensus.json` unchanged. The verifier checks that both name the same `R_final` and `t`, and that `t` matches the bytes.
  4. Any later task-list edit creates a new `R_final` and resets both consents.
- **Needed:** the owner and coordinator adopt this rule or another one in writing, and the challenger receives the same rule.

### C-02 Joint task-list authoring (DECISION; blocker 6)

- The challenger supplies falsification tests, fairness controls and missing prerequisites in its own `tasklist.md`. That file reaches me only inside a `verified-challenge` delivery.
- Converging on identical task-list bytes may therefore take several full verifier passes, within the three-round limit.
- **Options:**
  1. Accept the latency.
  2. Allow the verifier to forward a challenger task-list revision with a light, task-list-only adjudication.
  3. Define a task-list-only round that does not count against the three review rounds.

### C-03 Binding dependencies before signing (DECISION)

- The task list must bind its dependencies by content or SHA-256: baseline versions, metrics, thresholds, budgets, splits, oracle and stop rules.
- Several pilot inputs do not exist yet. Placed and routed designs with parasitics need a P&R run, and owner decision U6 says P&R has no allocation until the plan is accepted.
- **Needed:** either
  - permit binding by procedure (pinned ORFS and OpenSTA commits plus the SHA-256 of the generation scripts and configurations), with the output hashes recorded when the data are generated and checked by the verifier; or
  - authorize a scoped data-preparation allocation for P&R before consent.
- Without one of these, a fully bound task list cannot be signed.

### C-04 Promotion gate (DECISION; blocker 5)

- **Steps:**
  1. Both consents are on the same revision and task-list hash.
  2. The verifier issues `accept_for_pilot` and checks the digest.
  3. The coordinator opens a promotion PR into `topics/EDA-0002/`.
  4. A registered human reviewer on a **different** GitHub account from the PR author approves with `CONFIRM <full-head-sha>` (`docs/GITHUB.md`).
- **Needed:** an enrolled reviewer account in `VERIFIER_LOGINS`. One owner account for all roles cannot satisfy this.

### C-05 Running the pilot after promotion (MISSING until allocated)

The preregistered pilot needs:

- the OpenSTA build already made on the runner, plus the bison ruling (B-06);
- an implementation of the method P inside a pinned OpenSTA fork:
  - the bound pass;
  - clock-only search;
  - certificate logging;
  - cone-restricted refinement;
  - the P8 and P9 rules;
- **Needed for the implementation:** a decided home for that code (a fork or patch set under the runner, or a PR to the project repository), and who reviews it;
- ASAP7 libraries and designs from ORFS (GitHub) with repository-verified licenses (U5);
- the P&R allocation (U6) and the baseline runs B0 to B6 under the frozen limits (2 CPUs and 4 GiB per job; 8 CPU-hours for the pilot unless reallocated);
- a final experiment report under `reports/final/`, which needs the human `CONFIRM` again.

I will not estimate compute numbers that have not been measured; the plan's caps stand until you change them.

### C-06 Giving up: joint abandonment (MISSING; blocker 4)

- **Rule** (`docs/CHARTER.md`, `docs/WORKFLOW.md` step 8):
  - the proposer and the challenger independently sign the same frozen revision and dossier digest, on evidence-backed grounds;
  - the verifier checks the evidence and the process;
  - the dossier is archived with its evidence, penalties and resurrection conditions;
  - a successor needs a new topic ID.
- **Gap:** the consents live in my `direction-control.json`, under `abandonment.consents`. The challenger's release allowlist (`challenges.md`, `sources.json`, `search-log.md`, `prior-art.csv`, `independent-estimate.md`, `tasklist.md`, `experiment-consent.json`) has no file in which to sign, and the challenger must not edit my file.
- **Suggestion:**
  - Add `abandonment-consent.json` to both allowlists, with exactly these keys:
    - `session_id`;
    - `decision` (`agree`, `decline` or `pending`);
    - `grounds` (any of the four charter grounds);
    - `signed_revision`;
    - `signed_dossier_digest`;
    - `rationale`.
  - Validate it like `experiment-consent.json`, so it can only sign for the releasing session.
  - The coordinator copies both, unchanged, into `direction-control.json` → `abandonment.consents`, and the verifier checks them.
- **Test:** a synthetic abandonment on a test topic (section 6).

### C-07 Neither apply nor give up (DECISION)

- After three rounds without consensus, the options are to park with specific open questions or to request human arbitration (`docs/WORKFLOW.md` step 8).
- **Needed:** who arbitrates, and how a parked topic is resumed.

## 6. Suggested end-to-end test before the real round

Run it on a synthetic test topic configured in `round-transport.json` with the three real identities, so no EDA-0002 release is used. `docs/ISOLATION.md` allows at most one synthetic role test while controls are incomplete.

1. **Proposer send.** I freeze a trivial allowlisted release and `send` it.
   - *Expected:* the write grants into the challenger and verifier `from-proposer` folders work (never exercised so far), and `transmissions.jsonl` records two deliveries.
2. **Challenger to verifier.** The challenger freezes a one-objection release and sends it to the verifier.
3. **Verifier to proposer.**
   - The verifier rules on the objection and sends with `--adjudicates SUB-…`.
   - *Expected:* my background wait returns, I wake without a human prompt, `check` shows it `valid`, and I `ack` it.
   - *This is the first real test of N-01 and of model wake-up.*
4. **Consent drill.** Both roles release `experiment-consent.json` under the C-01 rule, and the verifier matches them.
5. **Abandonment drill**, if C-06 is implemented: both roles sign `abandonment-consent.json`, and the verifier checks it.
6. **Publisher dry run.** `round_publish.py publish ROUND-ID --dry-run` builds and validates the round commit.

**Pass criterion:** every step finishes without a human typing into any session, and each role leaves a receipt naming the delivery and release IDs.

## 7. Owner decisions requested, in one list

| ID | Decision | Section |
|---|---|---|
| OD-01 | Supply the written rationale for the round-1b exception. Decision 1 arrived with an unfilled placeholder; I will not write your reason for you | receipts |
| OD-02 | Bootstrap: freeze and send R1b unchanged now, or have the verifier adjudicate against digest `291fb885…` by packet | B-02 |
| OD-03 | PDF access route: Read on the `tool-results/` subfolder, a library fetcher, or wider Bash network | A-01 |
| OD-04 | Paywalled sources: supply copies (TCAD 2010 first), or route them to the verifier | A-02 |
| OD-05 | Add the official validator and templates to an amendment bundle | N-04 |
| OD-06 | The `signed_revision` rule for consents | C-01 |
| OD-07 | Task-list exchange path between challenger and proposer | C-02 |
| OD-08 | Add an abandonment-consent file to both allowlists | C-06 |
| OD-09 | Enroll a distinct reviewer account in `VERIFIER_LOGINS` | C-04 |
| OD-10 | Runner allocation for round-2 property checks; whether runner use counts against the pilot budget; the bison ruling | B-06 |
| OD-11 | Binding by procedure, or a scoped P&R preparation allocation | C-03 |
| OD-12 | Second verifier or human adjudicator for appeals; arbitration after three rounds | B-07, C-07 |
| OD-13 | Publication of proposer run manifests | B-05 |
| OD-14 | Pre-allowed command shapes for unattended running | N-02 |
| OD-15 | Launch the challenger and verifier runtimes with their inbox grants | B-01 |
| OD-16 | Still open from before: keep the edit-loop comparison in the pilot. ADD-0001 admissibility may be moot now that SRC-012 was read from the author host (CLD-P05-SELF-0001), but that reading still needs verifier re-checking | — |

## 8. What I will do without further input

- Keep the background wait running and restart it after each timeout.
- On a valid delivery, follow B-04 exactly.
- Record every exposure, access limit and delivery ID in files.
- Never open challenger output except inside a valid `verified-challenge` delivery.
- Never freeze or send before such a delivery (owner decision 3), unless OD-02 says otherwise.
- Never sign for another role, approve or merge.
- Never run an experiment without an allocation and consensus.
