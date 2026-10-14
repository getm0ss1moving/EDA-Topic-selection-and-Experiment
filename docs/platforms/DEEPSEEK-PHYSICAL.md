# DeepSeek physical-role instructions

## Released responsibilities

| Topic | Role | Identity | Model policy |
|---|---|---|---|
| EDA-0001 / D04 | Verifier | `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`) | observed `deepseek-flash` at low effort for bounded source checks; record actual model and effort |
| EDA-0002 / D05 | Verifier | `DeepSeek-V02-PHYSICAL` (`DSK-Ledger-PHYSICAL`) | one shared identity; the two queues run sequentially |

DeepSeek is the verification platform for both queues in this release (owner decision 2026-10-13, recorded in `config/launch-release.json` `role_handoffs` and `runs/DSK-ROLE-SUCCESSION-0001`). The former challenger seats were handed to Codex successors: `DeepSeek-C04-PHYSICAL` never ran; `DeepSeek-C05-TIMING` completed a round-1 challenge whose record is transported in `runs/DSK-C05-SESSION-0001` before the handoff to `Codex-C05-TIMING-R2`.

The verifier session is created only after the proposal and challenge artifacts are frozen and released. It reopens original sources, checks claim/locator entailment, adjudicates every objection (accepted, partially valid, unsupported, refuted or unresolved), audits direction penalties and experiment consensus, and writes a traceable verdict. It does not rewrite the proposal and cannot replace proposer or challenger consent; disputed mathematics, theoretical-limit claims or inaccessible commercial claims return `needs_expert_review` rather than an invented verdict. Only after the final files are committed may the separately registered GitHub identity confirm the exact PR head.

The historical DeepSeek onboarding packets remain evidence only. New packets must bind the verifier, the assigned queue, the full post-merge commit and a private outbox. No DeepSeek proposer or challenger identity is released in this division of work.
