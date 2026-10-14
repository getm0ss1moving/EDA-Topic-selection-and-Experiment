#!/usr/bin/env python3
"""Synthetic proposer -> challenger -> verifier -> proposer circuit with three live sessions.

Starts three headless sessions of the pinned Claude Code CLI on a throwaway fixture, with no
scientific content. Each session runs in its own sandbox: the proposer with settings derived
from runs/CLD-P05-LAUNCH-0001/launch-settings.json; the challenger and verifier with stand-in
settings that grant exactly what config/round-transport.json asks of their platforms (read the
own inbox; write only the own outbox and the own from-<role> folders elsewhere). Every session
freezes and transmits with the trusted tools, waits for deliveries as a background command and
acts only when the CLI wakes it. The coordinator side then finds the completed round and builds
its GitHub publication commit in a dry run. The result file records outcomes and IDs only.

The work directory must not contain a name the proposer guard blocks.

    python3 -I circuit_test.py --workdir EXISTING_DIR --out RESULT.json --repo CHECKOUT
"""
import argparse
import datetime
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid

RUN_DIR = Path(__file__).resolve().parent
SCRIPTS = RUN_DIR.parents[1] / 'scripts'
LAUNCH = RUN_DIR.parent / 'CLD-P05-LAUNCH-0001'
HOME = os.path.expanduser('~')
CG = '/Users/duanzeyu/Documents/ChatGPT'
REAL = {'packet': f'{CG}/EDA-Agent-Packets/physical-release-d437c2f66090/Claude-P05-TIMING',
        'outbox': f'{CG}/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING',
        'results': f'{CG}/EDA-Agent-Inboxes/physical-release-d437c2f66090/Claude-P05-TIMING/lab-results',
        'rounds': f'{CG}/EDA-Agent-Inboxes/rounds/EDA-0002'}
ROLE_DIRS = {'proposer': 'Claude-P05-TIMING', 'challenger': 'Codex-C05-TIMING-R2', 'verifier': 'DeepSeek-V02-PHYSICAL'}
IDS = {'proposer': ('Claude-CIRCUIT-P', 'circuit-p'), 'challenger': ('CIRCUIT-C', 'circuit-c'),
       'verifier': ('CIRCUIT-V', 'circuit-v')}
SWITCHES = {'CLAUDE_CODE_DISABLE_AUTO_MEMORY': '1', 'CLAUDE_CODE_DISABLE_CLAUDE_MDS': '1',
            'CLAUDE_CODE_DISABLE_BUNDLED_SKILLS': '1', 'DISABLE_AUTOUPDATER': '1'}
BLOCKED_NAMES = ('getm0ss1moving', 'eda-topic-selection', 'm0nitor-eda')
REF, PACKET = 'a' * 40, 'b' * 64


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def q(path):
    return "'" + str(path).replace("'", "'\\''") + "'"


def stand_in_settings(base, packet, outbox, inbox, writes, foreign):
    """Challenger/verifier stand-in: the proposer's controls with that role's own grants."""
    deny_tools = [r for r in base['permissions']['deny'] if '(' not in r]
    return {'autoMemoryEnabled': False,
            'permissions': {'defaultMode': 'dontAsk', 'blockReadsOutsideWorkingDirectories': True,
                            'allow': [f'Read(/{inbox}/**)', f'Write(/{outbox}/**)', f'Edit(/{outbox}/**)'],
                            'deny': deny_tools + [f'Edit(/{inbox}/**)', f'Write(/{inbox}/**)']
                            + [f'Read(/{x}/**)' for x in foreign]},
            'sandbox': {'enabled': True, 'failIfUnavailable': True, 'allowUnsandboxedCommands': False,
                        'autoAllowBashIfSandboxed': True,
                        'filesystem': {'denyRead': [HOME], 'allowRead': [str(packet), str(outbox), str(inbox)],
                                       'denyWrite': [str(packet), str(inbox)],
                                       'allowWrite': [str(outbox), *map(str, writes)]},
                        'network': {'allowedDomains': [], 'strictAllowlist': True}}}


def prompts(tools, cfg, inbox, out):
    rt_cmd, rs_cmd = f'python3 {q(tools / "round_transmit.py")}', f'python3 {q(tools / "role_submission.py")}'
    def wait(role):
        return (f'{rt_cmd} wait --config {q(cfg)} --inbox {q(inbox[role])} '
                f'--seen-file {q(out[role] / "processed-deliveries.json")} --timeout 1500 --interval 5')
    def ack(role):
        return f'{rt_cmd} ack --seen-file {q(out[role] / "processed-deliveries.json")} --delivery <that delivery ID>'
    def freeze(role):
        actor, session = IDS[role]
        return (f'{rs_cmd} freeze --source {q(out[role] / "release")} --queue {q(out[role] / "submissions")} '
                f'--role {role} --actor {actor} --session {session} --topic EDA-0002 --ref {REF} --packet {PACKET}')
    send = f'{rt_cmd} send --config {q(cfg)} --release <the release path that the freeze command printed>'
    head = ('SYNTHETIC ROUND CIRCUIT TEST, {role} stand-in. There is no research task. Follow the steps '
            'exactly, use exactly the commands given, and do not poll or sleep while waiting: a background '
            'command wakes you when it finishes.\n')
    background = ('Bash tool with run_in_background set to true: {cmd}\nThen end your turn immediately.')
    return {
        'proposer': head.format(role='proposer') +
            f'1. Bash tool: {freeze("proposer")}\n2. Bash tool: {send}\n3. '
            + background.format(cmd=wait('proposer')) +
            '\n4. When the wait reports a delivery, use the Read tool on the DELIVERY.json inside the delivery '
            f'path it printed. Then use the Write tool to create {out["proposer"] / "circuit-result.json"} '
            'containing exactly the "delivery", "kind" and "valid" values from the wait output as one JSON '
            f'object. Then Bash tool: {ack("proposer")}. Reply DONE.',
        'challenger': head.format(role='challenger') +
            '1. ' + background.format(cmd=wait('challenger')) +
            '\n2. When the wait reports a valid proposer-release delivery: use the Read tool on the DELIVERY.json '
            'inside its delivery path and note the release ID listed under "releases". Use the Write tool three '
            f'times: {out["challenger"] / "release" / "challenges.md"} with the text "Synthetic objection to '
            f'<that release ID>."; {out["challenger"] / "release" / "sources.json"} with the text []; and '
            f'{out["challenger"] / "release" / "search-log.md"} with the text "Synthetic search log." Then '
            f'Bash tool: {freeze("challenger")}. Then Bash tool: {send}. Then Bash tool: {ack("challenger")}. '
            'Then ' + background.format(cmd=wait('challenger')) +
            '\n3. When the wait reports a valid verification delivery, use the Write tool to create '
            f'{out["challenger"] / "circuit-result.json"} containing exactly the "delivery", "kind" and '
            f'"valid" values from the wait output as one JSON object. Then Bash tool: {ack("challenger")}. '
            'Reply DONE.',
        'verifier': head.format(role='verifier') +
            '1. ' + background.format(cmd=wait('verifier')) +
            '\n2. Each time the wait reports a delivery:\n'
            f'- kind "proposer-release": Bash tool: {ack("verifier")}. Then '
            + background.format(cmd=wait('verifier')) +
            '\n- kind "challenger-release": use the Read tool on the DELIVERY.json inside its delivery path and '
            'note the challenger release ID listed under "releases". Use the Write tool twice: '
            f'{out["verifier"] / "release" / "verification.md"} with the text "Synthetic adjudication of '
            f'<that challenger release ID>."; and {out["verifier"] / "release" / "verification.json"} with the '
            f'text {{}}. Then Bash tool: {freeze("verifier")}. Then Bash tool: {send} --adjudicates '
            f'<that challenger release ID>. Then Bash tool: {ack("verifier")}. Reply DONE.'}


def parse(stdout):
    init, results, notes, uses = {}, [], 0, []
    for line in stdout.splitlines():
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        if not isinstance(msg, dict):
            continue
        if msg.get('type') == 'system' and msg.get('subtype') == 'init':
            init = init or msg
        elif msg.get('type') == 'system' and msg.get('subtype') == 'task_notification':
            notes += 1
        elif msg.get('type') == 'result':
            results.append({'subtype': msg.get('subtype'), 'is_error': msg.get('is_error'),
                            'turns': msg.get('num_turns'), 'text': str(msg.get('result'))[:200]})
        message = msg.get('message')
        if isinstance(message, dict):
            for block in message.get('content') or []:
                if isinstance(block, dict) and block.get('type') == 'tool_use':
                    uses.append(block.get('name'))
    return {'model': init.get('model'), 'permission_mode': init.get('permissionMode'), 'tools': init.get('tools'),
            'mcp_servers': init.get('mcp_servers'), 'plugins': [p.get('name') for p in init.get('plugins') or []],
            'wake_notifications': notes, 'result_events': results, 'tool_calls': len(uses)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--cli', default=f'{HOME}/.local/claude-code-2.1.293/node_modules/@anthropic-ai/'
                                     'claude-code-darwin-arm64/claude')
    ap.add_argument('--model', default='claude-sonnet-5-5')
    ap.add_argument('--effort', default='low')
    ap.add_argument('--workdir', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--repo', type=Path, help='checkout for the publication dry run')
    ap.add_argument('--timeout', type=int, default=2400)
    args = ap.parse_args()
    if any(n in str(args.workdir.resolve()).lower() for n in BLOCKED_NAMES):
        raise SystemExit('Choose a work directory whose path names no blocked repository or account.')
    rt, rp = load('round_transmit'), load('round_publish')
    rs = rt.rs

    root = args.workdir.resolve() / f'circuit-{uuid.uuid4().hex[:8]}'
    rounds = root / 'rounds' / 'EDA-0002'
    inbox = {role: rounds / name for role, name in ROLE_DIRS.items()}
    packet = {role: root / 'packets' / role for role in rt.ROLES}
    out = {role: root / 'outboxes' / role for role in rt.ROLES}
    results_dir = root / 'lab-results'
    for role in rt.ROLES:
        for sender in rt.ROLES:
            if role in rt.ROUTES[sender]:
                (inbox[role] / f'from-{sender}').mkdir(parents=True)
        packet[role].mkdir(parents=True)
        (packet[role] / 'README.txt').write_text('SYNTHETIC CIRCUIT PACKET\n')
        (out[role] / 'release').mkdir(parents=True)
        (out[role] / 'processed-deliveries.json').write_text('[]\n')
        out[role].chmod(0o700)
    results_dir.mkdir()
    config = {'schema': 1, 'topics': {'EDA-0002': {'challenger_stage': 'full', 'roles': {
        role: {'actor_id': IDS[role][0], 'session_id': IDS[role][1], 'inbox': str(inbox[role])} for role in rt.ROLES}}}}
    tools = {}
    for role in rt.ROLES:  # Each role receives its own read-only copy of the trusted tools and config.
        bundle = inbox[role] / 'COORDINATOR-TOOLS'
        bundle.mkdir()
        for name in ('role_submission.py', 'round_transmit.py'):
            shutil.copy2(SCRIPTS / name, bundle / name)
        (bundle / 'round-transport.json').write_text(json.dumps(config, indent=2) + '\n')
        for p in [*bundle.iterdir(), bundle]:
            p.chmod(0o555 if p.is_dir() else 0o444)
        tools[role] = bundle
    for name in sorted(rs.REQUIRED['proposer']):
        (out['proposer'] / 'release' / name).write_text('[]\n' if name.endswith('.json') else f'Synthetic {name}\n')
    for role in rt.ROLES:
        for p in [*packet[role].iterdir(), packet[role]]:
            p.chmod(0o555 if p.is_dir() else 0o444)

    real = json.loads((LAUNCH / 'launch-settings.json').read_text())
    text = json.dumps(real)
    for key, path in (('packet', packet['proposer']), ('outbox', out['proposer']), ('results', results_dir),
                      ('rounds', rounds)):
        text = text.replace(REAL[key], str(path))
    settings = {'proposer': json.loads(text),
                'challenger': stand_in_settings(real, packet['challenger'], out['challenger'], inbox['challenger'],
                                                [inbox['verifier'] / 'from-challenger'],
                                                [inbox['proposer'], inbox['verifier']]),
                'verifier': stand_in_settings(real, packet['verifier'], out['verifier'], inbox['verifier'],
                                              [inbox['proposer'] / 'from-verifier', inbox['challenger'] / 'from-verifier'],
                                              [inbox['proposer'], inbox['challenger']])}
    env = {'HOME': HOME, 'USER': os.environ.get('USER', ''), 'LOGNAME': os.environ.get('USER', ''),
           'SHELL': '/bin/bash', 'TERM': 'dumb', 'LANG': 'en_US.UTF-8', 'PATH': '/usr/bin:/bin:/usr/sbin:/sbin',
           **SWITCHES}
    texts = {role: prompts(tools[role], tools[role] / 'round-transport.json', inbox, out)[role] for role in rt.ROLES}
    procs, logs, started = {}, {}, {}
    for role in ('challenger', 'verifier', 'proposer'):  # receivers wait first, then the proposer starts the round
        path = root / f'settings-{role}.json'
        path.write_text(json.dumps(settings[role], indent=2))
        dirs = [out[role], inbox[role]] + ([results_dir] if role == 'proposer' else [])
        cmd = [args.cli, '-p', texts[role], '--strict-mcp-config', '--setting-sources', 'project',
               '--settings', str(path), '--tools', 'Bash,Read,Write,Edit' if role != 'proposer'
               else 'Bash,Read,Write,Edit,WebSearch,WebFetch',
               *[x for d in dirs for x in ('--add-dir', str(d))], '--model', args.model, '--effort', args.effort,
               '--output-format', 'stream-json', '--verbose', '--max-turns', '40']
        logs[role] = open(root / f'stream-{role}.jsonl', 'w')
        started[role] = utc()
        procs[role] = subprocess.Popen(cmd, cwd=packet[role], env=env, stdin=subprocess.DEVNULL,
                                       stdout=logs[role], stderr=subprocess.STDOUT, text=True)
        time.sleep(15 if role != 'proposer' else 0)
    deadline, finished = time.monotonic() + args.timeout, {}
    while len(finished) < 3 and time.monotonic() < deadline:
        for role, proc in procs.items():
            if role not in finished and proc.poll() is not None:
                finished[role] = utc()
        time.sleep(5)
    for role, proc in procs.items():
        if proc.poll() is None:
            proc.kill()
        logs[role].close()

    sessions = {role: {**parse((root / f'stream-{role}.jsonl').read_text()), 'started_at_utc': started[role],
                       'finished_at_utc': finished.get(role), 'exit_code': procs[role].returncode}
                for role in rt.ROLES}
    cfg = rt.load_config(tools['proposer'] / 'round-transport.json')
    state = {role: rt.scan(cfg, inbox[role]) for role in rt.ROLES}
    kinds = {role: sorted(d['kind'] for d in state[role]['deliveries']) for role in rt.ROLES}

    def result(role):
        try:
            return json.loads((out[role] / 'circuit-result.json').read_text())
        except (OSError, ValueError):
            return None

    found = rp.rounds(cfg, 'EDA-0002')
    publication = None
    if found and args.repo:
        registry = root / 'synthetic-registry.json'
        registry.write_text(json.dumps({'sessions': [
            {'session_id': IDS[r][1], 'actor_id': IDS[r][0], 'role': r, 'topic': 'EDA-0002',
             'input_commit': REF, 'packet_sha256': PACKET} for r in rt.ROLES]}))
        try:
            publication = rp.publish_round(found[0], args.repo, root / 'ledger.jsonl', dry_run=True,
                                           registry_file=registry)
        except Exception as e:  # recorded, not raised: the report must still be written
            publication = {'error': str(e)}
    verified = next((d for d in state['proposer']['deliveries'] if d['kind'] == 'verified-challenge'), None)
    order = [d['delivery'][4:20] for d in (
        next((d for d in state['challenger']['deliveries'] if d['kind'] == 'proposer-release'), None),
        next((d for d in state['verifier']['deliveries'] if d['kind'] == 'challenger-release'), None), verified) if d]
    checks = {
        'all_sessions_exited_cleanly': all(s['exit_code'] == 0 for s in sessions.values()),
        'sessions_in_dont_ask_mode_without_mcp': all(s['permission_mode'] == 'dontAsk' and s['mcp_servers'] == []
                                                     for s in sessions.values()),
        'every_delivery_valid': all(d['valid'] for s in state.values() for d in s['deliveries']),
        'no_stray_inbox_entries': all(not s['stray_entries_not_opened'] for s in state.values()),
        'proposer_received_only_the_verified_challenge': kinds['proposer'] == ['verified-challenge'],
        'challenger_received_proposal_and_verification': kinds['challenger'] == ['proposer-release', 'verification'],
        'verifier_received_proposal_and_challenge': kinds['verifier'] == ['challenger-release', 'proposer-release'],
        'deliveries_in_circuit_order': len(order) == 3 and order == sorted(order),
        'proposer_woke_and_recorded_the_verified_challenge':
            sessions['proposer']['wake_notifications'] >= 1 and (result('proposer') or {}).get('kind') == 'verified-challenge'
            and (result('proposer') or {}).get('delivery') == (verified or {}).get('delivery'),
        'challenger_woke_twice_and_recorded_the_verification':
            sessions['challenger']['wake_notifications'] >= 2 and (result('challenger') or {}).get('kind') == 'verification',
        'verifier_woke_for_both_deliveries': sessions['verifier']['wake_notifications'] >= 2,
        'receipts_cover_every_delivery': all(
            set(json.loads((out[r] / 'processed-deliveries.json').read_text())) == {d['delivery'] for d in state[r]['deliveries']}
            for r in rt.ROLES),
        'one_completed_round_found': len(found) == 1 and not found[0]['problems'],
        'round_bundle_roles_in_order': bool(found) and [rs.verify(p)[0]['role'] for p in found[0]['releases']]
            == ['proposer', 'challenger', 'verifier'],
        'publication_dry_run_validated': bool(publication) and publication.get('validation') == 'passed',
    }
    report = {'test': 'ROUND-CIRCUIT-0001 synthetic proposer-challenger-verifier-proposer circuit',
              'scientific_content': False, 'model': args.model, 'effort': args.effort,
              'proposer_settings_sha256': rs.sha((LAUNCH / 'launch-settings.json').read_bytes()),
              'transmitter_sha256': rs.sha((SCRIPTS / 'round_transmit.py').read_bytes()),
              'role_submission_sha256': rs.sha((SCRIPTS / 'role_submission.py').read_bytes()),
              'publisher_sha256': rs.sha((SCRIPTS / 'round_publish.py').read_bytes()),
              'sessions': sessions,
              'deliveries': {role: [{k: d[k] for k in ('delivery', 'from', 'kind', 'valid')} for d in state[role]['deliveries']]
                             for role in rt.ROLES},
              'round': found[0] and {k: found[0][k] for k in ('round_id', 'deliveries', 'adjudicates', 'problems')}
              if found else None,
              'round_releases': [Path(p).name for p in found[0]['releases']] if found else [],
              'publication_dry_run': publication, 'checks': checks}
    report['all_pass'] = all(checks.values())
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'all_pass': report['all_pass'], 'failed': [k for k, v in checks.items() if not v],
                      'fixture': str(root)}, indent=2))
    raise SystemExit(0 if report['all_pass'] else 1)


if __name__ == '__main__':
    main()
