#!/bin/bash
# REQ-0002 (tooling, lab234, no network): probe the build host and check that
# /ws is shared with lab231 (marker and OpenSTA tree from REQ-0001).
set -u
OUT=$(pwd)/out
mkdir -p "$OUT"
REV=e01d3f163f483f233db00410b6515a767a6ca03b
{
  echo "## host"; hostname; uname -srm; head -4 /etc/os-release 2>/dev/null
  echo "nproc=$(nproc)"; free -g 2>/dev/null | head -2; df -h /ws | tail -1
  echo "## shared workspace check"
  cat /ws/data/marker-REQ-0001.txt 2>&1
  ls -d /ws/data/src/OpenSTA-$REV 2>&1 && sha256sum /ws/data/src/OpenSTA-$REV/dcalc/DmpCeff.cc 2>&1
  echo "## tools"
  for t in gcc g++ clang cmake make ninja git tclsh tclsh8.6 swig swig4.0 swig3.0 bison yacc byacc flex lex m4 \
           autoconf automake libtoolize autopoint pkg-config perl python3 makeinfo help2man gettext; do
    printf '%s: ' "$t"; command -v "$t" || echo MISSING
  done
  gcc --version 2>&1 | head -1; cmake --version 2>&1 | head -1
  for t in swig swig4.0 swig3.0; do command -v $t >/dev/null && $t -version 2>&1 | grep -i version; done
  command -v bison >/dev/null && bison --version 2>&1 | head -1
  command -v flex >/dev/null && flex --version 2>&1
  command -v m4 >/dev/null && m4 --version 2>&1 | head -1
  command -v autoconf >/dev/null && autoconf --version 2>&1 | head -1
  command -v automake >/dev/null && automake --version 2>&1 | head -1
  echo "## headers and libraries"
  ls -d /usr/include/eigen3 /usr/local/include/eigen3 /usr/include/tcl8.6/tcl.h /usr/include/tcl.h /usr/include/zlib.h \
        /usr/include/pcre2.h /usr/include/pcre.h /usr/include/readline/readline.h 2>&1
  ls /usr/lib/x86_64-linux-gnu/libtcl* /usr/lib/x86_64-linux-gnu/libpcre* 2>/dev/null | head -20
  python3 --version 2>&1
  python3 -c "import numpy; print('numpy', numpy.__version__)" 2>&1 | tail -1
  ls /ws/tools 2>&1 | head
} > "$OUT/env.txt" 2>&1
echo done >> "$OUT/env.txt"
