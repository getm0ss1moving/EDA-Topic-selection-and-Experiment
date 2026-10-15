#!/usr/bin/env python3
"""Audit coordinator metadata and released bytes; never inspect role scratch."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('loop', ROOT/'scripts/codex_loop.py')
loop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--final', action='store_true')
    args = parser.parse_args()
    config, home = loop.config(ROOT/'config/codex-research.json')
    state = loop.read(home/'state.json')
    run = Path(__file__).resolve().parent
    counts = {d: sum(t['round'] for t in state['topics'].values() if t['domain'] == d)
              for d in ('D04', 'D05')}
    jobs, packets, releases = {}, [], []
    for topic, entry in state['topics'].items():
        for role, seat in entry['seats'].items():
            loop.verify_packet(seat)
            target = run/'inputs'/topic/role/'PACKET.json'
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path(seat['packet'])/'PACKET.json', target)
            packets.append({'topic': topic, 'role': role, 'session_id': seat['session_id'],
                            'packet_sha256': seat['packet_sha256']})
        for path in entry['history']:
            path = Path(path)
            manifest, payload = loop.rs.verify(path)
            releases.append({'release_id': path.name, 'topic': topic, 'role': manifest['role'],
                             'session_id': manifest['session_id'], 'file_count': len(payload),
                             'submission_manifest_sha256': loop.sha(path/'SUBMISSION.json')})
            jobs[str(path.parent.parent)] = None
        if entry.get('job'):
            jobs[entry['job']['work']] = None
    for record in state['publication_queue']:
        entry = {**state['topics'][record['topic']], 'latest': record['releases']}
        for role, path in record['releases'].items():
            work = Path(path).parent.parent
            loop.validate_result(state, entry, {'role': role, 'work': str(work)},
                                 loop.read(work/'result.json'))
    job_records = []
    for name in jobs:
        work = Path(name)
        job = loop.read(work/'JOB.json')
        dest = run/'inputs'/job['topic']/f'cycle-{job["batch_round"]}-{job["role"]}'
        dest.mkdir(parents=True, exist_ok=True)
        for filename in ('JOB.json', 'prompt.txt'):
            shutil.copyfile(work/filename, dest/filename)
        job_records.append({'topic': job['topic'], 'domain': job['domain'], 'role': job['role'],
                            'batch_round': job['batch_round'], 'requested': job['models'][job['role']],
                            'job_snapshot_sha256': loop.sha(work/'JOB.json'),
                            'prompt_snapshot_sha256': loop.sha(work/'prompt.txt')})
    if args.final:
        assert counts == {'D04': 4, 'D05': 4}, counts
        assert all(t.get('job') is None for t in state['topics'].values())
        assert len(state['publication_queue']) == 8
        assert len(releases) == len(job_records) == 24
    report = {'scope': 'Released files and coordinator metadata only; not scientific truth or OS isolation.',
              'status': 'bounded_batch_complete' if args.final else 'in_progress',
              'input_commit': state['source_commit'], 'target_cycles_per_domain': 4,
              'completed_cycles': counts, 'completed_rounds': len(state['publication_queue']),
              'logical_seats': packets, 'jobs': job_records, 'verified_releases': releases,
              'published': state['published'], 'merged': state.get('merged', []),
              'coordinator_script_snapshot_sha256': loop.sha(ROOT/'scripts/codex_loop.py'),
              'snapshot_note': 'Hashes describe files at this audit; no physical model attestation is implied.'}
    loop.save(run/'release-audit.json', report)
    print(json.dumps({'cycles': counts, 'hash_valid_releases': len(releases),
                      'completed_rounds': len(state['publication_queue'])}, indent=2))

if __name__ == '__main__':
    main()
