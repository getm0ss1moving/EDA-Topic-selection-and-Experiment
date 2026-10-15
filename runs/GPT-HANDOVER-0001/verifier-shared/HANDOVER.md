# Handover — verifier seat, EDA-0002 (D05), round-1 challenge adjudicated

**Working note, not a release artifact.** The verifier release allowlist is exactly
`{verification.md, verification.json}` (`scripts/role_submission.py`, `FILES['verifier']`). Do not copy this
file, `readiness.json`, `first-pass-plan.md` or `gap-analysis.md` into `release/` — `validate_manifest` will
reject the whole release as "not role-owned". Do not freeze anything without a coordinator-registered
session ID (see §6, G1) and never invent one.

| Item | Value |
|---|---|
| Actor / role | `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`), verifier, domains D04/D05 |
| Topic / stage | EDA-0002, domain D05 (TIMING), round 0 dossier `submitted`, round-1 challenge adjudicated |
| Session (host-observed, **not** registered) | `e6bc9983-e74b-4576-9c1d-3abc95ea3df9` |
| Packet SHA-256 / input commit | `db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78` / `27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88` |
| Status | Verification complete for this round; **`decision: revise`; not frozen, not published, not released** |
| Written | 2026-10-15 (handover note; content of the release files dates from 2026-10-14) |

**One-paragraph orientation.** The round-1 challenge (OBJ-001 CRPR sign, OBJ-002 `thresholdAdjust`) has been
fully adjudicated against the pinned OpenSTA commit. OBJ-001 is `refuted` (the challenger's entailment is
sign-inverted; the code is quoted accurately but the conclusion is wrong), OBJ-002 is `partially_valid`
(non-blocking; needs a CLM-007/P4 wording amendment plus an EXP-002 audit addition), and novelty kill
criterion K1 is **not triggered**. Nothing blocks the dossier, but seven of eight admission gates remain
false for reasons unrelated to the objections, so the decision is `revise`, not `accept_for_pilot`. The two
release files are final and hash-stable; the freeze was not executed because the registered session ID was
never supplied.

---

## 1. Release payload (the deliverable; frozen-candidate)

Directory: `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL/release/`
Exactly two files, nothing else may be added.

| Path | Bytes | SHA-256 | Content |
|---|---|---|---|
| `release/verification.md` | 14 219 | `1d1fa656e8bf273bb535498a216ea937fbcbe8f8469fb4708560c5762a0d8489` | Human-readable record: reviewer identity and independence disclosure, packet provenance, per-claim/objection evidence table with exact locators, eight-gate table, decision `revise` with reversal conditions and limitations |
| `release/verification.json` | 10 398 | `b018b8c2a918275724c2ff58cf5fe739ebc00f55e1b6618afe5e9cd61b77853f` | Machine record: `decision`, `verifier_session`, `dossier_digest` (`null`), eight gates, 14 `source_checks`, 2 `objections` |

Facts a successor must not disturb without cause:

- `gates`: only `direction_integrity` is `true`; `novelty`, `mechanism`, `utility`, `contest_originality`,
  `headroom`, `feasibility`, `experiment_consensus` are `false`.
- `objections`: `OBJ-001` → `refuted`, `blocking: false`, `resolution: resolved`; `OBJ-002` →
  `partially_valid`, `blocking: false`, `resolution: open`.
- `dossier_digest` is `null` because `scripts/project.py` is absent from the packet. `verifier_session`
  holds the host-observed session ID and is explicitly flagged in `verification.md` as pending coordinator
  confirmation — replace it only with the registered value.
- The payload already passes the packet's own validators (`validate_manifest`, `check_content`: UTF-8, valid
  JSON, no credential-like text; 24 617 B against 8 MiB/file and 32 MiB/bundle caps), verified in memory
  without writing any artifact. See `gap-analysis.md` §3.1.

## 2. Working notes in the same outbox (context, not releasable)

Outbox root: `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL/`

| Path | Bytes | SHA-256 | Purpose |
|---|---|---|---|
| `readiness.json` | 13 015 | `fa038aaa3caf6b094e87b1d09b18587ff52bf96d22119c09a554fc90520b9cc4` | Onboarding record: identity, declared model, packet hash recomputed, 42/42 file hashes, observed isolation controls, unlisted context, contamination assessment, the two documentary items DOC-1/DOC-2, list of referenced-but-absent inputs |
| `first-pass-plan.md` | 16 083 | `8f0f647c62380494e2c878fe40c3e1f30ceac2c86a30a8befa20449904cdb9b8` | Pre-adjudication plan: triage order T0–T6, per-class claim check spec, objection protocol, gate plan, escalation conditions, evidence required for a verdict |
| `gap-analysis.md` | 16 237 | `dfa3c177cf8641351dd5a74f9b387552d6c348d5de4e56124b5b276ce5539bb5` | Why the freeze/transport/role-handoff have not happened: four-leg gap table, the exact code lines that would have to differ to uphold OBJ-001, freeze flag inventory, G1–G10 gap list by owner |
| `HANDOVER.md` | this file | — | File-location map and successor instructions |

## 3. Read-only packet inputs (scientific record of this round)

Packet root (read-only; do not write):
`/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/verifier-release-20261014/DeepSeek-V02-PHYSICAL/`

| Path under packet root | Why it matters to a successor |
|---|---|
| `PACKET.json` | 42 listed file hashes, actor, role, commit, phase; recomputing its SHA-256 reproduces the packet identifier |
| `ASSIGNMENT.json` | Declared model/effort (`deepseek-flash`, low), domains, isolation statement |
| `candidates/EDA-0002/proposal.md` | CLM-001…CLM-017, P1–P6, CH1–CH5, K1–K6, U1–U9 — the claims this verification is about |
| `candidates/EDA-0002/challenges.md` | **OBJ-001**, **OBJ-002**, OQ-1…OQ-5, S-1…S-4 — the objections adjudicated |
| `candidates/EDA-0002/findings-challenger.md` | F-1…F-15 supporting findings |
| `candidates/EDA-0002/sources.json` / `sources-challenger.json` | 52 + 30 evidence records (SRC-…, C-A…); the ledgers my `source_checks` reference |
| `candidates/EDA-0002/experiment-plan.md`, `tasklist.md`, `experiment-consensus.json` | D_M(S) definition, EXP-001…EXP-009 with caps, guardrails G1–G6, consensus still `pending` with null consents |
| `candidates/EDA-0002/direction-control.json`, `forecast.json`, `dossier.json`, `responses.md` | Anchor with penalties 0/0; null forecast with calibration plan; dossier status; `responses.md` correctly empty |
| `candidates/EDA-0002/verification.md` / `verification.json` | The stub I replaced (all TBD / `pending`) — do not confuse with my release copies |
| `config/launch-release.json` | Assignments for EDA-0002, `packet_ref_policy`, `experiment_authorization: false`; source of the DOC-1 inconsistency |
| `config/research-brief.json`, `config/physical-resources.lock.json` | 8 CPU-h cap, 2 CPU/4 GiB per job, D05 metric and thresholds, resource lock |
| `domains/D05/brief.json` | Still names challenger `DeepSeek-C05-TIMING` / verifier `Codex-V02-PHYSICAL` — the DOC-1 conflict |
| `harness/ONBOARDING.md`, `harness/VERIFIER.md` | Role rules; item 8 of VERIFIER.md is the digest instruction I could not satisfy |
| `docs/WORKFLOW.md`, `docs/EVIDENCE.md`, `docs/FORMATS.md`, `docs/SELF-SUBMISSION.md`, `docs/ISOLATION.md`, `docs/CHARTER.md`, `docs/PHYSICAL-PILOT.md` | Workflow steps 4–8, evidence standard, `verification.json` schema and gate rules, freeze/publish procedure, isolation rules |
| `templates/topic/verification.md` | The skeleton my `verification.md` follows |
| `scripts/role_submission.py` | The trusted freeze/verify/publish tool (allowlists, manifest validators, SECRET regex, size caps, publish identity checks) |

## 4. Out-of-packet evidence copies (scratch — may be ephemeral)

Root: `/tmp/claude/ds-v02-scratch/` (`/tmp` survives reboots inconsistently; re-fetch from the URLs below if
missing). Nothing here is releasable; it exists so a successor can re-read the decisive bytes without
re-downloading.

### 4.1 Pinned OpenSTA sources — `scratch/opensta/`

Fetched from `https://raw.githubusercontent.com/The-OpenROAD-Project/OpenSTA/<commit>/<path>` with
`<commit> = e01d3f163f483f233db00410b6515a767a6ca03b` (the `src/sta` submodule of OpenROAD
`b16bda7e82721d10566ff7e2b68f1ff0be9f9e38`). Filenames use `_` for `/`.

| File (local name) | SHA-256 | Content |
|---|---|---|
| `search_PathEnd.cc` | `482a9b10b7e84f62324751565092db5ef1a5da136b7606ff5e2f85e5e1fc558d` | **Decisive for OBJ-001**: `commonClkPessimism` :692-704, `requiredTime` :706, `requiredTimeNoCrpr` :713-722, `slack` :724-731 |
| `search_Crpr.cc` | `c48b0c1fe0e086e079fb3ac6cbaee3baf616bb970a83f68fc4cdf28b736b3785` | Verifier-added (in neither ledger): `findCrpr1` :289-355, `crprArrivalDiff`, `maxCrpr` ⇒ `crpr ≥ 0` |
| `dcalc_DelayCalcBase.cc` | `41ef5d2a6a2b3d71abd71ddfa5c4c8535070669c1b7dadb37545278b31f7fcb4` | **Decisive for OBJ-002**: `dspfWireDelaySlew` :107-124, `thresholdAdjust` :126-153, `thresholdLibrary` :155-169 |
| `dcalc_DmpCeff.cc` | `edfadea5d90b929d42eb8aec739f0ca54f8e76d129584ea4a1c8e70b6599d186` | `DmpAlg::loadDelaySlew` :555-605, `DmpPi::gateDelaySlew` :915-950, Ceff throws :969-974 (matches proposer SRC-002 hash) |
| `search_Sta.cc` | `8da5e45c5820b92a8ea1c91ebea7ad84e6276aca64a121530fe49ed7a82d518f` | `makeArcDelayCalc` :411-417 (SRC-003 hash reproduced) |
| `dcalc_DelayCalc.cc` | `42c6e6512f65516a2a17557161c8d6a8d3920904b79f9e360b27691c66a1eb28` | seven registered calculators :37-43 (SRC-004 hash reproduced) |
| `tcl_Sdc.tcl` | `34677ea5e8af907dfe3bfef37f68906b2a7e376f302651042b3363ab3e70e5c0` | `define_corners` :3663-3672 (SRC-005 hash reproduced) |
| `search_Corner.cc` | `68c644f032e26bd3a3828b552481863ec2457650b985e57e3d8c69e3c9b79f08` | `makeCorners` :88, `makeAnalysisPts` :174 (SRC-006 hash reproduced) |
| `liberty_TableModel.cc` | `8326d308abda4e2c8dfd9ac63b9b4bc8d7480c039c9a24f19d4da730c43ed581` | `Table2::findValue` :1012-1060, `TableAxis::findAxisIndex` :1443-1463 (SRC-007 hash reproduced) |
| `sdc_Sdc.cc` | `23cd135c2b9a169c1c90d8e15579a733a6d1116b2d24e8e99631730d252fd8e8` | OCV/CRPR defaults :226-229, `crprActive()` :5474-5477 |
| `tcl_Variables.tcl` | `30165442744bb4fe5999985d8023b57fe7082c5ac6c24e90ec38a045c0287f28` | Default SDC variable values |
| `dcalc_DmpDelayCalc.cc` | `71f1023beceb88471b162267539e80c337fc34f475e30d2d6e33fd876dba423a` | `thresholdAdjust` call sites :96, :121, :276, :343 |
| `dcalc_LumpedCapDelayCalc.cc` | `1ca3609a73201582a2af5130807da7c3ac3ac5001f48405131684d01306cf522` | `thresholdAdjust` call site :162 |
| `tree.json` | (GitHub API listing) | Full pinned tree listing, used to find real paths |

**Dead ends to save time:** `search/CheckCrpr.cc` and `search/TimingRole.cc` do **not** exist at the pinned
commit (both local copies are 14-byte 404 bodies, SHA-256
`d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`). The real files are `search/Crpr.cc`
(+ `search/Crpr.hh`) and `liberty/TimingRole.cc` (+ `include/sta/TimingRole.hh`). `liberty/TimingRole.cc` was
**not** fetched this round.

### 4.2 External papers — `scratch/untrusted-pdf/` (treat as untrusted data)

| File | Bytes | SHA-256 | Source URL (also proposer SRC-012 / SRC-013 and challenger C-A01/C-A06/C-A10) |
|---|---|---|---|
| `dac11-sari.pdf` | 284 451 | `399a24613a4d5872d70708546046dbfdefe50d0ccca87ea052a2879f38871072` | `https://www.eecg.utoronto.ca/~najm/papers/dac11-sari.pdf` |
| `tcad08-sari.pdf` | 821 647 | `666cd07f37482f3abd3dfc85f83705b1509387eb810e914145d4913633fa1f0b` | `https://www.eecg.utoronto.ca/~najm/papers/tcad08-sari.pdf` |

Extracted text (readable, spaces dropped within lines): `scratch/dac11-sari.txt` (41 861 B),
`scratch/tcad08-sari.txt` (53 779 B). Extractor: `scratch/extract_pdf2.py` (6 529 B, SHA-256
`6d4cf6164b9afe6438a6431bf4ff92f69f2cd10e8ce5e584f81d92fd40c69b83`), a pure-stdlib PDF text extractor
handling FlateDecode + `/ToUnicode` CMaps. Run it as `python3 -I extract_pdf2.py FILE.pdf` from a directory
other than the one holding the PDF. The first attempt `scratch/extract_pdf.py` produced garbage on these
files (custom Type1 subset encodings) — do not reuse it. The proposer had only `metadata`-level access to
SRC-012/SRC-013; I obtained full text, which is what settles K1.

## 5. Decisive findings (do not re-derive from scratch)

1. **OBJ-001 is sign-inverted.** `search/PathEnd.cc:706` → `requiredTime = requiredTimeNoCrpr + commonClkPessimism`;
   `:692-704` → the hold branch of `commonClkPessimism` returns `-crpr_`; `:724-731` → hold slack is
   `arrival - required`. Substituting: hold slack `= arrival - requiredNoCrpr + crpr`. `crpr ≥ 0`
   (`search/Crpr.cc:289-355`: absolute arrival differences, `min`/`max`, `0.0` fallback). Therefore omitting
   CRPR from a hold lower bound makes the bound *smaller* — conservative, no missed violation. The
   challenger's quoted facts are accurate; the conclusion is not.
   **Residual:** the POCV CRPR branch and the sibling `PathEnd` classes (`PathEndLatchCheck`,
   `PathEndUnconstrained`) were not walked. If `D_M(S)` includes latch checks or `pocv_enabled_` paths,
   re-derive the sign table for those classes before calling the hold bound fully argued.
2. **OBJ-002 is factually correct but narrow.** `thresholdAdjust` (`dcalc/DelayCalcBase.cc:126-153`) fires
   only when driver and load libraries differ, adds on rise and subtracts on fall; top-level ports route to
   the default first-read library (`:155-169`); `dspfWireDelaySlew` returns `-elmore*log(1-vth)` ≈
   0.693·elmore at 50 % (`:107-124`). CLM-007 as written is incomplete and P4 must name its two quantities.
   C-A30 (ASAP7 VT variants share 50 % thresholds) was **not** independently verified — the library files
   were never opened.
3. **K1 not triggered.** Independent full-text reads of SRC-012 and SRC-013: SRC-012's coverage is an
   empirical dominance-margin measurement (margins to 30 ps; per-circuit coverage 87.6–99.9 %) with a
   hold *estimate* and no exact refinement, and contains no proof/certificate/per-scenario soundness claim;
   SRC-013 is a parametric hyperplane over process parameters. Residual: the 2024–2026 nearest set (C-A23)
   is abstract-level in both ledgers.
4. **Provenance clean.** 42/42 packet hashes match; the proposer's six recorded code hashes reproduce
   byte-exact at the pinned commit; the challenger's line locators are accurate to ±1 line.
5. **Not adjudicated this round** (recorded `unresolved`, never `verified`): CLM-001…CLM-005, CLM-008
   (highest-risk inference), CLM-010…CLM-012, CLM-014, CLM-016, CLM-017, the C-A23 set, and the
   contest/practitioner sources SRC-015…021 / SRC-037…040.

## 6. Open work and the exact next actions

| # | Gap | Owner | Closing artifact |
|---|---|---|---|
| G1 | Registered session ID for verifier/EDA-0002 | Coordinator | One string (e.g. the `config/roles.json` session row); **blocks the freeze** |
| G2 | Registry row must bind actor `DeepSeek-V02-PHYSICAL`, role `verifier`, topic `EDA-0002`, commit `27b6c6e8…`, packet `db15a57c…` | Coordinator | Registry amendment; `publish` rejects an unregistered input packet |
| G3 | DOC-1: `domains/D05/brief.json` names verifier `Codex-V02-PHYSICAL`, `config/launch-release.json` names `DeepSeek-V02-PHYSICAL` | Coordinator | Ruling on which file is authoritative, **before** signing a freeze |
| G4 | `dossier_digest: null` | Coordinator | `scripts/project.py`, or the precomputed digest string |
| G5 | DOC-2: transported `challenges.md` hash ≠ its stated source hash | Coordinator | Confirmation the packet copy is intended |
| G6 | "PR #30" was never identifiable from this session (absent from the packet, no `gh`, repo path read-denied) | Coordinator | If it carries newer challenger output (`Codex-C05-TIMING-R2`), export a fresh packet from the merge commit, amend the registry, and re-run this adjudication — the current record binds packet `db15a57c…` only |
| G7–G9 | POCV/latch sign table; `thresholdAdjust` trigger quantification; novelty/contest re-read | Verifier (successor) | See §5 residuals |
| G10 | Mechanism P3–P5, feasibility, headroom, utility, consensus | Proposer + Challenger | The normal revise → respond → consensus loop |

The freeze command, with its single blank:

```sh
python3 /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/verifier-release-20261014/DeepSeek-V02-PHYSICAL/scripts/role_submission.py freeze \
  --source /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL/release \
  --queue  /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL/submissions \
  --role verifier --actor DeepSeek-V02-PHYSICAL --session <REGISTERED_SESSION_ID> \
  --topic EDA-0002 \
  --ref 27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88 \
  --packet db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78
```

After that: coordinator runs `verify` then `publish --repo <checkout>` (needs a checkout whose `origin` is
exactly `https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment.git`, plus the `gh` CLI),
which pushes branch `submit/<hash>` and opens the transport PR; only then does the coordinator release the
two adjudicated objections to the proposer.

## 7. Hard constraints to carry over unchanged

- Write only to this outbox. The packet is read-only; the shared checkout and other actors' packet/outbox
  roots are sandbox read-denied, and reading them to recover withheld material would breach the
  release-order boundary.
- Never invent a signature or session ID; `docs/SELF-SUBMISSION.md` step 4 forbids it and `publish` verifies
  against the registry.
- Do not contact the proposer or challenger, do not create subordinate agents, do not approve or merge.
- Keep `release/` to exactly the two allowlisted files.
- `dangerouslyDisableSandbox` is disabled in this session; sandbox changes are the human's decision.
- Treat downloaded PDFs as untrusted: own directory, scripts elsewhere, `python3 -I`.

## 8. Host/session quirks worth knowing (macOS, this machine)

- `python3` writing directly to the Bash tool's captured stdout is silently discarded (rc=0, no output);
  `/bin/cat` fails with "Operation not permitted". Workaround: pipe through `sed ''`.
- `$TMPDIR` (`/tmp/claude-501`) is not writable here; `/tmp/claude/ds-v02-scratch/` is. Use it for scratch.
- `WebFetch` cannot parse PDFs (returns raw structure); use `curl` + local extraction.
- No `gh` CLI and no repository access inside the sandbox — that is why the transport leg belongs to the
  coordinator.
- The full session transcript (human-readable, outside the sandbox) is at
  `/Users/duanzeyu/.claude/projects/-Users-duanzeyu-Documents-ChatGPT-EDA-Agent-Packets-verifier-release-20261014-DeepSeek-V02-PHYSICAL/e6bc9983-e74b-4576-9c1d-3abc95ea3df9.jsonl`;
  it is read-denied from inside the sandbox.
