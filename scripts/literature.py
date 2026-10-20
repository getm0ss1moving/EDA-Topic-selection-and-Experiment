#!/usr/bin/env python3
"""Validate bibliography provenance/counts; never certify scientific claims."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGES = {'floorplanning', 'placement', 'CTS', 'global_routing', 'detailed_routing',
          'timing_signoff', 'power_integrity', 'physical_verification'}

def identity(value):
    value = value.lower().strip()
    if value.startswith('arxiv:'):
        return re.sub(r'v\d+$', '', value)
    return value

def validate_catalog(data):
    errors, ids, identities, titles = [], set(), set(), set()
    def check(ok, why):
        if not ok: errors.append('literature: '+why)
    check(data.get('schema') == 1, 'unsupported schema')
    target = data.get('target_unique_papers')
    check(type(target) is int and target == 100, 'target must be 100 unique papers')
    papers, artifacts = data.get('papers'), data.get('artifacts')
    if not isinstance(papers, list) or not isinstance(artifacts, list):
        return errors + ['literature: papers/artifacts must be separate arrays']
    check(len(papers) <= 100, 'target exceeded; review scope before adding papers')
    for entry in papers + artifacts:
        if not isinstance(entry, dict):
            errors.append('literature: invalid entry'); continue
        eid = entry.get('id')
        check(isinstance(eid, str) and eid and eid not in ids, 'missing/duplicate ID')
        ids.add(str(eid))
        check(str(entry.get('url', '')).startswith('https://'), f'{eid}: primary URL required')
        check(bool(entry.get('retrieved')) and bool(entry.get('locator')), f'{eid}: retrieval and locator required')
        check(entry.get('access') in {'full', 'abstract', 'metadata'}, f'{eid}: access level required')
    for entry in papers:
        if not isinstance(entry, dict): continue
        eid = entry.get('id')
        check(entry.get('kind') == 'paper', f'{eid}: contest/project cannot count as a paper')
        aliases = entry.get('aliases', [])
        check(isinstance(aliases, list), f'{eid}: aliases must be an array')
        keys = {identity(str(k)) for k in [entry.get('identity', ''), *(aliases if isinstance(aliases, list) else [])]}
        for key in keys:
            check(bool(re.fullmatch(r'arxiv:\d{4}\.\d{4,5}|doi:10\.\d{4,9}/\S+', key)), f'{eid}: stable identity required')
            check(key not in identities, f'{eid}: duplicate paper/version/alias')
        identities.update(keys)
        title = re.sub(r'\W+', '', str(entry.get('title_en', '')).casefold())
        check(bool(title) and title not in titles, f'{eid}: missing/duplicate title or conference alias')
        titles.add(title)
        for field in ['title_zh', 'summary_zh', 'key_point_en', 'reading_focus_zh', 'published', 'limits']:
            check(bool(entry.get(field)), f'{eid}: missing {field}')
        stages = entry.get('stages')
        check(isinstance(stages, list) and bool(stages) and all(s in STAGES for s in stages), f'{eid}: invalid stages')
        status = entry.get('reading_status')
        check(status in {'metadata_only', 'abstract_screened', 'method_reviewed'}, f'{eid}: reading depth required')
        check(status != 'method_reviewed' or entry.get('access') == 'full', f'{eid}: abstract access is not method review')
        check(entry.get('priority') in {'priority', 'context'}, f'{eid}: invalid reading priority')
    for entry in artifacts:
        if isinstance(entry, dict): check(entry.get('kind') in {'contest', 'project'}, 'artifact must be contest/project')
    batches = data.get('batches')
    if batches is not None:
        if not isinstance(batches, list):
            return errors + ['literature: batches must be an array']
        paper_ids = {p.get('id') for p in papers if isinstance(p, dict)}
        artifact_ids = {a.get('id') for a in artifacts if isinstance(a, dict)}
        batch_ids, assigned = set(), []
        for batch in batches:
            if not isinstance(batch, dict):
                errors.append('literature: invalid batch'); continue
            bid = batch.get('id')
            check(isinstance(bid, str) and bid and bid not in batch_ids, 'missing/duplicate batch ID')
            batch_ids.add(str(bid))
            members = batch.get('paper_ids')
            if not isinstance(members, list):
                errors.append(f'literature: {bid}: paper_ids must be an array'); continue
            check(0 < len(members) <= 10, f'{bid}: a released batch needs 1–10 papers')
            check(all(isinstance(x, str) and x in paper_ids for x in members), f'{bid}: unknown paper in batch')
            assigned.extend(str(x) for x in members)
            artifacts_in_batch = batch.get('artifact_ids', [])
            check(isinstance(artifacts_in_batch, list) and all(isinstance(x, str) and x in artifact_ids for x in artifacts_in_batch),
                  f'{bid}: unknown artifact in batch')
        check(len(assigned) == len(set(assigned)), 'paper counted in multiple batch slots')
        check(set(assigned) == paper_ids, 'batch membership does not cover the catalog')
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate'])
    parser.add_argument('--catalog', type=Path, default=ROOT/'literature/catalog.json')
    args = parser.parse_args()
    try:
        data = json.loads(args.catalog.read_text())
        errors = validate_catalog(data)
        if errors: print('\n'.join(errors)); return 1
        print(f"Literature structure passed: {len(data['papers'])}/100 papers; "
              f"{len(data['artifacts'])} separate artifacts. Reading depths remain explicit; no scientific approval.")
        return 0
    except (ValueError, TypeError, OSError) as exc:
        print(f'Literature validation failed: {exc}'); return 1

if __name__ == '__main__': raise SystemExit(main())
