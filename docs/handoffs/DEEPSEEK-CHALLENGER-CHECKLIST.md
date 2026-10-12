# DeepSeek challenger launch checklist

This checklist is for the DeepSeek platform lead, who coordinates `DeepSeek-C04-PHYSICAL` and `DeepSeek-C05-TIMING` (human owner decision, 2026-10-13). The Claude platform coordinator wrote it from the `Claude-P05-TIMING` launch (`runs/CLD-P05-LAUNCH-0001`, `runs/CLD-P05-SESSION-0001`). It records host facts and launch controls, not scientific guidance. Adapt the Claude launch files rather than copying them: their settings digest, paths and session ID belong to that launch.

## When a challenger may start

- Only after the topic's proposal has been submitted, merged and frozen, with its proposer session registered in `config/roles.json`. `scripts/actor_packet.py` refuses an earlier challenger packet.
  - EDA-0002: `Claude-P05-TIMING` (session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`) is in its research round, and no dossier exists yet.
  - EDA-0001: no `Codex-P04-PHYSICAL` session is registered.
- Export with `--stage initial` first, which withholds `forecast.json`, responses and verification files. Export `--stage full` only after the challenger's independent estimate is committed.
- `config/launch-release.json` allows at most two scientific sessions at once. Ask the operator to close a proposer session once its dossier is submitted; it can be resumed for responses later.

## Budget

- Spend only the prepaid DeepSeek balance; no top-ups (`config/research-brief.json`, `deepseek_api_allowance`).
- Record the observed balance in each launch's run record. Stop when the balance is exhausted, with no automatic retries.

## Model and effort

- Record the model ID the DeepSeek API actually serves. The registry requests `deepseek-flash`, but the operator's Claude Code default on 2026-10-13 was `deepseek-v4-flash[1m]`. Never report Flash as V4 Pro.
- `config/agents-deepseek.json` requests effort `medium` for both challengers. `docs/TEAM-DEEPSEEK.md`, however, says the host offers only `off`, `low`, `high` and `max`, and it assigns challengers `max`. Correct the registry before launch.
- Do not run `/model` inside a role session. On the Claude launch, an operator `/model` selection changed the session's effort and also the user-level default.

## Routing and credentials

- The operator's interactive shell profile exports `ANTHROPIC_BASE_URL` (`api.deepseek.com`), an auth token and model-name remaps. That is the DeepSeek route, but inheriting the whole shell brings other state too. Start the role with `env -i` and pass only the routing variables explicitly.
- Since 2026-10-12, the shared Claude Code configuration also holds a first-party Claude subscription login, used by the Claude actors. A DeepSeek session must authenticate with the DeepSeek key and must never fall back to that login.
- Keep the key out of the role. Bash subprocesses inherit the CLI environment, so prefer an `apiKeyHelper` that reads the key from the macOS Keychain over an environment variable. Never write the key to the repository, a packet, an outbox or a run record.
- Map every model alias Claude Code may use to a DeepSeek model: opus, sonnet, haiku and the small helper model. In the Claude launch, `WebFetch` processing billed a separate helper model (`claude-haiku-5-5`); in a DeepSeek launch that call must also reach DeepSeek.

## CLI

- npm's `allowScripts` policy on this host blocks the Claude Code postinstall step, leaving `bin/claude.exe` as a placeholder. The nvm-global install (2.1.296) is currently such a placeholder; the Homebrew install is 2.1.226.
- Pin one version in its own prefix and run the native platform binary directly, checking its SHA-256, as `runs/CLD-P05-LAUNCH-0001/launch.sh` does.
- Shells spawned by the Claude desktop app export a cross-session messaging socket and token. Launch only from the operator's own Terminal.app, and make the launcher refuse to start inside a Claude session.

## Isolation controls validated in the Claude launch

- **Flags:** `--safe-mode`, which removes `CLAUDE.md`, plugins (including the globally enabled Codex plugin), skills, hooks and MCP servers. Also `--strict-mcp-config`, `--setting-sources project` and `--settings` with a reviewed file.
- **Tools:** `--tools Bash,Read,Write,Edit,WebSearch,WebFetch`. A deny-list alone missed `RemoteTrigger`, which appears only after sign-in.
- **Bash sandbox:**
  - enabled, with `failIfUnavailable` set and `allowUnsandboxedCommands` false;
  - `denyRead` covers the whole home directory, with `allowRead` for the packet and outbox only;
  - `denyWrite` covers the packet;
  - Bash has no network.
- **Deny rules:**
  - Read and Edit are denied for repository checkouts, other actors' packets and outboxes, home dot-directories, `~/Library` and coordinator temporary trees.
  - A challenger's rules must also cover the proposer's packet and outbox, `EDA-Agent-*/physical-release-*/Claude-P05-*`. The Claude rules covered only `Claude-V02-*`.
  - Add the corresponding Codex paths.
- **Packet:** keep the packet directories read-only (0555). Claude Code then cannot create its `.claude/.cc-writes` staging folder in the packet. It may create one in the outbox; exclude that folder from transport.
- **Pre-launch test:** run a synthetic isolation test before the real launch, using `runs/CLD-P05-LAUNCH-0001/isolation_smoke.py` as a template. For DeepSeek, add checks that:
  - every billed model is a DeepSeek model;
  - `auth status` shows the DeepSeek credential rather than `claude.ai`;
  - no Bash command can see the key.
- **Settings digest:** make the launcher enforce the reviewed settings digest. A Codex review found that the Claude launcher first only printed it.

## Records

- The host clock runs 54,000 s behind NTP, so correct the timestamps in run records.
- Register each session in `config/roles.json` with every required field and role `challenger`, and record the digests of its onboarding outputs, as in `runs/CLD-P05-SESSION-0001`.
- A coordinator reads a role's released outputs, never its transcript.
