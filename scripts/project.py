#!/usr/bin/env python3
"""Standard-library dossier tooling. Structural checks are not scientific review."""
import argparse
import csv
import hashlib
import json
import importlib.util
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
                       'dead_end', 'immutable_direction_blocked', 'no_anchor_preserving_direction'}

def read_json(path):
    return json.loads(path.read_text())

def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json_bytes(body):
    return json.loads(body.decode())

def is_scientific_verifier(session):
    """Protocol/governance review cannot authorize a scientific decision.

    Legacy scientific registrations have no purpose field. Recognize the
    existing explicit audit markers as well as the new machine-readable field.
    This checks registry attribution, not unseen backend independence.
    """
    if session.get('role') != 'verifier':
        return False
    if session.get('verification_purpose', 'scientific') != 'scientific':
        return False
    kind = str(session.get('session_kind', '')).casefold()
    actor = str(session.get('actor_id', '')).casefold()
    return not any(marker in kind for marker in ('protocol audit', 'protocol_audit', 'governance')) and '-protocol' not in actor

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
                require(sessions.get(sid, {}).get('topic', d['id']) == d['id'],
                        f'{role} session is assigned to a different topic')
            require(is_scientific_verifier(sessions.get(d.get('verifier_session'), {})),
                    'scientific verifier required; protocol/governance auditor cannot authorize acceptance')
            require(v.get('purpose', 'scientific') == 'scientific',
                    'protocol/governance verdict cannot authorize scientific acceptance')
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
                require(re.fullmatch(r'SUB-[0-9a-f]{64}|[0-9a-f]{40}', str(consent.get('signed_revision', ''))),
                        f'{role} experiment consent lacks a full signed revision')
                require(consent.get('tasklist_sha256') == tasklist_hash,
                        f'{role} experiment consent binds a stale task list')
                require(sid in sessions and sessions[sid].get('role') == role,
                        f'{role} experiment-consensus session not registered')
                require(sid == d.get(role + '_session'),
                        f'{role} consent must belong to the assigned dossier session')
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
            require(is_scientific_verifier(sessions.get(verifier_sid, {})),
                    'scientific verifier required; protocol/governance auditor cannot authorize abandonment')
            require(sessions.get(verifier_sid, {}).get('topic', d['id']) == d['id'],
                    'abandonment verifier session is assigned to a different topic')
            require(v.get('purpose', 'scientific') == 'scientific',
                    'protocol/governance verdict cannot authorize scientific abandonment')
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
                require(re.fullmatch(r'SUB-[0-9a-f]{64}|[0-9a-f]{40}', str(consent.get('signed_revision', ''))),
                        f'{role} abandonment consent lacks a full signed revision')
                signed_revisions.append(consent.get('signed_revision'))
                signed_digests.append(consent.get('signed_dossier_digest'))
                require(sid in sessions and sessions[sid].get('role') == role,
                        f'{role} abandonment session not registered')
                require(sid == d.get(role + '_session'),
                        f'{role} abandonment consent must belong to the assigned dossier session')
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
    errors.extend(validate_registry(root))
    errors.extend(validate_launch_release(root))
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

def validate_launch_release(root=ROOT):
    """Validate an explicit role-creation release without claiming sessions exist."""
    path = root/'config/launch-release.json'
    if not path.is_file():
        return []
    errors = []
    try:
        release = read_json(path)
        if release.get('schema_version') == 2:
            return validate_codex_release(root, release)
        registries = [read_json(root/name) for name in
                      ['config/agents.json','config/agents-deepseek.json','config/agents-claude.json']]
        actor_list = [a for registry in registries for a in registry.get('actors', [])]
        actors = {a.get('actor_id'): a for a in actor_list}
        if len(actors) != len(actor_list):
            errors.append('config/launch-release.json: actor IDs collide across platform registries')
        released = release.get('released_actors')
        first_wave = release.get('first_wave')
        scopes = set(release.get('scope_domains', []))
        if release.get('state') != 'ready_for_role_creation':
            errors.append('config/launch-release.json: release is not ready_for_role_creation')
        if scopes != {'D04', 'D05'}:
            errors.append('config/launch-release.json: only D04/D05 may be released')
        if release.get('topic_containers') != {'D04': 'EDA-0001', 'D05': 'EDA-0002'}:
            errors.append('config/launch-release.json: physical topic-container mapping is invalid')
        if not isinstance(released, list) or len(released) != 5 or len(set(released)) != 5:
            errors.append('config/launch-release.json: exactly five distinct released actors are required after the recorded role handoffs')
            released = []
        baseline = {'Codex-P04-PHYSICAL', 'Claude-P05-TIMING',
                    'DeepSeek-C04-PHYSICAL', 'DeepSeek-C05-TIMING',
                    'Claude-V02-PHYSICAL', 'Codex-V02-PHYSICAL'}
        required_handoffs = {
            'EDA-0001': {
                'challenger': ('DeepSeek-C04-PHYSICAL', 'Codex-C04-PHYSICAL-R2'),
                'verifier': ('Claude-V02-PHYSICAL', 'DeepSeek-V02-PHYSICAL')},
            'EDA-0002': {
                'challenger': ('DeepSeek-C05-TIMING', 'Codex-C05-TIMING-R2'),
                'verifier': ('Codex-V02-PHYSICAL', 'DeepSeek-V02-PHYSICAL')}}
        expected = set(baseline)
        expected_assignments = {
            'EDA-0001': {'domain': 'D04', 'proposer': 'Codex-P04-PHYSICAL',
                         'challenger': 'DeepSeek-C04-PHYSICAL', 'verifier': 'Claude-V02-PHYSICAL'},
            'EDA-0002': {'domain': 'D05', 'proposer': 'Claude-P05-TIMING',
                         'challenger': 'DeepSeek-C05-TIMING', 'verifier': 'Codex-V02-PHYSICAL'}}
        handoffs = release.get('role_handoffs', {})
        if not isinstance(handoffs, dict) or set(handoffs) != set(required_handoffs):
            errors.append('config/launch-release.json: invalid role handoff record')
        else:
            for topic, roles in required_handoffs.items():
                got = handoffs.get(topic) or {}
                if not isinstance(got, dict) or set(got) != set(roles):
                    errors.append(f'config/launch-release.json: invalid role handoff record for {topic}')
                    continue
                for role, (source, successor) in roles.items():
                    rec = got.get(role) or {}
                    if (rec.get('from') != source or rec.get('to') != successor
                            or rec.get('owner_authorized') is not True or not rec.get('reason')):
                        errors.append(f'config/launch-release.json: invalid {role} handoff record for {topic}')
                        continue
                    expected.discard(source)
                    expected.add(successor)
                    expected_assignments[topic][role] = successor
        if set(released) != expected:
            errors.append('config/launch-release.json: released actor set does not match the cross-platform physical slice')
        for actor_id in released:
            actor = actors.get(actor_id)
            if not actor:
                errors.append(f'config/launch-release.json: unknown released actor {actor_id}')
                continue
            if actor.get('status') != 'ready_for_fresh_session' or actor.get('active_scope') is not True:
                errors.append(f'config/launch-release.json: {actor_id} is not ready for fresh session creation')
            if actor.get('fresh_session_required') is not True:
                errors.append(f'config/launch-release.json: {actor_id} may accidentally reuse a historical session')
            if not set(actor.get('domain_ids', [])).issubset(scopes):
                errors.append(f'config/launch-release.json: {actor_id} exceeds released domains')
            if not actor.get('model_requested') or not actor.get('reasoning_requested'):
                errors.append(f'config/launch-release.json: {actor_id} lacks an explicit model/effort policy')
        if release.get('assignments') != expected_assignments:
            errors.append('config/launch-release.json: cross-platform assignment matrix is invalid')
        else:
            for topic, assignment in expected_assignments.items():
                for role in ['proposer', 'challenger', 'verifier']:
                    actor = actors.get(assignment[role], {})
                    if actor.get('role') != role or assignment['domain'] not in actor.get('domain_ids', []):
                        errors.append(f'config/launch-release.json: {topic} {role} registry binding is invalid')
        if not isinstance(first_wave, list) or set(first_wave) != {'Codex-P04-PHYSICAL','Claude-P05-TIMING'}:
            errors.append('config/launch-release.json: invalid first wave')
        elif any(actors.get(a, {}).get('role') != 'proposer' for a in first_wave):
            errors.append('config/launch-release.json: first wave must contain proposers only')
        cap = release.get('max_concurrent_scientific_sessions')
        if type(cap) is not int or not 1 <= cap <= 2:
            errors.append('config/launch-release.json: concurrency cap must be one or two')
        if release.get('fresh_sessions_required') is not True or release.get('old_sessions_are_inputs') is not False:
            errors.append('config/launch-release.json: historical sessions must remain isolated')
        if release.get('experiment_authorization') is not False:
            errors.append('config/launch-release.json: role creation must not authorize experiments')
        readiness = release.get('platform_readiness', {})
        for platform in ['codex','deepseek']:
            item = readiness.get(platform, {})
            if (item.get('state') != 'ready_after_merge_and_packet_export' or item.get('models_verified') is not True
                    or (platform == 'deepseek' and not item.get('model_policy'))):
                errors.append(f'config/launch-release.json: {platform} readiness is incomplete')
        claude = readiness.get('claude', {})
        if (claude.get('state') != 'ready_for_host_bound_creation' or
                claude.get('models_verified') is not False or not claude.get('model_policy')):
            errors.append('config/launch-release.json: Claude host-bound readiness policy is incomplete')
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f'config/launch-release.json: malformed data: {exc}')
    return errors

def validate_codex_release(root, release):
    """Validate active bindings rather than hardcoding historical platform handoffs."""
    errors = []
    def check(ok, why):
        if not ok:
            errors.append('config/launch-release.json: ' + why)
    actors = {a['actor_id']: a for a in read_json(root/'config/agents.json')['actors']}
    check(release.get('active_platforms') == ['codex'], 'only Codex may run new work')
    check(release.get('state') == 'ready_for_role_creation', 'release is not ready')
    check(release.get('fresh_sessions_required') is True and release.get('old_sessions_are_inputs') is False,
          'historical sessions must remain isolated')
    assigned = []
    for topic, entry in release.get('assignments', {}).items():
        check(bool(ID.fullmatch(topic)), 'invalid topic ID')
        domain = entry.get('domain')
        for role in ('proposer', 'challenger', 'verifier'):
            aid = entry.get(role)
            assigned.append(aid)
            a = actors.get(aid, {})
            check(a.get('role') == role and domain in a.get('domain_ids', []), f'{topic} {role} binding invalid')
            check(a.get('platform') == 'OpenAI Codex' and a.get('active_scope') is True,
                  f'{aid} is not an active Codex actor')
            check(bool(a.get('model_requested')) and bool(a.get('reasoning_requested')), f'{aid} lacks model policy')
        brief = root/'domains'/str(domain)/'brief.json'
        if brief.is_file():
            b = read_json(brief)
            check(all(b.get(r) == entry.get(r) for r in ('proposer', 'challenger', 'verifier')),
                  f'{domain} brief disagrees with assignments')
    check(bool(assigned) and len(set(assigned)) == len(assigned), 'distinct scientific seats required')
    check(set(release.get('released_actors', [])) == set(assigned), 'released actor set differs from assignments')
    check(release.get('experiment_authorization') is False, 'creation cannot authorize experiments')
    return errors

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def revision_topic_blobs(ref, topic):
    """Return one frozen topic tree as relative-path -> blob bytes, or None."""
    try:
        if re.fullmatch(r'SUB-[0-9a-f]{64}', str(ref)):
            # Consents bind an earlier immutable proposal, avoiding self-reference.
            tool = Path(__file__).with_name('role_submission.py')
            spec = importlib.util.spec_from_file_location('consent_submission', tool)
            rs = importlib.util.module_from_spec(spec); spec.loader.exec_module(rs)
            manifest, payload = rs.verify(ROOT/'runs'/ref)
            if manifest['topic'] != topic or manifest['role'] != 'proposer':
                return None
            return {k:v for k,v in payload.items() if k not in {
                'workflow.json', 'experiment-consent.json', 'abandonment-consent.json'}}
        object_type = subprocess.check_output(
            ['git', '-C', str(ROOT), 'cat-file', '-t', ref], stderr=subprocess.DEVNULL)
        if object_type.decode().strip() != 'commit':
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
    except (subprocess.CalledProcessError, UnicodeDecodeError, ValueError, OSError):
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
        common = name in {'AGENTS.md', 'scripts/project.py', 'scripts/role_submission.py'} or name.startswith('templates/') or name.startswith('docs/') or name.startswith('config/') or (name.startswith('runs/') and name.endswith('/manifest.json')) or name == f'harness/{role.upper()}.md'
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

def export_domain_packet(role, domain, actor, ref, out):
    """Export a frozen onboarding packet for one platform actor on one domain.

    The actor record is read from the frozen commit, never from the working tree,
    so a packet cannot silently describe an assignment that was never committed.
    """
    if not re.fullmatch(r'[0-9a-f]{40}', ref):
        raise ValueError('Use a full frozen commit SHA')
    if role not in {'proposer', 'challenger', 'verifier'}:
        raise ValueError('Invalid role')
    if not domain or not re.fullmatch(r'D\d{2}', domain):
        raise ValueError('Valid domain ID required (DNN)')
    if not actor:
        raise ValueError('--actor is required with --domain')
    out = out.resolve()
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Packet must be outside the repository')
    if out.exists():
        raise ValueError('Output must not exist; packets are immutable snapshots')
    match = [a for a in read_json_bytes(git('cat-file', 'blob', f'{ref}:config/agents-deepseek.json'))['actors']
             if a.get('actor_id') == actor]
    if len(match) != 1:
        raise ValueError(f'Actor not in frozen registry: {actor}')
    record = match[0]
    if record.get('role') != role:
        raise ValueError(f'Actor {actor} has role {record.get("role")}, not {role}')
    if domain not in record.get('domain_ids', []):
        raise ValueError(f'Actor {actor} is not assigned to {domain}')
    owned = {f'domains/README.md', f'domains/{domain}/brief.json', f'domains/{domain}/README.md',
             f'harness/{role.upper()}.md', 'harness/ONBOARDING.md'}
    entries = git('ls-tree', '-r', '-z', ref).split(b'\0')
    selected = []
    for entry in entries:
        if not entry:
            continue
        meta, rawname = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = rawname.decode()
        allowed = (name in {'AGENTS.md', 'README.md', 'scripts/project.py', 'scripts/role_submission.py'} or name.startswith('templates/')
                   or name.startswith('docs/') or name.startswith('config/')
                   or (name.startswith('runs/') and name.endswith('/manifest.json')) or name in owned)
        if allowed:
            if mode not in {'100644', '100755'} or kind != 'blob':
                raise ValueError(f'Unsafe tracked entry: {name}')
            selected.append((name, git('cat-file', 'blob', oid)))
    if not any(name == f'domains/{domain}/brief.json' for name, _ in selected):
        raise ValueError(f'Domain brief not found at requested revision: {domain}')
    if any(name.endswith('.md') and name.startswith('harness/') and name not in owned for name, _ in selected):
        raise ValueError('Role packet must not contain another role harness')
    manifest = {'role': role, 'topic': None, 'domain': domain, 'actor_id': actor,
                'call_sign': record.get('call_sign'), 'commit': ref, 'stage': 'onboarding',
                'governance': False, 'files': {}, 'generated': {}}
    out.mkdir(parents=True)
    for name, body in selected:
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        target.chmod(0o444)
        manifest['files'][name] = hashlib.sha256(body).hexdigest()
    assignment = {'actor_id': actor, 'call_sign': record.get('call_sign'), 'platform': record.get('platform'),
                  'role': role, 'domain_id': domain, 'domain_ids': record.get('domain_ids'),
                  'model_requested': record.get('model_requested'),
                  'reasoning_requested': record.get('reasoning_requested'),
                  'input_commit': ref, 'stage': 'onboarding',
                  'required_outputs': ['readiness.json', 'first-pass-plan.md'],
                  'output_location': 'the coordinator-designated outbox outside this packet; never write into the packet',
                  'forbidden': ['other role harnesses', 'other domains', 'another session or memory',
                                'agent messaging', 'editing the shared checkout', 'self-approval']}
    assignment_body = (json.dumps(assignment, indent=2)+'\n').encode()
    (out/'ASSIGNMENT.json').write_bytes(assignment_body)
    (out/'ASSIGNMENT.json').chmod(0o444)
    manifest['generated']['ASSIGNMENT.json'] = hashlib.sha256(assignment_body).hexdigest()
    (out/'PACKET.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (out/'PACKET.json').chmod(0o444)
    return manifest

def validate_registry(root=ROOT):
    """Cross-check the platform registry against the domain briefs. Structure only."""
    errors = []
    path = root/'config/agents-deepseek.json'
    if not path.is_file():
        return errors
    try:
        actors = read_json(path)['actors']
    except (ValueError, KeyError, TypeError) as exc:
        return [f'config/agents-deepseek.json: malformed data: {exc}']
    if not isinstance(actors, list):
        return ['config/agents-deepseek.json: actors must be a list']
    ids = [a.get('actor_id') for a in actors]
    if len(ids) != len(set(ids)):
        errors.append('config/agents-deepseek.json: duplicate actor_id')
    by = {a.get('actor_id'): a for a in actors}
    for a in actors:
        for key in ['actor_id', 'call_sign', 'platform', 'role', 'domain_ids', 'model_requested', 'reasoning_requested']:
            if not a.get(key):
                errors.append(f'agent {a.get("actor_id")}: missing {key}')
        if a.get('role') not in {'proposer', 'challenger', 'verifier'}:
            errors.append(f'agent {a.get("actor_id")}: invalid role')
    activation = read_json(path).get('activation')
    if activation:
        activation_state = activation.get('state', 'active')
        if activation_state not in {'active', 'paused_governance', 'ready_for_role_creation'}:
            errors.append(f'config/agents-deepseek.json: unknown activation state {activation_state}')
        active = activation.get('active_actors')
        deferred = activation.get('deferred_actors')
        if not isinstance(active, list):
            errors.append('config/agents-deepseek.json: activation.active_actors must be a list')
            active = []
        elif not active and activation_state == 'active':
            errors.append('config/agents-deepseek.json: active state requires active actors')
        if activation_state != 'active' and activation.get('active_domains'):
            errors.append(f'config/agents-deepseek.json: {activation_state} cannot have active domains')
        released = activation.get('released_actors', [])
        if activation_state == 'ready_for_role_creation':
            if not isinstance(released, list) or not released:
                errors.append('config/agents-deepseek.json: role-creation release needs released actors')
            for aid in released:
                if aid not in by or by[aid].get('status') != 'ready_for_fresh_session':
                    errors.append(f'config/agents-deepseek.json: released actor {aid} is not ready')
        if len(active) != len(set(active)):
            errors.append('config/agents-deepseek.json: duplicate active actor')
        for aid in active:
            if aid not in by:
                errors.append(f'config/agents-deepseek.json: active actor {aid} absent from registry')
        if sorted(list(active) + list(deferred or [])) != sorted(ids):
            errors.append('config/agents-deepseek.json: active and deferred actors must partition the registry')
        for d in activation.get('active_domains', []):
            if not any(d in by[aid].get('domain_ids', []) for aid in active if aid in by):
                errors.append(f'config/agents-deepseek.json: active domain {d} has no active actor')
        for d, tid in activation.get('topic_containers', {}).items():
            if not ID.fullmatch(str(tid)):
                errors.append(f'config/agents-deepseek.json: activation topic container {tid} is not a valid topic ID')
    for p in sorted((root/'domains').glob('D*/brief.json')):
        try:
            d = read_json(p)
            roles = d['platform_roles']['deepseek']
        except (ValueError, KeyError, TypeError):
            errors.append(f'{p.parent.name}/brief.json: missing platform_roles.deepseek binding')
            continue
        for role in ['proposer', 'challenger', 'verifier']:
            aid = roles.get(role)
            if aid not in by:
                errors.append(f'{p.parent.name}/brief.json: {role} {aid} absent from DeepSeek registry')
                continue
            if by[aid].get('role') != role:
                errors.append(f'{p.parent.name}/brief.json: {aid} registered as {by[aid].get("role")}')
            if d.get('domain_id') not in by[aid].get('domain_ids', []):
                errors.append(f'{p.parent.name}/brief.json: {aid} not assigned to {d.get("domain_id")}')
            if roles.get(f'{role}_call_sign') != by[aid].get('call_sign'):
                errors.append(f'{p.parent.name}/brief.json: {role} call sign mismatch for {aid}')
    return errors

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
    e.add_argument('--domain',help='DNN domain onboarding packet instead of a topic dossier packet')
    e.add_argument('--actor',help='actor_id from config/agents-deepseek.json; required with --domain')
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
            if a.domain:
                if a.topic or a.governance or a.evidence_run:
                    raise ValueError('Do not combine --domain with a topic ID, --governance or --evidence-run')
                m=export_domain_packet(a.role,a.domain,a.actor,a.ref,a.out)
            else:
                m=export_packet(a.role,a.topic,a.ref,a.out,a.stage,a.governance,a.evidence_run)
            print(f'Exported {len(m["files"])} files to {a.out}')
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        p.exit(1,str(exc)+'\n')
if __name__=='__main__':main()
