# Human-led literature and topic review

Owner update, 2026-10-16: AI proposer is retired. Active AI roles are searcher,
challenger and verifier. The human is the sole research-idea author. This contract
supersedes older platform launch, automatic AI proposal and successor instructions.

## Literature

Searcher discovers frontier papers, then follows references to the strongest
older work. Scope: floorplanning, placement, CTS, routing, timing/power signoff and
physical verification. Target 100 unique papers, released in batches of ten.
Keep contests and open projects in separate counts. Classify, retain English
bibliography, translate titles, paraphrase abstracts in Chinese and identify
reading priorities. Mark abstract screening separately from full-method reading.
Searcher does not propose a new topic, claim novelty or select an experiment.

## Human idea -> challenge -> verification -> human revision

1. Human supplies an idea, using templates/human-idea.md if useful. Preserve the
   author's wording. Translation or formatting must be labelled assistance; no AI
   may silently supply a mechanism, consent or human answer. Unknown resources stay
   unknown and block feasibility only, not exploratory review.
2. Coordinator commits the idea and explicitly released supporting files, records
   the full input SHA and file hashes, and gives a fresh challenger only common
   rules, its own harness and these released inputs. No parent-history fork.
3. Challenger independently searches sources, contests, hints/winners and strong
   implementations. It writes the strongest substantive attacks, counterexamples,
   fair baselines, a forecast labelled as such and cheapest decisive tests. It
   self-freezes its own files. Raw objections go to verifier first.
4. A fresh verifier receives the matching human idea and challenge. It reopens
   sources, rules on each material claim and objection, grades retirement risk
   independently and self-freezes compact tables plus machine-readable evidence.
   Unsupported objections cannot block the idea. Coordinator is transport only.
5. Coordinator publishes exact released outputs and provenance through a PR after
   each completed review round. Required CI must pass before coordinator merge;
   no self-approval or simulated scientific approval. Deliver adjudicated feedback
   to the human, who authors or explicitly adopts the next revision. Waiting for
   a human idea or revision is a legitimate state; do not generate a replacement.

Searcher, challenger and verifier communicate through released files only. Each
may read accessible external research without per-source approval, but no other
role's private notes, sessions, memories or unreleased files. Read only the assigned
harness. Shared OS account means policy isolation, not a security boundary.

## Outcomes

Keep the anchored question and direction-drift penalties. High-quality useful
combinations and structural contributions are both eligible. For verified fatal
or persistent risks apply TOPIC-RETIREMENT.md: stop investment, keep uncertainty
and resurrection conditions, then wait for a new human idea under a new ID.
The old runner's automatic AI successor allocation is inactive.

Acceptance needs the complete dossier, independent scientific gates, zero drift,
explicit agreement by human author and challenger on the exact task-list hash,
and real tool/data/compute allocation. A reviewer may draft tasks or experimental
forecasts; only the human adopts changes to the idea. A forecast is not a result.
Never impersonate a human session, consent or GitHub approval. Existing canonical
`proposer_*` fields name the author slot, now human, not a new AI actor. Preserve
old schemas and frozen signatures; register the real human author separately
when a formal dossier is submitted. Transport/configuration success is not topic
acceptance and does not authorize experiments.

## Execution status

Active settings are config/research-workflow.json. No unattended service is
claimed by these documents. Historical P/C/V launch configs are disabled and
archived under legacy/. Tests may replay synthetic old-format jobs. Research
snapshots under runs/ and previous reports are not modified by new policy.
