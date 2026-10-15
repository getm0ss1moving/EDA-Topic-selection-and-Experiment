#!/bin/bash
# REQ-0003 (data, lab231, network): download the build toolchain sources from
# official GitHub repositories/releases into /ws/data/src, pinned by commit or
# release asset, logging URL, resolved revision and SHA-256 for every download.
set -u
OUT=$(pwd)/out
mkdir -p "$OUT"
SRC=/ws/data/src
mkdir -p "$SRC"
NETLOG=$OUT/network-log.tsv
printf 'url\tresolved_revision\tsha256\tnote\n' > "$NETLOG"
LIC=$OUT/licenses.txt
: > "$LIC"

fetch() {  # url file revision note
  if curl -fsSL --retry 2 --max-time 900 -o "$SRC/$2" "$1"; then
    printf '%s\t%s\t%s\t%s\n' "$1" "$3" "$(sha256sum "$SRC/$2" | cut -d' ' -f1)" "$4" >> "$NETLOG"
  else
    printf '%s\t%s\t%s\t%s\n' "$1" "$3" "DOWNLOAD_FAILED" "$4" >> "$NETLOG"
  fi
}
resolve() {  # repo-url tag -> peeled commit sha
  local s
  s=$(git ls-remote "$1" "refs/tags/$2^{}" | cut -f1)
  [ -n "$s" ] || s=$(git ls-remote "$1" "refs/tags/$2" | cut -f1)
  printf '%s\t%s\t%s\t%s\n' "$1 refs/tags/$2" "$s" "-" "git ls-remote tag resolution" >> "$NETLOG"
  echo "$s"
}
unpack() {  # file dir
  rm -rf "$SRC/$2" && mkdir -p "$SRC/$2" && tar -xzf "$SRC/$1" -C "$SRC/$2" --strip-components=1
}
license() {  # label path...
  local label=$1; shift
  for f in "$@"; do
    if [ -f "$f" ]; then
      echo "== $label: ${f#$SRC/} sha256=$(sha256sum "$f" | cut -d' ' -f1)" >> "$LIC"
      head -12 "$f" >> "$LIC"
    else
      echo "== $label: MISSING $f" >> "$LIC"
    fi
  done
}

# 1. CMake 3.27.9 official Kitware release binary and its published SHA-256 list.
CM=https://github.com/Kitware/CMake/releases/download/v3.27.9
fetch $CM/cmake-3.27.9-linux-x86_64.tar.gz cmake-3.27.9-linux-x86_64.tar.gz v3.27.9 "Kitware release asset"
fetch $CM/cmake-3.27.9-SHA-256.txt cmake-3.27.9-SHA-256.txt v3.27.9 "Kitware published checksums"
( cd "$SRC" && grep ' cmake-3.27.9-linux-x86_64.tar.gz$' cmake-3.27.9-SHA-256.txt | sha256sum -c - ) > "$OUT/cmake-sha-check.txt" 2>&1
unpack cmake-3.27.9-linux-x86_64.tar.gz cmake-3.27.9
license CMake "$SRC/cmake-3.27.9/doc/cmake-3.27/Copyright.txt"

# 2. flex 2.6.4 release asset uploaded by the maintainer.
fetch https://github.com/westes/flex/releases/download/v2.6.4/flex-2.6.4.tar.gz flex-2.6.4.tar.gz v2.6.4 "westes/flex release asset"
unpack flex-2.6.4.tar.gz flex-2.6.4
license flex "$SRC/flex-2.6.4/COPYING"

# 3. Berkeley yacc, maintainer snapshot t20240109 (public domain).
R=https://github.com/ThomasDickey/byacc-snapshots.git; S=$(resolve $R t20240109)
fetch https://codeload.github.com/ThomasDickey/byacc-snapshots/tar.gz/$S byacc-$S.tar.gz "$S" "tag t20240109"
unpack byacc-$S.tar.gz byacc
license byacc "$SRC/byacc/LICENSE" "$SRC/byacc/README"

# 4. Tcl 8.6.13 (tcltk/tcl, mirror of core.tcl-lang.org).
R=https://github.com/tcltk/tcl.git; S=$(resolve $R core-8-6-13)
fetch https://codeload.github.com/tcltk/tcl/tar.gz/$S tcl-$S.tar.gz "$S" "tag core-8-6-13"
unpack tcl-$S.tar.gz tcl8.6.13
license Tcl "$SRC/tcl8.6.13/license.terms"

# 5. SWIG 4.1.1.
R=https://github.com/swig/swig.git; S=$(resolve $R v4.1.1)
fetch https://codeload.github.com/swig/swig/tar.gz/$S swig-$S.tar.gz "$S" "tag v4.1.1"
unpack swig-$S.tar.gz swig-4.1.1
license SWIG "$SRC/swig-4.1.1/LICENSE" "$SRC/swig-4.1.1/LICENSE-GPL" "$SRC/swig-4.1.1/LICENSE-UNIVERSITIES"

# 6. Eigen 3.3.7 from the Eigen team's GitHub mirror (deprecated after 3.3.7, see repo description).
R=https://github.com/eigenteam/eigen-git-mirror.git; S=$(resolve $R 3.3.7)
fetch https://codeload.github.com/eigenteam/eigen-git-mirror/tar.gz/$S eigen-$S.tar.gz "$S" "tag 3.3.7"
unpack eigen-$S.tar.gz eigen-3.3.7
license Eigen "$SRC/eigen-3.3.7/COPYING.README" "$SRC/eigen-3.3.7/COPYING.MPL2"

ls -la "$SRC" > "$OUT/src-listing.txt" 2>&1
du -sh "$SRC"/* >> "$OUT/src-listing.txt" 2>&1
echo done >> "$OUT/src-listing.txt"
