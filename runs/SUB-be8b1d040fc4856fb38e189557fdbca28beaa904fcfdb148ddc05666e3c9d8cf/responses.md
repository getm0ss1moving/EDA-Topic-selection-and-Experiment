# EDA-0005 round-2 response to verified review

Reviewed own release: SUB-5dc96f7c6ba6ea7f2d1cf5940be29d9cd08da069e1694ce3b7822e6c4f6e4243. Verifier release: SUB-13665529cc044fd6c0fbcc0952a154cf8a2bba4ae1d47ebd80ce3c1a0bd81011. Its exact adjudicated challenger release: SUB-5596d53194873abeed4cccdb0d140e212c4ec8bf398a28f1c76c16800085c45b. Literal current objection inventory: OBJ-001 only. Historical objections remain historical. No historical approval is inherited.

## OBJ-001 — accepted; operational ambiguity removed, positive distinction not established

Verifier verdict: valid, blocking. Accept the same-assumption reduction. B3 is now an equivalence/strongest-composition control. It receives the same action-conditioned table, full shared coverage and occupancy/connection predicates, candidate order, exact tie-breaks, realization oracle, failure policy and operation budget. No different generation/cache/schedule is claimed for C.

Side-by-side pseudocode (C-T01):

| Operation | C producer/selector | B3 ordinary monolithic composition |
|---|---|---|
| Candidate order | Descending common cheap score; ties by move IDs | Identical |
| Checkpoint / demands | Restore; apply full X; legalize; fresh GR/RC/min-max STA | Identical |
| Option generation | Full capped O(X), keyed to X and checkpoint; charge all work | Identical |
| Finite selection | Enumerate binary option masks; minimize area then option IDs under complete predicates | Ordinary subset enumeration with identical objective/ties |
| No table solution | Reject restricted X; no physical impossibility inference | Identical |
| Realization | Apply full compound edit; fresh whole-design guards; record failure/rollback | Identical |
| Incumbent / stop | Update only realized safe state; no cheap-score early-optimality claim; stop at any charged operation boundary | Identical |

Formal scope: if states match and the next operation and its deterministic output match, successor states match. Induct over operations. Therefore transcripts, evaluated prefixes, rejected candidates and realized incumbents match at all caps. Different internal enumeration order may affect solver timing on real hardware, but no timing advantage is established by a Python functional check. Identical finite optima without matched order/stops would not suffice. An eager all-table schedule may differ, yet the strong baseline is allowed the same schedule as C.

Five deterministic mock cases return the same incumbents: conflict AC/50, shared AB/55, nonconflict AB/55, compound failure BC/45, incompatible net split BC/45. The full common conflict trace begins:

```json
{"AB":["RESTORE","MOVE_LEGALIZE","GR_RC_MINMAX","GENERATE_OPTIONS:A,B","SELECT_TABLE:null","TABLE_REJECT"],"AC":["RESTORE","MOVE_LEGALIZE","GR_RC_MINMAX","GENERATE_OPTIONS:A,C","SELECT_TABLE:A,C","COMPOUND_REALIZE_GR_STA:pass","INCUMBENT:AC/50"],"first_differing_operation":null,"physical_tool_calls":0}
```

Full code and trace are in search-log.md. workflow.json stores the structured case ledger. Operation names denote deterministic mock events, not actual engine invocations. Unit credits merely enumerate stopping boundaries; they are not timing estimates. Each arm constructs 6 movement tables in this fixture. Conflict pruning saves one compound realization compared with a deliberately blind attempt, but saves no table-production calls and is equally available to B3. This exposes why a win over a naive rollout would not establish contribution.

Correction to CLM-009: do not claim superiority beyond identical B3. H1 remains an anchored, unresolved engineering question; the current implementation contrast supplies no distinguishing useful capability. No invented mechanism was attached to escape the objection. Request independent review of this negative outcome. It does not support universal impossibility, exhausted novelty or unilateral abandonment.

## C-T02 — same-assumption source matrix

| Source / exact locator | Movement / timing / resource model | Relation and remaining limit |
|---|---|---|
| S22 author manuscript §§2,3.4-3.5 pp.3-6 | Buffered interconnect, fixed non-repeater bin usage; maximum-path bounds; bin capacities | Resource coupling is prior. Subsequent simultaneous legalization is discussed. Candidate data-cell moves, individual repair sites and min-delay admission are not established equivalent by this formulation. |
| S14 Figure 2 description; claims 4-6,11 | Hold buffers can precede or guide incremental placement; routing reservation | B2 must include feedback from inserted buffers. A coarse reservation-only comparator would omit disclosed capability. No runtime or legal conclusion. |
| S13 §3.1 Eq.3 and §3.2 (own prior reading; not reopened) | Gate perturbation and buffer-hole occupancy | Movement/space coupling is prior; exact hold/engine contract still not established. |
| S23 official slides 10-15; diagrams 13-14 | Feasible padding positions first; setup/hold path relationships; cross-corner variables | Generic location-first planning and path coupling excluded from novelty. Concrete relocation/site/DR implementation not established by slides. |
| S27 author thesis Chapter 5 §§5.2.1,5.2.3.2-.3,5.2.5 pp.109-112,127-130,135-137 | Early/late critical moves, buffering positions, legal whitespace search, global-route feedback and rollback | Strong conventional repeated-lookahead context. Author identifies 2016 S11 antecedent; not asserted identical to exact article, nor a complete joint-site repair audit. |
| S12 publisher Abstract/Introduction/Section-4 summary | Evaluates transform footprints including legalization/routing disturbances | General demand corroborated, not candidate-specific incidence. Complete Algorithm 3 unavailable. |
| S17/S19/S26 official indices | Joint relocation/buffering task, post-placement contest, current FloorSet track | Winner algorithms still uninspected. NVIDIA paper endpoint returned a Git LFS pointer; never report it as paper access. |

S22/S23 full selected originals were genuinely recovered; unavailable source reading was not treated as novelty. S25 unofficial expansion is discovery-only and not evidence for formulas or gains. No copyrighted paper copies are in this release.

## Other verifier findings and C-T03

| Reviewed item | Action in coupled revision |
|---|---|
| CLM-003 / shared-load handling | Retain shared repair control; no endpoint-per-buffer straw model. |
| CLM-004 / need | Independently reopened S12 publisher preview. General side effects supported; representative conflict rate and meaningful threshold remain unknown. |
| CLM-007 / resource sharing | Replace abstract-only status with inspected author formulation and precise applicability limits. |
| CLM-009 / system delta | Negative equivalent-treatment trace above; no favorable claim asserted as verified. |
| CLM-010 / feasibility, CLM-013 / allocation | Keep all actual resource/oracle/rights gates. No physical/training/service/API execution or fabricated allocation. |
| CLM-011 / table scope | Finite matching checks passed, but no physical completeness/signoff extension. |
| CLM-012 / roadmap | Preserve future-under-consideration status; no claim 2027 contest ran. |
| CLM-015 / occupancy planning | Prior movement-to-buffer-hole coupling retained; no renaming as novelty. |
| C-T03 / safety and costs | Copy full existing-hold endpoint/slack-vector nonworsening guards into proposal, plan and tasklist; generation/checkpoint/failure/fallback work charged; keep evaluated-prefix logs. |
| Unreviewed CLM-001/014 context | Remain inherited/nonselected context, not current independent approval or selection-critical performance claims. |

## Direction, next action and consent

Same user, workflow, primary cell-movement intervention and complete joint physical repair interface. combination_drift=0, demand_drift=0: conceding unsupported advantage and adding no replacement mechanism is anchor-preserving. These scores do not override the negative contribution result. No experiment or abandonment signature. Further review should decide whether an evidenced useful anchored distinction remains; otherwise park through the normal scientific process. A different cache/scheduler/model or clock problem needs new direction review and, if scientifically different, a new topic ID. Do not spend a physical pilot merely to compare identical treatments.
