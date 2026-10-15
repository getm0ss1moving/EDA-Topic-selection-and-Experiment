"""Evaluate P3-P5 (and side checks) on pinned-OpenSTA DMP results.

Usage: python3 p05_check.py FIXTURE_DIR RAW_TSV OUT_DIR
Inputs: cases.json from p05_fixtures.py, raw.tsv from p05_extract.tcl.
Outputs: summary.json, counterexamples.csv, results_G.csv, results_W.csv.

Property statements tested (from proposal.md, made precise):
  P3  driver slew s_d lies in [min, max] of the slew table over C' in [0, C1+C2]
      at the arc's actual input slew (the exact-slew instance of the box rule).
  P4  wire delay w <= Elmore delay tau of the reduced model (and w >= 0).
  P5  load slew s_l <= s_d + tau*ln((1-vl)/(1-vh))/k (OpenSTA's own single-pole
      slew increment, DelayCalcBase::dspfWireDelaySlew), and s_l >= s_d.
Code-derived candidate bounds (finite-test evidence only; see the record):
  BR3 s_d <= (dt + 2*C*(Rd+Rpi))/k            (root-finder bracket, Pi/C2=0 paths)
  BR5 s_l <= max(s_d, (dt + 2*C*(Rd+Rpi) + 2*tau)/k)
  ADT dt <= k*T(s, Ceff)/(vh-vl)               (ramp fit; assumption of BR3/BR5)
  LAG w <= tau*ln(vh/(vh-vth)) + k*s_d + 0.02*gate_delay
"""
import csv
import json
import math
import re
import struct
import sys

FIX, RAW, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
REL = 1e-5      # relative tolerance for float storage and printing
ABS = 1e-18     # seconds

data = json.load(open("%s/cases.json" % FIX))
meta, cases = data["meta"], {c["net"]: c for c in data["cases"]}
SA, CA = meta["slew_axis"], meta["cap_axis"]
NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


def f32(x):
    return struct.unpack("f", struct.pack("f", x))[0]


def axis_index(axis, v):
    n = len(axis)
    if n <= 1 or v <= axis[0]:
        return 0
    if v >= axis[-1]:
        return n - 2
    lo, hi = -1, n
    while hi - lo > 1:
        mid = (hi + lo) >> 1
        if v >= axis[mid]:
            lo = mid
        else:
            hi = mid
    return lo


def table2(tab, x1, x2):
    x1, x2 = f32(x1), f32(x2)
    i1, i2 = axis_index(SA, x1), axis_index(CA, x2)
    a1l, a1u = f32(SA[i1]), f32(SA[i1 + 1])
    a2l, a2u = f32(CA[i2]), f32(CA[i2 + 1])
    dx1 = (x1 - a1l) / (a1u - a1l)
    dx2 = (x2 - a2l) / (a2u - a2l)
    y00, y10 = f32(tab[i1][i2]), f32(tab[i1 + 1][i2])
    y01, y11 = f32(tab[i1][i2 + 1]), f32(tab[i1 + 1][i2 + 1])
    v = ((1 - dx1) * (1 - dx2) * y00 + dx1 * (1 - dx2) * y10
         + dx1 * dx2 * y11 + (1 - dx1) * dx2 * y01)
    return f32(v)


def slew_at(tab, s, c):
    return max(0.0, table2(tab, s, c))


def box(tab, s, c_hi, clip):
    pts = [0.0, c_hi] + [c for c in CA if 0.0 < c < c_hi]
    vals = [slew_at(tab, s, c) if clip else table2(tab, s, c) for c in pts]
    return min(vals), max(vals)


def last(pattern, text):
    m = re.findall(pattern, text)
    return m[-1] if m else None


def parse_g(rpt, dbg):
    r = {}
    m = re.search(r"Pi model C2=(\S+) Rpi=(\S+) C1=(\S+), Ceff=(\S+)", rpt)
    if m:
        r["c2"], r["rpi"], r["c1"], r["ceff"] = [float(NUM.search(x).group()) for x in m.groups()]
    m = last(r"DMP in_slew = (\S+) c2 = (\S+) rpi = (\S+) c1 = (\S+) Rd = (\S+) \(([^)]*) alg\)", dbg)
    if m:
        r["rd"] = float(NUM.search(m[4]).group())
        r["alg"] = m[5]
    m = last(r"t0 = (\S+) dt = (\S+) ceff = (\S+)", dbg)
    if m:
        r["t0"], r["dt"], r["ceff_dbg"] = [float(NUM.search(x).group()) for x in m]
    r["fails"] = ";".join(sorted(set(re.findall(r"DMP failed - ([^|]*?) c2=", dbg))))
    return r


G, W = {}, []
with open(RAW) as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if p[0] == "G":
            net, rf = p[1], p[2]
            rec = {"net": net, "rf": rf, "in_slew": float(p[3]), "gd": float(p[4]),
                   "sd": float(p[5])}
            rec.update(parse_g(p[6] if len(p) > 6 else "", p[7] if len(p) > 7 else ""))
            G[(net, rf)] = rec
        elif p[0] == "W":
            W.append({"net": p[1], "rf": p[2], "pin": p[3], "w": float(p[4]), "sl": float(p[5])})

rows_g, rows_w = [], []
for (net, rf), g in G.items():
    c = cases[net]
    lib = meta["libs"][c["lib"]]
    cell = meta["cells"][c["cell"]]
    k, vl, vh, vth = lib["derate"], lib["vl"], lib["vh"], lib["vth"]
    tab_s, tab_d = cell[rf]["slew"], cell[rf]["delay"]
    s_ns = g["in_slew"] * 1e9
    if "c1" not in g:
        g["status"] = "no_pi_report"
        rows_g.append(g)
        continue
    ctot = g["c1"] + g["c2"]
    lo, hi = box(tab_s, s_ns, ctot, True)
    lo_x, hi_x = box(tab_s, s_ns, 1.01 * ctot, True)
    sd_ns = g["sd"] * 1e9
    g.update({"mode": c["mode"], "lib": c["lib"], "cell": c["cell"], "weird": cell["weird"],
              "family": c.get("family", "pi"), "group": c.get("group"), "target": c.get("target"),
              "a_target": c.get("a_target"), "ctot": ctot, "T_lo": lo, "T_hi": hi,
              "s_ns": s_ns, "sd_ns": sd_ns})
    g["P3"] = lo * (1 - REL) - 1e-9 <= sd_ns <= hi * (1 + REL) + 1e-9
    g["P3_ext"] = lo_x * (1 - REL) - 1e-9 <= sd_ns <= hi_x * (1 + REL) + 1e-9
    g["P3_ratio_hi"] = sd_ns / hi if hi > 0 else float("inf")
    g["P3_ratio_lo"] = sd_ns / lo if lo > 0 else float("inf")
    g["sd_nonneg"] = sd_ns >= 0.0
    if c["mode"] == "spef":
        py = c["pi_py"]
        # Relative to C1+C2 (c2 near 0 suffers cancellation in both implementations).
        g["pi_relerr"] = max(abs(g["c1"] - py["c1"]) / py["ctot"], abs(g["c2"] - py["c2"]) / py["ctot"])
        g["rpi_relerr"] = abs(g["rpi"] - py["rpi"]) / max(py["rpi"], 1e-6)
    alg = g.get("alg")
    driver_valid = alg in ("Pi", "c2=0") and not re.search(
        r"Newton|find Vo|eqn eval|LU decomposition", g["fails"])
    g["driver_valid_guess"] = driver_valid
    if alg == "cap":
        g["path"] = "cap"
    elif alg in ("Pi", "c2=0"):
        g["path"] = "waveform_driver" if driver_valid else "driver_fallback"
    else:
        g["path"] = str(alg)
    if "rd" in g and g.get("rpi"):
        g["a_actual"] = g["rpi"] / (g["rd"] + g["rpi"])
    if alg in ("Pi", "c2=0") and "dt" in g and "rd" in g:
        cb = ctot if alg == "Pi" else g["c1"]
        g["BR3_bound"] = (g["dt"] + 2 * cb * (g["rd"] + g["rpi"])) / k
        g["BR3"] = (not driver_valid) or sd_ns <= g["BR3_bound"] * (1 + REL) + 1e-9
        t_ceff = slew_at(tab_s, s_ns, g["ceff"])
        g["ADT_ratio"] = g["dt"] / (k * t_ceff / (vh - vl)) if t_ceff > 0 else float("inf")
    if alg == "Pi":
        d_ceff = table2(tab_d, s_ns, g["ceff"])
        g["P2_table_match"] = abs(g["gd"] * 1e9 - d_ceff) <= REL * abs(d_ceff) + 1e-9
        g["P2_ceff_in"] = -1e-12 <= g["ceff"] <= ctot * (1 + REL) + 1e-12
    elif alg == "c2=0":
        dlo, dhi = box(tab_d, s_ns, ctot, False)
        g["P2_table_match"] = abs(g["gd"] * 1e9 - table2(tab_d, s_ns, g["c1"])) <= REL * dhi + 1e-9
        g["P2_delay_in_box"] = dlo * (1 - REL) - 1e-9 <= g["gd"] * 1e9 <= dhi * (1 + REL) + 1e-9
    rows_g.append(g)

for w in W:
    c = cases[w["net"]]
    g = G.get((w["net"], w["rf"]))
    if not g or "ctot" not in g:
        continue
    lib = meta["libs"][c["lib"]]
    k, vl, vh, vth = lib["derate"], lib["vl"], lib["vh"], lib["vth"]
    tau_ns = (c["elmore_py"] if c["mode"] == "spef" else c["elmore_inj"])[w["pin"]]
    w_ns, sl_ns, sd_ns = w["w"] * 1e9, w["sl"] * 1e9, g["sd_ns"]
    w.update({"mode": c["mode"], "lib": c["lib"], "cell": c["cell"], "family": g["family"],
              "group": c.get("group"), "target": c.get("target"), "path": g.get("path"),
              "a_actual": g.get("a_actual"),
              "alg": g.get("alg"), "fails": g["fails"], "tau_ns": tau_ns, "w_ns": w_ns,
              "sl_ns": sl_ns, "sd_ns": sd_ns, "gd_ns": g["gd"] * 1e9,
              "kind": c.get("elmore_kind", {}).get(w["pin"], c.get("family")),
              "regime": "elmore_small" if tau_ns < sd_ns * 1e-3 else "waveform"})
    w["P4"] = w_ns <= tau_ns * (1 + REL) + 1e-9
    w["P4_ratio"] = w_ns / tau_ns if tau_ns > 0 else float("inf")
    w["P4_excess_ns"] = w_ns - tau_ns
    w["P4_lower"] = w_ns >= -1e-9
    inc = tau_ns * math.log((1 - vl) / (1 - vh)) / k
    w["P5_bound"] = sd_ns + inc
    w["P5"] = sl_ns <= w["P5_bound"] * (1 + REL) + 1e-9
    w["P5_ratio"] = sl_ns / w["P5_bound"] if w["P5_bound"] > 0 else float("inf")
    w["P5_lower"] = sl_ns >= sd_ns * (1 - REL) - 1e-9
    w["LAG"] = w_ns <= tau_ns * math.log(vh / (vh - vth)) + k * sd_ns + 0.02 * w["gd_ns"] + 1e-9
    if "BR3_bound" in g:
        br5 = max(sd_ns, (g["BR3_bound"] * k + 2 * tau_ns) / k)
        w["BR5"] = (not g["driver_valid_guess"]) or sl_ns <= br5 * (1 + REL) + 1e-9
        w["BR4"] = (not g["driver_valid_guess"]) or w_ns <= (g["BR3_bound"] * k + 2 * tau_ns) * (1 + REL) + 1e-9
    rows_w.append(w)


def tally(rows, prop, keys=("mode", "alg")):
    out = {}
    for r in rows:
        if prop not in r:
            continue
        key = "/".join(str(r.get(k)) for k in keys)
        t = out.setdefault(key, {"n": 0, "fail": 0})
        t["n"] += 1
        t["fail"] += 0 if r[prop] else 1
    tot = {"n": sum(v["n"] for v in out.values()), "fail": sum(v["fail"] for v in out.values())}
    return {"total": tot, "by": out}


summary = {
    "n_driver_arcs": len(rows_g), "n_wire_arcs": len(rows_w),
    "algs": {a: sum(1 for r in rows_g if r.get("alg") == a) for a in sorted({str(r.get("alg")) for r in rows_g})},
    "fail_reasons": {},
    "P3": tally(rows_g, "P3", ("mode", "alg", "lib")), "P3_ext": tally(rows_g, "P3_ext"),
    "P3_by_path": tally(rows_g, "P3", ("path",)), "P3_by_group": tally(rows_g, "P3", ("group",)),
    "P4_by_group": tally(rows_w, "P4", ("group", "path")), "P5_by_group": tally(rows_w, "P5", ("group", "path")),
    "P3_ext_by_path": tally(rows_g, "P3_ext", ("path",)),
    "sd_nonneg": tally(rows_g, "sd_nonneg"),
    "BR3": tally(rows_g, "BR3"), "P2_table_match": tally(rows_g, "P2_table_match"),
    "P2_ceff_in": tally(rows_g, "P2_ceff_in"), "P2_delay_in_box": tally(rows_g, "P2_delay_in_box"),
    "P4": tally(rows_w, "P4", ("mode", "alg", "regime")), "P4_lower": tally(rows_w, "P4_lower"),
    "P5": tally(rows_w, "P5", ("mode", "alg", "regime")), "P5_lower": tally(rows_w, "P5_lower"),
    "LAG": tally(rows_w, "LAG", ("mode", "alg")), "BR4": tally(rows_w, "BR4"), "BR5": tally(rows_w, "BR5"),
}
for r in rows_g:
    for reason in filter(None, r.get("fails", "").split(";")):
        summary["fail_reasons"][reason] = summary["fail_reasons"].get(reason, 0) + 1
spef_err = [r["pi_relerr"] for r in rows_g if "pi_relerr" in r]
summary["spef_pi_replication_max_relerr_vs_ctot"] = max(spef_err) if spef_err else None
rerr = [r["rpi_relerr"] for r in rows_g if "rpi_relerr" in r and r.get("alg") != "cap"]
summary["spef_rpi_replication_max_relerr_noncap"] = max(rerr) if rerr else None
adt = [r["ADT_ratio"] for r in rows_g if "ADT_ratio" in r and math.isfinite(r["ADT_ratio"])]
summary["ADT_ratio_max"] = max(adt) if adt else None
summary["ADT_ratio_gt_1.01"] = sum(1 for a in adt if a > 1.01)


def extreme(rows, key, prop, n=3, reverse=True):
    sel = [r for r in rows if prop in r and not r[prop] and key in r and math.isfinite(r[key])]
    sel.sort(key=lambda r: r[key], reverse=reverse)
    return sel[:n]


worst = {
    "P3_hi": extreme(rows_g, "P3_ratio_hi", "P3"), "P3_lo": extreme(rows_g, "P3_ratio_lo", "P3", reverse=False),
    "P4": extreme(rows_w, "P4_ratio", "P4"), "P4_abs": extreme(rows_w, "P4_excess_ns", "P4"),
    "P5": extreme(rows_w, "P5_ratio", "P5"),
}
keep = ("net", "rf", "mode", "group", "family", "target", "a_target", "a_actual", "path", "lib", "cell", "alg", "fails", "s_ns", "ctot", "c2", "rpi", "c1",
        "ceff", "rd", "dt", "t0", "sd_ns", "T_lo", "T_hi", "P3_ratio_hi", "P3_ratio_lo", "pin", "tau_ns",
        "w_ns", "sl_ns", "gd_ns", "P4_ratio", "P4_excess_ns", "P5_bound", "P5_ratio", "regime", "kind")
summary["worst"] = {k: [{x: r.get(x) for x in keep if x in r} for r in v] for k, v in worst.items()}
for k in ("P3_ratio_hi", "P4_ratio", "P5_ratio"):
    src = rows_g if k.startswith("P3") else rows_w
    vals = [r[k] for r in src if k in r and math.isfinite(r[k])]
    summary["max_" + k] = max(vals) if vals else None
json.dump(summary, open("%s/summary.json" % OUT, "w"), indent=1, default=str)

with open("%s/counterexamples.csv" % OUT, "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(("property",) + keep)
    for prop, ratio, src, rev in (("P3", "P3_ratio_hi", rows_g, True), ("P3", "P3_ratio_lo", rows_g, False),
                                  ("P4", "P4_ratio", rows_w, True), ("P4", "P4_excess_ns", rows_w, True),
                                  ("P5", "P5_ratio", rows_w, True)):
        for r in extreme(src, ratio, prop, n=25, reverse=rev):
            wr.writerow((prop + ":" + ratio,) + tuple(r.get(x, "") for x in keep))
for name, rows in (("results_G.csv", rows_g), ("results_W.csv", rows_w)):
    cols = sorted({k for r in rows for k in r})
    with open("%s/%s" % (OUT, name), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        for r in rows:
            wr.writerow(r)
print(json.dumps({k: summary[k] for k in ("n_driver_arcs", "n_wire_arcs", "algs")}))
for p in ("P3", "P3_ext", "BR3", "P4", "P4_lower", "P5", "P5_lower", "LAG", "BR4", "BR5", "P2_table_match"):
    print(p, summary[p]["total"])
