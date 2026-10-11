# Claude physical-role instructions

## Released responsibilities

| Topic | Role | Identity | Model policy |
|---|---|---|---|
| EDA-0002 / D05 | Proposer | `Claude-P05-TIMING` | strongest Claude-family model exposed by the destination host |
| EDA-0001 / D04 | Verifier | `Claude-V02-PHYSICAL` | lightweight Claude-family model suitable for bounded source checking |

The D05 proposer independently surveys extraction, STA, corner robustness, timing closure/ECO and signoff methodology. It must separate tool-speed proxies from timing-decision correctness and must define the reference oracle, missed-violation policy and practical engineer need. It writes one anchored proposal and a falsifiable task list without reading DeepSeek challenger scratch or Codex proposer history.

The D04 verifier is created only after the Codex proposal and DeepSeek challenge are frozen. It checks original sources, locators, applicability, novelty overlap, headroom assumptions, direction drift and experiment readiness. Disputed mathematics, theoretical limits or inaccessible commercial claims return `needs_expert_review` rather than an invented verdict.

Claude model names are host-bound. Before scientific input is released, the platform lead records the exact exposed Claude model, effort setting, session ID, packet SHA-256 and isolation controls. If the destination host exposes no Claude-family model, creation stops; a GPT or DeepSeek model may not run under a Claude identity.
