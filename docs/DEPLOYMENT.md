# Deployment status

- Repository: `getm0ss1moving/EDA-Topic-selection-and-Experiment` (public).
- Bootstrap and governance framework: merged to `main` through independently confirmed PRs.
- Research: no accepted topics and no completed domain survey yet.
- Roles: owner/transport coordinator `getm0ss1moving`; the exact six-role cross-platform matrix is in `config/launch-release.json` and `docs/platforms/`. It releases Codex and Claude proposers, DeepSeek challengers, and cross-platform Codex/Claude verifiers for fresh role creation after the release PR is merged and new packets are exported. No session is registered in `config/roles.json` yet.
- Independent GitHub verifier: `M0nitor-EDA` is enrolled. Every PR still needs its exact-current-head confirmation; enrollment alone is not approval.
- Isolation: packet exporter implemented, including actor-scoped domain packets (`scripts/project.py packet ROLE --domain DNN --actor ID`); worktree and outbox separation prevent collisions but an OS/container sandbox must be provided by the session operator for enforced file isolation.
- Compute/tool/data constraints: `config/research-brief.json` records measured local capability and provisional coordinator caps. Those caps permit literature research and bounded baseline preparation; representative publication designs, macro-rich cases, additional corners and a qualified signoff oracle remain experiment blockers.

Live deployment checks and PR links are available in GitHub. This file states bootstrap intent and known prerequisites; do not interpret a configured workflow as a completed scientific review.
