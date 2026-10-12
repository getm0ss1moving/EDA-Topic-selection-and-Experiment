# CLD-LAB-0001 governance decision

Decision date: 2026-10-13. Decision owner: `getm0ss1moving`. Coordinator: Codex. This record authorizes infrastructure setup and bounded method-soundness checks for `Claude-P05-TIMING`; it does not authorize hypothesis or performance experiments and it does not accept EDA-0002.

## Runner decision

The proposer may submit one job at a time through the file-mediated runner. Jobs are limited to `tooling`, `data`, `substrate`, and `property-check`. The permitted work in this round is tool and public-data setup plus checks of P3-P5 against the pinned `dmp_ceff_elmore` implementation. Any runtime, speedup, certifiable-fraction, band-width, or QoR experiment remains out of scope until the proposer and challenger agree on the frozen experiment task list.

The infrastructure ceiling is 300 core-hours across this actor's runner ledger, at most 8 cores and 12 hours per job. This is a safety ceiling, not a scientific allocation or a promise that all of it will be used. The runner rejects starts above 75% machine load or above the 60 GiB actor workspace cap. `lab234` has no network. `lab231` is the only network-capable execution host. The proposer-facing Claude session permits downloads only from GitHub and arXiv; every other WebFetch domain is denied without an approval prompt. Network-capable lab jobs must likewise be used only to obtain public GitHub or arXiv inputs and must record URLs, revisions and hashes.

The remote job sees `/ws` as its home and cannot see the SSH account's home. It inherits the requested CPU affinity, a 32 GiB virtual-memory limit and an enforced wall timeout. Returned files must be regular files below 50 MiB each and 200 MiB in aggregate. Symlinks and ineligible files are not copied back. Eligible results are hash-checked and published read-only. Large outputs remain in the actor's remote `/ws`; their paths, sizes and hashes appear in `result.json`, so a later authorized job can consume them without routing them through Claude's local Read tool.

## Owner answers to U1-U9

| ID | Decision for this round |
|---|---|
| U1 | Re-attempt acquisition of Onaissi et al. (DAC 2011) only through arXiv or GitHub. If the full text is not publicly available there, keep the assumptions unresolved; do not infer them from snippets or secondary summaries. |
| U2 | Authorized now as bounded `property-check` work. Set up the pinned implementation, construct adversarial and boundary fixtures, inspect the implementation, and check P3-P5. A proof-quality code argument may accompany tests, but tests alone cannot establish a universal claim. Withdraw or narrow the certificate if a property cannot be made sound. |
| U3 | Do not run the OpenSTA MCMM runtime breakdown in this round. Preserve it as a proposed experiment pending proposer/challenger task-list consensus. |
| U4 | Do not measure the oracle-certifiable fraction or bound-band widths on real designs in this round. Preserve the question and its preregistered measurements for the agreed experiment plan. |
| U5 | Acquire tools and data only from GitHub or arXiv, pin revisions and hashes, and verify every license from the repository itself. Exclude any library or design whose redistribution/use license or provenance remains unclear. |
| U6 | Prerequisite P&R generation is not authorized in this round and therefore has no pilot allocation yet. The 300 core-hour runner value is an infrastructure ceiling. P&R cost must be estimated and explicitly allocated in the jointly accepted experiment task list. |
| U7 | Static inspection and focused fixtures needed to evaluate P3-P5 are authorized. A full experiment on cone-restricted search, clock tags, CRPR and path groups is deferred until task-list consensus. Record any code-level side effect found now as a threat and a required falsification test. |
| U8 | Search GitHub and arXiv for primary records of the TAU 2018 and 2019 topics. If no primary record is available through those sources, keep both years unresolved and avoid the global claim that no relevant contest existed. |
| U9 | No practitioner evidence is supplied by this decision. Keep `M = 0 ps` as the primary reporting margin, retain 5% of the clock period only as a labelled sensitivity analysis, and mark the 20% threshold provisional. Challenger review or later practitioner evidence may revise these values before experiment consensus. |

## Gate after the proposer revision

The proposer must update the dossier, source and search records, the P3-P5 status, kill criteria and task list in English. It must distinguish proof, code-level argument, finite test evidence and unresolved assumptions. The revised dossier is then frozen by the human owner for a fresh DeepSeek challenger packet. No experiment starts until proposer and challenger independently sign the same exact task-list revision as reasonable.

