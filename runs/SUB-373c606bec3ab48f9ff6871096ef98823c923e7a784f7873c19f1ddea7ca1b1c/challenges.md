# EDA-0007 cycle-4 independent challenge

Reviewed proposer: SUB-e0cef865c5877d07c062554b61e073024cb0f6ed28b7ef45f31c19d7a5cb335a. Actor ChatGPT-C05-TIMING-EDA-0007; logical session f4cc281a-8e7a-4b97-b540-94824b0d44fb. Input f68c1492c05be3fac5622deac4bb479eabf957de; packet 064da980d2a3e2a4aea886f369745c5cd5c92c5a51c1e9fd9cc6d61cc5226cc6. Unblinded source-based assessment; no inherited scientific approval. Proposal prose, task list and sources/workflow were exposed, including provisional thresholds; forecast.json was not separately opened. No EDA experiment executed.

**Assessment: revise; park after this final scheduled cycle, without pilot selection or abandonment consent.** The electrical-feature covariance hypothesis is legitimate and may support a useful hybrid contribution. This release finds a specific one-step acquisition reduction, not a proof that useful covariance learning is impossible. The proposer already accurately declares utility/readiness unresolved. No absence of compute is used to deny research merit.

## OBJ-001 — The specified one-step measured-only regret acquisition reduces to constrained expected improvement

Target CLM-703 and proposal Controller and state interaction steps 2-4; EXP-004/006. Severity major, fixable formulation/attribution concern. Sources C03 Section 2.1 versus Section 3; C04 terminal selection formulation; exact current proposal is the primary specification. Confidence high under the assumptions below; interpretation uncertainty remains because “after each possible bundled observation” could conceal an unstated multi-step rollout.

**Own derivation, not a literature quotation.** Condition on current history H and let b be the known best feasible measured gain, including unchanged base. Let M be the latent best feasible gain over the fixed complete candidate set. Query q returns its deterministic gain and feasibility, so the new eligible incumbent is b'=max(b,g_q) if feasible, otherwise b. Define Bayes simple regret R(H)=E[M|H]-b. By the tower property,

R(H)-E[R(H,Y_q)|H] = E[b'-b|H] = E[(g_q-b)_+ 1{q feasible}|H].

The expected best-unknown term cancels. Dividing by a fixed history-based predicted transaction time retains the same ranking as constrained EI per cost. This calculation needs only the current joint marginal of the queried candidate's gain/feasibility, not its covariance with other currently unmeasured candidates. It does NOT assume independent gain and slew, Gaussianity, or equal candidate costs. Therefore do not factor into EI times probability of feasibility unless that same-candidate independence is established.

Consequence: joint hypothetical complete tables and posterior fantasies are unnecessary for this literal one-step objective. A comparator with the SAME posterior updates, W, observations and measured-only eligibility, but direct constrained-EI acquisition, should reproduce its action up to sampling/ties. Differences caused merely by Monte Carlo noise are not a useful information-policy mechanism. C04's ordinary knowledge gradient may value unmeasured posterior-mean alternatives at termination, so its claims cannot silently certify this different policy. C03's entropy objective is also different.

Important limit: cross-candidate covariance still changes future candidate marginals after a real observation and can thus improve a sequence of myopic EI choices. Cross-output covariance can matter to current feasibility. A multi-step rollout or risk-threshold stopping rule can depend on joint uncertainty. This objection does not refute those surviving routes, nor the physical W feature hypothesis. State exactly which benefit is claimed; preserve the measured-only guard contract.

Cheapest falsifier/repair: analytic equality audit, then finite-table or Gaussian quadrature comparisons under identical same-candidate marginals and varied cross-candidate correlations; compare full-table fantasy regret to direct constrained EI with common random samples. Include a second-round case showing whether genuine posterior transfer changes choices. Reversal condition: an explicitly specified horizon greater than one, non-measured terminal action, or different loss makes the identity inapplicable; any such change needs explicit cost/contract audit, not an implicit implementation choice.

Lightweight check actually executed: exact Fraction enumeration of two feasible candidates with values +/-1, b=0, under same-sign, opposite-sign and independent laws. Prior regrets are 1/2,1,3/4; expected one-query regret reduction is 1/2 for either query in all three. This illustrates cancellation; it is not an EDA benchmark or Gaussian calibration result. Reproducible snippet is in independent-estimate.md.

## OBJ-002 — Newer contest material is available and should replace a roadmap-only coverage gap

Target CLM-702 and EXP-001 contest dependency; severity medium documentary update, not a fatal novelty objection. C08 README identifies ISPD2027 MCMM Post-CTS Buffering and Sizing and registration opening October 5, 2026. C09 already documents setup/hold analysis at BC/TC/WC, legality checks, distinct tool/total-flow runtime and currently dummy scoring weights. C07 gives 2026 final results; C11 winner page supplies identities only. Independent search found the 2027 repository through the official symposium link, rather than inferring it from the prior roadmap.

Consequence: current contest audit can be more concrete now. However this successor's ideal-clock single-scenario setup slice is NOT a full 2027 solution and should not be pushed into MCMM merely to resemble the contest. Use the new rules to document applicability/non-applicability and baseline availability. No winner mechanism, exact same-task superiority or organizer-provided physical covariance method was established. The latest weights are explicitly not final.

Cheapest repair: pin C08/C09; inspect the description PDF through an ordinary supported reader and current evaluator/reference code without running it; separately locate 2026 winner method reports. This turn's PDF web fetch failed because raw content is application/octet-stream, not because source access is prohibited. Exclude the mislabeled 2025 closing-slide link. Reversal condition: repository archival/version evidence shows these materials postdate the cutoff or are not organizer-endorsed. Current official link, October commit and timeline support availability, but live-source evolution remains a reproducibility caveat.

## Exact same-assumption mechanism reduction and surviving contribution

For a finite candidate/output index i, take pre-query feature phi_i=W_i, prior weights z~N(0,Omega), and latent per-index residual epsilon~N(0,D). Bayesian linear regression or a GP with k(i,j)=phi_i Omega phi_j^T + D_ij produces exactly the proposed Gaussian joint law. Give the comparator the identical analytical mean, hyperparameters, labels, history, observation semantics and controller: posterior means, covariance and acquisition distributions are identical. This is an algebraic representation identity, not a claim that a cited generic paper already implemented this EDA system. D must be latent model discrepancy conditioned to zero uncertainty at an exactly observed entry, rather than artificial observation noise that keeps deterministic queried labels uncertain.

C02 supplies standard conditioning and a narrower separable block-design cancellation example. Its latter theorem does not establish cancellation for arbitrary W. The proposal already acknowledges faithful B5 equivalence: useful novelty could reside in obtaining physically informative W cheaply, stable calibration/transfer or a deployment cost tradeoff relative to generic feature construction and current calibrated timing. Do not declare all such contributions trivial merely because this kernel is familiar. C05/C06 make calibrated analytical estimation a necessary strong alternative. Missing physical residual data leaves this contribution unresolved, not refuted.

## Coverage and final selection position

| Required key | Status | Reason |
|---|---|---|
| duplicate_prior_art | unresolved | Exact statistical representation maps to a standard supplied-feature GP; no checked source establishes complete EDA-system duplication. Newer method/winner full-text review remains incomplete. |
| mechanism | supported | Conditional covariance arithmetic is coherent, and OBJ-001 identifies a checkable acquisition reduction. Physical residual correspondence is still unmeasured. |
| composition | unresolved | Known components are eligible; no measured useful W/integration delta over B5 plus constrained EI is demonstrated. |
| demand | supported | C01 is a real temporary replacement/local-arrival consumer. It does not prove enough legal alternatives or a large bottleneck; global utility remains unresolved. |
| industry_gap | unresolved | Open implementations establish baseline capability; commercial internals/comparable workload are unknown. No industry-absence claim is supported or needed. |
| headroom | unresolved | Query costs, candidate counts and remaining residual structure unknown. No applicable EDA saturation bound; OBJ-001 is only a policy identity. |
| contests | unresolved | C07-C09 improve current official coverage; winner algorithms and full description/code audit remain incomplete. |
| experiments | unresolved | Sensible dormant sequence, but actual owners, rights/build, label data, thresholds/resources and matching consents absent. Add acquisition falsifier before fitting. |
| cost | unresolved | Full ledger is specified, not measured; eliminate unnecessary fantasy overhead and charge probes, labels, restore, global guards and invalidation. |

Owner lens assessment: hybrid electrical predictor plus analytical/reference work is the strongest surviving hypothesis here. Separate specialist/fusion and shared-trunk joint predictors remain fair baselines. There is no evidence that adding algorithmic agents helps this tightly specified single-driver decision; do not add them to satisfy a label. Component reuse alone incurs no drift. Initial EDA-0007 combination_drift=0 and demand_drift=0 relative to its own frozen anchor; these are not novelty scores. EDA-0006 status is not independently re-adjudicated here.

No supported fatal contradiction, universal equivalence verdict, theoretical exhaustion or joint abandonment is asserted. No experiment consent: task additions and actual readiness remain unresolved. The scheduled verifier must adjudicate these two objections; this challenger cannot veto. Stop after cycle 4. A later restart must be separately authorized and retain this negative/conditional record.
