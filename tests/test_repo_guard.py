"""Deterministic guard tests, independent of whether an LLM invokes a probe."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('repo_guard', Path(__file__).resolve().parents[1] / 'runs/CLD-P05-LAUNCH-0001/repo_guard.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

class RepoGuardTests(unittest.TestCase):
    def call(self, tool, key, value):
        with tempfile.TemporaryDirectory() as tmp:
            event = {'session_id': 'synthetic', 'tool_name': tool, 'tool_input': {key: value}}
            with patch.object(g, 'LOG', str(Path(tmp) / 'guard.jsonl')), patch('sys.stdin', io.StringIO(json.dumps(event))), contextlib.redirect_stderr(io.StringIO()):
                return g.main()
    def test_known_project_routes_are_blocked(self):
        for tool, key, value in [
            ('Bash', 'command', 'curl https://github.com/getm0ss1moving/x'),
            ('WebSearch', 'query', 'M0nitor-EDA'),
            ('WebFetch', 'url', 'https://github.com/%2567etm0ss1moving'),
            ('WebFetch', 'url', 'https://cdn.jsdelivr.net/gh/getm0ss1moving/EDA-Topic-selection-and-Experiment@main/README.md')]:
            with self.subTest(tool=tool, value=value): self.assertEqual(self.call(tool, key, value), 2)
    def test_external_research_is_allowed(self):
        self.assertEqual(self.call('WebFetch', 'url', 'https://example.com/paper.pdf'), 0)
    def test_unknown_mirror_is_not_claimed_covered(self):
        self.assertEqual(self.call('WebFetch', 'url', 'https://example.com/renamed-copy'), 0)
