"""Public activity-ledger validation; never inspect private role transcripts."""
import re

RULES = ('inputs', 'isolation', 'writes', 'evidence', 'claims', 'consent',
         'resources', 'direction', 'publication')
SELF_STATUSES = {'no_violation_disclosed', 'deviation_disclosed', 'unknown'}
AUDIT_STATUSES = {'no_violation_found_within_scope', 'supported_deviation', 'unresolved'}
DISPOSITIONS = {'clear_within_scope', 'nonblocking_findings', 'unresolved', 'blocking_violation'}


class ProtocolViolation(ValueError):
    """A disclosed contamination cannot be repaired by deleting its disclosure."""


def validate_ledger(value, manifest, assignment, allowed_releases):
    if not isinstance(value, dict) or value.get('schema') != 1:
        raise ValueError('compliance.json schema must be 1')
    for key in ('role', 'actor_id', 'session_id', 'input_commit', 'packet_sha256'):
        if value.get(key) != manifest[key]:
            raise ValueError('compliance.json identity mismatch: ' + key)
    if value.get('job_id') != assignment['job_id']:
        raise ValueError('compliance.json job mismatch')
    reads = value.get('read_releases')
    if not isinstance(reads, list) or not all(isinstance(x,str) for x in reads) or len(set(reads)) != len(reads):
        raise ValueError('compliance.json read_releases must be a unique list')
    if not set(reads) <= set(allowed_releases):
        raise ProtocolViolation('Unreleased input disclosed; stop and preserve evidence, do not erase disclosure')
    rules = value.get('rules')
    if not isinstance(rules, dict) or set(rules) != set(RULES):
        raise ValueError('compliance.json must cover all nine rule areas')
    for key, row in rules.items():
        if (not isinstance(row, dict) or row.get('status') not in SELF_STATUSES
                or not isinstance(row.get('evidence'), list) or not row['evidence']
                or not isinstance(row.get('limits'), str) or not row['limits'].strip()):
            raise ValueError('Invalid compliance rule row: ' + key)
    activity = value.get('activity', {})
    if activity.get('checkout_access') not in {'none', 'common_policy_only', 'other', 'unknown'}:
        raise ValueError('Declare checkout access honestly')
    if not isinstance(activity.get('foreign_private_reads'), list):
        raise ValueError('Declare foreign_private_reads')
    if activity['foreign_private_reads']:
        raise ProtocolViolation('Foreign private exposure disclosed; independent replacement required, preserve incident')
    for key in ('agent_messages_sent', 'subagents_spawned', 'new_eda_runs',
                'training_runs', 'new_paid_api_calls'):
        if type(activity.get(key)) is not int or activity[key] < 0:
            raise ValueError('Invalid activity count: ' + key)
    if any(activity[k] for k in ('agent_messages_sent', 'subagents_spawned',
                                'new_eda_runs', 'training_runs', 'new_paid_api_calls')):
        raise ProtocolViolation('Unallocated/forbidden activity disclosed; preserve incident for coordinator')
    if not isinstance(value.get('operations'), list) or not isinstance(value.get('incidents'), list):
        raise ValueError('Public operations/incidents lists required; no private reasoning')
    if not isinstance(value.get('observability'), str) or not value['observability'].strip():
        raise ValueError('Activity ledger must state its observability limits')


def validate_review(value, flow, expected):
    """Structural audit completeness, not proof that each audit finding is true."""
    if value.get('purpose') != 'protocol_audit' or flow.get('purpose') != 'protocol_audit':
        raise ValueError('Audit must not impersonate a scientific disposition')
    if value.get('reviewed_releases') != expected or flow.get('reviewed_releases') != expected:
        raise ValueError('Audit must bind all three exact current releases')
    disposition = value.get('disposition')
    if disposition not in DISPOSITIONS or flow.get('disposition') != disposition:
        raise ValueError('Invalid/inconsistent audit disposition')
    if set(value.get('roles', {})) != {'proposer', 'challenger', 'verifier'}:
        raise ValueError('Audit omitted a scientific role')
    deviations=set();unresolved=False
    for role, row in value['roles'].items():
        if row.get('release_id') != expected[role] or set(row.get('checks', {})) != set(RULES):
            raise ValueError('Audit role/check coverage incomplete: ' + role)
        for rule,check in row['checks'].items():
            if (check.get('status') not in AUDIT_STATUSES or not check.get('evidence')
                    or not isinstance(check.get('reason'), str)):
                raise ValueError('Invalid audit check row')
            if check['status']=='supported_deviation':deviations.add((role,rule))
            if check['status']=='unresolved':unresolved=True
    if not isinstance(value.get('findings'), list) or not value.get('limitations'):
        raise ValueError('Audit findings and observability limitations required')
    ids = set();supported=set();critical=False
    for finding in value['findings']:
        if not re.fullmatch(r'INC-\d+', finding.get('id', '')) or finding['id'] in ids:
            raise ValueError('Audit finding IDs must be unique')
        ids.add(finding['id'])
        if (finding.get('role') not in expected or finding.get('rule') not in RULES
                or finding.get('classification') not in
                {'supported_violation', 'potential_violation', 'research_defect', 'limitation'}
                or finding.get('severity') not in {'critical','noncritical'}
                or not finding.get('evidence') or not finding.get('action')
                or type(finding.get('needs_scientific_adjudication')) is not bool):
            raise ValueError('Incomplete audit finding')
        if finding['classification']=='supported_violation':
            supported.add((finding['role'],finding['rule']))
            critical |= finding['severity']=='critical'
    if deviations != supported:raise ValueError('Supported findings and matrix deviations disagree')
    if disposition=='clear_within_scope' and (deviations or unresolved):
        raise ValueError('Clear audit conflicts with deviation/unknown matrix')
    if unresolved and disposition not in {'unresolved','blocking_violation'}:
        raise ValueError('Unresolved matrix cannot be silently cleared as nonblocking')
    if critical != (disposition=='blocking_violation'):
        raise ValueError('Critical supported violations require blocking disposition')
    return disposition
