# GPT innovation batch 0002 — coordinator audit

Owner-authorized finite batch: D04 and D05, four complete proposer/challenger/verifier cycles per domain including successors. Initial topics are EDA-0005 and EDA-0006. This run is separate from GPT-FOUR-ROUNDS-0001 and does not reopen or overwrite its frozen decisions.

- Policy and bounded discovery questions: docs/INNOVATION-BATCH-0002.md and docs/INNOVATION-STRATEGY.md.
- Configuration: config/codex-innovation-research.json.
- Exact source: f68c1492c05be3fac5622deac4bb479eabf957de, public tag codex/gpt-innovation-source-20261015. Setup metadata added afterward is not part of this source snapshot.
- Setup PR: https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/45 (merged).
- Requested app models: proposer gpt-6.1-sol/high; challenger gpt-6-astra/low; verifier gpt-6.1-sol/low. Each execution starts without inherited conversation. Requested configuration and actual successful app dispatch are recorded; backend identity is not independently attested.
- Scientific communication uses immutable released files. The coordinator handles scheduling, byte/provenance checks and GitHub transport; it does not supply independent scientific approval.

`controller.py` records successful app dispatches and audits coordinator state, packet manifests, explicitly released inputs and frozen output bytes. It never reads role scratch or transcripts. `progress.json` and `topic-index.json` are generated checkpoints; `release-audit.json` states whether the finite batch is complete. Use `python3 runs/GPT-INNOVATION-0002/controller.py --final` only after four complete cycles in each domain, eight published/merged rounds and 24 valid releases.

This is a bounded app-driven batch, not an unattended daemon or adversarial OS sandbox. The owner authorized research/source work and lightweight local analytical checks, not new EDA full-flow, training, GPU, remote or paid-API resources. A toy result is not a measured EDA result. Forecasts remain uncalibrated unless the frozen scientific record establishes otherwise.

Completion: four complete cycles per domain, 24 valid frozen releases and eight merged round PRs. All four topics' last scientific decisions are `park`; no pilot or joint abandonment was approved. The two original topics received three cycles each; each successor received the fourth domain cycle. The stop check actually invoked both domain dispatches and verified `finished`, no pending jobs and no new topic/job.

The [Chinese owner report](../../reports/final/GPT-INNOVATION-0002.zh-CN.md) summarizes the evidence and conditional next tests. `publication-audit.json` compares all public `origin/main` release bytes with collected runtime bytes; `publication-receipts.json` records actual merge commits/checks/review-thread state. One automated source-locator follow-up on parked EDA-0006 remains explicitly unadjudicated in `review-followups.json`; frozen history is preserved and the questioned locators cannot support promotion pending independent recheck. To reproduce while the original local runtime is available:

```sh
python3 runs/GPT-INNOVATION-0002/controller.py --final
python3 runs/GPT-INNOVATION-0002/audit_publication.py
```

These commands audit existing records; they launch no research role. `completion.json` records repository validation and test results. Public receipts are snapshots at their recorded UTC time, not promises about later comments or branch state.
