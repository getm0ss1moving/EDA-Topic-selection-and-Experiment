# Governance Review — PR3 Snapshot

**Verdict: REVISE before merge.** The snapshot has strong explicit scope/resource caveats, useful packet-filter tests, and passing unit tests. It inherits the fresh-checkout validator crash found in PR1. In addition, its physical smoke result is described as reproducible evidence, but the cited run manifest and artifacts are absent from this frozen packet; that result remains unverified here.

## Identity and provenance

- Role: `Codex-V02-PHYSICAL`, governance verifier; review scope is infrastructure only.
- Reviewed commit: `38fdcf02b1eed6a53fc27224cd209c6b4ba63c0c`.
- `PACKET.json` SHA-256: `f983336b59b7c85d84da1221a1d30cc4a68c0f64a90c8d2617bebc6cff11f0d4` (matches assignment).
- All 51 file hashes listed in `PACKET.json` matched; no mismatches.
- No public-source browsing, network calls, Docker run, EDA run, GitHub API access, or other-task inspection was performed. The packet and this report are the evidence boundary.

## Findings

### PR3-1 — High: documented validation command crashes on a clean checkout

`README.md:10-12` and `.github/workflows/structure.yml:13-17` invoke the repository validator. `scripts/project.py:114-122` unconditionally iterates `candidates`, `topics`, and `archive`; these empty directories are absent from the frozen snapshot. `init` creates only `candidates` (`scripts/project.py:188-194`). The exact scratch reproduction exited 1 with `FileNotFoundError` for `candidates`; creating the three empty directories in scratch made it pass. Thus a fresh workflow, and a repository after only `init`, can fail CI. Handle absent areas as empty or commit the expected directories, then rerun CI.

### PR3-2 — Medium: cited physical smoke evidence is not in the frozen packet

`docs/PHYSICAL-PILOT.md:17-19` reports a completed flow and says `runs/PHYSICAL-PILOT-0001` contains its log, metrics, and output hashes. The supplied PR3 `PACKET.json` includes only `runs/CODEX-ONBOARD-0001/manifest.json` (and no `runs/PHYSICAL-PILOT-0001/manifest.json` entry); the cited smoke evidence is not available in this snapshot. Accordingly, the claimed successful flow, WNS/TNS values, and output hashes cannot be reproduced or provenance-checked from this packet. Add a run manifest with exact input commit, command, image/data hashes, patch, result paths and artifact hashes (or revise the claim to identify an accessible immutable evidence location). This finding means “unverified from supplied snapshot,” not that the run did not occur.

### PR3-3 — Medium, deployment evidence unavailable: live GitHub gate state

`docs/GITHUB.md:5-15` and `docs/PHYSICAL-PILOT.md:37-43` describe the exact-head review process and say invitation/actual review remain pending. This packet cannot establish current branch protection, required-check settings, Actions variable contents, invitation acceptance, or a successful independent review. The workflow source is API-only and statically checks a trusted reviewer, author separation, current head and exact confirmation; deployment enforcement must still be evidenced externally before merge.

## Scope, resources, model, and admission policy

- `docs/PHYSICAL-PILOT.md:5` and `config/research-brief.json:2` consistently limit the pilot to D04/D05; D06 is outside this pilot. The V02 record in `config/agents.json:485-501` also lists D04/D05. `docs/TEAM.md:7,26-28` aligns with that bounded assignment.
- `config/research-brief.json:9-25` clearly labels the two-week horizon and CPU/GPU/memory/API caps as coordinator-selected provisional limits, not user commitments. It specifies one two-CPU/4-GiB job, eight CPU-hours, no GPU or paid API allocation, and states remote resources are absent. `docs/PHYSICAL-PILOT.md:7` repeats the caveat. The stated 10-CPU/16-GiB local host capability is not accompanied by a machine capture in this packet; treat it as a configuration assertion, not independently verified fact.
- The pinned OpenROAD commit and per-file SHA-256/byte manifest in `config/physical-resources.lock.json` provide a reproducible input lock. `config/research-brief.json:44-65` correctly limits Nangate45 to research use and disclaims production PDK, silicon signoff, multi-corner, and commercial-tool parity.
- Provisional D04/D05 metrics and thresholds are labeled as screening choices in `config/research-brief.json:68-82`; the plan requires multiple designs, paired seeds, uncertainty and baseline variance. `docs/PHYSICAL-PILOT.md:27-29` explicitly says GCD alone is insufficient and sets representative-design, macro-design, corner/oracle, equal-budget baseline and preregistration requirements. These are sound controls, not scientific acceptance.
- Model settings in `config/agents.json:4,158-256,485-501` match the documented requested allocation in `docs/TEAM.md:11-17`. Quota failures are recorded, and `docs/PHYSICAL-PILOT.md:35` says no silent downgrade or automatic retry. The registry is a file record, not technical enforcement; actual runtime settings cannot be proven by this packet alone.

## Checks and gate assessment

- `python3 -m unittest discover -s tests -v` in a writable private scratch copy: **16 tests passed**, including `tests/test_actor_packet.py`'s role/domain allowlist and exclusion checks.
- `python3 scripts/project.py validate` in the unmodified scratch copy: **failed** due to the missing dossier area; with all three empty areas created in scratch: **passed**.
- Static review of `scripts/actor_packet.py:10-63`: explicit common allowlist, role-only harness, assigned-domain briefs, full commit pin, blob/mode checks, content hashes, read-only packet output, and exclusion of roster/private paths. `docs/ISOLATION.md:5,16,20-26` correctly states that filtering and file permissions do not create an OS sandbox and requires an actual container/account for enforced isolation.
- Static review of `.github/workflows/independent-verifier.yml:20-46`: pinned action, API-only execution, fail-closed allowlist, author separation, exact-current-SHA approval and draft/blocking-review checks. Actual GitHub settings and identity enrollment remain outside the packet.
- `scripts/physical_smoke.py` was not run: it downloads files and invokes Docker/OpenROAD. Offline governance tests do not validate a physical EDA run. No scientific admission verdict is made.

## Limitations and follow-up

The findings are limited to the two supplied frozen packets; no repository history, live PR, live branch protection, credentials, other task, or external system was inspected. The audit neither repairs findings nor confirms an account identity. File-policy/worktree separation is not an enforced OS sandbox. Recheck both exact snapshots after remediation; for PR3 also bind the pilot result to a released run manifest before relying on its reported measurements.
