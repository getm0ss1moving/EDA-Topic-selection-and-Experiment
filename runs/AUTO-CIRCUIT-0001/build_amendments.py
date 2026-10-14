#!/usr/bin/env python3
"""Build the proposer and verifier amendments of run AUTO-CIRCUIT-0001 from one exact commit.

Each bundle is written read-only into the role's own round inbox with an AMENDMENT.json that
hashes every file and binds the source commit. Existing bundles are never overwritten.

    python3 -I build_amendments.py COMMIT
"""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
TEMPLATES = ['templates/topic/' + n for n in (
    'challenges.md', 'contest-audit.md', 'direction-control.json', 'dossier.json', 'experiment-consensus.json',
    'experiment-plan.md', 'forecast.json', 'industry-gap.md', 'prior-art.csv', 'proposal.md', 'responses.md',
    'search-log.md', 'sources.json', 'tasklist.md', 'verification.json', 'verification.md')]
COMMON = ['scripts/round_transmit.py', 'scripts/role_submission.py', 'scripts/project.py', 'config/round-transport.json',
          'docs/AUTO-ROUND.md', 'docs/SELF-SUBMISSION.md', 'docs/WORKFLOW.md', 'docs/ISOLATION.md',
          'domains/D05/brief.json', 'domains/D05/README.md'] + TEMPLATES
BUNDLES = {
    'proposer': {'name': 'COORDINATOR-AMENDMENT-0002', 'id': 'CLD-P05-AMEND-0002',
                 'files': COMMON + ['harness/PROPOSER.md'], 'changes': RUN / 'CHANGES-proposer.md'},
    'verifier': {'name': 'COORDINATOR-AUTO-CIRCUIT-0001', 'id': 'AUTO-CIRCUIT-0001-V02',
                 'files': COMMON + ['harness/VERIFIER.md', 'docs/CHARTER.md', 'docs/EVIDENCE.md'],
                 'changes': RUN / 'CHANGES-verifier.md'},
}


def sha(body):
    return hashlib.sha256(body).hexdigest()


def main():
    commit = sys.argv[1]
    if len(commit) != 40:
        raise SystemExit('Pass the full source commit')
    cfg = json.loads(subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{commit}:config/round-transport.json']))
    records = []
    for role, spec in BUNDLES.items():
        actor = cfg['topics']['EDA-0002']['roles'][role]
        inbox = Path(actor['inbox'])
        dest, tmp = inbox / spec['name'], inbox / f".pending-{spec['name']}"
        if dest.exists() or tmp.exists():
            raise SystemExit(f'Refusing to overwrite {dest}')
        tmp.mkdir()
        (tmp / 'CHANGES.md').write_text(spec['changes'].read_text().replace('@SOURCE_COMMIT@', commit))
        for name in spec['files']:
            target = tmp / 'files' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{commit}:{name}']))
        files = {str(p.relative_to(tmp)): sha(p.read_bytes()) for p in sorted(tmp.rglob('*')) if p.is_file()}
        manifest = {'schema': 1, 'amendment_id': spec['id'], 'actor_id': actor['actor_id'], 'role': role,
                    'topic': 'EDA-0002', 'session_id': actor['session_id'],
                    'issued_by': 'Claude platform coordinator; transport only, no scientific content or approval',
                    'issued_at_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'source_commit': commit, 'files': files}
        (tmp / 'AMENDMENT.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
        for p in sorted(tmp.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            p.chmod(0o555 if p.is_dir() else 0o444)
        tmp.chmod(0o555)
        tmp.rename(dest)
        records.append({'role': role, 'actor_id': actor['actor_id'], 'amendment_id': spec['id'], 'path': str(dest),
                        'amendment_sha256': sha((dest / 'AMENDMENT.json').read_bytes()), 'file_count': len(files)})
    (RUN / 'deployment.json').write_text(json.dumps({'source_commit': commit, 'bundles': records}, indent=2) + '\n')
    print(json.dumps(records, indent=2))


if __name__ == '__main__':
    main()
