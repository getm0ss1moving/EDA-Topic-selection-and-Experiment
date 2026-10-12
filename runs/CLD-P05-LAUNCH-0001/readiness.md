# Claude platform launch readiness: Claude-P05-TIMING

Run `CLD-P05-LAUNCH-0001` prepares exactly one role session, the EDA-0002 / D05 proposer. It does not create that session, release scientific input, accept a topic or authorize an experiment. Coordinator: Claude platform lead, session `9273c928-a2eb-46ba-890d-9dedad60ac78`, model `claude-opus-5-5`, Claude desktop app 2.31226.0 running Claude Code 2.1.293, operator `getm0ss1moving`. Input commit: `main` at `7c9771196db41fab1593ceead9ebb93d935a3508`. The coordinator is a transport and scheduling role, not a scientific voter.

## Released Claude actors

| Actor | Role | Topic | State |
|---|---|---|---|
| `Claude-P05-TIMING` (`CLD-Origin-TIMING`) | proposer | EDA-0002 / D05 | First wave. Launch prepared; no session exists yet. |
| `Claude-V02-PHYSICAL` (`CLD-Proof-PHYSICAL`) | verifier | EDA-0001 / D04 | Blocked by design until the Codex D04 proposal and the DeepSeek D04 challenge are frozen and both upstream sessions are registered. |

`Claude-P04-PHYSICAL`, `Claude-C04-PHYSICAL` and `Claude-C05-TIMING` remain deferred namespace entries and will not be created.

## Governance state (observed)

- PRs #1-#3 and #5-#7 are merged with approval. For #6 and #7 the final `M0nitor-EDA` review body is `CONFIRM` plus the exact head SHA, and earlier confirmations were dismissed after new pushes. `main` requires the `research-structure` and `independent-verifier` checks (strict), one approving review, stale-review dismissal and enforcement for admins, and forbids force pushes. CI succeeded at `7c97711`.
- On a clean tree, `python3 scripts/project.py validate` passes and all 33 unit tests pass (Python 3.9.6).
- `config/roles.json` registers no session on any platform. `max_concurrent_scientific_sessions` is 2, and the first wave holds two proposers.
- PR #4 (historical R1) is still an open draft and is excluded from every input. The DeepSeek worktree tracks a pre-rebase branch whose commits were merged under new SHAs; it was not touched.

## Packet provenance

| Field | Value |
|---|---|
| Packet | `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/physical-release-d437c2f66090/Claude-P05-TIMING` |
| Input commit | `d437c2f660906efe9351a90451905826d00b63e3`, the post-release `main` commit |
| `PACKET.json` SHA-256 | `ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d`, equal to the value in `runs/PHYSICAL-ROLE-CREATION-0001/manifest.json` |
| Files | 31. Each was re-hashed against the git blobs at `d437c2f` and at `7c97711`: no mismatch, no unlisted file, no symlink, no drift. |
| Content | Proposer harness only. `challenges.md`, `verification.md` and `verification.json` are withheld. EDA-0002 is `draft` with no registered session. |
| Hardening | Files were already mode 0444. This run set the packet directories to 0555 so that no file can be added. Hashes are unchanged. |
| Outbox | `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING`, created empty with mode 0700 |

Governance gap (not fixed here): `docs/LAUNCH.md` asks an actor to read "your platform contract", but `scripts/actor_packet.py` does not export `docs/platforms/`. The prompts below therefore refer only to packet contents; the coordinator does not inject assignment text from outside the hashed packet.

## Model availability and decision

Observed: the desktop host exposes `claude-fable-5-1`, `claude-opus-5-5`, `claude-sonnet-5-5` and `claude-haiku-5-5`, all Claude-family, so the abort condition in `docs/platforms/CLAUDE-PHYSICAL.md` does not apply. The bundled Claude API reference (model table cached 2026-10-06) lists Fable 5.1 as the most capable widely released model at USD 10/50 per million input/output tokens, Opus 5.5 at 4/20, Sonnet 5.5 at 2/10 and Haiku 5.5 at 0.10/0.50, each supporting effort `low` through `max`. These list prices serve only as a relative usage indicator: the project consumes subscription quota and no paid API.

Decision by the human owner on 2026-10-12: `claude-opus-5-5` at effort `xhigh`. Fable 5.1 was declined because it uses about 2.5 times the per-token usage of Opus 5.5 and earlier Codex runs in this project failed on subscription quota. This is a resource decision under the charter's human decision rights, recorded with its rationale. It resolves the packet's `claude-family:strongest-exposed` placeholder as strongest-affordable; it is not a scientific judgement. `model_observed` stays null until the onboarding turn reports it. The model for `Claude-V02-PHYSICAL` is chosen when that role is released; Haiku 5.5 is the lightweight candidate.

## Host findings that shape the launch

1. Neither standalone CLI on this host is signed in. The desktop app authenticates its own sessions internally.
2. The CLI on `PATH` is 2.1.241 and flags `claude-haiku-5-5` as an unrecognized model. The desktop app uses 2.1.293, which is published on npm. The launch pins 2.1.293 in a separate prefix (`~/.local/claude-code-2.1.293`), leaving the global CLI that other platforms' sessions use unchanged.
3. `~/.zshrc` exports `ANTHROPIC_BASE_URL` with host `api.deepseek.com`, together with an auth token and model-name remaps (values not recorded). A `claude` process started from an ordinary terminal would therefore run DeepSeek models under any requested Claude model name, which is exactly the prohibited "non-Claude model under a Claude identity" path. The role process inherits no environment variable (`env -i`) and must hold first-party OAuth.
4. Shells spawned by the desktop app export the desktop's cross-session messaging socket and token. A role started from such a shell could reach other local sessions, so the launcher refuses to run inside a Claude session.
5. `--bare` was rejected because it requires an API key, which means paid API usage. `--safe-mode` keeps subscription authentication while disabling `CLAUDE.md`, third-party plugins (including the globally enabled Codex plugin), skills, hooks and MCP servers.
6. The host clock runs 54,000 s (15 h) behind NTP, GitHub and Anthropic server time. Timestamps in this run's manifest are corrected; git commit dates written on this host are not. A large skew can also break OAuth sign-in.
7. Probes run during this check: two headless calls in an empty scratch directory, one per CLI version. Neither reached a model (not signed in; unrecognized model), so no model output exists.

## Isolation controls

The operator runs `launch.sh` from Terminal.app. It aborts unless every check passes:

- CLI version 2.1.293 and the reviewed SHA-256 of the native binary.
- `launch-settings.json` byte-identical to the reviewed and smoke-tested digest `f5622a13e7275540a87bfd12baa7972a2a38545103659faf14b3460645ee16de`. A Codex review comment on `7a99ca1` noted that the launcher only printed this digest; it now aborts on mismatch.
- First-party Claude subscription sign-in (`authMethod` `claude.ai`, `apiProvider` `firstParty`). After the operator signed in, `auth status` reported subscription type `pro`.
- Packet digest and all 31 file hashes, with no extra file and no writable path.
- An empty outbox with mode 0700.
- No earlier session for the packet directory.

It then starts the CLI with:

- `env -i`, so the role inherits no variable from the caller;
- `SHELL=/bin/bash`, so the zsh profile is not sourced;
- auto-memory off (`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` and `autoMemoryEnabled: false`);
- `--safe-mode`, `--strict-mcp-config`, `--setting-sources project` and `--settings launch-settings.json`;
- `--tools Bash,Read,Write,Edit,WebSearch,WebFetch`, a built-in tool allow-list, so no other tool exists in the session;
- the packet as the working directory and the outbox via `--add-dir`;
- `--model claude-opus-5-5`, `--effort xhigh` and the pre-assigned `--session-id 76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`.

`launch-settings.json` adds these controls:

- **Denied tools (second layer behind the allow-list):** sub-agents (`Task`, `Agent`), messaging (`SendMessage`, `ListAgents`), remote routines (`RemoteTrigger`, which appears only after sign-in), workflows, skills, scheduling and monitoring, notifications, artifact publishing, worktrees and notebook editing.
- **Writes:** allowed only in the outbox. Edits are denied in every packet, every repository checkout and every other actor's outbox.
- **Reads:** denied for repository checkouts, other packets and export records, other actors' outboxes, every home dot-directory (Claude, Codex and shell state), `~/Library` (desktop transcripts) and the coordinator's temporary tree.
- **Bash:** runs in the macOS sandbox with `failIfUnavailable` and no unsandboxed escape. The sandbox denies reading anything under the home directory except the packet and outbox, denies writes to the packet and has no network.
- **Web:** `WebSearch` and `WebFetch` are pre-approved because literature search needs them.

Known limits:

- The role runs as the same macOS user, not in a container or separate account. Tool permissions and the seatbelt sandbox are enforcement layers inside Claude Code, not a security boundary, consistent with `docs/ISOLATION.md` and the packet's own "no OS sandbox claim".
- The `Read` rules are a deny-list. Reads of unlisted paths outside the packet and outbox still need the operator's interactive approval, which is a human control.
- Web tools can reach the public repository. The actor is instructed not to inspect other agents' material, and the repository currently holds no proposal or challenge text.
- The role transcript is stored under `~/.claude/projects/`. The coordinator can technically read it and records here that it will not.
- `WebFetch` returns page content processed by a Claude helper model: both test runs billed `claude-haiku-5-5` next to `claude-opus-5-5`. Bash has no network, so raw downloads are unavailable. The proposer must record each source's access level and check quoted locators.
- Claude Code tries to create `.claude/.cc-writes`, a staging folder for atomic writes, in its working directory. The packet directories are read-only, so this fails harmlessly and outbox writes still succeed (verified in run 2). When the CLI asks for a permission, the operator should choose the one-time "Yes"; "don't ask again" would try to save project settings into the read-only packet.

## Isolation test results

`isolation_smoke.py` runs one headless session of the pinned CLI on a synthetic fixture with no project content. It records pass/fail flags only, never file contents. The two deny rules that cover the coordinator's own temporary tree are dropped in the fixture because the fixture lives there; the same rule form is exercised by the other path rules.

| Run | Configuration | Result |
|---|---|---|
| 1 (`isolation-smoke-run1-writable.json`) | Earlier settings, no `--tools`, writable fixture packet | All 20 step checks passed. Deny rules blocked reads of the repository, other packets, export records, `~/.claude`, `~/Library` and the canary. Bash was sandboxed with no home access, no network and no `ANTHROPIC_*` variables. Writes landed only in the outbox, and `WebFetch` worked. The run also exposed two defects, both since fixed: the CLI itself created `.claude/.cc-writes` in the writable packet, and the signed-in session exposed `RemoteTrigger`. |
| 2 (`isolation-smoke-run2-readonly.json`) | Final settings, `--tools` allow-list, read-only fixture packet as in the real launch | All 20 step checks and all 12 environment checks passed. The session exposed exactly the six allowed tools, ran `claude-opus-5-5` with no API key source, loaded no MCP server or third-party plugin, kept auto-memory off and left the packet unmodified. |

A follow-up probe loaded `launch-settings.json` from its repository path and confirmed that the sandbox engaged: a Bash read of `~/.claude` was denied. The CLI's own settings load is therefore not blocked by the role's `Read` rules. Test timestamps come from the host clock, which is 15 h slow.

## Budget

This stage requests 0 CPU-hours, 0 GPU-hours and USD 0 of API spend from the shared 8 CPU-hour cap; it covers literature and design work only. Agent usage comes from the existing subscription, with no automatic retries. Any experiment needs an accepted topic, the signed task list and a separate allocation record.

## Prerequisites before launch

1. The operator installs the pinned CLI into its own prefix: `npm install --prefix ~/.local/claude-code-2.1.293 @anthropic-ai/claude-code@2.1.293`. This downloads about 236 MB, mostly the native macOS arm64 binary, from the npm registry. Done on 2026-10-12. The operator's npm `allowScripts` policy blocked the package's postinstall step, which only hard-links the native binary over a placeholder. The launcher therefore executes the native binary directly from `@anthropic-ai/claude-code-darwin-arm64` and requires its SHA-256 `4e21122a227857da1178aca3299700c1fd7f2b77c93f12e73c2c76db796a105e`. The binary is signed by Developer ID Application: Anthropic PBC (Q6L2SF6YDW), and `codesign --verify --strict` passes. No npm policy was changed.
2. The operator signs in from Terminal.app with `bash launch.sh --login`, choosing the Claude subscription and never the Console option. Correct the host clock first if sign-in fails. The sign-in is stored in the shared Claude Code configuration. Sessions that export their own `ANTHROPIC_AUTH_TOKEN` (the DeepSeek routing) should keep using that token; the operator should confirm afterwards that DeepSeek sessions still report their DeepSeek model. Done on 2026-10-12: `auth status` reports `claude.ai`, `firstParty`, subscription `pro`.
3. The coordinator runs `python3 -I isolation_smoke.py` against the final configuration. Done: run 2 passed every check (see above).
4. Pending: `M0nitor-EDA` confirms the final head with `CONFIRM <sha>` and the PR is merged.

## Launch sequence

1. After the merge, update the main checkout with `git pull`. From it, in Terminal.app, run `bash runs/CLD-P05-LAUNCH-0001/launch.sh --check` and then `bash runs/CLD-P05-LAUNCH-0001/launch.sh`, and accept the folder-trust prompt for the packet directory. The launcher prints the commit it ran from; record that commit with the session registration.
2. Send the onboarding prompt verbatim. The session writes `readiness.json` and `first-pass-plan.md` to its outbox and stops; no web survey happens in this turn.
3. The coordinator records the observed model and the session in `config/roles.json` and `config/agents-claude.json` through a PR.
4. Send the research prompt verbatim. Output returns only through the outbox, and the coordinator transports it by PR without editing scientific content.

Onboarding prompt:

> You are `Claude-P05-TIMING` (`CLD-Origin-TIMING`), the Claude proposer for EDA-0002 (D05). Your only project input is the frozen packet in your working directory, identified by the SHA-256 of its `PACKET.json`: `ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d`. Read `AGENTS.md`, `ASSIGNMENT.json`, `PACKET.json`, the common policy and only `harness/ONBOARDING.md` and `harness/PROPOSER.md`. Use English. Verify every listed file hash. Record actor ID, actual model ID, role, topic, input commit, packet hash, the isolation controls you can observe and any unlisted context in `readiness.json` and `first-pass-plan.md` in your outbox `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING`. Write only to that outbox. Do not begin a web survey in this turn. Do not inspect another actor's files, converse with another role, approve or merge. Finish the turn after writing both files.

Research prompt (sent only after step 3):

> You are the proposer for EDA-0002. Your only project input is the frozen packet in your working directory, identified by its `PACKET.json` checksum `ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d`. Read `AGENTS.md`, the common policy, the research brief and `harness/PROPOSER.md`. Use English. Independently research the D05 slice and deliver the full dossier for at most one candidate to your outbox `/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING`. Treat unknown resources as unknown. Communicate only through output files; do not inspect other agents, conversations, memories or private notes. Do not approve or merge your work. Log public sources, input provenance and unresolved questions.

## Not authorized by this record

No session exists yet. This record creates or approves no topic, survey result, novelty claim, experiment or verifier session.
