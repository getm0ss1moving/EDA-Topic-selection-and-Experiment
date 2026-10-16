# Independent protocol audit — D04 batch 0004 cycle 2

Actor `ChatGPT-B04-PROTOCOL-D04-EDA-0009-R2`; session `4d949ecf-ec0e-421a-b0de-42a5e6a3572b`; job `747156e5-6c9f-42cc-8b3a-da02cc027b73`. Input commit `d0eedf3130de673ea92e4be202a32d463a63f301`; packet `d035415655571592e441d9b6044f5fb3ae2ce251edfc3d6df8cea820db65c9e0`.

Disposition: **clear_within_scope**. No supported deviation or conduct violation was found in the supplied record. This is not proof of absent undisclosed actions and is not scientific acceptance.

| Role | Frozen release |
|---|---|
| challenger | SUB-3090026e572d0cecae72323cca434d6748d78424acd61699d6ecfb2e8aad0f6b |
| proposer | SUB-988d5b734de75037f4ca472fe6c9799a673f9538cd7b4053da26a004347406f8 |
| verifier | SUB-b69a8b5d5ff701c8a70bb5122fcfe70e9cf376634d0f50de420109f7e3b8d8a0 |

N = no_violation_found_within_scope. Precise evidence locators and reasons for every cell are in verification.json roles/ROLE/checks/RULE.

| Role | inputs | isolation | writes | evidence | claims | consent | resources | direction | publication |
|---|---|---|---|---|---|---|---|---|---|
| challenger | N | N | N | N | N | N | N | N | N |
| proposer | N | N | N | N | N | N | N | N | N |
| verifier | N | N | N | N | N | N | N | N | N |

Findings: none. The self-ledgers disclose no forbidden checkout/private exposure. Distinct identities, public allowlists and frozen file hashes match. Public tiny-fixture code/stdout distinguish abstract counts from physical results; null forecasts and closed EXP-100 are candid limitations. The pending proposer record expressly disclaims a signature over changed bytes; challenger requests revision, and the scientific verifier does not turn either into agreement. The source-binding assertion repair and corrected source locator are disclosed research corrections, not evidence of contamination or fabricated measurement.

The existing scientific verdict remains revise. OBJ-1101 is independently adjudicated in the scientific verifier release; no new ruling is created here. Narrow demand, selective-adapter feasibility, equal-action comparator, winner bridge and missing measured utility remain scientific unresolved prerequisites, not conduct violations. No source-error allegation was independently established; any later such dispute requires scientific adjudication.

## Limits

- Only the exact three frozen releases, public JOB/prompt descriptors and assigned common policy/verifier harness were reviewed. No rejected attempts were supplied. Historical releases named in those documents were not opened.
- Role ledgers are self-authored disclosures, not complete tool traces. Unseen filesystem/network actions, private reads, actual model/backend configuration and adversarial isolation remain unobserved; absence is not certified.
- No external original was reopened for this conduct-only audit; no independent scientific source-error finding or novelty/performance verdict is made. Scientific verifier source rulings retain their original limited scope.
- Some combined reads were truncated and targeted current logs, consents, tasklists and verification were reopened. This is not exhaustive line-by-line bibliographic verification.
- Full project validation was attempted via python3 policy/scripts/project.py validate and failed because policy/config/roles.json is absent. Standalone packet validation does not replace coordinator repository/PR validation.
- Frozen manifests protect accidental byte changes, not malicious same-account modification. No publication transport, merge, real resource allocation, historical execution or complete host trace is certified.

## Own bounded mechanical check

Code below only hashes released files and compares public descriptors/metadata. It does not execute another role script, source download, EDA flow or experiment, and does not prove source entailment or historic execution. Run from this assigned job root.

```python
from pathlib import Path
import json, hashlib
job=json.loads(Path('JOB.json').read_text())
for role,rid in sorted(job['reviewed_releases'].items()):
    base=Path('shared')/rid
    manifest=json.loads((base/'SUBMISSION.json').read_text())
    descriptor=json.loads((Path('shared/job-descriptors')/role/'JOB.json').read_text())
    ledger=json.loads((base/'compliance.json').read_text())
    for key in ('actor_id','session_id','input_commit','packet_sha256','role','topic'):
        assert manifest[key]==descriptor[key]
    for key in ('actor_id','session_id','input_commit','packet_sha256','role','job_id'):
        assert ledger[key]==descriptor[key]
    for name,digest in manifest['files'].items():
        assert hashlib.sha256((base/name).read_bytes()).hexdigest()==digest
    allowed={p.split('/')[-1] for p in descriptor['released_inputs']}
    assert set(ledger['read_releases']) <= allowed
    assert set(ledger['rules'])==set('inputs isolation writes evidence claims consent resources direction publication'.split())
    print(role+': identities/hash map/read allowlist/nine-rule coverage PASS')
p=Path('shared')/job['reviewed_releases']['proposer']
c=Path('shared')/job['reviewed_releases']['challenger']
v=Path('shared')/job['reviewed_releases']['verifier']
h=hashlib.sha256((p/'tasklist.md').read_bytes()).hexdigest()
assert json.loads((p/'workflow.json').read_text())['tasklist_sha256']==h
assert json.loads((c/'experiment-consent.json').read_text())['tasklist_sha256']==h
assert json.loads((v/'verification.json').read_text())['experiment_consensus']['tasklist_sha256']==h
assert json.loads((p/'experiment-consent.json').read_text())['decision']=='pending'
assert json.loads((c/'experiment-consent.json').read_text())['decision']=='revision_requested'
print('tasklist binding PASS; no dual agreement asserted')
assert len({json.loads((Path('shared')/rid/'SUBMISSION.json').read_text())['session_id'] for rid in job['reviewed_releases'].values()})==3
print('three distinct declared scientific sessions PASS; backend/isolation unobserved')
```

Exact stdout:

```text
challenger: identities/hash map/read allowlist/nine-rule coverage PASS
proposer: identities/hash map/read allowlist/nine-rule coverage PASS
verifier: identities/hash map/read allowlist/nine-rule coverage PASS
tasklist binding PASS; no dual agreement asserted
three distinct declared scientific sessions PASS; backend/isolation unobserved
```

Code SHA-256: `198dbd8e2c6932d2f0cb076192c6bda2ef2a4f6534befd61c786f800cadf36c9`; stdout SHA-256: `9d41b063ba5e610ef2d8387b183c3dac0c1a066ead1a1ac2c099a7d77b4c0174`.

Validation attempt: `python3 policy/scripts/project.py validate` failed with missing `policy/config/roles.json`; no checkout was opened to repair the incomplete standalone policy export. Trusted submission freeze/verify are separate mechanical checks.
