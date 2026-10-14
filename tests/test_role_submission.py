import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('submission', Path(__file__).resolve().parents[1] / 'scripts/role_submission.py')
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

class SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.source = self.root / 'release'; self.source.mkdir()
        for name in s.REQUIRED['challenger']:
            (self.source / name).write_text('[]\n' if name.endswith('.json') else 'Explicit actor output\n')
    def tearDown(self):
        for p in self.root.rglob('*'):
            if not p.is_symlink(): p.chmod(0o755 if p.is_dir() else 0o644)
        self.tmp.cleanup()
    def freeze(self):
        return s.freeze(self.source, self.root / 'queue', 'challenger', 'C', 'session', 'EDA-0002', 'a'*40, 'b'*64)
    def test_roundtrip_and_idempotence(self):
        snap = self.freeze()
        self.assertEqual(snap, self.freeze())
        self.assertEqual(s.verify(snap)[1]['challenges.md'], b'Explicit actor output\n')
        (self.source / 'challenges.md').write_text('New revision')
        self.assertNotEqual(snap, self.freeze())
        self.assertEqual(s.verify(snap)[1]['challenges.md'], b'Explicit actor output\n')
    def test_tamper_rejected(self):
        snap = self.freeze(); p = snap / 'challenges.md'; p.chmod(0o644); p.write_text('tampered')
        with self.assertRaises(ValueError): s.verify(snap)
    def test_role_overreach_rejected(self):
        (self.source / 'verification.json').write_text('{}')
        with self.assertRaises(ValueError): self.freeze()
    def test_symlink_rejected(self):
        p = self.source / 'challenges.md'; p.unlink(); p.symlink_to(self.source / 'sources.json')
        with self.assertRaises(ValueError): self.freeze()
    def test_missing_required_rejected(self):
        (self.source / 'challenges.md').unlink()
        with self.assertRaises(ValueError): self.freeze()
    def test_size_cap(self):
        (self.source / 'challenges.md').write_bytes(b'x' * (s.LIMIT + 1))
        with self.assertRaises(ValueError): self.freeze()
    def test_extra_snapshot_path(self):
        snap = self.freeze(); snap.chmod(0o755); (snap / 'extra').write_text('unexpected')
        with self.assertRaises(ValueError): s.verify(snap)
    def test_credential_rejected(self):
        (self.source / 'challenges.md').write_text('key sk-ant-' + 'a' * 24 + '\n')
        with self.assertRaises(ValueError): self.freeze()
    def test_non_text_and_bad_json_rejected(self):
        (self.source / 'challenges.md').write_bytes(b'\xff\xfe\x00binary')
        with self.assertRaises(ValueError): self.freeze()
        (self.source / 'challenges.md').write_text('Explicit actor output\n')
        (self.source / 'sources.json').write_text('not json')
        with self.assertRaises(ValueError): self.freeze()
    def test_host_artifacts_ignored(self):
        (self.source / '.DS_Store').write_bytes(b'\x00\x00\x00\x01Bud1')
        (self.source / '.claude' / '.cc-writes').mkdir(parents=True)
        snap = self.freeze()
        self.assertNotIn('.DS_Store', s.verify(snap)[0]['files'])
    def test_consent_signs_only_for_own_session(self):
        consent = {'session_id': 'other', 'decision': 'agree', 'signed_revision': 'a' * 40,
                   'tasklist_sha256': 'c' * 64, 'rationale': 'Reasonable plan'}
        (self.source / 'experiment-consent.json').write_text(json.dumps(consent))
        with self.assertRaises(ValueError): self.freeze()
        consent['session_id'] = 'session'
        (self.source / 'experiment-consent.json').write_text(json.dumps(consent))
        self.assertIn('experiment-consent.json', s.verify(self.freeze())[0]['files'])
    def test_malformed_manifest_is_value_error(self):
        with self.assertRaises(ValueError):
            s.validate_manifest({'schema': 1, 'role': 'challenger', 'topic': None})
    def test_abandonment_consent_signs_only_for_own_session_with_grounds(self):
        vote = {'session_id': 'session', 'decision': 'agree', 'grounds': ['dead_end'],
                'signed_revision': 'SUB-' + 'a' * 64, 'signed_dossier_digest': 'd' * 64, 'rationale': 'Evidence-backed'}
        path = self.source / 'abandonment-consent.json'
        for bad in ({'session_id': 'other'}, {'grounds': ['bored']}, {'grounds': []}, {'signed_dossier_digest': ''}):
            path.write_text(json.dumps({**vote, **bad}))
            with self.assertRaises(ValueError):
                self.freeze()
        path.write_text(json.dumps(vote))
        self.assertIn('abandonment-consent.json', s.verify(self.freeze())[0]['files'])
    def test_agreeing_experiment_consent_must_sign_a_revision(self):
        consent = {'session_id': 'session', 'decision': 'agree', 'signed_revision': 'latest',
                   'tasklist_sha256': 'c' * 64, 'rationale': 'Reasonable plan'}
        (self.source / 'experiment-consent.json').write_text(json.dumps(consent))
        with self.assertRaises(ValueError):
            self.freeze()
