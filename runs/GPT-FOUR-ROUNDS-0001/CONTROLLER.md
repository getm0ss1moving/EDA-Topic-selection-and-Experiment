# Bounded batch controller archive

All eight scientific cycles are complete. No role dispatch is pending or authorized for this batch. The procedure below is an archival checkpoint, not an instruction to restart research; final publication and audit status are in completion.md.

Owner request: inherit the released Claude proposer and DeepSeek verifier work, create GPT successors, run D04 and D05 concurrently for four complete proposer/challenger/verifier cycles per domain, stop, then produce a Chinese topic explanation. Scientific role artifacts remain English. No predecessor transcript/private scratch is permitted.

Runtime state: `/Users/duanzeyu/Documents/ChatGPT/EDA-GPT-Four-Rounds-20261015/state.json`.
Pinned source: `a48f03d4bc254c0b0957d0fe0f265e072d6cf49a` (PR #34 merged as `b946ec3de2ee0c9144e233316621d7e052a682b2`).

Use `python3 scripts/codex_loop.py collect --domain D04|D05` after a role writes its own result.json and immutable submission. Then `dispatch --domain ...` returns the next job path/model. Spawn the assigned model as a fresh `fork_turns=none` app subagent, giving only the job prompt/file paths and privacy rules. Models: proposer `gpt-6.1-sol high`; challenger `gpt-6-astra low`; verifier `gpt-6.1-sol low`. The native CLI explicitly refused 6.1-Sol for this account; do not retry it or substitute a model. App probe passed. Do not inspect a running role's private files/logs.

When a collect operation reports a mechanical error, give that role its own retry-note.json path; let the same scientific author repair/re-freeze. Never rewrite its science or fabricate consent. Each verifier must bind the exact current proposal/challenge and rule on every OBJ ID.

After each verifier collect, run `python3 scripts/codex_loop.py publish-pending`; attach every new PR via the app attachment tool. Required checks must pass before coordinator merge; no self-approval or bypass. Publication errors retain the queue. `merge_checked` now updates a BEHIND branch with a normal base merge. No scientific job may be dispatched after a domain total reaches four. Continue only publication/owner synthesis afterwards.

`dispatches.json` records started app-agent jobs; state.json holds exact latest releases and completed counts. Latest actual app agents and completed release IDs are recorded in `dispatches.json`; current counts and publication URLs are in `progress.json`. Consult app agent status, then collect only finished role output. Do not read private role logs. The root procedural checkpoint updater is `/tmp/eda-controller-journal.py` (metadata only).

The verifier packet contains HANDOVER.md and the two historical release files. Before its first D05 turn, also copy the separately hashed `runs/GPT-HANDOVER-0001/verifier-supplement.json` and the three named files (readiness.json, first-pass-plan.md, gap-analysis.md) into that new job's shared/legacy-verifier directory; list this extra released context in JOB.json. Do not modify the immutable base packet. Legacy R0 verdicts are historical and do not verify the current R1b/GPT revision.

Final work: verify 4/4 completed counts for both domains, no fifth dispatch, all role releases hash-valid, publish all eight rounds (or explicit successor-topic equivalents), inspect final released proposer/challenger/verifier records, and write a Chinese owner topic explanation under reports/final/ identifying mechanism, closest work, value, fatal/unresolved issues, experiment task list and forecast limits. Do not call a topic accepted unless its scientific gates/dual consent actually pass; a bounded four-round stop may end with conditional or unresolved recommendations. Commit/report by PR, validate, attach, and merge after checks. Formal canonical topics/ promotion remains an adapter gap unless completed separately. Private runtime logs must never be published.

Current uncommitted coordinator-only changes: merge_checked handles BEHIND; nested model policy corrected; three additional owner-released verifier handover files and their manifest copied; launch/dispatch checkpoint files created. Keep unrelated node_modules and yarn.lock unstaged. Final transport/report PR may include these changes. Do not reset any actor state.


Owner scope clarification is recorded in SCOPE.md and all new job prompts: public/legitimately accessible chip EDA academic research, no cyber intrusion, trade-secret acquisition or access-control bypass. Native GitHub and connector requests have shown TLS/transport failures; publication queue and pushed orphan branches are preserved. The coordinator now reports validation errors, includes required transport login metadata, records publication/merge errors durably, and reuses an orphan branch only if its patch/files match the intended record. Do not force-push or bypass TLS checks.

PR #40 needed a normal conflict resolution in `config/roles.json` after parallel publications: the coordinator took the union of distinct session IDs and asserted identical bytes for any duplicate ID and identical non-session metadata. All 16 pre-existing/current registrations were retained; no scientific output was edited. A racing GitHub base-update commit was fetched and merged normally rather than force-pushed. Structural validation passed after reconciliation.
