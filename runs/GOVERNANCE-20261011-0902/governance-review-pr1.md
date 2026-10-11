# Governance Review — PR1 Snapshot

**Verdict: REVISE before merge.** The frozen governance packet is internally hash-consistent and the unit suite passes, but the documented repository validator crashes on the fresh snapshot because expected dossier directories are absent. No scientific topic is reviewed or approved here.

## Identity and provenance

- Role: `Codex-V02-PHYSICAL`, governance verifier; review scope is infrastructure only.
- Reviewed commit: `ac3207ec184c2f156f12e66024dd58199cec35b3`.
- `PACKET.json` SHA-256: `96c6764f99486d8663661e6ab2bb36b711933c60e768026d79a7f9fb9d58ebae` (matches assignment).
- All 39 file hashes listed in `PACKET.json` matched; no mismatches.
- No public-source browsing, network calls, GitHub API access, Docker run, EDA run, or other-task inspection was performed. The packet and this report are the evidence boundary.

## Findings

### PR1-1 — High: documented validation command crashes on a clean checkout

`README.md:10-12` directs contributors to run `python3 scripts/project.py validate`, and `.github/workflows/structure.yml:13-17` invokes it in CI. But `scripts/project.py:114-122` calls `.iterdir()` unconditionally for `candidates`, `topics`, and `archive`. These empty directories are not represented in the frozen packet; `init` creates only `candidates` (`scripts/project.py:188-194`). In a writable scratch copy of this exact packet, `python3 scripts/project.py validate` exited 1 with `FileNotFoundError` for `candidates`. Creating all three empty directories in scratch made it pass. The defect therefore blocks a fresh workflow and remains after a draft is initialized unless the other two directories are created. Fix the validator to treat absent areas as empty, or establish all required directories as tracked content, then rerun CI.

### PR1-2 — Medium, deployment evidence unavailable: live branch protection and verifier enrollment

`docs/GITHUB.md:5-15` describes branch protection, required checks, bypass settings, and the external `VERIFIER_LOGINS` variable. These controls are not included as API snapshots or other evidence in this packet, so their live configuration cannot be confirmed here. `docs/DEPLOYMENT.md:7-9` itself says no independent verifier is enrolled and that merging is intentionally blocked. Treat the deployment gate as unverified/blocked until an operator records the actual settings and a current-head check. This is not a claim that the workflow source is unsafe.

## Checks and gate assessment

- `python3 -m unittest discover -s tests -v` in a writable private scratch copy: **15 tests passed**.
- `python3 scripts/project.py validate` in the unmodified scratch copy: **failed** as described above; after adding empty `candidates/`, `topics/`, and `archive/` directories: **passed**.
- Static review of `.github/workflows/independent-verifier.yml:20-46`: the pinned action uses GitHub API data only, does not check out or execute PR code, allowlists logins, excludes the PR author, binds approval to the current head SHA and exact confirmation body, and blocks drafts or a latest trusted `CHANGES_REQUESTED` review. The workflow fails closed when no verifier is configured. Live branch-protection enforcement remains outside this packet.
- `scripts/project.py` documents at line 2 that its checks are structural, and `docs/GITHUB.md:33` similarly disclaims semantic verification. The human/verifier evidence obligations are therefore policy requirements, not automated scientific guarantees.
- No resource/model policy or experiment claims are admitted by this snapshot; `config/research-brief.json` retains unknown resource constraints.

## Limitations

This review uses the supplied immutable governance packet only. It does not establish live GitHub settings, account enrollment, actual review identity, or scientific validity. File-policy/worktree separation is not an enforced OS sandbox. The approval workflow's event behavior was statically inspected; no live GitHub events were simulated. Recheck the exact changed snapshot after remediation.
