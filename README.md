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

The governance framework and platform allocations are on `main`. No topic, literature survey, experimental result, or scientific approval is claimed. `M0nitor-EDA` is enrolled as an independent GitHub review identity, but account enrollment is not scientific confirmation. The physical-slice role-creation release is recorded in `config/launch-release.json`: after that release is merged, six fresh cross-platform role sessions may be created in workflow order from packets exported at the resulting full `main` SHA.

The released D04/D05 assignment is documented separately for [Codex](docs/platforms/CODEX-PHYSICAL.md), [DeepSeek](docs/platforms/DEEPSEEK-PHYSICAL.md), and [Claude](docs/platforms/CLAUDE-PHYSICAL.md). These are execution contracts, not survey results.

Repository: https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment

## Released physical team

See [team allocation](docs/TEAM.md), the three platform documents above, and `config/agents*.json` for role identities and runtime status. Codex and Claude each supply one proposer and one cross-topic verifier; DeepSeek supplies both challengers. This does not resume archived historical sessions and does not authorize experiments.

Current scope and reproducible resource checks: [Physical pilot](docs/PHYSICAL-PILOT.md). The first wave contains the D04 and D05 proposers only; challenger and verifier scientific inputs are released later in workflow order.

Platform lead handoffs: [DeepSeek](docs/handoffs/DEEPSEEK-LEAD.md), [Claude](docs/handoffs/CLAUDE-LEAD.md), and the [shared coordinator contract](docs/handoffs/PLATFORM-LEAD-CONTRACT.md). These documents describe assignments; they do not by themselves launch or message external agents.
