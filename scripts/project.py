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
            'tasklist.md', 'challenges.md', 'responses.md', 'verification.md', 'verification.json']
STATES = {'draft', 'submitted', 'revision_requested', 'verified', 'accepted', 'parked', 'rejected'}
GATES = {'novelty', 'mechanism', 'utility', 'contest_originality', 'headroom', 'feasibility'}

def read_json(path):
    return json.loads(path.read_text())

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
        v = read_json(path / 'verification.json')
        require(d['id'] == path.name and bool(ID.fullmatch(path.name)), 'invalid ID')
        require(d['status'] in STATES, 'invalid state')
        require(forecast.get('kind') == 'forecast_not_measurement', 'forecast label missing')
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
            with (path/'prior-art.csv').open() as stream:
                rows = list(csv.DictReader(stream))
            require(bool(rows), 'prior-art matrix empty')
            require(all(row.get('source_id') in ids for row in rows), 'prior-art source unresolved')
        if area == 'topics' or d['status'] in {'accepted', 'verified'}:
            require(area == 'topics' if d['status'] == 'accepted' else area != 'topics', 'state/storage mismatch')
            require(d['status'] in {'accepted', 'verified'}, 'topics require accepted state')
            people = [d.get(k+'_session') for k in ['proposer', 'challenger', 'verifier']]
            require(all(people) and len(set(people)) == 3, 'three distinct sessions required')
            for role, sid in zip(['proposer', 'challenger', 'verifier'], people):
                require(sid in sessions and sessions[sid].get('role') == role, f'{role} session not registered')
            require(v.get('decision') == 'accept_for_pilot', 'no independent acceptance decision')
            require(v.get('verifier_session') == d.get('verifier_session'), 'verifier identity mismatch')
            require(v.get('dossier_digest') == digest(path), 'stale dossier digest')
            require(all(v.get('gates', {}).get(k) is True for k in GATES), 'admission gate incomplete')
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
            require(d['status'] in {'parked', 'rejected'}, 'archive needs parked/rejected state')
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

def export_packet(role, topic, ref, out, stage='initial', governance=False):
    if not re.fullmatch(r'[0-9a-f]{40}', ref):
        raise ValueError('Use a full frozen commit SHA')
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
    e=sub.add_parser('packet');e.add_argument('role',choices=['proposer','challenger','verifier']);e.add_argument('topic',nargs='?')
    e.add_argument('--ref',required=True);e.add_argument('--out',type=Path,required=True)
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
        elif a.command=='packet':
            m=export_packet(a.role,a.topic,a.ref,a.out,a.stage,a.governance)
            print(f'Exported {len(m["files"])} files to {a.out}')
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        p.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
