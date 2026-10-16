# EDA-0011 fourth-cycle independent protocol audit

Disposition: nonblocking_findings. No supported conduct violation found within supplied scope; no scientific acceptance vote.

| Role | Rule | Status | Evidence / reason |
|---|---|---|---|
| challenger | inputs | no_violation_found_within_scope | shared/job-descriptors/challenger/JOB.json#/released_inputs; shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/compliance.json#/read_releases — Declared reads are in the descriptor allowlist; identity and packet bindings match. No complete trace is supplied. |
| challenger | isolation | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/compliance.json#/activity; shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/compliance.json#/observability — Distinct logical sessions and no disclosed checkout/private reads or messaging. Self-report does not establish invisible behavior or physical backend identity. |
| challenger | writes | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/SUBMISSION.json#/files; shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/compliance.json#/operations — Frozen file hashes match the manifest; released files are role-owned artifacts. Unseen filesystem writes are outside scope. |
| challenger | evidence | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/sources.json; shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/search-log.md — Sources have identities, locators and access limitations; incomplete method/winner access remains explicit. This audit does not independently settle scientific entailment. |
| challenger | claims | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/independent-estimate.md — Forecasts, conditional reasoning and finite-model observations are distinguished from physical measurements; no empirical EDA gain or universal novelty clearance asserted. |
| challenger | consent | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/experiment-consent.json — Current task hash matches; both scientific parties request revision. Verifier records no matching agreement and parks; no invented consent. |
| challenger | resources | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/compliance.json#/activity; shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/challenges.md#Coverage, limits and final scientific position — No new EDA/training/paid allocation claimed. Proposer tiny rational fixture is allowed research, with public code/stdout; other roles disclose no numerical replay. Future caps are requests. |
| challenger | direction | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/challenges.md#Positive findings and anchor — New EDA-0011 anchor is distinguished from predecessor, negatives retained, zero drift is not merit or acceptance. Scientific judgments remain assigned verifier decisions. |
| challenger | publication | no_violation_found_within_scope | shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/workflow.json; shared/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/SUBMISSION.json — English frozen artifacts and final-cycle park/unresolved position; no self-approval, merge, fifth cycle or pilot authorization shown. Transport beyond release is outside scope. |
| proposer | inputs | no_violation_found_within_scope | shared/job-descriptors/proposer/JOB.json#/released_inputs; shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/compliance.json#/read_releases — Declared reads are in the descriptor allowlist; identity and packet bindings match. No complete trace is supplied. |
| proposer | isolation | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/compliance.json#/activity; shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/compliance.json#/observability — Distinct logical sessions and no disclosed checkout/private reads or messaging. Self-report does not establish invisible behavior or physical backend identity. |
| proposer | writes | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/SUBMISSION.json#/files; shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/compliance.json#/operations — Frozen file hashes match the manifest; released files are role-owned artifacts. Unseen filesystem writes are outside scope. |
| proposer | evidence | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/sources.json; shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/search-log.md — Sources have identities, locators and access limitations; incomplete method/winner access remains explicit. This audit does not independently settle scientific entailment. |
| proposer | claims | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/forecast.json — Forecasts, conditional reasoning and finite-model observations are distinguished from physical measurements; no empirical EDA gain or universal novelty clearance asserted. |
| proposer | consent | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/experiment-consent.json — Current task hash matches; both scientific parties request revision. Verifier records no matching agreement and parks; no invented consent. |
| proposer | resources | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/compliance.json#/activity; shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/experiment-plan.md#A01: own finite analytical check, actually executed — No new EDA/training/paid allocation claimed. Proposer tiny rational fixture is allowed research, with public code/stdout; other roles disclose no numerical replay. Future caps are requests. |
| proposer | direction | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/direction-control.json#/anchor — New EDA-0011 anchor is distinguished from predecessor, negatives retained, zero drift is not merit or acceptance. Scientific judgments remain assigned verifier decisions. |
| proposer | publication | no_violation_found_within_scope | shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/workflow.json; shared/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/SUBMISSION.json — English frozen artifacts and final-cycle park/unresolved position; no self-approval, merge, fifth cycle or pilot authorization shown. Transport beyond release is outside scope. |
| verifier | inputs | no_violation_found_within_scope | shared/job-descriptors/verifier/JOB.json#/released_inputs; shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/compliance.json#/read_releases — Declared reads are in the descriptor allowlist; identity and packet bindings match. No complete trace is supplied. |
| verifier | isolation | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/compliance.json#/activity; shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/compliance.json#/observability — Distinct logical sessions and no disclosed checkout/private reads or messaging. Self-report does not establish invisible behavior or physical backend identity. |
| verifier | writes | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/SUBMISSION.json#/files; shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/compliance.json#/operations — Frozen file hashes match the manifest; released files are role-owned artifacts. Unseen filesystem writes are outside scope. |
| verifier | evidence | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.json#/source_checks; shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.md#Limits — Sources have identities, locators and access limitations; incomplete method/winner access remains explicit. This audit does not independently settle scientific entailment. |
| verifier | claims | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.json#/claim_checks — Forecasts, conditional reasoning and finite-model observations are distinguished from physical measurements; no empirical EDA gain or universal novelty clearance asserted. |
| verifier | consent | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.json#/consent_details — Current task hash matches; both scientific parties request revision. Verifier records no matching agreement and parks; no invented consent. |
| verifier | resources | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/compliance.json#/activity; shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.json#/analytical_checks — No new EDA/training/paid allocation claimed. Proposer tiny rational fixture is allowed research, with public code/stdout; other roles disclose no numerical replay. Future caps are requests. |
| verifier | direction | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.json#/successor_assessment — New EDA-0011 anchor is distinguished from predecessor, negatives retained, zero drift is not merit or acceptance. Scientific judgments remain assigned verifier decisions. |
| verifier | publication | no_violation_found_within_scope | shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/workflow.json; shared/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/SUBMISSION.json — English frozen artifacts and final-cycle park/unresolved position; no self-approval, merge, fifth cycle or pilot authorization shown. Transport beyond release is outside scope. |

## Findings

INC-001 (limitation): Retain observability limitation for all three roles; do not describe this audit as certification of unseen conduct. Scientific adjudication required for a disputed scientific interpretation: False.

INC-002 (research_defect): Preserve the assigned verifier’s recorded fixable dependency-readiness finding and dormant park outcome. This audit neither independently re-adjudicates it nor orders new work. Any disputed scientific interpretation requires independent scientific adjudication. Scientific adjudication required for a disputed scientific interpretation: True.

No missing measurement, unallocated workload, unresolved novelty or honest inaccessible-paper disclosure is treated as misconduct. The scientific verifier adjudicated OBJ-1401/1402/1403 and retained park. A01 public code/stdout is present; this auditor did not replay another actor’s code. No new source-error allegation is decided here.

## Limits

- Released artifacts and public descriptors are the complete audited conduct evidence; self-ledgers are not complete tool traces or proof of absence of undisclosed actions.
- Physical model/backend, OS/network behavior and adversarial confinement are not independently attested.
- Aggregate reads were truncated; targeted readings covered ledgers, current findings, task dependencies, finite fixture, consent and provenance. No claim of exhaustive bibliography review.
- No external original reopened: no decision-critical source-error/conduct allegation was advanced here. Scientific novelty, demand and complete source entailment remain the assigned scientific verifier domain.
- Historical predecessor bytes and late allegations were not supplied directly to this auditor and were not independently audited. No rejected-attempt index was assigned in JOB.json.
- Full repository validate/publication is the coordinator duty under standalone prompts; this job uses frozen-byte and trusted submission checks.

## Reproducible mechanical check

The following is own mechanical checking only, no scientific numerical experiment or foreign code execution. Run from the assigned job root. The earlier equivalent check returned the same stdout; this exact published version was also executed.

```python
import json, pathlib, hashlib
job = json.load(open("JOB.json"))
for role, rid in job["reviewed_releases"].items():
    root = pathlib.Path("shared") / rid
    manifest = json.load(open(root / "SUBMISSION.json"))
    descriptor = json.load(open("shared/job-descriptors/" + role + "/JOB.json"))
    ledger = json.load(open(root / "compliance.json"))
    for key in ("actor_id", "session_id", "input_commit", "packet_sha256", "role"):
        assert manifest[key] == descriptor[key] == ledger[key]
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
    allowed = {pathlib.Path(x).name for x in descriptor["released_inputs"]}
    assert set(ledger["read_releases"]) <= allowed
    print(role + ": manifest hashes, identity and declared read allowlist PASS")
p = pathlib.Path("shared") / job["reviewed_releases"]["proposer"]
h = hashlib.sha256((p / "tasklist.md").read_bytes()).hexdigest()
for role in ("proposer", "challenger"):
    c = json.load(open(pathlib.Path("shared") / job["reviewed_releases"][role] / "experiment-consent.json"))
    assert c["tasklist_sha256"] == h and c["decision"] == "revision_requested"
v = json.load(open(pathlib.Path("shared") / job["reviewed_releases"]["verifier"] / "verification.json"))
assert {x["id"] for x in v["objections"]} == {"OBJ-1401", "OBJ-1402", "OBJ-1403"}
print("task hashes and nonagreeing consents PASS; all three current objections adjudicated")
```

Exact stdout:

```text
challenger: manifest hashes, identity and declared read allowlist PASS
proposer: manifest hashes, identity and declared read allowlist PASS
verifier: manifest hashes, identity and declared read allowlist PASS
task hashes and nonagreeing consents PASS; all three current objections adjudicated
```
