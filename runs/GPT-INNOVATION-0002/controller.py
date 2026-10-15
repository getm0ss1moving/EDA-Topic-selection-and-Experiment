#!/usr/bin/env python3
"""Public coordinator metadata audit. Never read role scratch or transcripts."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("loop", ROOT / "scripts/codex_loop.py")
loop = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop)
RUN = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-job")
    parser.add_argument("--agent")
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    config, home = loop.config(ROOT / "config/codex-innovation-research.json")
    state = loop.read(home / "state.json")
    dispatch_path = RUN / "dispatches.json"
    dispatches = loop.read(dispatch_path) if dispatch_path.exists() else []
    if args.record_job:
        if not args.agent:
            parser.error("--agent is required with --record-job")
        work = Path(args.record_job)
        job = loop.read(work / "JOB.json")
        if not any(x["work"] == str(work) for x in dispatches):
            dispatches.append({
                "agent": args.agent, "work": str(work), "topic": job["topic"],
                "domain": job["domain"], "cycle": job["batch_round"], "role": job["role"],
                "requested": job["models"][job["role"]], "fork_turns": "none",
                "logical_session": job["session_id"],
                "note": "Coordinator records successful app dispatch; no backend identity attestation."
            })
        loop.save(dispatch_path, dispatches)
    counts = {d: sum(t["round"] for t in state["topics"].values() if t["domain"] == d)
              for d in ("D04", "D05")}
    packets, releases, jobs, domains, index = [], [], {}, {}, []
    for topic, entry in state["topics"].items():
        domains.setdefault(entry["domain"], []).append({
            "topic": topic, "cycles": entry["round"], "status": entry["status"],
            "phase": entry["phase"], "last_scientific_decision": entry.get("last_scientific_decision")
        })
        for role, seat in entry["seats"].items():
            loop.verify_packet(seat)
            dest = RUN / "inputs" / topic / role / "PACKET.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path(seat["packet"]) / "PACKET.json", dest)
            packets.append({"topic": topic, "role": role, "session_id": seat["session_id"],
                            "packet_sha256": seat["packet_sha256"]})
        for name in entry["history"]:
            path = Path(name)
            manifest, payload = loop.rs.verify(path)
            releases.append({"release_id": path.name, "topic": topic, "role": manifest["role"],
                             "session_id": manifest["session_id"], "file_count": len(payload),
                             "submission_manifest_sha256": loop.sha(path / "SUBMISSION.json")})
            jobs[str(path.parent.parent)] = None
        if entry.get("job"):
            jobs[entry["job"]["work"]] = None
    seen = {"D04": 0, "D05": 0}
    for record in state["publication_queue"]:
        topic = state["topics"][record["topic"]]
        entry = {**topic, "latest": record["releases"]}
        for role, name in record["releases"].items():
            work = Path(name).parent.parent
            loop.validate_result(state, entry, {"role": role, "work": str(work)},
                                 loop.read(work / "result.json"))
        domain = topic["domain"]
        seen[domain] += 1
        index.append({"domain": domain, "domain_cycle": seen[domain], "topic": record["topic"],
                      "topic_round": record["round"], "decision": record["decision"],
                      "pr": state["published"].get(record["verification_release"]),
                      "releases": {r: Path(p).name for r, p in record["releases"].items()}})
    job_records = []
    for name in jobs:
        work = Path(name)
        job = loop.read(work / "JOB.json")
        dest = RUN / "inputs" / job["topic"] / f"cycle-{job['batch_round']}-{job['role']}"
        dest.mkdir(parents=True, exist_ok=True)
        for filename in ("JOB.json", "prompt.txt"):
            shutil.copyfile(work / filename, dest / filename)
        job_records.append({"topic": job["topic"], "domain": job["domain"], "role": job["role"],
                            "cycle": job["batch_round"], "requested": job["models"][job["role"]],
                            "job_sha256": loop.sha(work / "JOB.json"),
                            "prompt_sha256": loop.sha(work / "prompt.txt")})
    if args.final:
        assert counts == {"D04": 4, "D05": 4}, counts
        assert all(not t.get("job") for t in state["topics"].values())
        assert len(index) == len(state["published"]) == len(state.get("merged", [])) == 8
        assert len(releases) == len(job_records) == 24
    loop.save(RUN / "topic-index.json", index)
    loop.save(RUN / "progress.json", {"domains": domains, "completed_cycles": counts,
                                    "published": state["published"], "merged": state.get("merged", [])})
    loop.save(RUN / "release-audit.json", {
        "status": "bounded_batch_complete" if args.final else "in_progress",
        "input_commit": state["source_commit"], "completed_cycles": counts,
        "completed_rounds": len(index), "logical_seats": packets, "jobs": job_records,
        "verified_releases": releases, "published": state["published"],
        "merged": state.get("merged", []),
        "coordinator_script_sha256_at_audit": loop.sha(ROOT / "scripts/codex_loop.py"),
        "scope": "Released bytes and coordinator metadata; not scientific truth or OS confinement.",
        "snapshot_note": "Hashes reflect this audit; requested models are not independently attested."
    })
    print(json.dumps({"cycles": counts, "hash_valid_releases": len(releases),
                      "published_rounds": len(state["published"]),
                      "merged_rounds": len(state.get("merged", []))}, indent=2))


if __name__ == "__main__":
    main()
