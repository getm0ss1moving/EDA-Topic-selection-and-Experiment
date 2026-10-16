"""Evidence-bound portfolio retirement. Scores are not scientific truth or consent."""
import copy
import math
import re

AXES = {'novelty', 'utility', 'mechanism', 'headroom', 'contest_originality', 'experiments', 'anchor'}
GRADES = {'clear': 0, 'unresolved': 1, 'major': 2, 'fatal': 3}
FATAL_GROUNDS = {
    'novelty': 'equivalent_prior_no_residual',
    'utility': 'incompatible_engineering_objective',
    'mechanism': 'counterexample_no_anchor_repair',
    'headroom': 'proven_bound_below_locked_threshold',
    'contest_originality': 'supplied_solution_no_residual',
    'experiments': 'nondiscriminating_no_anchor_repair',
    'anchor': 'no_remaining_anchor_preserving_path'}
SUB = re.compile(r'SUB-[0-9a-f]{64}')


def require(condition, message):
    if not condition:
        raise ValueError('Retirement: ' + message)


def validate_policy(policy):
    require(isinstance(policy, dict), 'policy must be an object')
    require(policy.get('schema') == 1 and bool(policy.get('policy_id')), 'invalid policy identity')
    require(set(policy.get('weights', {})) == AXES, 'seven weighted axes required')
    require(all(type(x) is int and 1 <= x <= 3 for x in policy['weights'].values()), 'invalid weights')
    require(policy.get('grade_points') == GRADES and all(type(x) is int for x in policy['grade_points'].values()), 'grade meanings cannot be changed')
    for key, low, high in [('fatal_count', 1, 7), ('persistent_score', 1, 63),
                           ('persistent_rounds', 2, 10), ('minimum_common_axes', 2, 7)]:
        require(type(policy.get(key)) is int and low <= policy[key] <= high, 'invalid ' + key)
    return policy


def axis_rows(value):
    require(isinstance(value, list) and len(value) == len(AXES), 'one row per axis required')
    require(all(isinstance(x, dict) for x in value), 'axis row must be an object')
    require(all(isinstance(x.get('axis'), str) for x in value), 'axis must be a string')
    require({x.get('axis') for x in value} == AXES, 'missing or duplicate axis')
    result = {}
    for row in value:
        axis = row['axis']
        require(isinstance(row.get('grade'), str) and row['grade'] in GRADES, 'invalid grade')
        require(isinstance(row.get('issue_key'), str) and bool(re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,95}', row['issue_key'])), 'invalid stable issue key')
        require(isinstance(row.get('reason'), str) and bool(row['reason'].strip()), 'reason required')
        refs = row.get('references')
        require(isinstance(refs, list) and all(isinstance(x, str) and x for x in refs)
                and len(refs) == len(set(refs)), 'invalid claim/objection references')
        if row['grade'] != 'clear':
            require(bool(row.get('repair_test')), 'nonclear axis requires cheapest decisive repair/test')
        result[axis] = row
    return result


def validate_screen(screen, policy, proposer_release):
    require(isinstance(screen, dict), 'challenger elimination_screen required')
    require(screen.get('policy_id') == policy['policy_id'], 'screen policy mismatch')
    require(screen.get('reviewed_proposer_release') == proposer_release, 'stale screen')
    require(screen.get('recommendation') in {'continue', 'revise', 'retire'}, 'screen recommendation missing')
    return axis_rows(screen.get('axes'))


def validated_point(binding, screen, verdict, proposer_release, challenger_release,
                    verifier_release, proposal_digest, headroom_contract=None):
    """Check format/bindings; only the independent scientific verifier supplies entailment."""
    policy = validate_policy(binding['definition'])
    suggested = validate_screen(screen, policy, proposer_release)
    require(verdict.get('purpose', 'scientific') == 'scientific', 'protocol auditor is not a scientific verifier')
    review = verdict.get('elimination_review')
    require(isinstance(review, dict), 'scientific elimination_review required')
    require(review.get('policy_id') == policy['policy_id'] and review.get('policy_sha256') == binding['sha256'], 'review policy mismatch')
    require(review.get('reviewed_proposer_release') == proposer_release
            and review.get('reviewed_challenger_release') == challenger_release, 'stale review pair')
    rows = axis_rows(review.get('axes'))
    resurrection = review.get('resurrection_conditions')
    require(isinstance(resurrection, list) and resurrection and all(isinstance(x, str) and x.strip() for x in resurrection), 'resurrection conditions required')
    judged = {}
    for name in ('objections', 'claims'):
        claims = verdict.get(name, [])
        require(isinstance(claims, list) and all(isinstance(x, dict) for x in claims), 'invalid adjudication list')
        for claim in claims:
            ident = claim.get('id', claim.get('objection_id'))
            require(isinstance(ident, str) and ident and ident not in judged, 'duplicate/missing adjudicated claim ID')
            judged[ident] = claim
    checked = verdict.get('source_checks', [])
    require(isinstance(checked, list) and all(isinstance(x, dict) and isinstance(x.get('id'), str) and x['id'] for x in checked), 'invalid source checks')
    sources = {x['id']: x for x in checked}
    require(len(sources) == len(checked), 'duplicate checked source IDs')
    consumed = set()
    active, fatal, total = [], [], 0
    for axis, row in rows.items():
        require(row['issue_key'] == suggested[axis]['issue_key'], 'verifier changed challenger issue identity')
        require(type(row.get('no_anchor_preserving_repair')) is bool, 'explicit repairability required')
        source_ids = row.get('checked_source_ids')
        require(isinstance(source_ids, list) and all(isinstance(x, str) for x in source_ids), 'checked source IDs required')
        require(all(x in sources for x in source_ids), 'unknown checked source')
        refs = row['references']
        grade = row['grade']
        if grade == 'clear':
            require(not row['no_anchor_preserving_repair'], 'clear axis cannot be unrepairable')
            continue
        require(refs and all(x in judged for x in refs), 'nonclear axis needs adjudicated claims')
        require(not consumed.intersection(refs), 'one objection/claim cannot inflate multiple axes')
        consumed.update(refs)
        require(all(judged[x].get('blocking') is True for x in refs), 'nonblocking issue cannot drive retirement')
        allowed = {'valid', 'partially_valid', 'unresolved'} if grade == 'unresolved' else {'valid', 'partially_valid'}
        if grade == 'fatal':
            allowed = {'valid'}
            require(row['no_anchor_preserving_repair'], 'fatal grade needs no supported repair within anchor')
            require(row.get('fatal_ground') == FATAL_GROUNDS[axis], 'invalid fatal ground')
            if axis == 'headroom':
                contract = headroom_contract or {}
                effect = contract.get('minimum_meaningful_effect')
                bound = row.get('remaining_improvement_upper_bound')
                require(contract.get('primary_metric') and row.get('primary_metric') == contract['primary_metric'], 'headroom metric must match frozen brief')
                require(type(effect) in (int,float) and math.isfinite(effect) and effect > 0
                        and type(bound) in (int,float) and math.isfinite(bound) and 0 <= bound < effect,
                        'headroom needs applicable bound below locked meaningful effect')
        else:
            require(not row['no_anchor_preserving_repair'], 'only verified fatal may assert no repair')
        require(all(judged[x].get('verdict') in allowed for x in refs), 'grade contradicts scientific adjudication')
        if grade in {'major', 'fatal'}:
            require(source_ids, 'confirmed failure needs reopened primary evidence')
            require(all(sources[x].get('access_level', sources[x].get('access')) == 'full'
                        and sources[x].get('locator') and sources[x].get('url') for x in source_ids),
                    'confirmed failure needs full-access source locators')
        active.append(axis)
        if grade == 'fatal':
            fatal.append(axis)
        total += policy['weights'][axis] * GRADES[grade]
    return {'policy_id': policy['policy_id'], 'policy_sha256': binding['sha256'],
            'proposer_release': proposer_release, 'challenger_release': challenger_release,
            'verifier_release': verifier_release, 'proposal_digest': proposal_digest,
            'score': total, 'active_axes': sorted(active), 'fatal_axes': sorted(fatal),
            'axes': copy.deepcopy(review['axes']), 'resurrection_conditions': resurrection}


def evaluate(policy, history, point):
    """A fatal finding stops immediately; persistent risk stops portfolio spending, not truth."""
    validate_policy(policy)
    if len(point['fatal_axes']) >= policy['fatal_count']:
        return {'status': 'retired_by_policy', 'reason': 'verified_fatal',
                'epistemic_status': 'verified_fatal_in_declared_scope_not_universal_impossibility',
                'reviews': [copy.deepcopy(point)]}
    # Consent-only/metadata-only republishes cannot manufacture a second repair attempt.
    distinct = []
    for row in [*history, point]:
        require(row['policy_sha256'] == point['policy_sha256'], 'mixed-policy history')
        if distinct and row['proposal_digest'] == distinct[-1]['proposal_digest']:
            distinct[-1] = row
        else:
            distinct.append(row)
    window = distinct[-policy['persistent_rounds']:]
    if len(window) == policy['persistent_rounds'] and all(x['score'] >= policy['persistent_score'] for x in window):
        common = set.intersection(*(set(x['active_axes']) for x in window))
        if len(common) >= policy['minimum_common_axes']:
            return {'status': 'retired_by_policy', 'reason': 'persistent_decision_critical_risk',
                    'epistemic_status': 'portfolio_stop_not_scientific_refutation',
                    'common_axes': sorted(common), 'reviews': copy.deepcopy(window)}
    return None
