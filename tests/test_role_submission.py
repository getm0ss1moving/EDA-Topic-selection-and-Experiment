import importlib.util
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
            (self.source / name).write_text('Explicit actor output\n')
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
