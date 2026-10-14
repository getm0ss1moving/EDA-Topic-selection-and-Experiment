# External review findings on PR #23 — recorded, not adjudicated

Source: automated review by the `chatgpt-codex-connector[bot]` GitHub App on PR #23, submitted 2026-10-13T18:01Z against head `fa926740ddcb9c7c74711621a0362501e565509d`. PR chat is not admissible project evidence until copied into versioned files; this record performs that copy. It changes nothing in the transported challenge content, and it is not a scientific act by any project role.

## Finding 1 (bot-labeled P1) — `candidates/EDA-0002/challenges.md`: "Correct the inverted hold-CRPR algebra"

Claim (paraphrased; full text is retrievable from the PR review comment): for hold checks with `crpr > 0` the bot derives `slack = slackNoCrpr + crpr`, concludes CRPR **increases** hold slack, and states that OBJ-001, its inferential bridge, F-8/C-A15 and the verifier brief all propagate a reversed sign; it recommends withdrawing or recomputing OBJ-001 before adjudication.

Disposition: unadjudicated outside allegation, kept for the verifier. It contradicts the challenger's source-located reading of the pinned engine (`search/PathEnd.cc:691-710` returns `-crpr` for hold; `sdc/Sdc.cc:226-229` shows OCV+CRPR defaults) and the submission packet's decisive test (a minutes-scale reference hold `report_checks` diff with `set_crpr_enabled false`, plus a static check that the pilot flows leave the defaults in place). Under `docs/CHARTER.md`, an assertion by any party — including an automated review — is not a verdict. The sign question is decidable by that test and by reading the pinned code; both belong to the verifier's claim-level adjudication. No text was changed.

## Finding 2 (bot-labeled P2) — `candidates/EDA-0002/sources-challenger.json`: "Give each swept work its own traceable source record"

Claim: C-A23 aggregates nine works into one record without per-work URLs/DOIs, publication dates, retrieval routes and precise locators, weakening the traceability the novelty conclusion depends on.

Disposition: recorded for the verifier's evidence-quality weighing. The file belongs to the challenger; per `harness/CHALLENGER.md` item 12, corrections flow through the adjudication loop, where the verifier can require per-work records (as a finding or as a source-format repair). No text was changed.

## Notes

- The bot is not a project actor; these findings were neither requested nor reviewed by any role, proposer, challenger or verifier. They are preserved so downstream review can weigh them without relying on PR chat.
- Both PR threads were resolved after this recording — meaning "addressed by recording into versioned files", not "accepted" and not "refuted".
