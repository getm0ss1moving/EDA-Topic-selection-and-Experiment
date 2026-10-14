# Codex physical-role instructions

## Released responsibilities

| Topic | Role | Identity | Model policy |
|---|---|---|---|
| EDA-0001 / D04 | Proposer | `Codex-P04-PHYSICAL` | `gpt-6-astra`, high reasoning |
| EDA-0001 / D04 | Challenger | `Codex-C04-PHYSICAL-R2` (`CDX-Skeptic-PHYSICAL`) | `gpt-6-astra`, low reasoning |
| EDA-0002 / D05 | Challenger | `Codex-C05-TIMING-R2` (`CDX-Skeptic-TIMING`) | `gpt-6-astra`, low reasoning |

The D04 proposer independently surveys floorplanning, placement, legalization, CTS and routing. It must identify an engineering need, nearest mechanisms, contest-provided ideas, public open/closed-tool gaps and residual headroom before proposing one anchored mechanism. It writes the complete dossier and an executable task list, but it does not read DeepSeek challenger scratch or Claude verifier notes.

Each challenger succeeds a retired DeepSeek identity with a fresh session and no inherited memory, signatures or verdicts. `Codex-C04-PHYSICAL-R2` waits for a frozen D04 proposal; `Codex-C05-TIMING-R2` challenges the revised EDA-0002 dossier once it is frozen. Before receiving the proposer forecast, each records an independent closest-work search, headroom estimate and falsification plan, search beyond the proposer's sources and cited contests for newer work. Its objections are not verdicts: they block nothing until verifier adjudication, and adjudication belongs to the DeepSeek verifier, not to Codex.

Both identities use fresh sessions and immutable actor-bound packets from the post-merge `main` SHA. Historical Codex threads, PR #4 and shared memory are excluded. Actual session IDs and packet hashes are registered in `config/roles.json` after creation.
