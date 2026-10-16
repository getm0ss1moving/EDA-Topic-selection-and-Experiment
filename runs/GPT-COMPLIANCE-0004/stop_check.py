#!/usr/bin/env python3
"""Check the four-cycle cap without creating a fifth job or logical seat."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
RUNTIME = ROOT.parent / 'EDA-GPT-Compliance-Four-Rounds-20261016'


def snapshot():
    raw = (RUNTIME / 'state.json').read_bytes()
    state = json.loads(raw)
    return {'state_sha256': hashlib.sha256(raw).hexdigest(),
            'cycles': {d: sum(t['round'] for t in state['topics'].values() if t['domain'] == d)
                       for d in ('D04', 'D05')},
            'topics': {key: {f: t.get(f) for f in ('domain', 'round', 'status', 'job')}
                       for key, t in state['topics'].items()},
            'seat_sessions': sorted(s['session_id'] for t in state['topics'].values() for s in t['seats'].values()),
            'job_descriptors': sorted(str(p.relative_to(RUNTIME)) for p in RUNTIME.glob('**/jobs/*/JOB.json'))}


def main():
    before = snapshot()
    assert before['cycles'] == {'D04': 4, 'D05': 4}
    assert all(not t['job'] for t in before['topics'].values())
    results = []
    for domain in ('D04', 'D05'):
        command = ['python3', 'scripts/codex_loop.py', '--config',
                   'config/codex-compliance-research-0004.json', 'dispatch', '--domain', domain]
        p = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=60)
        result = json.loads(p.stdout)
        assert p.returncode == 0 and result == {'status': 'finished', 'domain': domain, 'rounds': 4}
        results.append({'command': command, 'exit_code': p.returncode, 'result': result, 'stderr': p.stderr})
    after = snapshot()
    assert before == after
    record = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'before': before,
              'after': after, 'dispatch_results': results,
              'state_bytes_jobs_and_seat_sessions_unchanged': True,
              'scope': 'Finite app-agent batch stopped; this is not proof of a persistent daemon or hidden-action isolation.'}
    (RUN / 'stop-check.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'status': 'hard_stop_verified', 'cycles': after['cycles'],
                      'no_fifth_job_or_new_seat': True}))


if __name__ == '__main__':
    main()
