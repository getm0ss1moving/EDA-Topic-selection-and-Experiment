# Verification

**EDA-0002, round-1 challenge adjudication** (round 0 dossier `submitted`, round-1 challenge filed by
`DeepSeek-C05-TIMING`). Scope of this release: every filed objection adjudicated against the pinned
original sources, plus the decision-critical claims I could re-open in this round. Claims not touched
here are recorded as unresolved, not as verified.

## Reviewer identity and independence

| Input / identity | Value |
|---|---|
| Verifier actor | `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`), role verifier, domains D04/D05 |
| Session | host-observed `e6bc9983-e74b-4576-9c1d-3abc95ea3df9`; the registry (`config/roles.json`) is not exported in the packet, so registration is a coordinator check. If the registry value differs, replace this field before transport. |
| Independence | Fresh session, packet-only scientific inputs, no other-role private material read. **Disclosure:** the round-1 objections were authored by an actor on the verifier's own platform (`DeepSeek-C05-TIMING`, session `af136556-…`, a distinct registered session); I authored neither. Same-platform review is a diversity limitation. The challenger seat has since passed to `Codex-C05-TIMING-R2` (`config/launch-release.json` role_handoffs). |
| Model / effort | host-declared `deepseek-flash`, low effort; not independently verifiable from inside the session |
| I did not | propose the topic, author either objection, inspect private reasoning, converse across roles, approve, merge, or freeze-as-approval |

## Input commits and packet provenance

| Item | Value |
|---|---|
| Topic, revision, dossier digest | EDA-0002, round-0 submitted revision, frozen dossier in packet `db15a57c…`. **Dossier digest not computed**: `scripts/project.py` is not exported in this packet. This is required for an `accept_for_pilot` record and for consensus checks; it is not required for this `revise` record. |
| Packet hash | `db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78` — recomputed from `PACKET.json` bytes, matches the assigned identifier |
| Input commit | `27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88` (not a git checkout; the packet is a read-only export) |
| File hashes | 42/42 listed files verified, 0 mismatches, 0 missing; no unlisted files except `PACKET.json` itself; no symlinks |
| External sources re-opened | OpenSTA tree at pinned `e01d3f163f483f233db00410b6515a767a6ca03b` (14 files fetched, SHA-256 recorded); `dac11-sari.pdf` (SRC-012, 6 pp., SHA-256 `399a24613a4d5872d70708546046dbfdefe50d0ccca87ea052a2879f38871072`); `tcad08-sari.pdf` (SRC-013, SHA-256 `666cd07f37482f3abd3dfc85f83705b1509387eb810e914145d4913633fa1f0b`). Both PDFs were text-extracted locally through their ToUnicode CMaps. |
| Provenance finding | The proposer's six recorded code hashes recompute exactly at the pinned commit (SRC-002 `edfadea5…`, SRC-003 `8da5e45c…`, SRC-004 `42c6e651…`, SRC-005 `34677ea5…`, SRC-006 `68c644f0…`, SRC-007 `8326d308…`), and the challenger's line locators are accurate to ±1 line throughout. No contamination or tampering found; the DOC-1/DOC-2 items in `readiness.json` are documentary and open. |

## Source identity, locator, entailment, and applicability checks

| Claim / objection | Source ID and exact locator | Verdict | Blocks advancement? | Reason / required action |
|---|---|---|---|---|
| **OBJ-001** — "hold certificate omits CRPR and CRPR *reduces* hold slack; 'CRPR only adds slack' is false for hold" | C-A15 and my re-read: `search/PathEnd.cc:692-711` (`commonClkPessimism` returns `−crpr_` for `genericRole()==hold`), `:724-731` (`slack` = `arrival − required` for hold), `sdc/Sdc.cc:226-229` + `:5474-5477` (OCV + CRPR enabled by default); verifier-added `search/Crpr.cc:289-350` (`findCrpr1`/`crprArrivalDiff` return `abs(…)`/`min` ⇒ `crpr ≥ 0`) | **refuted** | no | The quoted code facts are accurate, but the entailment is inverted. Hold slack is `arrival − required`, and `required = requiredTimeNoCrpr + commonClkPessimism`; with the hold branch returning `−crpr`, hold slack becomes `arrival − requiredNoCrpr + crpr` — CRPR **raises** hold slack by `crpr ≥ 0`, exactly as for setup. Omitting the term makes the certificate's lower bound *smaller*: conservative, not unsound. The alleged hole (missed hold violations in `[−crpr, 0)`, inexact hold TNS) does not exist. Action: close the objection; optionally adopt suggestion S-1 (per-term sign table) as an EXP-002 convenience, not a defect fix. |
| **OBJ-002** — CLM-007 hides `thresholdAdjust`; P4's Elmore bound is not established for the returned quantity | C-A16 and my re-read: `dcalc/DelayCalcBase.cc:126-153` (`load_delay ± load_slew·(load_vth−drvr_vth)/drvr_slew_delta`, applied only when `load_library != drvr_library`), `:155-169` (top-level ports resolve to the default library), `:107-124` (`wire_delay = −elmore·ln(1−vth)`, ≈0.693·elmore at 50 %); call sites `dcalc/DmpDelayCalc.cc:96,121,276,343`, `dcalc/LumpedCapDelayCalc.cc:162`; `dcalc/DmpCeff.cc:569-570`; narrowing evidence C-A30 | **partially_valid** | no | Every quoted line verified. As written, CLM-007 is an incomplete OBS claim and P4 is an obligation between two *unnamed* quantities (crossing vs returned delay plus port formula). However, the practical trigger is narrow — it needs a driver/load library pair whose threshold attributes differ, or input-port arcs in the decision set — and C-A30 shows the planned ASAP7 VT variants share 50 % thresholds. Cure is a wording amendment plus audit-scope extension, not a mechanism change. Required action: amend CLM-007; restate P4 with the `thresholdAdjust` term and the port formula; add both to EXP-002's audit list with a per-corner enumeration of driver/load library pairs and an explicit port-arc inclusion rule. |
| CLM-007 (wire-delay description, as written) | SRC-002 `dcalc/DmpCeff.cc:555-605`, `:915-948`, `:969-974`; SRC-007 `liberty/TableModel.cc:1012-1060`, `:1443-1463` | **partially_valid** | no | The described `DmpAlg`/`DmpPi` behaviour is confirmed at the cited lines (including the `slew = table_slew` fallback and the `Ceff ∈ [0, c1+c2]` throw conditions). Incomplete per OBJ-002 for the two paths above. Proposer's own status labels (P1 "3-D tables not inspected", P2 "DmpCap/DmpZeroC2/LumpedCap still need checking") are accurate. |
| CLM-006 (pinned engine facts) | SRC-003 `search/Sta.cc:411,417`; SRC-004 `dcalc/DelayCalc.cc:37-43`; SRC-005 `tcl/Sdc.tcl:3663-3672`; SRC-006 `search/Corner.cc:88,174` | **valid** | no | Verified line-for-line at the pinned commit: default calculator `dmp_ceff_elmore`, seven registered calculators, `define_corners` before `read_liberty`, all corners in one run via `Corners::makeAnalysisPts`. |
| CLM-015 and kill criterion **K1** (novelty not established; nearest work SRC-012) | SRC-012 `dac11-sari.pdf` full text read independently by me; SRC-013 `tcad08-sari.pdf` | **valid** as a self-assessment; K1 **not triggered** | no | My own read of SRC-012: setup coverage is an empirical dominance-margin measurement (worst-case slack "expected to occur" at max-arrival corners; margins to 30 ps; per-circuit coverage 87.6–99.9 %), hold is an anchor-corner plus clock-only partial-run **estimate** with error term Eq. (11) and no exact refinement or fallback; the paper itself states a hold-bounding corner set "has to include a large number of corners". No proof, certificate or per-scenario soundness language appears. SRC-013 is a parametric hyperplane method over process parameters. Neither source already provides the proposal's certificate-plus-exact-refinement guarantee, so the anchor survives. Residual risk recorded: the 2024–2026 nearest set (C-A23) is abstract/summary-level in both ledgers and I did not re-open it this round. |
| CLM-009 / P1–P6 (decision equivalence via sound bounds) | Proposal § Soundness properties; SRC-002, SRC-007 | **unresolved** | yes (at acceptance; not this round's objections) | P3–P5 are "not established" by the proposer and P4 is now additionally qualified by OBJ-002; P1/P2 rest on partial code paths. EXP-002 is the right vehicle and the K2 kill criterion already covers failure. Until then the mechanism gate stays closed. |
| Forecast labelling | `forecast.json` | **valid** | no | Values are null with an explicit calibration plan after EXP-003; the metric, unit, direction and guardrails are stated; nothing measured is presented as a result. Thresholds and M are labelled provisional. |
| Direction integrity | `direction-control.json` vs `proposal.md` | **valid** | no | Anchor frozen, `forbidden_pivots` enumerated, penalties `combination_drift 0 + demand_drift 0 = 0`; no response revision exists yet, so no drift can have occurred. |

**Claims not adjudicated in this round** (recorded as unresolved, not as verified): CLM-001…CLM-005 and
CLM-014 (vendor/practitioner and contest sources; the challenger's ledger and my spot reads are
consistent but I did not re-open SRC-015…SRC-021, SRC-037…SRC-040), CLM-010…CLM-012 (hypotheses),
CLM-013 (resource self-report accepted as an accurate admission, which is why feasibility stays false),
CLM-016, CLM-017, and the C-A23 2024–2026 set. Access limits: nothing decision-critical was found
paywalled in this round; the residual items above are budget-scoped, not access-blocked.

## Response verification

None. This is the round-0 dossier and `responses.md` is correctly empty: per `docs/WORKFLOW.md` step 4,
no objection is established until adjudicated, and responses follow the release of this adjudication.
`experiment-consensus.json` remains `pending` with null consents, and the task list still carries the
empty "Challenger additions (pending)" section, so no consensus check is possible or claimed.

## Admission gates (six named gates plus direction integrity and experiment consensus)

| Gate | Result | Evidence / missing prerequisite |
|---|---|---|
| Novelty | false — not established (no adverse finding) | K1 not triggered by an independent full-text read of the nearest work (SRC-012, SRC-013); residual: 2024–2026 set not re-opened by me; the proposer's own CLM-015 says novelty is not established. |
| Mechanism | false | P3–P5 unresolved (highest risk P3); P4 additionally needs the `thresholdAdjust`/port terms; EXP-002 not run (not authorised). |
| Engineering utility | false — partially supported | Downstream need and decision set D_M(S) are specified and tied to the D05 metric; the 20 % threshold and M are provisional; OQ-3 (TNS/decision-set definition must match the reference tool) is open; practice claims not re-verified this round. |
| Contest originality | false — not re-checked this round | No contrary evidence; the challenger's closed sweep (F-6, F-11, C-A11/C-A12/C-A18…C-A21, C-A25) is credible but I did not re-open the contest sources in this round. |
| Headroom | false | No measurement; oracle-screen plan (EXP-003) is preregistered with stop rule K3/S3, but `experiment_authorization` is false and no range exists yet. |
| Feasibility | false | Proposer's own CLM-013: multi-corner libraries (with licence provenance), RC corners, designs and compute fit are unresolved; EXP-001 unexecuted; compute allocation not authorised. |
| Direction integrity and penalties | **true** | Anchor preserved, penalties 0 + 0 = 0, no revision yet. |
| Experiment consensus (both sessions, revision, task-list hash) | false | `status: pending`, no challenger additions, no consents, no task-list SHA-256; also the challenger session of record must be confirmed (DOC-1). |

## Decision, limitations, and reversal conditions

**Decision: `revise`.** Rationale: the round-1 challenge is adjudicated — one major objection is
**refuted** on the pinned code, one is **partially valid** and requires only a wording/audit-scope
amendment, and the novelty kill criterion is **not triggered**. No valid, unresolved, decision-critical
objection blocks the dossier. Advancement is nevertheless impossible now: mechanism (P3–P5),
feasibility, headroom, utility details, and experiment consensus are all open, and acceptance requires
zero penalties, all eight gates true, a current dossier digest and a dual-signed task list.

**Required of the proposer in the next revision round:** (1) amend CLM-007 and restate P4 with the
`thresholdAdjust` term, the port formula, and the per-corner library-pair/port-arc rule, adding both to
EXP-002's audit list; (2) respond to the adjudicated objections (OBJ-001 closed as refuted; OBJ-002
amendment); (3) keep the anchor unchanged — the round-1 outcome removes a claimed soundness hole and
weakens no other part of the mechanism; (4) refresh the novelty search before promotion (charter).

**Conditions for reversal:** I will revisit this decision toward `park` if K4 prerequisites (libraries
with verified licences, designs, RC corners, compute allocation) are shown unobtainable within the
pilot caps, and toward `accept_for_pilot` only if all eight gates become true with P3–P5 established or
soundly argued and accepted, the task list frozen with both consents, and the dossier digest recomputed
at the PR head. A later packet that changes the challenge material or the revision invalidates this
record; new evidence can reopen it.

**Limitations of this record:** dossier digest not computable in-packet (no `scripts/project.py`);
**self-freeze not performed** — `scripts/role_submission.py freeze` requires a registered `--session`,
and `publish` resolves it against `config/roles.json`, which is not exported in this packet; freezing
under the host-observed session ID would assert a registration this session cannot check and that the
publisher would reject, so these two files are delivered in `release/` for the coordinator to freeze
and publish, or for a re-run once the session ID and digest tool are supplied;
session registration pending coordinator confirmation; DOC-1 (role-of-record inconsistency between
`domains/D05/brief.json` and `config/launch-release.json`) and DOC-2 (transported `challenges.md` hash
differs from its stated source hash) remain open and are process questions, not verdicts; this release
binds to packet `db15a57c…` only.
