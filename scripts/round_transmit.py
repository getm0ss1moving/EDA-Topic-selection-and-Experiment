#!/usr/bin/env python3
"""Local round transport between the three scientific roles (auto research mode).

Owner directives, 2026-10-14 (docs/AUTO-ROUND.md). After freezing a release with
role_submission.py, the releasing role runs `send`, which copies the verified release into
the next roles' inboxes on this host, so a round needs no GitHub update. Each role watches its
own inbox with `wait`, normally as a background command. Routing is fixed here, not by config:

  proposer   -> challenger and verifier: the proposer release
  challenger -> verifier only: the challenger release
  verifier   -> proposer: the verifier release plus the challenger releases it adjudicated
                (the verified challenge packet); challenger: the verifier release

A proposer therefore never receives challenger output without the verifier's adjudication.
Every inbox has one `from-<role>` folder per permitted sender. Each platform's sandbox lets a
role read only its own inbox and write only its own `from-<role>` folders elsewhere; those
sandbox rules, not this program, are the access boundary. Delivery checks catch mistakes and
misrouting, not a malicious actor on the same OS account.
"""
import argparse
import datetime
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time

HERE = Path(__file__).absolute().parent
_spec = importlib.util.spec_from_file_location('role_submission', HERE / 'role_submission.py')
rs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rs)

ROLES = ('proposer', 'challenger', 'verifier')
ROUTES = {'proposer': ('challenger', 'verifier'), 'challenger': ('verifier',),
          'verifier': ('proposer', 'challenger')}
KINDS = {('proposer', 'challenger'): 'proposer-release', ('proposer', 'verifier'): 'proposer-release',
         ('challenger', 'verifier'): 'challenger-release',
         ('verifier', 'proposer'): 'verified-challenge', ('verifier', 'challenger'): 'verification'}
SUB = re.compile(r'SUB-[0-9a-f]{64}')
DLV = re.compile(r'DLV-\d{8}T\d{6}Z-(proposer|challenger|verifier)-[0-9a-f]{12}')


def no_symlinks(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in [path, *path.parents]):
        raise ValueError('Symlink in delivery path')
    return path


def utc(fmt='%Y-%m-%dT%H:%M:%SZ'):
    return datetime.datetime.now(datetime.timezone.utc).strftime(fmt)


def load_config(path):
    cfg = json.loads(Path(path).read_text())
    if cfg.get('schema') != 1 or not isinstance(cfg.get('topics'), dict):
        raise ValueError('Invalid round-transport config')
    for topic, entry in cfg['topics'].items():
        if entry.get('challenger_stage') not in {'initial', 'full'}:
            raise ValueError(f'{topic}: challenger_stage must be initial or full')
        for role in ROLES:
            r = entry.get('roles', {}).get(role, {})
            if not all(isinstance(r.get(k), str) and r[k] for k in ('actor_id', 'session_id', 'inbox')) \
                    or not r['inbox'].startswith('/'):
                raise ValueError(f'{topic}: incomplete {role} entry')
    return cfg


def topic_entry(cfg, topic):
    if topic not in cfg['topics']:
        raise ValueError(f'{topic} is not configured for round transport')
    return cfg['topics'][topic]


def checked_release(snapshot, entry, role, topic):
    m, payload = rs.verify(snapshot)
    want = entry['roles'][role]
    if (m['role'], m['topic'], m['actor_id'], m['session_id']) != (role, topic, want['actor_id'], want['session_id']):
        raise ValueError(f'{Path(snapshot).name}: not a {topic} release of the configured {role}')
    return m, payload


def verification_text(payload):
    return payload.get('verification.md', b'') + payload.get('verification.json', b'')


def write_delivery(entry, topic, sender, recipient, releases, adjudicates):
    """Create <recipient inbox>/from-<sender>/DLV-... atomically; never lists the target folder."""
    # Coordinator provisions trusted destination directories. Sender is write-only:
    # do not stat/list/read them here; receiver rejects symlink routes before reading.
    target = Path(entry['roles'][recipient]['inbox']) / f'from-{sender}'
    name = f"DLV-{utc('%Y%m%dT%H%M%SZ')}-{sender}-{releases[0][0].name[4:16]}"
    record = {'schema': 1, 'delivery_id': name, 'topic': topic, 'kind': KINDS[(sender, recipient)],
              'from': {'role': sender, 'actor_id': entry['roles'][sender]['actor_id'],
                       'session_id': entry['roles'][sender]['session_id']},
              'to': {'role': recipient, 'actor_id': entry['roles'][recipient]['actor_id']},
              'releases': [{'id': snap.name, 'role': m['role'], 'actor_id': m['actor_id']}
                           for snap, m, _ in releases],
              'adjudicates': list(adjudicates), 'created_at_utc': utc(),
              'transmitter_sha256': rs.sha(Path(__file__).read_bytes())}
    try:
        tmp = Path(tempfile.mkdtemp(prefix='.pending-', dir=str(target)))
    except FileNotFoundError:
        raise ValueError(f'Inbox folder missing: {target} (coordinator setup)')
    try:
        for snap, m, payload in releases:
            folder = tmp / snap.name
            folder.mkdir()
            for n, body in {**payload, 'SUBMISSION.json': rs.encoded(m)}.items():
                (folder / n).write_bytes(body)
                (folder / n).chmod(0o444)
            folder.chmod(0o555)
        (tmp / 'DELIVERY.json').write_bytes(rs.encoded(record))
        (tmp / 'DELIVERY.json').chmod(0o444)
        tmp.chmod(0o555)
        os.rename(tmp, target / name)  # Atomic visibility: readers ignore .pending-*.
    except BaseException:
        try:  # A sender may lack read access here; a leftover .pending-* folder is inert.
            for p in [tmp, *tmp.rglob('*')]:
                p.chmod(0o755 if p.is_dir() else 0o644)
            shutil.rmtree(tmp)
        except OSError:
            pass
        raise
    return name


def send(config, release, adjudicates=(), ledger=None):
    release = Path(release).absolute()
    m, payload = rs.verify(release)
    cfg = load_config(config)
    topic = m['topic']
    entry = topic_entry(cfg, topic)
    role = m['role']
    checked_release(release, entry, role, topic)
    if role == 'verifier' and not adjudicates:
        raise ValueError('Name the challenger releases this verification adjudicates (--adjudicates SUB-...)')
    if role != 'verifier' and adjudicates:
        raise ValueError('Only a verifier release names adjudicated challenger releases')
    included = [(release, m, payload)]
    for sid in adjudicates:
        if not SUB.fullmatch(sid):
            raise ValueError(f'Invalid release ID: {sid}')
        if sid.encode() not in verification_text(payload):
            raise ValueError(f'{sid} is not named in verification.md or verification.json')
        own = Path(entry['roles']['verifier']['inbox']) / 'from-challenger'
        found = sorted(own.glob(f'DLV-*/{sid}'))
        if not found:
            raise ValueError(f'{sid} was not delivered to this verifier by the challenger')
        cm, cp = checked_release(found[-1], entry, 'challenger', topic)
        included.append((found[-1], cm, cp))
    ledger = Path(ledger) if ledger else release.parent.parent / 'transmissions.jsonl'
    done = set()
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            e = json.loads(line)
            if e.get('status') == 'delivered':
                done.add((e['release'], e['to']))
    results = []
    for recipient in ROUTES[role]:
        if (release.name, recipient) in done:
            results.append({'to': recipient, 'status': 'already_delivered'})
            continue
        if role == 'proposer' and recipient == 'challenger' and entry['challenger_stage'] == 'initial':
            # Semantic forecast masking needs the coordinator (docs/ISOLATION.md).
            result = {'to': recipient, 'status': 'held_for_coordinator_forecast_screening'}
        else:
            parts = included if recipient == 'proposer' else included[:1]
            result = {'to': recipient, 'status': 'delivered',
                      'delivery': write_delivery(entry, topic, role, recipient, parts, adjudicates)}
        with open(ledger, 'a') as f:  # Record each outcome at once so a retry never duplicates it.
            f.write(json.dumps({'utc': utc(), 'release': release.name, **result}) + '\n')
        results.append(result)
    return results


def recipient_of(cfg, inbox):
    inbox = str(Path(inbox).absolute())
    for topic, entry in cfg['topics'].items():
        for role in ROLES:
            if entry['roles'][role]['inbox'] == inbox:
                return topic, entry, role
    raise ValueError(f'{inbox} is not a configured inbox')


def validate(path, topic, entry, sender, recipient):
    """Return problems with one delivery; an empty list means it may be opened."""
    try:
        path = no_symlinks(path)
        rec = json.loads(rs.regular(path / 'DELIVERY.json'))
        if not isinstance(rec, dict) or rec.get('schema') != 1:
            return ['Invalid delivery schema']
        if recipient not in ROUTES.get(sender, ()):
            return [f'{sender} may not deliver to the {recipient}']
        problems = []
        if (rec.get('delivery_id'), rec.get('topic'), rec.get('kind')) != (path.name, topic, KINDS[(sender, recipient)]):
            problems.append('delivery record does not match its folder, topic or route')
        if rec.get('from', {}).get('role') != sender or rec.get('to', {}).get('role') != recipient:
            problems.append('delivery record names another sender or recipient')
        for key, actor_role in [('from', sender), ('to', recipient)]:
            if rec.get(key, {}).get('actor_id') != entry['roles'][actor_role]['actor_id']:
                problems.append('delivery actor identity mismatch')
        if rec.get('from', {}).get('session_id') != entry['roles'][sender]['session_id']:
            problems.append('delivery session identity mismatch')
        ids = [r.get('id') for r in rec.get('releases', [])]
        if (not ids or any(not isinstance(sid, str) or not SUB.fullmatch(sid) for sid in ids)
                or len(ids) != len(set(ids))):
            return ['Invalid or duplicate release IDs; payload not opened']
        if {p.name for p in path.iterdir()} != {'DELIVERY.json', *ids}:
            problems.append('unexpected or missing entries')
        roles, texts = [], {}
        for sid in ids:
            m, payload = rs.verify(path / sid)
            want = entry['roles'][m['role']]
            if (m['topic'], m['actor_id'], m['session_id']) != (topic, want['actor_id'], want['session_id']):
                problems.append(f'{sid}: not from the configured {m["role"]}')
            claimed = rec['releases'][len(roles)]
            if (claimed.get('role'), claimed.get('actor_id')) != (m['role'], m['actor_id']):
                problems.append('release descriptor identity mismatch')
            roles.append(m['role'])
            texts[sid] = verification_text(payload)
        if sender in ('proposer', 'challenger') and roles != [sender]:
            problems.append(f'expected exactly one {sender} release')
        if sender == 'verifier':
            if not roles or roles[0] != 'verifier' or roles.count('verifier') != 1:
                problems.append('expected exactly one verifier release, listed first')
            challenged = [sid for sid, role in zip(ids, roles) if role == 'challenger']
            adjudicated = rec.get('adjudicates', [])
            if recipient == 'challenger' and challenged:
                problems.append('a verification delivery to the challenger carries no challenger release')
            if recipient == 'proposer':
                if not challenged or sorted(challenged) != sorted(adjudicated):
                    problems.append('challenger releases must be exactly the adjudicated ones')
                if roles and roles[0] == 'verifier' and not all(s.encode() in texts[ids[0]] for s in challenged):
                    problems.append('the verification record does not name every included challenger release')
            if set(roles) - {'verifier', 'challenger'}:
                problems.append('unexpected release role in a verifier delivery')
        return problems
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        return [f'unreadable or invalid delivery: {e}']


def scan(cfg, inbox):
    topic, entry, role = recipient_of(cfg, inbox)
    root = no_symlinks(inbox)
    found, stray = [], []
    allowed = {f'from-{s}' for s in ROLES if role in ROUTES[s]}
    for sub in sorted(p for p in root.iterdir() if p.name.startswith('from-')):
        if sub.is_symlink() or not sub.is_dir() or sub.name not in allowed:
            stray.append(sub.name)  # Never opened: no sender may write here.
            continue
        for d in sorted(sub.iterdir()):
            if d.name.startswith('.pending-'):
                continue
            if d.is_symlink() or not d.is_dir() or not DLV.fullmatch(d.name):
                stray.append(f'{sub.name}/{d.name}')
                continue
            problems = validate(d, topic, entry, sub.name[5:], role)
            found.append({'delivery': d.name, 'path': str(d), 'from': sub.name[5:],
                          'kind': KINDS.get((sub.name[5:], role)), 'valid': not problems, 'problems': problems})
    found.sort(key=lambda x: x['delivery'])
    return {'topic': topic, 'role': role, 'deliveries': found, 'stray_entries_not_opened': stray}


def wait(config, inbox, after='', timeout=540, interval=10, seen_file=None):
    if timeout < 0 or interval <= 0:
        raise ValueError('timeout must be nonnegative and interval positive')
    seen = set()
    if seen_file is not None:
        data = json.loads(rs.regular(seen_file))
        if not isinstance(data, list) or any(not isinstance(x, str) or not DLV.fullmatch(x) for x in data):
            raise ValueError('seen-file must be a JSON array of acknowledged delivery IDs')
        seen = set(data)
    cfg = load_config(config)
    deadline = time.monotonic() + timeout
    while True:
        state = scan(cfg, inbox)
        new = [d for d in state['deliveries'] if d['valid'] and
               (d['delivery'] not in seen if seen_file is not None else
                d['delivery'] != after and (not after or d['delivery'][4:20] >= after[4:20]))]
        if new:
            return {'status': 'delivered', **new[0], 'stray_entries_not_opened': state['stray_entries_not_opened']}
        if time.monotonic() >= deadline:
            return {'status': 'timeout', 'after': after}
        time.sleep(min(interval, max(0, deadline - time.monotonic())))


def ack(seen_file, delivery):
    """Record a processed delivery in the role's own receipt file, atomically and idempotently."""
    if not DLV.fullmatch(delivery):
        raise ValueError(f'Invalid delivery ID: {delivery}')
    path = Path(seen_file).absolute()
    seen = json.loads(rs.regular(path)) if path.exists() else []
    if not isinstance(seen, list) or any(not isinstance(x, str) or not DLV.fullmatch(x) for x in seen):
        raise ValueError('seen-file must be a JSON array of acknowledged delivery IDs')
    if delivery not in seen:
        seen.append(delivery)
        fd, tmp = tempfile.mkstemp(prefix='.ack-', dir=str(path.parent))
        with os.fdopen(fd, 'w') as f:
            f.write(json.dumps(seen, indent=2) + '\n')
        os.replace(tmp, path)
    return {'acknowledged': delivery, 'count': len(seen)}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    s = sub.add_parser('send', help='deliver a frozen release to the next roles')
    s.add_argument('--config', required=True)
    s.add_argument('--release', required=True)
    s.add_argument('--adjudicates', nargs='*', default=[])
    s.add_argument('--ledger')
    w = sub.add_parser('wait', help='block until a new delivery reaches your inbox')
    w.add_argument('--config', required=True)
    w.add_argument('--inbox', required=True)
    w.add_argument('--after', default='', help='last delivery ID already handled')
    w.add_argument('--seen-file', help='own-outbox JSON array of processed IDs; preferred over --after')
    w.add_argument('--timeout', type=int, default=540)
    w.add_argument('--interval', type=int, default=10)
    c = sub.add_parser('check', help='list your inbox deliveries with their validity')
    c.add_argument('--config', required=True)
    c.add_argument('--inbox', required=True)
    k = sub.add_parser('ack', help='record a processed delivery in your own receipt file')
    k.add_argument('--seen-file', required=True)
    k.add_argument('--delivery', required=True)
    a = p.parse_args()
    try:
        if a.command == 'send':
            out = send(a.config, a.release, a.adjudicates, a.ledger)
        elif a.command == 'wait':
            out = wait(a.config, a.inbox, a.after, a.timeout, a.interval, a.seen_file)
        elif a.command == 'ack':
            out = ack(a.seen_file, a.delivery)
        else:
            out = scan(load_config(a.config), a.inbox)
    except (ValueError, OSError) as e:
        sys.stderr.write(f'round_transmit: {e}\n')
        sys.exit(1)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
