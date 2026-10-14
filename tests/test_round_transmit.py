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
        got = t.wait(self.config, self.inbox['verifier'], timeout=0)
        self.assertEqual(got['status'], 'delivered')
        self.assertEqual(t.wait(self.config, self.inbox['verifier'], got['delivery'], timeout=0)['status'], 'timeout')
