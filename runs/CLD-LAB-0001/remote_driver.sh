#!/bin/bash
# Remote job driver for the sandboxed lab runner (run CLD-LAB-0001).
#
#   driver.sh ACTOR JOB_ID CORES TIMEOUT_SECONDS NETWORK(0|1)
#
# Runs $HOME/eda-agents/ACTOR/work/JOB_ID/in/job.sh inside bubblewrap. The sandbox sees only the
# actor workspace (mounted at /ws), read-only system directories and a private /tmp; the shared
# home directory is not mounted. Control files, logs and output hashes are written outside the
# workspace, under $HOME/eda-agents/.runner/jobs/ACTOR/JOB_ID, where the job cannot alter them.
set -u
actor=${1:-} id=${2:-} cores=${3:-} secs=${4:-} net=${5:-}
[[ $actor =~ ^[A-Za-z0-9-]{3,64}$ && $id =~ ^REQ-[0-9]{4}$ && $cores =~ ^[1-8]$ \
   && $secs =~ ^[0-9]{1,6}$ && $net =~ ^[01]$ ]] || { echo "invalid arguments" >&2; exit 2; }

root="$HOME/eda-agents"
ws="$root/$actor"
job="$ws/work/$id"
ctl="$root/.runner/jobs/$actor/$id"
umask 077
mkdir -p "$ctl" "$job/out" || exit 2
[ -f "$job/in/job.sh" ] || { echo "missing in/job.sh" >&2; exit 2; }

ncpu=$(nproc --all)
[ "$cores" -le "$ncpu" ] || cores=$ncpu
first=$(( RANDOM % (ncpu - cores + 1) ))
cpus="$first-$(( first + cores - 1 ))"

args=(--unshare-all --die-with-parent --new-session)
[ "$net" = 1 ] && args+=(--share-net)
args+=(--ro-bind /usr /usr --ro-bind /etc /etc)
for p in /bin /sbin /lib /lib32 /lib64 /libx32; do
  if [ -L "$p" ]; then args+=(--symlink "$(readlink "$p")" "$p")
  elif [ -d "$p" ]; then args+=(--ro-bind "$p" "$p"); fi
done
[ -d /opt ] && args+=(--ro-bind /opt /opt)
if [ "$net" = 1 ] && [ -d /run/systemd/resolve ]; then
  args+=(--ro-bind /run/systemd/resolve /run/systemd/resolve)
fi
args+=(--bind "$ws" /ws --tmpfs /tmp --proc /proc --dev /dev
       --setenv HOME /ws --setenv TMPDIR /tmp --setenv LANG C.UTF-8
       --setenv PATH /ws/tools/bin:/usr/local/bin:/usr/bin:/bin
       --chdir "/ws/work/$id")
exec 3<"$root/.runner/seccomp.bpf" || exit 2

echo "$cpus" > "$ctl/cpus"
cut -d' ' -f1-3 /proc/loadavg > "$ctl/load_at_start"
date -u +%s > "$ctl/started"
env -i PATH=/usr/bin:/bin nice -n 19 timeout --kill-after=60 "$secs" taskset -c "$cpus" \
  bwrap --seccomp 3 "${args[@]}" /bin/bash -c 'ulimit -v 33554432; exec /bin/bash in/job.sh' \
  > "$ctl/stdout.log" 2> "$ctl/stderr.log" < /dev/null
echo $? > "$ctl/exit_code"
date -u +%s > "$ctl/finished.tmp"

( cd "$job" && find out -type f -printf '%s\t%p\n' ) > "$ctl/out.sizes" 2>/dev/null
( cd "$job" && find out -type f -print0 | xargs -0 -r sha256sum ) > "$ctl/out.sha256" 2>/dev/null
du -sk "$ws" | cut -f1 > "$ctl/workspace_kb"
mv "$ctl/finished.tmp" "$ctl/finished"
