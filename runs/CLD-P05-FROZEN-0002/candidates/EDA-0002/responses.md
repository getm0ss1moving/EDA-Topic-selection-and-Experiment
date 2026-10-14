# Responses

## Verified objection IDs and decisions

None. No challenge or verifier adjudication has been released to the proposer, and no verifier is assigned. Round 1 is a proposer revision made under owner decision CLD-LAB-0001 before any challenge. Per `docs/WORKFLOW.md` step 4, unadjudicated objections are allegations, and the proposer responds only to adjudicated ones.

Amendment 1b (below) takes in the challenger's *independent first pass*, on the human owner's instruction. That pass was written before any dossier was released and states that it issues no topic-specific objection. Its items are therefore treated as leads and proposed tests, not as objections, and none receives an OBJ ID here.

## Point-by-point response and changed claims

No adjudicated objections yet.

**Round-1b intake of the challenger's independent first pass.** Input: `runs/CDX-C05-INDEPENDENT-0001/` on branch `codex/challenger-initial-search`, commit `b7822234587292124a6d033167beb5f9d942e818`, by `Codex-C05-TIMING-R2`. The six files listed in its output manifest match their recorded SHA-256 values (`runs/CLD-P05-REVISION-0002/manifest.json`).

| Item | Challenger item (paraphrase) | Disposition | Changed |
|---|---|---|---|
| CF-01 | S01: classical parameterized timing removes paths while preserving the envelope, with sufficient versus exact pruning | **Adopted as a nearest-work lead.** Not read by the proposer, because its host is outside GitHub and arXiv. Certified elimination as such is conceded to be known. | SRC-066; CLM-026; `proposal.md` closest-work item 8 and `prior-art.csv`; K1 widened; U11 |
| CF-02 | S02: unified MCMM branch-and-bound engine (abstract) | Already SRC-014 (slides, full access). The DOI is added as challenger-reported metadata. A backward-citation pass on SRC-014's reference list then found SRC-068, which round 0 had missed. | SRC-014 note; SRC-068 |
| CF-03 | S03: exact worst-delay corner (text not retrieved) | **Adopted as a lead.** Cross-checked with SRC-014 slide 29 [9]. Unread by both roles. | SRC-067; U11; K1 |
| CF-04 | S04: matrix-filling prediction is a prediction lead, not a safe-elimination guarantee | Agrees with the existing treatment of SRC-025 (CLM-002; baseline B4 style). Venue and DOI added as challenger-reported metadata. | SRC-025 note |
| CF-05 | S05: incremental timing must be a cost baseline, not only complete reruns | **Adopted.** P is stated as a from-scratch method, consistent with the round-0 exclusion of slice S1. Incremental exact timing becomes baseline B6 in a preregistered edit loop. | CLM-029; CH8; U13; B6; EXP-007 (2) |
| CF-06 | Priority 1: fix which result is preserved | **Adopted.** D_M(S) is unchanged; the outputs it does not preserve are now listed. | `proposal.md` § Scope; `experiment-plan.md` § Primary metric |
| CF-07 | Priority 2: audit every discard certificate and every unresolved case; ranking prediction is not an acceptance rule | **Adopted.** The acceptance rule was already a bound, not a ranking. Guardrail G7 now audits every certificate against B0 with no tolerance, and a G7 failure counts even without a decision change. | G7; K7 extended; EXP-006 (4) |
| CF-08 | Priority 3: ranking reversals, near-boundary cases, setup and hold semantics, clock effects, invalidation after edits | **Adopted.** Checking this against the pinned code found two soundness gaps in R1: multicycle hold shifts (CLM-027) and float rounding (CLM-028). Both are closed by conservative rules, P8 and P9. Certificate validity after edits is stated. | CLM-027; CLM-028; P8; P9; CH9; EXP-002b (6)-(9); EXP-004 (1), (3) |
| CF-09 | Priority 4: compare exhaustive exact, incremental exact, naive screening plus fallback, and the nearest certified method at equal accounting | **Mostly adopted:** B0 and B1 (exhaustive), B6 (incremental, new), B2 to B5 (screens with fallback). **Not runnable:** the nearest certified method, because its papers are unread or need parametric models absent from open libraries. A2 is the closest runnable certified comparator, and the gap is reported as a limitation. | `experiment-plan.md` § Baselines |
| CF-10 | Priority 5: end-to-end costs and residual false exclusions; thresholds chosen with the owner before execution | **Adopted.** The accounting identity is a preregistered metric. False exclusions are G1 and G7. The thresholds remain as set by owner decision U9. | `proposal.md` § Mechanism; `experiment-plan.md` secondary metrics |
| CF-11 | Accounting identity: preprocessing + certificate construction + screening + refinement + update maintenance | **Adopted**, with T_maintain = a full re-run in v1. | `proposal.md` cost model |
| CF-12 | Headroom hypothesis: positive if certificates are cheap and stay valid after changes; no gain or a slowdown is equally plausible | Consistent with CH1, CH2, CH6 and CH8 and with the null forecast. No number is adopted or changed. | none |
| CF-13 | Engineering demand, commercial comparability and contest ideas are unresolved in the challenger's own search | Consistent with the dossier: demand rests on vendor and practitioner statements (U9), commercial internals are unknown, and the contest audit makes no global claim (CLM-014). | `industry-gap.md` round-1b note |
| CF-14 | Blocker: project validation not run by the challenger | For the coordinator. The proposer's own structural checks are recorded in its run manifest. | none |

## Evidence-backed disputes

None yet.

## New tests and remaining issues

No objection-driven tests yet. Round 1b adds proposer tests prompted by the challenger's first pass: EXP-002b steps (6) to (9), the EXP-003 exception census, guardrail G7 and the EXP-007 edit loop. Remaining issues added: U11 to U13. The round-1 changes come from the proposer's own owner-authorized property checks, not from objections: P3-P5 are falsified, K2 is activated, and the certificate is narrowed (`runs/CLD-P05-REVISION-0001/p3-p5-record.md`). The proposer's own known unknowns (U1-U13) and kill criteria (K1-K7) are listed in `proposal.md`. Task-list slots for the challenger's falsification tests are reserved in `tasklist.md` (§ Challenger additions).

## Revision history

| Round | Date (UTC) | Change |
|---|---|---|
| 0 | 2026-10-13 (recorded in round 0 as 2026-10-12, an erratum of the host clock offset) | Initial submission by `Claude-P05-TIMING` (session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`). Anchor frozen in `direction-control.json`. Both direction-drift penalties are 0. |
| 1 | 2026-10-14 | Proposer revision under owner decision CLD-LAB-0001, with no challenge received. The changes:<br>- P3-P5 checks on the pinned calculator through the lab runner: falsified (CLM-018 to CLM-020); K2 activated; the guarantee narrowed to R1 (CLM-021 to CLM-023); side effects recorded (CLM-024); P2 `DmpZeroC2` finding (CLM-025);<br>- owner answers U1-U9 applied;<br>- ADD-0001 evidence folded into the dossier, with SRC-012 held unresolved per U1;<br>- erratum E1 (+15 h) applied to the retrieval times.<br>Penalties: combination drift 1, demand drift 0 (`direction-control.json`). |
| 1b | 2026-10-14 | Pre-freeze amendment on the human owner's instruction (no verifier assigned), taking in the challenger's independent first pass (CF-01 to CF-14 above):<br>- leads SRC-066 to SRC-068 (K1 widened; CLM-026);<br>- preserved outputs listed;<br>- soundness rules P8 (exceptions) and P9 (rounding), from CLM-027 and CLM-028;<br>- certificate validity after edits; baseline B6 and the edit-loop comparison (CLM-029, CH8);<br>- guardrail G7; the accounting identity; CH9; U11 to U13.<br>No experiment or runner job. Penalties unchanged: combination drift 1, demand drift 0. Run `runs/CLD-P05-REVISION-0002/manifest.json`. |
