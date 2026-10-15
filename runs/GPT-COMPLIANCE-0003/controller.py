#!/usr/bin/env python3
"""Batch 0003 metadata/released-byte audit. No private notes or transcripts."""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]
RUN=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('loop',ROOT/'scripts/codex_loop.py')
loop=importlib.util.module_from_spec(spec);spec.loader.exec_module(loop)


def main():
    p=argparse.ArgumentParser();p.add_argument('--record-job');p.add_argument('--agent')
    p.add_argument('--final',action='store_true');args=p.parse_args()
    config,home=loop.config(ROOT/'config/codex-compliance-research.json')
    state=loop.read(home/'state.json');file=RUN/'dispatches.json'
    dispatches=loop.read(file) if file.exists() else []
    if args.record_job:
        if not args.agent:p.error('--agent required')
        work=Path(args.record_job);job=loop.read(work/'JOB.json')
        if not any(r['work']==str(work) for r in dispatches):
            dispatches.append({'agent':args.agent,'work':str(work),'topic':job['topic'],
                'domain':job['domain'],'cycle':job['batch_round'],'role':job['role'],
                'purpose':job.get('purpose','research'),'requested':job['models'][job['role']],
                'fork_turns':'none','logical_session':job['session_id'],
                'recorded_at_utc':datetime.now(timezone.utc).isoformat(),
                'note':'Successful app dispatch recorded, not independent backend attestation.'})
        loop.save(file,dispatches)
    counts={d:sum(t['round'] for t in state['topics'].values() if t['domain']==d) for d in ('D04','D05')}
    science=[];audits=[];packets=[];jobs={};index=[];compliance=[]
    for topic,t in state['topics'].items():
        for role,seat in t['seats'].items():
            loop.verify_packet(seat)
            dest=RUN/'inputs'/topic/role/'PACKET.json';dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(Path(seat['packet'])/'PACKET.json',dest)
            packets.append({'topic':topic,'role':role,'session_id':seat['session_id'],
                            'packet_sha256':seat['packet_sha256']})
        for name in t['history']:
            path=Path(name);m,payload=loop.rs.verify(path);jobs[str(path.parent.parent)]=None
            science.append({'topic':topic,'role':m['role'],'release_id':path.name,
                            'files':len(payload),'manifest_sha256':loop.sha(path/'SUBMISSION.json')})
        if t.get('job'):jobs[t['job']['work']]=None
    for key,a in state.get('audits',{}).items():
        loop.verify_packet(a['seat']);work=Path(a['job']['work']);jobs[str(work)]=None
        dest=RUN/'inputs'/'audits'/key/'PACKET.json';dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(Path(a['seat']['packet'])/'PACKET.json',dest)
        if a.get('release'):
            path=Path(a['release']);m,payload=loop.rs.verify(path)
            audits.append({'release_id':path.name,'session_id':m['session_id'],
                           'files':len(payload),'manifest_sha256':loop.sha(path/'SUBMISSION.json')})
    seen={'D04':0,'D05':0}
    for rec in state['publication_queue']:
        t=state['topics'][rec['topic']];entry={**t,'latest':rec['releases']}
        for role,name in rec['releases'].items():
            work=Path(name).parent.parent
            loop.validate_result(state,entry,{'role':role,'work':str(work)},loop.read(work/'result.json'))
        domain=t['domain'];seen[domain]+=1
        row={'domain':domain,'domain_cycle':seen[domain],'topic':rec['topic'],
             'topic_round':rec['round'],'decision':rec['decision'],
             'releases':{r:Path(n).name for r,n in rec['releases'].items()},
             'pr':state['published'].get(rec['verification_release']),
             'compliance_gate':rec.get('compliance_gate')}
        if rec.get('compliance_audit'):
            m,payload=loop.rs.verify(rec['compliance_audit']);v=loop.read(Path(rec['compliance_audit'])/'verification.json')
            loop.compliance.validate_review(v,loop.read(Path(rec['compliance_audit'])/'workflow.json'),row['releases'])
            row['audit_release']=Path(rec['compliance_audit']).name
            compliance.append({**row,'roles':v['roles'],'findings':v['findings'],'limitations':v['limitations']})
        index.append(row)
    descriptors=[]
    for name in jobs:
        work=Path(name);job=loop.read(work/'JOB.json');inputs=[]
        paths=[Path(p) for p in job['released_inputs'] if Path(p).is_dir()]
        paths+=list((work/'own-previous').glob('SUB-*'))
        for path in paths:
            m,_=loop.rs.verify(path)
            inputs.append({'release_id':path.name,'role':m['role'],
                           'manifest_sha256':loop.sha(path/'SUBMISSION.json')})
        purpose=job.get('purpose','research')
        dest=RUN/'inputs'/job['topic']/f'cycle-{job["batch_round"]}-{purpose}-{job["role"]}'
        dest.mkdir(parents=True,exist_ok=True)
        for filename in ('JOB.json','prompt.txt'):shutil.copyfile(work/filename,dest/filename)
        descriptors.append({'topic':job['topic'],'domain':job['domain'],'role':job['role'],
                            'purpose':purpose,'cycle':job['batch_round'],'requested':job['models'][job['role']],
                            'job_sha256':loop.sha(work/'JOB.json'),'prompt_sha256':loop.sha(work/'prompt.txt'),
                            'released_inputs':inputs})
    if args.final:
        assert counts=={'D04':4,'D05':4},counts
        assert all(not t.get('job') for t in state['topics'].values())
        assert len(index)==len(state['published'])==len(state.get('merged',[]))==8
        assert len(science)==24 and len(audits)==len(compliance)==8 and len(descriptors)==32
        assert not any(r['compliance_gate']=='blocking_violation' for r in index)
        assert {r['work'] for r in dispatches} >= set(jobs)
    loop.save(RUN/'topic-index.json',index);loop.save(RUN/'role-compliance-index.json',compliance)
    loop.save(RUN/'progress.json',{'completed_cycles':counts,'topics':{
        k:{f:v.get(f) for f in ('domain','round','status','phase','last_scientific_decision')}
        for k,v in state['topics'].items()},'published':state['published'],'merged':state.get('merged',[])})
    loop.save(RUN/'release-audit.json',{'status':'bounded_batch_complete' if args.final else 'in_progress',
        'input_commit':state['source_commit'],'completed_cycles':counts,'logical_scientific_seats':packets,
        'scientific_releases':science,'protocol_audits':audits,'jobs':descriptors,
        'published':state['published'],'merged':state.get('merged',[]),
        'scope':'Frozen byte/binding audit and independent protocol findings, not proof of unseen actions, scientific truth or OS confinement.'})
    print({'cycles':counts,'scientific_releases':len(science),'independent_protocol_audits':len(audits),
           'published':len(state['published']),'merged':len(state.get('merged',[]))})


if __name__=='__main__':main()
