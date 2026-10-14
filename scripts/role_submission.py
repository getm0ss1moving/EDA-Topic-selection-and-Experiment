#!/usr/bin/env python3
"""Freeze role-owned releases; transport verified releases to an intermediate PR.

The actor needs no GitHub credentials. The coordinator invokes publish using its
own checkout/credentials. Neither operation supplies a scientific approval.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile

LIMIT = 8 * 1024 * 1024
TOTAL = 32 * 1024 * 1024
FILES = {
    'proposer': {'proposal.md', 'sources.json', 'search-log.md', 'prior-art.csv',
                 'contest-audit.md', 'industry-gap.md', 'experiment-plan.md',
                 'forecast.json', 'tasklist.md', 'responses.md', 'direction-control.json'},
    'challenger': {'challenges.md', 'sources.json', 'search-log.md', 'prior-art.csv',
                   'independent-estimate.md', 'tasklist.md'},
    'verifier': {'verification.md', 'verification.json'},
}
REQUIRED = {
    'proposer': FILES['proposer'] - {'responses.md'},
    'challenger': {'challenges.md', 'sources.json', 'search-log.md'},
    'verifier': FILES['verifier'],
}


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()


def sha(body):
    return hashlib.sha256(body).hexdigest()


def regular(path):
    # Reject symlinks in every component, including the containing outbox.
    path = Path(path).absolute()
    for parent in [path, *path.parents]:
        if parent.is_symlink():
            raise ValueError(f'Symlink prohibited: {parent}')
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
            raise ValueError('Only regular files may be released')
        body = f.read(LIMIT + 1)
    if len(body) > LIMIT or not body.strip():
        raise ValueError('Empty or oversized release file')
    return body


def validate_manifest(m):
    if m.get('schema') != 1 or m.get('role') not in FILES:
        raise ValueError('Invalid schema/role')
    if not re.fullmatch(r'EDA-\d{4,}', m.get('topic', '')):
        raise ValueError('Invalid topic')
    for key, pattern in [('input_commit', r'[0-9a-f]{40}'), ('packet_sha256', r'[0-9a-f]{64}')]:
        if not re.fullmatch(pattern, m.get(key, '')):
            raise ValueError(f'Invalid {key}')
    for key in ['actor_id', 'session_id']:
        if not isinstance(m.get(key), str) or not m[key].strip():
            raise ValueError(f'Missing {key}')
    names = set(m['files'])
    if not REQUIRED[m['role']] <= names <= FILES[m['role']]:
        raise ValueError('Missing required files or forbidden role output')
    if any(not re.fullmatch(r'[0-9a-f]{64}', h) for h in m['files'].values()):
        raise ValueError('Invalid file hash')


def verify(snapshot):
    snapshot = Path(snapshot)
    m = json.loads(regular(snapshot / 'SUBMISSION.json'))
    validate_manifest(m)
    if set(p.name for p in snapshot.iterdir()) != set(m['files']) | {'SUBMISSION.json'}:
        raise ValueError('Unexpected snapshot entry')
    payload = {n: regular(snapshot / n) for n in m['files']}
    if sum(map(len, payload.values())) > TOTAL:
        raise ValueError('Release exceeds total size cap')
    if any(sha(b) != m['files'][n] for n, b in payload.items()):
        raise ValueError('Frozen release hash mismatch')
    if snapshot.name != 'SUB-' + sha(encoded(m)):
        raise ValueError('Snapshot identity mismatch')
    return m, payload


def freeze(source, queue, role, actor, session, topic, ref, packet):
    source, queue = Path(source).absolute(), Path(queue).absolute()
    if source == queue or source in queue.parents:
        raise ValueError('Queue must be outside the release directory')
    payload = {p.name: regular(p) for p in source.iterdir()}
    m = dict(schema=1, role=role, actor_id=actor, session_id=session,
             topic=topic, input_commit=ref, packet_sha256=packet,
             files={n: sha(b) for n, b in payload.items()})
    validate_manifest(m)
    if sum(map(len, payload.values())) > TOTAL:
        raise ValueError('Release exceeds total size cap')
    queue.mkdir(parents=True, exist_ok=True)
    if any(p.is_symlink() for p in [queue, *queue.parents]):
        raise ValueError('Symlink queue prohibited')
    dest = queue / ('SUB-' + sha(encoded(m)))
    if dest.exists():
        verify(dest)
        return dest
    temp = Path(tempfile.mkdtemp(prefix='.pending-', dir=queue))
    try:
        for name, body in {**payload, 'SUBMISSION.json': encoded(m)}.items():
            (temp / name).write_bytes(body)
            (temp / name).chmod(0o444)
        temp.chmod(0o555)
        temp.rename(dest)  # Atomic visibility: consumers ignore .pending-*.
    except BaseException:
        temp.chmod(0o755)
        shutil.rmtree(temp)
        raise
    verify(dest)
    return dest


def run(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def publish(snapshot, repo):
    m, payload = verify(snapshot)
    repo = Path(repo).resolve()
    run('git', 'fetch', 'origin', 'main', cwd=repo)
    registry = json.loads(run('git', 'show', 'origin/main:config/roles.json', cwd=repo))
    matches = [s for s in registry['sessions'] if s['session_id'] == m['session_id']
               and s.get('actor_id') == m['actor_id'] and s['role'] == m['role']
               and s.get('topic') == m['topic']]
    if len(matches) != 1:
        raise ValueError('Release identity is not the registered topic/role session')
    # Packet amendments must be recorded before using a new packet provenance.
    s = matches[0]
    if (s['input_commit'], s['packet_sha256']) != (m['input_commit'], m['packet_sha256']):
        raise ValueError('Unregistered input packet; register the amendment first')
    submission = Path(snapshot).name
    branch = 'codex/submit-' + submission[4:]
    remote = run('git', 'remote', 'get-url', 'origin', cwd=repo)
    if remote != 'https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment.git':
        raise ValueError('Unexpected repository remote')
    slug = 'getm0ss1moving/EDA-Topic-selection-and-Experiment'
    previous = json.loads(run('gh', 'pr', 'list', '--repo', slug, '--head', branch,
                              '--state', 'all', '--json', 'url'))
    if previous:
        return previous[0]['url']
    with tempfile.TemporaryDirectory(prefix='eda-transport-') as tmp:
        work = Path(tmp) / 'repo'
        run('git', 'clone', '--quiet', '--no-hardlinks', str(repo), str(work))
        run('git', 'remote', 'set-url', 'origin', remote, cwd=work)
        run('git', 'fetch', 'origin', 'main', cwd=work)
        run('git', 'checkout', '-b', branch, 'origin/main', cwd=work)
        dest = work / 'runs' / submission
        dest.mkdir()
        for n, body in {**payload, 'SUBMISSION.json': encoded(m)}.items():
            (dest / n).write_bytes(body)
        run('python3', 'scripts/project.py', 'validate', cwd=work)
        run('git', 'add', '--', str(dest.relative_to(work)), cwd=work)
        run('git', 'commit', '-m', f"Freeze {m['role']} release for {m['topic']}", cwd=work)
        # No force push, no approvals, no final-topic paths, no actor code execution.
        existing = run('git', 'ls-remote', '--heads', 'origin', branch, cwd=work)
        if existing:
            run('git', 'fetch', 'origin', branch, cwd=work)
            expected_tree = run('git', 'rev-parse', 'HEAD^{tree}', cwd=work)
            remote_tree = run('git', 'rev-parse', 'FETCH_HEAD^{tree}', cwd=work)
            if expected_tree != remote_tree:
                raise ValueError('Existing transport branch differs; preserve it for explicit reconciliation')
        else:
            run('git', 'push', 'origin', branch, cwd=work)
        body = Path(tmp) / 'body.md'
        body.write_text(f"Actor-authored {m['role']} release for {m['topic']}.\n\n"
                        f"Frozen artifact: `runs/{submission}/SUBMISSION.json`.\n"
                        "Transport preserves bytes and role identity. Freeze is not scientific acceptance. "
                        "Candidate integration and next-role packet release retain existing verification, "
                        "forecast masking and experiment gates.\n")
        return run('gh', 'pr', 'create', '--repo', slug, '--base', 'main', '--head', branch,
                   '--title', f"{m['topic']}: submit frozen {m['role']} dossier",
                   '--body-file', str(body), cwd=work)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    f = sub.add_parser('freeze')
    for key in ['source', 'queue', 'role', 'actor', 'session', 'topic', 'ref', 'packet']:
        f.add_argument('--' + key, required=True)
    v = sub.add_parser('verify'); v.add_argument('snapshot')
    t = sub.add_parser('publish'); t.add_argument('snapshot'); t.add_argument('--repo', required=True)
    a = vars(p.parse_args()); command = a.pop('command')
    if command == 'freeze': print(freeze(**a))
    elif command == 'verify': print(json.dumps(verify(a['snapshot'])[0], indent=2))
    else: print(publish(**a))


if __name__ == '__main__':
    main()
