#!/bin/bash
# Fail-closed launcher for Claude-P05-TIMING (EDA-0002 / D05 proposer), run CLD-P05-LAUNCH-0001.
#
# Run from your own Terminal.app, never from inside a Claude desktop session or its terminal tabs:
#   bash launch.sh --check    verify every precondition and launch nothing
#   bash launch.sh --login    sign this CLI in with the Claude subscription (clean environment)
#   bash launch.sh            start the fresh role session with the pre-assigned session ID
#   bash launch.sh --resume   reopen the same registered session after an interruption
#
# The role process receives no variable from the calling shell: env -i drops ANTHROPIC_* routing
# (for example a DeepSeek-compatible base URL), API keys/tokens and desktop messaging sockets.
set -euo pipefail

RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_VERSION="2.1.293"
# Separate prefix so the global CLI, which other platforms' sessions also use, stays unchanged.
CLAUDE_BIN="$HOME/.local/claude-code-$CLI_VERSION/node_modules/.bin/claude"
MODEL="claude-opus-5-5"
EFFORT="xhigh"
SESSION_ID="76d0bf61-78f7-4b93-a557-7c29f1a2cbe8"
PACKET="/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Packets/physical-release-d437c2f66090/Claude-P05-TIMING"
PACKET_SHA256="ff20816f623585d4bf7ba7b13d79db58aab90a2e947cd05c719cd93f3574602d"
OUTBOX="/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING"
SETTINGS="$RUN_DIR/launch-settings.json"
CLEAN_ENV=(HOME="$HOME" USER="$USER" LOGNAME="${LOGNAME:-$USER}" SHELL=/bin/bash
           TERM="${TERM:-xterm-256color}" LANG=en_US.UTF-8 PATH=/usr/bin:/bin:/usr/sbin:/sbin
           CLAUDE_CODE_DISABLE_AUTO_MEMORY=1)

die() { echo "ABORT: $*" >&2; exit 1; }
ok() { echo "ok    $*"; }

mode="${1:-launch}"
case "$mode" in launch|--check|--login|--resume) ;; *) die "unknown mode $mode" ;; esac

if [ -n "${CLAUDECODE:-}${CLAUDE_CODE_SESSION_ID:-}${CLAUDE_CODE_MESSAGING_SOCKET:-}" ]; then
  die "called from inside a Claude session; open Terminal.app and run this script there"
fi

[ -x "$CLAUDE_BIN" ] || die "CLI not found at $CLAUDE_BIN"
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
sys.exit(0 if a.get("loggedIn") is True and a.get("authMethod") == "oauth"
         and a.get("apiProvider") == "firstParty" else 1)' "$auth" || \
  die "not signed in with first-party Claude subscription OAuth; run: bash $0 --login"
ok "first-party OAuth sign-in (no API key, no third-party base URL in the role environment)"

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
if [ "$mode" = "--resume" ]; then
  [ -f "$transcripts/$SESSION_ID.jsonl" ] || die "no existing session $SESSION_ID to resume"
else
  [ -z "$(ls -A "$OUTBOX")" ] || die "outbox is not empty; a fresh session requires an empty outbox"
  [ ! -e "$transcripts" ] || die "a Claude Code session already exists for this packet directory"
fi
ok "outbox $OUTBOX"

[ -f "$SETTINGS" ] || die "settings file missing: $SETTINGS"
echo "info  settings sha256 $(shasum -a 256 "$SETTINGS" | awk '{print $1}')"
echo "info  launch record commit $(git -C "$RUN_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"

flags=(--safe-mode --strict-mcp-config --setting-sources project --settings "$SETTINGS"
       --add-dir "$OUTBOX" --model "$MODEL" --effort "$EFFORT")
if [ "$mode" = "--check" ]; then
  echo "All preconditions hold. Nothing was launched."
  exit 0
fi
cd "$PACKET"
if [ "$mode" = "--resume" ]; then
  exec env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" "${flags[@]}" --resume "$SESSION_ID"
fi
exec env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" "${flags[@]}" --session-id "$SESSION_ID"
