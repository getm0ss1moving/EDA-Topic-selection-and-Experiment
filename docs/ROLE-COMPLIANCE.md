# Per-role compliance evidence and independent protocol review

Effective for jobs with `JOB.json.compliance_required=true`. Historical releases
remain valid and are never retroactively edited. This is an audit of observable
conduct, not a presumption of misconduct and not a new scientific acceptance vote.

## Scientific role activity ledger

Before discovery open only your assigned JOB/prompt and its policy directory.
The checkout is not your packet. Do not run broad checkout/home/session discovery
to find instructions: the required common policies and your one harness are in
the job. Independently accessible external research remains allowed. Another
role's withheld material is forbidden regardless of location.

Every new scientific release includes `compliance.json`, using the supplied
template. Fill the exact manifest role/actor/session/input commit/packet hash and
JOB job_id. `read_releases` lists only actual explicitly released inputs or your
own previous outputs read; do not list an input as read merely because it exists.
`operations` is a concise public activity ledger: file/source references, searches,
analytical commands, output writes and freeze. It may reference your search log
and source IDs instead of duplicating them. Never include credentials, private
reasoning, transcripts or another role's withheld content.

Cover all nine rule areas: inputs, isolation, writes, evidence, claims, consent,
resources, direction and publication. Each self-report row has `status` from
`no_violation_disclosed`, `deviation_disclosed`, `unknown`, a nonempty `evidence`
list and a candid `limits` string. State actual checkout exposure and any incident.
No experiment resources are newly allocated in this batch. Counts concern this
job, not historical experiments. Source retrieval and tiny own analytical tests
are research; EDA builds/flow execution and training are distinct resource use.

A ledger is self-authored evidence, not a complete tool trace. Do not claim it
proves the absence of undisclosed actions. Unknown observations stay unknown.
Public common-policy-only checkout reads are a procedural deviation; they do not
alone prove private scientific contamination. Reading withheld scientific material,
cross-role private messages/memory, fabricated consent, or unallocated experiment
execution is materially different and requires stopping/quarantine and independent
replacement/review. Never delete an exposure disclosure to pass collection.

The ledger is frozen with the research release. It is metadata excluded from the
consent scientific-content comparison; proposal/tasklist/dependencies remain
protected. Identity, hash and allowlist checks remain mandatory. Failed findings
do not disappear when a corrected release is created.

## Independent verifier protocol-audit mode

After a complete P/C/V cycle, a NEW verifier execution with a distinct logical
session receives only the exact three frozen outputs, their public JOB/prompt
descriptors, common policy and the verifier harness. It is a governance review
under that harness, not a fourth advocating/challenging scientific role. Requested
model is the configured verifier model/effort. No inherited conversations or
private logs, notes, transcripts or memory are inspected. This explicitly covers
the scientific verifier rather than allowing it to certify itself.

Write `verification.md` as a compact three-role by nine-rule matrix, plus findings
and limits. Write `verification.json` and `workflow.json` with:

```json
{
  "purpose": "protocol_audit",
  "reviewed_releases": {"proposer":"SUB-...","challenger":"SUB-...","verifier":"SUB-..."},
  "disposition": "clear_within_scope"
}
```

`workflow.json` also has `role: verifier`. Allowed dispositions are
`clear_within_scope`, `nonblocking_findings`, `unresolved`, `blocking_violation`.
`verification.json.roles` has exactly proposer/challenger/verifier; each contains
its exact `release_id` and `checks` covering all nine rule names. Every check has
`status` from `no_violation_found_within_scope`, `supported_deviation`, `unresolved`,
an evidence list with precise file/JSON/line locators and a reason. Include a
`limitations` list and `findings` list (empty is valid). Each finding has unique
`id: INC-NNN`, role, rule, `severity` (critical or noncritical), `classification` from supported_violation,
potential_violation, research_defect, limitation; evidence, action and boolean
`needs_scientific_adjudication`. Add your OWN compliance.json and self-freeze as
the assigned verifier. Final result.json follows the job schema.

Check role inputs/separation, evidence traceability/access claims, forecast and
measurement labels, source locators, task/consent bindings, budget and anchor
claims, release integrity, English artifacts and publication conduct. Reopen a
decision-critical source where necessary for a conduct finding. A source error
does not establish deliberate fabrication. Distinguish a weak hypothesis, missing
resource or honestly disclosed inaccessible paper from a rule violation. A known
component, missing empirical gain or unresolved novelty is not itself misconduct.

Do not replace the assigned scientific verifier's evidence ruling or silently
rewrite another role's output. Scientific disagreements/source-error allegations
are explicitly marked for scientific adjudication and remain unverified until
that occurs. Later scientific verifiers may receive the released audit; proposers
do not receive its unadjudicated scientific criticism. No acceptance/abandonment
vote is created by this review. The auditor's own self-ledger is mechanically
checked, not represented as an infinite chain of independent audit.

## Transport, consequences and limits

The coordinator checks exact bindings, completeness and frozen bytes, then
publishes the audit with that cycle's three scientific releases in the SAME PR.
Audited batches cannot publish a round or dispatch the next scientific role until
the independent protocol review is collected. `blocking_violation` blocks both;
preserve the incident and replace contaminated executions/downstream reviews,
without counting a tainted cycle as valid. Mechanical omissions go to the author
for a new freeze, never a coordinator-written scientific edit. Nonblocking
deviations and unresolved observability are published candidly; they do not turn
into clearance or justify pilot selection. Unresolved/blocking audits cannot
support scientific acceptance or joint abandonment. Both are distinct from park.

Four cycles per domain count the substantive research cycles, including any
successor. Eight small independent protocol reviews audit the 24 scientific
outputs in this two-domain batch. No fifth research cycle is started to erase an
unresolved final audit. Final reporting includes every role/round, supported
deviations, unresolved observations, corrections, quarantine/replacement if any,
and the audit's limits. The shared OS does not enforce adversarial confinement;
the audit cannot certify unseen filesystem/network behavior from self-reports.

### Durable quarantine and clean replacement

The coordinator saves the clean released-input checkpoint before each audited
proposer job. A disclosed forbidden read/activity is a `ProtocolViolation`, not
a mechanical retry: preserve its frozen attempts and incident metadata, remove
the job from the active queue, and mark the domain quarantined. Deleting a
disclosure or re-freezing that same job cannot advance it. A critical supported
protocol audit similarly removes the tainted triple from the publication queue
while preserving its complete round/audit record as an incident.

Use `codex_loop.py --config CONFIG recover --domain D04` (or D05) to prepare
fresh identities, sessions and packets for all three scientific roles from that
cycle's clean checkpoint. The replacement inherits no tainted-cycle output;
previously released clean history remains available. Dispatch the replacement
proposer, rerun the full triple and create a new independent audit. Only the
replacement counts toward the four valid cycles. Quarantined bytes and findings
remain in the incident index and cannot be rewritten into clearance. A recovery
command prepares files; it neither launches a model nor supplies any scientific
approval. Preserve and report a recovery failure rather than manually clearing
the quarantine flag.

Mechanical rejections also receive an immediate coordinator copy under
`rejected-attempts/JOB_ID/`, outside the retried role's job. The index and verified
owned frozen bytes there are the audit authority; a deletable author-facing
mirror is only a retry aid. Auditors receive these explicitly released attempts
alongside the latest three bindings, and publication preserves them. Invalid or
foreign-identity snapshots are not exported as owned evidence. Frozen hashes and
read-only files support accidental-change detection under this policy; the shared
OS account still does not enforce adversarial immutability.
