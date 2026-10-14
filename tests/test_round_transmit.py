import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('round_transmit', Path(__file__).resolve().parents[1] / 'scripts/round_transmit.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
s = t.rs

IDS = {'proposer': ('P', 'p-session'), 'challenger': ('C', 'c-session'), 'verifier': ('V', 'v-session')}


class RoundTransmitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.inbox = {r: self.root / 'inbox' / r for r in t.ROLES}
        for r in t.ROLES:
            for sender in t.ROLES:
                if r in t.ROUTES[sender]:
                    (self.inbox[r] / f'from-{sender}').mkdir(parents=True)
        self.config = self.root / 'round-transport.json'
        self.write_config('full')

    def tearDown(self):
        for p in self.root.rglob('*'):
            if not p.is_symlink():
                p.chmod(0o755 if p.is_dir() else 0o644)
        self.tmp.cleanup()

    def write_config(self, stage):
        roles = {r: {'actor_id': IDS[r][0], 'session_id': IDS[r][1], 'inbox': str(self.inbox[r])} for r in t.ROLES}
        self.config.write_text(json.dumps({'schema': 1, 'topics': {'EDA-0002': {'challenger_stage': stage, 'roles': roles}}}))

    def release(self, role, text='Explicit actor output\n', session=None):
        source = self.root / 'work' / role / 'release'
        if source.exists():
            shutil.rmtree(source)
        source.mkdir(parents=True)
        for name in s.REQUIRED[role]:
            (source / name).write_text('[]\n' if name.endswith('.json') else text)
        actor, sid = IDS[role]
        return s.freeze(source, self.root / 'work' / role / 'submissions', role, actor, session or sid,
                        'EDA-0002', 'a' * 40, 'b' * 64)

    def deliveries(self, role):
        return t.scan(t.load_config(self.config), self.inbox[role])['deliveries']

    def challenge_round(self):
        t.send(self.config, self.release('challenger'))
        [d] = self.deliveries('verifier')
        return next(p.name for p in Path(d['path']).iterdir() if p.name.startswith('SUB-'))

    def test_proposer_release_reaches_challenger_and_verifier(self):
        out = t.send(self.config, self.release('proposer'))
        self.assertEqual([r['status'] for r in out], ['delivered', 'delivered'])
        for role in ('challenger', 'verifier'):
            [d] = self.deliveries(role)
            self.assertTrue(d['valid'], d['problems'])
            self.assertEqual(d['kind'], 'proposer-release')
        self.assertEqual(self.deliveries('proposer'), [])

    def test_initial_stage_holds_the_challenger_copy(self):
        self.write_config('initial')
        out = t.send(self.config, self.release('proposer'))
        self.assertEqual(out[0]['status'], 'held_for_coordinator_forecast_screening')
        self.assertEqual(self.deliveries('challenger'), [])
        self.assertEqual(len(self.deliveries('verifier')), 1)

    def test_challenger_release_reaches_only_the_verifier(self):
        out = t.send(self.config, self.release('challenger'))
        self.assertEqual([r['to'] for r in out], ['verifier'])
        self.assertEqual(self.deliveries('proposer'), [])

    def test_verifier_must_bind_adjudicated_challenges(self):
        cid = self.challenge_round()
        with self.assertRaises(ValueError):
            t.send(self.config, self.release('verifier', f'Adjudicates {cid}\n'))
        with self.assertRaises(ValueError):
            t.send(self.config, self.release('verifier', 'Names nothing\n'), [cid])
        with self.assertRaises(ValueError):
            t.send(self.config, self.release('verifier', 'Adjudicates SUB-' + 'f' * 64 + '\n'), ['SUB-' + 'f' * 64])

    def test_verified_packet_reaches_proposer_and_verification_reaches_challenger(self):
        cid = self.challenge_round()
        t.send(self.config, self.release('verifier', f'Adjudicates {cid}\n'), [cid])
        [d] = self.deliveries('proposer')
        self.assertTrue(d['valid'], d['problems'])
        self.assertEqual(d['kind'], 'verified-challenge')
        self.assertIn(cid, {p.name for p in Path(d['path']).iterdir()})
        [v] = self.deliveries('challenger')
        self.assertTrue(v['valid'], v['problems'])
        self.assertNotIn(cid, {p.name for p in Path(v['path']).iterdir()})

    def test_unverified_challenger_material_is_never_valid_for_the_proposer(self):
        t.send(self.config, self.release('challenger'))
        src = Path(self.deliveries('verifier')[0]['path'])
        fake = self.inbox['proposer'] / 'from-verifier' / src.name.replace('-challenger-', '-verifier-')
        shutil.copytree(src, fake)
        [d] = self.deliveries('proposer')
        self.assertFalse(d['valid'])
        (self.inbox['proposer'] / 'from-challenger').mkdir()
        state = t.scan(t.load_config(self.config), self.inbox['proposer'])
        self.assertIn('from-challenger', state['stray_entries_not_opened'])

    def test_tampered_delivery_is_invalid(self):
        t.send(self.config, self.release('proposer'))
        d = Path(self.deliveries('verifier')[0]['path'])
        sub = next(p for p in d.iterdir() if p.name.startswith('SUB-'))
        sub.chmod(0o755)
        (sub / 'proposal.md').chmod(0o644)
        (sub / 'proposal.md').write_text('tampered')
        self.assertFalse(self.deliveries('verifier')[0]['valid'])

    def test_unregistered_identity_is_refused(self):
        with self.assertRaises(ValueError):
            t.send(self.config, self.release('proposer', session='someone-else'))

    def test_resend_is_idempotent(self):
        rel = self.release('proposer')
        t.send(self.config, rel)
        self.assertEqual({r['status'] for r in t.send(self.config, rel)}, {'already_delivered'})
        self.assertEqual(len(self.deliveries('challenger')), 1)

    def test_wait_returns_the_next_delivery(self):
        t.send(self.config, self.release('proposer'))
        seen = self.root / 'work' / 'seen.json'  # missing file: nothing handled yet
        got = t.wait(self.config, self.inbox['verifier'], seen, timeout=0)
        self.assertEqual(got['status'], 'delivered')
        t.ack(seen, got['delivery'])
        self.assertEqual(t.wait(self.config, self.inbox['verifier'], seen, timeout=0)['status'], 'timeout')

    def test_delivery_symlink_is_not_followed(self):
        t.send(self.config, self.release('challenger'))
        src = Path(self.deliveries('verifier')[0]['path'])
        alias = src.parent / src.name.replace('-challenger-', '-proposer-')
        alias.symlink_to(src, target_is_directory=True)
        state = t.scan(t.load_config(self.config), self.inbox['verifier'])
        self.assertEqual(len(state['deliveries']), 1)
        self.assertTrue(state['stray_entries_not_opened'])

    def test_traversal_id_is_rejected_before_payload_read(self):
        t.send(self.config, self.release('challenger'))
        d = Path(self.deliveries('verifier')[0]['path'])
        p = d / 'DELIVERY.json'; p.chmod(0o644)
        m = json.loads(p.read_text()); m['releases'][0]['id'] = '../../private'
        p.write_text(json.dumps(m))
        problems = self.deliveries('verifier')[0]['problems']
        self.assertEqual(problems, ['Invalid or duplicate release IDs; payload not opened'])

    def test_identity_tamper_is_invalid(self):
        t.send(self.config, self.release('challenger'))
        d = Path(self.deliveries('verifier')[0]['path'])
        p = d / 'DELIVERY.json'; p.chmod(0o644)
        m = json.loads(p.read_text()); m['from']['session_id'] = 'impostor'
        p.write_text(json.dumps(m))
        self.assertFalse(self.deliveries('verifier')[0]['valid'])
        self.assertEqual(t.wait(self.config, self.inbox['verifier'], self.root / 'seen.json', timeout=0)['status'], 'timeout')

    def test_acknowledged_ids_do_not_skip_same_second_deliveries(self):
        from unittest.mock import patch
        with patch.object(t, 'utc', side_effect=lambda fmt='%Y-%m-%dT%H:%M:%SZ':
                          '20261014T120000Z' if fmt == '%Y%m%dT%H%M%SZ' else '2026-10-14T12:00:00Z'):
            t.send(self.config, self.release('challenger', 'first'))
            t.send(self.config, self.release('proposer', 'second'))
        deliveries = self.deliveries('verifier')
        seen = self.root / 'seen.json'
        seen.write_text(json.dumps([deliveries[-1]['delivery']]))
        out = t.wait(self.config, self.inbox['verifier'], seen, timeout=0)
        self.assertEqual(out['delivery'], deliveries[0]['delivery'])

    def test_wait_wakes_after_atomic_delivery_without_a_model(self):
        import subprocess
        import sys
        seen = self.root / 'seen.json'; seen.write_text('[]')
        proc = subprocess.Popen([sys.executable, str(Path(t.__file__)), 'wait',
                                 '--config', str(self.config), '--inbox', str(self.inbox['verifier']),
                                 '--seen-file', str(seen), '--timeout', '5', '--interval', '1'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            t.send(self.config, self.release('challenger'))
            stdout, stderr = proc.communicate(timeout=8)
            self.assertEqual(proc.returncode, 0, stderr)
            self.assertTrue(json.loads(stdout)['valid'])
        finally:
            if proc.poll() is None: proc.kill(); proc.wait()

    def test_sender_does_not_inspect_write_only_destination(self):
        from unittest.mock import patch
        original = Path.is_symlink
        destinations = [self.inbox[r] for r in ('challenger', 'verifier')]
        def guarded(path):
            if any(path == d or d in path.parents for d in destinations):
                raise PermissionError('destination metadata is not readable by sender')
            return original(path)
        release = self.release('proposer')
        with patch.object(Path, 'is_symlink', guarded):
            self.assertEqual([r['status'] for r in t.send(self.config, release)], ['delivered', 'delivered'])

    def test_ack_records_each_delivery_once_and_wait_skips_it(self):
        t.send(self.config, self.release('proposer'))
        seen = self.root / 'work' / 'seen.json'
        got = t.wait(self.config, self.inbox['verifier'], seen, timeout=0)
        for _ in range(2):
            self.assertEqual(t.ack(seen, got['delivery'])['count'], 1)
        self.assertEqual(json.loads(seen.read_text()), [got['delivery']])
        self.assertEqual(t.wait(self.config, self.inbox['verifier'], seen, timeout=0)['status'], 'timeout')
        with self.assertRaises(ValueError):
            t.ack(seen, 'not-a-delivery')
