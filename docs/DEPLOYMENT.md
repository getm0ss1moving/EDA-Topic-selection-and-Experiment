# Deployment status

- Repository: `getm0ss1moving/EDA-Topic-selection-and-Experiment` (public).
- Bootstrap: minimal README and trusted independent review workflow on `main` because the repository had no commits.
- Framework: branch `codex/research-governance-foundation`, submitted by PR; not self-merged.
- Research: no accepted topics and no completed domain survey yet.
- Roles: owner/transport coordinator `getm0ss1moving`; Codex roles allocated in `docs/TEAM.md`; DeepSeek roles allocated in `docs/TEAM-DEEPSEEK.md`. Onboarding only: no broad research round is authorized by either allocation, and no session is registered in `config/roles.json` yet.
- Independent GitHub verifier: not enrolled; the review gate intentionally blocks merging until enrollment and confirmation.
- Isolation: packet exporter implemented, including actor-scoped domain packets (`scripts/project.py packet ROLE --domain DNN --actor ID`); worktree and outbox separation prevent collisions but an OS/container sandbox must be provided by the session operator for enforced file isolation.
- Compute/tool/data constraints: unknown until the human fills `config/research-brief.json`.

Live deployment checks and PR links are available in GitHub. This file states bootstrap intent and known prerequisites; do not interpret a configured workflow as a completed scientific review.
