#!/usr/bin/env python3
"""Render the eight frozen independent reviews without re-adjudicating them."""
import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
RULES = ("inputs", "isolation", "writes", "evidence", "claims", "consent", "resources", "direction", "publication")
SHORT = {"no_violation_found_within_scope": "N", "supported_deviation": "D", "unresolved": "U"}


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def main():
    data = json.loads((RUN / "role-compliance-index.json").read_text())
    assert len(data) == 8
    assert {d: sum(r["domain"] == d for r in data) for d in ("D04", "D05")} == {"D04": 4, "D05": 4}
    lines = ["# Batch 0003: independent per-role conduct review", "",
             "This report transcribes eight frozen protocol-verifier rulings. It is a coordinator summary, not a new scientific or conduct vote. Twenty-four valid scientific outputs are covered across 216 rule cells. Superseded/aborted attempts and coordinator incidents remain separately recorded; a replacement does not erase them.", "",
             "N = no violation found within the supplied evidence; D = supported deviation; U = unresolved. N does not prove absent hidden actions. Scientific uncertainty, a weak hypothesis and honestly disclosed source/resource gaps are not automatically misconduct.", "",
             "| Domain/cycle | Topic | Role | Input | Isolation | Writes | Evidence | Claims | Consent | Resources | Direction | Publication | Frozen audit |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    totals = {key: 0 for key in SHORT}
    for row in sorted(data, key=lambda r: (r["domain"], r["domain_cycle"])):
        for role in ("proposer", "challenger", "verifier"):
            checks = row["roles"][role]["checks"]
            assert set(checks) == set(RULES)
            for check in checks.values():
                totals[check["status"]] += 1
            values = [f'{row["domain"]}/{row["domain_cycle"]}', row["topic"], role]
            values += [SHORT[checks[name]["status"]] for name in RULES]
            values += [f'[{row["audit_release"][:20]}](../../runs/{row["audit_release"]}/verification.md)']
            lines.append("| " + " | ".join(values) + " |")
    assert sum(totals.values()) == 216
    lines += ["", "Exact source checks, reasons, evidence locators and independent limitations are in each linked audit and in runs/GPT-COMPLIANCE-0003/role-compliance-index.json.", "", "## Findings as authored by independent reviewers", ""]
    for row in sorted(data, key=lambda r: (r["domain"], r["domain_cycle"])):
        lines += [f'### {row["domain"]} cycle {row["domain_cycle"]}: {row["compliance_gate"]}', "",
                  "| Finding | Role/rule | Classification/severity | Action | Scientific recheck required |", "|---|---|---|---|---|"]
        for finding in row["findings"]:
            values = [finding["id"], f'{finding["role"]}/{finding["rule"]}',
                      f'{finding["classification"]}/{finding["severity"]}', finding["action"],
                      finding["needs_scientific_adjudication"]]
            lines.append("| " + " | ".join(cell(v) for v in values) + " |")
        if not row["findings"]:
            lines.append("| none reported within scope | — | — | Preserve observability limits | false |")
        lines += ["", "Limits: " + " ".join(cell(x) for x in row["limitations"]), ""]
    incident = json.loads((RUN / "incident-review-request.json").read_text())
    lines += ["## Separately adjudicated prior scope incident", "",
              f'Independent source: [frozen incident review](../../{incident["public_audit"]}). The following findings concern an old quarantined execution, not the current replacement.', "",
              "| Old release | Finding | Independent classification | Reason |", "|---|---|---|---|"]
    for prior in incident["prior_incidents"]:
        for finding in prior["findings"]:
            lines.append("| " + " | ".join(cell(v) for v in (prior["release_id"], finding["id"],
                finding["classification"], finding["reason"])) + " |")
    aborted = json.loads((RUN / "aborted-review-request.json").read_text())
    old_totals = {key: 0 for key in SHORT}
    assert len(aborted["aborted_attempts"]) == 2
    lines += ["", "## Separate metadata-only review of two aborted attempts", "",
              f'Independent source: [final protocol audit](../../{aborted["public_audit"]}). These two rows are excluded from the 24 valid scientific outputs and 216 current rule cells. They contain no valid-cycle or scientific-acceptance credit.', "",
              "| Aborted role | Release | Input | Isolation | Writes | Evidence | Claims | Consent | Resources | Direction | Publication |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for attempt in aborted["aborted_attempts"]:
        checks = attempt["checks"]
        assert set(checks) == set(RULES)
        for check in checks.values():
            old_totals[check["status"]] += 1
        values = [attempt["role"], attempt["release_id"]]
        values += [SHORT[checks[name]["status"]] for name in RULES]
        lines.append("| " + " | ".join(cell(v) for v in values) + " |")
    assert sum(old_totals.values()) == 18
    lines += ["", "Only original JOB/prompt, self-ledger, manifest and same-author prior manifest metadata were supplied. Raw quarantined science and private traces were excluded. Candid extra frozen-proposal reads and a malformed enum support the old challenger deviations; ambiguity in the coordinator's shared-input instructions remains material. Deliberate evasion or exposure of foreign private content is not established. Other unknown coverage remains U; the final audit therefore retains an overall unresolved disposition despite nonblocking current-role findings.", ""]
    for attempt in aborted["aborted_attempts"]:
        lines += [f'Limits for old {attempt["role"]}: ' + " ".join(cell(v) for v in attempt["limitations"]), ""]
    lines += ["", "## Evidence bounds and retained attempts", "",
              "Two late PR67 source-locator/analytical-reproducibility comments arrived after the final frozen audit. See public-review-followups.json for exact public comment IDs, bodies and hashes. They remain open and unadjudicated; neither the 216 original cells nor scientific releases are rewritten. N within the original supplied scope is not a dismissal of new evidence. Publication-byte checks do not confer scientific clearance, and no fifth cycle or experiment follows.", "",
              "See the Chinese final report for the research outcome and the adjudicated coordinator incident. quarantine-incidents.json retains the invalid partial cycle; mechanical-rejections.json retains format failures; audit-corrections.json retains the original and corrected presentation. The current clean cycle does not silently inherit the invalid cycle's conclusions or consent.", "",
              "All execution uses logical separation on a shared OS account. Frozen released bytes, exact public job descriptors and candid self-ledgers are inspectable evidence, not complete OS/network/tool traces. Independent backend-model identity, hidden reads/writes and adversarial confinement are not certified. The protocol auditor's own ledger is checked mechanically; this is not an infinite independent audit chain.", ""]
    out = ROOT / "reports/final/GPT-COMPLIANCE-0003.conduct.en.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    (RUN / "conduct-counts.json").write_text(json.dumps({"scientific_role_rows": 24, "rule_cells": 216,
        "cell_status_counts": totals, "aborted_metadata_only": {"role_rows": 2, "rule_cells": 18,
            "cell_status_counts": old_totals, "excluded_from_valid_cycle_counts": True},
        "overall_unresolved_audits": [r["audit_release"] for r in data if r["compliance_gate"] == "unresolved"],
        "scope": "Counts transcribe independent reviewer cells; a deviation is not necessarily material contamination. N is evidence-bounded and does not certify hidden actions."}, indent=2) + "\n")
    print(out)


if __name__ == "__main__":
    main()
