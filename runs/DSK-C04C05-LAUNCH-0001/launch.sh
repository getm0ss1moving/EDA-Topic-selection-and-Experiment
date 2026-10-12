#!/bin/bash
# Fail-closed launcher for the two released DeepSeek challengers, run DSK-C04C05-LAUNCH-0001.
#
#   DeepSeek-C04-PHYSICAL  EDA-0001 / D04 challenger (Codex-P04-PHYSICAL proposes)
#   DeepSeek-C05-TIMING    EDA-0002 / D05 challenger (Claude-P05-TIMING proposes)
#
# Run from your own Terminal.app, never from inside a Claude desktop session or its tabs:
#   bash launch.sh --actor DeepSeek-C05-TIMING --check   verify every precondition, launch nothing
#   bash launch.sh --actor DeepSeek-C05-TIMING           start the fresh role session (pre-assigned ID)
#   bash launch.sh --actor DeepSeek-C05-TIMING --resume  reopen the same session after an interruption
#
# The role process receives no variable from the calling shell (`env -i`), and no API token:
# the credential comes from the macOS Keychain through the apiKeyHelper configured in
# launch-settings-<C04|C05>.json. Only the routing variables are passed explicitly, and they map
# every model alias Claude Code may use (main, opus, sonnet, haiku, subagent) to the DeepSeek
# route, so no request can fall back to the shared claude.ai subscription login.
#
# The launch binding (packet path and digest, outbox, settings digest, session ID) is read from
# actor-launch.json. Packet fields stay PENDING until the corresponding proposal is frozen; the
# launcher refuses to start while any required field is PENDING.
set -euo pipefail

RUN_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_VERSION="2.1.293"
# Separate prefix so the global CLI, which other platforms' sessions also use, stays unchanged.
# The signed native binary is executed directly, so npm's postinstall copy step is not needed.
CLAUDE_BIN="$HOME/.local/claude-code-$CLI_VERSION/node_modules/@anthropic-ai/claude-code-darwin-arm64/claude"
CLI_SHA256="4e21122a227857da1178aca3299700c1fd7f2b77c93f12e73c2c76db796a105e"
# Canonical API model ID served by api.deepseek.com/models (owner decision 2026-10-13):
# pin deepseek-flash itself, not the operator's shell alias deepseek-v4-flash[1m].
MODEL="deepseek-flash"
EFFORT="max"
BASE_URL="https://api.deepseek.com/anthropic"
HELPER="$RUN_DIR/keychain-token.sh"
LAUNCH_CONFIG="$RUN_DIR/actor-launch.json"
# Built-in tool allow-list; the deny rules in launch-settings-<actor>.json are a second layer.
TOOLS="Bash,Read,Write,Edit,WebSearch,WebFetch"
CLEAN_ENV=(HOME="$HOME" USER="$USER" LOGNAME="${LOGNAME:-$USER}" SHELL=/bin/bash
           TERM="${TERM:-xterm-256color}" LANG=en_US.UTF-8 PATH=/usr/bin:/bin:/usr/sbin:/sbin
           CLAUDE_CODE_DISABLE_AUTO_MEMORY=1)
ROUTE_ENV=(ANTHROPIC_BASE_URL="$BASE_URL" ANTHROPIC_MODEL="$MODEL"
           ANTHROPIC_DEFAULT_OPUS_MODEL="$MODEL" ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL"
           ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL" CLAUDE_CODE_SUBAGENT_MODEL="$MODEL")

die() { echo "ABORT: $*" >&2; exit 1; }
ok() { echo "ok    $*"; }

actor=""; mode="launch"
while [ $# -gt 0 ]; do
  case "$1" in
    --actor) actor="${2:-}"; shift 2 ;;
    --check) mode="--check"; shift ;;
    --resume) mode="--resume"; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done
[ -n "$actor" ] || die "usage: bash $0 --actor DeepSeek-C04-PHYSICAL|DeepSeek-C05-TIMING [--check|--resume]"

if [ -n "${CLAUDECODE:-}${CLAUDE_CODE_SESSION_ID:-}${CLAUDE_CODE_MESSAGING_SOCKET:-}" ]; then
  die "called from inside a Claude session; open Terminal.app and run this script there"
fi

[ -x "$CLAUDE_BIN" ] || die "CLI not found at $CLAUDE_BIN; run: npm install --prefix $HOME/.local/claude-code-$CLI_VERSION @anthropic-ai/claude-code@$CLI_VERSION"
[ "$(shasum -a 256 "$CLAUDE_BIN" | awk '{print $1}')" = "$CLI_SHA256" ] || die "CLI binary SHA-256 differs from the reviewed $CLI_SHA256"
version="$( (env -i "${CLEAN_ENV[@]}" "$CLAUDE_BIN" --version 2>/dev/null || true) | awk '{print $1}')"
[ "$version" = "$CLI_VERSION" ] || \
  die "CLI version '$version' is not $CLI_VERSION; run: npm install --prefix $HOME/.local/claude-code-$CLI_VERSION @anthropic-ai/claude-code@$CLI_VERSION"
ok "CLI $version at $CLAUDE_BIN"

IFS=$'\t' read -r A_ACTOR A_ROLE A_TOPIC A_DOMAIN A_STAGE A_PACKET A_PACKET_SHA A_OUTBOX A_SESSION A_SETTINGS A_SETTINGS_SHA < <(
  python3 -I - "$LAUNCH_CONFIG" "$actor" <<'PYEOF'
import json, sys
cfg = json.load(open(sys.argv[1]))
a = (cfg.get('actors') or {}).get(sys.argv[2])
if not a:
    sys.exit(2)
print('\t'.join(str(a.get(k) if a.get(k) is not None else 'PENDING') for k in
      ['actor_id', 'role', 'topic', 'domain', 'stage', 'packet_dir', 'packet_sha256',
       'outbox_dir', 'session_id', 'settings_file', 'settings_sha256']))
PYEOF
) || die "actor $actor is not present in $LAUNCH_CONFIG"
[ "$A_ACTOR" = "$actor" ] || die "launch binding mismatch: config returned '$A_ACTOR'"
ok "binding: $A_ACTOR role=$A_ROLE topic=$A_TOPIC stage=$A_STAGE session=$A_SESSION"

SETTINGS_ABS="$RUN_DIR/$A_SETTINGS"
[ -f "$SETTINGS_ABS" ] || die "settings file missing: $SETTINGS_ABS"
[ "$A_SETTINGS_SHA" != "PENDING" ] || die "settings digest not yet recorded for $A_ACTOR"
[ "$(shasum -a 256 "$SETTINGS_ABS" | awk '{print $1}')" = "$A_SETTINGS_SHA" ] || \
  die "launch settings differ from the reviewed and smoke-tested digest $A_SETTINGS_SHA"
ok "settings $A_SETTINGS_SHA ($A_SETTINGS)"

[ -x "$HELPER" ] || die "apiKeyHelper missing or not executable: $HELPER"
helper_value="$(env -i HOME="$HOME" USER="$USER" "$HELPER" 2>/dev/null || true)"
[ -n "$helper_value" ] || \
  die "Keychain entry 'deepseek-api-key' missing for $USER; run: security add-generic-password -U -s deepseek-api-key -a \"\$USER\" -w \"\$ANTHROPIC_AUTH_TOKEN\""
unset helper_value
ok "Keychain credential resolves through the apiKeyHelper (value never printed)"

AUTH_TMP="$(mktemp -d "${TMPDIR:-/tmp}/dsk-authcheck.XXXXXX")"
mkdir -p "$AUTH_TMP/.claude" && cp "$SETTINGS_ABS" "$AUTH_TMP/.claude/settings.json"
auth="$(cd "$AUTH_TMP" && env -i "${CLEAN_ENV[@]}" "${ROUTE_ENV[@]}" "$CLAUDE_BIN" auth status 2>/dev/null || true)"
rm -rf "$AUTH_TMP"
printf '%s' "$auth" | python3 -I -c '
import json, sys
a = json.load(sys.stdin)
good = (a.get("loggedIn") is True and a.get("apiKeySource") == "apiKeyHelper"
        and a.get("authMethod") not in ("claude.ai", "oauth_token"))
sys.exit(0 if good else 1)' || \
  die "auth does not resolve to the Keychain helper; a claude.ai fallback is not permitted"
ok "auth resolves to apiKeyHelper (DeepSeek Keychain credential; no claude.ai fallback)"

pends=()
[ "$A_PACKET_SHA" = "PENDING" ] && pends+=("packet_sha256 is PENDING: the $A_TOPIC proposal is not frozen yet; at freeze time export the challenger packet with scripts/actor_packet.py (research phase, --stage initial) and record its PACKET.json digest in actor-launch.json")
[ -d "$A_PACKET" ] || pends+=("packet directory does not exist yet: $A_PACKET")

if [ "${#pends[@]}" -eq 0 ]; then
  [ "$(shasum -a 256 "$A_PACKET/PACKET.json" | awk '{print $1}')" = "$A_PACKET_SHA" ] || die "PACKET.json digest mismatch"
  python3 -I - "$A_PACKET" <<'EOF' || die "packet contents do not match PACKET.json"
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
  ok "packet $A_PACKET_SHA: all listed hashes match, no extra files, read-only"
fi

[ -d "$A_OUTBOX" ] || die "outbox missing: $A_OUTBOX"
[ "$(stat -f '%Lp' "$A_OUTBOX")" = "700" ] || die "outbox must be mode 700"
transcripts="$HOME/.claude/projects/$(printf '%s' "$A_PACKET" | tr '/.' '--')"
if [ "$mode" = "--resume" ]; then
  [ -f "$transcripts/$A_SESSION.jsonl" ] || die "no existing session $A_SESSION to resume"
else
  [ -z "$(ls -A "$A_OUTBOX")" ] || die "outbox is not empty; a fresh session requires an empty outbox"
  [ ! -e "$transcripts" ] || die "a Claude Code session already exists for this packet directory"
fi
ok "outbox $A_OUTBOX"
echo "info  launch record commit $(git -C "$RUN_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"

if [ "${#pends[@]}" -gt 0 ]; then
  for p in "${pends[@]}"; do echo "PENDING $p"; done
  if [ "$mode" = "--check" ]; then
    echo "Prepared but not startable by design. Nothing was launched."
    exit 1
  fi
  die "missing launch prerequisites (see PENDING lines above)"
fi

flags=(--safe-mode --strict-mcp-config --setting-sources project --settings "$SETTINGS_ABS"
       --tools "$TOOLS" --add-dir "$A_OUTBOX" --model "$MODEL" --effort "$EFFORT")
if [ "$mode" = "--check" ]; then
  echo "All preconditions hold. Nothing was launched."
  exit 0
fi
cd "$A_PACKET"
if [ "$mode" = "--resume" ]; then
  exec env -i "${CLEAN_ENV[@]}" "${ROUTE_ENV[@]}" "$CLAUDE_BIN" "${flags[@]}" --resume "$A_SESSION"
fi
exec env -i "${CLEAN_ENV[@]}" "${ROUTE_ENV[@]}" "$CLAUDE_BIN" "${flags[@]}" --session-id "$A_SESSION"
