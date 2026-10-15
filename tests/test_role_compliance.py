"""Synthetic protocol checks; no live-model or scientific-compliance claims."""
import copy
import json
import os
import shutil
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_codex_loop as fixtures

l = fixtures.l
ROOT = fixtures.ROOT


class AuditedLoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.home = self.root / 'runtime'
        self.c = l.read(ROOT / 'config/codex-research.json')
        self.c.update(backend='codex_app_agents', require_compliance=True,
                      batch_brief='docs/INNOVATION-BATCH-0003.md', stop_after_rounds=1)
        self.c['topics'] = {'EDA-0002': dict(self.c['topics']['EDA-0002'], seed_prefix=None)}
        self.c['publication'] = {'enabled': False, 'auto_merge': False}
        with patch.object(l, 'frozen', side_effect=lambda ref, name: (ROOT/name).read_bytes()):
            self.state = l.prepare(self.c, self.home, l.git('rev-parse', 'HEAD'))
        self.action = 'revise'

    def tearDown(self):
        for p in self.root.rglob('*'):
            if not p.is_symlink(): p.chmod(0o755 if p.is_dir() else 0o644)
        self.tmp.cleanup()

    def ledger(self, assignment):
        return {**{k: assignment[k] for k in ('role','actor_id','session_id','input_commit',
                                             'packet_sha256','job_id')}, 'schema': 1,
                'read_releases': [],
                'activity': {'checkout_access':'none','foreign_private_reads':[],
                             'agent_messages_sent':0,'subagents_spawned':0,'new_eda_runs':0,
                             'training_runs':0,'new_paid_api_calls':0},
                'rules': {r:{'status':'no_violation_disclosed','evidence':['Synthetic fixture'],
                             'limits':'Not a live trace'} for r in l.compliance.RULES},
                'operations':[], 'incidents':[], 'observability':'Synthetic fixture, not live evidence'}

    def freeze(self, work):
        a = l.read(work/'JOB.json')
        path = l.rs.freeze(work/'release',work/'submissions',a['role'],a['actor_id'],
                           a['session_id'],a['topic'],a['input_commit'],a['packet_sha256'])
        result = {'status':'complete','release_id':path.name,'reason':'Synthetic fixture only'}
        l.save(work/'result.json',result)
        return result

    def science(self):
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        fixtures.LoopTests.fake(self,self.c,job)
        l.save(work/'release/compliance.json',self.ledger(l.read(work/'JOB.json')))
        self.freeze(work)
        return l.collect(self.c,self.home,'D05'),work

    def audit(self, disposition='clear_within_scope'):
        job=l.audit_dispatch(self.c,self.home,'D05');work=Path(job['work'])
        a=l.read(work/'JOB.json');expected=a['reviewed_releases']
        review={'purpose':'protocol_audit','reviewed_releases':expected,'disposition':disposition,
                'roles':{r:{'release_id':sid,'checks':{
                    rule:{'status':'no_violation_found_within_scope','evidence':['Synthetic fixture'],
                          'reason':'Not a live audit'} for rule in l.compliance.RULES}}
                         for r,sid in expected.items()},'findings':[], 'limitations':['Synthetic only']}
        if disposition=='blocking_violation':
            review['roles']['verifier']['checks']['isolation']['status']='supported_deviation'
            review['findings']=[{'id':'INC-001','role':'verifier','rule':'isolation','severity':'critical',
                                 'classification':'supported_violation','evidence':['Synthetic fixture'],
                                 'action':'Replace synthetic role','needs_scientific_adjudication':False}]
        l.save(work/'release/verification.json',review)
        (work/'release/verification.md').write_text('Synthetic governance protocol audit, not science.\n')
        l.save(work/'release/workflow.json',{'role':'verifier','purpose':'protocol_audit',
                                          'reviewed_releases':expected,'disposition':disposition})
        l.save(work/'release/compliance.json',self.ledger(a))
        self.freeze(work)
        return work

    def test_legacy_freezer_does_not_require_new_ledger(self):
        for role in l.ROLES:
            self.assertNotIn('compliance.json',l.rs.REQUIRED[role])
            self.assertIn('compliance.json',l.rs.FILES[role])

    def test_missing_ledger_refused_before_scientific_advancement(self):
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        result=fixtures.LoopTests.fake(self,self.c,job);l.save(work/'result.json',result)
        with self.assertRaisesRegex(ValueError,'compliance.json'):
            l.collect(self.c,self.home,'D05')
        self.assertEqual(l.read(self.home/'state.json')['topics']['EDA-0002']['round'],0)

    def test_disclosed_private_exposure_cannot_be_erased_by_collector(self):
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        fixtures.LoopTests.fake(self,self.c,job);a=l.read(work/'JOB.json');ledger=self.ledger(a)
        ledger['activity']['foreign_private_reads']=['foreign withheld artifact ID, no content']
        l.save(work/'release/compliance.json',ledger);self.freeze(work)
        with self.assertRaises(l.compliance.ProtocolViolation):l.collect(self.c,self.home,'D05')
        self.assertEqual(l.read(work/'release/compliance.json'),ledger)

    def test_all_three_roles_and_cap_wait_for_independent_audit(self):
        for _ in range(3):self.science()
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'awaiting_compliance_audit')
        state=l.read(self.home/'state.json');record=state['publication_queue'][0]
        with self.assertRaisesRegex(ValueError,'publication waits'):
            l.publish_record(record,self.c,self.home,dry_run=True)
        work=self.audit();a=l.read(work/'JOB.json')
        self.assertNotIn(a['session_id'],{s['session_id'] for s in state['topics']['EDA-0002']['seats'].values()})
        self.assertEqual(l.audit_collect(self.c,self.home,'D05')['disposition'],'clear_within_scope')
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'finished')
        record=l.read(self.home/'state.json')['publication_queue'][0]
        self.assertIn('compliance_audit',record)
        # Real offline transport includes the fourth frozen output and its registration.
        real=l.subprocess.check_output
        def local_only(args, **kwargs):
            self.assertNotEqual(args[0],'gh')
            self.assertNotEqual(args[:2],['git','fetch'])
            return real(args,**kwargs)
        identity={k:'protocol-test' for k in ('GIT_AUTHOR_NAME','GIT_COMMITTER_NAME')}
        identity.update({k:'protocol-test@example.invalid' for k in ('GIT_AUTHOR_EMAIL','GIT_COMMITTER_EMAIL')})
        with patch.dict(os.environ,identity),patch.object(l.subprocess,'check_output',side_effect=local_only):
            published=l.publish_record(record,self.c,self.home,dry_run=True)
            self.assertTrue(published['dry_run'])
            self.assertEqual(set(published['descriptor_roles']),set(l.ROLES)|{'protocol_audit'})

    def test_audit_cannot_omit_scientific_verifier_or_use_stale_inputs(self):
        for _ in range(3):self.science()
        work=self.audit();v=l.read(work/'release/verification.json')
        del v['roles']['verifier'];l.save(work/'release/verification.json',v);self.freeze(work)
        with self.assertRaisesRegex(ValueError,'omitted'):l.audit_collect(self.c,self.home,'D05')

    def test_blocking_audit_never_releases_publication_or_next_job(self):
        for _ in range(3):self.science()
        record=l.read(self.home/'state.json')['publication_queue'][0]
        self.audit('blocking_violation');l.audit_collect(self.c,self.home,'D05')
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'quarantined')
        with self.assertRaisesRegex(ValueError,'publication waits'):
            l.publish_record(record,self.c,self.home,dry_run=True)

    def test_disclosed_exposure_cannot_be_retried_by_deleting_the_ledger_entry(self):
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        fixtures.LoopTests.fake(self,self.c,job);a=l.read(work/'JOB.json');ledger=self.ledger(a)
        ledger['activity']['foreign_private_reads']=['withheld-artifact-id']
        l.save(work/'release/compliance.json',ledger);bad=self.freeze(work)
        old=l.read(self.home/'state.json')['topics']['EDA-0002']['seats']
        with self.assertRaises(l.compliance.ProtocolViolation):l.collect(self.c,self.home,'D05')
        self.assertFalse((work/'retry-note.json').exists())
        l.save(work/'release/compliance.json',self.ledger(a));self.freeze(work)
        with self.assertRaisesRegex(ValueError,'Exactly one'):l.collect(self.c,self.home,'D05')
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'quarantined')
        l.recover(self.c,self.home,'D05')
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        self.assertEqual(t['history'],[]);self.assertEqual(t['round'],0)
        self.assertTrue(all(t['seats'][r]['session_id']!=old[r]['session_id'] for r in l.ROLES))
        self.assertIn(str(work/'submissions'/bad['release_id']),state['incidents'][0]['frozen_attempts'])
        self.assertEqual(l.read(work/'submissions'/bad['release_id']/'compliance.json'),ledger)
        new=Path(l.dispatch(self.c,self.home,'D05')['work'])
        self.assertFalse(list((new/'shared').glob('SUB-*')))

    def test_blocked_round_replaced_from_checkpoint_without_counting_tainted_cycle(self):
        for _ in range(3):self.science()
        old=l.read(self.home/'state.json')['topics']['EDA-0002']['seats']
        audit=self.audit('blocking_violation');out=l.audit_collect(self.c,self.home,'D05')
        self.assertEqual(out['status'],'quarantined')
        self.assertEqual(l.audit_dispatch(self.c,self.home,'D05')['status'],'no_pending_audit')
        l.recover(self.c,self.home,'D05')
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        self.assertEqual(t['round'],0);self.assertEqual(state['publication_queue'],[])
        self.assertTrue(all(t['seats'][r]['session_id']!=old[r]['session_id'] for r in l.ROLES))
        self.assertEqual(state['incidents'][0]['round']['compliance_gate'],'blocking_violation')
        for _ in range(3):self.science()
        fresh=self.audit();self.assertNotEqual(audit,fresh)
        l.audit_collect(self.c,self.home,'D05')
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'finished')
        self.assertEqual(len(l.read(self.home/'state.json')['publication_queue']),1)

    def test_terminal_decisions_cannot_skip_critical_audit_quarantine(self):
        for action in ('accept_for_pilot','abandon'):
            with self.subTest(action=action):
                self.home=self.root/action
                with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
                    l.prepare(self.c,self.home,l.git('rev-parse','HEAD'))
                for _ in range(3):self.science()
                state=l.read(self.home/'state.json');state['publication_queue'][0]['decision']=action
                l.save(self.home/'state.json',state)
                self.audit('blocking_violation')
                self.assertEqual(l.audit_collect(self.c,self.home,'D05')['status'],'quarantined')
                state=l.read(self.home/'state.json');self.assertEqual(state['publication_queue'],[])
                self.assertEqual(state['incidents'][0]['round']['decision'],action)

    def test_pre_checkpoint_inflight_phases_recover_using_only_released_history(self):
        for phase,completed in (('challenger',1),('verifier',2),('protocol_audit',3)):
            with self.subTest(phase=phase):
                self.home=self.root/phase
                with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
                    l.prepare(self.c,self.home,l.git('rev-parse','HEAD'))
                for _ in range(completed):self.science()
                if phase=='protocol_audit':work=self.audit('blocking_violation')
                else:
                    job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
                    fixtures.LoopTests.fake(self,self.c,job);a=l.read(work/'JOB.json');v=self.ledger(a)
                    v['activity']['foreign_private_reads']=['withheld-id']
                    l.save(work/'release/compliance.json',v);self.freeze(work)
                state=l.read(self.home/'state.json');state['topics']['EDA-0002'].pop('cycle_checkpoint')
                l.save(self.home/'state.json',state)
                if phase=='protocol_audit':l.audit_collect(self.c,self.home,'D05')
                else:
                    with self.assertRaises(l.compliance.ProtocolViolation):l.collect(self.c,self.home,'D05')
                state=l.read(self.home/'state.json');self.assertEqual(state['incidents'][0]['clean_checkpoint']['history'],[])
                l.recover(self.c,self.home,'D05');job=l.dispatch(self.c,self.home,'D05')
                self.assertEqual(job['role'],'proposer')
                self.assertEqual(l.read(self.home/'state.json')['topics']['EDA-0002']['round'],0)

    def test_unreconstructable_checkpoint_still_persists_fail_closed_quarantine(self):
        self.science();job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        fixtures.LoopTests.fake(self,self.c,job);a=l.read(work/'JOB.json');v=self.ledger(a)
        v['activity']['foreign_private_reads']=['withheld-id']
        l.save(work/'release/compliance.json',v);self.freeze(work)
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        t.pop('cycle_checkpoint');t['history']=[];l.save(self.home/'state.json',state)
        with self.assertRaises(l.compliance.ProtocolViolation):l.collect(self.c,self.home,'D05')
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'quarantined')
        with self.assertRaisesRegex(ValueError,'quarantine preserved'):l.recover(self.c,self.home,'D05')
        self.assertEqual(l.read(self.home/'state.json')['incidents'][0]['status'],'quarantined')

    def test_migrated_consent_cycle_keeps_prior_substantive_round_and_closure(self):
        self.c.pop('stop_after_rounds');self.action='consent_experiment'
        l.save(self.home/'settings.json',self.c)
        for _ in range(3):self.science()
        self.audit();l.audit_collect(self.c,self.home,'D05')
        for _ in range(3):self.science()
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        self.assertEqual(t['round'],1);self.assertEqual(len(t['history']),6)
        t.pop('cycle_checkpoint');l.save(self.home/'state.json',state)
        self.audit('blocking_violation');l.audit_collect(self.c,self.home,'D05')
        l.recover(self.c,self.home,'D05')
        t=l.read(self.home/'state.json')['topics']['EDA-0002']
        self.assertEqual(t['round'],1);self.assertEqual(len(t['history']),3)
        self.assertEqual(t['closure'],'experiment')

    def test_mechanical_rejections_remain_visible_to_auditor_with_latest_bindings(self):
        for _ in range(2):self.science()
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        fixtures.LoopTests.fake(self,self.c,job);a=l.read(work/'JOB.json');v=self.ledger(a)
        v['activity']['checkout_access']='none with explanation'
        l.save(work/'release/compliance.json',v);bad=self.freeze(work)
        with self.assertRaisesRegex(ValueError,'checkout access'):l.collect(self.c,self.home,'D05')
        self.assertEqual(l.read(work/'mechanical-attempts.json')[0]['release_id'],bad['release_id'])
        # A retry cannot erase the auditor's evidence by deleting its own mirror/snapshot.
        (work/'mechanical-attempts.json').unlink()
        old=work/'submissions'/bad['release_id'];old.chmod(0o700)
        for item in old.iterdir():item.chmod(0o600)
        shutil.rmtree(old)
        l.save(work/'release/compliance.json',self.ledger(a));good=self.freeze(work)
        l.collect(self.c,self.home,'D05');audit=Path(l.audit_dispatch(self.c,self.home,'D05')['work'])
        assignment=l.read(audit/'JOB.json')
        self.assertEqual(assignment['reviewed_releases']['verifier'],good['release_id'])
        self.assertEqual(len(assignment['released_inputs']),4)
        self.assertTrue((audit/'shared/rejected-attempts'/bad['release_id']/'compliance.json').is_file())
        self.assertEqual(Path(l.read(self.home/'state.json')['publication_queue'][0]['mechanical_releases'][0]).name,bad['release_id'])

    def test_copied_consent_target_is_explicit_in_receiving_job_allowlist(self):
        for _ in range(3):self.science()
        self.audit();l.audit_collect(self.c,self.home,'D05')
        self.c['stop_after_rounds']=4
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002'];t['status']='researching'
        target=Path(t['history'][0]).name
        l.save(self.home/'state.json',state);l.save(self.home/'settings.json',self.c)
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work']);fixtures.LoopTests.fake(self,self.c,job)
        a=l.read(work/'JOB.json');l.save(work/'release/compliance.json',self.ledger(a))
        l.save(work/'release/experiment-consent.json',{'session_id':a['session_id'],'decision':'revision_requested',
            'signed_revision':target,'tasklist_sha256':'a'*64,'rationale':'Synthetic target transport, not consent'})
        self.freeze(work);l.collect(self.c,self.home,'D05')
        receiver=Path(l.dispatch(self.c,self.home,'D05')['work']);assignment=l.read(receiver/'JOB.json')
        self.assertTrue((receiver/'shared'/target).is_dir())
        self.assertIn(str(receiver/'shared'/target),assignment['released_inputs'])

    def test_auditor_may_read_explicit_metadata_only_incident_release_id(self):
        for _ in range(3):self.science()
        work=self.audit();a=l.read(work/'JOB.json');sid='SUB-'+'e'*64
        a['released_metadata_ids']=[sid];l.save(work/'JOB.json',a)
        ledger=self.ledger(a);ledger['read_releases']=[sid]
        l.save(work/'release/compliance.json',ledger);self.freeze(work)
        self.assertEqual(l.audit_collect(self.c,self.home,'D05')['status'],'audit_collected')

    def test_identity_and_unreleased_input_are_checked(self):
        a=l.read(Path(l.dispatch(self.c,self.home,'D05')['work'])/'JOB.json')
        ledger=self.ledger(a);manifest={k:a[k] for k in ('role','actor_id','session_id','input_commit','packet_sha256')}
        wrong=copy.deepcopy(ledger);wrong['session_id']='foreign'
        with self.assertRaisesRegex(ValueError,'identity'):l.compliance.validate_ledger(wrong,manifest,a,[])
        wrong=copy.deepcopy(ledger);wrong['read_releases']=['SUB-'+'a'*64]
        with self.assertRaises(l.compliance.ProtocolViolation):l.compliance.validate_ledger(wrong,manifest,a,[])

    def test_audit_findings_are_not_scientific_approval(self):
        for _ in range(3):self.science()
        work=self.audit('unresolved');l.audit_collect(self.c,self.home,'D05')
        state=l.read(self.home/'state.json')
        self.assertEqual(state['topics']['EDA-0002']['last_scientific_decision'],'revise')
        self.assertEqual(state['publication_queue'][0]['compliance_gate'],'unresolved')
        with self.assertRaisesRegex(ValueError,'dispatch/collect'):l.tick(self.c,self.home)

    def test_continuation_exports_only_public_adjudicated_files_with_fresh_seats(self):
        c=l.read(ROOT/'config/codex-compliance-research.json')
        c['topics']={'EDA-0007':c['topics']['EDA-0007']}
        home=self.root/'continued'
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            state=l.prepare(c,home,l.git('rev-parse','HEAD'))
        topic=state['topics']['EDA-0007'];self.assertEqual(topic['latest'],{})
        job=l.job_for(state,topic,c);work=Path(job['work'])
        releases=list((work/'shared/predecessor').glob('SUB-*'))
        self.assertEqual({l.rs.verify(p)[0]['role'] for p in releases},set(l.ROLES))
        self.assertNotIn(topic['seats']['proposer']['session_id'],{l.rs.verify(p)[0]['session_id'] for p in releases})
        self.assertEqual([p.name for p in (work/'policy/harness').iterdir()],['PROPOSER.md'])

    def test_continuation_refuses_nonpublic_path(self):
        c=copy.deepcopy(self.c)
        c['topics']['EDA-0002']['continuation_releases']={r:'../private' for r in l.ROLES}
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            with self.assertRaisesRegex(ValueError,'public runs/SUB'):
                l.prepare(c,self.root/'bad-continuation',l.git('rev-parse','HEAD'))

    def test_ledger_metadata_does_not_change_consent_science_digest(self):
        payload={'proposal.md':b'Fixed synthetic science','tasklist.md':b'Fixed synthetic tasks'}
        self.assertEqual(l.proposal_digest(payload),
                         l.proposal_digest({**payload,'compliance.json':b'{"job":"new"}'}))

    def test_literal_objections_in_all_challenger_files_must_be_covered(self):
        self.science()
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        fixtures.LoopTests.fake(self,self.c,job)
        (work/'release/tasklist.md').write_text('Synthetic incidental OBJ-099 requires an explicit scope row.\n')
        l.save(work/'release/compliance.json',self.ledger(l.read(work/'JOB.json')))
        self.freeze(work);l.collect(self.c,self.home,'D05')
        with self.assertRaisesRegex(ValueError,'omitted objection'):
            self.science()
