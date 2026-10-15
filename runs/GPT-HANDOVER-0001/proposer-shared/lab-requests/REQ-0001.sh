#!/bin/bash
# REQ-0001 (tooling, lab231, network): probe the build environment and fetch
# pinned OpenSTA e01d3f163f483f233db00410b6515a767a6ca03b from GitHub.
# Every network access is logged to out/network-log.tsv (url, revision, sha256).
set -u
JOB=$(pwd)
OUT=$JOB/out
mkdir -p "$OUT" /ws/tools /ws/data/src
REV=e01d3f163f483f233db00410b6515a767a6ca03b
URL=https://github.com/The-OpenROAD-Project/OpenSTA.git
TGZ=https://codeload.github.com/The-OpenROAD-Project/OpenSTA/tar.gz/$REV
NETLOG=$OUT/network-log.tsv
printf 'url\tresolved_revision\tsha256\tnote\n' > "$NETLOG"

{
  echo "## host"; hostname; uname -srm; head -4 /etc/os-release 2>/dev/null
  echo "nproc=$(nproc)"; free -g 2>/dev/null | head -2; df -h /ws | tail -1
  echo "## tools"
  for t in gcc g++ clang cmake make ninja git tclsh swig bison flex python3 curl sha256sum tar; do
    printf '%s: ' "$t"; command -v "$t" || echo MISSING
  done
  gcc --version 2>&1 | head -1; cmake --version 2>&1 | head -1
  swig -version 2>&1 | grep -i 'version'; bison --version 2>&1 | head -1; flex --version 2>&1
  echo 'puts [info patchlevel]' | tclsh 2>&1
  echo "## headers and libraries"
  ls -d /usr/include/eigen3 /usr/include/tcl*/tcl.h /usr/include/tcl.h /usr/include/zlib.h 2>&1
  ls /usr/lib/x86_64-linux-gnu/libtcl* /usr/lib64/libtcl* 2>/dev/null | head
  python3 -c "import numpy; print('numpy', numpy.__version__)" 2>&1 | tail -1
  python3 -c "import scipy; print('scipy', scipy.__version__)" 2>&1 | tail -1
} > "$OUT/env.txt" 2>&1

# Marker to test whether /ws is shared with lab234.
echo "written by REQ-0001 on $(hostname)" > /ws/data/marker-REQ-0001.txt

DEST=/ws/data/src/OpenSTA-$REV
if command -v git >/dev/null 2>&1; then
  rm -rf "$DEST.tmp" && mkdir -p "$DEST.tmp"
  if git -C "$DEST.tmp" init -q \
     && git -C "$DEST.tmp" remote add origin "$URL" \
     && git -C "$DEST.tmp" fetch -q --depth 1 origin "$REV" \
     && git -C "$DEST.tmp" checkout -q FETCH_HEAD; then
    GOT=$(git -C "$DEST.tmp" rev-parse HEAD)
    ASHA=$(git -C "$DEST.tmp" archive --format=tar HEAD | sha256sum | cut -d' ' -f1)
    rm -rf "$DEST" && mv "$DEST.tmp" "$DEST"
    printf '%s\t%s\t%s\t%s\n' "$URL" "$GOT" "$ASHA" "sha256 of git archive --format=tar HEAD" >> "$NETLOG"
  else
    echo "git fetch of $REV failed" >> "$OUT/env.txt"
  fi
fi

# Tarball as a second, independent record of the same revision.
if curl -fsSL --max-time 300 -o /ws/data/src/OpenSTA-$REV.tar.gz "$TGZ"; then
  TSHA=$(sha256sum /ws/data/src/OpenSTA-$REV.tar.gz | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\n' "$TGZ" "$REV" "$TSHA" "GitHub-generated tarball (not guaranteed byte-stable over time)" >> "$NETLOG"
  if [ ! -d "$DEST" ]; then
    mkdir -p "$DEST" && tar -xzf /ws/data/src/OpenSTA-$REV.tar.gz -C "$DEST" --strip-components=1
  fi
else
  echo "tarball download failed" >> "$OUT/env.txt"
fi

# Repository-internal license evidence and hashes of the files read by the proposer.
if [ -d "$DEST" ]; then
  ( cd "$DEST" && sha256sum LICENSE README.md CMakeLists.txt dcalc/DmpCeff.cc dcalc/DmpDelayCalc.cc \
      dcalc/FindRoot.cc dcalc/DelayCalcBase.cc dcalc/LumpedCapDelayCalc.cc liberty/TableModel.cc \
      parasitics/ReduceParasitics.cc dcalc/GraphDelayCalc.cc ) > "$OUT/opensta-file-sha256.txt" 2>&1
  head -3 "$DEST/LICENSE" > "$OUT/opensta-license-head.txt" 2>&1
  du -sh "$DEST" >> "$OUT/env.txt" 2>&1
fi
echo "done" >> "$OUT/env.txt"
