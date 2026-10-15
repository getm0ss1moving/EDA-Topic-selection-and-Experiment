#!/usr/bin/env python3
"""Coordinator-owned, durable ChatGPT/Codex research queue. No provider fallback.

prepare creates private logical seats and frozen inputs, but starts no model.
watch runs a native Codex job whenever a role has work; no sleeping role must wake.
Scientific decisions are authored in role files. The coordinator only checks and routes them.
"""
import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile
import time
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE/(name+'.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

rt = module('round_transmit'); rs = rt.rs
project = module('project')
ROLES = ('proposer', 'challenger', 'verifier')
COVERAGE = {'duplicate_prior_art','mechanism','composition','demand','industry_gap',
            'headroom','contests','experiments','cost'}
COMMON = ('CHARTER', 'WORKFLOW', 'EVIDENCE', 'ISOLATION', 'AUTO-ROUND', 'SELF-SUBMISSION', 'CODEX-AUTOMATION', 'INNOVATION-STRATEGY')
FINAL = {'type':'object','properties':{'status':{'type':'string','enum':['complete','blocked']},
         'release_id':{'type':['string','null']},'reason':{'type':'string'}},
         'required':['status','release_id','reason'],'additionalProperties':False}


def read(p): return json.loads(rs.regular(Path(p)))
def save(p, data):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix('.tmp'); tmp.write_bytes(rs.encoded(data)); os.replace(tmp,p)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*args, cwd=ROOT): return subprocess.check_output(['git',*args],cwd=cwd,text=True).strip()
def frozen(ref, name): return subprocess.check_output(['git','show',f'{ref}:{name}'],cwd=ROOT,stderr=subprocess.DEVNULL)
def freeze_tree(path):
    for p in path.rglob('*'): p.chmod(0o555 if p.is_dir() else 0o444)
    path.chmod(0o555)


def config(path):
    c=read(path)
    if c.get('platform') != 'OpenAI Codex' or set(c.get('models',{})) != set(ROLES):
        raise ValueError('Only the three configured Codex roles are supported')
    if any(not x['model'].startswith('gpt-') for x in c['models'].values()):
        raise ValueError('Non-GPT model route refused')
    root=(ROOT/c['runtime_root']).resolve()
    if root == ROOT or ROOT in root.parents:
        raise ValueError('Runtime and private work must be outside the checkout')
    return c,root


def add_topic(state,c,home,topic,entry,seed=True):
    """Register logical seats before any role writes or freezes. Not a host-session claim."""
    if topic in state['topics']: return
    t={'topic':topic,'domain':entry['domain'],'phase':'proposer','round':0,'status':'researching',
       'latest':{},'history':[],'seats':{},'not_before':0,'job':None,'closure':None}
    for role in ROLES:
        actor=entry['actors'][role]
        base=home/topic/actor
        base.mkdir(parents=True,exist_ok=False); base.chmod(0o700)
        packet=base/'packet';packet.mkdir()
        names=['AGENTS.md',f'harness/{role.upper()}.md','config/research-brief.json',
               f'domains/{entry["domain"]}/brief.json','scripts/role_submission.py','scripts/project.py']
        names += [f'docs/{x}.md' for x in COMMON]
        if c.get('batch_brief'):
            brief=Path(c['batch_brief'])
            if brief.is_absolute() or not brief.parts or '..' in brief.parts or brief.parts[0]!='docs':
                raise ValueError('Batch brief must be a repository-relative docs path')
            names.append(str(brief))
        names += [str(p.relative_to(ROOT)) for p in (ROOT/'templates/topic').iterdir() if p.is_file()]
        for name in names:
            p=packet/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(frozen(state['source_commit'],name))
        for prefix in entry.get('handover_prefixes',{}).get(role,[]):
            listed=git('ls-tree','-r','--name-only',state['source_commit'],'--',prefix).splitlines()
            for name in listed:
                if not name.startswith(prefix):raise ValueError('Handover prefix escape')
                dest=packet/'released-handover'/name[len(prefix):]
                dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes(frozen(state['source_commit'],name))
        if role=='proposer' and seed and entry.get('seed_prefix'):
            # Historical *released* proposal only. No old challenge/verifier or private notes.
            for name in rs.FILES['proposer']:
                try: body=frozen(state['source_commit'],entry['seed_prefix']+name)
                except subprocess.CalledProcessError: continue
                p=packet/'released-seed'/name;p.parent.mkdir(exist_ok=True);p.write_bytes(body)
        manifest={'source_commit':state['source_commit'],'actor_id':actor,'role':role,'topic':topic,
                  'files':{str(p.relative_to(packet)):sha(p) for p in packet.rglob('*') if p.is_file()}}
        save(packet/'PACKET.json',manifest); freeze_tree(packet)
        (base/'inbox').mkdir()
        for sender in ROLES:
            if role in rt.ROUTES[sender]:(base/'inbox'/f'from-{sender}').mkdir()
        t['seats'][role]={'actor_id':actor,'session_id':str(uuid.uuid4()),'packet':str(packet),
                          'packet_sha256':sha(packet/'PACKET.json'),'inbox':str(base/'inbox'),
                          'base':str(base),'platform':'OpenAI Codex'}
    state['topics'][topic]=t


def transport_config(state,home):
    cfg={'schema':1,'topics':{}}
    for topic,t in state['topics'].items():
        cfg['topics'][topic]={'challenger_stage':'full','challenger_stage_basis':
            'Unblinded automatic review. No forecast-blindness claim or manual release dependency.',
            'roles':{r:{k:t['seats'][r][k] for k in ('actor_id','session_id','inbox')} for r in ROLES}}
    save(home/'round-transport.json',cfg)


def prepare(c,home,ref):
    if not re.fullmatch(r'[0-9a-f]{40}',ref) or git('cat-file','-t',ref)!='commit':
        raise ValueError('A frozen full commit is required')
    if (home/'state.json').exists():raise ValueError('Already prepared; use status/watch rather than replacing state')
    home.mkdir(parents=True,exist_ok=True);home.chmod(0o700)
    state={'schema':1,'source_commit':ref,'topics':{},'publication_queue':[],'published':{},'events':[]}
    save(home/'settings.json',c)
    for topic,entry in c['topics'].items(): add_topic(state,c,home,topic,entry)
    transport_config(state,home);save(home/'state.json',state)
    return state


def registry(state):
    return {'sessions':[{'session_id':s['session_id'],'role':r,'actor_id':s['actor_id'],
             'topic':topic,'platform':'OpenAI Codex','model':read(Path(s['base']).parents[1]/'settings.json')['models'][r]['model'],
             'operator':'getm0ss1moving',
             'github_login':'getm0ss1moving (transport account only; not an independent reviewer)',
             'input_commit':state['source_commit'],'packet_sha256':s['packet_sha256'],
             'session_kind':'logical file-mediated seat; fresh isolated-input execution per job',
             'independence_attestation':'Separate role inputs and own files only; shared OS account, policy isolation.'}
             for topic,t in state['topics'].items() for r,s in t['seats'].items()]}


def copy_release(snapshot,dest):
    m,payload=rs.verify(snapshot);dest.mkdir(parents=True,exist_ok=True)
    for name,body in {**payload,'SUBMISSION.json':rs.encoded(m)}.items():(dest/name).write_bytes(body)
    freeze_tree(dest)


def verify_packet(seat):
    packet=Path(seat['packet'])
    if rs.sha(rs.regular(packet/'PACKET.json'))!=seat['packet_sha256']:
        raise ValueError('Assigned packet manifest changed')
    m=read(packet/'PACKET.json')
    present={str(p.relative_to(packet)) for p in packet.rglob('*') if p.is_file()}
    if present!=set(m['files'])|{'PACKET.json'}:
        raise ValueError('Assigned packet entries changed')
    for name,want in m['files'].items():
        if rs.sha(rs.regular(packet/name))!=want:raise ValueError('Assigned packet content changed')


def job_for(state,t,c):
    role=t['phase']; seat=t['seats'][role]
    verify_packet(seat)
    work=Path(seat['base'])/'jobs'/str(uuid.uuid4()); work.mkdir(parents=True)
    shutil.copytree(seat['packet'],work/'policy')
    shared=work/'shared';shared.mkdir()
    paths=[]
    predecessor=Path(seat['base'])/'predecessor.json'
    if predecessor.is_file():
        prior=read(predecessor)
        # These are explicitly released end-of-round outputs, not predecessor memory.
        allowed_prior={'proposer':('proposer','verifier','challenger'),
                       'challenger':('proposer','verifier'),
                       'verifier':ROLES}[role]
        exported={}
        if role=='proposer' and prior['releases'].get('challenger'):
            _,verdict=rs.verify(prior['releases']['verifier'])
            if Path(prior['releases']['challenger']).name not in json.loads(verdict['verification.json']).get('adjudicated_challenger_releases',[]):
                raise ValueError('Predecessor challenge has not been adjudicated')
        (shared/'predecessor').mkdir()
        for sender in allowed_prior:
            old=prior['releases'].get(sender)
            if old:
                dest=shared/'predecessor'/Path(old).name
                copy_release(old,dest);paths.append(str(dest));exported[sender]=str(dest)
        save(shared/'predecessor.json',{**prior,'releases':exported})
        paths.append(str(shared/'predecessor.json'))
    allowed = {'proposer':('verifier',),'challenger':('proposer','verifier'),
               'verifier':('proposer','challenger')}[role]
    for sender in allowed:
        path=t['latest'].get(sender)
        if path:
            copy_release(path,shared/Path(path).name);paths.append(str(shared/Path(path).name))
    if role=='proposer' and t['latest'].get('verifier'):
        # Only challenge releases actually covered by this verifier's file may reach proposer.
        v=read(Path(t['latest']['verifier'])/'verification.json')
        for sid in v.get('adjudicated_challenger_releases',[]):
            found=[p for p in t['history'] if Path(p).name==sid]
            if not found:raise ValueError('Adjudicated release missing from history')
            copy_release(found[-1],shared/sid);paths.append(str(shared/sid))
    if role in t['latest']:
        copy_release(t['latest'][role],work/'own-previous'/Path(t['latest'][role]).name)
    # Consent signatures may refer to an earlier proposer release. Release it explicitly.
    for r in ('proposer','challenger'):
        if r not in t['latest']:continue
        _,payload=rs.verify(t['latest'][r])
        for name in ('experiment-consent.json','abandonment-consent.json'):
            if name not in payload:continue
            sid=json.loads(payload[name]).get('signed_revision')
            for old in t['history']:
                if Path(old).name==sid and not (shared/sid).exists():
                    copy_release(old,shared/sid)
    (work/'release').mkdir();(work/'submissions').mkdir()
    save(work/'result.schema.json',FINAL)
    assignment={'role':role,'topic':t['topic'],'domain':t['domain'],'round':t['round'],
                'actor_id':seat['actor_id'],'session_id':seat['session_id'],'input_commit':state['source_commit'],
                'packet_sha256':seat['packet_sha256'],'phase':t.get('closure') or 'research',
                'released_inputs':paths,'previous_proposal_release':Path(t['latest']['proposer']).name if t['latest'].get('proposer') else None,
                'batch_round':sum(x['round'] for x in state['topics'].values() if x['domain']==t['domain'])+1,
                'batch_round_limit':c.get('stop_after_rounds'),
                'batch_brief':c.get('batch_brief'),
                'models':c['models'],
                'readiness': 'logical seat registered; actual host model is recorded by the execution backend'}
    save(work/'JOB.json',assignment)
    prompt=(f'Run only the {role} role for {t["topic"]}. All artifacts and replies English. '
        'Read JOB.json, policy/docs/CODEX-AUTOMATION.md, common policy, and only your own harness. '
        'The shared folder holds explicitly released inputs; own-previous holds your own prior output. '
        'Independently search accessible external papers, source code, contest statements, newer editions and winner reports. '
        'Do not inspect another role\'s private files, sessions or memory. Do not call agents or send messages. '
        'Do not access the project checkout or GitHub branches for withheld files. No per-source approval is needed. '
        'Use the assigned model only. No provider fallback or new expenditure. '
        'This is academic chip electronic-design-automation research using public or legitimately accessible sources. '
        'Do not conduct cyber intrusion, acquire trade secrets, seek unpublished proprietary designs, '
        'bypass access controls, or retrieve credentials. Public vendor capability claims are research evidence only. '
        'Write complete role-owned files in release/. Include workflow.json per the automation contract. '
        'Verify every source claim, record access limitations, and distinguish prediction from measurement. '
        'For a consent phase preserve scientific content; sign the same explicitly released proposal revision as the other role. '
        'Do not wait or ask for a coordinator to freeze, register, transmit or restart you. '
        'If complete, self-freeze with the following command, then return the release ID in the final JSON; '
        'otherwise return blocked with a precise reason. If retry-note.json exists, read its '
        'mechanical validation error and repair your own output before freezing again.\n' +
        'python3 policy/scripts/role_submission.py freeze --source release --queue submissions '
        f'--role {role} --actor {seat["actor_id"]} --session {seat["session_id"]} --topic {t["topic"]} '
        f'--ref {state["source_commit"]} --packet {seat["packet_sha256"]}\n')
    if c.get('batch_brief'):
        prompt += f'Read the owner batch brief at policy/{c["batch_brief"]} before research. Its scope applies to this and successor topics.\n'
    prompt += ('This owner-authorized batch has exactly four completed P/C/V cycles per domain. '
               'D04 and D05 run independently in parallel. Use this round to make concrete scientific progress; '
               'do not spend it merely asking for infrastructure permission. On rounds 1-3, refine or '
               'collect matching consents as appropriate; on round 4 give your final evidence-backed '
               'feasibility/novelty and task-list position, including any unresolved limits. '
               'No new experiment compute is granted by this batch. Historical records, when supplied, '
               'retain their documented exposure and access limits; review is explicitly unblinded. '
               'Do not inherit independence or treat historical verifier findings as verification of a new revision. '
               'Use released-handover for your own predecessor\'s shared files, never its transcript or scratch. '
               'Write final protocol JSON to result.json in the job root after self-freezing, with status, release_id, reason. '
               'The status must be exactly "complete" or "blocked" per result.schema.json; a successfully frozen '
               'research release uses "complete", even when its scientific decision is revise or unresolved.\n')
    prompt += ('The coordinator runs full-repository validation during publication. This standalone job '
               'does not contain the entire repository or foreign harnesses; use the trusted freeze validator '
               'for your own release and record any limited local checks. Do not browse the checkout to '
               'satisfy a legacy validation instruction. Complete a candid research release even if '
               'scientific gates remain unresolved; that is a review outcome, not an infrastructure block.\n')
    (work/'prompt.txt').write_text(prompt)
    return {'role':role,'work':str(work),'attempt':0}


def command(c,role,work):
    m=c['models'][role]
    return [c['cli'],'--search','-a','never','exec','--ignore-user-config','--ignore-rules',
            '--ephemeral','--skip-git-repo-check','--sandbox','workspace-write',
            '-c','sandbox_workspace_write.network_access=true',
            '-c','features.memories=false','-c','features.multi_agent=false',
            '-c',f'model_reasoning_effort="{m["effort"]}"','--model',m['model'],
            '--cd',str(work),'--output-schema',str(work/'result.schema.json'),
            '--output-last-message',str(work/'result.json'),'-']


def execute(c,job):
    if c.get('backend')=='codex_app_agents':
        raise ValueError('This batch requires exact-model app-agent dispatch/collect; native CLI refused this account/model')
    work=Path(job['work'])
    if (work/'result.json').is_file():return read(work/'result.json')
    if (work/'process.json').exists():
        pid=read(work/'process.json')['pid']
        try: os.kill(pid,0)
        except ProcessLookupError: pass
        else: raise ValueError('Previous role process still exists; refusing a duplicate consumer')
    # No inherited API/provider overrides; use the existing local Codex login.
    env={k:v for k,v in os.environ.items() if k in ('PATH','HOME','USER','LOGNAME','SHELL','TMPDIR','LANG','TERM')}
    with open(work/'runtime.log','ab') as log:
        proc=subprocess.Popen(command(c,job['role'],work),cwd=work,env=env,
                stdin=subprocess.PIPE,stdout=log,stderr=log,start_new_session=True)
        save(work/'process.json',{'pid':proc.pid,'started':time.time()})
        try:
            proc.communicate((work/'prompt.txt').read_bytes(),timeout=c['turn_timeout_seconds'])
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
            raise ValueError('Role turn timed out; its files remain for retry')
        finally:
            if proc.poll() is not None:
                (work/'process.json').unlink(missing_ok=True)
    if proc.returncode or not (work/'result.json').is_file():
        raise ValueError(f'Codex execution failed (exit {proc.returncode}); private log retained')
    return read(work/'result.json')


def consent_check(t,kind):
    """No coordinator signatures, stale task-list reuse, or hand-written agreement flags."""
    name='experiment-consent.json' if kind=='experiment' else 'abandonment-consent.json'
    votes=[]
    for role in ('proposer','challenger'):
        m,p=rs.verify(t['latest'][role])
        if name not in p:return False
        vote=json.loads(p[name])
        if vote['session_id']!=m['session_id'] or vote['decision']!='agree':return False
        votes.append(vote)
    target=votes[0]['signed_revision']
    if target!=votes[1]['signed_revision']:return False
    prior=next((p for p in t['history'] if Path(p).name==target),None)
    if prior is None:return False
    m,payload=rs.verify(prior)
    if m['role']!='proposer':return False
    _,current=rs.verify(t['latest']['proposer'])
    # A consent-only release cannot change its target's science.
    names=rs.FILES['proposer']-{'workflow.json','experiment-consent.json','abandonment-consent.json'}
    if any(payload.get(n)!=current.get(n) for n in names):return False
    if kind=='experiment':
        h=rs.sha(payload['tasklist.md'])
        return all(v['tasklist_sha256']==h for v in votes)
    digest=proposal_digest(payload)
    return (set(votes[0]['grounds'])==set(votes[1]['grounds']) and
            all(v['signed_dossier_digest']==digest for v in votes))


def proposal_digest(payload):
    """Sign frozen proposer scientific bytes, excluding release/consent self-reference."""
    selected={k:v for k,v in payload.items() if k not in {'workflow.json','experiment-consent.json','abandonment-consent.json'}}
    with tempfile.TemporaryDirectory() as td:
        for n,b in selected.items():(Path(td)/n).write_bytes(b)
        return project.digest(Path(td))


def validate_result(state,t,job,result):
    role=job['role']
    if result.get('status')!='complete':raise ValueError(result.get('reason') or 'Role reports blocked')
    sid=result.get('release_id')
    if not isinstance(sid,str) or not rt.SUB.fullmatch(sid):raise ValueError('No valid frozen release ID')
    snapshot=Path(job['work'])/'submissions'/sid
    m,p=rs.verify(snapshot);s=t['seats'][role]
    if (m['role'],m['topic'],m['actor_id'],m['session_id'],m['input_commit'],m['packet_sha256']) != (
        role,t['topic'],s['actor_id'],s['session_id'],state['source_commit'],s['packet_sha256']):
        raise ValueError('Frozen release does not match assigned role/input')
    flow=json.loads(p.get('workflow.json',b'{}'))
    if flow.get('role')!=role:raise ValueError('workflow.json role mismatch')
    if role in ('challenger','verifier'):
        if flow.get('reviewed_proposer_release')!=Path(t['latest']['proposer']).name:
            raise ValueError('Review names a stale or missing proposer release')
    if role=='challenger':
        if flow.get('assessment') not in {'revise','not_meaningful','feasible','unresolved'}:
            raise ValueError('Missing challenger assessment')
        if set(flow.get('coverage',{}))!=COVERAGE or not all(
                x in {'supported','unresolved','not_applicable'} for x in flow['coverage'].values()):
            raise ValueError('Missing or invalid challenger coverage ledger')
    if role=='verifier':
        v=json.loads(p['verification.json']);expected=Path(t['latest']['challenger']).name
        if v.get('reviewed_proposer_release')!=flow['reviewed_proposer_release'] or v.get('adjudicated_challenger_releases')!=[expected]:
            raise ValueError('Verifier must bind the current proposer/challenger pair')
        _,cp=rs.verify(t['latest']['challenger'])
        objections=set(re.findall(r'\bOBJ-\d+\b',cp['challenges.md'].decode()))
        judged={o.get('id',o.get('objection_id')) for o in v.get('objections',[])}
        if not objections<=judged:raise ValueError('Verifier omitted objection verdicts')
        if any(o.get('verdict') not in {'valid','partially_valid','unsupported','refuted','unresolved'}
               for o in v.get('objections',[])):
            raise ValueError('Invalid objection verdict')
        if flow.get('next_action') not in {'revise','consent_experiment','consent_abandonment','accept_for_pilot','abandon','park'}:
            raise ValueError('Invalid next action')
    return snapshot,p,flow


def accept_result(state,t,job,result,home):
    snapshot,p,flow=validate_result(state,t,job,result)
    role=job['role']
    if role=='verifier':
        action=flow['next_action'];v=json.loads(p['verification.json'])
        if action=='accept_for_pilot':
            if not consent_check(t,'experiment'):raise ValueError('Experiment dual consent absent or stale')
            _,pp=rs.verify(t['latest']['proposer'])
            direction=json.loads(pp['direction-control.json'])
            if v.get('decision')!='accept_for_pilot' or set(v.get('gates',{}))!=project.GATES or not all(x is True for x in v['gates'].values()):
                raise ValueError('Acceptance gates incomplete')
            if direction['penalties']['total']!=0 or not v.get('experiment_consensus_checked') or not v.get('direction_penalty_checked'):
                raise ValueError('Acceptance controls incomplete')
            if not v.get('source_checks') or any(o.get('blocking') and o.get('resolution')!='resolved' for o in v.get('objections',[])):
                raise ValueError('Unchecked sources or unresolved blockers')
            if v.get('proposal_digest')!=proposal_digest(pp):
                raise ValueError('Selection must bind the checked proposer scientific bytes')
        elif action=='abandon':
            if not consent_check(t,'abandonment') or v.get('abandonment_process_checked') is not True:
                raise ValueError('Abandonment needs both matching consents and evidence verification')
            if not v.get('source_checks'):raise ValueError('Abandonment evidence missing')
    # State tracks only actor-authored frozen output, never private runtime logs.
    t['latest'][role]=str(snapshot)
    if str(snapshot) not in t['history']:t['history'].append(str(snapshot))
    rt.send(home/'round-transport.json',snapshot,
            [Path(t['latest']['challenger']).name] if role=='verifier' else (),
            ledger=Path(t['seats'][role]['base'])/'transmissions.jsonl',
            reviews=Path(t['latest']['proposer']).name if role=='verifier' else None)
    if role=='proposer':t['phase']='challenger'
    elif role=='challenger':t['phase']='verifier'
    else:
        action=flow['next_action'];t['round']+=1 if read(home/'settings.json').get('stop_after_rounds') else (0 if t['closure'] else 1)
        record={'topic':t['topic'],'round':t['round'],'decision':action,
                'releases':dict(t['latest']),'registrations':registry(state),
                'verification_release':snapshot.name,'source_commit':state['source_commit']}
        state['publication_queue'].append(record)
        limit=read(home/'settings.json').get('stop_after_rounds')
        completed=sum(x['round'] for x in state['topics'].values() if x['domain']==t['domain'])
        t['last_scientific_decision']=action
        if action in ('accept_for_pilot','abandon','park'):
            t['status']={'accept_for_pilot':'selected_for_pilot','abandon':'abandoned','park':'parked'}[action]
        elif t['round']>=read(home/'settings.json')['max_substantive_rounds'] and action=='revise':
            t['status']='parked';record['decision']='parked_round_limit';record['reason']='Unresolved after the configured research rounds; no fabricated consent.'
        else:
            t['closure']={'consent_experiment':'experiment','consent_abandonment':'abandonment'}.get(action)
            t['phase']='proposer'
        if limit and completed>=limit:
            t['status']='stopped_after_round_limit'
        elif limit and action=='accept_for_pilot':
            # Extra rounds are audits, not a silent override of the scientific verdict.
            t['status']='researching';t['phase']='proposer';t['closure']='experiment'
    t['job']=None;t['not_before']=0


def successor(state,t,c,home):
    if t['status'] not in ('abandoned','parked') or t.get('successor'):return
    if c.get('stop_after_rounds') and sum(x['round'] for x in state['topics'].values()
            if x['domain']==t['domain'])>=c['stop_after_rounds']:return
    cap=c.get('max_topics_per_domain')
    if cap and sum(x['domain']==t['domain'] for x in state['topics'].values())>=cap:return
    ids=[int(x[4:]) for x in state['topics']]
    # Include repository IDs; never reuse an archived or accepted ID.
    for area in ('candidates','topics','archive'):
        ids += [int(p.name[4:]) for p in (ROOT/area).glob('EDA-*') if project.ID.fullmatch(p.name)]
    topic=f'EDA-{max(ids+[0])+1:04d}'
    entry={'domain':t['domain'],'actors':{r:t['seats'][r]['actor_id'].split('-EDA-')[0]+'-'+topic for r in ROLES}}
    add_topic(state,c,home,topic,entry,seed=False)
    t['successor']=topic
    # Only explicitly released negative evidence becomes successor input, never private reasoning.
    new=state['topics'][topic]
    for r in ROLES:
        packet=Path(new['seats'][r]['packet'])
        # Packet remains frozen; deliver a separate shared closure record instead.
        save(Path(new['seats'][r]['base'])/'predecessor.json',
             {'topic':t['topic'],'status':t['status'],'releases':dict(t['latest']),
              'note':'Historical released outputs; recheck sources; no inherited acceptance/signatures.'})
    transport_config(state,home)


def publish_record(record,c,home,dry_run=False):
    """One idempotent branch/PR per completed three-role round, including registrations."""
    key=record['verification_release'][4:20]
    branch=f'codex/round-{record["topic"].lower()}-{key}'
    slug='getm0ss1moving/EDA-Topic-selection-and-Experiment'
    def cmd(*a,cwd=ROOT):return subprocess.check_output(a,cwd=cwd,text=True,timeout=60).strip()
    if not dry_run:
        prs=json.loads(cmd('gh','pr','list','--repo',slug,'--head',branch,'--state','all','--json','url'))
        if prs:return prs[0]['url']
    with tempfile.TemporaryDirectory(prefix='eda-codex-publish-') as tmp:
        repo=Path(tmp).resolve()/'repo'
        cmd('git','clone','--quiet','--no-hardlinks',str(ROOT),str(repo))
        remote=git('remote','get-url','origin')
        if remote!='https://github.com/'+slug+'.git':raise ValueError('Unexpected remote')
        cmd('git','remote','set-url','origin',remote,cwd=repo)
        cmd('git','fetch','--quiet','origin','main',cwd=repo)
        cmd('git','checkout','--quiet','-b',branch,'origin/main',cwd=repo)
        for path in record['releases'].values():
            m,payload=rs.verify(path);dest=repo/'runs'/Path(path).name;dest.mkdir(exist_ok=True)
            for n,b in {**payload,'SUBMISSION.json':rs.encoded(m)}.items():
                if (dest/n).exists() and (dest/n).read_bytes()!=b:raise ValueError('Existing release differs')
                (dest/n).write_bytes(b)
        # Consents can name an earlier release; publish that target as well.
        published_ids={Path(p).name for p in record['releases'].values()}
        for role in ('proposer','challenger'):
            _,payload=rs.verify(record['releases'][role])
            for name in ('experiment-consent.json','abandonment-consent.json'):
                target=json.loads(payload.get(name,b'{}')).get('signed_revision')
                if target and target.startswith('SUB-') and target not in published_ids:
                    candidates=list(home.glob(f'*/**/submissions/{target}'))
                    if not candidates:raise ValueError('Consent target not found for publication')
                    m,p=rs.verify(candidates[0]);dest=repo/'runs'/target;dest.mkdir(exist_ok=True)
                    for n,b in {**p,'SUBMISSION.json':rs.encoded(m)}.items():(dest/n).write_bytes(b)
                    published_ids.add(target)
        public={k:v for k,v in record.items() if k!='releases' and not k.startswith('publication_')}
        public['releases']={r:'runs/'+Path(p).name for r,p in record['releases'].items()}
        save(repo/'runs'/f'CODEX-ROUND-{record["topic"]}-{key}'/'round.json',public)
        # Registry travels atomically with this round; no registration PR has to merge first.
        registry_path=repo/'config/roles.json';registered=read(registry_path)
        by={s['session_id']:s for s in registered['sessions']}
        for s in record['registrations']['sessions']:
            if s['session_id'] in by and by[s['session_id']]!=s:raise ValueError('Session registration changed')
            by[s['session_id']]=s
        registered['sessions']=list(by.values());save(registry_path,registered)
        validation=subprocess.run(['python3','scripts/project.py','validate'],cwd=repo,
                                  capture_output=True,text=True)
        if validation.returncode:
            raise ValueError('Publication validation failed:\n'+validation.stdout+validation.stderr)
        cmd('git','add','runs','config/roles.json',cwd=repo)
        cmd('git','commit','--quiet','-m',f'Publish {record["topic"]} research round: {record["decision"]}',cwd=repo)
        if dry_run:return {'dry_run':True,'branch':branch,'commit':git('rev-parse','HEAD',cwd=repo)}
        if cmd('git','ls-remote','--heads','origin',branch,cwd=repo):
            # A network failure after push must not strand the durable publication.
            # Reuse only a branch whose complete patch and bytes match our record.
            cmd('git','fetch','--quiet','origin',branch,cwd=repo)
            remote_base=cmd('git','merge-base','origin/main','FETCH_HEAD',cwd=repo)
            remote_files=set(cmd('git','diff','--name-only',remote_base,'FETCH_HEAD',cwd=repo).splitlines())
            expected_files={'config/roles.json',
                f'runs/CODEX-ROUND-{record["topic"]}-{key}/round.json'}
            for sid in published_ids:
                expected_files.update(str(p.relative_to(repo)) for p in (repo/'runs'/sid).rglob('*') if p.is_file())
            if not remote_files.issubset(expected_files):
                raise ValueError('Existing remote branch has unexpected changes; preserved')
            for name in expected_files:
                remote_bytes=subprocess.check_output(['git','show',f'FETCH_HEAD:{name}'],cwd=repo)
                if remote_bytes!=(repo/name).read_bytes():
                    raise ValueError('Existing remote branch differs from publication record; preserved')
        else:
            cmd('git','push','--quiet','origin',branch,cwd=repo)
        body=Path(tmp)/'body.md'
        body.write_text(f'Automatic three-role round for {record["topic"]}. Decision: `{record["decision"]}`.\n\n'
                        'The round includes the frozen proposer, challenger and verifier outputs, '
                        'their exact logical registrations and provenance. Scientific verdicts belong to the verifier. '
                        'Research selection does not allocate new compute.\n')
        return cmd('gh','pr','create','--repo',slug,'--head',branch,'--base','main',
                   '--title',f'{record["topic"]}: {record["decision"]} ({key})','--body-file',str(body),cwd=repo)


def merge_checked(url):
    """Coordinator transport merge only, no self-approval or protection bypass."""
    # Ignore this invocation's branch and inspect the exact PR head through GitHub.
    detail=json.loads(subprocess.check_output(['gh','pr','view',url,'--json',
        'state,headRefOid,statusCheckRollup,mergeStateStatus'],text=True,timeout=60))
    if detail['state']=='MERGED':return True
    if detail['state']!='OPEN':return False
    checks=detail.get('statusCheckRollup') or []
    if not checks or not all(x.get('conclusion') in {'SUCCESS','NEUTRAL','SKIPPED'} or
                             x.get('state')=='SUCCESS' for x in checks):return False
    if detail.get('mergeStateStatus')=='BEHIND':
        subprocess.run(['gh','pr','update-branch',url],check=True,timeout=60)
        return False
    if detail.get('mergeStateStatus')!='CLEAN':return False
    subprocess.run(['gh','pr','merge',url,'--squash','--delete-branch',
                    '--match-head-commit',detail['headRefOid']],check=True,timeout=60)
    return True


def dispatch(c,home,domain):
    """Prepare one exact-model app-agent job; never spawn a native fallback."""
    state=read(home/'state.json')
    for t in list(state['topics'].values()):successor(state,t,c,home)
    done=sum(t['round'] for t in state['topics'].values() if t['domain']==domain)
    if c.get('stop_after_rounds') and done>=c['stop_after_rounds']:
        save(home/'state.json',state);return {'status':'finished','domain':domain,'rounds':done}
    choices=[t for t in state['topics'].values() if t['domain']==domain and t['status']=='researching']
    if not choices:return {'status':'no_ready_topic','domain':domain}
    t=choices[0]
    if not t['job']:t['job']=job_for(state,t,c)
    save(home/'state.json',state)
    return {'status':'ready','topic':t['topic'],'domain':domain,**t['job'],**c['models'][t['phase']]}


def collect(c,home,domain):
    state=read(home/'state.json')
    choices=[t for t in state['topics'].values() if t['domain']==domain and t['job']]
    if len(choices)!=1:raise ValueError('Exactly one dispatched job is required')
    t=choices[0];job=t['job'];result=read(Path(job['work'])/'result.json')
    try:
        accept_result(state,t,job,result,home)
    except (ValueError,OSError) as e:
        save(Path(job['work'])/'retry-note.json',{'mechanical_error':str(e),
              'instruction':'Repair your own output; do not invent scientific agreement.'})
        raise
    save(home/'state.json',state)
    return {'status':'collected','topic':t['topic'],'role':job['role'],'rounds':t['round'],
            'next_role':t['phase'],'topic_status':t['status']}


def publish_pending(c,home):
    state=read(home/'state.json');out=[]
    for rec in state['publication_queue']:
        key=rec['verification_release']
        if key not in state['published']:
            try:
                state['published'][key]=publish_record(rec,c,home)
                rec.pop('publication_error',None)
            except (ValueError,OSError,subprocess.SubprocessError) as exc:
                rec['publication_error']=str(exc)
                save(home/'state.json',state)
                continue
            save(home/'state.json',state)
        out.append(state['published'][key])
    if c['publication'].get('auto_merge'):
        for url in out:
            if url not in state.setdefault('merged',[]):
                try:
                    if merge_checked(url):state['merged'].append(url)
                    state.setdefault('merge_errors',{}).pop(url,None)
                except (ValueError,OSError,subprocess.SubprocessError) as exc:
                    state.setdefault('merge_errors',{})[url]=str(exc)
    save(home/'state.json',state);return out


def tick(c,home,executor=execute,publisher=publish_record):
    state=read(home/'state.json')
    # Publish independently of scientific advancement; a GitHub outage cannot lose a round.
    for rec in state['publication_queue']:
        key=rec['verification_release']
        if key in state['published'] or not c['publication']['enabled']:continue
        if rec.get('publication_retry_at',0)>time.time():continue
        try:
            url=publisher(rec,c,home);state['published'][key]=url
        except (ValueError,OSError,subprocess.SubprocessError) as e:
            rec['publication_error']=str(e);rec['publication_retry_at']=time.time()+c['failure_backoff_seconds']
        save(home/'state.json',state)
    if c['publication'].get('auto_merge'):
        merged=state.setdefault('merged',[])
        for url in state['published'].values():
            if url in merged:continue
            try:
                if merge_checked(url):merged.append(url)
            except (ValueError,OSError,subprocess.SubprocessError):
                pass  # Research and publication keep running; the PR remains reviewable.
    for t in list(state['topics'].values()):successor(state,t,c,home)
    # Fair rotation avoids an early blocked topic starving the other domain.
    ready=sorted((t for t in state['topics'].values() if t['status']=='researching' and t['not_before']<=time.time()),
                 key=lambda t:t.get('last_run',0))
    if not ready:save(home/'state.json',state);return {'status':'idle','pending_publications':len(state['publication_queue'])-len(state['published'])}
    t=ready[0]
    try:
        if t['job'] is None:t['job']=job_for(state,t,c)
        save(home/'state.json',state)  # Resume this exact job after a crash.
        result=executor(c,t['job']);accept_result(state,t,t['job'],result,home)
        outcome={'status':'advanced','topic':t['topic'],'next_role':t['phase'],'topic_status':t['status']}
    except (ValueError,OSError,subprocess.SubprocessError) as e:
        t['not_before']=time.time()+c['failure_backoff_seconds'];t['last_error']=str(e)
        # A blocked/faulty final reply must not permanently pin retries to the same result file.
        if t['job']:
            t['job']['attempt']+=1
            save(Path(t['job']['work'])/'retry-note.json',{'attempt':t['job']['attempt'],
                 'mechanical_error':str(e),'instruction':'Repair your own output; do not invent evidence or a consent.'})
            result_file=Path(t['job']['work'])/'result.json'
            if result_file.exists():result_file.rename(result_file.with_name(f'result-attempt-{t["job"]["attempt"]}.json'))
        outcome={'status':'retry_scheduled','topic':t['topic'],'role':t['phase'],'reason':str(e),'retry_at':t['not_before']}
    t['last_run']=time.time();save(home/'state.json',state);return outcome


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',default=str(ROOT/'config/codex-research.json'))
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('prepare');a.add_argument('--ref',required=True)
    sub.add_parser('status');sub.add_parser('tick');sub.add_parser('watch')
    sub.add_parser('preflight')
    for name in ('dispatch','collect'):
        q=sub.add_parser(name);q.add_argument('--domain',choices=['D04','D05'],required=True)
    sub.add_parser('publish-pending')
    args=p.parse_args();c,home=config(args.config)
    if args.command=='preflight':
        print(subprocess.check_output([c['cli'],'--version'],text=True).strip())
        subprocess.run([c['cli'],'login','status'],check=True)
        print('CLI/auth checked. Model availability, research quality and unattended wake-up are not yet tested.');return
    if args.command=='prepare':out=prepare(c,home,args.ref)
    elif args.command=='status':out=read(home/'state.json')
    else:
        home.mkdir(parents=True,exist_ok=True)
        with open(home/'coordinator.lock','w') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            if args.command=='tick':out=tick(c,home)
            elif args.command=='dispatch':out=dispatch(c,home,args.domain)
            elif args.command=='collect':out=collect(c,home,args.domain)
            elif args.command=='publish-pending':out=publish_pending(c,home)
            else:
                while True:
                    print(json.dumps(tick(c,home)),flush=True)
                    time.sleep(c['poll_seconds'])
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
