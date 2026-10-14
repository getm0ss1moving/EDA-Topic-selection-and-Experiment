# Claude physical-role instructions

## Released responsibilities

| Topic | Role | Identity | Model policy |
|---|---|---|---|
| EDA-0002 / D05 | Proposer | `Claude-P05-TIMING` | strongest Claude-family model exposed by the destination host |

The D05 proposer independently surveys extraction, STA, corner robustness, timing closure/ECO and signoff methodology. It must separate tool-speed proxies from timing-decision correctness and must define the reference oracle, missed-violation policy and practical engineer need. It writes one anchored proposal and a falsifiable task list without reading DeepSeek challenger scratch or Codex proposer history.

The former D04 verifier seat (`Claude-V02-PHYSICAL`) moved to `DeepSeek-V02-PHYSICAL` under the owner decision of 2026-10-13 recorded in `config/launch-release.json` `role_handoffs`; no Claude verification identity is released in this division of work.

Claude model names are host-bound. Before scientific input is released, the platform lead records the exact exposed Claude model, effort setting, session ID, packet SHA-256 and isolation controls. If the destination host exposes no Claude-family model, creation stops; a GPT or DeepSeek model may not run under a Claude identity.
