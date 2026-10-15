# ChatGPT-only automatic research contract

Effective 2026-10-15. This is the current operational contract for all three roles.
It supersedes the platform assignments and manual transport/wake-up steps in older
Claude/DeepSeek launch packets. Historical artifacts are evidence, not active instructions.

## Objective and role seats

Run `proposal -> challenger -> verifier -> proposal` without a human reminder.
Every substantive round includes all three roles. Freeze and transport happen as
part of finishing a role turn; GitHub publication follows every verifier turn.
A verifier-only diagnostic is not a completed three-role research round.

| Role | Active identity pattern | Requested model | Effort | Responsibility |
|---|---|---|---|---|
| Proposer | ChatGPT-P04-PHYSICAL / ChatGPT-P05-TIMING | gpt-6-astra | high | Survey a bounded area; propose and revise a causal mechanism; produce the executable task list |
| Challenger | ChatGPT-C04-PHYSICAL / ChatGPT-C05-TIMING | gpt-6-astra | low | Independently search papers, implementations and contests; test novelty, usefulness, headroom and feasibility |
| Verifier | ChatGPT-V04-PHYSICAL / ChatGPT-V05-TIMING | gpt-6-luna | medium | Reopen evidence; adjudicate all objections and critical positive claims; validate consent and outcome |

These are requested configurations, not observed model-availability assertions.
No unavailable model may silently fall back to another model or provider.
The existing ChatGPT login is used by native Codex CLI; no Claude/DeepSeek gateway
or paid API key is needed by this runner. All research artifacts are English.

Separate logical role sessions are registered before the first job. Each job uses
a fresh ephemeral native Codex execution and receives its own previous released
output plus explicitly released shared files. A logical seat UUID is not the
Codex CLI's physical thread ID. Independence comes from restricted input exposure
and evidence work, not different provider names. Shared-account restrictions are
policy isolation; they are not adversarial filesystem confinement.

## Small set of retained rules

1. Roles read accessible external research sources independently, without approval.
   Preserve actual access limits; a paywall is not evidence of novelty.
2. Never read another role's private notes, scratch, conversations, memory, runtime
   log or unpublished outputs. Use only the job's released shared files and your own files.
3. Sources must be traceable. Separate facts, inferences, hypotheses and forecasts.
   A challenger cannot turn an assertion into a verdict; the verifier checks it.
4. Only adjudicated challenger releases reach the proposer. The verifier rules on
   every OBJ ID in an included release, including explicit unresolved outcomes.
5. Preserve the problem, causal mechanism and engineering demand. Keep the two
   direction-drift penalties. A trivial composition or demand-free pivot cannot
   rescue a topic under the same ID.
6. The proposer and challenger independently sign the same frozen proposal and
   task-list hash before selection for a pilot. Joint abandonment needs their
   matching signatures and a verifier check of the evidence.
7. Retain released negative results, budgets, licenses and correctness controls.
   Research autonomy does not invent compute, paid access or measured results.

Removed administrative dependencies: human freezing, per-source permission,
manual session-ID entry, a separate registry PR before every output, human
round-by-round wake-up, cross-platform coordinators, manual forecast-screen
release, required reviewer-account approval for automatic research decisions,
and a mandatory human arbitration step after three unsuccessful rounds.
First-pass Codex review is explicitly unblinded. Make an independent assessment
and log forecast exposure; do not claim a blinded experiment.

## Proposer turn

Read the brief and released historical seed if supplied. A legacy seed belongs to
its original author; recheck it and do not inherit that author's signature,
verification or feasibility status. Search classical methods, AI methods, contest
rules, supplied hints, winner reports, current implementations and public industry
capabilities. Identify the engineering user, downstream metric, nearest mechanisms,
real residual gap, assumptions and decisive falsification experiment.

Write every required proposer file, including `tasklist.md`, direction control and
forecast. On a returned verified challenge, address each verdict, revise the
coupled artifacts and rescore drift. Choose one of: improve the anchored mechanism,
request experiment consensus, propose supported abandonment, or state a specific
unresolved prerequisite. Never wait for a raw challenge or human freeze.

## Challenger turn

The job provides the current immutable proposer release. Inspect its actual cited
papers and contests; also run your own wider search. Expand terminology, forward
and backward citations, current venue proceedings, public code/issue history,
contest editions, tracks, statements, organizer baselines and winner reports.
A bibliography copied from the proposer is not independent review.

Explicitly assess duplication/equivalence, mechanism novelty, composition value,
engineering demand, open/commercial comparability, applicable theoretical headroom,
contest-supplied ideas, experiment execution and full resource cost. Use
`workflow.json.coverage` to state supported, unresolved or not applicable for each.

Every OBJ identifies the exact claim, original source locator, applicability,
reasoning, severity, uncertainty, reversal condition and cheapest decisive test.
Do not manufacture objections. The overall assessment is `revise`,
`not_meaningful`, `feasible`, or `unresolved`; `not_meaningful` is a recommendation
with evidence, never a unilateral veto. `feasible` means no supported blocking
issue was found in the checked plan, not proof of universal novelty or success.
Supply falsification tasks and sign only your own consent.

## Verifier turn

Wait for the matching proposal and challenge pair; the scheduler does this.
Reopen decision-critical original sources and check locators, chronology,
applicability and entailment. Check favorable claims as carefully as criticisms.
Use a compact table: `claim/OBJ | source + locator | verdict | blocking | action`.
The five objection verdicts remain valid, partially_valid, unsupported, refuted,
unresolved. Keep the JSON and table consistent. Unread evidence is unresolved.

In `verification.json`, name `reviewed_proposer_release` and the exact
`adjudicated_challenger_releases`. Every OBJ in an included challenge must have a
row. A complete ruling can still require revision. The scheduler transports your
ruling and those adjudicated challenge bytes to the proposer automatically.

## Machine outcome and consent

Every new Codex-mode release contains `workflow.json`:

```json
{"role":"challenger","reviewed_proposer_release":"SUB-<64 hex>",
 "assessment":"revise","coverage":{"duplicate_prior_art":"supported",
 "mechanism":"supported","composition":"supported","demand":"unresolved",
 "industry_gap":"unresolved","headroom":"unresolved","contests":"supported",
 "experiments":"supported","cost":"supported"}}
```

The proposer uses `{"role":"proposer"}` plus any concise operational fields.
The verifier uses its role, the same reviewed release, and `next_action` from:
`revise`, `consent_experiment`, `consent_abandonment`, `accept_for_pilot`,
`abandon`, `park`. Scientific reasons stay in the evidence/verdict files.

A consent names an earlier frozen proposer release, never the release containing
the signature itself. The scientific proposer bytes must remain identical to that
target while consents are collected. Each role emits its own `experiment-consent.json`
or `abandonment-consent.json`; the coordinator never generates a vote.
Experiment signatures bind the exact task-list SHA-256. Abandonment signatures
bind the proposer-science digest, computed with the project's digest framing over
all proposer files except workflow and consent files. The verifier checks the
matching signatures and cited evidence. A refused consent returns to revision or
parks; it does not become agreement through a retry.

A task list can bind not-yet-generated input by pinned generation procedure:
source/tool versions, script/config hashes, oracle, output-validation procedure,
resource cap and stop rule. Record actual output hashes when generated. This avoids
a circular demand to run the full experiment before agreeing to its plan.

An invalid or exhausted topic is archived after joint abandonment. A topic still
unresolved after three substantive rounds is parked with its open questions.
A successor receives a new ID and fresh logical seats. Consent-only turns do not
consume substantive rounds. A successor receives only released predecessor
outcomes, negative evidence and resurrection conditions, never private reasoning.
No topic is silently renamed or given inherited acceptance.

## Runtime and publication

The coordinator process, not a role's background wait, drives work:

```sh
python3 scripts/codex_loop.py preflight
python3 scripts/codex_loop.py prepare --ref FULL_COMMIT_SHA
python3 scripts/codex_loop.py watch
```

`prepare` launches no model. `watch` serially runs native `codex exec`, validates
its actor-authored frozen release, transmits it and schedules the next role.
`status` displays durable state. `tick` executes one ready job. Only one coordinator
may hold the lock. Failed or quota-limited turns preserve their own files and
retry after the configured backoff. GitHub failures retain a separate publication
queue; they do not erase research. No role must stay alive while waiting.

Every completed round has one deterministic GitHub branch/PR holding all three
immutable releases and exact logical registrations. Registration is included in
the same PR, eliminating the old registry-before-publish deadlock. The coordinator
merges only its transport PR after required checks pass. No self-approval is used.
Human review is optional for research selection; it remains possible at any time.
New compute or paid access still needs an actual allocation.

A selected-for-pilot runtime outcome is a research decision. Formal `topics/`
promotion must additionally pass the complete dossier validator; runtime state or
a green transport test alone is insufficient. Likewise, actual experiments run
only through the allocated runner. See the gap report for these remaining adapters.

Official runtime reference: [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).
Local CLI help was checked against codex-cli 0.145.0. The code uses the observed
`--ephemeral`, `--ignore-user-config`, `--output-schema`, model and sandbox flags.
Model availability and end-to-end native runtime behavior require an actual test.
