# Codex physical-role instructions

## Released responsibilities

| Topic | Role | Identity | Model policy |
|---|---|---|---|
| EDA-0001 / D04 | Proposer | `Codex-P04-PHYSICAL` | `gpt-6-astra`, high reasoning |
| EDA-0002 / D05 | Verifier | `Codex-V02-PHYSICAL` | `gpt-6-luna`, medium reasoning |

The D04 proposer independently surveys floorplanning, placement, legalization, CTS and routing. It must identify an engineering need, nearest mechanisms, contest-provided ideas, public open/closed-tool gaps and residual headroom before proposing one anchored mechanism. It writes the complete dossier and an executable task list, but it does not read DeepSeek challenger scratch or Claude verifier notes.

The D05 verifier is created only after the Claude proposal and DeepSeek challenge are frozen. It reopens original sources, checks claim/locator entailment, adjudicates objections and audits direction penalties and experiment consensus. It does not rewrite the proposal or supply missing proposer/challenger consent.

Both identities use fresh sessions and immutable actor-bound packets from the post-merge `main` SHA. Historical Codex threads, PR #4 and shared memory are excluded. Actual session IDs and packet hashes are registered in `config/roles.json` after creation.
