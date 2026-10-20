# EDA Literature and Human-Led Topic Review

The human owner proposes research ideas. Three AI roles support that work:

| Role | Responsibility | Instructions |
|---|---|---|
| Searcher | Find, classify and summarize papers, contests and useful open projects from floorplanning to signoff; provide Chinese reading aids | [Searcher](harness/SEARCHER.md) |
| Challenger | Independently search prior art, challenge novelty and need, forecast experiments and propose decisive falsification tests | [Challenger](harness/CHALLENGER.md) |
| Verifier | Independently check evidence and adjudicate objections in compact tables | [Verifier](harness/VERIFIER.md) |

There is no AI proposer or automatic AI replacement-topic generator.

## Start here

1. Read the [workflow](docs/WORKFLOW.md), [charter](docs/CHARTER.md), [evidence](docs/EVIDENCE.md) and [isolation](docs/ISOLATION.md) rules.
2. Browse the [literature index](literature/README.md) and [the latest ten reading cards](literature/batches/002.zh-CN.md). The target is 100 distinct papers; contests and repositories are tracked separately.
3. Submit your idea using [the human idea template](templates/human-idea.md). The coordinator commits and freezes it before independent review; an incomplete idea can receive exploratory feedback without being called experiment-ready.
4. Challenger submits evidence-backed criticism to verifier. Verifier returns adjudicated findings to you. You decide and author the next revision.
5. A promising plan needs an explicit human/challenger task-list agreement, independent verification and allocated resources before experiments. [Retirement rules](docs/TOPIC-RETIREMENT.md) stop weak topics without erasing their history.

Active settings: [research-workflow.json](config/research-workflow.json).
Role jobs are configured, not claimed running; the historical automated P/C/V loop is disabled.

Research and review prose is English. Chinese titles, paraphrased summaries and reading notes are explicitly allowed for the requested literature translations; original English titles and precise sources remain attached. User-facing explanations are Chinese.

## Files and validation

`literature/` holds the catalog and reading aids; `harness/` holds only the active role instructions plus a retired-role notice. `candidates/`, `topics/`, `archive/` and `runs/` preserve research and audit evidence. [Historical configurations](legacy/README.md) are inactive. Existing proposer-labelled provenance fields remain for old records and human-authored dossier compatibility; they do not authorize an AI proposer.

```sh
python3 scripts/project.py validate
python3 scripts/literature.py validate
python3 -m unittest discover -s tests -v
```

## Historical research

The completed four-round D04/D05 batches remain frozen. See the [latest Chinese report](reports/final/GPT-COMPLIANCE-0004.zh-CN.md), [conduct matrix](reports/final/GPT-COMPLIANCE-0004.conduct.en.md) and [stop record](runs/GPT-COMPLIANCE-0004/stop-check.json). No old topic was deleted, rescored or experimentally accepted by this workflow change.

Repository: https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment
