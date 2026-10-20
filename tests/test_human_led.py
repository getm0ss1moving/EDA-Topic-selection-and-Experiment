"""Regression checks: no AI proposer launch and no inflated literature progress."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/f'{name}.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
lit = load('literature'); project = load('project')

class HumanLedTests(unittest.TestCase):
    def test_current_bindings_have_no_ai_proposer(self):
        self.assertEqual(project.validate_launch_release(ROOT), [])
        workflow = json.loads((ROOT/'config/research-workflow.json').read_text())
        self.assertEqual(set(workflow['roles']), {'searcher','challenger','verifier'})
        for actor in json.loads((ROOT/'config/agents.json').read_text())['actors']:
            if actor['role'] == 'proposer': self.assertFalse(actor.get('active_scope'))

    def test_old_config_cannot_restart_loop_via_cli(self):
        # Config override must not bypass the owner policy or create runtime state.
        with tempfile.TemporaryDirectory() as tmp:
            config = ROOT/'legacy/config/codex-research.json'
            result = subprocess.run([sys.executable, str(ROOT/'scripts/codex_loop.py'),
                '--config', str(config), 'prepare', '--ref', '0'*40], cwd=tmp,
                text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('AI proposer execution is disabled', result.stderr)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_default_config_is_inactive(self):
        loop = load('codex_loop')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'runtime'
            with self.assertRaisesRegex(ValueError, 'disabled'):
                loop.prepare(json.loads((ROOT/'config/codex-research.json').read_text()), path, '0'*40)
            self.assertFalse(path.exists())

class LiteratureTests(unittest.TestCase):
    def setUp(self): self.data = json.loads((ROOT/'literature/catalog.json').read_text())
    def test_real_catalog_has_ten_paper_batches_separate_from_artifacts(self):
        self.assertEqual(lit.validate_catalog(self.data), [])
        batches = self.data['batches']
        self.assertEqual(len(batches[0]['paper_ids']), 10)
        self.assertEqual(len(self.data['papers']), sum(len(b['paper_ids']) for b in batches))
        self.assertTrue(self.data['artifacts'])
    def test_new_preprint_version_cannot_inflate_count(self):
        duplicate = copy.deepcopy(self.data['papers'][0]); duplicate['id'] = 'LIT-999'
        duplicate['identity'] = duplicate['identity'].replace('v7', 'v8')
        duplicate['title_en'] += ' revised'
        self.data['papers'].append(duplicate)
        self.assertTrue(any('duplicate paper' in e for e in lit.validate_catalog(self.data)))
    def test_contest_cannot_be_counted_as_paper(self):
        self.data['papers'][0]['kind'] = 'contest'
        self.assertTrue(any('cannot count' in e for e in lit.validate_catalog(self.data)))
    def test_abstract_cannot_be_claimed_method_review(self):
        self.data['papers'][0]['reading_status'] = 'method_reviewed'
        self.assertTrue(any('not method review' in e for e in lit.validate_catalog(self.data)))
    def test_title_alias_cannot_be_counted_twice(self):
        duplicate = copy.deepcopy(self.data['papers'][0]); duplicate.update(id='LIT-999', identity='doi:10.1234/test')
        self.data['papers'].append(duplicate)
        self.assertTrue(any('duplicate title' in e for e in lit.validate_catalog(self.data)))

    def test_conference_doi_alias_cannot_inflate_count(self):
        paper = next(p for p in self.data['papers'] if p.get('aliases'))
        duplicate = copy.deepcopy(paper)
        duplicate.update(id='LIT-999', identity=paper['aliases'][0], title_en='Renamed conference version', aliases=[])
        self.data['papers'].append(duplicate)
        self.assertTrue(any('duplicate paper/version/alias' in e for e in lit.validate_catalog(self.data)))

    def test_paper_cannot_be_credited_to_two_batches(self):
        self.data['batches'].append({'id':'999','paper_ids':[self.data['papers'][0]['id']]})
        self.assertTrue(any('multiple batch slots' in e for e in lit.validate_catalog(self.data)))

    def test_unknown_paper_cannot_be_claimed_in_batch(self):
        self.data['batches'][0]['paper_ids'][0] = 'LIT-999'
        self.assertTrue(any('unknown paper' in e for e in lit.validate_catalog(self.data)))

    def test_unassigned_paper_prevents_progress_claim(self):
        self.data['batches'][0]['paper_ids'].pop()
        self.assertTrue(any('does not cover' in e for e in lit.validate_catalog(self.data)))

    def test_batch_cannot_exceed_released_size(self):
        self.data['batches'][0]['paper_ids'].append(self.data['papers'][10]['id'])
        self.assertTrue(any('1–10' in e for e in lit.validate_catalog(self.data)))
