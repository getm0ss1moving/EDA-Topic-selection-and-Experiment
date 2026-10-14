#!/bin/bash
# Fail-closed launcher for Claude-P05-TIMING (EDA-0002 / D05 proposer), run CLD-P05-LAUNCH-0001.
#
# Run from your own Terminal.app, never from inside a Claude desktop session or its terminal tabs:
#   bash launch.sh --check    verify every precondition and launch nothing
#   bash launch.sh --check-resume verify resume preconditions and launch nothing
#   bash launch.sh --login    sign this CLI in with the Claude subscription (clean environment)
#   bash launch.sh            start the fresh role session with the pre-assigned session ID
#   bash launch.sh --resume   reopen the same registered session after an interruption
#
# The role process receives no variable from the calling shell: env -i drops ANTHROPIC_* routing
# (for example a DeepSeek-compatible base URL), API keys/tokens and desktop messaging sockets.
#
# Amendment CLD-P05-AMEND-0001 (2026-10-14): --safe-mode is replaced by the DISABLE switches in
# CLEAN_ENV because safe mode also disables the settings hook that keeps the proposer away from
# this project's repository, where challenger output is public before verifier adjudication.
set -euo pipefail

RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_VERSION="2.1.293"
# Separate prefix so the global CLI, which other platforms' sessions also use, stays unchanged.
# The signed native binary is executed directly, so npm's postinstall copy step is not needed.
CLAUDE_BIN="$HOME/.local/claude-code-$CLI_VERSION/node_modules/@anthropic-ai/claude-code-darwin-arm64/claude"
CLI_SHA256="4e21122a227857da1178aca3299700c1fd7f2b77c93f12e73c2c76db796a105e"
MODEL="claude-opus-5-5"
EFFORT="xhigh"
# Built-in tool allow-list; the deny rules in launch-settings.json are a second layer.
TOOLS="Bash,Read,Write,Edit,WebSearch,WebFetch"
SESSION_ID="76d0bf61-78f7-4b93-a557-7c29f1a2cbe8"
PACKET="/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/physical-release-d437c2f66090/Claude-P05-TIMING"
PACKET_SHA256="ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d"
OUTBOX="/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING"
RESULTS="/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/physical-release-d437c2f66090/Claude-P05-TIMING/lab-results"
# Read-only round inbox (docs/AUTO-ROUND.md); the verifier writes its from-verifier folder.
INBOX="/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/rounds/EDA-0002/Claude-P05-TIMING"
# Hashed policy amendment the session must acknowledge (runs/CLD-P05-AMEND-0001).
AMENDMENT="$INBOX/COORDINATOR-AMENDMENT-0001"
AMENDMENT_SHA256="4ea6204028f4c279f3f4f955af889a70fa74ce5da334c87dc844cf0d288b68c5"
SETTINGS="$RUN_DIR/launch-settings.json"
SETTINGS_SHA256="6009cc41dd0d8f8c6714bb81227166d0490632b64a2d92221c790bb96a005cc9"
# PreToolUse hook named in launch-settings.json; installed read-only outside every checkout.
GUARD="/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Guards/Claude-P05-TIMING/repo_guard.py"
GUARD_SHA256="46f2fe7386eab766af9a22638db8281d2c2231b0c8465f370d2e8c7f98708eee"
CLEAN_ENV=(HOME="$HOME" USER="$USER" LOGNAME="${LOGNAME:-$USER}" SHELL=/bin/bash
           TERM="${TERM:-xterm-256color}" LANG=en_US.UTF-8 PATH=/usr/bin:/bin:/usr/sbin:/sbin
           CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 CLAUDE_CODE_DISABLE_CLAUDE_MDS=1
           CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1 DISABLE_AUTOUPDATER=1)

die() { echo "ABORT: $*" >&2; exit 1; }
ok() { echo "ok    $*"; }

mode="${1:-launch}"
case "$mode" in launch|--check|--check-resume|--login|--resume) ;; *) die "unknown mode $mode" ;; esac

if [ -n "${CLAUDECODE:-}${CLAUDE_CODE_SESSION_ID:-}${CLAUDE_CODE_MESSAGING_SOCKET:-}" ]; then
  die "called from inside a Claude session; open Terminal.app and run this script there"
fi

[ -x "$CLAUDE_BIN" ] || die "CLI not found at $CLAUDE_BIN; run: npm install --prefix ~/.local/claude-code-$CLI_VERSION @anthropic-ai/claude-code@$CLI_VERSION"
[ "$(shasum -a 256 "$CLAUDE_BIN" | awk '{print $1}')" = "$CLI_SHA256" ] || die "CLI binary SHA-256 differs from the reviewed $CLI_SHA256"
version="$( (env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" --version 2>/dev/null || true) | awk '{print $1}')"
[ "$version" = "$CLI_VERSION" ] || \
  die "CLI version '$version' is not $CLI_VERSION; run: npm install --prefix ~/.local/claude-code-$CLI_VERSION @anthropic-ai/claude-code@$CLI_VERSION"
ok "CLI $version at $CLAUDE_BIN"

if [ "$mode" = "--login" ]; then
  exec env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" auth login --claudeai
fi

auth="$(env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" auth status 2>/dev/null || true)"
python3 -I -c '
import json, sys
a = json.loads(sys.argv[1] or "{}")
sys.exit(0 if a.get("loggedIn") is True and a.get("authMethod") == "claude.ai"
         and a.get("apiProvider") == "firstParty" else 1)' "$auth" || \
  die "not signed in with a first-party Claude subscription; run: bash $0 --login"
ok "first-party Claude subscription sign-in (no API key, no third-party base URL in the role environment)"

[ "$(shasum -a 256 "$PACKET/PACKET.json" | awk '{print $1}')" = "$PACKET_SHA256" ] || die "PACKET.json digest mismatch"
python3 -I - "$PACKET" <<'EOF' || die "packet contents do not match PACKET.json"
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
listed = json.loads((root/'PACKET.json').read_text())['files']
present = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
bad = [n for n, h in listed.items() if hashlib.sha256((root/n).read_bytes()).hexdigest() != h]
extra = sorted(present - set(listed) - {'PACKET.json'})
writable = [str(p) for p in [root, *root.rglob('*')] if p.stat().st_mode & 0o222]
if bad or extra or writable or any((root/n).is_symlink() for n in present):
    sys.exit(f'mismatch={bad} extra={extra} writable={writable}')
EOF
ok "packet $PACKET_SHA256: all listed hashes match, no extra files, read-only"

[ -d "$OUTBOX" ] || die "outbox missing: $OUTBOX"
[ "$(stat -f '%Lp' "$OUTBOX")" = "700" ] || die "outbox must be mode 700"
transcripts="$HOME/.claude/projects/$(printf '%s' "$PACKET" | tr '/.' '--')"
if [ "$mode" = "--resume" ] || [ "$mode" = "--check-resume" ]; then
  [ -f "$transcripts/$SESSION_ID.jsonl" ] || die "no existing session $SESSION_ID to resume"
else
  [ -z "$(ls -A "$OUTBOX")" ] || die "outbox is not empty; a fresh session requires an empty outbox"
  [ ! -e "$transcripts" ] || die "a Claude Code session already exists for this packet directory"
fi
ok "outbox $OUTBOX"
[ -d "$RESULTS" ] || die "read-only lab results folder missing: $RESULTS (initialize the runner first)"
[ "$(stat -f '%Lp' "$RESULTS")" = "700" ] || die "lab results root must be mode 700"
ok "read-only lab results $RESULTS"
[ -d "$INBOX/from-verifier" ] || die "round inbox missing: $INBOX/from-verifier"
[ "$(stat -f '%Lp' "$INBOX")" = "700" ] || die "round inbox must be mode 700"
[ ! -e "$INBOX/from-challenger" ] || die "the proposer inbox must not have a from-challenger folder"
ok "read-only round inbox $INBOX"
[ "$(shasum -a 256 "$AMENDMENT/AMENDMENT.json" 2>/dev/null | awk '{print $1}')" = "$AMENDMENT_SHA256" ] || \
  die "AMENDMENT.json missing or differs from the pinned $AMENDMENT_SHA256"
python3 -I - "$AMENDMENT" <<'EOF' || die "amendment contents do not match AMENDMENT.json"
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
listed = json.loads((root/'AMENDMENT.json').read_text())['files']
present = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
bad = [n for n, h in listed.items() if hashlib.sha256((root/n).read_bytes()).hexdigest() != h]
extra = sorted(present - set(listed) - {'AMENDMENT.json'})
writable = [str(p) for p in [root, *root.rglob('*')] if p.stat().st_mode & 0o222]
if bad or extra or writable or any((root/n).is_symlink() for n in present):
    sys.exit(f'mismatch={bad} extra={extra} writable={writable}')
EOF
ok "policy amendment $AMENDMENT_SHA256: all listed hashes match, no extra files, read-only"

[ -f "$SETTINGS" ] || die "settings file missing: $SETTINGS"
[ "$(shasum -a 256 "$SETTINGS" | awk '{print $1}')" = "$SETTINGS_SHA256" ] || \
  die "launch-settings.json differs from the pinned $SETTINGS_SHA256"
ok "settings $SETTINGS_SHA256 (digest pinned; final smoke is a separate governance gate)"
[ -f "$GUARD" ] && [ ! -L "$GUARD" ] || die "repository guard missing: $GUARD"
[ "$(shasum -a 256 "$GUARD" | awk '{print $1}')" = "$GUARD_SHA256" ] || die "repository guard differs from the pinned $GUARD_SHA256"
[ "$(stat -f '%Lp' "$GUARD")" = "444" ] || die "repository guard must be mode 444"
ok "repository guard $GUARD_SHA256"
echo "info  launch record commit $(git -C "$RUN_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"

flags=(--strict-mcp-config --setting-sources project --settings "$SETTINGS"
       --tools "$TOOLS" --add-dir "$OUTBOX" --add-dir "$RESULTS" --add-dir "$INBOX"
       --model "$MODEL" --effort "$EFFORT")
if [ "$mode" = "--check" ] || [ "$mode" = "--check-resume" ]; then
  echo "All preconditions hold. Nothing was launched."
  exit 0
fi
cd "$PACKET"
if [ "$mode" = "--resume" ]; then
  exec env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" "${flags[@]}" --resume "$SESSION_ID"
fi
exec env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" "${flags[@]}" --session-id "$SESSION_ID"
