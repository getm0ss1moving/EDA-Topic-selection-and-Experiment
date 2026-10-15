#!/bin/bash
# REQ-0009 (tooling, lab234, no network): record the build configuration of the
# OpenSTA binary used by REQ-0006..0008 (compiler, CMake cache flags, tool versions).
set -u
OUT=$(pwd)/out; mkdir -p "$OUT"
P=/ws/tools/p05; B=/ws/build; REV=e01d3f163f483f233db00410b6515a767a6ca03b
export PATH=$P/bin:/ws/data/src/cmake-3.27.9/bin:/usr/bin:/bin; export LD_LIBRARY_PATH=$P/lib
{
  echo "## versions"; gcc --version | head -1; cmake --version | head -1
  "$P/bin/yacc" -V 2>&1 | head -1; "$P/bin/flex" --version; "$P/bin/swig" -version | grep -i version
  echo 'puts [info patchlevel]' | "$P/bin/tclsh8.6"; echo "tclsh -> $(readlink $P/bin/tclsh)"
  echo "## bison wrapper"; sha256sum "$P/bin/bison"; "$P/bin/bison" --version
  echo "## OpenSTA CMakeCache (selected)"
  grep -E '^(CMAKE_BUILD_TYPE|CMAKE_CXX_COMPILER:|CMAKE_CXX_FLAGS|CMAKE_C_FLAGS_RELEASE|BISON_EXECUTABLE|FLEX_EXECUTABLE|FLEX_INCLUDE_DIR|SWIG_EXECUTABLE|TCL_LIBRARY|TCL_INCLUDE_PATH|USE_CUDD|USE_TCL_READLINE|ZLIB_LIBRARY|Eigen3_DIR)' "$B/opensta/CMakeCache.txt"
  echo "## compile flags of DmpCeff.cc"
  grep -rh "CXX_FLAGS\|CXX_DEFINES" "$B/opensta/CMakeFiles/OpenSTA.dir/flags.make" 2>&1 | head -5
  echo "## binaries"; sha256sum /ws/tools/opensta-$REV/bin/sta "/ws/data/src/OpenSTA-$REV/app/sta"
  echo "## generated parser provenance"; head -3 "$B/opensta/LibertyParse.cc" 2>&1; ls "$B/opensta"/*Parse*.cc 2>&1 | head
} > "$OUT/build-config.txt" 2>&1
