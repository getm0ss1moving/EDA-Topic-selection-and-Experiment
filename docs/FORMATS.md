# Structured record formats

Templates are incomplete by design and cannot be promoted. The standard-library validator checks structure, registration, state, evidence presence and content binding. It does not understand whether claims are true or whether an English paragraph is scientifically sufficient.

## Source entry in sources.json

```json
{
  "id": "SRC-001",
  "title": "Exact verified source title",
  "url": "https://publisher.example/actual-source",
  "type": "paper",
  "published": "YYYY-MM-DD or unknown",
  "retrieved": "YYYY-MM-DDTHH:MM:SSZ",
  "locator": "Section, equation, page, function, or commit/path/line",
  "access": "full",
  "claims": ["CLM-001"],
  "limitations": "What this source does not establish",
  "version": "DOI/version/commit where applicable",
  "license": "Verified license or unknown"
}
```

This example is a schema illustration, not a real citation. Supported source types include paper, contest, repository, official documentation and measured artifact. The verifier checks all decision-critical claims and their applicable sources; a nonempty source-check array alone is not sufficient scientific coverage.

## Verification

`verification.json` uses a `decision` of `pending`, `revise`, `park`, `reject`, or `accept_for_pilot`. For acceptance, all eight named gates, including `direction_integrity` and `experiment_consensus`, must be true, the direction penalty total must be zero, the three role sessions must be distinct and registered, and `dossier_digest` must equal the current digest. Change `dossier.json` to the target state before calculating the digest. `verification.md` and `verification.json` are excluded from this content digest; the final GitHub head review covers both, preventing an infinite self-hash loop.

## Direction control and abandonment

`direction-control.json` freezes the original problem/user/need/mechanism anchor. `combination_drift` and `demand_drift` are integer penalties from 0 through 3; their recorded total must equal their sum. A component at 2 or more, or a total at 3 or more, requires `abandonment_proposed` or `jointly_abandoned` rather than further experimental advancement. These penalties cannot be offset by performance forecasts.

For `jointly_abandoned`, set dossier status to `abandoned`, set direction state to `jointly_abandoned`, move it to `archive/`, choose at least one enumerated ground, preserve evidence and resurrection conditions, and record proposer and challenger consent. Both consents must use distinct registered sessions and bind the same existing full 40-character commit plus the same frozen dossier digest. The referenced commit must contain that topic revision. A registered verifier must independently verify every cited source and set `abandonment_process_checked`; the verifier cannot create either role's consent. A successor topic ID is optional but, when present, must differ from the abandoned ID.

## Experiment consensus

`experiment-consensus.json` binds agreement to the byte-exact SHA-256 of `tasklist.md`. Compute it with `python3 scripts/project.py tasklist-digest PATH_TO_DOSSIER`. Status `agreed` requires all readiness checks true, no open conditions and distinct registered proposer/challenger sessions. Both consents must say `agree`, provide a rationale, bind the same existing full 40-character commit and repeat the current task-list digest. The referenced commit must contain that exact task list. Any edit to `tasklist.md` makes the consensus stale and blocks `verified`, `accepted`, promotion to `topics/` and experiment start until both roles sign again.

Each `source_checks` entry has `source_id`, `locator`, `verdict` (`verified` for admission evidence), `checked_at`, and a concise entailment explanation. Each `objections` entry has `id`, `claim_id`, `verdict`, `blocking` (boolean), `resolution` (`resolved` or `open`), and an evidence-backed rationale. Do not omit a material objection to satisfy a gate; the verifier checks completeness against `challenges.md` manually.

## Forecast

`forecast.json` remains labeled `forecast_not_measurement`. Values may be null during intake; each null needs a task in the plan. Before pilot admission the verifier requires either evidence-backed ranges with units and direction or an explicit plan to estimate uncertain headroom before a larger commitment. Define whether an effect is relative percent, absolute difference or a ratio. Do not compare percentage points and relative percentages interchangeably.

## Session and run record

Register scientific sessions in `config/roles.json` with every listed required field. `packet_sha256` is the SHA-256 of the exported `PACKET.json`; it describes a prior frozen input, not the commit containing the newly created registration. A coordinator may first export the packet, then register the new session in the next commit. No circular hash is needed.

Create `runs/<run-id>/manifest.json` from `templates/run.json`. Only released manifests are included in ordinary role packets. Put governance review reports next to their manifest. Never put private reasoning into `runs/`. Use `shasum -a 256 /absolute/packet/PACKET.json` to compute packet identity. Record missing metadata honestly rather than substituting another role's identity.
