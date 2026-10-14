"""Synthetic fixtures for the EDA-0002 P3-P5 property checks (no real designs).

Writes, into the directory given as argv[1]:
  p05a.lib, p05b.lib  synthetic NLDM libraries (ramp-through-R model tables)
  p05.v               one driver buffer per net, 1-4 load buffers per net
  p05.spef            RC trees for SPEF-mode nets
  p05_inputs.tcl      set_input_transition, set_pi_model, set_elmore
  p05_nets.tcl        Tcl list of {net driver_inst {load_pins}}
  cases.json          per-net parameters, Python-computed Elmore and pi model

Mode "spef": RC trees reduced by the pinned OpenSTA reducer (reachable cases).
Mode "pi": pi model and Elmore injected with set_pi_model/set_elmore
(dense parameter sampling; any counterexample found here is labelled
injected until reproduced in spef mode).
Targeted families (appended after the random nets): "plateau" (spef and pi modes)
places the DMP driver waveform plateau a = Rpi/(Rd+Rpi) near a threshold; "singular"
(pi mode) sets the load Elmore to 1/p1 or 1/p2 of the driver waveform.
Injected pi models always include the load pin caps (OpenSTA ignores a pi model
whose total cap is below the pin caps: GraphDelayCalc::loadCap).
Usage: python3 p05_fixtures.py OUTDIR N_SPEF N_PI SEED [N_PLATEAU N_SINGULAR]
"""
import json
import math
import random
import sys

OUT = sys.argv[1]
N_SPEF = int(sys.argv[2])
N_PI = int(sys.argv[3])
SEED = int(sys.argv[4])
N_PLAT = int(sys.argv[5]) if len(sys.argv) > 5 else 0
N_SING = int(sys.argv[6]) if len(sys.argv) > 6 else 0
rng = random.Random(SEED)

SLEW_AXIS = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32]           # ns
CAP_AXIS = [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]    # pF

LIBS = {
    # name: thresholds (vth, vl, vh), slew_derate, load pin cap (pF), cells (strength list)
    "p05a": {"vth": 0.5, "vl": 0.2, "vh": 0.8, "derate": 1.0, "pincap": 0.002,
             "prefix": "BUFA", "strengths": [1, 2, 4, 8, 16], "weird": True},
    "p05b": {"vth": 0.5, "vl": 0.1, "vh": 0.9, "derate": 0.5, "pincap": 0.003,
             "prefix": "BUFB", "strengths": [1, 4, 16], "weird": False},
}
R_UNIT = 4.0  # kOhm, drive resistance of the X1 cell (rise); fall uses 0.8x


def ramp_rc_crossing(t_s, t_r, tau, level):
    """Time at which a 0->1 ramp (start t_s, duration t_r) through RC tau crosses level."""
    def v(t):
        def y0(x):
            if x <= 0.0:
                return 0.0
            if tau <= 0.0:
                return x
            return x - tau * (1.0 - math.exp(-x / tau))
        return (y0(t - t_s) - y0(t - t_s - t_r)) / t_r
    lo, hi = t_s, t_s + t_r + 60.0 * tau + 1e-6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if v(mid) < level:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def make_tables(r_drv, lib, weird):
    vth, vl, vh, k = lib["vth"], lib["vl"], lib["vh"], lib["derate"]
    delay, slew = [], []
    for s in SLEW_AXIS:
        s_full = s * k / (vh - vl)            # full input ramp duration
        t_in = s_full * vth                  # input threshold crossing
        t_s = t_in - 0.1 * s_full + 0.006    # internal source start
        t_r = 0.004 + 0.4 * s_full           # internal source ramp duration
        drow, srow = [], []
        for c in CAP_AXIS:
            tau = r_drv * c
            t50 = ramp_rc_crossing(t_s, t_r, tau, vth)
            tl = ramp_rc_crossing(t_s, t_r, tau, vl)
            th = ramp_rc_crossing(t_s, t_r, tau, vh)
            d = t50 - t_in
            sl = (th - tl) / k
            if weird:
                # Deliberately inconsistent with any ramp-through-R driver.
                sl = sl * (0.3 + 2.5 * c / CAP_AXIS[-1])
                d = d + 0.02 * math.sin(30.0 * s)
            drow.append(d)
            srow.append(sl)
        delay.append(drow)
        slew.append(srow)
    return delay, slew


def fmt_table(rows):
    return ", \\\n            ".join('"' + ", ".join("%.9g" % x for x in row) + '"' for row in rows)


def write_lib(name, lib):
    cells = {}
    lines = []
    w = lines.append
    w("library (%s) {" % name)
    w("  delay_model : table_lookup ;")
    w('  time_unit : "1ns" ;')
    w('  voltage_unit : "1V" ;')
    w('  current_unit : "1mA" ;')
    w('  pulling_resistance_unit : "1kohm" ;')
    w('  leakage_power_unit : "1nW" ;')
    w("  capacitive_load_unit (1,pf) ;")
    w("  nom_process : 1 ;")
    w("  nom_voltage : 1.0 ;")
    w("  nom_temperature : 25 ;")
    for rf in ("rise", "fall"):
        w("  input_threshold_pct_%s : %g ;" % (rf, 100 * lib["vth"]))
        w("  output_threshold_pct_%s : %g ;" % (rf, 100 * lib["vth"]))
        w("  slew_lower_threshold_pct_%s : %g ;" % (rf, 100 * lib["vl"]))
        w("  slew_upper_threshold_pct_%s : %g ;" % (rf, 100 * lib["vh"]))
    w("  slew_derate_from_library : %g ;" % lib["derate"])
    w("  default_max_transition : 100 ;")
    w("  lu_table_template (tmpl_7x8) {")
    w("    variable_1 : input_net_transition ;")
    w("    variable_2 : total_output_net_capacitance ;")
    w('    index_1 ("%s") ;' % ", ".join("%g" % x for x in SLEW_AXIS))
    w('    index_2 ("%s") ;' % ", ".join("%g" % x for x in CAP_AXIS))
    w("  }")
    variants = [("%s_X%d" % (lib["prefix"], x), R_UNIT / x, False) for x in lib["strengths"]]
    if lib["weird"]:
        variants.append(("%s_W4" % lib["prefix"], R_UNIT / 4, True))
    for cname, r, weird in variants:
        d_r, s_r = make_tables(r, lib, weird)
        d_f, s_f = make_tables(0.8 * r, lib, weird)
        cells[cname] = {"rise": {"delay": d_r, "slew": s_r}, "fall": {"delay": d_f, "slew": s_f},
                        "r_rise": r, "r_fall": 0.8 * r, "weird": weird}
        w("  cell (%s) {" % cname)
        w("    area : 1 ;")
        w("    pin (A) { direction : input ; capacitance : %g ; }" % lib["pincap"])
        w("    pin (Z) {")
        w("      direction : output ;")
        w('      function : "A" ;')
        w("      max_capacitance : 100 ;")
        w("      timing () {")
        w('        related_pin : "A" ;')
        w("        timing_sense : positive_unate ;")
        w("        timing_type : combinational ;")
        for group, tab in (("cell_rise", d_r), ("rise_transition", s_r),
                           ("cell_fall", d_f), ("fall_transition", s_f)):
            w("        %s (tmpl_7x8) {" % group)
            w("          values ( \\\n            %s ) ;" % fmt_table(tab))
            w("        }")
        w("      }")
        w("    }")
        w("  }")
    w("}")
    with open("%s/%s.lib" % (OUT, name), "w") as f:
        f.write("\n".join(lines) + "\n")
    return cells


def loguni(a, b):
    return 10.0 ** rng.uniform(a, b)


def f32(x):
    import struct
    return struct.unpack("f", struct.pack("f", x))[0]


def axis_index(axis, v):
    n = len(axis)
    if v <= axis[0]:
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
    i1, i2 = axis_index(SLEW_AXIS, x1), axis_index(CAP_AXIS, x2)
    dx1 = (x1 - SLEW_AXIS[i1]) / (SLEW_AXIS[i1 + 1] - SLEW_AXIS[i1])
    dx2 = (x2 - CAP_AXIS[i2]) / (CAP_AXIS[i2 + 1] - CAP_AXIS[i2])
    return ((1 - dx1) * (1 - dx2) * tab[i1][i2] + dx1 * (1 - dx2) * tab[i1 + 1][i2]
            + dx1 * dx2 * tab[i1 + 1][i2 + 1] + (1 - dx1) * dx2 * tab[i1][i2 + 1])


def model_rd(delay_tab, s_in, ctot, vth):
    """DmpCeff.cc gateModelRd: finite difference over 1 fF at C1+C2 (kOhm)."""
    cap1 = f32(ctot * 1e-12)
    cap2 = f32(cap1 + 1e-15)
    d1 = table2(delay_tab, s_in, cap1 * 1e12)
    d2 = table2(delay_tab, s_in, cap2 * 1e12)
    return -math.log(vth) * abs(d1 - d2) / ((cap2 - cap1) * 1e12)


def poles(rd, c2, rpi, c1):
    """DmpPi::init poles (1/ns) for rd [kOhm], caps [pF]."""
    a = rpi * rd * c1 * c2
    b = rd * (c1 + c2) + rpi * c1
    q = math.sqrt(max(b * b - 4 * a, 0.0))
    return (b + q) / (2 * a), (b - q) / (2 * a)


class Tree:
    """RC tree rooted at the driver pin node; reproduces ReduceToPi/ReduceToPiElmore."""

    def __init__(self):
        self.cap = {}      # node -> wire cap (pF)
        self.pincap = {}   # node -> pin cap added by OpenSTA (pF)
        self.kids = {}     # node -> list of (child, r)
        self.res = []      # (n1, n2, r)

    def add(self, parent, child, r):
        self.kids.setdefault(parent, []).append((child, r))
        self.kids.setdefault(child, [])
        self.res.append((parent, child, r))

    def moments(self, node):
        y1 = self.cap.get(node, 0.0) + self.pincap.get(node, 0.0)
        y2 = y3 = 0.0
        dwn = y1
        for child, r in self.kids.get(node, []):
            yd1, yd2, yd3, dc = self.moments(child)
            y1 += yd1
            y2 += yd2 - r * yd1 * yd1
            y3 += yd3 - 2 * r * yd1 * yd2 + r * r * yd1 * yd1 * yd1
            dwn += dc
        self.down = getattr(self, "down", {})
        self.down[node] = dwn
        return y1, y2, y3, dwn

    def pi_and_elmore(self, root):
        y1, y2, y3, _ = self.moments(root)
        if y2 == 0.0 and y3 == 0.0:
            c1, c2, rpi = y1, 0.0, 0.0
        else:
            c1 = y2 * y2 / y3
            c2 = y1 - y2 * y2 / y3
            rpi = -y3 * y3 / (y2 * y2 * y2)
        elm = {}

        def dfs(node, e):
            elm[node] = e
            for child, r in self.kids.get(node, []):
                dfs(child, e + r * self.down[child])
        dfs(root, 0.0)
        return {"c2": c2, "rpi": rpi, "c1": c1, "ctot": y1}, elm


def main():
    cells = {}
    for name, lib in LIBS.items():
        for cname, cdata in write_lib(name, lib).items():
            cdata["lib"] = name
            cells[cname] = cdata
    cases = []
    ports, body = [], []
    spef = ['*SPEF "IEEE 1481-1998"', '*DESIGN "p05"', '*DATE "fixture"', '*VENDOR "p05"',
            '*PROGRAM "p05_fixtures.py"', '*VERSION "1"', '*DESIGN_FLOW "PIN_CAP NONE"',
            "*DIVIDER /", "*DELIMITER :", "*BUS_DELIMITER [ ]",
            "*T_UNIT 1 NS", "*C_UNIT 1 PF", "*R_UNIT 1 KOHM", "*L_UNIT 1 HENRY", ""]
    tcl = ["set_cmd_units -time ns -capacitance pF -resistance kohm -digits 9"]
    nets_tcl = ["set p05_nets {"]
    total = N_SPEF + N_PI + 2 * N_PLAT + N_SING
    for i in range(total):
        if i < N_SPEF:
            grp = "rand_spef"
        elif i < N_SPEF + N_PI:
            grp = "rand_pi"
        elif i < N_SPEF + N_PI + N_PLAT:
            grp = "plat_spef"
        elif i < N_SPEF + N_PI + 2 * N_PLAT:
            grp = "plat_pi"
        else:
            grp = "sing_pi"
        mode = "spef" if grp.endswith("spef") else "pi"
        libname = "p05a" if rng.random() < 0.7 else "p05b"
        lib = LIBS[libname]
        names = [c for c in cells if cells[c]["lib"] == libname]
        if grp.startswith("plat"):
            names = [c for c in names if c.endswith(("_X1", "_X2"))]
        cname = rng.choice(names)
        r_drv = cells[cname]["r_rise"]
        load_cell = "%s_X1" % lib["prefix"]
        pincap = lib["pincap"]
        if grp.startswith("plat"):
            s_in = loguni(-2.5, -1.3)        # fast inputs so the source ramp is short
        else:
            s_in = loguni(-2.5, -0.3)        # 0.003 .. 0.5 ns, beyond both table ends
        net, drv, inp = "n%d" % i, "u%d" % i, "in%d" % i
        ports.append(inp)
        body.append("  wire %s;" % net)
        body.append("  %s %s ( .A(%s), .Z(%s) );" % (cname, drv, inp, net))
        tcl.append("set_input_transition %.9g [get_ports %s]" % (s_in, inp))
        case = {"net": net, "drv": drv, "cell": cname, "lib": libname, "mode": mode,
                "group": grp, "s_in": s_in}
        loads = []

        def plateau_target():
            thr = rng.choice(["vth", "vth", "vh", "vl"])
            side = 1.0 if rng.random() < 0.75 else -1.0
            return thr, lib[thr] + side * rng.uniform(0.002, 0.06)
        if mode == "spef":
            t = Tree()
            root = "%s:Z" % drv
            node_id = [0]

            def new_node():
                node_id[0] += 1
                return "%s:%d" % (net, node_id[0])

            def chain(start, r_tot, c_tot, m):
                cur = start
                for _ in range(m):
                    nxt = new_node()
                    t.add(cur, nxt, r_tot / m)
                    t.cap[nxt] = c_tot / m
                    cur = nxt
                return cur
            if grp == "plat_spef":
                fam = "plateau"
                t.cap[root] = loguni(-6, -4.5)
                c_far = loguni(-1.5, -0.5)
                c_near = loguni(-6, -4.5)
                thr, a = plateau_target()
                ctot_est = c_far + t.cap[root] + c_near + 2 * pincap
                rd = model_rd(cells[cname]["rise"]["delay"], s_in, ctot_est, lib["vth"])
                r_w = rd * a / (1.0 - a)
                tau_near = loguni(-3.5, -0.5)
                r_near = tau_near / (c_near + pincap)
                far = chain(root, r_w, c_far, 1)
                near = new_node()
                t.add(root, near, r_near)
                t.cap[near] = c_near
                pins = [("%s_0" % net, near), ("%s_1" % net, far)]
                params = {"family": fam, "target": thr, "a_target": a, "rd_py": rd, "r_w": r_w,
                          "c_far": c_far, "r_near": r_near, "c_near": c_near, "tau_near": tau_near}
            else:
                fam = rng.choice(["two_branch", "two_branch", "line", "star"])
                t.cap[root] = 0.0 if rng.random() < 0.3 else loguni(-4.5, -2)
                params = {"family": fam}
                if fam == "two_branch":
                    r_w = r_drv * loguni(-2, 1.5)
                    c_w = loguni(-3.3, -0.7)
                    m = rng.choice([1, 3, 10])
                    r_near = r_drv * loguni(-6, 0)
                    c_near = 0.0 if rng.random() < 0.3 else loguni(-4.5, -2)
                    far = chain(root, r_w, c_w, m)
                    near = new_node()
                    t.add(root, near, r_near)
                    t.cap[near] = c_near
                    pins = [("%s_0" % net, near), ("%s_1" % net, far)]
                    params.update({"r_w": r_w, "c_w": c_w, "m": m, "r_near": r_near, "c_near": c_near})
                elif fam == "line":
                    r_w = r_drv * loguni(-2, 1.5)
                    c_w = loguni(-3.3, -0.7)
                    m = rng.choice([2, 4, 10])
                    mid = chain(root, r_w / 2, c_w / 2, m // 2)
                    end = chain(mid, r_w / 2, c_w / 2, m - m // 2)
                    pins = [("%s_0" % net, mid), ("%s_1" % net, end)]
                    params.update({"r_w": r_w, "c_w": c_w, "m": m})
                else:
                    kst = rng.choice([2, 3, 4])
                    pins = []
                    stubs = []
                    for j in range(kst):
                        r_k = r_drv * loguni(-7, -1)
                        c_k = loguni(-5, -2.5)
                        nd = new_node()
                        t.add(root, nd, r_k)
                        t.cap[nd] = c_k
                        pins.append(("%s_%d" % (net, j), nd))
                        stubs.append([r_k, c_k])
                    params.update({"stubs": stubs})
            # Load pins are separate SPEF nodes joined to their tree node by a tiny resistor.
            pin_nodes = []
            for inst, nd in pins:
                pn = "%s:A" % inst
                t.add(nd, pn, 1e-6)
                t.pincap[pn] = pincap
                pin_nodes.append(pn)
                loads.append(inst + "/A")
                body.append("  %s %s ( .A(%s) );" % (load_cell, inst, net))
            pi, elm = t.pi_and_elmore(root)
            case.update(params)
            case["pi_py"] = pi
            case["elmore_py"] = {pn.replace(":", "/"): elm[pn] for pn in pin_nodes}
            wire_c = sum(t.cap.values())
            spef.append("*D_NET %s %.9g" % (net, wire_c))
            spef.append("*CONN")
            spef.append("*I %s:Z O" % drv)
            for pn in pin_nodes:
                spef.append("*I %s I" % pn)
            spef.append("*CAP")
            ci = 0
            for nd, c in t.cap.items():
                if c > 0.0:
                    ci += 1
                    spef.append("%d %s %.9g" % (ci, nd, c))
            spef.append("*RES")
            for ri, (a_, b_, r) in enumerate(t.res, 1):
                spef.append("%d %s %s %.9g" % (ri, a_, b_, r))
            spef.append("*END")
            spef.append("")
        else:
            elms = []
            if grp == "plat_pi":
                n_ld = 4
                c1 = loguni(-1.5, -0.5) + n_ld * pincap
                c2 = c1 * (loguni(-2.9, -1.4) if rng.random() < 0.5 else loguni(-5, -3.1))
                thr, a = plateau_target()
                rd = model_rd(cells[cname]["rise"]["delay"], s_in, c1 + c2, lib["vth"])
                rpi = rd * a / (1.0 - a)
                case.update({"family": "plateau", "target": thr, "a_target": a, "rd_py": rd})
                taus = [(loguni(-4, -0.5), "plateau") for _ in range(n_ld)]
            elif grp == "sing_pi":
                n_ld = rng.choice([3, 4])
                c1 = loguni(-3, -0.7) + n_ld * pincap
                c2 = c1 * loguni(-2.5, 0)
                rpi = r_drv * loguni(-1, 1)
                rd = model_rd(cells[cname]["rise"]["delay"], s_in, c1 + c2, lib["vth"])
                p1, p2 = poles(rd, c2, rpi, c1)
                case.update({"family": "singular", "rd_py": rd, "p1": p1, "p2": p2})
                taus = []
                for j in range(n_ld):
                    which = rng.choice(["sing_p2", "sing_p2", "sing_p1"])
                    eps = rng.choice([0.0, 1e-9, -1e-9, 1e-6, -1e-6, 1e-3, -1e-3])
                    taus.append(((1.0 / (p2 if which == "sing_p2" else p1)) * (1.0 + eps), which))
            else:
                n_ld = rng.choice([1, 2, 3, 4])
                c2 = loguni(-4.5, -0.7) if rng.random() > 0.08 else loguni(-9, -7)
                c1 = (loguni(-4.5, -0.7) if rng.random() > 0.08 else loguni(-9, -7)) + n_ld * pincap
                rpi = r_drv * loguni(-3.5, 1.5)
                case["family"] = "pi"
                taus = []
                for j in range(n_ld):
                    kind = rng.choice(["tiny", "near", "far", "free"])
                    if kind == "tiny":
                        e = loguni(-8, -4)
                    elif kind == "near":
                        e = rpi * c1 * loguni(-4, -1)
                    elif kind == "far":
                        e = rpi * c1 * rng.uniform(0.3, 1.3)
                    else:
                        e = loguni(-6, 0)
                    taus.append((e, kind))
            for j, (e, kind) in enumerate(taus):
                inst = "%s_%d" % (net, j)
                loads.append(inst + "/A")
                body.append("  %s %s ( .A(%s) );" % (load_cell, inst, net))
                elms.append({"pin": inst + "/A", "elmore": e, "kind": kind})
            tcl.append("sta::set_pi_model %s/Z %.9g %.9g %.9g" % (drv, c2, rpi, c1))
            for e in elms:
                tcl.append("sta::set_elmore %s/Z %s %.9g" % (drv, e["pin"], e["elmore"]))
            case.update({"pi_inj": {"c2": c2, "rpi": rpi, "c1": c1, "ctot": c1 + c2},
                         "elmore_inj": {e["pin"]: e["elmore"] for e in elms},
                         "elmore_kind": {e["pin"]: e["kind"] for e in elms}})
        case["loads"] = loads
        cases.append(case)
        nets_tcl.append("  {%s %s {%s}}" % (net, drv, " ".join(loads)))
    nets_tcl.append("}")
    verilog = ["module p05 (%s);" % ", ".join(ports)]
    verilog += ["  input %s;" % p for p in ports]
    verilog += body
    verilog.append("endmodule")
    with open("%s/p05.v" % OUT, "w") as f:
        f.write("\n".join(verilog) + "\n")
    with open("%s/p05.spef" % OUT, "w") as f:
        f.write("\n".join(spef) + "\n")
    with open("%s/p05_inputs.tcl" % OUT, "w") as f:
        f.write("\n".join(tcl) + "\n")
    with open("%s/p05_nets.tcl" % OUT, "w") as f:
        f.write("\n".join(nets_tcl) + "\n")
    meta = {"seed": SEED, "n_spef": N_SPEF, "n_pi": N_PI, "n_plateau": N_PLAT, "n_singular": N_SING, "slew_axis": SLEW_AXIS,
            "cap_axis": CAP_AXIS, "libs": LIBS, "cells": cells}
    with open("%s/cases.json" % OUT, "w") as f:
        json.dump({"meta": meta, "cases": cases}, f)


if __name__ == "__main__":
    main()
