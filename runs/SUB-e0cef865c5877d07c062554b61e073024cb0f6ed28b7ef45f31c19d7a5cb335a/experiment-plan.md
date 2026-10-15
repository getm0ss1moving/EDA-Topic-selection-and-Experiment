# Conditional experiment plan — dormant

## Hypotheses

H1: signed intervention-dependent electrical residual factors improve candidate query efficiency beyond current calibrated estimation and a faithful same-feature joint GP/controller at equal labels/cost. H2: the measured local choice retains useful global timing outcomes. Counter-hypotheses: errors cancel without querying; scalar calibration suffices; physical W adds no value; separable-kernel transfer cancels; path switching invalidates the approximation; exact incremental queries are too cheap; local score fails to improve closure. All outcomes are unknown.

## EXP-000 completed check

Exact arithmetic only, normalized arbitrary units, Python standard library:

```sh
python3 - <<'PY'
from fractions import Fraction as F
assert 10+10-2*9 == 2
assert 10+10-2*0 == 20
assert 10+10-2*(-9) == 38
assert F(10)-F(81,10) == F(19,10)
print('2, 20, 38; conditional variance 19/10')
PY
```

Executed successfully in /tmp/eda0007-p05-c807b92b. This is standard covariance algebra, not circuit realizability, fitting, timing or industrial evidence. Equal shared error can cancel before observation. A reduction of marginal variance alone does not imply ranking benefit; anticorrelation and misspecified signs are negative controls.

The second synthetic affine check was also executed with `fractions.Fraction`: a(k)=49/5+k/5, b(k)=51/5-k/5; assert a(1/2)<b(1/2), a(3/2)>b(3/2), and a(1)=b(1). Outputs are (99/10,101/10), (101/10,99/10), and (10,10). It represents opposite signed load changes under a positive upstream response slope, with an already known base intercept. It is not a manufactured physical process distribution. Exact knowledge of the slope removes the witness uncertainty. No circuit, data extraction, fitting or engine run was performed.

## Metrics and oracle

Full scalar enumeration of the SAME legal ordered candidates from the SAME immutable base provides reference local g, declared feasibility, tie order, best choice and full global guard outputs. Unqueried labels are withheld from the policy. Primary curve: total wall time versus feasible local-score simple regret in ps, g(best)-g(returned); report exact-choice frequency, no-action frequency, failures and unsupported contexts. Secondary: one-step post-commit global setup WNS/TNS and electrical counts/magnitudes. Enumerating a reference does not make its labels free training data.

The supplied >=20% runtime screen is provisional. Its 5ps endpoint-error screen is not repurposed as allowed ranking regret. EXP-005 must justify/freeze local regret and global thresholds before candidate comparisons. Zero known violating accepted choices on evaluated cases is a report, not unconditional correctness. A restore mismatch invalidates subsequent observations. No same-choice guarantee or hold/MCMM/foundry claim.

## Strong and equal-budget baselines

B0 full incremental enumeration; B1 modern calibrated analytical/window policy including STA slew bias; B2 independent specialists plus standard fusion/selection; B3 shared-trunk joint predictor; B4 generic multi-output GP with identical W/features/mean/data; B5 supplied-feature latent-factor GP with identical rank, regularization and controller (possibly exactly equivalent); B6 fixed/random/top-k or marginal-confidence order with the same query cap. Charge fitting and hyperparameter search, not merely EDA calls. B4/B5 cannot be deprived of features or routine implementation choices.

Classical LR/timing calibration and compatible differentiable sizers are broader alternatives (S06/S09/S16). Their un-reproduced industrial reported gains are not local measured baselines. An eventual source-compatible conventional optimization comparison tests whether this slice matters. No runtime agents are selected; multi-agent experiments and token calls are unnecessary. The shortlist gives fair repeated-call/non-LLM controls for a separate agent hypothesis.

## Mechanism controls

A1 zero cross-candidate covariance while preserving marginals/means. A2 independent output factors. A3 shuffle signed W rows among alternatives of one target. A4 same-feature generic GP. A5 strongest deterministic mean/calibration. A6 opposite/zero sensitivities, changed input capacitance, LUT boundaries and max-path/reconvergence switches. A7 noiseless bundled full-output block observations with separable kernel, testing cancellation. A8 cold-start versus amortized label cost. Exact queries always return objective/constraints as a bundle; no invented independently cheap tasks.

Match data, target/candidate generator, features, model rank, EDA/fallback budget, seeds and acquisition fantasies. W may only use base-state/library/analytical information. The finite-set controller estimates reduction of regret for a measured-only incumbent per full predicted transaction cost with bounded samples; the same code/caps apply to all kernel variants. It is approximate and offers no early-stop guarantee.

## Data and resource dependencies

The supplied brief documents only a historical GCD/Nangate45 smoke and typical corner; this job did not inspect/acquire its design files. It cannot establish representativeness or a usable VT candidate dataset. Audit rights separately for OpenROAD BSD source, OpenSTA GPL/commercial terms, each library/design, constraints and derived outputs. No licensed PDK/netlist/full-paper copies enter release.

Split by independent design family, grouping variants/checkpoints; separate training/calibration/tuning/held-out families before labels. No future reference table in fitting/acquisition. Report technology/corner scope and public benchmark exposure. The minimal factor model requires no pretrained LLM, but calibration label availability is unresolved.

No new experiment allocation exists. Proposed first authorized diagnostic request: CPU only, one tiny existing rights-cleared checkpoint, <=10 minutes, <=2GB, <=64 scalar transactions. This is a conditional request, not permission or available data. Fitting and subsequent pilot also require actual allocation and dual scientific consent. Historical provisional 8h/4GB is not an owner commitment.

After diagnostic variance, choose >=3 independently selected lawful design families if available; >=5 paired seeds per stochastic controller are a planning minimum, not power. Use family-clustered paired bootstrap intervals and all failures; deterministic methods need no artificial seeds. Freeze confirmatory sample size/tolerances before comparing candidate results. No GPU/remote/paid API/full flow is assumed.

## Stops and reproducibility

Stop on no real candidate-volume/bottleneck, poor held-out contrast calibration, no useful delta versus B4/B5, cost dominated by exact baseline, or failed global proxy utility. A valid negative result is not hidden by adding components. Restoration failure halts correctness claims. Changed task/dependency/threshold bytes invalidate consent.

Future artifacts: source/build/FP/library/SDC/parasitic locks; state/candidate/W definition and hashes; split manifest; oracle/candidate JSONL; per-transaction prepare/apply/update/report/restore times; fitting/acquisition/search/label costs; selected/global guard results; calibration and regret/Pareto tables; unsupported/failure ledger; independent reproduction. EXP-001 must instantiate commands against audited real APIs; no fictional CLI/build execution is claimed now. tasklist.md supplies bounded producer/consumer procedures for these unavailable dependencies.
