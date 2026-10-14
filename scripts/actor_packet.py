#!/usr/bin/env python3
"""Export one actor's frozen onboarding inputs without any conversation history."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

COMMON = {'docs/SELF-SUBMISSION.md', 'scripts/role_submission.py', 'docs/AUTO-ROUND.md', 'scripts/round_transmit.py',
          'config/round-transport.json', 'templates/topic/verification.md', 'AGENTS.md', 'harness/ONBOARDING.md', 'config/research-brief.json',
          'config/launch-release.json',
          'docs/CHARTER.md', 'docs/WORKFLOW.md', 'docs/EVIDENCE.md', 'docs/ISOLATION.md',
          'docs/EXPERIMENTS.md', 'docs/FORMATS.md', 'docs/GITHUB.md', 'templates/run.json',
          'docs/PHYSICAL-PILOT.md', 'config/physical-resources.lock.json'}
# The project's own digests and the dossier templates, so roles need no reimplementation (AUTO-ROUND).
COMMON |= {'scripts/project.py'} | {f'templates/topic/{n}' for n in (
    'challenges.md', 'contest-audit.md', 'direction-control.json', 'dossier.json', 'experiment-consensus.json',
    'experiment-plan.md', 'forecast.json', 'industry-gap.md', 'prior-art.csv', 'proposal.md', 'responses.md',
    'search-log.md', 'sources.json', 'tasklist.md', 'verification.json', 'verification.md')}
REGISTRIES = ('config/agents.json', 'config/agents-deepseek.json', 'config/agents-claude.json')

def make_packet(root, actor_id, ref, out, outbox, phase='onboarding', topic=None, stage='initial'):
    root, out, outbox = root.resolve(), out.resolve(), outbox.resolve()
    if not re.fullmatch(r'[a-f0-9]{40}', ref):
        raise ValueError('A full commit SHA is required')
    if out.exists() or out == root or root in out.parents:
        raise ValueError('Use a new packet directory outside the checkout')
    if (outbox.exists() or outbox == root or root in outbox.parents or outbox == out or
            out in outbox.parents or outbox in out.parents or outbox.name != actor_id):
        raise ValueError('Use a new actor-named private outbox outside the checkout and packet')
    def git(*args):
        return subprocess.check_output(['git','-C',str(root),*args], stderr=subprocess.DEVNULL)
    matches=[]
    registry_path=None
    for candidate in REGISTRIES:
        try:
            roster=json.loads(git('show',f'{ref}:{candidate}'))
        except subprocess.CalledProcessError:
            continue
        found=[a for a in roster.get('actors',[]) if a.get('actor_id')==actor_id]
        if found:
            matches.extend(found);registry_path=candidate
    if len(matches)!=1:
        raise ValueError('Actor must exist exactly once in frozen roster')
    actor=matches[0]
    if actor['role'] not in {'proposer','challenger','verifier'}:
        raise ValueError('Invalid role')
    if phase not in {'onboarding','research'}:
        raise ValueError('Phase must be onboarding or research')
    if phase == 'research' and not re.fullmatch(r'EDA-\d{4,}', topic or ''):
        raise ValueError('Research packets require a valid topic ID')
    if phase == 'onboarding' and topic is not None:
        raise ValueError('Onboarding packets cannot bind a topic')
    if stage not in {'initial','full'}:
        raise ValueError('Stage must be initial or full')
    paths=set(COMMON)
    paths.add('harness/'+actor['role'].upper()+'.md')
    for domain in actor['domain_ids']:
        if not re.fullmatch(r'D\d{2}',domain):
            raise ValueError('Invalid domain ID')
        paths.update({f'domains/{domain}/brief.json',f'domains/{domain}/README.md'})
    tree={}
    for entry in git('ls-tree','-rz',ref).split(b'\0'):
        if not entry:continue
        meta,name=entry.split(b'\t',1)
        tree[name.decode()]=meta.decode().split()
    if phase == 'research':
        release=json.loads(git('show',f'{ref}:config/launch-release.json'))
        if actor_id not in release.get('released_actors',[]):
            raise ValueError('Actor is not released for research role creation')
        assignment=release.get('assignments',{}).get(topic,{})
        if assignment.get(actor['role']) != actor_id or assignment.get('domain') not in actor['domain_ids']:
            raise ValueError('Topic and role are not assigned to this actor')
        prefix=f'candidates/{topic}/'
        topic_paths=[name for name in tree if name.startswith(prefix)]
        if not topic_paths:
            raise ValueError('Topic container missing at frozen revision')
        dossier_path=prefix+'dossier.json'
        try:
            dossier=json.loads(git('show',f'{ref}:{dossier_path}'))
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            raise ValueError('Frozen topic dossier is missing or invalid')
        status=dossier.get('status')
        if actor['role']=='proposer':
            if actor_id not in release.get('first_wave',[]) or status!='draft' or dossier.get('proposer_session'):
                raise ValueError('Proposer packet is outside the released first wave or draft creation stage')
        elif actor['role']=='challenger':
            if status not in {'submitted','revision_requested','verified'} or not dossier.get('proposer_session'):
                raise ValueError('Challenger packet requires a frozen submitted proposal and registered proposer')
            if stage=='full':
                challenge=git('show',f'{ref}:{prefix}challenges.md').decode(errors='replace')
                if not dossier.get('challenger_session') or '## Independent estimate before forecast exposure\n\nTBD' in challenge:
                    raise ValueError('Full challenger packet requires a frozen independent estimate and registered challenger')
        elif actor['role']=='verifier':
            challenge=git('show',f'{ref}:{prefix}challenges.md').decode(errors='replace')
            if (stage!='full' or status not in {'submitted','revision_requested','verified'} or
                    not dossier.get('proposer_session') or not dossier.get('challenger_session') or
                    '## Independent estimate before forecast exposure\n\nTBD' in challenge):
                raise ValueError('Verifier packet requires a frozen proposal, challenge, and registered role sessions')
        withheld=set()
        if stage == 'initial' and actor['role']=='proposer':
            withheld={'challenges.md','verification.md','verification.json'}
        elif stage == 'initial' and actor['role']=='challenger':
            withheld={'forecast.json','responses.md','verification.md','verification.json'}
        for name in topic_paths:
            if Path(name).name not in withheld:
                paths.add(name)
    blobs={}
    for name in sorted(paths):
        if name not in tree:
            raise ValueError(f'Missing required packet source: {name}')
        mode,kind,oid=tree[name]
        if mode not in {'100644','100755'} or kind!='blob':
            raise ValueError(f'Unsafe packet source: {name}')
        blobs[name]=git('cat-file','blob',oid)
    assignment={k:actor[k] for k in ['actor_id','platform','role','domain_ids','model_requested','reasoning_requested']}
    assignment.update({'phase':phase,'topic':topic,'stage':stage,'input_commit':ref,'outbox':str(outbox),
                       'communication':'Files only; no shared memory or other task inspection',
                       'isolation':'Fresh task and allowlisted inputs; no OS sandbox claim',
                       'output_files':(['readiness.json','first-pass-plan.md'] if phase=='onboarding' else
                                       ['role-output-manifest.json','released scientific files for the assigned role'])})
    blobs['ASSIGNMENT.json']=(json.dumps(assignment,indent=2)+'\n').encode()
    manifest={'actor_id':actor_id,'role':actor['role'],'registry':registry_path,'commit':ref,'phase':phase,
              'topic':topic,'stage':stage,'files':{}}
    out.mkdir(parents=True)
    for name,data in blobs.items():
        p=out/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(0o444)
        manifest['files'][name]=hashlib.sha256(data).hexdigest()
    data=(json.dumps(manifest,indent=2)+'\n').encode()
    (out/'PACKET.json').write_bytes(data);(out/'PACKET.json').chmod(0o444)
    return {'actor_id':actor_id,'packet_path':str(out),'outbox':str(outbox.resolve()),
            'input_commit':ref,'packet_sha256':hashlib.sha256(data).hexdigest(),'file_count':len(blobs)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('actor_id');p.add_argument('--ref',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--outbox',type=Path,required=True)
    p.add_argument('--phase',choices=['onboarding','research'],default='onboarding')
    p.add_argument('--topic');p.add_argument('--stage',choices=['initial','full'],default='initial')
    args=p.parse_args()
    print(json.dumps(make_packet(Path(__file__).resolve().parents[1],args.actor_id,args.ref,args.out,args.outbox,
                                 args.phase,args.topic,args.stage),indent=2))
