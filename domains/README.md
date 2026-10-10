# Survey territories

D01-D09 are macro-domain allocations, not topic IDs or scientific claims. All three approaches—traditional EDA, AI for EDA and relevant agentic methods—are considered within each territory. D09 additionally covers cross-domain agent orchestration. Formal topic IDs are created only after survey evidence supports a bounded candidate.

See `docs/TEAM.md` + `config/agents.json` (Codex platform) and `docs/TEAM-DEEPSEEK.md` + `config/agents-deepseek.json` (DeepSeek platform) for role/task assignments. Each territory is surveyed independently by both platforms.

Each `brief.json` carries a `platform_roles` block binding the platform-neutral top-level `proposer`/`challenger`/`verifier` fields (Codex) and the equivalent DeepSeek identities. Adding a platform is additive: it appends a key under `platform_roles` and does not renumber domains or rename existing actors.

Domain briefs contain scope and boundaries rather than unverified claims about current state of the art.
