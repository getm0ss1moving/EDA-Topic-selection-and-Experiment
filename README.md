> Active policy (2026-10-15): ChatGPT/Codex-only proposer, challenger and verifier. Start with [the automation contract](docs/CODEX-AUTOMATION.md) and [the challenger gap report](docs/CHATGPT-CHALLENGER-GAP-ANALYSIS.md). Historical platform tables below are superseded by `config/launch-release.json`.

# EDA Topic Selection and Experiment

A file-mediated research program for Agentic EDA, AI for EDA, and traditional EDA. The goal is falsifiable, useful research questions supported by literature, contest, implementation, and engineering evidence—not a stream of plausible ideas.

Current research preference: [useful combinations and structural innovation](docs/INNOVATION-STRATEGY.md), including cooperating EDA agents, unified prediction and specialist/learned/exact hybrids. Component reuse is eligible; unsupported assembly and engineering-demand drift are penalized.

## Start here

1. Read [the charter](docs/CHARTER.md), [workflow](docs/WORKFLOW.md), and [isolation policy](docs/ISOLATION.md).
2. The human owner fills [the research brief](config/research-brief.json), including domain, compute, tools, datasets, and publication constraints. Unknown constraints remain explicitly unknown.
3. Follow [the active automation contract](docs/CODEX-AUTOMATION.md) for separate logical seats, fresh role jobs and released-file transport. A completed finite batch is not authorization for another batch; use a new bounded owner brief rather than resetting its counters.
4. Create a draft: `python3 scripts/project.py init EDA-0001`.
5. Produce and contest evidence through PRs. Only confirmed dossiers enter `topics/`.
6. Validate with `python3 scripts/project.py validate` and `python3 -m unittest discover -s tests -v`.

Before confirming a topic or starting experiments, proposer and challenger must jointly finalize `tasklist.md` and separately bind its digest in `experiment-consensus.json`. Compute the digest with `python3 scripts/project.py tasklist-digest candidates/EDA-NNNN`.

## Project map

| Path | Purpose |
|---|---|
| `harness/` | Role-specific executable work instructions |
| `docs/` | Governance, evidence standards, EDA scope, experimental policy |
| `config/` | Human constraints and session registration |
| `templates/topic/` | Complete dossier template |
| `candidates/` | Submitted proposals, challenges, responses, verification; no acceptance implied |
| `topics/` | Independently confirmed research topics; experimental claims remain labeled |
| `archive/` | Rejected/parked ideas and resurrection criteria |
| `runs/` | Public run manifests and packet provenance; never private reasoning |
| `scripts/` | Dossier creation, checks, hashing, role packet export |

All research artifacts, role interactions, and technical reviews use English. Human-facing setup explanations may follow the human's language preference. Agents communicate through committed files only; reviews carry machine confirmation, not scientific arguments.

## Current status

The new innovation batch `GPT-INNOVATION-0002` completed four full proposer/challenger/verifier cycles per domain for D04 and D05: eight merged round PRs and 24 hash-verified role releases. EDA-0005 and EDA-0006 were parked after three cycles; the final cycle independently reviewed successor EDA-0008 (physical action-order prediction) and EDA-0007 (electrical-contrast modeling for selective timing evaluation). Both successors were also parked with concrete revision and reopening conditions. No topic passed experimental admission, no joint-abandonment signatures were fabricated, and no new EDA experiment or fifth cycle was launched.

Read the latest [Chinese topic report](reports/final/GPT-INNOVATION-0002.zh-CN.md), [round/release index](runs/GPT-INNOVATION-0002/topic-index.json), [public-byte audit](runs/GPT-INNOVATION-0002/publication-audit.json) and [actual stop check](runs/GPT-INNOVATION-0002/stop-check.json). Scientific originals remain English. Requested models are proposer gpt-6.1-sol/high, challenger gpt-6-astra/low, verifier gpt-6.1-sol/low. Each job used a fresh app agent; no running unattended service or independently attested backend identity is claimed.

The earlier batch `GPT-FOUR-ROUNDS-0001` and its [Chinese report](reports/final/GPT-FOUR-ROUNDS-20261015.zh-CN.md) remain historical. The new innovation strategy does not rewrite its frozen scores, decisions or signatures.

The scope is academic chip EDA using public or legitimately accessible research material. Public vendor information does not establish the absence of proprietary capabilities. The current [runtime-event record](runs/GPT-INNOVATION-0002/runtime-incidents.json) preserves a platform classification interruption and a same-verifier inventory repair; neither was counted as a completed round before valid collection.

Repository: https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment

## Historical platform allocation

The older [team allocation](docs/TEAM.md), [Codex](docs/platforms/CODEX-PHYSICAL.md), [DeepSeek](docs/platforms/DEEPSEEK-PHYSICAL.md), and [Claude](docs/platforms/CLAUDE-PHYSICAL.md) documents preserve the earlier cross-platform setup. They are superseded for new work by the ChatGPT-only automation contract and current config. Released historical handovers remain evidence; their approvals and private context do not transfer to new roles.

Historical resource checks: [Physical pilot](docs/PHYSICAL-PILOT.md). Proposed ceilings are not a new experiment allocation.

Historical lead handoffs: [DeepSeek](docs/handoffs/DEEPSEEK-LEAD.md), [Claude](docs/handoffs/CLAUDE-LEAD.md), and [shared coordinator contract](docs/handoffs/PLATFORM-LEAD-CONTRACT.md). These do not launch or message external agents.
