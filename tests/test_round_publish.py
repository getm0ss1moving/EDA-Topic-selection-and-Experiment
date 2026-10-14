import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('round_publish', ROOT / 'scripts/round_publish.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
t, s = p.rt, p.rs

IDS = {'proposer': ('P', 'p-session'), 'challenger': ('C', 'c-session'), 'verifier': ('V', 'v-session')}


def git(*args, cwd):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()


class RoundPublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.inbox = {r: self.root / 'inbox' / r for r in t.ROLES}
        for r in t.ROLES:
            for sender in t.ROLES:
                if r in t.ROUTES[sender]:
                    (self.inbox[r] / f'from-{sender}').mkdir(parents=True)
        roles = {r: {'actor_id': IDS[r][0], 'session_id': IDS[r][1], 'inbox': str(self.inbox[r])} for r in t.ROLES}
        self.config = self.root / 'round-transport.json'
        self.config.write_text(json.dumps({'schema': 1, 'topics': {'EDA-0002': {'challenger_stage': 'full', 'roles': roles}}}))
        self.ledger = self.root / 'ledger.jsonl'
        # CI runners have no git identity; publish_round commits in a temporary clone.
        env = mock.patch.dict(os.environ, {k: 'round-test' for k in ('GIT_AUTHOR_NAME', 'GIT_COMMITTER_NAME')}
                              | {k: 'round-test@example.invalid' for k in ('GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_EMAIL')})
        env.start()
        self.addCleanup(env.stop)

    def tearDown(self):
        for q in self.root.rglob('*'):
            if not q.is_symlink():
                q.chmod(0o755 if q.is_dir() else 0o644)
        self.tmp.cleanup()

    def release(self, role, text):
        source = self.root / 'work' / role / 'release'
        if source.exists():
            shutil.rmtree(source)
        source.mkdir(parents=True)
        for name in s.REQUIRED[role]:
            (source / name).write_text('[]\n' if name.endswith('.json') else text)
        return s.freeze(source, self.root / 'work' / role / 'submissions', role, *IDS[role], 'EDA-0002', 'a' * 40, 'b' * 64)

    def rounds(self):
        return p.rounds(t.load_config(self.config), 'EDA-0002')

    def full_round(self):
        prop = self.release('proposer', 'Synthetic proposal\n')
        t.send(self.config, prop)
        chal = self.release('challenger', f'Synthetic objection to {prop.name}\n')
        t.send(self.config, chal)
        self.assertEqual(self.rounds(), [])  # a challenge alone never completes a round
        ver = self.release('verifier', f'Adjudicates {chal.name}\n')
        t.send(self.config, ver, [chal.name])
        return prop, chal, ver

    def origin_and_clone(self):
        origin = self.root / 'origin'
        origin.mkdir()
        archive = subprocess.check_output(['git', 'archive', 'HEAD'], cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(origin)
        git('init', '--quiet', '-b', 'main', cwd=origin)
        git('add', '-A', cwd=origin)
        git('-c', 'user.name=t', '-c', 'user.email=t@example.invalid', 'commit', '--quiet', '-m', 'base', cwd=origin)
        clone = self.root / 'clone'
        git('clone', '--quiet', str(origin), str(clone), cwd=self.root)
        registry = self.root / 'registry.json'
        registry.write_text(json.dumps({'sessions': [
            {'session_id': IDS[r][1], 'actor_id': IDS[r][0], 'role': r, 'topic': 'EDA-0002',
             'input_commit': 'a' * 40, 'packet_sha256': 'b' * 64} for r in t.ROLES]}))
        return origin, clone, registry

    def test_round_completes_only_with_the_verified_delivery(self):
        prop, chal, ver = self.full_round()
        [rnd] = self.rounds()
        self.assertEqual([Path(x).name for x in rnd['releases']], [prop.name, chal.name, ver.name])
        self.assertEqual(rnd['adjudicates'], [chal.name])
        self.assertTrue(all(rnd['deliveries'].values()))
        self.assertEqual(rnd['problems'], [])

    def test_dry_run_builds_a_validated_round_commit(self):
        prop, chal, ver = self.full_round()
        origin, clone, registry = self.origin_and_clone()
        p.REMOTE = str(origin)
        try:
            out = p.publish_round(self.rounds()[0], clone, self.ledger, dry_run=True, registry_file=registry)
        finally:
            spec.loader.exec_module(p)
        self.assertEqual(out['validation'], 'passed')
        dirs = {f.split('/')[1] for f in out['files']}
        self.assertEqual(dirs, {prop.name, chal.name, ver.name, self.rounds()[0]['round_id']})
        self.assertFalse(self.ledger.exists())  # a dry run records nothing

    def test_unregistered_sessions_hold_the_round(self):
        self.full_round()
        origin, clone, _ = self.origin_and_clone()
        p.REMOTE = str(origin)
        try:
            with self.assertRaisesRegex(ValueError, 'held'):
                p.publish_round(self.rounds()[0], clone, self.ledger, dry_run=True)
        finally:
            spec.loader.exec_module(p)

    def test_registry_override_requires_a_dry_run(self):
        self.full_round()
        with self.assertRaises(ValueError):
            p.publish_round(self.rounds()[0], self.root, self.ledger, registry_file=self.root / 'registry.json')
