# Challenges

*Transported verbatim from the `DeepSeek-C05-TIMING` outbox by the DeepSeek platform lead
(run `DSK-C05-SESSION-0001`). Source `challenges.md` SHA-256
`b57953a2e5aab67677dacc2cd9caee3ce0edef58070f1a85588e29c03407e225`. The objection and
open-question blocks below are byte-identical to the source, asserted during assembly;
only the surrounding section skeleton follows the repository template, per the author's
transfer instruction (§3 of the submission packet). Nothing here is edited, signed or
adjudicated by the coordinator.*

# Challenges (objections)

**Actor:** `DeepSeek-C05-TIMING` (challenger, D05, EDA-0002). **Round 1**, written 2026-10-13 (session window ~11:45Z).
**Packet:** `e6c53f61…5332cf`, input commit `4b666c04…`. **Status of everything here: provisional.** Per `harness/CHALLENGER.md` items 12 and 24, an objection blocks nothing until the verifier adjudicates it, and I accept corrections.

**Evidence standard used.** Every objection below carries: targeted claim, severity, primary source IDs and locators, factual evidence, inferential bridge, confidence, conditions that invalidate the objection, and a cheapest decisive test. Code evidence comes from the pinned OpenSTA tree at `e01d3f163f483f233db00410b6515a767a6ca03b`, downloaded as a tarball and hash-verified against the proposer's recorded hashes (all eight match; `sources-challenger.json` C-A13). Symbolic claims about what the code means were read from the file, not from a summary.

**Classification.** OBJ-001 = major, fixable, soundness-relevant. OBJ-002 = minor (potentially major under a stated condition), precision/audit-scope. Open questions follow, then suggestion-only material marked as my hypotheses.

---

---

## Independent estimate before forecast exposure

Recorded pre-exposure by `DeepSeek-C05-TIMING` in `first-pass-plan.md` §2 ("Independent
headroom estimate before forecast exposure"), SHA-256
`dc3939f131e55ea7bd4bb74072f6c3f2c19a8bc1417b3986635a3daa681afaac`, transported with this
packet (`runs/DSK-C05-SESSION-0001/received/first-pass-plan.md`). `forecast.json` was
withheld from the challenger's packet at stage `initial`; no forecast was exposed before
the estimate or the objections below were written.

## Objection ledger (ID, claim, severity, sources, reasoning, uncertainty)

## OBJ-001 — The hold certificate omits CRPR, and CRPR *reduces* hold slack in the pinned engine: the stated justification ("CRPR only adds slack") is false for hold

**Targeted claim.** `proposal.md`, § Proposed mechanism, step B ("Derates and uncertainty" bullet list):

> "**CRPR:** give no credit in the bound. This is conservative, because CRPR only adds slack."

This sentence justifies the hold certificate of step C ("Hold lower bound = AL(D) − exact hold required time at s − (upper bound on hold time)") and carries into CLM-009's decision-equivalence argument ("Every violating triple is uncertified when M ≥ 0, so violation lists, sub-margin slacks and TNS are exact").

**Severity.** Major, fixable. It is a soundness hole specific to the hold half of the certificate; it does not touch the setup half or the refinement machinery.

**Primary sources and locators** (all in the pinned, hash-verified tree).

- `search/PathEnd.cc:691-710` — verbatim:

  ```cpp
  Crpr
  PathEndClkConstrained::commonClkPessimism(const StaState *sta) const
  {
    if (!crpr_valid_) {
      CheckCrpr *check_crpr = sta->search()->checkCrpr();
      crpr_ = check_crpr->checkCrpr(path_.path(), targetClkPath());
      crpr_valid_ = true;
    }
    if (checkRole(sta)->genericRole() == TimingRole::hold())
      return -crpr_;
    else
      return crpr_;
  }

  Required
  PathEndClkConstrained::requiredTime(const StaState *sta) const
  {
    return requiredTimeNoCrpr(sta)
      + commonClkPessimism(sta);
  }
  ```

- `sdc/Sdc.cc:226-229` — the Sdc constructor sets `analysis_type_ = AnalysisType::ocv;` and `crpr_enabled_ = true;` (`crpr_mode_ = CrprMode::same_pin;`).
- `sdc/Sdc.cc:5474-5477` — `Sdc::crprActive()` returns `analysis_type_ == AnalysisType::ocv && crpr_enabled_`.
- `tcl/Variables.tcl:50-70` — `set_crpr_enabled` / `crpr_mode` are the user-visible controls; defaults are as above.
- `search/PathEnd.cc:1015-1020` — `PathEndCheck::clkSkew` subtracts `crpr_` and subtracts target-clock uncertainty, with the comment "Uncertainty decreases slack, but increases skew" (evidence that required-time terms carry individual signs; not every omission is conservative).
- Source record: `sources-challenger.json` C-A15.

**Factual evidence.** With the pinned defaults, CRPR is **active**, and for a hold check `requiredTime = requiredTimeNoCrpr − crpr`. Hold slack is (arrival − required); therefore CRPR **decreases** hold slack by crpr. For a setup check the same code returns `+crpr`, which increases the required time and therefore setup slack. The sign flips with the check role.

**Inferential bridge.** The proposal's bound pass computes the hold lower bound with no crpr term. Where crpr > 0 at a checked pair, the bound exceeds the reference value by exactly crpr. Any hold triple whose reference slack lies in [M − crpr, M) is then certified although the reference does not certify it, so (i) the reported hold violation list can omit violations when M ≥ 0 and slack is in [−crpr, 0), and (ii) hold TNS is not exact. That is precisely the class of error the candidate claims to eliminate, and it falsifies the phrase "CRPR only adds slack" as a general statement.

**Confidence.** High on the code facts (verbatim lines, hash-verified tree, defaults read in the constructor). Medium-high that it bites the pilot: it requires only that some evaluated hold check has a shared launch/capture clock path with crpr > 0, which is the normal case with propagated clocks, **and** that the flows keep the default OCV/CRPR settings. Both are checkable before implementation.

**Conditions that invalidate this objection.**
(a) The evaluated runs have CRPR inactive in both the reference and the candidate (for example a flow that sets `set_crpr_enabled false` or a non-OCV analysis type), making crpr ≡ 0 on every check — then the omission is exact, not optimistic, though the proposal's sentence would still be wrong as written.
(b) The certificate is amended so the hold bound carries crpr with its own sign, taken from the exact clock pass (or a sound upper bound on it).
(c) Evidence that crpr ≡ 0 for all hold checks on all evaluated designs (not expected with propagated clocks and shared clock trees, but that is the measurement).

**Cheapest decisive test** (no implementation, no library work; EXP-scale: minutes).
1. On any evaluated design in the pinned container, run the reference flow's `report_checks` for hold once with the default settings and once with `set_crpr_enabled false`; diff the hold slacks. A non-zero difference closes the question: crpr is real, and its sign is observable.
2. Unit-scale variant: a two-flop design with a shared clock buffer, where the divergence is visible by inspection.
3. Static companion check, needed for severity rather than existence: confirm in the pilot's flow scripts whether OCV/CRPR defaults are left untouched.

**Verifier note.** The follow-on question — "which required-time terms can be dropped conservatively and which cannot?" — is the general form of this objection. I have verified the crpr sign only for hold; I have *not* audited every term (clock uncertainty, inter-clock uncertainty, derates) for sign in the certificate. I flag this as a task for EXP-002 rather than asserting further defects.

---

## OBJ-002 — CLM-007's wire-delay description is incomplete in a way that bears on P4: `thresholdAdjust` can raise the returned delay above the single-pole value, and ports use a different formula

**Targeted claim.** `proposal.md`, claim ledger CLM-007:

> "Wire delay is a single-pole crossing with τ = Elmore delay, with Elmore fallbacks, and load slew is at least driver slew."

and, in the mechanism, step B: "**Wire arcs:** upper bound = Elmore delay of the same reduced model the reference uses (P4)". CLM-007 is the factual basis on which P4's audit and the wire bound are built.

**Severity.** Minor as filed (a precision defect in an OBS claim plus an audit-scope gap); **potentially major** under one stated condition, **narrowed in this round**: if an evaluated scenario reads a driver/load library *pair whose threshold pct attributes differ* (some macro/IO libraries use different conventions), or has input-port arcs in the decision set, the wire bound as specified is not sound at the affected pins. Merely reading several libraries per corner is not sufficient — ASAP7's LVT/RVT/SLVT variants share identical threshold attributes, so mixed-VT is inert (evidence update below; record C-A30).

**Primary sources and locators** (pinned, hash-verified tree).

- `dcalc/DelayCalcBase.cc:126-153` — `thresholdAdjust(load_pin, drvr_library, rf, load_delay, load_slew)`: applies **only when** `load_library != drvr_library`; for a rise it does `load_delay += load_slew * ((load_vth - drvr_vth) / drvr_slew_delta)` (subtracting the same on a fall), and rescales the slew by the ratio of slew windows and derates.
- `dcalc/DelayCalcBase.cc:155-169` — `thresholdLibrary`: top-level ports resolve to the default (first-read) Liberty library, a second route by which driver and load libraries can differ.
- `dcalc/DmpCeff.cc:569-570` — the comment stating the delay and slew are measured at driver thresholds and "rely on thresholdAdjust to convert the delay and slew to the load's thresholds".
- `dcalc/DmpDelayCalc.cc:96, 121, 276, 343` and `dcalc/LumpedCapDelayCalc.cc:162` — where the adjustment is applied to the wire delay after the calculator returns it.
- `dcalc/DelayCalcBase.cc:107-124` — `dspfWireDelaySlew` (input-port DSPF path): `wire_delay = -elmore * log(1 - vth)`, a different formula from the `DmpAlg` crossing.
- `sources-challenger.json` C-A16.
- Companion source question: `sources-challenger.json` C-A14 (DAC 1995 read at full text) — the cited theorem bounds the 50% delay of the **true RC tree response** for inputs whose derivative is unimodal and symmetric, with tree structure used in the proofs and no stated coverage of floating capacitors or resistor loops. The pinned calculator returns a crossing time of an internal pi-model waveform, measured from the driver source waveform's own crossing. Those are different quantities.

**Factual evidence.** (i) The value returned to the timing engine is not always the single-pole crossing: a library-dependent additive adjustment is applied afterwards, positive on rises when `load_vth > drvr_vth`. (ii) Top-level ports are served by a third wire-delay formula. (iii) The cited theorem's object is not the calculator's waveform model.

**Inferential bridge.** P4 is stated as a property of "the load delay returned by the single-pole crossing" bounded by "the Elmore delay of the reduced model". For (i) the returned value can exceed that bound; for (iii) the cited backing does not connect the two objects, so even where no adjustment applies, P4 needs a modelling argument (the calculator's pi-model crossing versus the true RC tree response) rather than the theorem alone. Neither point shows the bound is unachievable — both are cheap to close — but as written the claim is not yet supported and its factual premise (CLM-007) understates the code.

**Confidence.** High on the code facts. Medium on the practical bite: it depends on whether the pilot's scenario sets have one or several Liberty libraries per corner, which `experiment-plan.md` does not currently state, and on whether port arcs are inside the evaluated decision set (the proposal's own scope notes flop-to-flop checks; ports are excluded in SRC-012's measurements and may be excluded in EXP-003).

**Evidence update (same round, sweep closure).** The condition this objection depends on was probed against a real multi-library corner: the ISPD 2026 contest platform reads ASAP7 LVT/RVT/SLVT libraries in a single TT corner (record C-A27), and the three library headers declare **identical** threshold attributes (input/output 50%, slew 10/90; record C-A30). Since the adjustment term is proportional to `(load_vth − drvr_vth)`, mixed-VT alone is inert. The trigger is therefore *differing threshold definitions across a driver/load pair*, which is narrower than "more than one library per corner". This self-narrowing is recorded in `findings-challenger.md` F-15; the CLM-007 completeness point and the P4 modelling obligation are unaffected.

**Conditions that invalidate this objection.**
(a) Every evaluated scenario's driver/load library pairs (and its port arcs) are shown to have equal threshold attributes and no port arcs in the decision set; then the adjustment is inert on the evaluated pins and the objection collapses to a wording fix (still worth making, because EXP-002's audit is defined against CLM-007).
(b) CLM-007 is amended to state the returned quantity (crossing plus threshold adjustment, with the port formula), and P4 is restated as an inequality between two named quantities with the connecting argument supplied.
(c) A unit test shows the adjusted delay is always ≤ the pure crossing for the thresholds in the evaluated libraries.

**Cheapest decisive test** (no implementation; EXP-scale: minutes to an hour).
1. Static: for each evaluated corner, extract the threshold pct attributes of every Liberty file read (and resolve the default-library route for ports, `DelayCalcBase.cc:155-169`); the condition is live only if two libraries that can drive/load each other differ, or if port arcs are in the decision set.
2. Unit (only if a mismatched pair exists): one driver arc at a rise with `load_vth > drvr_vth`; compare the returned wire delay with the pure crossing. Any returned value above it falsifies P4's bound at that pin and quantifies the gap.

---

## Conditions refuting each objection

Stated inside each objection block in the ledger above, per the challenger's filed format
(conditions that invalidate the objection).

## Cheapest decisive tests

Named inside each objection block above (OBJ-001: minutes-scale reference-hold CRPR on/off
diff plus a static default check; OBJ-002: per-corner static threshold-attribute scan over
the interacting libraries).

## Nonblocking questions and new hypotheses

## Open questions (not objections)

- **OQ-1.** P3 remains, on the proposer's own assessment, the highest-risk property ("the driver slew passed downstream … lies within a computable bound"; `proposal.md` § Soundness properties, marked "not established"). My reading of `DmpPi::gateDelaySlew` (`dcalc/DmpCeff.cc:915-949`) is consistent with the proposal's description: on the success path `slew = vo_slew` from the driver-waveform model, with table-slew fallback on failure. Whether the waveform-model slew can leave a computable band around the table values is exactly what EXP-002 must decide; I have nothing to add beyond noting the fallback branch (`slew = table_slew`) creates a second, differently-shaped case for the bound.
- **OQ-2.** U7 (cone-restricted search without global side effects) and CH5 interact with the refinement step; nothing in this window changes that.
- **OQ-3.** The definition of TNS in D_M(S) — per scenario, over which endpoint/check population, with what ties to OpenSTA's own reporting — is not pinned down in `experiment-plan.md`. Since the candidate claims TNS exactly, the oracle's definition must match the reference tool's, not a reimplementation's.
- **OQ-4.** The TAU 2019 benchmark package (6 designs, Nangate45, SPEF, early/late libraries; F-6) is a candidate partial answer to the dataset gap (CLM-013) if its licence and corner structure permit; the deck does not settle whether fast/typical are two PVT corners.
- **OQ-5.** The broadened contest sweep (F-11) leaves the dataset question as follows: the TAU series ended in 2021 (delay calculation; no corner scenarios), ICCAD 2025/2026 problems are optimization tasks, ISPD 2026 is setup-only with a single PVT corner and ideal clock, and MLCAD 2025 is single-setup resynthesis. So no contest supplies a multi-corner flow; if the proposer's related-work or dataset sections lean on "contest-adjacent" flows, the only live lead remains the TAU 2019 package.

## Suggestions (hypotheses of mine, explicitly not demands; the anchored contribution stays the proposer's)

- **S-1.** Carry crpr in the hold certificate from the exact clock pass (OBJ-001) and, while there, tabulate every required-time term with its sign (a one-page sign audit) so "conservative" is a per-term statement rather than a blanket one.
- **S-2.** Add a threshold-adjustment term to the wire bound, or prove it inert for the evaluated datasets (OBJ-002).
- **S-3.** Promote the two decisive tests above into the challenger additions list as unit tests, since both are cheap, independent of implementation, and would be falsifying for K2 (P2-P5 unachievable) rather than merely informational.
- **S-4.** Related-work framing after the SOTA sweep (F-12): place US 12,675,622 B1 explicitly — it already claims per-path corner marking, ML estimation with an error-threshold gate, and an aggressiveness knob — and state the candidate's differentiator as *certified margin plus exact violation lists/TNS plus exact refinement against the pinned non-affine engine*. Avoid importing the patent's looser vocabulary ("good coverage", "acceptable differences in QoR", a "consistent TNS error percentage") into the proposal, since the proposal's own claims are strictly stronger and the weaker phrasing would understate them.

## Revision and withdrawal history

| Round | Date (UTC) | Event |
|---|---|---|
| 1 | 2026-10-13 | OBJ-001 (major, fixable, soundness-relevant) and OBJ-002 (minor as filed; potentially-major branch narrowed by evidence C-A30/F-15) filed by `DeepSeek-C05-TIMING` (session `af136556-818c-47c7-b514-5a141cb14d85`) against frozen revision `4b666c04…` (packet `e6c53f61…`). Open questions and suggestions are not objections. No withdrawal. Status provisional: an objection blocks nothing until the verifier adjudicates it (harness items 12/24). |
