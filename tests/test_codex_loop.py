"""Deterministic coordinator tests. Fake role outputs are not live model evidence."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('codex_loop',ROOT/'scripts/codex_loop.py')
l=importlib.util.module_from_spec(spec);spec.loader.exec_module(l)


class LoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.home=Path(self.tmp.name).resolve()/'runtime'
        self.c=l.read(ROOT/'config/codex-research.json')
        self.c['retirement_policy']=False  # Explicit legacy-path regression fixture.
        self.c['topics']={'EDA-0002':dict(self.c['topics']['EDA-0002'],seed_prefix=None)}
        self.c['publication']={'enabled':False,'auto_merge':False}
        self.c.pop('stop_after_rounds',None)
        self.c['max_substantive_rounds']=3
        # Fixture exports current test source bytes; no production deployment claim.
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            self.state=l.prepare(self.c,self.home,l.git('rev-parse','HEAD'))
        self.action='revise'
    def tearDown(self):
        for p in self.home.rglob('*'):
            if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
        self.tmp.cleanup()
    def fake(self,c,job):
        work=Path(job['work']);assign=l.read(work/'JOB.json');role=assign['role']
        for n in l.rs.REQUIRED[role]:
            body='[]\n' if n.endswith('.json') else 'Synthetic fixture only.\n'
            (work/'release'/n).write_text(body)
        flow={'role':role,'fixture_turn':len(l.read(self.home/'state.json')['topics'][assign['topic']]['history'])}
        if role=='proposer':
            (work/'release/direction-control.json').write_text(json.dumps({'penalties':{'total':0}}))
        if role=='challenger':
            flow.update(reviewed_proposer_release=assign['previous_proposal_release'],assessment='feasible',
                        coverage={k:'supported' for k in l.COVERAGE})
            (work/'release/challenges.md').write_text('OBJ-001: synthetic checked concern.\n')
        if role=='verifier':
            state=l.read(self.home/'state.json');t=state['topics'][assign['topic']]
            cid=Path(t['latest']['challenger']).name
            flow.update(reviewed_proposer_release=assign['previous_proposal_release'],next_action=self.action)
            v={'decision':'revise','reviewed_proposer_release':assign['previous_proposal_release'],
               'adjudicated_challenger_releases':[cid],
               'objections':[{'id':'OBJ-001','verdict':'refuted','blocking':False}],
               'source_checks':[]}
            (work/'release/verification.json').write_text(json.dumps(v))
            (work/'release/verification.md').write_text(f'Reviews {assign["previous_proposal_release"]}; adjudicates {cid}.\n')
        (work/'release/workflow.json').write_text(json.dumps(flow))
        p=l.rs.freeze(work/'release',work/'submissions',role,assign['actor_id'],assign['session_id'],
                      assign['topic'],assign['input_commit'],assign['packet_sha256'])
        return {'status':'complete','release_id':p.name,'reason':'Synthetic fixture'}
    def tick(self):return l.tick(self.c,self.home,executor=self.fake)
    def topic(self):return l.read(self.home/'state.json')['topics']['EDA-0002']
    def test_each_role_receives_innovation_policy_without_foreign_harnesses(self):
        for role,seat in self.topic()['seats'].items():
            packet=Path(seat['packet'])
            self.assertEqual((packet/'docs/INNOVATION-STRATEGY.md').read_bytes(),
                             (ROOT/'docs/INNOVATION-STRATEGY.md').read_bytes())
            self.assertEqual([p.name for p in (packet/'harness').iterdir()],
                             [role.upper()+'.md'])
            l.verify_packet(seat)
    def test_custom_batch_brief_reaches_all_roles_and_job(self):
        c=dict(self.c,batch_brief='docs/INNOVATION-BATCH-0002.md')
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            state=l.prepare(c,self.home/'custom',l.git('rev-parse','HEAD'))
        t=state['topics']['EDA-0002']
        for seat in t['seats'].values():
            self.assertEqual((Path(seat['packet'])/c['batch_brief']).read_bytes(),
                             (ROOT/c['batch_brief']).read_bytes())
            l.verify_packet(seat)
        job=l.job_for(state,t,c);work=Path(job['work'])
        self.assertEqual(l.read(work/'JOB.json')['batch_brief'],c['batch_brief'])
        self.assertIn('policy/'+c['batch_brief'],(work/'prompt.txt').read_text())
    def test_batch_brief_cannot_escape_docs(self):
        for i,name in enumerate(('../AGENTS.md','/tmp/brief.md','.','harness/VERIFIER.md')):
            with self.subTest(name=name),patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
                with self.assertRaises(ValueError):
                    l.prepare(dict(self.c,batch_brief=name),self.home/f'invalid-{i}',l.git('rev-parse','HEAD'))
    def test_three_roles_then_proposer_without_human_wakeup(self):
        self.assertEqual(self.tick()['next_role'],'challenger')
        self.assertEqual(self.tick()['next_role'],'verifier')
        self.assertEqual(self.tick()['next_role'],'proposer')
        t=self.topic();self.assertEqual(t['round'],1)
        self.assertEqual(len(l.read(self.home/'state.json')['publication_queue']),1)
        state=l.read(self.home/'state.json');job=l.job_for(state,t,self.c)
        shared=list((Path(job['work'])/'shared').glob('SUB-*'))
        self.assertEqual(len(shared),2)  # verifier plus its adjudicated challenger
        self.assertTrue(any((p/'challenges.md').exists() for p in shared))
    def test_proposer_never_gets_raw_challenge(self):
        self.tick();self.tick()
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002'];t['phase']='proposer'
        job=l.job_for(state,t,self.c)
        self.assertFalse(list((Path(job['work'])/'shared').rglob('challenges.md')))
    def test_verifier_cannot_skip_challenger(self):
        self.tick()
        self.assertEqual(self.topic()['phase'],'challenger')
        self.assertNotIn('verifier',self.topic()['latest'])
    def test_frozen_release_byte_tamper_rejected(self):
        self.tick();p=Path(self.topic()['latest']['proposer'])/'proposal.md'
        p.chmod(0o644);p.write_text('altered')
        with self.assertRaises(ValueError):l.rs.verify(p.parent)
    def test_blocked_job_is_durable_and_retried_after_backoff(self):
        out=l.tick(self.c,self.home,executor=lambda c,j:{'status':'blocked','release_id':None,'reason':'quota'})
        self.assertEqual(out['status'],'retry_scheduled')
        state=self.topic();self.assertIsNotNone(state['job']);self.assertEqual(state['phase'],'proposer')
        self.assertEqual(l.tick(self.c,self.home,executor=self.fake)['status'],'idle')
    def test_selection_without_matching_consents_fails(self):
        self.tick();self.tick();self.action='accept_for_pilot'
        out=self.tick();self.assertEqual(out['status'],'retry_scheduled')
        self.assertIn('dual consent',out['reason'])
        self.assertEqual(self.topic()['status'],'researching')
    def test_abandonment_without_matching_consents_fails(self):
        self.tick();self.tick();self.action='abandon'
        out=self.tick();self.assertEqual(out['status'],'retry_scheduled')
        self.assertIn('consents',out['reason'])
    def test_round_limit_parks_without_fabricated_abandonment(self):
        for _ in range(9):self.tick()
        self.assertEqual(self.topic()['status'],'parked')
        self.assertEqual(self.topic()['round'],3)
    def test_successor_has_new_id_and_fresh_seats(self):
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002'];t['status']='parked'
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            l.successor(state,t,self.c,self.home)
        new=state['topics'][t['successor']]
        self.assertNotEqual(new['topic'],t['topic'])
        self.assertEqual(new['latest'],{})
        self.assertTrue(all(new['seats'][r]['session_id']!=t['seats'][r]['session_id'] for r in l.ROLES))
    def test_successor_inputs_keep_verifiable_names_and_adjudicated_challenge(self):
        self.tick();self.tick();self.tick()
        state=l.read(self.home/'state.json');old=state['topics']['EDA-0002'];old['status']='parked'
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            l.successor(state,old,self.c,self.home)
        job=l.job_for(state,state['topics'][old['successor']],self.c)
        assign=l.read(Path(job['work'])/'JOB.json')
        releases=[Path(p) for p in assign['released_inputs'] if Path(p).is_dir()]
        roles={l.rs.verify(p)[0]['role'] for p in releases}
        self.assertEqual(roles,set(l.ROLES))
        self.assertTrue(all(p.name.startswith('SUB-') for p in releases))
    def test_native_command_uses_assigned_model_and_no_provider_bridge(self):
        cmd=l.command(self.c,'challenger',self.home/'work')
        self.assertEqual(cmd[cmd.index('--model')+1],'gpt-6-astra')
        self.assertIn('--ephemeral',cmd);self.assertIn('--ignore-user-config',cmd)
        self.assertNotIn('deepseek',' '.join(cmd).lower());self.assertNotIn('claude',' '.join(cmd).lower())
    def test_duplicate_prepare_does_not_reset_progress(self):
        self.tick()
        with self.assertRaises(ValueError):l.prepare(self.c,self.home,self.state['source_commit'])
        self.assertEqual(self.topic()['phase'],'challenger')
    def test_round_registrations_satisfy_repository_required_fields(self):
        required=l.read(ROOT/'config/roles.json')['required_session_fields']
        for seat in l.registry(self.state)['sessions']:
            self.assertFalse([field for field in required if not seat.get(field)])
            self.assertIn('transport account only',seat['github_login'])
    def test_changed_input_packet_blocks_model_execution_and_retains_retry(self):
        seat=self.topic()['seats']['proposer'];p=Path(seat['packet'])/'harness/PROPOSER.md'
        p.chmod(0o644);p.write_text('tampered policy')
        with patch.object(l,'execute',side_effect=AssertionError('must not execute')):
            out=l.tick(self.c,self.home,executor=lambda c,j:self.fail('must not execute'))
        self.assertEqual(out['status'],'retry_scheduled')
        self.assertIn('packet content changed',out['reason'])
    def test_foreign_release_cannot_be_marked_complete(self):
        self.tick();state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        job=l.job_for(state,t,self.c);result=self.fake(self.c,job)
        # Wrong role/identity never gets substituted for a successful challenger.
        result['release_id']=Path(t['latest']['proposer']).name
        with self.assertRaises((ValueError,OSError)):l.validate_result(state,t,job,result)
    def test_missing_coverage_is_refused(self):
        self.tick();state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        job=l.job_for(state,t,self.c);self.fake(self.c,job);work=Path(job['work'])
        flow=l.read(work/'release/workflow.json');flow['coverage']={};l.save(work/'release/workflow.json',flow)
        a=l.read(work/'JOB.json');rel=l.rs.freeze(work/'release',work/'submissions','challenger',a['actor_id'],a['session_id'],a['topic'],a['input_commit'],a['packet_sha256'])
        with self.assertRaisesRegex(ValueError,'coverage'):
            l.validate_result(state,t,job,{'status':'complete','release_id':rel.name})
    def consented(self,kind):
        self.tick();self.tick();state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        target=t['latest']['proposer'];_,science=l.rs.verify(target)
        for role in ('proposer','challenger'):
            _,p=l.rs.verify(t['latest'][role]);source=self.home/('sign-'+role);source.mkdir()
            for n,b in p.items():(source/n).write_bytes(b)
            s=t['seats'][role]
            vote={'session_id':s['session_id'],'decision':'agree','signed_revision':Path(target).name,'rationale':'Synthetic consent only'}
            name='experiment-consent.json' if kind=='experiment' else 'abandonment-consent.json'
            if kind=='experiment':vote['tasklist_sha256']=l.rs.sha(science['tasklist.md'])
            else:vote.update(grounds=['dead_end'],signed_dossier_digest=l.proposal_digest(science))
            l.save(source/name,vote)
            rel=l.rs.freeze(source,self.home/('signed-'+role),role,s['actor_id'],s['session_id'],t['topic'],state['source_commit'],s['packet_sha256'])
            t['latest'][role]=str(rel);t['history'].append(str(rel))
        return t
    def test_matching_experiment_consents_are_recognized(self):
        t=self.consented('experiment');self.assertTrue(l.consent_check(t,'experiment'))
    def test_matching_abandonment_consents_are_recognized(self):
        t=self.consented('abandonment');self.assertTrue(l.consent_check(t,'abandonment'))
    def test_consents_do_not_survive_scientific_revision(self):
        t=self.consented('experiment');old=t['latest']['proposer'];m,p=l.rs.verify(old)
        source=self.home/'changed';source.mkdir()
        for n,b in p.items():(source/n).write_bytes(b)
        (source/'tasklist.md').write_text('Changed dependencies')
        rel=l.rs.freeze(source,self.home/'changed-submissions','proposer',m['actor_id'],m['session_id'],m['topic'],m['input_commit'],m['packet_sha256'])
        t['latest']['proposer']=str(rel)
        self.assertFalse(l.consent_check(t,'experiment'))
    def test_publication_failure_retains_round_and_does_not_block_research(self):
        self.tick();self.tick();self.tick();self.c['publication']['enabled']=True
        def unavailable(*a,**kw):raise ValueError('Synthetic GitHub outage')
        out=l.tick(self.c,self.home,executor=self.fake,publisher=unavailable)
        state=l.read(self.home/'state.json')
        self.assertEqual(out['status'],'advanced')
        self.assertIn('publication_error',state['publication_queue'][0])
        self.assertEqual(state['published'],{})
    def test_app_publication_failure_is_durable_and_retryable(self):
        self.tick();self.tick();self.tick()
        with patch.object(l,'publish_record',side_effect=ValueError('Synthetic network failure')):
            self.assertEqual(l.publish_pending(self.c,self.home),[])
        s=l.read(self.home/'state.json')
        self.assertIn('publication_error',s['publication_queue'][0])
        with patch.object(l,'publish_record',return_value='https://example.invalid/pr/1'):
            self.assertEqual(l.publish_pending(self.c,self.home),['https://example.invalid/pr/1'])
        s=l.read(self.home/'state.json')
        self.assertNotIn('publication_error',s['publication_queue'][0])
        self.assertEqual(len(s['publication_queue']),1)
    def test_app_merge_connection_failure_does_not_lose_publication(self):
        self.tick();self.tick();self.tick();s=l.read(self.home/'state.json')
        key=s['publication_queue'][0]['verification_release'];url='https://example.invalid/pr/1'
        s['published'][key]=url;l.save(self.home/'state.json',s)
        self.c['publication']['auto_merge']=True
        with patch.object(l,'merge_checked',side_effect=OSError('Synthetic TLS failure')):
            l.publish_pending(self.c,self.home)
        s=l.read(self.home/'state.json')
        self.assertEqual(s['published'][key],url)
        self.assertIn(url,s['merge_errors'])
    def test_unregistered_release_identity_is_refused(self):
        state=l.read(self.home/'state.json');t=state['topics']['EDA-0002'];job=l.job_for(state,t,self.c)
        result=self.fake(self.c,job);t['seats']['proposer']['session_id']='different'
        with self.assertRaises(ValueError):l.validate_result(state,t,job,result)
    def test_verifier_must_rule_on_every_objection(self):
        self.tick();self.tick();state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        job=l.job_for(state,t,self.c);self.fake(self.c,job);work=Path(job['work'])
        v=l.read(work/'release/verification.json');v['objections']=[];l.save(work/'release/verification.json',v)
        a=l.read(work/'JOB.json');release=l.rs.freeze(work/'release',work/'submissions','verifier',a['actor_id'],a['session_id'],a['topic'],a['input_commit'],a['packet_sha256'])
        with self.assertRaisesRegex(ValueError,'omitted'):
            l.validate_result(state,t,job,{'status':'complete','release_id':release.name})
    def test_four_completed_cycles_stop_further_dispatch(self):
        self.c['stop_after_rounds']=4;self.c['max_substantive_rounds']=4
        l.save(self.home/'settings.json',self.c)
        for _ in range(12):self.tick()
        t=self.topic();self.assertEqual(t['round'],4)
        self.assertEqual(t['status'],'stopped_after_round_limit')
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'finished')
        self.assertEqual(self.tick()['status'],'idle')
    def test_successor_uses_remaining_domain_budget_and_cannot_start_fifth_cycle(self):
        self.c['stop_after_rounds']=4;self.c['max_substantive_rounds']=4
        l.save(self.home/'settings.json',self.c)
        for _ in range(6):self.tick()
        self.tick();self.tick();self.action='park';self.tick()
        self.action='revise'
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            for _ in range(3):self.tick()
        state=l.read(self.home/'state.json')
        self.assertEqual(sum(t['round'] for t in state['topics'].values()),4)
        self.assertEqual(len(state['topics']),2)
        self.assertEqual(l.dispatch(self.c,self.home,'D05')['status'],'finished')
        self.assertEqual(self.tick()['status'],'idle')
    def test_app_backend_does_not_use_native_model_fallback(self):
        with self.assertRaisesRegex(ValueError,'app-agent'):
            l.execute({'backend':'codex_app_agents'},{})
    def test_two_domain_jobs_can_be_dispatched_without_shared_workspaces(self):
        state=l.read(self.home/'state.json')
        entry=l.read(ROOT/'config/codex-research.json')['topics']['EDA-0001']
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            l.add_topic(state,self.c,self.home,'EDA-0001',entry)
        l.save(self.home/'state.json',state);l.transport_config(state,self.home)
        a=l.dispatch(self.c,self.home,'D04');b=l.dispatch(self.c,self.home,'D05')
        self.assertNotEqual(a['work'],b['work'])
        self.assertEqual(a['role'],'proposer');self.assertEqual(b['role'],'proposer')


class ReleaseBindings(unittest.TestCase):
    def test_new_active_assignments_match_briefs_and_are_all_codex(self):
        self.assertEqual(l.project.validate_launch_release(ROOT),[])
        c=l.read(ROOT/'config/launch-release.json')
        self.assertEqual(c['active_platforms'],['codex'])
        self.assertEqual(len(c['released_actors']),6)
    def test_live_gate_can_be_opted_into_without_pr_code_execution(self):
        text=(ROOT/'.github/workflows/independent-verifier.yml').read_text()
        self.assertIn('REQUIRE_HUMAN_FINAL_REPORTS',text)
        self.assertIn('const requiresHuman = optInHuman &&',text)
        self.assertNotIn('actions/checkout',text)
