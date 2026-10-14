#!/bin/bash
# REQ-0005 (tooling, lab234, no network): retry of REQ-0004. Reuses the toolchain
# REQ-0004 built in /ws/tools/p05 when present, adds the 'tclsh' name that
# OpenSTA etc/TclEncode.tcl execs, and builds unmodified OpenSTA e01d3f16.
# Full logs stay in /ws/build/logs; tails and a summary are returned in out/.
set -u
OUT=$(pwd)/out
mkdir -p "$OUT"
SRC=/ws/data/src
P=/ws/tools/p05
B=/ws/build
LOGS=$B/logs
REV=e01d3f163f483f233db00410b6515a767a6ca03b
OSTA=$SRC/OpenSTA-$REV
J=$(nproc)
mkdir -p "$P/bin" "$B" "$LOGS"
export PATH=$P/bin:$SRC/cmake-3.27.9/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=$P/lib
SUM=$OUT/build-summary.txt
: > "$SUM"
CMLIC=$(find "$SRC/cmake-3.27.9" -path "*/doc/cmake/Copyright.txt" | head -1)
{ echo "## CMake license: ${CMLIC#$SRC/} sha256=$(sha256sum "$CMLIC" | cut -d' ' -f1)"; head -8 "$CMLIC"; } > "$OUT/cmake-license.txt" 2>&1

step() {  # name, then command string
  local name=$1; shift
  echo "## $name start $(date -u +%FT%TZ)" >> "$SUM"
  if bash -c "$*" > "$LOGS/$name.log" 2>&1; then
    echo "## $name OK $(date -u +%FT%TZ)" >> "$SUM"
  else
    echo "## $name FAILED (exit $?) $(date -u +%FT%TZ)" >> "$SUM"
    tail -60 "$LOGS/$name.log" > "$OUT/$name.FAILED.tail.txt"
    exit 1
  fi
}
fresh() { rm -rf "$B/$1" && cp -a "$SRC/$2" "$B/$1"; }

[ -x $P/bin/yacc ] || { fresh byacc byacc; step byacc "cd $B/byacc && ./configure --prefix=$P && make -j$J && make install"; }

[ -x $P/bin/flex ] || { fresh flex flex-2.6.4; step flex "cd $B/flex && CFLAGS='-O2 -D_GNU_SOURCE' ./configure --prefix=$P --disable-nls && make -j$J && make install"; }

[ -x $P/bin/tclsh8.6 ] || { fresh tcl tcl8.6.13; step tcl "cd $B/tcl/unix && ./configure --prefix=$P --enable-shared --enable-threads && make -j$J && make install"; }
[ -e $P/bin/tclsh ] || ln -s tclsh8.6 $P/bin/tclsh

[ -x $P/bin/swig ] || { fresh swig swig-4.1.1; step swig "cd $B/swig && ./autogen.sh && ./configure --prefix=$P --without-pcre --without-alllang YACC='$P/bin/yacc' && make -j$J && make install"; }

[ -f $P/share/eigen3/cmake/Eigen3Config.cmake ] || { rm -rf "$B/eigen-build"; step eigen "cmake -S $SRC/eigen-3.3.7 -B $B/eigen-build -DCMAKE_INSTALL_PREFIX=$P -DBUILD_TESTING=OFF -DEIGEN_BUILD_DOC=OFF && cmake --install $B/eigen-build"; }

# GNU-bison-style command line (as emitted by CMake FindBISON/BISON_TARGET) -> Berkeley yacc.
cat > "$P/bin/bison" <<'WRAP'
#!/bin/bash
# bison-to-byacc wrapper for CMake BISON_TARGET. It does not claim to be GNU Bison.
YACC=/ws/tools/p05/bin/yacc
prefix=""; out=""; hdr=""; defs=0; input=""
while [ $# -gt 0 ]; do
  case "$1" in
    --version) echo "byacc-wrapper: $($YACC -V 2>&1 | head -1)"; exit 0 ;;
    --name-prefix=*) prefix="${1#--name-prefix=}" ;;
    -p) prefix="$2"; shift ;;
    -d|--defines) defs=1 ;;
    --defines=*) defs=1; hdr="${1#--defines=}" ;;
    -v|--verbose) ;;
    -o) out="$2"; shift ;;
    --output=*) out="${1#--output=}" ;;
    -*) echo "bison-wrapper: unsupported option $1" >&2; exit 2 ;;
    *) input="$1" ;;
  esac
  shift
done
[ -n "$out" ] && [ -n "$input" ] || { echo "bison-wrapper: need -o and input" >&2; exit 2; }
if [ $defs = 1 ] && [ -z "$hdr" ]; then
  ext="${out##*.}"; hdr="${out%.*}.${ext//c/h}"
fi
args=()
[ -n "$prefix" ] && args+=(-p "$prefix")
[ -n "$hdr" ] && args+=(-H "$hdr")
exec "$YACC" "${args[@]}" -o "$out" "$input"
WRAP
chmod +x "$P/bin/bison"

rm -rf "$B/opensta"
step opensta_cmake "cmake -S $OSTA -B $B/opensta -DCMAKE_BUILD_TYPE=Release \
  -DTCL_LIBRARY=$P/lib/libtcl8.6.so -DTCL_INCLUDE_PATH=$P/include \
  -DBISON_EXECUTABLE=$P/bin/bison -DFLEX_EXECUTABLE=$P/bin/flex -DFLEX_INCLUDE_DIR=$P/include \
  -DSWIG_EXECUTABLE=$P/bin/swig -DCMAKE_PREFIX_PATH=$P -DEigen3_DIR=$P/share/eigen3/cmake"
step opensta_build "cmake --build $B/opensta -j $J"

STA=$(find "$B/opensta" -maxdepth 2 -type f -name sta -perm -u+x | head -1)
mkdir -p /ws/tools/opensta-$REV/bin
cp "$STA" /ws/tools/opensta-$REV/bin/sta
cat > "$B/smoke.tcl" <<'TCL'
puts "sta_version [sta::version]"
puts "git_sha1 [sta::git_sha1]"
puts "delay_calc_names [sta::delay_calc_names]"
TCL
step smoke "/ws/tools/opensta-$REV/bin/sta -no_init -no_splash -exit $B/smoke.tcl"

{
  echo "## versions"
  gcc --version | head -1; cmake --version | head -1
  "$P/bin/yacc" -V 2>&1 | head -1; "$P/bin/flex" --version; "$P/bin/swig" -version | grep -i version
  echo 'puts [info patchlevel]' | "$P/bin/tclsh8.6"
  echo "tclsh -> $(readlink $P/bin/tclsh)"
  echo "## opensta cache flags"
  grep -E '^(CMAKE_BUILD_TYPE|CMAKE_CXX_COMPILER|CMAKE_CXX_FLAGS_RELEASE|CMAKE_CXX_FLAGS|BISON_EXECUTABLE|FLEX_EXECUTABLE|SWIG_EXECUTABLE|TCL_LIBRARY|USE_CUDD|ZLIB_LIBRARY)' "$B/opensta/CMakeCache.txt"
  echo "## binary"
  sha256sum /ws/tools/opensta-$REV/bin/sta; ls -la /ws/tools/opensta-$REV/bin/sta
  echo "## smoke"
  cat "$LOGS/smoke.log"
} >> "$SUM" 2>&1
tail -30 "$LOGS/opensta_build.log" > "$OUT/opensta_build.tail.txt"
grep -iE "warning:.*(parse|lex)|error" "$LOGS/opensta_build.log" | head -40 > "$OUT/opensta_build.parser-warnings.txt"
echo done >> "$SUM"
