#!/usr/bin/env python3
"""Standard-library dossier tooling. Structural checks are not scientific review."""
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r'EDA-\d{4,}')
REQUIRED = ['dossier.json', 'proposal.md', 'sources.json', 'search-log.md', 'prior-art.csv',
            'contest-audit.md', 'industry-gap.md', 'experiment-plan.md', 'forecast.json',
            'tasklist.md', 'challenges.md', 'responses.md', 'direction-control.json',
            'experiment-consensus.json',
            'verification.md', 'verification.json']
STATES = {'draft', 'submitted', 'revision_requested', 'verified', 'accepted', 'parked',
          'rejected', 'abandoned'}
GATES = {'novelty', 'mechanism', 'utility', 'contest_originality', 'headroom',
         'feasibility', 'direction_integrity', 'experiment_consensus'}
DIRECTION_STATES = {'continue', 'revise_same_problem', 'abandonment_proposed', 'jointly_abandoned'}
ABANDONMENT_GROUNDS = {'novelty_exhausted', 'theoretical_headroom_exhausted',
                       'dead_end', 'immutable_direction_blocked'}

def read_json(path):
    return json.loads(path.read_text())

def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def digest(path):
    h = hashlib.sha256()
    for p in sorted(path.rglob('*')):
        if p.is_symlink():
            raise ValueError(f'Symlink prohibited: {p}')
        if p.is_file() and p.name not in {'verification.json', 'verification.md'}:
            # Length framing avoids ambiguous concatenation.
            name = p.relative_to(path).as_posix().encode()
            body = p.read_bytes()
            h.update(len(name).to_bytes(8, 'big') + name + len(body).to_bytes(8, 'big') + body)
    return h.hexdigest()

def validate_topic(path, area, sessions):
    errors = []
    def require(ok, message):
        if not ok:
            errors.append(f'{path.name}: {message}')
    for name in REQUIRED:
        require((path / name).is_file() and not (path / name).is_symlink(), f'missing or unsafe {name}')
    if errors:
        return errors
    try:
        digest(path)  # Reject nested symlinks even in drafts.
        d = read_json(path / 'dossier.json')
        sources = read_json(path / 'sources.json')
        forecast = read_json(path / 'forecast.json')
        direction = read_json(path / 'direction-control.json')
        experiment_consensus = read_json(path / 'experiment-consensus.json')
        v = read_json(path / 'verification.json')
        require(d['id'] == path.name and bool(ID.fullmatch(path.name)), 'invalid ID')
        require(d['status'] in STATES, 'invalid state')
        require(forecast.get('kind') == 'forecast_not_measurement', 'forecast label missing')
        require(direction.get('state') in DIRECTION_STATES, 'invalid direction-control state')
        anchor = direction.get('anchor', {})
        for field in ['problem', 'engineering_user', 'downstream_need', 'causal_mechanism',
                      'mechanism_invariants', 'forbidden_pivots']:
            require(bool(anchor.get(field)), f'direction anchor missing {field}')
        penalties = direction.get('penalties', {})
        penalty_scores = []
        for key in ['combination_drift', 'demand_drift']:
            item = penalties.get(key, {})
            score = item.get('score')
            require(type(score) is int and 0 <= score <= 3, f'invalid {key} penalty')
            if type(score) is int:
                penalty_scores.append(score)
            require('rationale' in item and 'evidence_refs' in item,
                    f'incomplete {key} penalty record')
        total = penalties.get('total')
        require(type(total) is int and total == sum(penalty_scores),
                'direction penalty total mismatch')
        if any(score >= 2 for score in penalty_scores) or sum(penalty_scores) >= 3:
            require(direction.get('state') in {'abandonment_proposed', 'jointly_abandoned'},
                    'severe direction drift requires abandonment review')
        require(experiment_consensus.get('status') in {'pending', 'revision_requested', 'agreed'},
                'invalid experiment consensus status')
        require(isinstance(sources, list), 'sources must be an array')
        if not isinstance(sources, list):
            return errors
        ids = set()
        for s in sources:
            fields = ['id', 'title', 'url', 'type', 'published', 'retrieved', 'locator', 'access', 'claims', 'limitations']
            require(isinstance(s, dict), 'invalid source record')
            if not isinstance(s, dict):
                continue
            require(all(k in s for k in fields), 'incomplete source record')
            require(bool(s.get('id')) and s.get('id') not in ids, 'missing or duplicate source ID')
            ids.add(s.get('id'))
            require(str(s.get('url', '')).startswith(('https://', 'http://')), 'source needs URL')
            require(s.get('access') in {'full', 'abstract', 'metadata'}, 'invalid access level')
        if d['status'] != 'draft':
            require(bool(sources), 'submitted work requires sources')
            require(d.get('proposer_session') in sessions and sessions[d['proposer_session']].get('role') == 'proposer', 'proposer not registered')
            for name in ['proposal.md', 'search-log.md', 'contest-audit.md', 'industry-gap.md', 'experiment-plan.md']:
                require(not re.search(r'\bTBD\b', (path/name).read_text()), f'unresolved template placeholder: {name}')
            require(not re.search(r'\bTBD\b', (path/'direction-control.json').read_text()),
                    'unresolved template placeholder: direction-control.json')
            with (path/'prior-art.csv').open() as stream:
                rows = list(csv.DictReader(stream))
            require(bool(rows), 'prior-art matrix empty')
            require(all(row.get('source_id') in ids for row in rows), 'prior-art source unresolved')
        if area == 'topics' or d['status'] in {'accepted', 'verified'}:
            require(area == 'topics' if d['status'] == 'accepted' else area != 'topics', 'state/storage mismatch')
            require(d['status'] in {'accepted', 'verified'}, 'topics require accepted state')
            for name in ['challenges.md', 'responses.md', 'verification.md']:
                require(not re.search(r'\bTBD\b', (path/name).read_text()),
                        f'unresolved review placeholder: {name}')
            people = [d.get(k+'_session') for k in ['proposer', 'challenger', 'verifier']]
            require(all(people) and len(set(people)) == 3, 'three distinct sessions required')
            for role, sid in zip(['proposer', 'challenger', 'verifier'], people):
                require(sid in sessions and sessions[sid].get('role') == role, f'{role} session not registered')
            require(v.get('decision') == 'accept_for_pilot', 'no independent acceptance decision')
            require(v.get('verifier_session') == d.get('verifier_session'), 'verifier identity mismatch')
            require(v.get('dossier_digest') == digest(path), 'stale dossier digest')
            require(all(v.get('gates', {}).get(k) is True for k in GATES), 'admission gate incomplete')
            require(v.get('direction_penalty_checked') is True,
                    'verifier did not check direction penalties')
            require(v.get('experiment_consensus_checked') is True,
                    'verifier did not check experiment consensus')
            require(direction.get('state') in {'continue', 'revise_same_problem'},
                    'abandonment state cannot be promoted')
            require(sum(penalty_scores) == 0, 'direction drift penalty blocks promotion')
            require(experiment_consensus.get('status') == 'agreed',
                    'experiment task list lacks proposer/challenger consensus')
            tasklist_hash = file_sha256(path / 'tasklist.md')
            require(experiment_consensus.get('tasklist_sha256') == tasklist_hash,
                    'experiment consensus binds a stale task list')
            readiness = experiment_consensus.get('readiness_checks', {})
            required_readiness = {'dependencies', 'resources', 'baselines', 'metrics',
                                  'correctness_oracle', 'stop_rules', 'owners',
                                  'reproducible_procedures'}
            require(all(readiness.get(k) is True for k in required_readiness),
                    'experiment readiness checks incomplete')
            require(experiment_consensus.get('open_conditions') == [],
                    'experiment consensus still has open conditions')
            consensus_people = []
            consensus_revisions = []
            consensus_hashes = []
            for role in ['proposer', 'challenger']:
                consent = experiment_consensus.get('consents', {}).get(role, {})
                sid = consent.get('session_id')
                consensus_people.append(sid)
                consensus_revisions.append(consent.get('signed_revision'))
                consensus_hashes.append(consent.get('tasklist_sha256'))
                require(consent.get('decision') == 'agree',
                        f'{role} has not agreed that the experiment task list is reasonable')
                require(bool(consent.get('rationale')),
                        f'{role} experiment consent lacks rationale')
                require(re.fullmatch(r'[0-9a-f]{40}', str(consent.get('signed_revision', ''))),
                        f'{role} experiment consent lacks a full signed revision')
                require(consent.get('tasklist_sha256') == tasklist_hash,
                        f'{role} experiment consent binds a stale task list')
                require(sid in sessions and sessions[sid].get('role') == role,
                        f'{role} experiment-consensus session not registered')
            require(len(set(consensus_people)) == 2,
                    'experiment consensus requires distinct proposer and challenger')
            require(len(set(consensus_revisions)) == 1,
                    'proposer and challenger must sign the same experiment revision')
            require(len(set(consensus_hashes)) == 1,
                    'proposer and challenger must sign the same experiment task list')
            if len(set(consensus_revisions)) == 1:
                require(revision_tasklist_digest(consensus_revisions[0], d['id']) == tasklist_hash,
                        'experiment revision does not contain the consented task list')
            checked = v.get('source_checks', [])
            require(bool(checked), 'no independently checked sources')
            require(all(s.get('source_id') in ids and s.get('locator') and s.get('verdict') == 'verified' for s in checked), 'invalid source checks')
            objections = v.get('objections', [])
            require(isinstance(objections, list), 'invalid objection ledger')
            if isinstance(objections, list):
                for obj in objections:
                    require(obj.get('verdict') in {'valid', 'partially_valid', 'unsupported', 'refuted', 'unresolved'}, 'invalid adjudication')
                    require(not (obj.get('blocking') is True and obj.get('resolution') != 'resolved'), 'unresolved blocking objection')
        if area == 'archive':
            require(d['status'] in {'parked', 'rejected', 'abandoned'},
                    'archive needs parked/rejected/abandoned state')
        if d['status'] == 'abandoned' or direction.get('state') == 'jointly_abandoned':
            require(area == 'archive' and d['status'] == 'abandoned',
                    'joint abandonment must be stored as archive/abandoned')
            require(direction.get('state') == 'jointly_abandoned',
                    'abandoned dossier requires jointly_abandoned direction state')
            abandonment = direction.get('abandonment', {})
            require(bool(abandonment.get('decision_id')), 'abandonment decision ID missing')
            grounds = abandonment.get('grounds', [])
            require(bool(grounds) and set(grounds) <= ABANDONMENT_GROUNDS,
                    'invalid abandonment grounds')
            require(bool(abandonment.get('rationale')) and bool(abandonment.get('evidence_refs')),
                    'abandonment requires rationale and evidence')
            evidence_refs = abandonment.get('evidence_refs', [])
            require(set(evidence_refs) <= ids, 'abandonment evidence references unknown sources')
            verifier_sid = d.get('verifier_session')
            require(verifier_sid in sessions and sessions[verifier_sid].get('role') == 'verifier',
                    'abandonment verifier session not registered')
            require(v.get('verifier_session') == verifier_sid,
                    'abandonment verifier identity mismatch')
            require(v.get('abandonment_process_checked') is True,
                    'verifier did not check abandonment evidence and process')
            verified_source_ids = {check.get('source_id') for check in v.get('source_checks', [])
                                   if check.get('verdict') == 'verified' and check.get('locator')}
            require(set(evidence_refs) <= verified_source_ids,
                    'abandonment evidence lacks independent source verification')
            consents = abandonment.get('consents', {})
            people = []
            signed_revisions = []
            signed_digests = []
            for role in ['proposer', 'challenger']:
                consent = consents.get(role, {})
                sid = consent.get('session_id')
                people.append(sid)
                require(consent.get('decision') == 'agree', f'{role} has not agreed to abandonment')
                require(re.fullmatch(r'[0-9a-f]{40}', str(consent.get('signed_revision', ''))),
                        f'{role} abandonment consent lacks a full signed revision')
                signed_revisions.append(consent.get('signed_revision'))
                signed_digests.append(consent.get('signed_dossier_digest'))
                require(sid in sessions and sessions[sid].get('role') == role,
                        f'{role} abandonment session not registered')
            require(len(set(people)) == 2, 'abandonment requires distinct proposer and challenger')
            require(len(set(signed_revisions)) == 1,
                    'proposer and challenger must sign the same frozen revision')
            require(len(set(signed_digests)) == 1 and
                    re.fullmatch(r'[0-9a-f]{64}', str(signed_digests[0] or '')),
                    'proposer and challenger must sign the same dossier digest')
            if len(set(signed_revisions)) == 1 and len(set(signed_digests)) == 1:
                require(revision_topic_digest(signed_revisions[0], d['id']) == signed_digests[0],
                        'abandonment revision does not contain the consented dossier')
            successor = abandonment.get('successor_topic_id')
            require(successor is None or (bool(ID.fullmatch(str(successor))) and successor != d['id']),
                    'successor must be a distinct topic ID')
            require(bool(abandonment.get('resurrection_conditions')),
                    'abandonment needs resurrection conditions')
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f'{path.name}: malformed data: {exc}')
    return errors

def validate(root=ROOT):
    errors = []
    roles = read_json(root/'config/roles.json')
    sessions = {}
    for s in roles['sessions']:
        sid = s.get('session_id')
        if not sid or sid in sessions:
            errors.append('Missing or duplicate session ID')
        if not all(s.get(k) for k in roles['required_session_fields']):
            errors.append(f'Incomplete session registration: {sid}')
        sessions[sid] = s
    seen = set()
    for area in ['candidates', 'topics', 'archive']:
        for path in sorted((root/area).iterdir()):
            if path.is_symlink():
                errors.append(f'Unsafe symlink: {path}')
            elif path.is_dir():
                if path.name in seen:
                    errors.append(f'Duplicate dossier: {path.name}')
                seen.add(path.name)
                errors.extend(validate_topic(path, area, sessions))
    return errors

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def revision_topic_blobs(ref, topic):
    """Return one frozen topic tree as relative-path -> blob bytes, or None."""
    try:
        if git('cat-file', '-t', ref).decode().strip() != 'commit':
            return None
        matches = []
        for area in ['candidates', 'topics', 'archive']:
            prefix = f'{area}/{topic}/'
            entries = git('ls-tree', '-r', '-z', ref, '--', prefix).split(b'\0')
            blobs = {}
            for entry in entries:
                if not entry:
                    continue
                meta, rawname = entry.split(b'\t', 1)
                mode, kind, oid = meta.decode().split()
                name = rawname.decode()
                if mode not in {'100644', '100755'} or kind != 'blob' or not name.startswith(prefix):
                    return None
                blobs[name[len(prefix):]] = git('cat-file', 'blob', oid)
            if blobs:
                matches.append(blobs)
        return matches[0] if len(matches) == 1 else None
    except (subprocess.CalledProcessError, UnicodeDecodeError, ValueError):
        return None

def revision_topic_digest(ref, topic):
    blobs = revision_topic_blobs(ref, topic)
    if blobs is None:
        return None
    h = hashlib.sha256()
    for name in sorted(blobs):
        if Path(name).name in {'verification.json', 'verification.md'}:
            continue
        rawname = name.encode()
        body = blobs[name]
        h.update(len(rawname).to_bytes(8, 'big') + rawname + len(body).to_bytes(8, 'big') + body)
    return h.hexdigest()

def revision_tasklist_digest(ref, topic):
    blobs = revision_topic_blobs(ref, topic)
    if blobs is None or 'tasklist.md' not in blobs:
        return None
    return hashlib.sha256(blobs['tasklist.md']).hexdigest()

def export_packet(role, topic, ref, out, stage='initial', governance=False, evidence_runs=()):
    if evidence_runs and not governance:
        raise ValueError('Explicit evidence runs require a governance packet')
    if any(not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', run) for run in evidence_runs):
        raise ValueError('Invalid evidence run ID')
    if not re.fullmatch(r'[0-9a-f]{40}', ref):
        raise ValueError('Use a full frozen commit SHA')
    if git('cat-file', '-t', ref).decode().strip() != 'commit':
        raise ValueError('Frozen reference must resolve to a commit object')
    if role not in {'proposer', 'challenger', 'verifier'}:
        raise ValueError('Invalid role')
    if not governance and (not topic or not ID.fullmatch(topic)):
        raise ValueError('Valid topic ID required')
    out = out.resolve()
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Packet must be outside the repository')
    if out.exists():
        raise ValueError('Output must not exist; packets are immutable snapshots')
    entries = git('ls-tree', '-r', '-z', ref).split(b'\0')
    selected = []
    for entry in entries:
        if not entry:
            continue
        meta, rawname = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = rawname.decode()
        common = name in {'AGENTS.md', 'scripts/project.py'} or name.startswith('templates/') or name.startswith('docs/') or name.startswith('config/') or (name.startswith('runs/') and name.endswith('/manifest.json')) or name == f'harness/{role.upper()}.md'
        relevant = any(name.startswith(f'{a}/{topic}/') for a in ['candidates','topics','archive']) if topic else False
        allowed = common or relevant
        if governance:
            allowed = common or name.startswith(('scripts/', 'tests/', '.github/', 'harness/', 'templates/')) or name in {'README.md', 'CONTRIBUTING.md', 'candidates/README.md', 'topics/README.md', 'archive/README.md'}
        if relevant and stage == 'initial':
            base = Path(name).name
            if role == 'challenger' and base in {'forecast.json','responses.md','verification.md','verification.json'}:
                allowed = False
            if role == 'proposer' and base in {'challenges.md','verification.md','verification.json'}:
                allowed = False
        if governance and any(name.startswith(f'runs/{run}/') for run in evidence_runs):
            allowed = True
        if allowed:
            if mode not in {'100644','100755'} or kind != 'blob':
                raise ValueError(f'Unsafe tracked entry: {name}')
            selected.append((name, git('cat-file', 'blob', oid)))
    if not governance and not any(f'/{topic}/' in name for name, _ in selected):
        raise ValueError('Topic not found at requested revision')
    manifest = {'role':role,'topic':topic,'commit':ref,'stage':stage,'governance':governance,'files':{}}
    out.mkdir(parents=True)
    for name, body in selected:
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        target.chmod(0o444)
        manifest['files'][name] = hashlib.sha256(body).hexdigest()
    (out/'PACKET.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (out/'PACKET.json').chmod(0o444)
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command', required=True)
    i=sub.add_parser('init');i.add_argument('id')
    sub.add_parser('validate')
    d=sub.add_parser('digest');d.add_argument('path',type=Path)
    t=sub.add_parser('tasklist-digest');t.add_argument('path',type=Path)
    e=sub.add_parser('packet');e.add_argument('role',choices=['proposer','challenger','verifier']);e.add_argument('topic',nargs='?')
    e.add_argument('--ref',required=True);e.add_argument('--out',type=Path,required=True)
    e.add_argument('--evidence-run', action='append', default=[], help='Explicit public run directory for governance evidence')
    e.add_argument('--stage',choices=['initial','full'],default='initial');e.add_argument('--governance',action='store_true')
    a=p.parse_args()
    try:
        if a.command=='init':
            if not ID.fullmatch(a.id):raise ValueError('Expected EDA-NNNN')
            if any((ROOT/area/a.id).exists() for area in ['candidates','topics','archive']):raise ValueError('Topic already exists')
            dst=ROOT/'candidates'/a.id
            shutil.copytree(ROOT/'templates/topic',dst)
            data=read_json(dst/'dossier.json');data['id']=a.id
            (dst/'dossier.json').write_text(json.dumps(data,indent=2)+'\n')
            print(dst)
        elif a.command=='validate':
            errors=validate()
            print('\n'.join(errors) if errors else 'Structural checks passed; scientific verification remains independent.')
            raise SystemExit(bool(errors))
        elif a.command=='digest':print(digest(a.path))
        elif a.command=='tasklist-digest':
            target = a.path/'tasklist.md' if a.path.is_dir() else a.path
            if target.name != 'tasklist.md' or not target.is_file():
                raise ValueError('Expected a dossier directory or tasklist.md')
            print(file_sha256(target))
        elif a.command=='packet':
            m=export_packet(a.role,a.topic,a.ref,a.out,a.stage,a.governance,a.evidence_run)
            print(f'Exported {len(m["files"])} files to {a.out}')
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        p.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
