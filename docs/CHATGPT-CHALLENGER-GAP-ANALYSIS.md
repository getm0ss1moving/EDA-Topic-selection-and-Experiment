> Historical operational reference. Current human-led workflow: [WORKFLOW.md](WORKFLOW.md). AI proposer launch and automatic AI succession instructions below are inactive.

# Challenger automation gap analysis and ChatGPT-only migration

Written 2026-10-15 by the coordinator from released artifacts and repository code.
This is an infrastructure assessment, not a scientific verdict on EDA-0002.

## Answer

The challenger has already performed a real R1b review, self-frozen it and delivered
it to the verifier. What was missing was durable scheduling of the next native
GPT job, current role bindings and automatic outcome handling. A delivered file did
not prove that an idle model session would wake. The new Codex-only coordinator
removes that dependence. Live GPT research-loop validation is still required.

## Inspected inputs

- PR #32, `claude/auto-circuit`, input commit
  `4f0068934ebe280ae6db6bb1fa3a42ff7f0056a0`: contains #18, #26, #29, #30 and #31.
- Explicitly owner-released verifier `gap-analysis.md` under
  `EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL/`.
- Explicitly owner-released proposer `AUTO-RESEARCH-REQUIREMENTS.md` under
  `EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING/`.
- Existing Codex challenger release `SUB-e81a3116230c993ef314885730e0e5202a2bbfeab70328f5bfcc8b35c0511c7f`,
  PR #30; transport receipt `DLV-20261014T105602Z-challenger-e81a3116230c`.

No private conversation, reasoning, memory or another role's scratch was inspected.
The two historical requirement notes contain stale blockers; they are reconciled
below rather than treated as current runtime authority.

## Capability map

| Required challenger step | Existing evidence | Change in this revision | Remaining proof |
|---|---|---|---|
| Receive a completed proposal automatically | Frozen packet export and local inbox transport exist | Native coordinator schedules challenger after a validated proposer release; no human reminder or forecast-screen request | One real GPT delivery-triggered job |
| Read the actual cited papers and contest material | Search contract and R1b source ledger exist | Any accessible external source may be read; record abstract/full-text level and access gaps | PDF/full-text access must be observed per source |
| Independently find other papers and contests | #18 extended search beyond proposer bibliography | Coverage outcome is required; newer contest editions, baselines and winner reports are explicit | Review actual search ledger for breadth and source quality |
| Find meaningful objections | Stable OBJ IDs, locators and falsification tests exist | Bind every assessment to the exact proposer release; retain evidence burden | Semantic quality remains verifier work |
| Recommend the proposal is not meaningful | Previously an informal narrative | Explicit `not_meaningful` outcome, matching abandonment signatures and verifier evidence check | A real or synthetic matching-consent closure |
| Recommend feasibility | Task-list and feasibility checks exist | Explicit `feasible` outcome; no forced objection quota; both task-list consents required for selection | Actual resource and oracle evidence |
| Freeze and send to verifier | Existing release and actual challenger delivery demonstrated | Self-freeze remains actor-owned; coordinator routes the completed release and invokes verifier | Native all-GPT run, not a Claude stand-in |
| Resume proposer after verification | Claude live stand-in circuit passed in #32 | Scheduler invokes a fresh proposer job with only adjudicated challenges | A complete native GPT proposer/challenger/verifier/proposer circuit |
| Publish every completed round | #32 publisher exists but main registration could block it | Each automatic round PR includes exact logical registrations with its frozen outputs | GitHub publication against deployed code/checks |

## What changes for the three ChatGPT roles

| Role | Inputs | Decision/output | Automatic next step |
|---|---|---|---|
| Proposer | Brief, own previous release, optional historical released seed, adjudicated challenges | Complete proposal/task list; responses; own consents | Self-freeze, transmit, schedule challenger |
| Challenger | Current proposer release, own previous output, verifier corrections | Independent search and OBJ ledger; revise/not_meaningful/feasible/unresolved; own consents | Self-freeze, transmit only to verifier |
| Verifier | Matching proposer/challenger pair and their released consent targets | Compact evidence table, all OBJ verdicts, eight gates, next action | Self-freeze, publish round, release adjudicated packet, schedule proposer or closure |

A model-family change does not inherit a predecessor's session or signature.
New ChatGPT seats recheck historical released work. Old Claude and DeepSeek
registries and runs remain audit history; no new role uses their launchers or API.

## Reconciliation of historical gaps

| Historical gap | Current resolution |
|---|---|
| Verifier G1/G2: unknown registered ID and packet pair | Coordinator assigns a logical UUID before the first job and includes the binding atomically in the round PR; no model invents registration |
| G3: brief and launch registry disagree | Schema-2 active assignments and D04/D05 briefs agree; validator checks them |
| G4 / proposer N-04: missing project digest tool | Every new role packet includes `project.py`, `role_submission.py` and topic templates |
| G5/G6: old challenge or incorrect proposal pairing | Each review and verdict must name the current immutable proposer/challenger pair; historical R0 verification is not reused for R1b |
| Proposer B-01/N-01: counterpart runtime and wake-up | A coordinator starts finite native jobs; no Claude background task wake-up is assumed |
| B-02: cannot freeze before receiving verification | Removed: first completed proposer output is the bootstrap release |
| C-01: self-referential consent | Sign an earlier proposal release; scientific bytes cannot change during consent collection |
| C-06: nowhere for challenger abandonment consent | #32 added the file; both roles can sign their own copy and the coordinator validates matching targets |
| C-02/B-07: task-list latency and human arbitration | Consent exchanges have a separate phase; unresolved topics park and a fresh successor starts automatically |
| A-01/A-03/A-04: source/PDF/network restrictions | Remove provider/domain allowlists for research reading; log real access failures. Actual PDF parsing support still needs native-runtime testing |
| C-04: distinct human GitHub account required | Human approval is optional for automatic research decisions under the latest owner instruction; scientific three-role verification remains required |
| B-05: provenance cannot travel | `workflow.json`, frozen manifests and the completed-round registration/decision record travel in the same PR; private logs stay private |
| B-06/C-05: experiment allocation and implementation | Retain actual existing resource limits; autonomous research cannot manufacture licenses, compute or a completed implementation |

## Remaining work before claiming the entire system is operational

1. Run one native GPT synthetic end-to-end circuit using the account's actual
   model IDs. Check that each job completes, sources can be retrieved, every
   release is immutable, pairing errors are refused and the proposer sees only
   adjudicated challenges. A prior Claude/DeepSeek smoke does not prove this.
2. Test timeout/restart/quota recovery and GitHub publication from the deployed
   coordinator. Keep a process alive or install a user service; a committed script
   does not prove a daemon is running. No supervisor is launched by this revision's
   `prepare` or unit tests.
3. Complete and exercise the canonical dossier promotion/archive adapter. Runtime
   `selected_for_pilot` and `abandoned` decisions are recorded with releases and
   consents, but cannot be advertised as a validated `topics/` promotion until the
   full dossier passes `project.py validate` and is published. The original
   project validator still enforces the scientific acceptance criteria.
4. Connect a selected topic's task list to the existing bounded experiment runner,
   including input-generation provenance, budget accounting, result collection and
   the return of measured results to the next research round. No new compute or
   paid-source access is invented. Missing prerequisites stay explicit.

These are concrete integration/validation tasks, not reasons to ask the owner to
freeze packets, paste session IDs, wake roles or approve each research iteration.
Do not label the system fully unattended until the native circuit and recovery
checks have actually passed.
