# Physical implementation pilot

## Scope and resource contract

Only D04 (floorplan, placement, CTS, routing) and D05 (extraction, STA, signoff methodology) are active. Keep one proposer/challenger pair per territory and one shared verifier; do not multiply sessions per flow stage. Existing archived tasks retain their history. All platforms follow this scope, including future DeepSeek/Claude dispatches; their externally running sessions must be paused by their own coordinator. This repository update does not assert control over another platform's runtime.

`config/research-brief.json` distinguishes measured local capability from provisional caps and acceptance thresholds. The local host has 10 logical CPUs and 16 GiB RAM. The pilot defaults to one two-CPU, 4 GiB container at a time, eight CPU-hours total, no GPU or paid API allocation. These are conservative coordinator choices, not a claim that the user supplied a budget. The two-week planning horizon is provisional. Stop experiments at the cap; do not acquire paid infrastructure.

## Reproduction

The available arm64 OpenLane image is pinned by digest, and public OpenROAD test assets are pinned by commit and SHA-256 in `config/physical-resources.lock.json`. Nangate45 is a research library/technology fixture, not evidence of access to a production foundry PDK. The smoke uses a synthesized GCD netlist, typical corner, fixed upstream SDC and die/core geometry.

```sh
python3 scripts/physical_smoke.py --out /absolute/new/external/eda-gcd-smoke
```

The script fetches about 7 MB of public data, checks every checksum, runs without container network access, enforces a ten-minute timeout, and requires expected outputs plus absence of Tcl error lines. The image must already be available or be pulled separately. The initial unmodified flow failed because the image lacked `getconf`; the recorded single-line patch fixes router threads to two. Docker CPU/memory limits also apply. Upstream license notices remain in downloaded files; assets are not vendored into this repository.

`runs/PHYSICAL-PILOT-0001` contains the actual successful flow log, metrics and output hashes. Setup WNS -0.054 ns and TNS -0.880 ns mean **timing is not closed**. An empty router DRC report is not independent DRC/LVS or certified signoff. Flow completion establishes only a reproducible tool/data path.

## Bounded next research round

1. Replace historical onboarding packets with new frozen, role-specific packets from the reviewed configuration. Do not modify old packet contents or their hashes.
2. Each proposer selects at most one opportunity in its active territory. Search primary papers, contest statements and winner reports, open implementations and public commercial material; record query/date/source/locator and nearest competing mechanism. Contest-provided ideas are baseline knowledge, not novelty.
3. The challenger first commits an independent search and effect estimate, then receives the released proposal without its forecast. Assess duplicate mechanisms, actual downstream metrics, theoretical bounds under their stated assumptions, implementation costs and negative controls.
4. The verifier checks source identity, exact locator, entailment and applicability. Escalate mathematical novelty or contested engineering assumptions to an independent expert; lightweight verification must not imply expert consensus. Release only adjudicated objections to the proposer.
5. Before any experiment claims feasibility, acquire representative benchmarks: at least three independent designs; macro-containing designs for floorplanning; additional corners and an explicitly qualified reference oracle for signoff claims. Reproduce strongest accessible baselines under equal resource constraints. GCD cannot satisfy this requirement.
6. Preregister metric, smallest meaningful effect, guardrails, seeds/splits, failure accounting, ablations and stop rule. The current numerical thresholds are pilot screening choices awaiting baseline variance and practitioner feedback. Forecasts must include assumptions and failure scenarios; they are never measurements.
7. Submit proposal, challenge, response and verification changes through PRs. No accepted-topic promotion without both scientific checks and exact-head independent GitHub confirmation.

## Runtime independence

The 21 original tasks were created without conversation forks. Memory mode was initially enabled; it was subsequently disabled through the Codex app-server API, and each worktree received `[memories] use_memories=false, generate_memories=false`. This does not prove earlier context was absent. No scientific verdict from onboarding is accepted. If an actor reports contamination, replace it with a fresh packet-only session. Worktree separation and file rules are not an OS sandbox.

Five assignments remain in scope; some failed on subscription quota. No automatic retries or model downgrades are scheduled. The coordinator reads released files and metadata only, never private transcripts or hidden reasoning.

## Independent GitHub review

`M0nitor-EDA` (GitHub user ID 341092537) is enrolled in `VERIFIER_LOGINS`. A write collaborator invitation was sent (invitation 337230623); acceptance and actual review remain pending. Write access supports GitHub's required review mechanism; no admin access was requested. This account is distinct from the PR author `getm0ss1moving`, but its scientific verifier session must still be bound to a file-based run and evidence record. A name in the allowlist is not an approval.

After accepting the repository invitation, the reviewer examines the final diff and submits an APPROVE review with exactly `CONFIRM <full current head SHA>`. Any subsequent push requires a new confirmation. Never use the author's token to impersonate this account. PR #2's confirmation gate has been rerun with the registered identity and still requires a genuine review. PR #1, #3 and #2 form a stacked sequence; rebase/retarget and recheck each current head as preceding changes land.

Reviewer identity correction: the user corrected the earlier username to `M0nitor-EDA`. The invitation to the unrelated `M0nitor` account was revoked and that login removed from the allowlist. Separate GitHub accounts satisfy account separation only; independent scientific review still requires a distinct verifier session and evidence record, even when both accounts belong to the same human.
