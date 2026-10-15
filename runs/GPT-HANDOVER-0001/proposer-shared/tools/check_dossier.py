"""Consistency checks for an EDA dossier directory (structure only, not science)."""
import csv
import json
import os
import re
import sys

d = sys.argv[1]
problems = []

json_files = ["dossier.json", "direction-control.json", "experiment-consensus.json",
              "forecast.json", "sources.json"]
data = {}
for name in json_files:
    try:
        with open(os.path.join(d, name)) as f:
            data[name] = json.load(f)
    except Exception as e:
        problems.append(f"{name}: JSON error {e}")

sources = data.get("sources.json", [])
src_ids = [s["id"] for s in sources]
if len(src_ids) != len(set(src_ids)):
    problems.append("duplicate source ids")
required = ["id", "title", "url", "type", "published", "retrieved", "locator",
            "access", "claims", "limitations", "version", "license"]
date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ts_re = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
for s in sources:
    for k in required:
        if k not in s:
            problems.append(f"{s.get('id')}: missing {k}")
    if s.get("access") not in ("full", "abstract", "metadata"):
        problems.append(f"{s['id']}: bad access {s.get('access')}")
    if s.get("published") != "unknown" and not date_re.match(s.get("published", "")):
        problems.append(f"{s['id']}: bad published {s.get('published')}")
    if not ts_re.match(s.get("retrieved", "")):
        problems.append(f"{s['id']}: bad retrieved {s.get('retrieved')}")

with open(os.path.join(d, "proposal.md")) as f:
    proposal = f.read()
ledger_claims = set(re.findall(r"^\| (CLM-\d{3}) \|", proposal, re.M))
source_claims = {c for s in sources for c in s.get("claims", [])}
for c in sorted(source_claims - ledger_claims):
    problems.append(f"claim {c} cited by sources but absent from ledger")
for c in sorted(ledger_claims - source_claims):
    print(f"note: ledger claim {c} has no sources.json back-reference")

referenced = set()
for name in os.listdir(d):
    if name.endswith((".md", ".csv", ".json")):
        with open(os.path.join(d, name)) as f:
            referenced |= set(re.findall(r"SRC-\d{3}", f.read()))
for r in sorted(referenced - set(src_ids)):
    problems.append(f"referenced {r} not defined in sources.json")
for s in sorted(set(src_ids) - referenced - set(src_ids)):
    pass

with open(os.path.join(d, "prior-art.csv"), newline="") as f:
    rows = list(csv.reader(f))
header = rows[0]
if header != ["source_id", "task", "mechanism", "data", "evaluation", "assumptions",
              "limitation", "overlap", "distinction"]:
    problems.append(f"prior-art.csv header {header}")
for i, row in enumerate(rows[1:], 2):
    if len(row) != len(header):
        problems.append(f"prior-art.csv line {i}: {len(row)} fields")
    elif row[0] not in src_ids:
        problems.append(f"prior-art.csv line {i}: unknown {row[0]}")

dc = data.get("direction-control.json", {})
pen = dc.get("penalties", {})
if pen.get("total") != pen.get("combination_drift", {}).get("score", -1) + pen.get("demand_drift", {}).get("score", -1):
    problems.append("penalty total mismatch")

print(f"sources: {len(src_ids)}; ledger claims: {len(ledger_claims)}; prior-art rows: {len(rows) - 1}")
print("PROBLEMS:" if problems else "no problems found")
for p in problems:
    print(" -", p)
