# EDA Topic Selection and Experiment

A file-mediated research program for Agentic EDA, AI for EDA, and traditional EDA. The goal is falsifiable, useful research questions supported by literature, contest, implementation, and engineering evidence—not a stream of plausible ideas.

## Start here

1. Read [the charter](docs/CHARTER.md), [workflow](docs/WORKFLOW.md), and [isolation policy](docs/ISOLATION.md).
2. The human owner fills [the research brief](config/research-brief.json), including domain, compute, tools, datasets, and publication constraints. Unknown constraints remain explicitly unknown.
3. After the governance pause is explicitly released, enroll independent sessions using [the coordinator runbook](harness/COORDINATOR.md). Proposer, challenger, and verifier have separate harnesses and file packets.
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

The repository began empty. `main` contains a minimal trusted review-gate bootstrap; this framework is delivered as a PR. No topic, literature survey, experimental result, or scientific approval is claimed. `M0nitor-EDA` is enrolled as an independent GitHub review identity, but no review or scientific confirmation is implied by enrollment. See [deployment status](docs/DEPLOYMENT.md).

Repository: https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment

## Assigned Codex team

See [team allocation](docs/TEAM.md) for the role identities and `config/agents.json` for their model settings and runtime status. All scientific role conversations are paused during governance hardening.

Current future scope and reproducible resource checks: [Physical pilot](docs/PHYSICAL-PILOT.md). Five Codex assignments remain planned for D04/D05, but the active actor count is zero; see [actor registry](config/agents.json).

Platform lead handoffs: [DeepSeek](docs/handoffs/DEEPSEEK-LEAD.md), [Claude](docs/handoffs/CLAUDE-LEAD.md), and the [shared coordinator contract](docs/handoffs/PLATFORM-LEAD-CONTRACT.md). These documents describe assignments; they do not by themselves launch or message external agents.
