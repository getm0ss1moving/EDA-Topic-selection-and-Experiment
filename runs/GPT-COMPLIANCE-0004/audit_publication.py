#!/usr/bin/env python3
"""Reopen public batch bytes/assignments and actual GitHub merge receipts."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import time

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
REMOTE = "https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment.git"
spec = importlib.util.spec_from_file_location("loop", ROOT / "scripts/codex_loop.py")
loop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop)


def command(*args, cwd=ROOT):
    # This helper only reads GitHub. Retry transient read failures; never invent
    # a successful receipt or reuse an earlier head in place of a fresh check.
    for attempt in range(3 if args[0] == 'gh' else 1):
        try:
            return subprocess.check_output(args, cwd=cwd, timeout=60)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            if args[0] != 'gh' or attempt == 2:
                raise
            time.sleep(attempt + 1)


def retained_followups():
    path = RUN / 'public-review-followups.json'
    return loop.read(path)['followups'] if path.is_file() else []


def receipt(url):
    captured = RUN / 'connector-github-receipts.json'
    if captured.is_file():
        evidence = loop.read(captured)
        row = evidence['records'][url.rsplit('/', 1)[-1]]
        pr = row['info']
        assert pr['url'] == url and pr['merged'] is True and pr['state'] == 'closed'
        assert row['checked_head'] == pr['head_sha']
        runs = row['workflows']['workflow_runs']
        statuses = row['status']['statuses']
        assert runs and all(x['status'] == 'completed' and x['conclusion'] in ('success','neutral','skipped') for x in runs)
        assert any(x['name'] == 'Research structure' and x['conclusion'] == 'success' for x in runs)
        assert statuses and all(x['state'] == 'success' for x in statuses)
        assert any(x['context'] == 'independent-verifier' for x in statuses)
        info = {'number':pr['number'], 'url':url, 'state':'MERGED',
                'headRefOid':pr['head_sha'], 'mergeCommit':{'oid':pr['merge_commit_sha']},
                'mergedAt':pr['merged_at'], 'workflow_summaries':runs, 'commit_statuses':statuses,
                'receipt_transport':evidence['retrieval_transport'],
                'receipt_recorded_at_utc':evidence['recorded_at_utc'],
                'receipt_scope':evidence['limits']}
        threads = {'nodes':row['threads']['review_threads']}
    else:
        info = json.loads(command("gh", "pr", "view", url, "--json",
                             "number,url,state,headRefOid,mergeCommit,mergedAt,statusCheckRollup"))
        assert info["state"] == "MERGED", info
        checks = info["statusCheckRollup"]
        assert checks and all(c.get("conclusion") in ("SUCCESS", "NEUTRAL", "SKIPPED")
                          or c.get("state") == "SUCCESS" for c in checks), info
        query = ('query { repository(owner:"getm0ss1moving",name:"EDA-Topic-selection-and-Experiment") '
             '{ pullRequest(number:' + str(info["number"]) + ') { reviewThreads(first:100) '
             '{ nodes { id isResolved comments(first:100) { nodes { id body } '
             'pageInfo { hasNextPage } } } pageInfo { hasNextPage } } } } }')
        threads = json.loads(command("gh", "api", "graphql", "-f", "query=" + query))[
        "data"]["repository"]["pullRequest"]["reviewThreads"]
        assert not threads["pageInfo"]["hasNextPage"]
    unresolved = [t for t in threads["nodes"] if not t.get('isResolved',t.get('is_resolved'))]
    # Do not turn late scientific allegations into coordinator verdicts or silently
    # hide them to obtain a clean receipt. Permit only the exact publicly retained
    # unresolved allegations, including their comment identities and body hashes.
    retained = retained_followups()
    declared = {r["thread_id"]: r for r in retained if r["pr"] == url}
    for thread in unresolved:
        assert thread["id"] in declared, (url, thread["id"])
        if isinstance(thread['comments'],dict):
            assert not thread["comments"]["pageInfo"]["hasNextPage"]
        expected = declared[thread["id"]]
        assert expected["status"] in {"unadjudicated_scientific_followup", "independently_adjudicated_historical_followup", "governance_fix_ready_for_report_publication"}
        if expected['status'] == 'governance_fix_ready_for_report_publication':
            assert expected.get('fix_paths') and all((ROOT / p).is_file() for p in expected['fix_paths'])
        if expected['status'] == 'independently_adjudicated_historical_followup':
            assert expected.get('scientific_ruling') and expected.get('ruling_id')
            assert expected.get('verdict') in {'valid','partially_valid','unsupported','refuted','unresolved'}
        comments = thread['comments']['nodes'] if isinstance(thread['comments'],dict) else thread['comments']
        actual = {c["id"]: hashlib.sha256(c["body"].encode()).hexdigest() for c in comments}
        assert actual == {c["id"]: c["body_sha256"] for c in expected["comments"]}
    assert {t["id"] for t in unresolved} == set(declared)
    info["unresolved_review_threads"] = [t["id"] for t in unresolved]
    info["retained_scientific_followups"] = list(declared.values())
    return info


def main():
    _, home = loop.config(ROOT / "config/codex-compliance-research-0004.json")
    state = loop.read(home / "state.json")
    urls = list(state["published"].values())
    assert len(urls) == len(state["merged"]) == 8
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        receipts = list(pool.map(receipt, urls))
    incident_receipt = None
    incident = loop.read(RUN / 'incident-review.json') if (RUN / 'incident-review.json').exists() else None
    incident_fix_receipt = None
    authority_fix_receipt = None
    presence_fix_receipt = None
    if (RUN / 'scientific-authority-fix.json').exists():
        authority_fix_receipt = receipt(loop.read(RUN / 'scientific-authority-fix.json')['pr'])
    if (RUN / 'public-evidence-presence-fix.json').exists():
        presence_fix_receipt = receipt(loop.read(RUN / 'public-evidence-presence-fix.json')['pr'])
    if incident and incident.get('audit_release'):
        incident_receipt = receipt(loop.read(RUN / 'incident-publication.json')['pr'])
        if (RUN / 'incident-descriptor-fix.json').exists():
            incident_fix_receipt = receipt(loop.read(RUN / 'incident-descriptor-fix.json')['pr'])
    snapshots = {}
    for record in state["publication_queue"]:
        for name in list(record["releases"].values()) + [record["compliance_audit"]] + record.get("mechanical_releases", []):
            snapshots[Path(name).name] = Path(name)
    if incident and incident.get('audit_release'):
        for name in incident['releases'].values():
            snapshots[Path(name).name] = Path(name)
        work = Path(incident['work'])
        snapshots[incident['audit_release']] = work / 'submissions' / incident['audit_release']
    # Corrections preserve their original immutable snapshots as well.
    for row in (loop.read(RUN / "audit-corrections.json") if (RUN / "audit-corrections.json").exists() else []):
        candidates = list((home / "audits").glob("*/jobs/*/submissions/" + row["old_audit"]))
        assert len(candidates) == 1, row
        snapshots[row["old_audit"]] = candidates[0]
    release_rows, descriptor_rows, incident_descriptor_rows = [], [], []
    with tempfile.TemporaryDirectory(prefix="eda-public-compliance-audit-") as scratch:
        repo = Path(scratch).resolve() / "repo"
        command("git", "clone", "--quiet", REMOTE, str(repo))
        head = command("git", "rev-parse", "HEAD", cwd=repo).decode().strip()
        source = state["source_commit"]
        for ref in ("refs/tags/codex/gpt-compliance-source-20261016",
                    "refs/heads/codex/gpt-compliance-source-20261016"):
            assert command("git", "ls-remote", "origin", ref, cwd=repo).decode().split()[0] == source
        assert command("git", "cat-file", "-t", source, cwd=repo).strip() == b"commit"
        command("git", "merge-base", "--is-ancestor", source, "HEAD", cwd=repo)
        for followup in retained_followups():
            if followup['status'] == 'independently_adjudicated_historical_followup':
                verdict = loop.read(repo / followup['scientific_ruling'])
                rows = verdict.get('historical_public_review_adjudications', [])
                row = next(row for row in rows if row['id'] == followup['ruling_id'])
                assert row['verdict'] == followup['verdict']
        for sid, original in snapshots.items():
            public = repo / "runs" / sid
            manifest, payload = loop.rs.verify(public)
            names = set(payload) | {"SUBMISSION.json"}
            assert names == {p.name for p in public.iterdir() if p.is_file()}
            authorities = list((home / "rejected-attempts").glob("*/" + sid))
            assert len(authorities) <= 1
            for name in names:
                assert (public / name).read_bytes() == loop.rs.regular(original / name), (sid, name)
                if authorities:
                    assert (public / name).read_bytes() == loop.rs.regular(authorities[0] / name), (sid, name)
            release_rows.append({"release_id": sid, "role": manifest["role"], "topic": manifest["topic"],
                                 "payload_files": len(payload), "runtime_bytes_identical": True})
        for record in state["publication_queue"]:
            key = record["verification_release"][4:20]
            audit_work = Path(record["compliance_audit"]).parent.parent
            directory = repo / "runs" / f'CODEX-ROUND-{record["topic"]}-{key}'
            public_round = loop.read(directory / "round.json")
            assert public_round["compliance_audit"] == "runs/" + Path(record["compliance_audit"]).name
            descriptors = loop.read(directory / "DESCRIPTORS.json")
            assert set(descriptors["roles"]) == {"proposer", "challenger", "verifier", "protocol_audit"}
            for role, entry in descriptors["roles"].items():
                for name, expected in entry["files"].items():
                    public = repo / entry["root"] / name
                    assert loop.sha(public) == expected, public
                snapshot = snapshots[entry["release_id"]]
                work = snapshot.parent.parent
                for name, original in {"JOB.json": work / "JOB.json", "prompt.txt": work / "prompt.txt",
                                       "PACKET.json": work / "policy/PACKET.json"}.items():
                    assert (repo / entry["root"] / name).read_bytes() == loop.rs.regular(original)
                if "mechanical-attempts.json" in entry["files"]:
                    original = audit_work / "shared/job-descriptors" / role / "mechanical-attempts.json"
                    assert (repo / entry["root"] / "mechanical-attempts.json").read_bytes() == loop.rs.regular(original)
                if 'public-evidence.json' in entry['files']:
                    public = repo / entry['root'] / 'public-evidence.json'
                    assert public.read_bytes() == loop.rs.regular(work / 'public-evidence.json')
                    assignment = loop.read(work / 'JOB.json')
                    assert role == 'verifier' and loop.sha(public) == assignment['public_evidence']['sha256']
                descriptor_rows.append({"topic": record["topic"], "round": record["round"], "role": role,
                                        "release_id": entry["release_id"], "files": entry["files"]})
            supplement = descriptors.get("supplemental_inputs")
            if supplement:
                for name, expected in supplement["files"].items():
                    assert loop.sha(repo / supplement["root"] / name) == expected
                    assert (repo / supplement["root"] / name).read_bytes() == loop.rs.regular(
                        audit_work / "shared/protocol-incident" / name)
        if incident and incident.get('audit_release'):
            descriptors = loop.read(repo / 'runs/GPT-COMPLIANCE-0004/incident-descriptors/DESCRIPTORS.json')
            assert set(descriptors['roles']) == {'proposer', 'challenger', 'verifier', 'protocol_audit'}
            assert descriptors['locator_map']['shared/job-descriptors/'] == 'runs/GPT-COMPLIANCE-0004/incident-descriptors/'
            paths = {**incident['releases'], 'protocol_audit': str(snapshots[incident['audit_release']])}
            for role, original in paths.items():
                work = Path(original).parent.parent
                files = {}
                entry = descriptors['roles'][role]
                assert entry['release_id'] == Path(original).name
                for name, source_path in {'JOB.json': work / 'JOB.json', 'prompt.txt': work / 'prompt.txt',
                                          'PACKET.json': work / 'policy/PACKET.json'}.items():
                    public = repo / 'runs/GPT-COMPLIANCE-0004/incident-descriptors' / role / name
                    assert public.read_bytes() == loop.rs.regular(source_path)
                    files[name] = loop.sha(public)
                    assert files[name] == entry['files'][name]
                incident_descriptor_rows.append({'role': role, 'release_id': Path(original).name, 'files': files})
            supplemental = descriptors['supplemental_inputs']
            for name, expected in supplemental['files'].items():
                public = repo / supplemental['root'] / name
                assert loop.sha(public) == expected
                assert public.read_bytes() == loop.rs.regular(Path(incident['work']) / 'shared' / name)
    assert len(descriptor_rows) == 32
    now = datetime.now(timezone.utc).isoformat()
    loop.save(RUN / "publication-receipts.json", {"checked_at_utc": now, "round_prs": receipts,
        "incident_evidence_pr": incident_receipt,
        "incident_descriptor_fix_pr": incident_fix_receipt,
        "scientific_authority_fix_pr": authority_fix_receipt,
        "public_evidence_presence_fix_pr": presence_fix_receipt,
        "scope": "Actual merged PR heads, checks and review-thread inventory. Exact retained followups retain their recorded scientific status; an open UI thread is not silently dismissed and no coordinator scientific clearance is inferred."})
    loop.save(RUN / "publication-audit.json", {"checked_at_utc": now, "public_main_commit": head,
        "source_commit": source, "fresh_ordinary_public_clone": True,
        "verified_release_count": len(release_rows), "releases": release_rows,
        "descriptor_count": len(descriptor_rows), "descriptors": descriptor_rows,
        "quarantined_attempt_descriptors": incident_descriptor_rows,
        "unresolved_scientific_review_threads": [tid for r in receipts for tid in r["unresolved_review_threads"]],
        "scope": "Frozen manifests/payload and exact public descriptors reopened from ordinary public clone; retained corrections included. No private traces or hidden behavior certification."})
    print(json.dumps({"public_main_commit": head, "verified_releases": len(release_rows),
                      "exact_public_descriptors": len(descriptor_rows), "merged_round_prs": len(receipts)}, indent=2))


if __name__ == "__main__":
    main()
