#!/usr/bin/env python3
"""Run disposable end-to-end isolation jobs on lab234 and lab231."""
import argparse
import datetime
import importlib.util
import json
import shutil
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('lab_runner', HERE / 'lab_runner.py')
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def request(root, rid, host, script, cores=2, seconds=30, network=False):
    req = root / 'EDA-Agent-Outboxes' / 'smoke' / ACTOR / 'lab-requests'
    req.mkdir(parents=True, exist_ok=True)
    script_name = rid + '.sh'
    (req / script_name).write_text(script)
    (req / f'{rid}.json').write_text(json.dumps({
        'id': rid, 'category': 'property-check', 'purpose': 'CLD-LAB-0001 end-to-end isolation test',
        'host': host, 'network': network, 'cores': cores,
        'timeout_hours': seconds / 3600, 'script': script_name, 'inputs': []}, indent=2))


def run_one(runner, rid, limit=120):
    deadline = time.time() + limit
    while time.time() < deadline:
        runner.cycle()
        result = runner.results / rid / 'result.json'
        if result.is_file():
            return json.loads(result.read_text())
        time.sleep(1)
    raise RuntimeError(f'{rid} did not finish within {limit} seconds')


def cpu_count(spec):
    values = set()
    for part in spec.strip().split(','):
        if '-' in part:
            lo, hi = map(int, part.split('-', 1)); values.update(range(lo, hi + 1))
        elif part:
            values.add(int(part))
    return len(values)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', type=Path, required=True)
    args = ap.parse_args()
    global ACTOR
    ACTOR = 'CLD-LAB-SMOKE-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')
    base = Path(tempfile.mkdtemp(prefix='cld-lab-e2e-'))
    runner = MOD.Runner(ACTOR, base, 'smoke')
    checks, details = {}, {}
    try:
        runner.init()
        request(base, 'REQ-9901', 'lab234', r'''set -eu
mkdir -p out
[ "$HOME" = /ws ]
[ ! -e /home/shiliangliang ]
grep '^Cpus_allowed_list:' /proc/self/status | cut -f2 > out/cpus.txt
if taskset -pc 0-63 $$ >/dev/null 2>&1; then exit 42; fi
grep '^Cpus_allowed_list:' /proc/self/status | cut -f2 > out/cpus-after-escape.txt
printf 'lab234-ok\n' > out/normal.txt
truncate -s 52428801 out/oversized.bin
ln -s /etc/passwd out/symlink
if curl -fsS --connect-timeout 2 --max-time 5 https://github.com/ >/dev/null 2>&1; then exit 41; fi
''', cores=2, network=False)
        r234 = run_one(runner, 'REQ-9901')
        p234 = runner.results / 'REQ-9901'
        cpus = (p234 / 'out/cpus.txt').read_text().strip()
        cpus_after = (p234 / 'out/cpus-after-escape.txt').read_text().strip()
        returned = {x['path'] for x in r234['returned_files']}
        kept = {x['path'] for x in r234['kept_on_server']}
        checks.update({
            'lab234_completed': r234['exit_code'] == 0,
            'home_hidden': r234['exit_code'] == 0,
            'lab234_network_blocked': r234['exit_code'] == 0,
            'core_cap_holds': cpu_count(cpus) <= 2 and cpus_after == cpus,
            'normal_file_returned': 'out/normal.txt' in returned,
            'symlink_not_returned': 'out/symlink' not in returned and 'out/symlink' not in kept,
            'oversized_not_returned': 'out/oversized.bin' not in returned and 'out/oversized.bin' in kept,
            'results_read_only': not any(p.stat().st_mode & 0o222 for p in [p234, *p234.rglob('*')]),
        })
        details['lab234'] = {'result': r234, 'cpus_allowed_list': cpus,
                             'cpus_after_escape_attempt': cpus_after}

        request(base, 'REQ-9902', 'lab231', r'''set -eu
mkdir -p out
curl -fsSL --connect-timeout 5 --max-time 20 https://github.com/ >/dev/null
curl -fsSL --connect-timeout 5 --max-time 20 https://arxiv.org/ >/dev/null
grep '^Cpus_allowed_list:' /proc/self/status | cut -f2 > out/cpus.txt
if taskset -pc 0-63 $$ >/dev/null 2>&1; then exit 42; fi
grep '^Cpus_allowed_list:' /proc/self/status | cut -f2 > out/cpus-after-escape.txt
printf 'lab231-network-ok\n' > out/network.txt
''', cores=2, network=True)
        r231 = run_one(runner, 'REQ-9902')
        p231 = runner.results / 'REQ-9902'
        checks['lab231_network_available'] = r231['exit_code'] == 0 and (p231 / 'out/network.txt').is_file()
        cpus231 = (p231 / 'out/cpus.txt').read_text().strip()
        cpus231_after = (p231 / 'out/cpus-after-escape.txt').read_text().strip()
        checks['lab231_core_cap_holds'] = cpu_count(cpus231) <= 2 and cpus231_after == cpus231
        details['lab231'] = {'result': r231, 'cpus_allowed_list': cpus231,
                             'cpus_after_escape_attempt': cpus231_after}

        request(base, 'REQ-9903', 'lab234', 'sleep 10\n', cores=1, seconds=2, network=False)
        timeout_result = run_one(runner, 'REQ-9903')
        checks['timeout_kills_job'] = timeout_result['timed_out'] and timeout_result['wall_seconds'] < 10
        details['timeout'] = timeout_result
    finally:
        p = MOD.remote(ACTOR)
        for host in MOD.HOSTS:
            MOD.ssh(host, f'rm -rf {p["ws"]} {p["runner"]}/jobs/{ACTOR}', timeout=120)
        shutil.rmtree(base, ignore_errors=True)
    report = {'run_id': 'CLD-LAB-0001-E2E', 'actor': ACTOR, 'checks': checks,
              'passed': bool(checks) and all(checks.values()), 'details': details,
              'tested_at_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report['checks'], indent=2, sort_keys=True))
    raise SystemExit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
