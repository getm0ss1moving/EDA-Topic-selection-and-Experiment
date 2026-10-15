# First-pass plan — verifier, EDA-0002 (D05)

**Actor:** `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`), verifier, domains D04/D05.
**Turn:** onboarding only. **No claim or objection below has been adjudicated.** Nothing here is an
approval, a novelty finding or a feasibility finding. Status of the dossier is `submitted`, round 0,
with a round-1 challenge filed; `verification.json` is a stub (`decision: pending`) and
`experiment-consensus.json` reads `status: pending` with null consents.
**Plan reference:** packet SHA-256 `db15a57c…`, input commit `27b6c6e8…` (both recomputed and confirmed
in `readiness.json`). All locators quoted below are copied from the packet; **none of the external
sources have been opened yet in this session.**

## 1. What the verification queue contains

| Artifact | Content relevant to me |
|---|---|
| `proposal.md` | Claim ledger CLM-001…CLM-017; mechanism "certify then refine"; soundness properties P1–P6; counter-hypotheses CH1–CH5; kill criteria K1–K6; unknowns U1–U9; constructed counterexample CLM-017 |
| `sources.json` | 52 records; access mix: 34 full, 17 metadata, 1 abstract. Decision-critical records at metadata level: SRC-012 (kill-criterion source), SRC-013, SRC-025–SRC-027, SRC-035, SRC-037, SRC-039, SRC-040, SRC-041, SRC-046–SRC-049 |
| `challenges.md` | **OBJ-001** (CRPR sign in the hold certificate), **OBJ-002** (`thresholdAdjust` / port wire-delay formula vs P4), open questions OQ-1…OQ-5, suggestions S-1…S-4, revision history round 1 |
| `findings-challenger.md` | F-1…F-15 supporting the two objections and closing the contest gate (F-6, F-11) |
| `sources-challenger.json` | 30 records C-A01…C-A30 incl. C-A13 (pinned tree, all eight proposer hashes recomputed), C-A14 (Elmore bound theorem), C-A15, C-A16, C-A30 |
| `search-log.md`, `search-log-challenger.md`, `prior-art.csv` (16 rows), `contest-audit.md`, `industry-gap.md` | Novelty-search coverage, contest originality, headroom framing |
| `experiment-plan.md` | H1–H3, D_M(S) definition, guardrails G1–G6, baselines B0–B5 + oracle O, ablations A1–A5, stopping rules S1–S4, preregistration state |
| `tasklist.md`, `experiment-consensus.json`, `direction-control.json`, `forecast.json`, `dossier.json`, `responses.md`, `verification.*` | EXP-001…EXP-009 with caps totalling 8 CPU-h; consensus pending; anchor with penalties 0/0; forecast deliberately null with a calibration plan; `responses.md` correctly empty at round 0 |

Not present in this packet: any D04/EDA-0001 dossier; `config/roles.json`; `config/agents-deepseek.json`;
`scripts/project.py`; `docs/TEAM-DEEPSEEK.md`; `runs/PHYSICAL-PILOT-0001`; the challenger's
`first-pass-plan.md` and the challenger's harness. Consequences in §8–§9.

## 2. Triage order (each stage bounded; later stages do not start while a stage's finding is undecided)

**T0 — Provenance and independence (minutes).**
Confirm packet hash, file hashes (done: 42/42), release order (proposal frozen before challenger
search; challenger estimate written before forecast exposure), three distinct sessions, and that the
filed objections are the ones I adjudicate. Check the two documentary items DOC-1/DOC-2 in
`readiness.json` with the coordinator. Nothing here is scientific; it gates whether an independence
claim may be made at all.

**T1 — OBJ-001 first (soundness of the hold certificate).** It is the only filed objection with a
major severity and it can invalidate CLM-009's decision-equivalence argument for a whole check type.
Its evidence is code-level and cheap to check: `search/PathEnd.cc:691-710` (sign flip on
`TimingRole::hold()`), `sdc/Sdc.cc:226-229` and `5474-5477` (OCV/CRPR defaults), `tcl/Variables.tcl:50-70`.
I will read the pinned files myself at `e01d3f163f483f233db00410b6515a767a6ca03b`, not the quotation.

**T2 — OBJ-002 second.** `dcalc/DelayCalcBase.cc:126-153` (`thresholdAdjust`, applied only when
driver and load libraries differ), `155-169` (top-level port default-library route), `dcalc/DmpCeff.cc:569-570`,
`dcalc/DmpDelayCalc.cc:96,121,276,343`, `dcalc/LumpedCapDelayCalc.cc:162`, and the port formula at
`DelayCalcBase.cc:107-124`. Then judge whether the objection's own narrowing (C-A30: ASAP7 LVT/RVT/SLVT
share identical 50% thresholds) makes it inert on the evaluations actually planned, which turns it
into a wording-and-audit-scope finding rather than a soundness finding.

**T3 — Positive decision-critical claims, most risky first.** CLM-008 (inference, marked high risk),
CLM-009 (logic), then the code-fact claims CLM-006/CLM-007 and the property statements P1–P6, then the
prior-art and limitation claims CLM-002/CLM-003/CLM-005 (nearest-work source SRC-012, access = metadata
for the proposer) and CLM-001/CLM-004 (vendor/practitioner practice), then CLM-013 (resources) and
CLM-014 (contest coverage). Verify favourable evidence as strictly as hostile evidence.

**T4 — Novelty and the kill criterion.** CLM-015's honest "novelty not established" plus K1. The
challenger reports a full-text read of SRC-012 and its 2008 companion (C-A01, C-A06, C-A10) and
concludes K1 is not triggered (F-1, F-2, F-10, F-12). K1 is a kill condition for the whole topic, so I
will re-check the decisive entailment myself from the papers' own text (or record the access limit),
not only from the challenger's summary.

**T5 — Gate-closing checks and integrity.** Evidence quality per gate; evaluation integrity
(equal-budget rule for B2–B4, leave-one-design-out calibration, no test-set tuning); oracle definition
(OQ-3, TNS definition must match the reference tool, not a reimplementation); forecast labelling and
calibration plan; direction integrity (anchor invariance, `forbidden_pivots`, penalties 0/0);
experiment consensus (structurally impossible to be `agreed` this round — no challenger additions, no
consents, no task-list hash).

**T6 — Decision.** `revise` / `park` / `reject` / `accept_for_pilot`, with reversal conditions. A
reasonable unresolved critical premise (P3–P5, K1, or OBJ-001 if it stands uncured) prevents
acceptance; a speculative low-impact concern does not.

## 3. Claim / source / locator check specification

For every row I will record: source ID, exact locator, version/commit or DOI, access level actually
achieved at check time, the entailment step (what the source states → what the claim asserts), and the
applicability step (same engine, same design family, same metric, same constraints).

| Class | Claims | What counts as `verified` | Automatic non-`verified` conditions |
|---|---|---|---|
| Code facts | CLM-006, CLM-007, and the code half of CLM-005/P1–P2 | I read the same file at the pinned commit and the quoted behaviour holds at the quoted lines | Locator drift, a different commit, or a paraphrase that omits a branch (exactly OBJ-002's complaint) |
| Inference | CLM-008, CLM-009, CLM-017, CLM-016 | Each premise has its own verified source row and the step is stated; a constructive counterexample is arithmetically checked | A premise resting on an abstract or metadata-only record; a missing assumption |
| Hypothesis/forecast | CLM-010…CLM-012, `forecast.json` | Correctly labelled as hypothesis; a preregistered endpoint exists; no measurement claimed | A forecast presented as evidence, or a null forecast without a resolution task (here: a plan exists) |
| Prior-art/limitation | CLM-001…CLM-005, CLM-014, CLM-015 | Primary text read at the locator, or the claim is explicitly degraded to what the access level supports | Vendor marketing used as a controlled comparison; abstract-only access cited as method inspection |
| Practice claims | CLM-004, CLM-001 | Statement about what practitioners/vendors say, at the stated locator | Any leap from "stated practice" to prevalence |
| Resource claims | CLM-013 | Matches `config/research-brief.json` and `config/physical-resources.lock.json` (both verified in-packet) | Licences asserted without a read |

Access rule: a source I cannot reach is `unresolved`, never `refuted` and never silently omitted.
Metadata- or abstract-only support cannot carry a decision-critical gate.

## 4. Objection adjudication protocol

Allowed verdicts: `valid`, `partially_valid`, `unsupported`, `refuted`, `unresolved`; plus a
`blocking` flag and a `resolution` state (`resolved` / `open`) per objection.

- **OBJ-001.** Check the quoted sign logic and the defaults it depends on. If the sign flip is as
  quoted and the default analysis is OCV with CRPR enabled, the objection is `valid`; the severity then
  depends on whether the evaluated flows keep those defaults and whether some hold check has
  `crpr > 0` — I will state explicitly that existence is a code fact while practical bite is a
  measurement planned in EXP-002/EXP-006, and grade the verdict accordingly. It is `blocking` while
  the guarantee claim (CLM-009) is asserted unamended.
- **OBJ-002.** Split into (i) the code facts, (ii) the P4 modelling obligation, (iii) the practical
  trigger. Expect `partially_valid` if (i) holds and (iii) is inert on the planned datasets; the audit
  obligation (P4 restated between two named quantities) stays open either way.
- Do not force the proposer to answer `unsupported` or non-blocking material; close it with a reason.
- Neither objection may be resolved by the verifier rewriting the proposal; the cure is the proposer's
  (or a joint-abandonment process if a ground exists).

## 5. Gate plan

| Gate | What I will require before it can be `true` | Current expectation |
|---|---|---|
| Novelty | Decision-critical nearest work verified at full text where the claim is decisive; documented two-expansion stop; K1 explicitly settled | Open — rests on SRC-012 full text (proposer access was metadata-only) |
| Mechanism | The certify-then-refine composition shown to be more than a composition: the certificate's soundness properties P1–P6 established or soundly argued, not assumed | Open — P3–P5 explicitly "not established" |
| Engineering utility | User, workflow stage, decision and threshold tied to D_M(S) with the 20% threshold's provenance labelled provisional; oracle equals reference-tool semantics | Partly supported; OQ-3 must be closed |
| Contest originality | Contest audit verified (F-6, F-11, C-A11/C-A12/C-A18–C-A21, C-A25); no organizer hint or winner approach presented as the contribution | Likely supported, to be spot-checked |
| Headroom | Oracle ceiling plan sound, scenario-set size honestly flagged as small, no theoretical-limit claim overreach | Open — depends on EXP-003, which is not authorized |
| Feasibility | Datasets, licences, RC corners, compute fit and correctness oracle identified; 8 CPU-h versus the planned 9 tasks assessed; authorisation state respected (`experiment_authorization: false`) | Open — CLM-013 is the proposer's own admission |
| Direction integrity | Anchor problem/user/need/mechanism unchanged by any response; penalties sum to their parts; `forbidden_pivots` respected | Currently 0/0 at round 0; no response exists yet |
| Experiment consensus | Byte-exact `tasklist.md` hash, both readiness fields true, open conditions empty, two distinct registered sessions with matching revision and hash | Cannot be true this round (`status: pending`, challenger additions missing) |

Evaluation-integrity checks (leakage, equal budget, seeds/splits, corner/PDK consistency) are folded
into the utility/feasibility rows and reported in the reason column; if the coordinator's machine
schema counts gates differently from the six-gate stub plus direction/consensus, I will follow the
schema and say so.

## 6. Domain queue separation and role boundaries

- This packet binds topic EDA-0002 (D05). The D04/EDA-0001 queue has no dossier here; I will not
  import D04 material, hypotheses or verdicts into D05, and I will not treat `domains/D04/*` content as
  evidence for anything in D05.
- Objections are adjudicated as filed. I cannot verify an objection I authored; I authored none. The
  round-1 objections come from `DeepSeek-C05-TIMING` (distinct registered session), and the challenger
  seat has since passed to `Codex-C05-TIMING-R2`. I will disclose the same-platform relationship in
  `verification.md` and treat any contested verdict as escalatable to a second verifier or the human.
- No contact with either scientific role; all communication is by released files. Only adjudicated
  objections are released back to the proposer — that release is a coordinator action, not mine.
- Forecast blindness applies to the challenger, not to me; I will still preserve release order and
  check that the challenger's pre-exposure estimate claim is not contradicted by in-packet evidence.

## 7. Escalation conditions

Escalate (state the question in the verification file and request an independent expert, a second
verifier or a human decision) when any of these holds:

1. A mathematical soundness question decides a gate and I cannot settle it by code reading and
   arithmetic — P1's table geometry, P3 (waveform-model slew bound), P4 (single-pole crossing vs
   Elmore-based theorem, C-A14), P5.
2. Contested engineering assumptions change the verdict — the definition of TNS/decision set (OQ-3),
   the reporting margin M, whether port arcs are in the decision set, the 20% threshold's status.
3. A decision-critical source remains inaccessible after independent attempts: SRC-012 legacy PDF and
   its companion, TAU 2018/2019/2021 material, IEEE/ACM paywalls, C-A24's snippet-only lead.
4. Any evidence of cross-role contamination, of a packet file changing, or of a session-registration
   mismatch (DOC-1/DOC-2).
5. Any request to treat a forecast, a vendor claim or an automated reviewer's assertion as evidence
   without adjudication.

## 8. Evidence required for a verdict

- Every row of `verification.md` carries source ID + exact locator + access level actually achieved +
  a one-line entailment statement; `verification.json` mirrors it with `source_checks`
  (`source_id`, `locator`, `verdict`, `checked_at`, entailment) and `objections`
  (`id`, `claim_id`, `verdict`, `blocking`, `resolution`, rationale).
- `accept_for_pilot` would require: all eight gates true, both drift penalties zero, three distinct
  registered sessions, a current dossier digest, experiment consensus agreed on a byte-exact task list,
  and no unresolved decision-critical premise. Conditions for reversal are stated per row.
- `revise` if a valid blocking objection exists and a cure is plausible under the same anchor;
  `park` if a prerequisite is unobtainable within the caps (K4); `reject` if a validated fatal flaw is
  not curable; `accept_for_pilot` only under the paragraph above. `verification.md` + `verification.json`
  are the only releasable files; they are self-frozen with `scripts/role_submission.py freeze`
  (allowlist confirmed: `{'verification.md','verification.json'}`).

## 9. Blockers and non-goals

**Blockers to record honestly rather than work around:** no `scripts/project.py` in the packet, so I
cannot compute the dossier or task-list digest myself (needed for `verification.json` and for any
consensus check) — I will request the tool or a supplied digest; no `config/roles.json` /
`config/agents-deepseek.json`, so registration and distinct-session checks rely on the coordinator;
`runs/PHYSICAL-PILOT-0001` absent, so pilot evidence is taken from the brief's summary only. Session
runtime limits observed this turn (python stdout capture and an unwritable TMPDIR) are logged in
`readiness.json`.

**Non-goals for the next turn:** no search-survey beyond the sources needed for a verdict; no
experiments, no tool installs, no container runs; no edits to the packet; no contact with the proposer
or challenger; no approval, merge or freeze-as-approval; no adjudication of anything not filed or
decision-critical.

**Stop condition for my own turn:** once `verification.md` and `verification.json` are written and
self-frozen, or once an escalation in §7 is raised, the turn ends with a short status message.
