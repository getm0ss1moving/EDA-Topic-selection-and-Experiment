#!/usr/bin/env python3
"""Sandboxed lab runner for one actor (run CLD-LAB-0001).

Watches the actor's lab-requests folder, checks each request against the limits the human owner
approved on 2026-10-13, runs it on lab231 or lab234 through remote_driver.sh (bubblewrap, private
workspace), and publishes the outcome to the actor's read-only results folder. Every job is
appended to a ledger. Run it in Terminal.app, outside any Claude session:

    python3 -I lab_runner.py --actor Claude-P05-TIMING --init
    python3 -I lab_runner.py --actor Claude-P05-TIMING --watch
"""
import argparse
import datetime
import fcntl
import hashlib
import io
import json
import re
import shutil
import struct
import subprocess
import sys
import tarfile
import time
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
DRIVER = RUN_DIR / 'remote_driver.sh'
# Classic seccomp BPF: deny sched_setaffinity(2) with EPERM, allow every other syscall.
# taskset establishes the job's mask before bwrap installs this inherited filter.
SECCOMP = b''.join(struct.pack('<HBBI', *insn) for insn in (
    (0x20, 0, 0, 0),           # BPF_LD | BPF_W | BPF_ABS: seccomp_data.nr
    (0x15, 0, 1, 203),         # BPF_JMP | BPF_JEQ: x86_64 __NR_sched_setaffinity
    (0x06, 0, 0, 0x00050001),  # BPF_RET: SECCOMP_RET_ERRNO | EPERM
    (0x06, 0, 0, 0x7fff0000),  # BPF_RET: SECCOMP_RET_ALLOW
))
BASE = Path('/Users/duanzeyu/Documents/ChatGPT')
RELEASE = 'physical-release-d437c2f66090'
HOSTS = {'lab231': {'network': True}, 'lab234': {'network': False}}
CATEGORIES = {'tooling', 'data', 'substrate', 'property-check'}  # no hypothesis experiments yet
MAX_CORES, MAX_HOURS, LOAD_LIMIT, BUDGET_CORE_HOURS = 8, 12.0, 0.75, 300.0
WORKSPACE_CAP_KB = 60 * 1024 * 1024
RETURN_FILE_MAX, RETURN_TOTAL_MAX, LOG_TAIL = 50 << 20, 200 << 20, 2 << 20
SCRIPT_MAX, INPUTS_MAX, REQUEST_MAX = 1 << 20, 200 << 20, 64 << 10
POLL_SECONDS = 30
ID_RE = re.compile(r'REQ-\d{4}')
ACTOR_RE = re.compile(r'[A-Za-z0-9-]{3,64}')
NAME_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}')
OUT_RE = re.compile(r'out/[A-Za-z0-9._+-]+(/[A-Za-z0-9._+-]+)*')
SSH = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15', '-o', 'ServerAliveInterval=30']


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def iso(epoch):
    return datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') if epoch else None


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def ssh(host, command, stdin=None, timeout=600):
    return subprocess.run(SSH + [host, command], input=stdin, capture_output=True, timeout=timeout)


def remote(actor, rid=None):
    p = {'root': 'eda-agents', 'runner': 'eda-agents/.runner', 'ws': f'eda-agents/{actor}'}
    if rid:
        p['job'], p['ctl'] = f"{p['ws']}/work/{rid}", f"{p['runner']}/jobs/{actor}/{rid}"
    return p


class Runner:
    def __init__(self, actor, base=BASE, release=RELEASE):
        self.actor = actor
        self.requests = base / 'EDA-Agent-Outboxes' / release / actor / 'lab-requests'
        self.results = base / 'EDA-Agent-Inboxes' / release / actor / 'lab-results'
        self.state = base / 'EDA-Agent-Lab' / actor
        for d in (self.results, self.state / 'processed'):
            d.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.ledger, self.running = self.state / 'ledger.jsonl', self.state / 'running.json'

    def log(self, message):
        line = f'{now()} [host clock] {message}'
        print(line, flush=True)
        with (self.state / 'runner.log').open('a') as f:
            f.write(line + '\n')

    def used(self):
        if not self.ledger.exists():
            return 0.0
        return sum(json.loads(l).get('core_hours', 0.0) for l in self.ledger.read_text().splitlines() if l.strip())

    def publish(self, rid, files):
        tmp = self.results / f'.tmp-{rid}'
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(mode=0o700)
        for rel, data in files.items():
            dest = tmp / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        for path in sorted(tmp.rglob('*'), reverse=True):
            path.chmod(0o500 if path.is_dir() else 0o400)
        tmp.chmod(0o500)
        tmp.rename(self.results / rid)

    def finish(self, rid, status, result, ledger=None):
        result = dict(result, id=rid, status=status, runner='CLD-LAB-0001', actor=self.actor)
        files = result.pop('_files', {})
        files['result.json'] = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
        self.publish(rid, files)
        if ledger is not None:
            with self.ledger.open('a') as f:
                f.write(json.dumps(ledger, sort_keys=True) + '\n')
        (self.state / 'processed' / rid).write_text(status + '\n')
        self.log(f'{rid} {status}: {result.get("reasons") or result.get("exit_code")}')

    def validate(self, path):
        errors = []
        try:
            if path.is_symlink() or not path.is_file():
                return None, {}, ['request must be a regular file, not a symlink']
            if path.stat().st_size > REQUEST_MAX:
                return None, {}, ['request file is larger than 64 KiB']
            req = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            return None, {}, [f'request is not readable JSON: {exc}']
        if not isinstance(req, dict):
            return None, {}, ['request must be a JSON object']
        if req.get('id') != path.stem:
            errors.append('id must equal the file name, for example REQ-0001')
        if req.get('category') not in CATEGORIES:
            errors.append(f'category must be one of {sorted(CATEGORIES)}; hypothesis experiments are not '
                          'authorized before task-list consensus')
        purpose = req.get('purpose')
        if not isinstance(purpose, str) or not purpose.strip() or len(purpose) > 4000:
            errors.append('purpose must be a non-empty string of at most 4000 characters')
        host, net = req.get('host'), req.get('network', False)
        if host not in HOSTS:
            errors.append(f'host must be one of {sorted(HOSTS)}')
        if not isinstance(net, bool):
            errors.append('network must be true or false')
        elif net and not HOSTS.get(host, {}).get('network'):
            errors.append('network is available only on lab231')
        cores, hours = req.get('cores'), req.get('timeout_hours')
        if type(cores) is not int or not 1 <= cores <= MAX_CORES:
            errors.append(f'cores must be an integer from 1 to {MAX_CORES}')
        if type(hours) not in (int, float) or not 0 < hours <= MAX_HOURS:
            errors.append(f'timeout_hours must be greater than 0 and at most {MAX_HOURS:g}')
        inputs = req.get('inputs', [])
        if not isinstance(inputs, list):
            errors.append('inputs must be a list of file names')
            inputs = []
        names = [req.get('script')] + inputs
        if len(set(map(str, names))) != len(names) or 'job.sh' in inputs:
            errors.append('script and inputs must be distinct, and no input may be named job.sh')
        blobs = {}
        for i, name in enumerate(names):
            label = 'script' if i == 0 else 'input'
            if not isinstance(name, str) or not NAME_RE.fullmatch(name):
                errors.append(f'{label} {name!r} must be a plain file name in the lab-requests folder')
                continue
            f = self.requests / name
            if f.is_symlink() or not f.is_file():
                errors.append(f'{label} {name} is missing or is not a regular file')
                continue
            blobs['job.sh' if i == 0 else name] = f.read_bytes()
        if len(blobs.get('job.sh', b'')) > SCRIPT_MAX:
            errors.append('script is larger than 1 MiB')
        if sum(map(len, blobs.values())) > INPUTS_MAX:
            errors.append('script and inputs together exceed 200 MiB')
        return req, blobs, errors

    def start(self, req, blobs):
        rid, host = req['id'], req['host']
        p = remote(self.actor, rid)
        reserve = req['cores'] * float(req['timeout_hours'])
        if self.used() + reserve > BUDGET_CORE_HOURS:
            return 'reject', [f'core-hour budget: {self.used():.1f} of {BUDGET_CORE_HOURS:g} used; '
                              f'this request reserves {reserve:.1f}']
        r = ssh(host, f'cut -d" " -f1 /proc/loadavg; nproc --all; sha256sum {p["runner"]}/driver.sh '
                      f'{p["runner"]}/seccomp.bpf; '
                      f'du -sk {p["ws"]}', timeout=900)
        fields = r.stdout.decode(errors='replace').split()
        if r.returncode != 0 or len(fields) < 7:
            return 'defer', [f'{host} is unreachable or the workspace is not initialized']
        load, ncpu = float(fields[0]), int(fields[1])
        driver_sha, seccomp_sha, ws_kb = fields[2], fields[4], int(fields[6])
        if driver_sha != sha256(DRIVER.read_bytes()) or seccomp_sha != sha256(SECCOMP):
            return 'reject', ['the server driver or seccomp filter differs from the reviewed copy; run --init']
        if ws_kb > WORKSPACE_CAP_KB:
            return 'reject', ['the workspace exceeds its 60 GiB cap; free space with a cleanup request']
        if load > LOAD_LIMIT * ncpu:
            return 'defer', [f'{host} load {load:.0f} exceeds {LOAD_LIMIT:.0%} of its {ncpu} cores']
        r = ssh(host, f'test ! -e {p["job"]} && test ! -e {p["ctl"]} && mkdir -p {p["job"]}/in {p["job"]}/out '
                      f'&& echo ok')
        if r.stdout.decode().strip() != 'ok':
            return 'reject', ['a job folder with this id already exists on the server']
        archive = io.BytesIO()
        with tarfile.open(fileobj=archive, mode='w') as tar:
            for name, data in blobs.items():
                info = tarfile.TarInfo(name)
                info.size, info.mode, info.mtime = len(data), 0o600, int(time.time())
                tar.addfile(info, io.BytesIO(data))
        r = ssh(host, f'tar xf - -C {p["job"]}/in', stdin=archive.getvalue(), timeout=3600)
        if r.returncode != 0:
            ssh(host, f'rm -rf {p["job"]}')
            return 'defer', ['upload failed; will retry']
        secs = int(float(req['timeout_hours']) * 3600)
        r = ssh(host, f'setsid nohup bash {p["runner"]}/driver.sh {self.actor} {rid} {req["cores"]} {secs} '
                      f'{1 if req.get("network") else 0} > /dev/null 2>&1 < /dev/null & echo launched')
        if b'launched' not in r.stdout:
            return 'defer', ['launch failed; will retry']
        self.running.write_text(json.dumps({'request': req, 'launched_host_clock': now(),
                                            'request_sha256': {n: sha256(d) for n, d in blobs.items()}}))
        self.log(f'{rid} started on {host} with {req["cores"]} cores')
        return 'running', []

    def collect(self):
        info = json.loads(self.running.read_text())
        req = info['request']
        rid, host = req['id'], req['host']
        p = remote(self.actor, rid)
        r = ssh(host, f'test -f {p["ctl"]}/finished && cd {p["ctl"]} && for f in started finished exit_code cpus '
                      f'load_at_start workspace_kb; do printf "%s=%s\\n" $f "$(head -c 200 $f)"; done', timeout=120)
        if r.returncode != 0:
            return False
        meta = dict(l.split('=', 1) for l in r.stdout.decode(errors='replace').splitlines() if '=' in l)
        sizes = ssh(host, f'cat {p["ctl"]}/out.sizes').stdout.decode(errors='replace')
        sums = ssh(host, f'cat {p["ctl"]}/out.sha256').stdout.decode(errors='replace')
        digests = {line[66:]: line[:64] for line in sums.splitlines() if len(line) > 66}
        entries = {}
        for line in sizes.splitlines():
            size, _, path = line.partition('\t')
            if size.isdigit():
                entries[path] = (int(size), digests.get(path))
        chosen, kept, total, errors = [], [], 0, []
        for path in sorted(entries):
            size, digest = entries[path]
            if OUT_RE.fullmatch(path) and '..' not in path.split('/') and digest and size <= RETURN_FILE_MAX \
                    and total + size <= RETURN_TOTAL_MAX:
                chosen.append(path)
                total += size
            else:
                kept.append({'path': path, 'bytes': size, 'sha256': digest})
        files = {}
        if chosen:
            r = ssh(host, f'cd {p["job"]} && tar cf - --no-recursion -T -', stdin=('\n'.join(chosen) + '\n').encode(),
                    timeout=3600)
            with tarfile.open(fileobj=io.BytesIO(r.stdout), mode='r:') as tar:
                for m in tar.getmembers():
                    if not m.isreg() or m.name not in entries or m.name not in chosen:
                        continue
                    data = tar.extractfile(m).read()
                    if sha256(data) == entries[m.name][1]:
                        files[m.name] = data
                    else:
                        errors.append(f'hash mismatch, not returned: {m.name}')
        logs = {}
        for name in ('stdout.log', 'stderr.log'):
            r = ssh(host, f'stat -c %s {p["ctl"]}/{name}; tail -c {LOG_TAIL} {p["ctl"]}/{name}', timeout=600)
            head, _, body = r.stdout.partition(b'\n')
            files[name], logs[name] = body, {'bytes': int(head or 0), 'truncated_to_tail': int(head or 0) > LOG_TAIL}
        started, finished = int(meta.get('started') or 0), int(meta.get('finished') or 0)
        code = meta.get('exit_code', '').strip()
        exit_code = int(code) if code.lstrip('-').isdigit() else None
        core_hours = round(req['cores'] * max(0, finished - started) / 3600, 4)
        result = {'host': host, 'category': req['category'], 'purpose': req['purpose'],
                  'network': bool(req.get('network')), 'cores': req['cores'], 'cpus': meta.get('cpus'),
                  'timeout_hours': req['timeout_hours'], 'exit_code': exit_code, 'timed_out': exit_code in (124, 137),
                  'started_utc': iso(started), 'finished_utc': iso(finished), 'wall_seconds': finished - started,
                  'core_hours_charged': core_hours, 'load_at_start': meta.get('load_at_start'),
                  'workspace_kb_after': int(meta.get('workspace_kb') or 0), 'logs': logs,
                  'returned_files': [{'path': n, 'bytes': entries[n][0], 'sha256': entries[n][1]} for n in sorted(files)
                                     if n.startswith('out/')],
                  'kept_on_server': kept, 'errors': errors, 'request_sha256': info['request_sha256'],
                  'server_workspace': '/ws inside jobs; files persist across jobs', '_files': files}
        self.finish(rid, 'completed', result, ledger={
            'id': rid, 'actor': self.actor, 'host': host, 'category': req['category'], 'cores': req['cores'],
            'started_utc': iso(started), 'finished_utc': iso(finished), 'core_hours': core_hours,
            'exit_code': exit_code})
        self.running.unlink()
        return True

    def cycle(self):
        if self.running.exists() and not self.collect():
            return
        for path in (sorted(self.requests.glob('REQ-*.json')) if self.requests.is_dir() else []):
            rid = path.stem
            if not ID_RE.fullmatch(rid) or (self.state / 'processed' / rid).exists() or (self.results / rid).exists():
                continue
            req, blobs, errors = self.validate(path)
            if errors:
                self.finish(rid, 'rejected', {'reasons': errors})
                continue
            status, reasons = self.start(req, blobs)
            if status == 'reject':
                self.finish(rid, 'rejected', {'reasons': reasons})
                continue
            if status == 'defer':
                self.log(f'{rid} deferred: {reasons}')
            return

    def init(self):
        p, driver = remote(self.actor), DRIVER.read_bytes()
        for host in HOSTS:
            r = ssh(host, f'umask 077 && mkdir -p {p["runner"]}/jobs/{self.actor} {p["ws"]}/tools/bin '
                          f'{p["ws"]}/data {p["ws"]}/work && chmod 700 {p["root"]} {p["runner"]} {p["ws"]} && '
                          f'cat > {p["runner"]}/driver.sh.tmp && chmod 500 {p["runner"]}/driver.sh.tmp && '
                          f'mv {p["runner"]}/driver.sh.tmp {p["runner"]}/driver.sh', stdin=driver)
            if r.returncode != 0:
                sys.exit(f'init failed on {host}: {r.stderr.decode(errors="replace")}')
            r = ssh(host, f'cat > {p["runner"]}/seccomp.bpf.tmp && chmod 400 '
                          f'{p["runner"]}/seccomp.bpf.tmp && mv {p["runner"]}/seccomp.bpf.tmp '
                          f'{p["runner"]}/seccomp.bpf', stdin=SECCOMP)
            if r.returncode != 0:
                sys.exit(f'seccomp init failed on {host}: {r.stderr.decode(errors="replace")}')
            r = ssh(host, f'sha256sum {p["runner"]}/driver.sh {p["runner"]}/seccomp.bpf; bwrap --version')
            output = r.stdout.decode(errors='replace')
            if r.returncode != 0 or sha256(driver) not in output or sha256(SECCOMP) not in output:
                sys.exit(f'init verification failed on {host}: {r.stderr.decode(errors="replace")}')
            self.log(f'{host}: {output.split()} (driver {sha256(driver)[:16]}, seccomp {sha256(SECCOMP)[:16]})')

    def status(self):
        print(json.dumps({'actor': self.actor, 'core_hours_used': round(self.used(), 3),
                          'core_hours_budget': BUDGET_CORE_HOURS,
                          'running': json.loads(self.running.read_text())['request']['id'] if self.running.exists() else None,
                          'processed': sorted(f.name for f in (self.state / 'processed').iterdir())}, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--actor', required=True)
    ap.add_argument('--base', type=Path, default=BASE, help='folder holding the outbox, inbox and lab-state trees')
    ap.add_argument('--release', default=RELEASE)
    mode = ap.add_mutually_exclusive_group(required=True)
    for flag in ('--init', '--once', '--watch', '--status'):
        mode.add_argument(flag, action='store_true')
    args = ap.parse_args()
    if not ACTOR_RE.fullmatch(args.actor):
        sys.exit('invalid actor id')
    runner = Runner(args.actor, args.base.resolve(), args.release)
    with (runner.state / 'lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            sys.exit('another runner is already active for this actor')
        if args.init:
            runner.init()
        elif args.status:
            runner.status()
        elif args.once:
            runner.cycle()
        else:
            runner.log('watching; press Ctrl-C to stop')
            while True:
                try:
                    runner.cycle()
                except (subprocess.TimeoutExpired, OSError) as exc:
                    runner.log(f'transient error, will retry: {exc}')
                time.sleep(POLL_SECONDS)


if __name__ == '__main__':
    main()
