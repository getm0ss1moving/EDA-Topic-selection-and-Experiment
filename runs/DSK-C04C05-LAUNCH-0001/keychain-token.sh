#!/bin/sh
# apiKeyHelper for the DeepSeek-routed challenger sessions (DeepSeek-C04-PHYSICAL, DeepSeek-C05-TIMING).
#
# Claude Code executes this with /bin/sh and uses its stdout as the API credential, so the key
# travels from the macOS Keychain to the CLI process without ever entering the role environment.
# Bash subprocesses inside the role inherit the CLI environment; that environment contains no
# token, and this file only holds the Keychain *service name*, never the key.
#
# One-time operator setup (run in your own Terminal.app, not inside any agent session):
#   security add-generic-password -U -s deepseek-api-key -a "$USER" -w "$ANTHROPIC_AUTH_TOKEN"
set -eu
exec /usr/bin/security find-generic-password -s deepseek-api-key -a "${USER:?USER must be set}" -w
