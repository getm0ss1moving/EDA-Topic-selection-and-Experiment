#!/usr/bin/env python3
"""Fetch pinned public fixtures, then run the bounded GCD physical-flow smoke test."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
IMAGE = 'efabless/openlane@sha256:840fe28388494220dae9e2be6cf3c7cb2dadfa0eabae4144f0873b9ee949597f'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=pathlib.Path, required=True, help='New external resource/output directory')
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists() or out == ROOT or ROOT in out.parents:
        parser.error('Use a new directory outside the repository')
    lock = json.loads((ROOT / 'config/physical-resources.lock.json').read_text())
    out.mkdir(parents=True)
    for record in lock['files']:
        with urllib.request.urlopen(record['url'], timeout=60) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != record['sha256']:
            raise ValueError('Checksum mismatch: ' + record['path'])
        target = out / record['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    flow = out / 'test/flow.tcl'
    original = flow.read_text()
    old = 'set_thread_count [exec getconf _NPROCESSORS_ONLN]'
    if original.count(old) != 1:
        raise ValueError('Unexpected upstream thread setting')
    flow.write_text(original.replace(old, 'set_thread_count 2'))
    # The pinned image lacks getconf; this sole patch also bounds router threads.
    name = 'eda-smoke-' + str(time.time_ns())
    command = ['docker', 'run', '--rm', '--name', name, '--network', 'none',
               '--cpus', '2', '--memory', '4g', '--entrypoint', 'bash',
               '-v', str(out / 'test') + ':/work', '-w', '/work', IMAGE,
               '-lc', 'openroad -no_init -exit gcd_nangate45.tcl']
    start = time.monotonic()
    try:
        with (out / 'openroad.log').open('w') as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=600)
    except subprocess.TimeoutExpired:
        subprocess.run(['docker', 'rm', '-f', name], capture_output=True)
        raise
    log_text = (out / 'openroad.log').read_text()
    products = ['gcd_nangate45_route-tcl.def', 'gcd_nangate45-tcl.spef', 'gcd_nangate45_cts-tcl.db']
    # Some OpenROAD Tcl errors return zero: require artifacts AND no error lines.
    passed = result.returncode == 0 and not any(line.startswith('Error:') for line in log_text.splitlines())
    passed = passed and all((out / 'test/results' / f).is_file() for f in products)
    summary = {'flow_completed': passed, 'elapsed_seconds': time.monotonic() - start,
               'returncode': result.returncode, 'image': IMAGE, 'upstream_commit': lock['commit'],
               'patch': {old: 'set_thread_count 2'}, 'not_a_timing_closure_verdict': True}
    (out / 'result.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    raise SystemExit(0 if passed else 1)

if __name__ == '__main__':
    main()
