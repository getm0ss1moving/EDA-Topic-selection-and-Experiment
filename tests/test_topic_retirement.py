"""Synthetic retirement evidence/state tests; never live scientific judgments."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import test_codex_loop as fixtures
import test_role_compliance as audits

l = fixtures.l
r = l.retirement
ROOT = fixtures.ROOT
POLICY = json.loads((ROOT/'config/topic-retirement.json').read_text())
BINDING = {'file':'config/topic-retirement.json',
           'sha256':hashlib.sha256((ROOT/'config/topic-retirement.json').read_bytes()).hexdigest(),
           'definition':POLICY}
P, C, V = ['SUB-'+letter*64 for letter in 'abc']


def documents(grades=None, binding=BINDING, proposer=P, challenger=C):
    grades = grades or {}
    axes = []
    objections = []
    for index, axis in enumerate(sorted(r.AXES)):
        grade = grades.get(axis, 'clear')
        refs = ['OBJ-'+str(100+index)] if grade != 'clear' else []
        row = {'axis':axis,'issue_key':axis+'-synthetic-gap','grade':grade,
               'references':refs,'reason':'Synthetic bounded test only.',
               'repair_test':'Synthetic discriminating control, not an executed EDA result.',
               'no_anchor_preserving_repair':grade=='fatal',
               'checked_source_ids':['TEST-S01'] if grade in {'major','fatal'} else []}
        if grade == 'fatal':row['fatal_ground'] = r.FATAL_GROUNDS[axis]
        axes.append(row)
        if refs:
            objections.append({'id':refs[0],'verdict':'unresolved' if grade=='unresolved' else 'valid',
                               'blocking':True})
    screen = {'policy_id':POLICY['policy_id'],'reviewed_proposer_release':proposer,
              'recommendation':'revise','axes':copy.deepcopy(axes)}
    verdict = {'decision':'revise','reviewed_proposer_release':proposer,
               'adjudicated_challenger_releases':[challenger],
               'objections':objections,'source_checks':[{'id':'TEST-S01','access_level':'full','verdict':'verified',
                   'url':'https://example.invalid/primary-fixture','locator':'Synthetic assumption 1'}],
               'elimination_review':{'policy_id':POLICY['policy_id'],'policy_sha256':binding['sha256'],
                   'reviewed_proposer_release':proposer,'reviewed_challenger_release':challenger,
                   'axes':axes,'resurrection_conditions':['A new independently checked synthetic counterexample.']}}
    return screen, verdict


def point(grades=None, digest='1'*64, **kwargs):
    screen, verdict = documents(grades)
    return r.validated_point(BINDING,screen,verdict,P,C,V,digest,**kwargs)


class ScoreTests(unittest.TestCase):
    def test_clear_science_is_not_retired_even_if_challenger_requests_it(self):
        screen, verdict = documents();screen['recommendation'] = 'retire'
        value = r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)
        self.assertEqual(value['score'],0)
        self.assertIsNone(r.evaluate(POLICY,[],value))

    def test_confirmed_fatal_retires_without_inventing_dual_consent(self):
        value = point({'mechanism':'fatal'})
        result = r.evaluate(POLICY,[],value)
        self.assertEqual(result['reason'],'verified_fatal')
        self.assertNotIn('consents',result)

    def test_persistent_unknowns_stop_investment_without_refutation(self):
        grades = {axis:'unresolved' for axis in ('novelty','utility','mechanism')}
        first = point(grades);second = point(grades,digest='2'*64)
        self.assertEqual(first['score'],6)
        self.assertIsNone(r.evaluate(POLICY,[],first))
        result = r.evaluate(POLICY,[first],second)
        self.assertEqual(result['epistemic_status'],'portfolio_stop_not_scientific_refutation')

    def test_metadata_or_consent_republication_cannot_manufacture_attempt(self):
        grades = {axis:'major' for axis in ('novelty','utility')}
        first = point(grades);second = point(grades)
        second['proposer_release'] = 'SUB-'+'d'*64
        self.assertIsNone(r.evaluate(POLICY,[first],second))

    def test_low_risk_breaks_streak_and_different_axes_do_not_accumulate(self):
        first = point({x:'unresolved' for x in ('novelty','utility','mechanism')})
        low = point(digest='2'*64)
        last = point({x:'unresolved' for x in ('novelty','utility','mechanism')},digest='3'*64)
        self.assertIsNone(r.evaluate(POLICY,[first,low],last))
        other = point({'anchor':'major','headroom':'major','contest_originality':'major'},digest='4'*64)
        self.assertEqual(other['score'],8)
        self.assertIsNone(r.evaluate(POLICY,[first],other))

    def test_refuted_partial_unknown_and_nonblocking_cannot_be_fatal(self):
        for verdict_value in ('unresolved','refuted','unsupported','partially_valid'):
            screen, verdict = documents({'novelty':'fatal'})
            verdict['objections'][0]['verdict'] = verdict_value
            with self.subTest(verdict=verdict_value),self.assertRaises(ValueError):
                r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)
        screen, verdict = documents({'novelty':'fatal'});verdict['objections'][0]['blocking'] = False
        with self.assertRaisesRegex(ValueError,'nonblocking'):
            r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)

    def test_full_source_and_no_repair_are_required_for_fatal(self):
        for damage in ('abstract','no-repair','budget-ground'):
            screen, verdict = documents({'experiments':'fatal'})
            row = next(x for x in verdict['elimination_review']['axes'] if x['axis']=='experiments')
            if damage=='abstract':verdict['source_checks'][0]['access_level']='abstract'
            elif damage=='no-repair':row['no_anchor_preserving_repair']=False
            else:row['fatal_ground']='no_budget'
            with self.subTest(damage=damage),self.assertRaises(ValueError):
                r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)

    def test_one_claim_cannot_inflate_two_axes(self):
        screen, verdict = documents({'novelty':'major','utility':'major'})
        rows = [x for x in verdict['elimination_review']['axes'] if x['grade']=='major']
        rows[1]['references'] = rows[0]['references']
        with self.assertRaisesRegex(ValueError,'inflate'):
            r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)

    def test_blocking_claim_cannot_be_hidden_by_clear_scorecard(self):
        screen,verdict=documents({'novelty':'major'})
        row=next(x for x in verdict['elimination_review']['axes'] if x['axis']=='novelty')
        row.update(grade='clear',references=[],checked_source_ids=[])
        with self.assertRaisesRegex(ValueError,'blocker omitted'):
            r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)
        verdict['objections'][0]['verdict']='refuted'
        self.assertEqual(r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)['score'],0)

    def test_canonical_source_id_and_legacy_id_are_supported_without_ambiguity(self):
        screen,verdict=documents({'mechanism':'fatal'})
        source=verdict['source_checks'][0];source['source_id']=source.pop('id')
        self.assertEqual(r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)['fatal_axes'],['mechanism'])
        source['id']='conflicting-legacy-id'
        with self.assertRaisesRegex(ValueError,'conflicting source identity'):
            r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)
        screen,verdict=documents()
        verdict['source_checks']=[{'source_id':'TEST-S01','locator':'Synthetic scope',
            'verdict':'verified','checked_at':'2026-10-16','entailment':'No retirement claim.'}]
        self.assertEqual(r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)['score'],0)

    def test_stale_pair_policy_and_protocol_reviewer_are_rejected(self):
        for damage in ('proposer','challenger','policy','protocol','missing','key'):
            screen, verdict = documents({'mechanism':'major'})
            rev = verdict['elimination_review']
            if damage=='proposer':rev['reviewed_proposer_release']='SUB-'+'d'*64
            elif damage=='challenger':rev['reviewed_challenger_release']='SUB-'+'d'*64
            elif damage=='policy':rev['policy_sha256']='0'*64
            elif damage=='protocol':verdict['purpose']='protocol_audit'
            elif damage=='missing':rev['axes'].pop()
            else:rev['axes'][0]['issue_key']='renamed-without-binding'
            with self.subTest(damage=damage),self.assertRaises(ValueError):
                r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)

    def test_headroom_fatal_requires_locked_metric_and_numeric_bound(self):
        screen, verdict = documents({'headroom':'fatal'})
        row = next(x for x in verdict['elimination_review']['axes'] if x['axis']=='headroom')
        row.update(primary_metric='WNS improvement ps',remaining_improvement_upper_bound=0.5)
        with self.assertRaises(ValueError):
            r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64)
        contract={'primary_metric':'WNS improvement ps','minimum_meaningful_effect':1.0}
        value=r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64,contract)
        self.assertEqual(value['fatal_axes'],['headroom'])
        for bound in (1.0,-1,float('inf'),True):
            row['remaining_improvement_upper_bound']=bound
            with self.subTest(bound=bound),self.assertRaises(ValueError):
                r.validated_point(BINDING,screen,verdict,P,C,V,'1'*64,contract)

    def test_policy_mixing_and_invalid_numeric_thresholds_fail(self):
        first=point();second=point(digest='2'*64);second['policy_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'mixed-policy'):
            r.evaluate(POLICY,[first],second)
        for value in (True,0,1):
            policy=copy.deepcopy(POLICY);policy['persistent_rounds']=value
            with self.subTest(value=value),self.assertRaises(ValueError):r.validate_policy(policy)


class LoopRetirementTests(unittest.TestCase):
    ledger = audits.AuditedLoopTests.ledger
    freeze = audits.AuditedLoopTests.freeze
    audit = audits.AuditedLoopTests.audit

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()
        self.home=self.root/'runtime';self.c=l.read(ROOT/'legacy/config/codex-research.json')
        self.c['topics']={'EDA-0002':dict(self.c['topics']['EDA-0002'],seed_prefix=None,handover_prefixes={})}
        self.c.update(require_compliance=True,max_substantive_rounds=10)
        self.c.pop('stop_after_rounds',None);self.c['publication']={'enabled':False,'auto_merge':False}
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            l.prepare(self.c,self.home,l.git('rev-parse','HEAD'))
        self.action='revise';self.proposal_number=0

    def tearDown(self):
        for p in self.root.rglob('*'):
            if not p.is_symlink():p.chmod(0o755 if p.is_dir() else 0o644)
        self.tmp.cleanup()

    def turn(self, grades=None):
        job=l.dispatch(self.c,self.home,'D05');work=Path(job['work'])
        fixtures.LoopTests.fake(self,self.c,job)
        a=l.read(work/'JOB.json');flow=l.read(work/'release/workflow.json')
        state=l.read(self.home/'state.json');t=state['topics'][a['topic']]
        if a['role']=='proposer':
            self.proposal_number+=1
            (work/'release/proposal.md').write_text('Synthetic scientific revision '+str(self.proposal_number))
        else:
            pid=Path(t['latest']['proposer']).name
            cid=Path(t['latest']['challenger']).name if a['role']=='verifier' else C
            screen,verdict=documents(grades,state['retirement_policy'],pid,cid)
            if a['role']=='challenger':
                flow['elimination_screen']=screen
                (work/'release/challenges.md').write_text('\n'.join(x['id'] for x in verdict['objections']))
            else:l.save(work/'release/verification.json',verdict)
        l.save(work/'release/workflow.json',flow)
        l.save(work/'release/compliance.json',self.ledger(a));self.freeze(work)
        return l.collect(self.c,self.home,'D05'),work

    def cycle(self, grades):
        for _ in range(3):self.turn(grades)

    def test_frozen_policy_reaches_all_roles_and_new_jobs(self):
        state=l.read(self.home/'state.json');binding=state['retirement_policy']
        for seat in state['topics']['EDA-0002']['seats'].values():
            self.assertEqual(l.sha(Path(seat['packet'])/binding['file']),binding['sha256'])
            self.assertTrue((Path(seat['packet'])/'docs/TOPIC-RETIREMENT.md').is_file())
        job=l.dispatch(self.c,self.home,'D05');a=l.read(Path(job['work'])/'JOB.json')
        self.assertEqual(a['retirement_policy']['sha256'],binding['sha256'])

    def test_new_prepare_defaults_on_even_when_copying_a_pre_policy_config(self):
        config=copy.deepcopy(self.c);config.pop('retirement_policy')
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            state=l.prepare(config,self.root/'new-default',l.git('rev-parse','HEAD'))
        self.assertEqual(state['retirement_policy']['definition']['policy_id'],POLICY['policy_id'])

    def test_mutable_policy_definition_cannot_override_frozen_bytes(self):
        state=l.read(self.home/'state.json')
        state['retirement_policy']['definition']['weights']['novelty']=3
        l.save(self.home/'state.json',state)
        with self.assertRaisesRegex(ValueError,'Frozen retirement policy'):
            l.dispatch(self.c,self.home,'D05')

    def test_mutable_score_cache_cannot_override_frozen_review(self):
        self.cycle({'novelty':'unresolved'});self.audit();l.audit_collect(self.c,self.home,'D05')
        state=l.read(self.home/'state.json');state['topics']['EDA-0002']['retirement_reviews'][0]['score']=99
        l.save(self.home/'state.json',state)
        with self.assertRaisesRegex(ValueError,'Retirement cache'):
            l.dispatch(self.c,self.home,'D05')

    def test_two_cycles_retire_then_audit_then_new_id_preserves_releases(self):
        grades={x:'unresolved' for x in ('novelty','utility','mechanism')}
        self.cycle(grades);self.audit();l.audit_collect(self.c,self.home,'D05')
        self.cycle(grades);state=l.read(self.home/'state.json');old=state['topics']['EDA-0002']
        self.assertEqual(old['status'],'retired_by_policy');self.assertEqual(len(old['history']),6)
        self.assertEqual(state['publication_queue'][-1]['scientific_decision'],'revise')
        l.successor(state,old,self.c,self.home)
        self.assertNotIn('successor',old)  # Cannot create roles before the required audit.
        self.audit();l.audit_collect(self.c,self.home,'D05')
        with patch.object(l,'frozen',side_effect=lambda ref,name:(ROOT/name).read_bytes()):
            job=l.dispatch(self.c,self.home,'D05')
        state=l.read(self.home/'state.json');old=state['topics']['EDA-0002'];new=state['topics'][old['successor']]
        self.assertEqual(job['role'],'proposer');self.assertEqual(new['history'],[])
        self.assertGreater(int(new['topic'][4:]),12)
        prior=l.read(Path(new['seats']['proposer']['base'])/'predecessor.json')
        self.assertEqual(prior['retirement']['reason'],'persistent_decision_critical_risk')
        self.assertEqual(prior['releases'],old['latest'])
        for role in l.ROLES:self.assertNotEqual(new['seats'][role]['session_id'],old['seats'][role]['session_id'])

    def test_retirement_does_not_extend_finite_domain_limit(self):
        self.c['stop_after_rounds']=1;l.save(self.home/'settings.json',self.c)
        self.cycle({'mechanism':'fatal'});self.audit();l.audit_collect(self.c,self.home,'D05')
        before=l.read(self.home/'state.json');result=l.dispatch(self.c,self.home,'D05')
        self.assertEqual(result,{'status':'finished','domain':'D05','rounds':1})
        after=l.read(self.home/'state.json');self.assertEqual(before['topics'].keys(),after['topics'].keys())
        self.assertEqual(after['publication_queue'][0]['decision'],'retired_by_policy')
        self.assertEqual(after['topics']['EDA-0002']['status'],'stopped_after_round_limit')

    def test_critical_protocol_failure_removes_invalid_retirement_credit(self):
        self.cycle({'mechanism':'fatal'});self.audit('blocking_violation')
        self.assertEqual(l.audit_collect(self.c,self.home,'D05')['status'],'quarantined')
        l.recover(self.c,self.home,'D05');state=l.read(self.home/'state.json');t=state['topics']['EDA-0002']
        self.assertEqual(t.get('retirement_reviews',[]),[]);self.assertNotIn('retirement',t)
        self.assertEqual(state['publication_queue'],[])
        self.assertIn('retirement',state['incidents'][0]['round'])

    def test_retirement_certificate_is_in_real_offline_publication(self):
        self.cycle({'mechanism':'fatal'});self.audit();l.audit_collect(self.c,self.home,'D05')
        record=l.read(self.home/'state.json')['publication_queue'][0]
        identity={key:'retirement-test' for key in ('GIT_AUTHOR_NAME','GIT_COMMITTER_NAME')}
        identity.update({key:'retirement-test@example.invalid' for key in ('GIT_AUTHOR_EMAIL','GIT_COMMITTER_EMAIL')})
        with patch.dict(os.environ,identity):
            result=l.publish_record(record,self.c,self.home,dry_run=True)
        self.assertEqual(result['retirement_certificate'],record['retirement'])
        self.assertEqual(set(result['descriptor_roles']),set(l.ROLES)|{'protocol_audit'})


if __name__=='__main__':unittest.main()
