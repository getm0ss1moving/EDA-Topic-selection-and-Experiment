# DeepSeek challenger launch readiness: DeepSeek-C04-PHYSICAL and DeepSeek-C05-TIMING

Run `DSK-C04C05-LAUNCH-0001` prepares the two released DeepSeek challenger sessions. It does not create them, release scientific input, accept a topic or authorize an experiment. Coordinator: DeepSeek platform lead, session `04fe4881-0c22-4292-ac03-ab73f00eaf29`, model `deepseek-v4-flash[1m]`, operator `getm0ss1moving`, prepared 2026-10-13 (true UTC; see the clock note). Input commit: `main` at `8f365d39cd5b05fd90024f999cfb409d06148245`, the base of this branch. The coordinator is a transport and scheduling role, not a scientific voter.

The session IDs were pre-assigned; no session exists. Actor state is `prepared_not_started`, recorded in `actor-launch.json`.

| Actor | Call sign | Role | Topic / domain | Session ID (planned) | State |
|---|---|---|---|---|---|
| `DeepSeek-C04-PHYSICAL` | DSK-Forge-PHYSICAL | challenger | EDA-0001 / D04 | `6225f73f-b676-44ce-a3a7-ee667e1a68d2` | Prepared; blocked until the EDA-0001 proposal is frozen |
| `DeepSeek-C05-TIMING` | DSK-Forge-TIMING | challenger | EDA-0002 / D05 | `af136556-818c-47c7-b514-5a141cb14d85` | Prepared; blocked until the EDA-0002 proposal is frozen |

The proposals are not frozen: `Claude-P05-TIMING` (session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`) is in its research round with no dossier, and no `Codex-P04-PHYSICAL` session is registered. `scripts/actor_packet.py` refuses a challenger packet before a frozen submitted proposal, so the packet fields in `actor-launch.json` are deliberately `null` (shown as `PENDING` by the launcher). No DeepSeek proposer or verifier is created; every other DeepSeek actor stays deferred.

Governance observed on 2026-10-13: PRs #1-#3 and #5-#10 are merged; PR #4 is an open historical draft and is excluded from every input. `config/roles.json` registers only the Claude D05 proposer. On a clean tree, `python3 scripts/project.py validate` passes and all 33 unit tests pass. `config/launch-release.json` releases exactly the six-actor cross-platform slice and caps concurrent scientific sessions at two.

## Model and effort (DeepSeek API observation)

Observed 2026-10-13T08:04:31Z at `GET https://api.deepseek.com/models`:

| API model ID | Name | Context | Effort levels |
|---|---|---|---|
| `deepseek-flash` | DeepSeek-V4.1-Flash | 1,048,576 tokens | low / high / max (default high) |
| `deepseek-v4-pro` | DeepSeek-V4-Pro | 1,048,576 tokens | low / high / max (default high) |

The operator's Claude Code DeepSeek route (declared in `~/.zshrc`, base URL `https://api.deepseek.com/anthropic`) remaps every model alias to `deepseek-v4-flash[1m]`, the 1M-context variant of the `deepseek-flash` family. The launch kit pins `--model deepseek-v4-flash[1m]` and maps `opus`, `sonnet`, `haiku` and the subagent alias to the same value, so no request can reach a model outside the DeepSeek family. Both smoke runs observed the session model as exactly `deepseek-v4-flash[1m]` and billed no other model. This is Flash; it is never reported as V4 Pro.

Registry correction (the task of this run): `config/agents-deepseek.json` requested `reasoning_requested: medium` for both challengers, a level the host does not expose (`docs/TEAM-DEEPSEEK.md`; the API reports low/high/max). Both entries now request `max`, the challenger tier in `docs/TEAM-DEEPSEEK.md`, and a top-level `challenger_launch_policy` block records the platform-family rule, the effort correction and this API observation. Neither actor has ever run a scientific session, so no executed run is relabelled; the deferred proposer tier keeps its historical requested/actual record.

## Budget (prepaid DeepSeek balance)

Recorded per `config/research-brief.json` (`deepseek_api_allowance`), no top-ups, no automatic retries:

| Observed at (true UTC) | Balance (CNY) | Note |
|---|---|---|
| 2026-10-13T08:04:31Z | 179.38 | Before any launch-kit work |
| 2026-10-13T08:41:32Z | 175.61 | After the three synthetic smoke runs |

The 3.77 CNY delta covers the three smoke turns and this coordinator session's own DeepSeek-route usage (the lead session itself runs on the prepaid balance); the per-run split is not separable from the coordinator's own traffic and is not claimed. Work stops when the balance is exhausted.

## Launch kit

| File | SHA-256 | Purpose |
|---|---|---|
| `launch.sh` | `7f8b7c792ec793f7807b2b05292b606ec042846c728f5227fd2674cbf3cc735b` | Fail-closed launcher; reads the per-actor binding from `actor-launch.json` |
| `launch-settings-C04.json` | `3eace9a6ac10a4e6040fd3fbb0cf741137ca37175159fe212fdac673c390613a` | Isolation surface for `DeepSeek-C04-PHYSICAL` (digest pinned by the launcher) |
| `launch-settings-C05.json` | `2c1984b1e329cc8c4ba8921ba461407a228b68a9a668fbd49c905dbbbafdbf72` | Isolation surface for `DeepSeek-C05-TIMING` (digest pinned by the launcher) |
| `keychain-token.sh` | `b719c94ceb6d5108807ba0e3c79215cd989687ea6d8edb084800f46a271fa5de` | `apiKeyHelper`: reads the DeepSeek key from the macOS Keychain (`deepseek-api-key`) |
| `actor-launch.json` | `f689aee08e0ebc35e4842c2b7c0c5d5eab5ece0c63a59c8b32509c90cbec1ef8` | Per-actor binding: packet path and digest (PENDING), outbox, settings digest, session ID |
| `isolation_smoke.py` | `5d05d66397bada76c493ca24bc2e9f394df735e7b3eb3329cff4872543d1a4bc` | Synthetic isolation test; records pass/fail flags only |
| `isolation-smoke-run1-writable.json` | — | Run 1 result (writable fixture, earlier script revision) |
| `isolation-smoke-run2-readonly.json` | — | Run 2 result: final C05 configuration, all checks pass |
| `isolation-smoke-run3-readonly-C04.json` | — | Run 3 result: final C04 configuration, all checks pass |

CLI pinned: Claude Code 2.1.293, native binary `~/.local/claude-code-2.1.293/node_modules/@anthropic-ai/claude-code-darwin-arm64/claude`, SHA-256 `4e21122a227857da1178aca3299700c1fd7f2b77c93f12e73c2c76db796a105e` (identical to the binary the Claude launch smoke-tested; reused rather than reinstalled, and hash-checked by the launcher). The nvm-global 2.1.296 install remains a placeholder and is not used.

Credential handling: the Keychain entry `deepseek-api-key` (account `$USER`) was created on 2026-10-13 with the operator's explicit approval, copying the value of the operator's existing `ANTHROPIC_AUTH_TOKEN` without printing it. The key appears in no repository file, packet, outbox or run record; the only check recorded here is that the helper resolves a non-empty value (36 bytes including newline). Role sessions receive no token variable; the CLI calls the helper.

## Isolation controls

`launch.sh` aborts unless every precondition below holds, and `--check` verifies the same set while launching nothing:

- not called from inside a Claude session (`CLAUDECODE`, session ID or desktop messaging socket present);
- CLI version and binary SHA-256 as pinned;
- `launch-settings-<actor>.json` byte-identical to its reviewed and smoke-tested digest in `actor-launch.json`;
- the Keychain helper resolves a non-empty credential, and `auth status` under this settings content reports `apiKeySource: apiKeyHelper` and not `claude.ai`/`oauth_token` (no fallback to the shared subscription login);
- packet digest and every listed file hash match `PACKET.json`, with no extra file, no symlink and no writable path (once the packet exists); while any packet field is PENDING the launcher refuses to start;
- the outbox exists with mode 0700 and is empty for a fresh session; a `--resume` requires the registered session's transcript.

It then starts the CLI with `env -i` (only `HOME`, `USER`, `LOGNAME`, `SHELL=/bin/bash`, `TERM`, `LANG`, `PATH`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` and the five routing variables), `--safe-mode`, `--strict-mcp-config`, `--setting-sources project`, `--settings`, `--tools Bash,Read,Write,Edit,WebSearch,WebFetch`, the packet as working directory, the outbox via `--add-dir`, `--model deepseek-v4-flash[1m]` and `--effort max`.

Each settings file additionally: denies the administrative/messaging/remote tool set; allows writes only in the actor's own outbox; denies reads of every repository checkout, every other actor's packet and outbox on both the `physical-release-*` and `challenger-release-*` trees (including the proposer's `Claude-P05-TIMING` / `Codex-P04-PHYSICAL` paths and the sibling challenger), the historical `eda-dsk` workspace and packet trees, `EDA-Resources`, every home dot-directory, `~/Library` and the coordinator temp trees; and runs Bash in the seatbelt sandbox (`failIfUnavailable`, no unsandboxed escape) that denies reading anything under the home directory except the actor's own packet and outbox, denies writing the packet, and has no network. Web tools remain available for literature search.

Known limits, all consistent with `docs/ISOLATION.md`: the role runs as the same macOS user, so this is layered tool-permission and sandbox enforcement inside Claude Code, not an OS security boundary; the Read rules are a deny-list, and unlisted reads outside the packet and outbox still need the operator's interactive approval; the coordinator can technically read the role transcript and records here that it will not.

Three findings from testing, recorded rather than hidden:

1. Claude Code creates its own `.claude/.cc-writes` staging folder in a writable working directory. Run 1 (writable fixture) shows `packet_unmodified: false` for that reason alone; exported packets must stay mode 0555, and runs 2-3 confirm the read-only packet stays unmodified.
2. Bash children receive host login-profile variables (proxy configuration used by other tools on this machine) from the CLI's shell snapshot. No Anthropic or DeepSeek credential appears: run 2-3 check that no environment variable name matches the project credential domain, and that the Keychain value itself never appears in any Bash environment dump (written to the outbox, checked, deleted, only a boolean recorded).
3. Each headless run creates its own child session with its own live messaging socket (`/tmp/cc-socks/<pid>.sock`) and exposes that session's token to its Bash children. This is CLI behavior, not inheritance from the launching shell: the child session ID differs from the coordinator's, and `env -i` excludes any desktop-socket inheritance. The role's Bash could therefore only address its own session endpoint; `SendMessage`/`ListAgents` are denied as tools, and use of any messaging channel by a role would be a contamination event under `docs/ISOLATION.md`. Recorded as a residual risk for review, not as a passed check for the scientific protocol.

## Isolation test results

`isolation_smoke.py` runs one headless turn of the pinned CLI on a synthetic fixture with no project content, derives test settings from the actor's real launch settings (substituting only packet/outbox paths), and records pass/fail flags only — never file contents or credentials.

| Run | Configuration | Result |
|---|---|---|
| 1 (`isolation-smoke-run1-writable.json`) | Earlier script revision, writable fixture | All DeepSeek checks passed (billed model `deepseek-v4-flash[1m]` only, `apiKeySource: apiKeyHelper`, key never in output). Two defects drove fixes: the CLI created `.claude/.cc-writes` in the writable packet, and the broad environment-name check matched the CLI's own messaging token and a host proxy variable, which are not the project credential. |
| 2 (`isolation-smoke-run2-readonly.json`) | Final C05 settings, read-only fixture | All 19 environment checks and all 26 step checks passed. |
| 3 (`isolation-smoke-run3-readonly-C04.json`) | Final C04 settings, read-only fixture | All 19 environment checks and all 26 step checks passed. |

Run 2-3 verified, among others: exactly the six allowed tools; no MCP server; no third-party plugin; auto-memory off; read-only packet unmodified; outbox writes landed; Bash sandbox denied reads of the repository, other packets, `~/.claude`, `~/Library` and the sibling canary, denied network, denied writes to the packet, and could not read the Keychain credential; `WebFetch` and `WebSearch` both succeeded on this route; the session model was exactly the pinned `deepseek-v4-flash[1m]`, every billed model was DeepSeek, and no `claude-*` model was billed. The static checks confirm the sibling challenger's and the proposer's packet paths are covered by deny rules. Smoke report timestamps come from the host clock (see below).

The launcher's post-freeze path was additionally exercised against a scratch copy with a synthetic, correctly hashed packet fixture (no real packet, no session): with the packet fields filled it reached `All preconditions hold. Nothing was launched.` (exit 0), after which a tampered file made it abort with `packet contents do not match PACKET.json` (exit 1), flagging both the hash mismatch and the writable paths. The simulated config and fixture live in private scratch and are not committed.

## Host clock

The host clock runs 54,000 s (15 h) behind NTP and the API server `Date` headers (verified again today against `api.deepseek.com` and `github.com`). Timestamps in this document and in `manifest.json` are corrected to true UTC; the smoke reports and git commit dates written on this host are not, and must be read with the +15 h correction.

## Prerequisites before each launch

1. Done: operator approval for the Keychain-based credential, entry created and helper verified.
2. Done: pinned CLI installed, hash recorded, launcher enforces it.
3. Done: registry effort correction, model/effort confirmed against the API, balance recorded.
4. Done: smoke tests 2 and 3 pass against the final, digest-pinned settings for both actors.
5. Pending — proposal freeze: when the corresponding dossier is submitted and frozen and its proposer session is registered, export the challenger packet from the then-current full `main` commit:
   `python3 scripts/actor_packet.py <ACTOR> --ref <MAIN_SHA> --out /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/challenger-release-20261013/<ACTOR> --outbox /Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/challenger-release-20261013/<ACTOR> --phase research --topic <EDA-NNNN> --stage initial`
   then record its `PACKET.json` SHA-256 and file count in `actor-launch.json`, set the packet directory to 0555, and re-run `launch.sh --actor <ACTOR> --check`.
6. Pending — review gate: this branch needs the independent exact-head confirmation (`CONFIRM <full-head-sha>`) by the registered account and a human merge before any session starts.
7. Scheduling note: `config/launch-release.json` caps concurrent scientific sessions at two, and the first wave currently occupies one with the Claude D05 proposer. The operator should close a proposer session once its dossier is submitted (it can be resumed later for responses) before a challenger is started.

## Launch sequence (after prerequisites 5-7)

1. From the operator's own Terminal.app, run `bash launch.sh --actor <ACTOR> --check` and then `bash launch.sh --actor <ACTOR>`; accept the folder-trust prompt for the packet directory. The launcher prints the commit it ran from.
2. Send the onboarding prompt below verbatim, with the placeholders substituted from `actor-launch.json`. The session writes `readiness.json` and `first-pass-plan.md` to its outbox and stops; no web survey happens in this turn.
3. The coordinator records the observed model and session in `config/roles.json` by PR, with the onboarding output digests.
4. Send the research prompt (drafted at freeze time; it carries the packet digest and the stage-`initial` instruction: independent search and headroom estimate are committed before `forecast.json` is released with stage `full`). All scientific method stays in the packet's `harness/CHALLENGER.md`; the coordinator adds no scientific content.

Onboarding prompt template:

> You are `<ACTOR>` (`<CALL_SIGN>`), the DeepSeek challenger for `<EDA-NNNN>` (`<DNN>`). Your only project input is the frozen packet in your working directory, identified by the SHA-256 of its `PACKET.json`: `<PACKET_SHA256>`. Read `AGENTS.md`, `ASSIGNMENT.json`, `PACKET.json`, the common policy and only `harness/ONBOARDING.md` and `harness/CHALLENGER.md`. Use English. Verify every listed file hash. Record actor ID, actual model ID, role, topic, input commit, packet hash, the isolation controls you can observe and any unlisted context in `readiness.json` and `first-pass-plan.md` in your outbox `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/challenger-release-20261013/<ACTOR>`. Write only to that outbox. Do not begin a web survey in this turn. Do not inspect another actor's files, converse with another role, approve or merge. Finish the turn after writing both files.

## Not authorized by this record

This record makes no topic, novelty, feasibility or experiment claim. No DeepSeek session exists on 2026-10-13; both entries are planned. Nothing here approves a proposal, releases a challenge or authorizes an experiment.
