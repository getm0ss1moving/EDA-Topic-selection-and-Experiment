# Industry Gap

## Engineer persona and workflow pain

**Persona.** A timing-closure or signoff engineer, or the owner of a closure flow, responsible for an MCMM scenario set: library corners × RC corners × modes. The persona matches the brief's engineering user (`config/research-brief.json` line 67). Practitioner validation is still pending.

**Pain [OBS].** Each closure iteration and the final signoff need timing at every scenario, and scenario counts run from 16 to hundreds (SRC-021, SRC-015, SRC-020, SRC-019). The practical choice today is:

1. Run everything. Cost grows roughly with the scenario count, and a vendor notes that core scaling flattens beyond eight cores (SRC-020).
2. Reduce the set by experience, greedy coverage or prediction, and accept a risk that is covered with extra margin (SRC-021: +10 to +20 ps hold uncertainty) or with "tolerance for risk" (SRC-020).

**Stated requirement [OBS].** "Reduction must not lead to a loss in accuracy or missed failing endpoints" (SRC-020, a vendor statement).

## Open implementations and exact versions

- **OpenSTA `e01d3f163f483f233db00410b6515a767a6ca03b`** (the `src/sta` submodule of OpenROAD `b16bda7e82721d10566ff7e2b68f1ff0be9f9e38`; SRC-010):
  - multi-corner analysis in one run: `define_corners` (SRC-005), analysis points per corner (SRC-006);
  - default `dmp_ceff_elmore` delay calculator (SRC-003);
  - no scenario-reduction or dominance command found in the inspected Tcl command files (`search-log.md`).
  - [INF] Open flows that time all corners therefore pay full cost per corner. Open flows that time one corner (ORFS ships only the SKY130 tt library, SRC-029) do not check the others at all.
- **OpenROAD-flow-scripts** (master `e5cc6e79…`, SRC-052): ASAP7 NLDM libraries at FF/SS/TT (SRC-028), a single OpenRCX rules file per platform (SRC-036), and designs `aes`, `ibex_sv`, `jpeg` (SRC-034).
- **No open implementation of corner reduction was found.** [Absence of evidence: open implementations were searched only through ORFS and OpenSTA.]

## Public commercial capability evidence

- **Synopsys** (patents describe methods; product behavior is unknown):
  - "Signoff-safe multi-corner reduction" (SRC-017): dominant corner, ratio estimation, ML, object marking; 3x-12x speedups claimed by the applicant.
  - "Priori corner and mode reduction" (SRC-018): synthetic worst corners and mode merging.
- **IBM:** empirical slack cutoffs for multi-corner STA (SRC-016).
- **Cadence:** an Encounter Timing System marketing article on handling hundreds of views by reduction and parallelism (SRC-020).
- **Abelite:** a vendor white paper arguing that corner-based signoff can miss violations even with 160-495 corners and promoting statistical signoff (SRC-019).
- **Unknown:** whether any shipping commercial timer implements *sound* per-endpoint scenario screening. This is not established either way, and public marketing cannot settle it (`docs/EVIDENCE.md` lines 7 and 23).

## Matched conditions and incomparable conditions

- **Matched (planned):** same netlist, SDC, libraries, parasitics, engine commit, thread count, container, and 2 CPU / 4 GiB limits for the baseline (full OpenSTA MCMM) and the candidate. The comparison runs inside one open engine, so no commercial-tool parity is claimed (`config/research-brief.json` line 65).
- **Incomparable:**
  - industrial speedups in SRC-017, SRC-015 and SRC-022 to SRC-025: different designs, nodes, corner counts and tools;
  - advanced-node corner counts (hundreds) vs open-PDK corner sets (3 for ASAP7, up to 16 PVT for SKY130, a single RC corner);
  - SI-aware commercial signoff vs OpenSTA without SI.

## Algorithm gap versus data, integration, and engineering gap

- **Algorithm gap (the claimed one; unproven):** no accessed method certifies non-violation per (endpoint, scenario) soundly against the reference engine's delay semantics while reproducing full decisions (CLM-015). Whether this gap is real depends on SRC-012 (K1) and on commercial internals that cannot be inspected.
- **Integration gap (certain but not research):** OpenSTA has no scenario-reduction feature at all. Porting a known heuristic, such as dominant corners, would be engineering, not a contribution.
- **Data gap (certain):** open multi-corner benchmarks with multiple RC corners are missing. ORFS ships one rules file per platform, and OpenRCX rules are corner-specific (SRC-035, SRC-036). This limits how strongly H3 (the safety contrast) can be tested on open data (CH3).

## Adoption costs and downstream validation

**Adoption costs [INF]:**

- implementation inside the timer (bound pass, clock-only search, cone-restricted refinement);
- an audit of soundness properties for each delay calculator. P2-P5 are specific to `dmp_ceff_elmore`, and each additional calculator (CCS, Arnoldi) needs its own proof or audit;
- extra memory for bound arrays per scenario;
- user trust: certificates must be logged and reproducible.

**Downstream validation required:**

- equality of D_M(S) with full analysis on every evaluated design and scenario set (EXP-006, EXP-007);
- an audit of bound validity at arc level (EXP-002);
- practitioner confirmation of what M and what speedup matter (U9).

**Not claimed:** silicon correlation or signoff-tool parity.
