#!/usr/bin/env python3
"""Render frozen independent protocol rulings; no new conduct/scientific vote."""
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
RULES = ("inputs", "isolation", "writes", "evidence", "claims", "consent", "resources", "direction", "publication")
STATUS = {"no_violation_found_within_scope": "N", "supported_deviation": "D", "unresolved": "U"}


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def main():
    rows = json.loads((RUN / "role-compliance-index.json").read_text())
    assert len(rows) == 8
    assert {d: sum(r["domain"] == d for r in rows) for d in ("D04", "D05")} == {"D04": 4, "D05": 4}
    totals = {s: 0 for s in STATUS}
    text = ["# Batch 0004: per-role independent conduct matrix", "",
            "This coordinator rendering transcribes eight frozen independent protocol reviews of 24 valid scientific outputs. It does not certify unseen conduct, replace a scientific ruling or erase rejected/invalid attempts. N means no violation found within the supplied scope; D means supported deviation; U means unresolved. A missing physical result or weak hypothesis is not automatically misconduct.", "",
            "| Domain/cycle | Topic | Role | Inputs | Isolation | Writes | Evidence | Claims | Consent | Resources | Direction | Publication | Audit |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["domain"], r["domain_cycle"])):
        for role in ("proposer", "challenger", "verifier"):
            checks = r["roles"][role]["checks"]
            assert set(checks) == set(RULES)
            for c in checks.values():
                totals[c["status"]] += 1
            values = [f'{r["domain"]}/{r["domain_cycle"]}', r["topic"], role]
            values += [STATUS[checks[rule]["status"]] for rule in RULES]
            values += [f'[frozen review](../../runs/{r["audit_release"]}/verification.md)']
            text.append("| " + " | ".join(values) + " |")
    assert sum(totals.values()) == 216
    incident = json.loads((RUN / 'incident-review.json').read_text()) if (RUN / 'incident-review.json').exists() else None
    incident_totals = {s: 0 for s in STATUS}
    if incident and incident.get('audit_release'):
        review = json.loads((ROOT / 'runs' / incident['audit_release'] / 'verification.json').read_text())
        text += ['', '## Quarantined attempt: excluded from the 24 valid scientific rows', '',
                 'The original attempt and all three outputs remain retained. Its fresh independent review is '
                 + review['disposition'] + '; the clean replacement does not erase it. '
                 'Canonical-ID formatting and missing own-previous ownership evidence are distinguished from proven forbidden content access.', '',
                 '| Role | Inputs | Isolation | Writes | Evidence | Claims | Consent | Resources | Direction | Publication |',
                 '|---|---|---|---|---|---|---|---|---|---|']
        for role in ('proposer', 'challenger', 'verifier'):
            checks = review['roles'][role]['checks']
            for check in checks.values():
                incident_totals[check['status']] += 1
            text.append('| ' + ' | '.join([role] + [STATUS[checks[rule]['status']] for rule in RULES]) + ' |')
        text += ['', f'Exact findings and scope: [incident review](../../runs/{incident["audit_release"]}/verification.md).', '']
    for r in sorted(rows, key=lambda r: (r["domain"], r["domain_cycle"])):
        text += ["", f'## {r["domain"]} cycle {r["domain_cycle"]}: {r["compliance_gate"]}', "",
                 "| Finding | Role/rule | Classification/severity | Action | Scientific adjudication needed |",
                 "|---|---|---|---|---|"]
        for f in r["findings"]:
            values = [f["id"], f'{f["role"]}/{f["rule"]}', f'{f["classification"]}/{f["severity"]}', f["action"], f["needs_scientific_adjudication"]]
            text.append("| " + " | ".join(cell(x) for x in values) + " |")
        if not r["findings"]:
            text.append("| none within supplied scope | — | — | Preserve limits | false |")
        text += ["", "Limits: " + " ".join(cell(x) for x in r["limitations"]), ""]
    text += ["## Evidence bounds", "",
             "See public-review-followups.json for any post-audit comments. Unadjudicated science is not a coordinator verdict and is not dismissed by prior N cells. Frozen source, manifest and public descriptor identity checks do not attest backend model identity, absent hidden reads, strong OS confinement or scientific novelty. Self-ledgers are not complete traces; no private conversations, scratch, memories or chain of thought are inspected for this report.", "",
             "mechanical-rejections.json and quarantine-incidents.json preserve any recorded attempts; valid-output counts do not include failed/replaced partial cycles. No experiment, resource allocation, joint abandonment or acceptance follows from this conduct rendering.", ""]
    text += ['Batch 0003 historical metadata-only coverage, including its 15 unresolved cells, remains unchanged. '
             'New scoped scientific rulings on HIST-LOCATOR/HIST-REPLAY do not retroactively certify historical execution or other conduct.', '',
             'backend-failures.json preserves platform screening interruptions and same-model continuations. '
             'The screening cause and unobserved interrupted activity are not inferred. In particular the D04 cycle-3 '
             'protocol review retains the proposer input/isolation/resource uncertainty rather than converting an interruption into misconduct or clearance.', '']
    out = ROOT / "reports/final/GPT-COMPLIANCE-0004.conduct.en.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(text))
    counts = {"scientific_role_rows": 24, "rule_cells": 216, "cell_status_counts": totals,
              "overall_audit_statuses": {s: sum(r["compliance_gate"] == s for r in rows) for s in sorted({r["compliance_gate"] for r in rows})},
              "scope": "Evidence-bounded independent reviewer cells; not a hidden-action compliance rate or a new scientific vote."}
    if incident and incident.get('audit_release'):
        counts['quarantined_attempt'] = {'role_rows': 3, 'rule_cells': 27,
            'cell_status_counts': incident_totals, 'audit_release': incident['audit_release'],
            'disposition': incident['disposition'], 'excluded_from_valid_cycle_counts': True}
    (RUN / "conduct-counts.json").write_text(json.dumps(counts, indent=2) + "\n")
    print(out)


if __name__ == "__main__":
    main()
