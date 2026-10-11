import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('project',Path(__file__).resolve().parents[1]/'scripts/project.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

class DossierTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.original_root=p.ROOT
        self.d=self.root/'candidates'/'EDA-0001'
        shutil.copytree(self.original_root/'templates/topic',self.d)
        p.ROOT=self.root
        self.update('dossier.json',id='EDA-0001')
        subprocess.check_call(['git','-C',str(self.root),'init'],stdout=subprocess.DEVNULL)
        subprocess.check_call(['git','-C',str(self.root),'add','.'])
        subprocess.check_call(['git','-C',str(self.root),'-c','user.name=test','-c','user.email=test@example.com',
                               'commit','-m','initial fixture'],stdout=subprocess.DEVNULL)
        self.initial_revision=subprocess.check_output(['git','-C',str(self.root),'rev-parse','HEAD']).decode().strip()
    def tearDown(self):
        p.ROOT=self.original_root
        self.tmp.cleanup()
    def update(self,name,**updates):
        f=self.d/name;data=json.loads(f.read_text());data.update(updates);f.write_text(json.dumps(data))
    def freeze(self,message='freeze fixture'):
        subprocess.check_call(['git','-C',str(self.root),'add','.'])
        subprocess.check_call(['git','-C',str(self.root),'-c','user.name=test','-c','user.email=test@example.com',
                               'commit','--allow-empty','-m',message],stdout=subprocess.DEVNULL)
        return subprocess.check_output(['git','-C',str(self.root),'rev-parse','HEAD']).decode().strip()
    def test_draft_is_not_accepted(self):
        self.assertEqual(p.validate_topic(self.d,'candidates',{}),[])
        self.assertTrue(p.validate_topic(self.d,'topics',{}))
    def test_hash_binds_content_not_verdict(self):
        before=p.digest(self.d)
        self.update('verification.json',decision='revise')
        self.assertEqual(before,p.digest(self.d))
        (self.d/'proposal.md').write_text('new mechanism')
        self.assertNotEqual(before,p.digest(self.d))
    def test_template_cannot_be_submitted(self):
        self.update('dossier.json',status='submitted')
        errors=p.validate_topic(self.d,'candidates',{})
        self.assertTrue(any('sources' in e for e in errors))
        self.assertTrue(any('placeholder' in e for e in errors))
    def test_self_review_rejected(self):
        self.update('dossier.json',status='accepted',proposer_session='same',challenger_session='same',verifier_session='same')
        self.assertTrue(any('distinct' in e for e in p.validate_topic(self.d,'topics',{})))
    def test_symlink_rejected(self):
        (self.d/'leak').symlink_to('/etc/passwd')
        with self.assertRaises(ValueError):p.digest(self.d)
    def test_invalid_source_shape_reported(self):
        (self.d/'sources.json').write_text('[42]')
        self.assertTrue(p.validate_topic(self.d,'candidates',{}))

class PacketTests(unittest.TestCase):
    def test_export_filters_and_uses_frozen_commit(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'repo';root.mkdir()
            def write(name,body='public'):
                f=root/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(body)
            for name in ['AGENTS.md','docs/CHARTER.md','harness/CHALLENGER.md','harness/PROPOSER.md','candidates/EDA-0001/proposal.md','candidates/EDA-0001/forecast.json','private/secret','runs/private.txt','candidates/README.md','topics/README.md','archive/README.md','runs/SMOKE/result.json','runs/OTHER/result.json']:
                write(name)
            def git(*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL)
            git('init');git('add','.');git('-c','user.name=test','-c','user.email=test@example.com','commit','-m','fixture')
            sha=git('rev-parse','HEAD').decode().strip()
            tree=git('rev-parse','HEAD^{tree}').decode().strip()
            write('candidates/EDA-0001/proposal.md','uncommitted private edit')
            original=p.ROOT;p.ROOT=root
            try:
                out=Path(td)/'packet'
                m=p.export_packet('challenger','EDA-0001',sha,out)
                self.assertNotIn('harness/PROPOSER.md',m['files'])
                self.assertNotIn('candidates/EDA-0001/forecast.json',m['files'])
                self.assertNotIn('private/secret',m['files'])
                self.assertNotIn('runs/private.txt',m['files'])
                self.assertFalse((out/'.git').exists())
                gov=p.export_packet('verifier',None,sha,Path(td)/'governance',governance=True)
                for area in ['candidates','topics','archive']:
                    self.assertIn(area+'/README.md',gov['files'])
                self.assertNotIn('candidates/EDA-0001/proposal.md',gov['files'])
                self.assertNotIn('private/secret',gov['files'])
                self.assertNotIn('runs/SMOKE/result.json',gov['files'])
                evidence=p.export_packet('verifier',None,sha,Path(td)/'evidence',governance=True,evidence_runs=['SMOKE'])
                self.assertIn('runs/SMOKE/result.json',evidence['files'])
                self.assertNotIn('runs/OTHER/result.json',evidence['files'])
                with self.assertRaises(ValueError):p.export_packet('verifier',None,sha,Path(td)/'unsafe',governance=True,evidence_runs=['../private'])
                self.assertEqual((out/'candidates/EDA-0001/proposal.md').read_text(),'public')
                with self.assertRaises(ValueError):p.export_packet('challenger','EDA-0001',sha,out)
                with self.assertRaises(ValueError):p.export_packet('challenger','EDA-0001','HEAD',Path(td)/'bad')
                with self.assertRaises(ValueError):p.export_packet('challenger','EDA-0001',tree,Path(td)/'tree')
            finally:p.ROOT=original

if __name__=='__main__':unittest.main()

class AcceptanceTests(DossierTests):
    def make_valid(self):
        self.update('dossier.json',status='accepted',proposer_session='p',challenger_session='c',verifier_session='v')
        for name in ['proposal.md','search-log.md','contest-audit.md','industry-gap.md','experiment-plan.md',
                     'challenges.md','responses.md','verification.md']:
            (self.d/name).write_text('Explicit scientific record; fixture only.')
        source={'id':'SRC-001','title':'fixture','url':'https://example.org/source','type':'paper','published':'unknown','retrieved':'2026-10-10T00:00:00Z','locator':'Section 1','access':'full','claims':['CLM-001'],'limitations':'fixture'}
        (self.d/'sources.json').write_text(json.dumps([source]))
        (self.d/'prior-art.csv').write_text('source_id,task\nSRC-001,fixture\n')
        direction=json.loads((self.d/'direction-control.json').read_text())
        direction['anchor'].update(problem='fixture problem',engineering_user='fixture engineer',
                                   downstream_need='fixture need',causal_mechanism='fixture mechanism',
                                   mechanism_invariants=['fixture invariant'])
        for key in ['combination_drift','demand_drift']:
            direction['penalties'][key]['rationale']='No drift in fixture.'
        (self.d/'direction-control.json').write_text(json.dumps(direction))
        tasklist_hash=p.file_sha256(self.d/'tasklist.md')
        consensus=json.loads((self.d/'experiment-consensus.json').read_text())
        consensus['status']='agreed'
        consensus['tasklist_sha256']=tasklist_hash
        consensus['readiness_checks']={key:True for key in consensus['readiness_checks']}
        consensus['consents']['proposer']={'session_id':'p','decision':'agree','signed_revision':self.initial_revision,
                                            'tasklist_sha256':tasklist_hash,'rationale':'Reasonable fixture plan.'}
        consensus['consents']['challenger']={'session_id':'c','decision':'agree','signed_revision':self.initial_revision,
                                              'tasklist_sha256':tasklist_hash,'rationale':'Reasonable fixture plan.'}
        (self.d/'experiment-consensus.json').write_text(json.dumps(consensus))
        self.update('verification.json',decision='accept_for_pilot',verifier_session='v',
                    gates={k:True for k in p.GATES},direction_penalty_checked=True,
                    experiment_consensus_checked=True,
                    source_checks=[{'source_id':'SRC-001','locator':'Section 1','verdict':'verified'}],
                    dossier_digest=p.digest(self.d))
        return {'p':{'role':'proposer'},'c':{'role':'challenger'},'v':{'role':'verifier'}}
    def test_valid_then_tampered(self):
        sessions=self.make_valid()
        self.assertEqual(p.validate_topic(self.d,'topics',sessions),[])
        (self.d/'proposal.md').write_text('Changed hypothesis')
        self.assertTrue(any('stale' in e for e in p.validate_topic(self.d,'topics',sessions)))
    def test_unresolved_objection_blocks(self):
        sessions=self.make_valid()
        self.update('verification.json',objections=[{'verdict':'valid','blocking':True,'resolution':'open'}])
        self.assertTrue(any('blocking' in e for e in p.validate_topic(self.d,'topics',sessions)))
    def test_direction_penalty_blocks_promotion(self):
        sessions=self.make_valid()
        direction=json.loads((self.d/'direction-control.json').read_text())
        direction['penalties']['combination_drift'].update(score=1,rationale='Minor drift')
        direction['penalties']['total']=1
        (self.d/'direction-control.json').write_text(json.dumps(direction))
        self.update('verification.json',dossier_digest=p.digest(self.d))
        self.assertTrue(any('direction drift penalty' in e for e in p.validate_topic(self.d,'topics',sessions)))
    def test_missing_experiment_consensus_blocks_promotion(self):
        sessions=self.make_valid()
        consensus=json.loads((self.d/'experiment-consensus.json').read_text())
        consensus['status']='revision_requested'
        consensus['consents']['challenger']['decision']='changes_requested'
        (self.d/'experiment-consensus.json').write_text(json.dumps(consensus))
        self.update('verification.json',dossier_digest=p.digest(self.d))
        errors=p.validate_topic(self.d,'topics',sessions)
        self.assertTrue(any('lacks proposer/challenger consensus' in e for e in errors))
    def test_tasklist_edit_invalidates_experiment_consensus(self):
        sessions=self.make_valid()
        with (self.d/'tasklist.md').open('a') as stream:
            stream.write('\n- [ ] EXP-010: New task after signatures.\n')
        self.update('verification.json',dossier_digest=p.digest(self.d))
        errors=p.validate_topic(self.d,'topics',sessions)
        self.assertTrue(any('stale task list' in e for e in errors))
    def test_experiment_consent_rejects_nonexistent_commit(self):
        sessions=self.make_valid()
        consensus=json.loads((self.d/'experiment-consensus.json').read_text())
        consensus['consents']['proposer']['signed_revision']='a'*40
        consensus['consents']['challenger']['signed_revision']='a'*40
        (self.d/'experiment-consensus.json').write_text(json.dumps(consensus))
        self.update('verification.json',dossier_digest=p.digest(self.d))
        errors=p.validate_topic(self.d,'topics',sessions)
        self.assertTrue(any('does not contain the consented task list' in e for e in errors))
    def test_joint_abandonment_requires_two_consents(self):
        sessions=self.make_valid()
        self.update('verification.json',abandonment_process_checked=True)
        self.freeze('candidate before abandonment request')
        self.update('dossier.json',status='abandoned')
        direction=json.loads((self.d/'direction-control.json').read_text())
        direction['state']='jointly_abandoned'
        direction['abandonment'].update(decision_id='ABN-001',grounds=['dead_end'],
                                        rationale='Fixture dead end.',evidence_refs=['SRC-001'],
                                        resurrection_conditions=['New counterexample'])
        (self.d/'direction-control.json').write_text(json.dumps(direction))
        errors=p.validate_topic(self.d,'archive',sessions)
        self.assertTrue(any('has not agreed' in e for e in errors))
    def test_joint_abandonment_valid_with_distinct_consents(self):
        sessions=self.make_valid()
        self.update('verification.json',abandonment_process_checked=True)
        frozen=self.freeze('candidate before valid abandonment')
        frozen_digest=p.revision_topic_digest(frozen,'EDA-0001')
        self.update('dossier.json',status='abandoned')
        direction=json.loads((self.d/'direction-control.json').read_text())
        direction['state']='jointly_abandoned'
        direction['abandonment'].update(decision_id='ABN-001',grounds=['novelty_exhausted'],
                                        rationale='Nearest work leaves no distinct mechanism.',
                                        evidence_refs=['SRC-001'],successor_topic_id='EDA-0002',
                                        resurrection_conditions=['New mechanism evidence'])
        direction['abandonment']['consents']['proposer']={'session_id':'p','decision':'agree','signed_revision':frozen,
                                                           'signed_dossier_digest':frozen_digest}
        direction['abandonment']['consents']['challenger']={'session_id':'c','decision':'agree','signed_revision':frozen,
                                                             'signed_dossier_digest':frozen_digest}
        (self.d/'direction-control.json').write_text(json.dumps(direction))
        self.assertEqual(p.validate_topic(self.d,'archive',sessions),[])
    def test_joint_abandonment_rejects_mismatched_revisions(self):
        sessions=self.make_valid()
        self.update('verification.json',abandonment_process_checked=True)
        frozen_a=self.freeze('first candidate freeze')
        frozen_digest=p.revision_topic_digest(frozen_a,'EDA-0001')
        frozen_b=self.freeze('second candidate freeze')
        self.update('dossier.json',status='abandoned')
        direction=json.loads((self.d/'direction-control.json').read_text())
        direction['state']='jointly_abandoned'
        direction['abandonment'].update(decision_id='ABN-002',grounds=['dead_end'],
                                        rationale='The mechanism cannot satisfy the invariant.',
                                        evidence_refs=['SRC-001'],
                                        resurrection_conditions=['A new causal mechanism'])
        direction['abandonment']['consents']['proposer']={'session_id':'p','decision':'agree','signed_revision':frozen_a,
                                                           'signed_dossier_digest':frozen_digest}
        direction['abandonment']['consents']['challenger']={'session_id':'c','decision':'agree','signed_revision':frozen_b,
                                                             'signed_dossier_digest':frozen_digest}
        (self.d/'direction-control.json').write_text(json.dumps(direction))
        errors=p.validate_topic(self.d,'archive',sessions)
        self.assertTrue(any('same frozen revision' in e for e in errors))
    def test_abandoned_status_requires_joint_direction_state(self):
        sessions=self.make_valid()
        self.update('dossier.json',status='abandoned')
        errors=p.validate_topic(self.d,'archive',sessions)
        self.assertTrue(any('jointly_abandoned direction state' in e for e in errors))
    def test_abandonment_requires_verifier_process_check(self):
        sessions=self.make_valid()
        frozen=self.freeze('candidate before unchecked abandonment')
        frozen_digest=p.revision_topic_digest(frozen,'EDA-0001')
        self.update('dossier.json',status='abandoned')
        direction=json.loads((self.d/'direction-control.json').read_text())
        direction['state']='jointly_abandoned'
        direction['abandonment'].update(decision_id='ABN-003',grounds=['dead_end'],
                                        rationale='Verified evidence is still required.',
                                        evidence_refs=['SRC-001'],
                                        resurrection_conditions=['A new causal path'])
        for role, sid in [('proposer','p'),('challenger','c')]:
            direction['abandonment']['consents'][role]={'session_id':sid,'decision':'agree',
                'signed_revision':frozen,'signed_dossier_digest':frozen_digest}
        (self.d/'direction-control.json').write_text(json.dumps(direction))
        errors=p.validate_topic(self.d,'archive',sessions)
        self.assertTrue(any('did not check abandonment' in e for e in errors))
