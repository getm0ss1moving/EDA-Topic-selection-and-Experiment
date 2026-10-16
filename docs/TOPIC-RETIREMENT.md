# Adversarial screening and automatic topic retirement

Current human-led scope: proposer/reviewed_proposer_release names the author input
slot in the historical wire format, not an AI proposer. A new human-authored
revision is needed for each distinct attempt. No replacement topic is generated
automatically. The pure scoring code and legacy loop tests are available, but
the historical P/C/V execution launcher is disabled; do not claim a live human-idea
dispatcher from these tests. Apply a bound certificate to a frozen review pair
before recording retirement. Preserve legacy schemas and evidence.

Owner instruction, 2026-10-16: challenge proposals more sharply, especially their
rationale and innovation, and automatically discontinue weak topics at explicit
thresholds. This policy applies only when a NEW job has a hash-bound
`JOB.json.retirement_policy`. New prepare operations enable it by default when the frozen source contains
the policy, including a new run copied from an older configuration. An explicit
retirement_policy:false opts out for a deliberately recorded legacy/test run;
an old source snapshot without the policy retains legacy behavior. Never rescore old releases, modify a running packet or restart a
completed batch merely to apply this policy. Existing runtime states without this binding retain their old behavior.

## What sharper review means

The challenger is a skeptical research investment reviewer. Put the strongest
reason to stop first. Do not settle for wording, formatting, missing-permission
or generic implementation complaints while the causal and novelty questions
remain untouched. Ask whether the proposed paper should exist, rather than only
whether a prototype could run. An explicitly supported feasible/no-objection
finding remains valid; sharper review is not permission to invent objections.

For every proposal and revision, produce a compact pressure-test table in
`challenges.md` with the question, strongest counterargument, inspected evidence,
applicability limits, current answer and cheapest discriminating test:

1. **Novelty / residual delta:** express the strongest prior method and the
   proposal in the same state, information, action, constraint and output model.
   Name the smallest actual delta. Substitute the proposal's learned score into
   the strongest conventional controller, and substitute that controller back.
   Is any useful capability or full-cost tradeoff left? Known components alone
   are not a duplication proof; do not demand superiority to an identical clone.
2. **Engineering need:** identify the engineer, exact decision, production stage,
   downstream metric and constraints. Does the narrow regime occur outside a
   manufactured fixture? Would the user prefer an available simpler operation?
   Missing practitioner testimony is a gap, not proof that no demand exists.
3. **Mechanism:** try to construct a smallest counterexample, degenerate case,
   zero-information control and alternative causal explanation. Does the method
   change the feasible problem, or only the search window/number of calls?
4. **Headroom:** separate a matching lower/upper bound from an empirical plateau.
   State bound assumptions and remaining attainable improvement in the locked
   metric. A fatal saturation grade requires a bound below the frozen brief's
   numerical minimum meaningful effect; null thresholds cannot support it.
5. **Contest originality:** inspect organizer hints, baselines, winner methods,
   later editions and differently named formulations. Identify the contribution
   beyond the supplied approach, rather than counting an unfinished task as new.
6. **Experiments / full cost:** could the proposed experiment distinguish the
   hypothesis from the strongest alternative explanation? Audit decision-time
   information, labels, oracle, dependency order, family splits, tuning, failed
   runs, fallback and complete training/inference/communication/EDA costs.
7. **Anchor viability:** after verified objections, is there a supported repair
   preserving the problem, need and mechanism? Cosmetic renaming and unsupported
   method stacking are not repairs. A different promising question gets a new ID.

For multi-agent/unified-prediction proposals, explicitly try the strong single
controller, repeated-call single agent, ordinary parallel search, specialists
with fusion, shared-trunk predictor and prediction-plus-checker as applicable.
Explain an exclusion; do not use the list as a fabricated baseline quota. For
each major objection give an anchor-preserving repair OR evidence that none is
supported, and a cheapest kill test with a result that would reverse your view.
Prioritize the top three consequential attacks. Preserve and withdraw refuted
objections; a long list of minor complaints is not strong review.

## Machine scorecard

The exact frozen `config/topic-retirement.json` supplies weights and thresholds:

| Axis | Weight | Question |
|---|---:|---|
| novelty | 2 | Is there a nontrivial residual contribution? |
| utility | 2 | Is the engineering decision/need justified? |
| mechanism | 2 | Does the proposed causal mechanism survive scrutiny? |
| headroom | 1 | Is meaningful attainable improvement left? |
| contest_originality | 1 | Is it beyond supplied/known contest ideas? |
| experiments | 1 | Can a fair feasible plan distinguish the contribution? |
| anchor | 2 | Can critical issues be repaired within the same question? |

Grades are `clear=0`, `unresolved=1`, `major=2`, `fatal=3`. The score is the sum
of weight times grade points. It is a portfolio priority signal, not a novelty
probability or scientific truth score. In particular, unresolved does not mean
disproved. A missing measurement is not automatically a major or fatal failure.

The challenger adds `workflow.json.elimination_screen`:

```json
{
  "policy_id": "evidence-first-retirement-v1",
  "reviewed_proposer_release": "SUB-<actual 64 hex>",
  "recommendation": "revise",
  "axes": [
    {"axis":"novelty","issue_key":"residual-delta",
     "grade":"unresolved","references":["OBJ-101"],
     "reason":"Specific source-backed comparison or explicit search/access gap.",
     "repair_test":"Smallest evidence/test that could settle the distinction."}
  ]
}
```

Supply exactly one row for EACH of the seven axes, including clear rows. Keep
issue keys stable across revisions and identify resolved/replaced attacks in the
human table. Recommending `retire` does not retire anything by itself. A clear
row may have no references; do not manufacture seven objections to fill rows.

The scientific verifier independently adds `verification.json.elimination_review`:

```json
{
  "policy_id":"evidence-first-retirement-v1",
  "policy_sha256":"<exact JOB policy hash>",
  "reviewed_proposer_release":"SUB-<actual 64 hex>",
  "reviewed_challenger_release":"SUB-<actual 64 hex>",
  "axes":[
    {"axis":"novelty","issue_key":"residual-delta","grade":"unresolved",
     "references":["OBJ-101"],"reason":"Independent adjudication and limits.",
     "repair_test":"Concrete reversal evidence/test.",
     "no_anchor_preserving_repair":false,"checked_source_ids":[]}
  ],
  "resurrection_conditions":["Specific new evidence that would justify reopening."]
}
```

Again supply seven rows. The verifier may downgrade/clear the challenger's grade;
matching issue keys bind what was assessed, not agreement. Every nonclear row
must cite an already adjudicated, blocking current OBJ/claim. Refuted or
unsupported objections never earn risk points. The same OBJ/claim cannot be
counted on multiple axes. Major/fatal grades require reopened full-access
source IDs and locators. Only `valid` references can support fatal. A protocol
auditor cannot grade science or trigger retirement.

Use the established source_checks.source_id field (legacy id is also accepted;
conflicting aliases are rejected). For each source driving major/fatal, the
verifier must record verdict:verified, access_level:full, url and locator on that
source check. Basic source checks without these extra fields remain readable,
but cannot establish a confirmed retirement failure.

Every still-blocking valid/partially_valid/unresolved OBJ or claim must appear
on a nonclear axis; a clear scorecard cannot hide the verifier's own blockers.
Refuted/unsupported or explicitly resolved issues cannot drive retirement.

A fatal row must set `no_anchor_preserving_repair:true` and the matching ground:

| Axis | fatal_ground |
|---|---|
| novelty | equivalent_prior_no_residual |
| utility | incompatible_engineering_objective |
| mechanism | counterexample_no_anchor_repair |
| headroom | proven_bound_below_locked_threshold |
| contest_originality | supplied_solution_no_residual |
| experiments | nondiscriminating_no_anchor_repair |
| anchor | no_remaining_anchor_preserving_path |

For headroom also supply `primary_metric` matching the frozen domain/common
brief and `remaining_improvement_upper_bound` in that metric's units. The bound
must be nonnegative and below its finite positive, locked numerical
`minimum_meaningful_effect`. A paper's bound on a different model is not enough.
Only fatal rows may assert no repair. No budget, an inaccessible paper, missing
implementation or absence of gain measurements is not a fatal ground.

## Automatic transitions

1. **Verified fatal:** at least one independent verifier-confirmed fatal axis
   with the above evidence/repairability checks automatically retires the topic
   after that completed P/C/V cycle. No additional proposer consent is required
   for this owner-authorized portfolio decision. Preserve any disagreement.
2. **Persistent critical risk:** score at least **6** on **two consecutive
   distinct scientific proposal revisions**, with at least **two nonclear axes
   shared across both**, automatically retires the topic. This includes honestly
   unresolved decision-critical gaps after a repair opportunity. It means stop
   spending this portfolio's next round, NOT that an unresolved idea is false.
   A low-risk revision breaks the streak. Consent-only/metadata-only republishes
   of identical proposer science do not manufacture additional attempts. Grades
   from different policy hashes cannot be combined.

The runtime status/round decision is `retired_by_policy`; the actor's original
scientific `next_action` remains separately recorded. Existing signed joint
abandonment remains `abandoned` and still requires both exact consents. Neither
path authorizes experiments or fabricates agreement. The earlier three-round
parking fallback remains for topics below the automatic-retirement thresholds.

Retirement retains the full frozen P/C/V triple, scorecard, checked policy bytes
and hash, decisive review IDs, disagreements and resurrection conditions. Each
round PR includes its `runs/CODEX-ROUND-*/retirement.json` certificate. These run
archives are not synthesized canonical `archive/EDA-*/` dossiers and are not
signed joint-abandonment records. No old content is deleted. A fresh successor
gets a new ID, fresh seats and only the released predecessor record, after any
required protocol audit. Quarantine cancels use of that cycle's risk points.
The domain/topic budget and finite four-round hard stop still take precedence;
retirement cannot start an extra research cycle or erase a quarantine.

The coordinator verifies structure, hashes, source/claim bindings and the
threshold calculation; the assigned scientific verifier supplies scientific
entailment. Hash checks cannot establish truthful judgments or unseen isolation.
Human exceptions or reopening must be explicit, recorded and delivered in a new
packet/run. Do not quietly relaunch a retired ID or inherit its signatures.
