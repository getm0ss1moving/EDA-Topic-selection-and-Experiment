#!/usr/bin/env python3
"""Publish retained incident evidence from public main; never authorize science."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
SLUG = 'getm0ss1moving/EDA-Topic-selection-and-Experiment'
BRANCH = 'codex/b04-quarantined-d04-attempt'


def command(*args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, text=True, timeout=60).strip()


def main():
    r = json.loads((RUN / 'incident-review.json').read_text())
    existing = json.loads(command('gh', 'pr', 'list', '--repo', SLUG, '--head', BRANCH,
                                  '--state', 'all', '--json', 'url'))
    if existing:
        print(existing[0]['url'])
        return
    paths = ['runs/GPT-COMPLIANCE-0004/' + n for n in
             ('incident_audit.py', 'publish_incident.py', 'incident-review.json',
              'incident-descriptors', 'quarantine-incidents.json')]
    ids = [Path(p).name for p in r['releases'].values()] + [r['audit_release']]
    paths += ['runs/' + sid for sid in ids]
    m = json.loads((ROOT / 'runs' / r['audit_release'] / 'SUBMISSION.json').read_text())
    row = {'session_id': m['session_id'], 'actor_id': m['actor_id'], 'role': 'verifier',
           'topic': m['topic'], 'platform': 'OpenAI Codex', 'model': 'gpt-6.1-sol',
           'operator': 'getm0ss1moving', 'github_login': 'getm0ss1moving (transport only)',
           'input_commit': m['input_commit'], 'packet_sha256': m['packet_sha256'],
           'session_kind': 'independent protocol audit of quarantined attempt; no valid-cycle credit',
           'independence_attestation': 'Fresh file-only input; no inherited conversation; policy isolation, not OS confinement.'}
    with tempfile.TemporaryDirectory(prefix='eda-b04-incident-publish-') as tmp:
        repo = Path(tmp) / 'repo'
        command('git', 'clone', '--quiet', 'https://github.com/' + SLUG + '.git', str(repo))
        command('git', 'checkout', '--quiet', '-b', BRANCH, cwd=repo)
        for name in paths:
            src, dest = ROOT / name, repo / name
            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest)
        registry = repo / 'config/roles.json'
        data = json.loads(registry.read_text())
        assert not any(s['session_id'] == row['session_id'] for s in data['sessions'])
        data['sessions'].append(row)
        registry.write_text(json.dumps(data, indent=2) + '\n')
        command('python3', 'scripts/project.py', 'validate', cwd=repo)
        command('git', 'add', '--', *paths, 'config/roles.json', cwd=repo)
        # Immutable CSV byte conventions are intentionally not normalized.
        command('git', 'diff', '--cached', '--check', '--', 'config/roles.json',
                'runs/GPT-COMPLIANCE-0004', cwd=repo)
        command('git', 'commit', '--quiet', '-m',
                'Preserve quarantined D04 attempt and independent protocol review', cwd=repo)
        head = command('git', 'rev-parse', 'HEAD', cwd=repo)
        command('git', 'push', '--quiet', 'origin', BRANCH, cwd=repo)
        body = Path(tmp) / 'body.md'
        body.write_text('A D04 attempt was quarantined by the ledger input gate and excluded from all valid cycle counts. '
                        'Preserve its exact frozen three outputs, public descriptors and fresh independent protocol review.\n\n'
                        'The review distinguishes an authorized-path/canonical-ID formatting deviation from forbidden content access. '
                        'It remains overall unresolved because one own-previous ownership mapping was outside the supplied audit packet. '
                        'No private trace, scientific clearance, quarantine reset or experiment approval is asserted. '
                        'The replacement cycle uses three fresh logical seats from the clean released checkpoint; these quarantined '
                        'outputs are not assigned to its scientific roles.\n')
        url = command('gh', 'pr', 'create', '--repo', SLUG, '--head', BRANCH, '--base', 'main',
                      '--title', 'Preserve D04 quarantined attempt and bounded independent conduct review',
                      '--body-file', str(body), cwd=repo)
    receipt = {'pr': url, 'head': head, 'included_release_ids': ids,
               'status': 'submitted_not_self_approved', 'excluded_from_valid_cycles': True}
    (RUN / 'incident-publication.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(url)


if __name__ == '__main__':
    main()
