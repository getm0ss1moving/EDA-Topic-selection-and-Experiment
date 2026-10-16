# D04 EDA-0009 B04-R3 independent protocol audit

Disposition: **unresolved** (bounded observability), not a scientific decision. No supported conduct deviation is found in the supplied current releases. No new research defect or source-error allegation is established.

Auditor: ChatGPT-B04-PROTOCOL-D04-EDA-0009-R3; session 54292b41-24b9-4994-b9e9-d603ca9c5ae2; input d0eedf3130de673ea92e4be202a32d463a63f301; packet 85919b4e3685966fb36bd01471c8a6063471be016ea5b1118ee8c05510a2b12a.

| Role | Exact release |
|---|---|
| challenger | SUB-83d9a23ab90f7ca974796e8ed39617078e1ee76f0abcab0f0746f6bab6c2278f |
| proposer | SUB-2966cec6a631f48b998ddb78b67aba187e072ad1d9b4d3498aeebdb879a9f0cc |
| verifier | SUB-047b42329a35771ca6788e18cc97583dedaf36526c13f12defa839e36c8b1ed0 |

N = no_violation_found_within_scope; U = unresolved. Evidence and reasons for every cell are in verification.json at roles.<role>.checks.<rule>.

| Role | inputs | isolation | writes | evidence | claims | consent | resources | direction | publication |
|---|---|---|---|---|---|---|---|---|---|
| challenger | N | N | N | N | N | N | N | N | N |
| proposer | U | U | N | N | N | N | U | N | N |
| verifier | N | N | N | N | N | N | N | N | N |

INC-001 (noncritical limitation): proposer compliance.json#/incidents/0 and search-log.md#Identity and observed exposure explicitly preserve unknown earlier interruption scope. Current allowed reads/bytes are consistent; earlier undisclosed activity is neither disproved nor alleged. Keep inputs/isolation/resources unresolved for that specific scope. No private records were sought. This is not evidence of deliberate fabrication, prohibited reads or unauthorized experiments.

The current challenger is unresolved, declines agreement, and recommends park; the scientific verifier covers all six OBJ IDs and parks. Proposer pending consent is not current agreement. The current task hash matches challenger and verifier records. Missing empirical gain, allocation, selective interface and novelty resolution remain honest research prerequisites, not misconduct. All three preserve strong conventional comparisons, endpoint guards and negative results. No numerical proposer model replay or physical test was performed by this auditor. Scientific entailment stays with the assigned scientific verifier.

## Limits

- The three self-authored ledgers are not complete filesystem/network/tool traces; declared logical sessions do not attest physical backend configuration or adversarial confinement.
- Only exact current releases and public descriptors were inspected. Historical inputs are checked against descriptor allowlists, not reopened; original source entailment is not independently adjudicated in this protocol audit.
- Proposer preserves unknown pre-interruption scope (OBS-R3-INTERRUPTION). The coordinator also reported an earlier interruption of this audit job; this continuation cannot reconstruct unseen actions and did not inspect any private transcript.
- No rejected-attempt index is supplied in the assigned shared inputs. Absence here is not proof that no interrupted/mechanical attempt occurred.
- Metadata/source-record completeness is not scientific verification. No external source reopening was necessary for a supported conduct finding; no new scientific source verdict or acceptance vote is made.
- Full-repository validation/publication is the coordinator duty under the public descriptors; standalone trusted freeze/verify is the local check.

## Exact own reproducible metadata check

Run from this job root using the assigned shared inputs and trusted policy script. It imports only the trusted policy validator, never upstream scientific code.

```python
from pathlib import Path
import hashlib,json,re,importlib.util
j=json.loads(Path('JOB.json').read_text())
spec=importlib.util.spec_from_file_location('trusted','policy/scripts/role_submission.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
roles=j['reviewed_releases']; sessions=[]
for role,rid in sorted(roles.items()):
 p=Path('shared')/rid; manifest,payload=m.verify(p)
 d=json.loads((Path('shared/job-descriptors')/role/'JOB.json').read_text()); c=json.loads(payload['compliance.json'])
 for key in ['role','actor_id','session_id','input_commit','packet_sha256']:
  assert manifest[key]==d[key]==c[key],(role,key)
 assert c['job_id']==d['job_id']
 allowed={Path(x).name for x in d['released_inputs']}
 assert set(c['read_releases'])<=allowed,(role,'unlisted read')
 sessions.append(manifest['session_id'])
 print(role,'frozen_bytes_identity_read_allowlist',True,'files',len(payload))
assert len(set(sessions))==3
p=Path('shared')/roles['proposer'];c=Path('shared')/roles['challenger'];v=Path('shared')/roles['verifier']
h=hashlib.sha256((p/'tasklist.md').read_bytes()).hexdigest();cs=json.loads((c/'experiment-consent.json').read_text());vs=json.loads((v/'verification.json').read_text())
assert cs['tasklist_sha256']==h==vs['experiment_consensus']['tasklist_sha256']
ids=set(re.findall(r'OBJ-\d+', (c/'challenges.md').read_text())); rows={x['id'] for x in vs['objections']}
assert ids<=rows
print('distinct_declared_sessions',True)
print('current_task_sha256',h)
print('challenger_consent',cs['decision'],'verifier_decision',vs['decision'])
print('challenge_OBJ_coverage',len(ids),len(ids&rows))
for role,rid in sorted(roles.items()):
 p=Path('shared')/rid
 sf=p/'sources.json'
 sources=json.loads(sf.read_text()) if sf.exists() else json.loads((p/'verification.json').read_text())['sources']
 required={'id','title','url','source_type','publication_date','retrieved_utc','locator','access_level','supported_claim_ids','limitations'}
 assert all(required<=set(s) for s in sources)
 assert all(s['access_level'] in ['full','abstract','metadata'] for s in sources)
 print(role,'source_record_structure',len(sources),True)
print('scope','metadata only; no source entailment, numerical toy replay or EDA execution')
```

Exact stdout:

```text
challenger frozen_bytes_identity_read_allowlist True files 9
proposer frozen_bytes_identity_read_allowlist True files 14
verifier frozen_bytes_identity_read_allowlist True files 4
distinct_declared_sessions True
current_task_sha256 fdf7b942d287db89fcf5ca528942d64cc41b5f715abbd278466b33c44874ed5c
challenger_consent revision_requested verifier_decision park
challenge_OBJ_coverage 6 6
challenger source_record_structure 16 True
proposer source_record_structure 43 True
verifier source_record_structure 10 True
scope metadata only; no source entailment, numerical toy replay or EDA execution
```

Code SHA-256: 951e4829294d1b99bd7cda7928daa79d19e17704d37729bc593528690a497f96. Stdout SHA-256: cc5af224167c1e400eb27b9b2a3b3985375dd28ab0ff175a2e83adb4c09eaa8c. These checks certify only declared metadata/bytes, not unseen conduct or source truth.
