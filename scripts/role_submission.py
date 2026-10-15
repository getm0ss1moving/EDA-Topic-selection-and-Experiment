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
                 'forecast.json', 'tasklist.md', 'responses.md', 'direction-control.json',
                 'experiment-consent.json', 'abandonment-consent.json'},
    'challenger': {'challenges.md', 'sources.json', 'search-log.md', 'prior-art.csv',
                   'independent-estimate.md', 'tasklist.md', 'experiment-consent.json',
                   'abandonment-consent.json'},
    'verifier': {'verification.md', 'verification.json'},
}
# Optional coordinator-readable outcome. Legacy releases remain valid.
for _owned in FILES.values():
    _owned.add('workflow.json')
REQUIRED = {
    'proposer': FILES['proposer'] - {'responses.md', 'experiment-consent.json', 'abandonment-consent.json', 'workflow.json'},
    'challenger': {'challenges.md', 'sources.json', 'search-log.md'},
    'verifier': FILES['verifier'] - {'workflow.json'},
}
# Host artifacts that are never research output (macOS Finder, Claude Code write staging).
IGNORED = {'.DS_Store', '.claude'}
CONSENT_KEYS = {'session_id', 'decision', 'signed_revision', 'tasklist_sha256', 'rationale'}
CONSENT_DECISIONS = {'pending', 'agree', 'revision_requested'}
# Joint abandonment (docs/CHARTER.md, docs/WORKFLOW.md step 8); each role signs only for itself.
ABANDON_KEYS = {'session_id', 'decision', 'grounds', 'signed_revision', 'signed_dossier_digest', 'rationale'}
ABANDON_DECISIONS = {'pending', 'agree', 'decline'}
ABANDON_GROUNDS = {'novelty_exhausted', 'theoretical_headroom_exhausted', 'dead_end', 'no_anchor_preserving_direction'}
# A signature names the frozen proposer release (SUB-<sha256>) or, for pre-release revisions, a commit.
REVISION = re.compile(r'SUB-[0-9a-f]{64}|[0-9a-f]{40}')
# Releases are published to a public repository without human review, so refuse credential-like text.
SECRET = re.compile(rb'sk-ant-[A-Za-z0-9_-]{10,}|sk-[A-Za-z0-9]{32,}|gh[pousr]_[A-Za-z0-9]{30,}|'
                    rb'-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|'
                    rb'(ANTHROPIC|OPENAI|DEEPSEEK)_[A-Z_]*(KEY|TOKEN)\s*=\s*\S')


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
            raise ValueError(f'Only regular files may be released: {path.name}')
        body = f.read(LIMIT + 1)
    if len(body) > LIMIT or not body.strip():
        raise ValueError(f'Empty or oversized release file: {path.name}')
    return body


def validate_manifest(m):
    if not isinstance(m, dict) or m.get('schema') != 1 or m.get('role') not in FILES:
        raise ValueError('Invalid schema/role')
    for key, pattern in [('topic', r'EDA-\d{4,}'), ('input_commit', r'[0-9a-f]{40}'),
                         ('packet_sha256', r'[0-9a-f]{64}')]:
        if not isinstance(m.get(key), str) or not re.fullmatch(pattern, m[key]):
            raise ValueError(f'Invalid {key}')
    for key in ['actor_id', 'session_id']:
        if not isinstance(m.get(key), str) or not m[key].strip():
            raise ValueError(f'Missing {key}')
    files = m.get('files')
    if not isinstance(files, dict) or not all(isinstance(h, str) for h in files.values()):
        raise ValueError('Invalid file map')
    names, role = set(files), m['role']
    if not REQUIRED[role] <= names <= FILES[role]:
        raise ValueError(f'{role} release: missing {sorted(REQUIRED[role] - names)}, '
                         f'not role-owned {sorted(names - FILES[role])}')
    if any(not re.fullmatch(r'[0-9a-f]{64}', h) for h in files.values()):
        raise ValueError('Invalid file hash')


def check_content(m, payload):
    """Text-level checks that must hold before anything is frozen or published."""
    for name, body in payload.items():
        try:
            text = body.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError(f'{name}: not UTF-8 text')
        if SECRET.search(body):
            raise ValueError(f'{name}: contains a credential-like string; remove it before freezing')
        if name.endswith('.json'):
            try:
                json.loads(text)
            except ValueError:
                raise ValueError(f'{name}: invalid JSON')
    if 'experiment-consent.json' in payload:
        consent = json.loads(payload['experiment-consent.json'])
        if not isinstance(consent, dict) or set(consent) != CONSENT_KEYS:
            raise ValueError(f'experiment-consent.json must contain exactly {sorted(CONSENT_KEYS)}')
        if consent['session_id'] != m['session_id']:
            raise ValueError('experiment-consent.json may only sign for the releasing session')
        if consent['decision'] not in CONSENT_DECISIONS:
            raise ValueError(f'experiment-consent.json decision must be one of {sorted(CONSENT_DECISIONS)}')
        if consent['decision'] == 'agree' and not (
                isinstance(consent['signed_revision'], str) and REVISION.fullmatch(consent['signed_revision'])
                and isinstance(consent['tasklist_sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', consent['tasklist_sha256'])):
            raise ValueError('An agreeing experiment consent must sign a release ID or commit and a task-list SHA-256')
    if 'abandonment-consent.json' in payload:
        vote = json.loads(payload['abandonment-consent.json'])
        if not isinstance(vote, dict) or set(vote) != ABANDON_KEYS:
            raise ValueError(f'abandonment-consent.json must contain exactly {sorted(ABANDON_KEYS)}')
        if vote['session_id'] != m['session_id']:
            raise ValueError('abandonment-consent.json may only sign for the releasing session')
        if vote['decision'] not in ABANDON_DECISIONS:
            raise ValueError(f'abandonment-consent.json decision must be one of {sorted(ABANDON_DECISIONS)}')
        if not isinstance(vote['grounds'], list) or not set(vote['grounds']) <= ABANDON_GROUNDS:
            raise ValueError(f'abandonment-consent.json grounds must be a list drawn from {sorted(ABANDON_GROUNDS)}')
        if vote['decision'] == 'agree' and not (
                vote['grounds'] and isinstance(vote['signed_revision'], str) and REVISION.fullmatch(vote['signed_revision'])
                and isinstance(vote['signed_dossier_digest'], str) and re.fullmatch(r'[0-9a-f]{64}', vote['signed_dossier_digest'])):
            raise ValueError('An agreeing abandonment consent must state grounds and sign a release ID or commit and a dossier digest')


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
    check_content(m, payload)
    if snapshot.name != 'SUB-' + sha(encoded(m)):
        raise ValueError('Snapshot identity mismatch')
    return m, payload


def freeze(source, queue, role, actor, session, topic, ref, packet):
    source, queue = Path(source).absolute(), Path(queue).absolute()
    if source == queue or source in queue.parents:
        raise ValueError('Queue must be outside the release directory')
    payload = {p.name: regular(p) for p in source.iterdir() if p.name not in IGNORED}
    m = dict(schema=1, role=role, actor_id=actor, session_id=session,
             topic=topic, input_commit=ref, packet_sha256=packet,
             files={n: sha(b) for n, b in payload.items()})
    validate_manifest(m)
    check_content(m, payload)
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
    branch = 'submit/' + submission[4:]  # platform-neutral: releases come from every platform's actors
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
