# Bounded batch completion

- D04: four completed three-role cycles (EDA-0001 x3, EDA-0003 x1).
- D05: four completed three-role cycles (EDA-0002 x3, EDA-0004 x1).
- 24 actor-authored frozen releases passed trusted hash checks and exact matching P/C/V result validation. No pending job remains. Both dispatch commands returned finished at four; no fifth model job was created.
- All eight round PRs #35–#42 were merged after required checks and resolution of actual transport/provenance findings. No GitHub self-approval or protection bypass was used. Supplementary run manifests are explicitly coordinator-authored reconstructions, not invented actor originals.
- All four final scientific decisions are park. No acceptance, joint-abandonment consent, experimental allocation or EDA measurement is asserted. Successor topics each received only one cycle.
- Requested models: proposer gpt-6.1-sol/high, challenger gpt-6-astra/low, verifier gpt-6.1-sol/low. Fresh app agents were used; the native CLI rejected the requested Sol model. Logical registrations and requested configurations are not physical backend attestation.
- The owner-facing Chinese report is reports/final/GPT-FOUR-ROUNDS-20261015.zh-CN.md. Scientific sources, claims, objections and verdicts remain the English frozen originals.

release-audit.json contains the final counts, public release identifiers, requested models, packet/input hashes and merged round URLs. dispatches.json records coordinator dispatch metadata. Neither records private role reasoning, scratch or conversation. The same-user filesystem is policy isolation, not adversarial confinement.

The audit.py script needs the original local runtime to recheck complete job bindings. On a public clone, each published snapshot can instead be rehashed with:

    python3 scripts/role_submission.py verify runs/SUB-<release-id>

Use the 24 identifiers in release-audit.json. Fetch the exact source with the explicit tag command in source-preservation.json / the final round's input-source.json; branch-only checkouts may omit unrelated tags. Byte-identical source-tree equivalence to the reachable main squash commit was checked separately. Full paper copies, restricted designs and private scratch were not published.

Local validation before submission: 111 unit tests passed, project structural validation passed and git diff --check passed. The final rebased tree is revalidated during PR submission; required GitHub checks remain authoritative for transport. These checks do not adjudicate science.

The batch is stopped. No unattended daemon or Terminal runner is claimed. The earlier Claude follow-up automation remains paused; no historical provider is resumed. Future scientific continuation requires a separate owner instruction.
