#!/usr/bin/env python3
"""PreToolUse guard for Claude-P05-TIMING (EDA-0002 proposer).

Owner directive, 2026-10-14: the proposer sees challenger output only after verifier
adjudication, released by the coordinator together with that adjudication. Transported
challenger output is public in this project's GitHub repository before adjudication, so this
hook blocks every WebFetch, WebSearch or Bash call that names the repository or its owner
accounts, including percent-encoded spellings and mirror URLs that carry those names. It is
an accidental-exposure guard, not adversarial isolation. It fails closed.

The installed copy is read-only and pinned by SHA-256 in launch.sh. A blocked call is
recorded as time, session, tool and matched name only; call text is never stored.
"""
import datetime
import json
import sys
from urllib.parse import unquote

BLOCKED = ('getm0ss1moving', 'eda-topic-selection', 'm0nitor-eda')
FIELDS = {'WebFetch': 'url', 'WebSearch': 'query', 'Bash': 'command'}
LOG = '/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Guards/Claude-P05-TIMING/blocked-calls.jsonl'
MESSAGE = ('Blocked by the coordinator guard (owner directive 2026-10-14): calls that name this '
           "project's repository or its owner accounts are not allowed in this session. Challenger "
           'output reaches you only in verified packets released by the coordinator. To write text '
           'that merely mentions these names, use the Write tool.')


def main():
    event = json.load(sys.stdin)
    tool = event.get('tool_name')
    text = str((event.get('tool_input') or {}).get(FIELDS.get(tool, ''), ''))
    for _ in range(3):  # percent-encoding may be nested
        text = unquote(text)
    text = text.lower()
    hit = next((name for name in BLOCKED if name in text), None)
    if hit is None:
        return 0
    try:
        with open(LOG, 'a') as f:
            f.write(json.dumps({
                'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'session_id': event.get('session_id'), 'tool': tool, 'matched': hit}) + '\n')
    except OSError:
        pass  # Logging is evidence only; the block does not depend on it.
    sys.stderr.write(MESSAGE + '\n')
    return 2


if __name__ == '__main__':
    try:
        code = main()
    except Exception:
        sys.stderr.write('Blocked: the coordinator guard could not read this call, so it fails closed.\n')
        code = 2
    sys.exit(code)
