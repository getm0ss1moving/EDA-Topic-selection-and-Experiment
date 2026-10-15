# P3-P5 property-check record for EDA-0002 (CLD-LAB-0001)

| Field | Value |
|---|---|
| Author | `Claude-P05-TIMING` (proposer), session `76d0bf61-78f7-4b93-a557-7c29f1a2cbe8`, run `CLD-P05-REVISION-0001` |
| Authority | Owner decision `COORDINATOR-owner-decisions.md` (SHA-256 `b479fc60e1dbfd38dbc45618f3670bca12b29bc73fc33bd637c07a11e4eb29c4`), item U2; runner instructions SHA-256 `f36cf54878f760005eda9fd7259000ab88f4c4ab11265e5f07d9c9f30b7e05de` |
| Scope | P3-P5 of `proposal.md` against pinned `dmp_ceff_elmore`. Synthetic libraries and synthetic or injected parasitics only. No real design. No hypothesis, runtime, certifiable-fraction, band-width or QoR measurement |
| Runner jobs | REQ-0001 to REQ-0009; ledger in `evidence/runner-ledger.json`, 0.45 core-hours in total |
| Result | **P3, P4 and P5 as stated are falsified** by reachable counterexamples. Narrowed properties survive as code arguments with passing finite tests. **K2 is activated**, and the guarantee claim is narrowed in `proposal.md` |

The labels below follow the runner instructions: `proved`, `code-argument-only`, `finite-tests-pass`, `falsified`, `unresolved`. A passing finite test suite is not a proof. Nothing in this record is labelled `proved`.

## 1. Pinned source revision

- **OpenSTA revision.** `e01d3f163f483f233db00410b6515a767a6ca03b`, the `src/sta` submodule of packet-pinned OpenROAD `b16bda7e82721d10566ff7e2b68f1ff0be9f9e38` (SRC-010).
- **Fetch (REQ-0001, lab231).** Fetched from `https://github.com/The-OpenROAD-Project/OpenSTA.git`.
  - Resolved commit: `e01d3f16…`.
  - SHA-256 of `git archive --format=tar HEAD`: `5fdc01f102ae6e3a7478ac9e2f95f6d60d08f82cb6ac06ea96bdc1d6b4da3b5c`.
  - GitHub tarball SHA-256: `db4433ccb71a0aa0f050fafb18dcbc18360ad012e62398f61b96762c40cf9f55` (`evidence/REQ-0001-network-log.tsv`).
- **Files read by the proposer.** All match this revision byte for byte:

  | File | SHA-256 (prefix) |
  |---|---|
  | `dcalc/DmpCeff.cc` | `edfadea5…` |
  | `dcalc/DmpDelayCalc.cc` | `71f1023b…` |
  | `dcalc/FindRoot.cc` | `271784b3…` |
  | `dcalc/DelayCalcBase.cc` | `41ef5d2a…` |
  | `dcalc/LumpedCapDelayCalc.cc` | `1ca3609a…` |
  | `dcalc/GraphDelayCalc.cc` | `d939d1bb…` |
  | `liberty/TableModel.cc` | `8326d308…` |
  | `parasitics/ReduceParasitics.cc` | `acdd3eb9…` |
- **License.** Repository `LICENSE`, SHA-256 `3972dc97…`, is GPL-3.0.

## 2. Build commands and toolchain

Toolchain sources were fetched from official GitHub repositories or releases only (REQ-0003, `evidence/REQ-0003-network-log.tsv`). Licenses were read from each repository (`evidence/REQ-0003-licenses.txt`, `evidence/REQ-0005-cmake-license.txt`).

| Tool | Source and pin | SHA-256 of download | License (from repository) |
|---|---|---|---|
| CMake 3.27.9 | Kitware release asset; matches Kitware's published SHA-256 list | `72b01478…` | BSD-3-Clause (`doc/cmake/Copyright.txt`) |
| flex 2.6.4 | `westes/flex` release asset | `e87aae03…` | BSD-style (`COPYING`) |
| byacc 2.0 20240109 | `ThomasDickey/byacc-snapshots` tag `t20240109`, commit `e0101393…` | `5ad4ada6…` | Public domain (`LICENSE`) |
| Tcl 8.6.13 | `tcltk/tcl` tag `core-8-6-13`, commit `338c6692…` | `03c142bc…` | Tcl BSD-style (`license.terms`) |
| SWIG 4.1.1 | `swig/swig` tag `v4.1.1`, commit `77323a0f…` | `79d42de4…` | GPL-3.0-or-later plus university terms |
| Eigen 3.3.7 | `eigenteam/eigen-git-mirror` tag `3.3.7`, commit `cf794d3b…` | `c7f57546…` | MPL-2.0 (`COPYING.MPL2`) |

**Build (REQ-0004, then REQ-0005, on lab234 with no network).** The scripts are `lab-requests/REQ-0004.sh` and `REQ-0005.sh`. The steps were:

- byacc, flex, Tcl and SWIG were built with `./configure --prefix=/ws/tools/p05 && make && make install`.
  - flex used `CFLAGS='-O2 -D_GNU_SOURCE'`.
  - SWIG used `--without-pcre --without-alllang YACC=byacc`.
- Eigen was installed with CMake.
- OpenSTA was configured as follows, then built with `cmake --build -j 8`:

  ```
  cmake -DCMAKE_BUILD_TYPE=Release -DTCL_LIBRARY=… -DTCL_INCLUDE_PATH=… \
        -DBISON_EXECUTABLE=/ws/tools/p05/bin/bison -DFLEX_EXECUTABLE=… \
        -DSWIG_EXECUTABLE=… -DEigen3_DIR=…
  ```

**Build configuration (REQ-0009, `evidence/REQ-0009-build-config.txt`).**
- Compiler: gcc 9.4.0.
- `CXX_FLAGS = -O3 -DNDEBUG -Wall -Wextra -pedantic -Wcast-qual -Wredundant-decls -Wformat-security`.
- CUDD off; readline off; zlib on.

**Binary.** The `sta` executable is written into the source tree's `app/` by the pinned CMakeLists (line 568).
- SHA-256 `d6821adce56e1f8dec50ca0730129e8ebe297a7c5663ba85f84e9558466b464c`.
- Smoke test: `sta_version 2.5.0 git_sha1 e01d3f163f483f233db00410b6515a767a6ca03b`.
- Registered calculators: `arnoldi ccs_ceff ccs_sim dmp_ceff_elmore dmp_ceff_two_pole lumped_cap unit`.
- `git status --porcelain` on the source tree is empty: no tracked file was changed (`evidence/REQ-0006-setup.txt`).

**Deviation: parser generator.** GNU bison has no GitHub release with clear provenance, so it was replaced by Berkeley yacc. A wrapper maps the CMake `BISON_TARGET` command line onto byacc:
- `--name-prefix` becomes `-p`;
- the header path is passed with `-H`.

The wrapper's SHA-256 is `5fb67dba…`, and it reports itself as byacc. OpenSTA's C++ sources and grammars were not modified, but the generated Liberty, SPEF, Verilog and SDF parsers differ from a bison build. The delay calculator code under test is unaffected. Parse fidelity on the fixtures is supported by two cross-checks:
- an independent Python reduction of every SPEF net matches OpenSTA's pi model to 1.7e-7 of C1+C2;
- every arc on a code path that returns the Elmore value exactly reproduces the Python Elmore value to 2.4e-7.

A verifier may still want a bison build.

## 3. Fixtures

All fixtures are synthetic; no external library or design is used.

**Generator.** `lab-requests/p05_fixtures.py` (SHA-256 `08488e01…` for REQ-0008). The REQ-0008 command was:

```
python3 p05_fixtures.py FX 3000 3000 20261015 1500 800
```

Fixture file hashes are in `evidence/REQ-0008-fixture-sha256.txt`. A local regeneration with the same seed reproduced `p05.v`, `p05.spef` and `p05_inputs.tcl` byte for byte.

**Libraries.** Two synthetic libraries:

| Library | Thresholds (vth / vl / vh) | Slew derate | Cells |
|---|---|---|---|
| `p05a` | 50 / 20 / 80 % | 1.0 | `BUFA_X1`, `X2`, `X4`, `X8`, `X16`, plus `BUFA_W4` |
| `p05b` | 50 / 10 / 90 % | 0.5 | `BUFB_X1`, `X4`, `X16` |

- The 7×8 NLDM tables are generated from a ramp source through R into C, with a drive resistance of 4 kΩ / X.
- `BUFA_W4` deliberately has tables that are inconsistent with any ramp-through-R driver.
- Input slews range from 0.003 to 0.5 ns, which includes extrapolation beyond both table ends.

**Nets.** There is one driver buffer per net with 1-4 load buffers. The families are:

| Family | Nets | Construction |
|---|---|---|
| `rand_spef` | 3,000 | Random SPEF RC trees: two-branch, uniform line, star of short stubs. Reduced by the pinned reducer, so cases are **reachable** |
| `rand_pi` | 3,000 | Random pi models and Elmore values injected with `sta::set_pi_model` / `sta::set_elmore`; pin caps included. Cases are **injected** |
| `plat_spef` | 1,500 | SPEF two-branch nets whose DMP waveform plateau a = Rpi/(Rd+Rpi) is placed near vth, vh or vl. Reachable |
| `plat_pi` | 1,500 | The injected equivalent of `plat_spef` |
| `sing_pi` | 800 | Load Elmore set to 1/p1 or 1/p2 of the driver waveform (±0, 1e-9, 1e-6, 1e-3) |

## 4. Exact check commands

- **Extraction.** In the fixture directory, `P05_OUT=RUN sta -no_init -no_splash -exit p05_extract.tcl` (`lab-requests/p05_extract.tcl`, SHA-256 `6ab3c290…`).
  - It reads the gate delay, driver slew, wire delay and load slew from the timing graph (`Edge::arc_delay`, `Vertex::slew`).
  - It reads Ceff, the pi model, Rd, t0, dt, the DMP variant and failure reasons from `report_delay_calc_cmd` with `dmp_ceff` debug output at level 3, captured for that single arc.
  - Raw output: `/ws/runs/REQ-0008/raw.tsv`, 22,794,491 bytes, SHA-256 `23cb3e8e123dbad4d1dfccaa53e773de23790a70bd68c2e9fe5309a8b24acf5b` (kept on the server).
- **Check.** `python3 p05_check.py FX RUN/raw.tsv RUN/check` (`lab-requests/p05_check.py`, SHA-256 `de153b24…`).
  - It replicates OpenSTA's bilinear table lookup (`TableModel.cc` 1012-1068, 1443-1463) and the slew clip at 0 (`TableModel.cc` 130-132).
  - The DMP debug `in_slew` equals the vertex slew used by the checker to 1.5e-7 (checked on the REQ-0007 raw data).
- **Results.** `evidence/REQ-0008-summary.json` and `evidence/REQ-0008-counterexamples.csv`. Full per-arc results are in the lab-results inbox (`REQ-0008/out/results_*.csv.gz`).

## 5. Expected invariants, observations and labels

Notation:

| Symbol | Meaning |
|---|---|
| s | input slew |
| C | C1+C2 of the reduced pi model |
| T(s,C), D(s,C) | slew and delay tables |
| s_d | driver slew |
| w | wire delay |
| s_l | load slew |
| τ | load Elmore delay of the reduced model |
| k | slew derate |
| dt, Rd | DMP's internal ramp duration and drive resistance |

Single library per scenario throughout, so `thresholdAdjust` is a no-op (`DelayCalcBase.cc` 127-153).

| ID | Invariant tested | Arcs | Violations | Worst (reachable, consistent tables) | Label |
|---|---|---|---|---|---|
| **P3** | s_d ∈ [min, max] of T(s, C') for C' ∈ [0, C] | 19,600 | 3,553 (18%), all on the DMP waveform path; 896 of 8,292 reachable arcs with consistent tables | n1246 (BUFB_X16, `two_branch`): s_d = 0.5972 ns, box max 0.4478 ns (ratio 1.334). Low side: s_d = 0.966 × box min | **falsified** |
| P3-ext | Same with C' ∈ [0, 1.01·C] | 19,600 | 3,083 | — | **falsified** |
| **P4** | w ≤ τ | 52,088 | 100; 12 of 17,978 reachable arcs with consistent tables | n7075 (BUFA_X1, plateau a = 0.756): w = 0.198922 ns, τ = 0.195235 ns (ratio 1.019, +3.7 ps). With the inconsistent `BUFA_W4` tables: ratio up to 1.159 (n730) | **falsified** |
| **P5** | s_l ≤ s_d + τ·ln((1−vl)/(1−vh))/k (OpenSTA's own single-pole increment, `DelayCalcBase.cc` 108-124) | 52,088 | 3,025; 1,543 of 17,978 reachable arcs with consistent tables | n6519 (BUFA_X1, plateau a = 0.807): s_l = 0.3287 ns, bound 0.1724 ns (ratio 1.907). Maximum over all arcs 2.14 | **falsified** |
| P3-lo | s_d ≥ 0 | 19,600 | 0 | — | code-argument-only; finite-tests-pass |
| P4-lo | w ≥ 0 | 52,088 | 0 (minimum w = 2e-10 ns) | — | code-argument-only; finite-tests-pass |
| P5-lo | s_l ≥ s_d | 52,088 | 0 | — | code-argument-only; finite-tests-pass |
| CAP | DmpCap path: s_d = T(s,C), w = τ, s_l = s_d | 603 driver, 1,613 wire | 0 (\|s_d/T−1\| ≤ 2.9e-6; \|w/τ−1\| ≤ 2e-7; s_l = s_d exactly) | — | code-argument-only; finite-tests-pass |
| SMALL | DMP waveform path with τ < 1e-3·s_d: w = τ, s_l = s_d | 15,816 wire | 0 | — | code-argument-only; finite-tests-pass |
| BR3 | Waveform path: s_d ≤ (dt + 2C'(Rd+Rpi))/k, with C' = C (Pi) or C1 (c2=0) | 18,997 | 0 | — | code-argument-only; finite-tests-pass. **Not a computable rule**: dt is internal |
| BR4 | w ≤ dt + 2C'(Rd+Rpi) + 2τ | 50,475 | 0 | — | code-argument-only; finite-tests-pass; same caveat |
| BR5 | s_l ≤ max(s_d, (dt + 2C'(Rd+Rpi) + 2τ)/k) | 50,475 | 0 | — | code-argument-only; finite-tests-pass; same caveat |
| ADT | dt ≤ 1.01·k·T(s, Ceff)/(vh−vl) (would make BR3-BR5 computable) | 18,997 | 0 (maximum ratio 1.0077) | — | finite-tests-pass; **unresolved** as proof |
| LAG | w ≤ τ·ln(vh/(vh−vth)) + k·s_d + 0.02·gate delay (candidate repair of P4) | 52,088 | 47 | — | **falsified** |
| P2-Pi | Pi path: gate delay = D(s, Ceff), Ceff ∈ [0, 1.01·C] | 16,739 | 0 (Ceff ∈ [0, C] in every case) | — | code-argument-only; finite-tests-pass |
| P2-Z | c2=0 path: gate delay = table value | 2,258 | 2,171 differ | — | **falsified** as stated. Delay ∈ [D(s,0), D(s,C)] in every case: finite-tests-pass, **unresolved** as proof |

Arc counts include rise and fall. "Reachable" means the counterexample arose from a SPEF RC tree reduced by the pinned reducer, not from an injected model.

## 6. Code arguments

All locators are in `e01d3f16`.

**A. Path selection.** `DmpCeffDelayCalc::setCeffAlgorithm` (`DmpCeff.cc` 1545-1585) chooses the variant:

| Variant | Condition |
|---|---|
| `DmpCap` | Rd < 1e-2 Ω, or Rpi < 1e-3·Rd, or C1 = 0, or C1 < 1e-3·C2, or Rpi = 0 |
| `DmpZeroC2` | C2 < 1e-3·C1 |
| `DmpPi` | otherwise |

- Rd comes from `gateModelRd` (1630-1649), a 1 fF finite difference of the delay table at C, so it depends on the input slew.
- Without a parasitic, `LumpedCapDelayCalc` uses the table at the lumped load (`DmpCeff.cc` 1531-1542).
- `GraphDelayCalc::loadCap` (`GraphDelayCalc.cc` 1255-1271) discards a pi model whose capacitance is below the pin capacitance. SPEF reductions include pin caps, so this applies only to injected models; the fixtures were corrected for it.

**B. CAP path.**
- `DmpCap::init` sets Ceff = C1+C2 (751).
- `gateDelaySlew` returns the table delay and the clipped table slew at (s, C) (755-763, `TableModel.cc` 104-135).
- `DmpCap::loadDelaySlew` returns w = τ and s_l = s_d (766-773).
- A load without an Elmore entry gets w = 0 and s_l = s_d (`DmpDelayCalc.cc` 113-121).
- Label: code-argument-only (complete reading of these paths; no machine-checked proof).

**C. Waveform path, driver slew (why P3 fails).** `DmpPi::gateDelaySlew` (915-949) reports the gate delay as D(s, Ceff), but the driver slew is measured on the pi-model waveform: s_d = (t_h − t_l)/k (`findDriverDelaySlew` 479-489). Nothing ties this measured slew to the table-slew box.
- The fitted ramp matches the table at Ceff, but the full pi load keeps charging after the threshold crossing (`ipiIceff` 1027-1043 matches charge only up to the crossing). The tail is therefore slower or faster than any lumped C' ∈ [0, C].
- `DmpZeroC2` (1222-1241) also returns the gate delay from the waveform crossing, not the table. This is the P2-Z finding.
- Fallbacks:
  - if the parameter fit fails: table at C;
  - if the crossing search fails: table at Ceff.
- Newton returns after an unchecked final step of at most 1% (`newtonRaphson` 1294-1311, tolerance `driver_param_tol` 54). Ceff ∈ [0, C] is checked only at the last evaluation (971-974), hence the [0, 1.01·C] statement.

**D. Waveform path, loads (why P4 and P5 fail).** `DmpAlg::loadDelaySlew` (555-607):
- Vl is the single-pole (τ) response to the driver waveform (`Vl0` 1057-1074).
- w = t_vth(Vl) − t_vth(Vo) and s_l = (t_vh − t_vl)/k come from root finding.
- The only clamps are: w < 0 is replaced by τ (585-591); s_l < s_d is replaced by s_d (592-597); exceptions fall back to (τ, s_d) (601-605).
- No upper clamp exists. When Vo plateaus just above a threshold, Vl approaches that level slowly. That produces w > τ (P4) and s_l far above s_d + τ·ln4 (P5), as observed in the plateau families.
- Further numerical facts:
  - `exp2` (1687-1709) approximates exp by (1 + x/4096)^4096 and returns 0 below x = −12;
  - D3 and D4 in `Vl0` divide by (p1 − 1/τ) and (p2 − 1/τ). The singular family produced no non-finite value; 75 `find Vl crossing failed` fallbacks were logged.

**E. Lower bounds.**
- P3-lo: table slews are clipped at 0 (`TableModel.cc` 130-132); the waveform slew satisfies t_h ≥ delay ≥ t_l by the brackets in 484-486.
- P4-lo: every return path gives w ≥ 0 (565, 590, 603).
- P5-lo: every return path gives s_l ≥ s_d (566, 596, 604).
- A NaN crossing never passes the convergence test (`FindRoot.cc` 89-93) and so ends in a failure, which falls back to (τ, s_d).
- Label: code-argument-only.

**F. Bracket bounds BR3-BR5.** `findRoot` (`FindRoot.cc` 41-103):
- returns failure if the initial bracket does not straddle a root (50-55);
- accepts a Newton step only inside the current bracket (76-79), otherwise bisects (80-84);
- updates the bracket monotonically (96-101).

So every returned crossing lies in its initial bracket:
- Vo crossings lie in [t0, t0 + dt + 2C'(Rd + Rpi)] (1076-1080, 1269-1273);
- Vl crossings lie in [t0, that bound + 2τ] (631-635).

This gives BR3-BR5. They depend on the internal dt. ADT would bound dt from the tables, but Newton termination is a step-size test, not a residual test, so ADT is not established by the code.

## 7. Side effects and threats found (owner item U7)

These are recorded as threats with required falsification tests. They were not investigated as experiments.

- **Multi-driver nets.** Delay calculation for a driver of a multi-driver net uses all parallel drivers (`GraphDelayCalc.cc` 940-967). A cone-restricted refinement must close over every driver of such a net. Required test: a multi-driver fixture whose second driver lies outside the fan-in cone.
- **Net-level coupling.** The driver waveform depends on the whole net's pi model (all loads), so refinement must recompute whole nets, not only the cone's load pins. Required test: a net with one cone load and one off-cone load; check exactness.
- **Multi-library scenarios.** `thresholdAdjust` can make w negative or change s_l by a ratio. Any bound rule must apply it with interval arithmetic. Required test: a two-library fixture.
- **Pi models below the pin caps** are ignored (`GraphDelayCalc.cc` 1263-1269). This affects only injected or estimated parasitics.
- **Build deviation:** the byacc parser generator (§ 2).
- **Untested code paths:** 3-D tables (P1), `dmp_ceff_two_pole`, CCS and POCV paths are out of scope or untested.

## 8. Conclusion and scope

- P3, P4 and P5, as stated in `proposal.md` round 0, are **falsified** for the pinned calculator.
  - Counterexamples are reachable from SPEF RC trees through the pinned reducer, with internally consistent tables.
  - The P4 violations with consistent tables are small (at most 1.9% here) but nonzero.
- On the DMP waveform path (`DmpPi`, `DmpZeroC2`), no computable bound is established. The bracket bounds need the unproven ADT and are loose (several RC time constants).
- On the capacitive path (`DmpCap`, and nets without parasitics), the bound rules are exact table lookups at C. Label: **code-argument-only + finite-tests-pass**.
- Per the owner's decision and kill criterion K2, the guarantee claim is narrowed. Certificates may only use cones whose data nets are all on the capacitive path for every slew in the box. Everything else is refined exactly. See `proposal.md`.
- The conclusions hold for the synthetic fixtures and the stated code reading. They do not estimate how often each path occurs in real designs. That is a measurement deferred to the agreed experiment plan (owner item U4).
