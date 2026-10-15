# Gap analysis — from current state to a frozen verifier release delivered to the proposer

**Working note, not a release artifact.** The verifier release allowlist is exactly
`{verification.md, verification.json}` (`scripts/role_submission.py`, `FILES['verifier']`); this file must not
be placed in `release/` and must not be frozen. It records why the freeze and transport have not happened,
what is missing, and who owns each missing piece.

| Item | Value |
|---|---|
| Actor / role | `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`), verifier |
| Topic | EDA-0002 (D05, TIMING), round 0 dossier, round-1 challenge adjudicated |
| Session (host-observed) | `e6bc9983-e74b-4576-9c1d-3abc95ea3df9` — not a registered session ID; see G1 |
| Packet / commit | `db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78` / `27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88` |
| Frozen-candidate payload | `release/verification.md` = `1d1fa656e8bf273bb535498a216ea937fbcbe8f8469fb4708560c5762a0d8489` (14 219 B); `release/verification.json` = `b018b8c2a918275724c2ff58cf5fe739ebc00f55e1b6618afe5e9cd61b77853f` (10 398 B) |
| Written | 2026-10-14T11:17:20Z |

---

## 0. Target end-state vs. current state

The requested pipeline has four legs: accept the challenger's content → verify → freeze → deliver to the
proposer. Measured against the tooling actually present in the packet:

| Leg | End-state | Current state | Blocked? |
|---|---|---|---|
| 1. "Accept the challenger's content" | Both filed objections stand as valid | OBJ-001 `refuted`, OBJ-002 `partially_valid` | **Yes — substantively impossible as filed** |
| 2. "Verify" | Sources checked, verdicts recorded | Done for both objections + 5 decision-critical claims; 11 claims and 2 code paths explicitly left unresolved | **Partially — bounded by declared residuals** |
| 3. "Freeze" | `submissions/SUB-<sha256>/` with `SUBMISSION.json` | `release/` holds the two final files; nothing frozen | **Yes — exactly one missing input string (G1)** |
| 4. "Send to the proposer" | Proposer receives the adjudicated objections | No transport, no publish, no packet release | **Yes — not this role's leg, and unreachable from this session** |

Freezing does not mean accepting: `publish` writes the PR body text "Freeze is not scientific acceptance."
A frozen verifier release is a byte-bound record, not an approval. Even with every gap below closed, the
artifact is a `decision: revise` record, not an admission.

---

## 1. Gap A — "accept the challenger's content": substantive, not procedural

No process repair closes this gap. One of the two objections is arithmetically inverted, and the exact
three lines that would have to read differently for it to survive can be named.

To uphold **OBJ-001** ("CRPR reduces hold slack; therefore omitting CRPR from the hold certificate is
unsound"), at least one of the following must hold at OpenSTA
`e01d3f163f483f233db00410b6515a767a6ca03b`:

| # | Must hold | Actually reads | Result |
|---|---|---|---|
| a | `PathEndClkConstrained::requiredTime` returns `requiredTimeNoCrpr − commonClkPessimism` | `search/PathEnd.cc:706` → `requiredTimeNoCrpr(sta) + commonClkPessimism(sta)` | objection fails |
| b | hold slack is `required − arrival` | `search/PathEnd.cc:724-731` → `arrival − required` for the hold role | objection fails |
| c | the hold branch of `commonClkPessimism` returns `+crpr_` | `search/PathEnd.cc:692-704` → `return -crpr_;` for `genericRole() == TimingRole::hold()` | objection fails |
| d | `crpr` can be negative for hold (would revive the argument by another route) | non-POCV branch read: `search/Crpr.cc:289-355` (`findCrpr1`, `crprArrivalDiff`, `maxCrpr`) → `min`/`abs`/`0.0`, so `crpr ≥ 0` | **not inspected to the same depth — residual** |

With (a)+(b)+(c) as read, hold slack = `arrival − requiredNoCrpr + crpr`: the omitted term *raises* hold
slack, so a certificate omitting it produces a **lower** bound and cannot miss a hold violation at the 0
threshold. The alleged severity — "missed violations in `[−crpr, 0)`" — describes the opposite of the code.
The residual risk that a fair reading must state is (d) plus the sibling path-end classes: the sign table is
established for `PathEndClkConstrained`; the POCV CRPR branch and the latch/time-borrowing and unconstrained
classes (`PathEndLatchCheck`, `PathEndUnconstrained`) were **not** walked in this round. If `D_M(S)` includes
latch checks or `pocv_enabled_` paths, the per-term sign table must be re-derived for those classes before
the certificate's hold bound is fully argued. Bounded, closable — and recorded rather than hidden.

To uphold **OBJ-002** in full (`valid` instead of `partially_valid`), the missing evidence is scope, not code:

| Missing evidence | Why it matters | Where it comes from |
|---|---|---|
| An evaluated driver/load library pair whose `input_threshold_pct_*` / `output_threshold_pct_*` (or slew thresholds/derates) actually differ | `thresholdAdjust` (`dcalc/DelayCalcBase.cc:126-153`) fires only when `load_library != drvr_library`; if no planned pair differs, the term is identically zero on the planned evaluations | The actual `.lib` files of the planned libraries. C-A30 asserts ASAP7 LVT/RVT/SLVT share 50 % thresholds, but those files were **not** opened by me — that assertion is `unresolved` in the record |
| Whether input-port arcs are inside the decision set | At a top-level port `thresholdLibrary` returns the default (first-read) library (`dcalc/DelayCalcBase.cc:155-169`), and `dspfWireDelaySlew` returns `−elmore·ln(1−vth)` ≈ 0.693·elmore at 50 % (`:107-124`) — a different quantity from the Elmore crossing P4 reasons about | `proposal.md` / `experiment-plan.md` definition of `D_M(S)`; OQ-3 is already open on exactly this |

Summary: OBJ-001 cannot be accepted under any honest reading of the pinned source (its reversal condition is
a code fact to re-check, not a matter of interpretation); OBJ-002 is accepted as true but downgraded in
severity, and the evidence that would upgrade it is two concrete artifacts obtainable without a new packet.

---

## 2. Gap B — "verify": done vs. deliberately not done

| Bucket | Status |
|---|---|
| Both filed objections | Adjudicated with code locators, hashes and entailment steps |
| Code-fact claims CLM-006 / CLM-007 | CLM-006 `valid`; CLM-007 `partially_valid` (the OBJ-002 amendment) |
| Novelty kill criterion K1 | **Not triggered**; established by my own full-text read of SRC-012 and SRC-013 (downloaded, hashed, text-extracted locally) |
| Provenance | 42/42 packet hashes verified; the proposer's six recorded code hashes reproduce byte-exact at the pinned commit |
| CLM-008 (highest-risk inference), CLM-010…CLM-012, CLM-016, CLM-017 | **Not adjudicated this round** — recorded unresolved, never verified |
| CLM-001…CLM-005, CLM-014 (vendor/practitioner/contest sources SRC-015…021, SRC-037…040) | **Not re-opened** — `contest_originality` is `false` for "not re-checked", *not* because it failed |
| P1–P6 mechanism properties | `unresolved`; P3–P5 are "not established" by the proposer's own text, and P4 now additionally carries the OBJ-002 qualification |
| C-A23 (2024–2026 nearest-work set) | Abstract/summary level in both ledgers; residual novelty risk to refresh before promotion |
| D04 / EDA-0001 queue | Out of scope; no cross-domain import |

None of these is an access wall; they are budget-bounded. The verification gate for *this round* (both
objections adjudicated, decision recorded) is met. The verification gate for *acceptance* is not, and
structurally cannot be in this round: promotion additionally requires the eight gates, zero drift penalties,
a current dossier digest and a dual-signed experiment task list.

---

## 3. Gap C — "freeze": one string

`docs/SELF-SUBMISSION.md` authorizes self-freeze for all three roles ("This replaces earlier instructions
to wait for the owner/coordinator to freeze a dossier"), so authorization is **not** the blocker. Identity is:

```sh
python3 /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/verifier-release-20261014/DeepSeek-V02-PHYSICAL/scripts/role_submission.py freeze \
  --source /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL/release \
  --queue  /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/verifier-release-20261014/DeepSeek-V02-PHYSICAL/submissions \
  --role verifier --actor DeepSeek-V02-PHYSICAL --session <REGISTERED_SESSION_ID> \
  --topic EDA-0002 \
  --ref 27b6c6e8cb4ef0d2ac7f2feb2521be1426940d88 \
  --packet db15a57c6355808e0faf90a6b2954c7f632bbe5b80071f069a905701d262ec78
```

| Flag | Value | Have it? |
|---|---|---|
| `--source` | the `release/` dir, containing exactly the two allowlisted files | yes |
| `--queue` | `.../DeepSeek-V02-PHYSICAL/submissions` (outside `release/`, writable, no symlinks in any component) | yes |
| `--role` | `verifier` → allowlist `{verification.md, verification.json}`, both required | yes |
| `--actor` | `DeepSeek-V02-PHYSICAL` (from `PACKET.json` / `ASSIGNMENT.json`) | yes |
| `--session` | **the coordinator-registered topic/role session for EDA-0002 as verifier** | **NO** |
| `--topic` / `--ref` / `--packet` | `EDA-0002` / 40-hex commit / 64-hex packet | yes |
| Content validators | UTF-8, valid JSON, no credential-like text, size caps | yes — executed in memory, see §3.1 |

`--session` will not be filled with the host-observed runtime ID `e6bc9983-e74b-4576-9c1d-3abc95ea3df9`.
`publish` resolves the manifest against `origin/main:config/roles.json` and requires exactly one session
whose `session_id`, `actor_id`, `role` and `topic` all match, otherwise
`Release identity is not the registered topic/role session`. A runtime session ID is not a registration;
writing it into a signed `SUBMISSION.json` would be fabricating a registration, which
`docs/SELF-SUBMISSION.md` step 4 forbids ("Finish the assigned phase without inventing signatures").
The same blocker is recorded inside `verification.md` itself.

**Second, smaller freeze-side gap:** `dossier_digest` is `null`. `harness/VERIFIER.md` item 8 requires
`python3 scripts/project.py digest PATH_TO_DOSSIER` to be stored in `verification.json`; `scripts/project.py`
is not exported in the packet, so the digest cannot be computed here. A `revise` record does not need it for
acceptance, but the harness instruction stays unmet, and `publish` runs `project.py validate` in its
temporary clone, so the tool must exist coordinator-side regardless.

**Third, a live risk that would fail `publish` even with a correct session ID:** DOC-1.
`domains/D05/brief.json` still names the verifier of record as `Codex-V02-PHYSICAL`, while
`config/launch-release.json` names `DeepSeek-V02-PHYSICAL`. If the registry follows the brief, the identity
match fails. The registry holder must rule which file is authoritative **before** a freeze is signed, or the
freeze produces a `SUB-` directory that the transport rejects.

### 3.1 Pre-flight performed (no artifact written)

The packet's own validators were executed **in memory** against the release payload, with a placeholder
session string, and nothing was persisted:

- `validate_manifest`: OK — role-owned set `['verification.json', 'verification.md']` satisfied
- `check_content`: OK — UTF-8, JSON parses, no credential-like string
- payload 24 617 B; per-file cap 8 388 608 B; bundle cap 33 554 432 B
- **no `SUB-*` directory created, no `SUBMISSION.json` written, freeze not executed**

Conclusion: the payload passes every freeze-time validator; the only missing freeze input is the registered
session identity.

---

## 4. Gap D — "send it to the proposer": not this role's leg

| Aspect | Fact | Source |
|---|---|---|
| Who releases to the proposer | The **coordinator**: "Coordinator releases the verified challenge packet. Proposer writes `responses.md`…" | `docs/WORKFLOW.md` step 5 |
| What may be released | "Release only adjudicated objections back to the proposer." | `config/launch-release.json` (rule); `docs/PHYSICAL-PILOT.md` item 4 |
| Content condition | Satisfied — both filed objections are adjudicated, so the releaseable set is well-defined | `release/verification.md` |
| Transport chain | freeze → `verify` → `publish --repo <checkout>` → branch `submit/<hash>` → PR; `publish` requires a git checkout whose `origin` is exactly `https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment.git`, plus the `gh` CLI | `scripts/role_submission.py` `publish` |
| Reach from this session | No repository access (sandbox read-deny on the repo path), no `gh`, no credentials, no path to another actor; role isolation forbids contacting the proposer directly | session sandbox; `docs/ISOLATION.md` |

Leg 4 therefore has **zero gap attributable to this session's work**: the adjudication content, the
byte-bound record and the releaseable set are ready. What is missing is the freeze (one string), the publish
(coordinator; needs the registered identity and a registry that matches), and the packet-release step
(coordinator). After those, the proposer receives exactly two adjudicated objections and owes `responses.md`.

---

## 5. Consolidated gap list, by owner

| # | Gap | Owner | Exact artifact / action to close | Blocks freeze? |
|---|---|---|---|---|
| G1 | Registered session ID for verifier/EDA-0002 | Coordinator | One string (e.g. paste the `config/roles.json` session row for this topic) | **Yes** |
| G2 | Registry row must bind actor `DeepSeek-V02-PHYSICAL`, role `verifier`, topic `EDA-0002`, input commit `27b6c6e8…`, packet `db15a57c…` | Coordinator | Registry amendment; `publish` rejects an unregistered input packet — "register the amendment first" | **Yes (at publish)** |
| G3 | DOC-1: verifier/challenger of record ambiguous between `domains/D05/brief.json` and `config/launch-release.json` | Coordinator | A ruling on which file is authoritative | **Yes (at publish)** |
| G4 | `dossier_digest` null — `scripts/project.py` absent | Coordinator | Ship `scripts/project.py`, or supply the precomputed digest string | No (harness completeness) |
| G5 | DOC-2: transported `challenges.md` hash ≠ its stated source hash | Coordinator | Confirm the packet's copy is the intended file | No |
| G6 | If PR #30 carries newer challenger output (`Codex-C05-TIMING-R2`) | Coordinator | Fresh packet export from the merge commit + registry amendment naming the new commit/packet, then a re-run of this adjudication | **Yes (would supersede this record)** |
| G7 | POCV CRPR branch and latch/unconstrained path-end classes not inspected | Verifier (me) | Read `search/Crpr.cc` POCV path and the sibling `PathEnd` subclasses at the pinned commit; re-derive the hold sign table if `D_M(S)` includes them | No |
| G8 | OBJ-002 practical scope (`thresholdAdjust` trigger) unquantified | Me with data, or Proposer in EXP-002 | Planned libraries' threshold attributes, or the EXP-002 library-pair / port-arc audit specified in the record | No |
| G9 | C-A23 (2024–2026 nearest work) and SRC-015…021 / SRC-037…040 not re-opened | Verifier (me), next round | One bounded search/read pass; flips `novelty` / `contest_originality` off "not re-checked" | No |
| G10 | Mechanism P3–P5, feasibility, headroom, utility, experiment consensus | Proposer + Challenger + Coordinator | The normal revise → respond → consensus loop | No (next workflow round) |

**Absolute minimum to complete legs 1–3:** G1 (with G2, G3), plus G4 if the harness instruction is to be
satisfied literally. Everything else either strengthens the record or belongs to the next workflow round.

**Sequence once G1–G3 are supplied:** verifier runs `freeze` → `submissions/SUB-<sha256>/SUBMISSION.json`
binds actor, session, topic, commit `27b6c6e8…`, packet `db15a57c…` and both file hashes → coordinator runs
`verify` then `publish --repo <checkout>` → PR on `submit/<hash>` → merge → coordinator releases the two
adjudicated objections to the proposer → proposer writes `responses.md`, amends CLM-007 with the restated
P4, and adds the EXP-002 audit items (library-pair enumeration + port-arc rule).
