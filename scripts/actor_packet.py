#!/usr/bin/env python3
"""Export one actor's frozen onboarding inputs without any conversation history."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

COMMON = {'AGENTS.md', 'harness/ONBOARDING.md', 'config/research-brief.json',
          'docs/CHARTER.md', 'docs/WORKFLOW.md', 'docs/EVIDENCE.md', 'docs/ISOLATION.md',
          'docs/EXPERIMENTS.md', 'docs/FORMATS.md', 'docs/GITHUB.md', 'templates/run.json',
          'docs/PHYSICAL-PILOT.md', 'config/physical-resources.lock.json'}

def make_packet(root, actor_id, ref, out, outbox):
    root, out = root.resolve(), out.resolve()
    if not re.fullmatch(r'[a-f0-9]{40}', ref):
        raise ValueError('A full commit SHA is required')
    if out.exists() or out == root or root in out.parents:
        raise ValueError('Use a new packet directory outside the checkout')
    def git(*args):
        return subprocess.check_output(['git','-C',str(root),*args])
    roster=json.loads(git('show',f'{ref}:config/agents.json'))
    matches=[a for a in roster['actors'] if a['actor_id']==actor_id]
    if len(matches)!=1:
        raise ValueError('Actor must exist exactly once in frozen roster')
    actor=matches[0]
    if actor['role'] not in {'proposer','challenger','verifier'}:
        raise ValueError('Invalid role')
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
    blobs={}
    for name in sorted(paths):
        if name not in tree:
            raise ValueError(f'Missing required packet source: {name}')
        mode,kind,oid=tree[name]
        if mode not in {'100644','100755'} or kind!='blob':
            raise ValueError(f'Unsafe packet source: {name}')
        blobs[name]=git('cat-file','blob',oid)
    assignment={k:actor[k] for k in ['actor_id','platform','role','domain_ids','model_requested','reasoning_requested']}
    assignment.update({'phase':'onboarding','input_commit':ref,'outbox':str(outbox.resolve()),
                       'communication':'Files only; no shared memory or other task inspection',
                       'isolation':'Fresh task and allowlisted inputs; no OS sandbox claim',
                       'output_files':['readiness.json','first-pass-plan.md']})
    blobs['ASSIGNMENT.json']=(json.dumps(assignment,indent=2)+'\n').encode()
    manifest={'actor_id':actor_id,'role':actor['role'],'commit':ref,'phase':'onboarding','files':{}}
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
    args=p.parse_args()
    print(json.dumps(make_packet(Path(__file__).resolve().parents[1],args.actor_id,args.ref,args.out,args.outbox),indent=2))
