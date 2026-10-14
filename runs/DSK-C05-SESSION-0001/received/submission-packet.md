# Challenger submission packet (output packet)

**Actor:** `DeepSeek-C05-TIMING` (challenger, D05, EDA-0002). **Role harness:** `harness/CHALLENGER.md` item 12 — *"Submit `challenges.md`, task-list changes, consent and evidence updates through a PR/output packet."*
**Packet:** `e6c53f61…5332cf`, input commit `4b666c04…`. **Prepared:** 2026-10-14. **Status:** provisional — per item 12, nothing here blocks the proposer until a verifier adjudicates it.

## 1. Purpose

This is the round-1 challenge record for EDA-0002, packaged for transfer to the project's challenge channel, because the challenge content currently exists only in this actor's outbox while the repository copy is reported empty.

Context as reported by the owner on 2026-10-14 (not independently verified by this actor — no repository access from this sandbox): `candidates/EDA-0002/challenges.md` on main (`86fb60b3`) is still the empty template; there are no issues or PRs carrying challenges; the R2 challenger is told to wait for the dossier, and the dossier waits for the owner's freeze of the proposer's round-1 revision.

This actor has **not** written to any repository, opened no PR, signed nothing, and agreed to nothing.

## 2. Manifest — transfer these files (SHA-256)

| file (in this outbox) | sha256 | content |
|---|---|---|
| `challenges.md` | `b57953a2e5aab67677dacc2cd9caee3ce0edef58070f1a85588e29c03407e225` | **the submission text**: OBJ-001, OBJ-002, OQ-1…OQ-5, S-1…S-4 |
| `sources-challenger.json` | `d0d3d39d31efff63056c95bf589a51abc88c9529f6e2299631843e35869b420c` | 30 appended source records C-A01…C-A30 |
| `findings-challenger.md` | `658803fab83efa9d84fe4ff9ce016324e83f213528ede46714a33fb44a3c02ed` | findings F-1…F-15 + status |
| `search-log-challenger.md` | `2f9f561ed41d001561744ab3e8bc9583527844b4d515999ad6016258802ba8a0` | retrieval routes, failed routes, corrections |
| `readiness.json` | `cc3888e56f66002b8509a532540ccb02dd476fe3dce6a4f6af39047572930f1c` | identity / isolation record (round 0) |
| `first-pass-plan.md` | `dc3939f131e55ea7bd4bb74072f6c3f2c19a8bc1417b3986635a3daa681afaac` | pre-exposure plan (headroom prior) |

## 3. Transfer instruction (for whoever holds repository write access)

1. `challenges.md` is already written in the harness's objection format (targeted claim, severity, primary sources and locators, factual evidence, inferential bridge, confidence, conditions that invalidate, cheapest decisive test). If the repository template's section names differ, paste **OBJ-001 and OBJ-002 unchanged** into it and record this outbox hash as provenance.
2. Do not edit the objection text during transfer. This actor accepts corrections only through the adjudication loop (item 12).
3. The two objections are separated by classification in the file: OBJ-001 = major, fixable, soundness-relevant; OBJ-002 = minor as filed (its formerly "potentially major" branch narrowed by evidence update C-A30/F-15). Open questions and suggestions are marked as such and are not objections.

## 4. Verifier brief (what exists to adjudicate)

- **OBJ-001** — the hold certificate omits CRPR, and CRPR *reduces* hold slack in the pinned engine: `search/PathEnd.cc:691-710` returns `-crpr` for hold; `sdc/Sdc.cc:226-229` shows OCV + CRPR enabled by default. Decisive test (minutes, no implementation): on one evaluated design, run the reference hold `report_checks` with defaults and with `set_crpr_enabled false`; diff slacks; plus a static check that the pilot flows leave the defaults in place.
- **OBJ-002** — CLM-007 understates the returned wire delay (`thresholdAdjust`, `dcalc/DelayCalcBase.cc:126-153`; port formula `:107-124`), which bears on P4's bound. Decisive test (minutes): per-corner static scan of every Liberty file's input/output threshold pct attributes across libraries that can drive/load each other; the adjustment is live only where a mismatched pair exists or port arcs are in the decision set (this round's narrowing).
- **Locator spot-checks** (all in the pinned tree `e01d3f163f483f233db00410b6515a767a6ca03b`; all eight proposer-recorded hashes recomputed and matching): `search/PathEnd.cc:691-710`, `sdc/Sdc.cc:226-229`, `sdc/Sdc.cc:5474-5477`, `dcalc/DelayCalcBase.cc:126-153` and `:155-169`, `dcalc/DmpDelayCalc.cc:96/121/276/343`.
- **Fidelity caveats to respect when weighing findings**: F-12's SOTA sweep is abstract/summary-level and no open full text of the five closed 2025-26 works exists (verified negative, C-A28); C-A17 was read through an extraction proxy; ISPD 2026 single-corner/ideal-clock claims are primary-confirmed from the contest repository scripts (C-A27).

## 5. Sequencing notes (owner decisions — recorded, not requested)

1. **The freeze does not depend on this packet.** Harness item 12 gates *blocking*, not freezing: the proposer's round-1 revision can be frozen now and the objections adjudicated after. If instead the owner prefers a pre-freeze fix of OBJ-001 (a one-term amendment to the hold certificate taken from the exact clock pass), that is the proposer's and owner's call; it is not required by this actor.
2. **The succession record's chain is unchanged by this packet**: R2 challenger waits for the dossier; dossier waits for the freeze. This packet exists so the round-1 challenge content is neither lost nor needlessly re-derived when the dossier is assembled.
3. **Succession decision**: if the R2 challenger starts without this record, decide explicitly whether this outbox is (a) folded into the dossier, or (b) archived. Option (a) is recommended on the record only because F-8/F-9 (CRPR sign; `thresholdAdjust`) and OBJ-001/002 are source-located and cheap to adjudicate; re-derivation would repeat the retrieval work recorded in the search log.

## 6. Non-actions (this actor, restated for the record)

No repository writes, PRs, merges or approvals; no contact with other roles; no experiments (`experiment_authorization: false` in the launch config); writes only to this outbox.

---

*This file cannot contain its own hash (self-reference); its SHA-256 is recorded in `outbox-hashes.txt` alongside it. The §2 manifest hashes are unaffected by edits to this file.*
