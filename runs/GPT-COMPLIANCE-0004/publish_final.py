#!/usr/bin/env python3
"""Submit the completed report from fresh public main, without unrelated edits."""
import json
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
SLUG = 'getm0ss1moving/EDA-Topic-selection-and-Experiment'
BRANCH = 'codex/compliance-batch-0004-final'
REPORTS = ('reports/final/GPT-COMPLIANCE-0004.zh-CN.md',
           'reports/final/GPT-COMPLIANCE-0004.conduct.en.md')


def command(*args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, text=True, timeout=60).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only', action='store_true',
                        help='Validate and push the exact branch; create PR via connector separately.')
    args = parser.parse_args()
    complete = json.loads((RUN / 'completion.json').read_text())
    assert complete['additional_complete_cycles'] == {'D04': 4, 'D05': 4}
    assert len(complete['merged_round_prs']) == 8
    assert complete['valid_scientific_outputs'] == 24
    assert complete['independent_protocol_audits'] == 8
    assert json.loads((RUN / 'stop-check.json').read_text())['state_bytes_jobs_and_seat_sessions_unchanged']
    if not args.prepare_only:
        existing = json.loads(command('gh', 'pr', 'list', '--repo', SLUG, '--head', BRANCH,
                                      '--state', 'all', '--json', 'url'))
        if existing:
            print(existing[0]['url'])
            return
    with tempfile.TemporaryDirectory(prefix='eda-b04-final-report-') as tmp:
        repo = Path(tmp) / 'repo'
        command('git', 'clone', '--quiet', 'https://github.com/' + SLUG + '.git', str(repo))
        command('git', 'checkout', '--quiet', '-b', BRANCH, cwd=repo)
        destination = repo / 'runs/GPT-COMPLIANCE-0004'
        shutil.copytree(RUN, destination, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for name in REPORTS:
            shutil.copyfile(ROOT / name, repo / name)
        readme = repo / 'README.md'
        previous = readme.read_text()
        assert '## Current status\n\n' in previous and 'GPT-COMPLIANCE-0004.zh-CN.md' not in previous
        summary = ('Batch `GPT-COMPLIANCE-0004` completed four additional full P/C/V cycles per domain: '
                   'eight merged research-round PRs, 24 valid scientific outputs and eight fresh independent '
                   'three-role protocol audits. A quarantined attempt and its separate independent review remain '
                   'public and excluded from valid-cycle counts. All predecessor topics and negative evidence are retained. '
                   'Read the [Chinese topic report](reports/final/GPT-COMPLIANCE-0004.zh-CN.md), '
                   '[English per-role conduct matrix](reports/final/GPT-COMPLIANCE-0004.conduct.en.md), '
                   '[completion record](runs/GPT-COMPLIANCE-0004/completion.json) and '
                   '[public byte/descriptor audit](runs/GPT-COMPLIANCE-0004/publication-audit.json). '
                   'The [hard-stop check](runs/GPT-COMPLIANCE-0004/stop-check.json) records unchanged state/jobs/seats '
                   'after both domains returned finished at four cycles; no live daemon or hidden-action certification is claimed.')
        summary += (' The preceding [batch 0003 report](reports/final/GPT-COMPLIANCE-0003.zh-CN.md) '
                    'and its frozen findings remain historical evidence, including unresolved observations.')
        previous = previous.replace('The new innovation batch `GPT-INNOVATION-0002`',
                                    'The earlier innovation batch `GPT-INNOVATION-0002`')
        previous = previous.replace('Read the latest [Chinese topic report]', 'Read the earlier [Chinese topic report]')
        previous = previous.replace('The current [runtime-event record]', 'The earlier [runtime-event record]')
        readme.write_text(previous.replace('## Current status\n\n',
            '## Current status\n\n' + summary + '\n\n### Earlier batches\n\n', 1))
        for name in REPORTS:
            for target in re.findall(r'\]\(([^)\s]+)\)', (repo / name).read_text()):
                if target.startswith(('https:', 'http:', '#')):
                    continue
                assert ((repo / name).parent / target.split('#', 1)[0]).is_file(), (name, target)
        command('python3', 'scripts/project.py', 'validate', cwd=repo)
        paths = ['runs/GPT-COMPLIANCE-0004', *REPORTS, 'README.md']
        command('git', 'add', '--', *paths, cwd=repo)
        staged = command('git', 'diff', '--cached', '--name-only', cwd=repo).splitlines()
        assert staged and all(any(n == p or n.startswith(p + '/') for p in paths) for n in staged)
        command('git', 'diff', '--cached', '--check', cwd=repo)
        command('git', 'commit', '--quiet', '-m', 'Complete batch 0004 topic and conduct reports at four cycles per domain', cwd=repo)
        head = command('git', 'rev-parse', 'HEAD', cwd=repo)
        command('git', 'push', '--quiet', 'origin', BRANCH, cwd=repo)
        body = Path(tmp) / 'body.md'
        body.write_text('Complete four additional research cycles per domain and publish the Chinese owner report, '
                        'English 24-role conduct matrix, frozen-input/source/publication audits and actual hard-stop evidence. '
                        'Eight research PRs are merged; quarantined attempts, recorded platform screening interruptions and '
                        'independent-review limits remain explicit. No scientific consent or experiment allocation is invented.\n\n'
                        'This report transcribes the assigned scientific and protocol rulings, including unresolved prerequisites '
                        'and incident observations. It does not edit frozen science or replace independent verification. '
                        'All 139 coordinator regression tests passed; helper syntax, project validation, report-link, '
                        'public byte/descriptor and diff checks passed. The finite app-agent batch stopped at four cycles, '
                        'without a fifth scientific job.\n')
        url = None if args.prepare_only else command('gh', 'pr', 'create', '--repo', SLUG, '--head', BRANCH, '--base', 'main',
                      '--title', 'Complete four further D04/D05 cycles with topic and independent conduct reports',
                      '--body-file', str(body), cwd=repo)
    receipt = {'url': url, 'head': head, 'branch': BRANCH,
               'status': 'prepared_for_connector_pr' if args.prepare_only else 'submitted',
               'source': 'fresh public main; only batch files, reports and README staged',
               'validation': ['project validate', 'relative report links', 'staged path allowlist', 'diff check']}
    Path('/tmp/eda-b04-final-publication.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
