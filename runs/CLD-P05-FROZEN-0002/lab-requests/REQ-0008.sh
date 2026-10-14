#!/bin/bash
# REQ-0008 (property-check, lab234, no network): FULL run of the P3-P5
# fixture checks with targeted plateau and near-singular families. Re-checks
# the pinned OpenSTA binary built by REQ-0005, then runs the P3-P5
# fixture checks (synthetic libraries and RC trees only; no real design, no
# runtime measurement). Inputs: p05_fixtures.py, p05_extract.tcl, p05_check.py.
set -u
JOB=$(pwd)
OUT=$JOB/out
mkdir -p "$OUT"
HERE=$(cd "$(dirname "$0")" && pwd)
REV=e01d3f163f483f233db00410b6515a767a6ca03b
OSTA=/ws/data/src/OpenSTA-$REV
STA=/ws/tools/opensta-$REV/bin/sta
export PATH=/ws/tools/p05/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/ws/tools/p05/lib
RUN=/ws/runs/REQ-0008
rm -rf "$RUN" && mkdir -p "$RUN/fx" "$RUN/check"
LOG=$OUT/run-log.txt
: > "$LOG"
note() { echo "## $* $(date -u +%FT%TZ)" >> "$LOG"; }

find_input() {  # locate a request input file
  for d in "$HERE" "$JOB/in" "$JOB"; do [ -f "$d/$1" ] && { echo "$d/$1"; return; }; done
  echo "MISSING_$1"
}
FXPY=$(find_input p05_fixtures.py); EXTCL=$(find_input p05_extract.tcl); CHKPY=$(find_input p05_check.py)
sha256sum "$FXPY" "$EXTCL" "$CHKPY" > "$OUT/harness-sha256.txt" 2>&1

note setup
mkdir -p "$(dirname "$STA")"
cp "$OSTA/app/sta" "$STA" && chmod 755 "$STA"
{
  echo "binary: $(sha256sum "$STA")"
  echo "source tree status (tracked files; untracked build outputs listed with ??):"
  git -C "$OSTA" status --porcelain 2>&1 | head -20
  echo "HEAD: $(git -C "$OSTA" rev-parse HEAD 2>&1)"
  printf 'puts "sta_version [sta::version] git_sha1 [sta::git_sha1]"\nputs "delay_calc_names [sta::delay_calc_names]"\n' > "$RUN/smoke.tcl"
  "$STA" -no_init -no_splash -exit "$RUN/smoke.tcl" 2>&1
} > "$OUT/setup.txt" 2>&1

note fixtures
python3 "$FXPY" "$RUN/fx" 3000 3000 20261015 1500 800 > "$OUT/fixtures.log" 2>&1 || note fixtures FAILED
( cd "$RUN/fx" && sha256sum p05a.lib p05b.lib p05.v p05.spef p05_inputs.tcl p05_nets.tcl cases.json ) > "$OUT/fixture-sha256.txt" 2>&1
cp "$RUN/fx/p05a.lib" "$RUN/fx/p05b.lib" "$OUT/" 2>/dev/null

note extract
cp "$EXTCL" "$RUN/fx/p05_extract.tcl"
( cd "$RUN/fx" && P05_OUT="$RUN" "$STA" -no_init -no_splash -exit p05_extract.tcl ) > "$RUN/extract.log" 2>&1 || note extract FAILED
tail -40 "$RUN/extract.log" > "$OUT/extract.tail.txt"
grep -c . "$RUN/extract.log" >> "$OUT/extract.tail.txt"
grep -iE "warning|error" "$RUN/extract.log" | sort | uniq -c | sort -rn | head -30 > "$OUT/extract.warnings.txt"
wc -l "$RUN/raw.tsv" >> "$LOG" 2>&1
sha256sum "$RUN/raw.tsv" > "$OUT/raw-sha256.txt" 2>&1; ls -la "$RUN/raw.tsv" >> "$OUT/raw-sha256.txt" 2>&1

note check
python3 "$CHKPY" "$RUN/fx" "$RUN/raw.tsv" "$RUN/check" > "$OUT/check.log" 2>&1 || note check FAILED
cp "$RUN/check/summary.json" "$RUN/check/counterexamples.csv" "$OUT/" 2>/dev/null
gzip -c "$RUN/check/results_G.csv" > "$OUT/results_G.csv.gz" 2>/dev/null
gzip -c "$RUN/check/results_W.csv" > "$OUT/results_W.csv.gz" 2>/dev/null
{ echo "fixtures: python3 p05_fixtures.py FX 3000 3000 20261015 1500 800"; echo "extract: (cd FX && P05_OUT=RUN sta -no_init -no_splash -exit p05_extract.tcl)"; echo "check: python3 p05_check.py FX RUN/raw.tsv RUN/check"; } > "$OUT/commands.txt"
note done
