# Runner instructions for Claude-P05-TIMING

The runner is transport infrastructure. Communicate with it only through files. Do not inspect its state directory, SSH account, another actor's workspace or another role's output.

## Submit a job

Create the shell script and any plain-file inputs under:

`/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Outboxes/physical-release-d437c2f66090/Claude-P05-TIMING/lab-requests/`

Then atomically create a request named `REQ-NNNN.json`. Use a new four-digit ID for every attempt:

```json
{
  "id": "REQ-0001",
  "category": "property-check",
  "purpose": "Check P3 boundary cases against pinned dmp_ceff_elmore revision ...",
  "host": "lab234",
  "network": false,
  "cores": 2,
  "timeout_hours": 1.0,
  "script": "REQ-0001.sh",
  "inputs": []
}
```

Allowed categories are `tooling`, `data`, `substrate`, and `property-check`. Use `lab234` unless a GitHub/arXiv download is necessary. Only `lab231` may set `network` to `true`, and every such job must log each public GitHub/arXiv URL, resolved revision and SHA-256. Other download sites are out of scope. Do not submit a hypothesis, performance, QoR or real-design measurement job.

Scripts run with `/ws` as `HOME`. Persist reusable tools under `/ws/tools`, public inputs under `/ws/data`, and outputs for the current request under `out/`. Keep each returned file under 50 MiB and the returned set under 200 MiB. Do not use symlinks as outputs. For a large artifact, leave it in `/ws`, write a small manifest containing its path and hash, and use it in a later job; `result.json` also lists server-retained files.

The runner processes one job at a time. Read results from the read-only folder:

`/Users/duanzeyu/Documents/ChatGPT/EDA-Agent-Inboxes/physical-release-d437c2f66090/Claude-P05-TIMING/lab-results/REQ-NNNN/`

Each result contains `result.json`, log tails and eligible regular outputs. Treat exit code 124 or 137 as a timeout. Do not modify result files. Correct a failed request by submitting a new ID; never overwrite the evidence from an earlier request.

## Required P3-P5 record

For every property, save the pinned source revision, build commands, generated fixtures, exact check command, expected invariant, observed counterexamples and the scope of the conclusion. Label the result as one of: `proved`, `code-argument-only`, `finite-tests-pass`, `falsified`, or `unresolved`. A passing finite test suite is not a proof. If P3-P5 cannot support the certificate without an empirical safety margin, activate K2 and revise or withdraw the guarantee claim rather than converting it into an unlabelled heuristic.

