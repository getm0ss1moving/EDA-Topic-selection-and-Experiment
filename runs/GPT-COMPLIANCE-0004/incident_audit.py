#!/usr/bin/env python3
"""Preserve and independently review a quarantined triple, outside valid cycles."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import uuid

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
spec = importlib.util.spec_from_file_location('loop', ROOT / 'scripts/codex_loop.py')
loop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--collect', action='store_true')
    args = parser.parse_args()
    config, home = loop.config(ROOT / 'config/codex-compliance-research-0004.json')
    state = loop.read(home / 'state.json')
    incident = state['incidents'][0]
    record_path = RUN / 'incident-review.json'
    if args.collect:
        record = loop.read(record_path)
        work = Path(record['work'])
        job = loop.read(work / 'JOB.json')
        result = loop.read(work / 'result.json')
        assert result['status'] == 'complete'
        release = work / 'submissions' / result['release_id']
        manifest, payload = loop.rs.verify(release)
        for key in ('role', 'actor_id', 'session_id', 'topic', 'input_commit', 'packet_sha256'):
            assert manifest[key] == job[key]
        loop.compliance.validate_ledger(json.loads(payload['compliance.json']), manifest, job,
                                       [Path(p).name for p in job['released_inputs']])
        disposition = loop.compliance.validate_review(json.loads(payload['verification.json']),
            json.loads(payload['workflow.json']), job['reviewed_releases'])
        record.update(status='independently_reviewed_quarantined_attempt',
                      audit_release=release.name, disposition=disposition)
        # Publish exact frozen bytes and public descriptors only, never scratch.
        for role, path in {**record['releases'], 'protocol_audit': str(release)}.items():
            path = Path(path)
            m, files = loop.rs.verify(path)
            target = ROOT / 'runs' / path.name
            target.mkdir(exist_ok=True)
            for name, data in {**files, 'SUBMISSION.json': loop.rs.regular(path / 'SUBMISSION.json')}.items():
                if (target / name).exists():
                    assert (target / name).read_bytes() == data
                else:
                    (target / name).write_bytes(data)
            dest = RUN / 'incident-descriptors' / role
            dest.mkdir(parents=True, exist_ok=True)
            for name in ('JOB.json', 'prompt.txt'):
                shutil.copyfile(path.parent.parent / name, dest / name)
            shutil.copyfile(path.parent.parent / 'policy/PACKET.json', dest / 'PACKET.json')
        loop.save(record_path, record)
        print(json.dumps(record, indent=2))
        return
    if record_path.exists():
        print(json.dumps(loop.read(record_path), indent=2))
        return
    original_work = Path(incident['job']['work'])
    bad_result = loop.read(original_work / 'result.json')
    releases = {**incident['releases'],
                'verifier': str(original_work / 'submissions' / bad_result['release_id'])}
    base = home / 'incident-audits' / incident['id']
    work = base / 'jobs' / str(uuid.uuid4())
    work.mkdir(parents=True)
    policy = work / 'policy'
    policy.mkdir()
    original_packet = Path(incident['old_seats']['verifier']['packet'])
    files = {}
    for name in loop.read(original_packet / 'PACKET.json')['files']:
        if Path(name).parts[0] in ('released-handover', 'released-seed'):
            continue
        dest = policy / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(loop.rs.regular(original_packet / name))
        files[name] = loop.sha(dest)
    actor = 'ChatGPT-B04-PROTOCOL-D04-QUARANTINED-R2'
    session = str(uuid.uuid4())
    loop.save(policy / 'PACKET.json', {'source_commit': state['source_commit'],
        'actor_id': actor, 'role': 'verifier', 'topic': incident['topic'],
        'purpose': 'protocol_audit', 'files': files})
    loop.freeze_tree(policy)
    shared = work / 'shared'
    shared.mkdir()
    for role, path in releases.items():
        path = Path(path)
        loop.copy_release(path, shared / path.name)
        descriptor = shared / 'job-descriptors' / role
        descriptor.mkdir(parents=True)
        for name in ('JOB.json', 'prompt.txt'):
            shutil.copyfile(path.parent.parent / name, descriptor / name)
    note = {'incident_id': incident['id'], 'reason': incident['reason'],
            'failed_job': incident['job'],
            'scope': 'Quarantine trigger is retained. Independently distinguish declared path spelling, actual authorization, and evidence of a forbidden read. No coordinator clearance, valid-cycle credit or scientific vote.'}
    loop.save(shared / 'incident.json', note)
    for name in ('release', 'submissions'):
        (work / name).mkdir()
    job = {'role': 'verifier', 'purpose': 'protocol_audit', 'topic': incident['topic'],
           'domain': incident['domain'], 'job_id': work.name, 'actor_id': actor,
           'session_id': session, 'input_commit': state['source_commit'],
           'packet_sha256': loop.sha(policy / 'PACKET.json'), 'models': config['models'],
           'compliance_required': True, 'batch_round': 2,
           'reviewed_releases': {r: Path(p).name for r, p in releases.items()},
           'released_inputs': [str(shared / Path(p).name) for p in releases.values()]}
    loop.save(work / 'JOB.json', job)
    prompt = ('Independently audit this quarantined D04 cycle-2 triple against all nine protocol rules. '
              'Start with JOB.json, this prompt, common policy, ROLE-COMPLIANCE and ONLY VERIFIER harness. '
              'Use only exact supplied frozen outputs, public job descriptors and shared/incident.json. '
              'No checkout, foreign scratch, transcripts, sessions, memory, role messages or subagents. '
              'Compare original JOB authorized input paths and ledger read_releases spelling precisely; '
              'classify mechanical formatting, supported deviations, actual forbidden exposure and unknowns separately. '
              'Do not clear the quarantine, edit the old ledger, supply a scientific vote or count this as a valid research round. '
              'Use the standard protocol_audit schema and exact enums for all three roles/nine rules; '
              'read_releases in YOUR ledger uses exact SUB IDs, not paths. English artifacts. '
              'Academic chip CAD records only; no cyber operation or resource allocation. Self-freeze and verify, then result.json.\n'
              'python3 policy/scripts/role_submission.py freeze --source release --queue submissions '
              f'--role verifier --actor {actor} --session {session} --topic {incident["topic"]} '
              f'--ref {state["source_commit"]} --packet {job["packet_sha256"]}\n')
    (work / 'prompt.txt').write_text(prompt)
    loop.save(work / 'result.schema.json', loop.FINAL)
    record = {'status': 'prepared', 'work': str(work), 'incident_id': incident['id'],
              'releases': releases, 'requested_model': config['models']['verifier'],
              'excluded_from_valid_cycles': True}
    loop.save(record_path, record)
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
