#!/usr/bin/env python3
"""Publish every completed local round to GitHub as one intermediate PR (coordinator side).

Owner directive, 2026-10-14: each finished and frozen proposer-challenger-verifier round goes to
GitHub. A round is complete when the verifier's valid `verified-challenge` delivery has reached
the proposer's inbox (docs/AUTO-ROUND.md). Its bundle holds the proposer release that the
verifier had last received before that delivery, the adjudicated challenger releases and the
verifier release, each re-verified byte for byte, plus `runs/ROUND-<topic>-<UTC>/round.json`
naming every delivery. Publication needs the coordinator's GitHub credentials, so it runs
outside every role sandbox, once per command or continuously with `watch`. It checks the
session registry on origin/main, never force-pushes and opens PRs only; merging stays with the
coordinator under docs/WORKFLOW.md.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).absolute().parent
_spec = importlib.util.spec_from_file_location('round_transmit', HERE / 'round_transmit.py')
rt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rt)
rs = rt.rs

REMOTE = 'https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment.git'
SLUG = 'getm0ss1moving/EDA-Topic-selection-and-Experiment'
LEDGER = '/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Transport/round-publish-ledger.jsonl'


def run(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def record_of(delivery):
    return json.loads(rs.regular(Path(delivery['path']) / 'DELIVERY.json'))


def holding(deliveries, sid):
    return next((d['delivery'] for d in deliveries if sid in {r['id'] for r in record_of(d)['releases']}), None)


def rounds(cfg, topic):
    """Completed rounds of a topic, oldest first, each with its releases and deliveries."""
    entry = rt.topic_entry(cfg, topic)
    inbox = {role: entry['roles'][role]['inbox'] for role in rt.ROLES}
    seen = {role: [d for d in rt.scan(cfg, inbox[role])['deliveries'] if d['valid']] for role in rt.ROLES}
    found = []
    for done in (d for d in seen['proposer'] if d['kind'] == 'verified-challenge'):
        stamp = done['delivery'][4:20]
        record = record_of(done)
        offered = [d for d in seen['verifier'] if d['from'] == 'proposer' and d['delivery'][4:20] <= stamp]
        problems = [] if offered else ['the verifier had received no proposer release before this verification']
        proposer = offered[-1] if offered else None
        releases = []
        if proposer:
            releases.append(Path(proposer['path']) / record_of(proposer)['releases'][0]['id'])
        ordered = sorted(record['releases'], key=lambda r: r['role'] != 'challenger')  # challenger(s), then verifier
        releases += [Path(done['path']) / r['id'] for r in ordered]
        verifier_id = next(r['id'] for r in record['releases'] if r['role'] == 'verifier')
        found.append({
            'round_id': f'ROUND-{topic}-{stamp}', 'topic': topic, 'problems': problems,
            'releases': [str(p) for p in releases],
            'deliveries': {
                'proposer_to_verifier': proposer and proposer['delivery'],
                'proposer_to_challenger': proposer and holding(
                    [d for d in seen['challenger'] if d['from'] == 'proposer'], releases[0].name),
                'challenger_to_verifier': [holding([d for d in seen['verifier'] if d['from'] == 'challenger'], sid)
                                           for sid in record['adjudicates']],
                'verified_challenge_to_proposer': done['delivery'],
                'verification_to_challenger': holding(
                    [d for d in seen['challenger'] if d['from'] == 'verifier'], verifier_id)},
            'adjudicates': record['adjudicates']})
    return found


def ledger_rounds(ledger):
    path = Path(ledger)
    if not path.exists():
        return {}
    return {e['round_id']: e for e in map(json.loads, path.read_text().splitlines()) if e.get('status') == 'published'}


def registry_problems(snapshots, registry):
    problems = []
    for m in snapshots:
        match = [s for s in registry['sessions'] if s['session_id'] == m['session_id'] and s.get('actor_id') == m['actor_id']
                 and s['role'] == m['role'] and s.get('topic') == m['topic']]
        if len(match) != 1:
            problems.append(f"{m['role']} {m['actor_id']}: session {m['session_id']} is not registered for {m['topic']}")
        elif (match[0]['input_commit'], match[0]['packet_sha256']) != (m['input_commit'], m['packet_sha256']):
            problems.append(f"{m['role']} {m['actor_id']}: release input pair is not the registered one")
    return problems


def publish_round(rnd, repo, ledger=LEDGER, dry_run=False, registry_file=None):
    """Publish one completed round; returns its PR URL, or a dry-run summary without pushing."""
    if rnd['problems']:
        raise ValueError(f"{rnd['round_id']}: " + '; '.join(rnd['problems']))
    if registry_file and not dry_run:
        raise ValueError('A registry override is only allowed in a dry run')
    done = ledger_rounds(ledger)
    if rnd['round_id'] in done and not dry_run:
        return done[rnd['round_id']]['url']
    snaps = [(Path(p), *rs.verify(p)) for p in rnd['releases']]
    repo = Path(repo).resolve()
    if run('git', 'remote', 'get-url', 'origin', cwd=repo) != REMOTE:
        raise ValueError('Unexpected repository remote')
    run('git', 'fetch', '--quiet', 'origin', 'main', cwd=repo)
    registry = json.loads(Path(registry_file).read_text() if registry_file else
                          run('git', 'show', 'origin/main:config/roles.json', cwd=repo))
    held = registry_problems([m for _, m, _ in snaps], registry)
    if held:
        raise ValueError(f"{rnd['round_id']} held: " + '; '.join(held))
    branch = 'round/' + rnd['round_id'][len('ROUND-'):]
    if not dry_run:
        previous = json.loads(run('gh', 'pr', 'list', '--repo', SLUG, '--head', branch, '--state', 'all', '--json', 'url'))
        if previous:
            return previous[0]['url']
    record = {'schema': 1, 'kind': 'local_round_publication_not_scientific_verification',
              'round_id': rnd['round_id'], 'topic': rnd['topic'], 'adjudicates': rnd['adjudicates'],
              'releases': [{'id': p.name, 'role': m['role'], 'actor_id': m['actor_id'], 'session_id': m['session_id'],
                            'input_commit': m['input_commit'], 'packet_sha256': m['packet_sha256'],
                            'path': f'runs/{p.name}/'} for p, m, _ in snaps],
              'deliveries': rnd['deliveries'], 'published_at_utc': rt.utc(),
              'publisher_sha256': rs.sha(Path(__file__).read_bytes()),
              'transmitter_sha256': rs.sha((HERE / 'round_transmit.py').read_bytes()),
              'note': ('Frozen role outputs copied byte for byte. Publication is not acceptance; '
                       'verifier adjudication inside the round is the scientific record.')}
    with tempfile.TemporaryDirectory(prefix='eda-round-') as tmp:
        work = Path(tmp) / 'repo'
        run('git', 'clone', '--quiet', '--no-hardlinks', str(repo), str(work))
        run('git', 'remote', 'set-url', 'origin', REMOTE, cwd=work)
        run('git', 'fetch', '--quiet', 'origin', 'main', cwd=work)
        run('git', 'checkout', '--quiet', '-b', branch, 'origin/main', cwd=work)
        for p, m, payload in snaps:
            dest = work / 'runs' / p.name
            dest.mkdir(exist_ok=True)
            for n, body in {**payload, 'SUBMISSION.json': rs.encoded(m)}.items():
                if (dest / n).exists() and (dest / n).read_bytes() != body:
                    raise ValueError(f'runs/{p.name}/{n} already differs on main')
                (dest / n).write_bytes(body)
        rdir = work / 'runs' / rnd['round_id']
        rdir.mkdir()
        (rdir / 'round.json').write_text(json.dumps(record, indent=2) + '\n')
        run('python3', 'scripts/project.py', 'validate', cwd=work)
        run('git', 'add', '--', 'runs', cwd=work)
        run('git', 'commit', '--quiet', '-m', f"Publish {rnd['topic']} round {rnd['round_id']}", cwd=work)
        files = run('git', 'show', '--name-only', '--format=', 'HEAD', cwd=work).splitlines()
        if dry_run:
            return {'dry_run': True, 'branch': branch, 'commit': run('git', 'rev-parse', 'HEAD', cwd=work),
                    'files': files, 'validation': 'passed'}
        if run('git', 'ls-remote', '--heads', 'origin', branch, cwd=work):
            raise ValueError(f'Remote branch {branch} exists without a PR; reconcile it explicitly')
        run('git', 'push', '--quiet', 'origin', branch, cwd=work)
        body = Path(tmp) / 'body.md'
        body.write_text(
            f"Local auto round `{rnd['round_id']}` for {rnd['topic']}, published after the verifier's "
            f"verified-challenge delivery reached the proposer.\n\n"
            + ''.join(f"- {m['role']} `{m['actor_id']}`: `runs/{p.name}/`\n" for p, m, _ in snaps)
            + f"- Round record: `runs/{rnd['round_id']}/round.json`\n\n"
            "Transport preserves bytes and role identity (docs/AUTO-ROUND.md). Publication is not "
            "acceptance and authorizes no experiment.\n")
        url = run('gh', 'pr', 'create', '--repo', SLUG, '--base', 'main', '--head', branch,
                  '--title', f"{rnd['topic']}: publish round {rnd['round_id'][len('ROUND-' + rnd['topic']) + 1:]}",
                  '--body-file', str(body), cwd=work)
    Path(ledger).parent.mkdir(parents=True, exist_ok=True)
    with open(ledger, 'a') as f:
        f.write(json.dumps({'utc': rt.utc(), 'round_id': rnd['round_id'], 'status': 'published', 'url': url}) + '\n')
    return url


def all_rounds(cfg):
    return [r for topic in cfg['topics'] for r in rounds(cfg, topic)]


def watch(cfg, repo, ledger, interval):
    """Publish each newly completed round; report a held round once per reason."""
    reported = set()
    while True:
        for rnd in all_rounds(cfg):
            if rnd['round_id'] in ledger_rounds(ledger):
                continue
            try:
                print(json.dumps({'utc': rt.utc(), 'round_id': rnd['round_id'],
                                  'published': publish_round(rnd, repo, ledger)}), flush=True)
            except (ValueError, OSError, subprocess.CalledProcessError) as e:
                if (rnd['round_id'], str(e)) not in reported:
                    reported.add((rnd['round_id'], str(e)))
                    print(json.dumps({'utc': rt.utc(), 'round_id': rnd['round_id'], 'held': str(e)}), flush=True)
        time.sleep(interval)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--config', default=str(HERE.parent / 'config' / 'round-transport.json'))
    p.add_argument('--ledger', default=LEDGER)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('scan', help='list completed rounds and their publication state')
    one = sub.add_parser('publish', help='publish one completed round')
    one.add_argument('round_id')
    one.add_argument('--repo', required=True)
    one.add_argument('--dry-run', action='store_true', help='build and validate the round commit; push nothing')
    one.add_argument('--registry', help='registry file for a dry run of synthetic identities')
    w = sub.add_parser('watch', help='publish rounds as they complete')
    w.add_argument('--repo', required=True)
    w.add_argument('--interval', type=int, default=60)
    a = p.parse_args()
    cfg = rt.load_config(a.config)
    try:
        if a.command == 'scan':
            done = ledger_rounds(a.ledger)
            out = [{**r, 'published': done.get(r['round_id'], {}).get('url')} for r in all_rounds(cfg)]
        elif a.command == 'publish':
            matches = [r for r in all_rounds(cfg) if r['round_id'] == a.round_id]
            if not matches:
                raise ValueError(f'{a.round_id} is not a completed round')
            out = publish_round(matches[0], a.repo, a.ledger, a.dry_run, a.registry)
        else:
            watch(cfg, a.repo, a.ledger, a.interval)
            return
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        sys.stderr.write(f'round_publish: {e}\n')
        sys.exit(1)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
