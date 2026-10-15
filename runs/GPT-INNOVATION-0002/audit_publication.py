#!/usr/bin/env python3
"""Reopen this batch's public bytes and GitHub merge receipts; no private logs."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[1]
SLUG = "getm0ss1moving/EDA-Topic-selection-and-Experiment"
spec = importlib.util.spec_from_file_location("loop", ROOT / "scripts/codex_loop.py")
loop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop)


def command(*args):
    return subprocess.check_output(args, cwd=ROOT, timeout=60)


def receipt(url):
    info = json.loads(command("gh", "pr", "view", url, "--json",
                             "number,url,state,headRefOid,mergeCommit,mergedAt,statusCheckRollup"))
    assert info["state"] == "MERGED", info
    checks = info["statusCheckRollup"]
    assert checks and all(c.get("conclusion") in ("SUCCESS", "NEUTRAL", "SKIPPED")
                          or c.get("state") == "SUCCESS" for c in checks), info
    query = ('query { repository(owner:"getm0ss1moving",name:"EDA-Topic-selection-and-Experiment") '
             '{ pullRequest(number:' + str(info["number"]) + ') { reviewThreads(first:100) '
             '{ nodes { id isResolved } pageInfo { hasNextPage } } } } }')
    threads = json.loads(command("gh", "api", "graphql", "-f", "query=" + query))[
        "data"]["repository"]["pullRequest"]["reviewThreads"]
    assert not threads["pageInfo"]["hasNextPage"]
    unresolved = [t["id"] for t in threads["nodes"] if not t["isResolved"]]
    known = {t["thread_id"] for t in loop.read(RUN / "review-followups.json")["unadjudicated_threads"]}
    assert set(unresolved) <= known, (url, unresolved)
    info["unresolved_review_threads"] = len(unresolved)
    info["unadjudicated_thread_ids"] = unresolved
    return info


def main():
    _, home = loop.config(ROOT / "config/codex-innovation-research.json")
    state = loop.read(home / "state.json")
    assert command("git", "remote", "get-url", "origin").decode().strip() == "https://github.com/" + SLUG + ".git"
    command("git", "fetch", "--quiet", "origin", "main")
    head = command("git", "rev-parse", "origin/main").decode().strip()
    tag = "refs/tags/codex/gpt-innovation-source-20261015"
    source = command("git", "ls-remote", "origin", tag).decode().split()[0]
    assert source == state["source_commit"]
    source_branch = "refs/heads/codex/gpt-innovation-source-20261015"
    assert command("git", "ls-remote", "origin", source_branch).decode().split()[0] == source
    assert command("git", "cat-file", "-t", source).strip() == b"commit"
    urls = list(state["published"].values())
    assert len(urls) == 8
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        receipts = list(pool.map(receipt, urls))
    releases = []
    with tempfile.TemporaryDirectory(prefix="eda-public-audit-") as scratch:
        # macOS /var is a symlink; the trusted verifier requires resolved parents.
        base = Path(scratch).resolve()
        for topic in state["topics"].values():
            for name in topic["history"]:
                original = Path(name)
                dest = base / original.name
                dest.mkdir()
                prefix = "runs/" + original.name + "/"
                names = command("git", "ls-tree", "-r", "--name-only", "origin/main", prefix).decode().splitlines()
                assert names, prefix
                for path in names:
                    mode = command("git", "ls-tree", "origin/main", path).decode().split()[0]
                    assert mode == "100644", (path, mode)
                    data = command("git", "show", "origin/main:" + path)
                    relative = path[len(prefix):]
                    target = dest / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    assert data == (original / relative).read_bytes(), path
                manifest, payload = loop.rs.verify(dest)
                releases.append({"release_id": original.name, "topic": manifest["topic"],
                                 "role": manifest["role"], "payload_files": len(payload),
                                 "manifest_sha256": hashlib.sha256((dest / "SUBMISSION.json").read_bytes()).hexdigest(),
                                 "runtime_bytes_identical": True})
    assert len(releases) == 24
    checked = datetime.now(timezone.utc).isoformat()
    loop.save(RUN / "publication-receipts.json", {
        "checked_at_utc": checked, "round_prs": receipts,
        "scope": "GitHub snapshot: actual merged PRs, head checks, merge commits and review-thread inventory. Documented unadjudicated follow-ups remain open; not independent scientific approval."
    })
    loop.save(RUN / "publication-audit.json", {
        "checked_at_utc": checked, "public_main_commit": head, "source_tag": tag,
        "source_commit": source, "source_branch": source_branch,
        "verified_release_count": len(releases), "releases": releases,
        "scope": "All 24 frozen submissions reopened from public origin/main; all payload and manifest bytes identical to collected runtime releases, regular files only."
    })
    print(json.dumps({"public_main_commit": head, "source_commit": source,
                      "public_byte_identical_releases": len(releases), "merged_prs": len(receipts),
                      "unresolved_review_threads": sum(r["unresolved_review_threads"] for r in receipts)}, indent=2))


if __name__ == "__main__":
    main()
