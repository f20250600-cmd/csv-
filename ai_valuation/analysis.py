"""
Runs every analysis and writes CSVs + outputs/model_results.md.

    python3 analysis.py
"""
from __future__ import annotations

import math
import os

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from inputs import LABEL, META, MSFT, SCENARIOS, build

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)
MD: list[str] = []
COS = ["META", "MSFT"]
NAME = {"META": "Meta Platforms", "MSFT": "Microsoft"}
PRICE = {"META": META["price"], "MSFT": MSFT["price"]}


# --------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------
def md_table(df: pd.DataFrame, floatfmt="{:,.1f}") -> str:
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join([""] + cols) + " |", "|" + "---|" * (len(cols) + 1)]
    for idx, row in df.iterrows():
        cells = []
        for v in row.values:
            if isinstance(v, (float, np.floating)):
                cells.append("n/a" if (v is None or (isinstance(v, float) and math.isnan(v))) else floatfmt.format(v))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join([str(idx)] + cells) + " |")
    return "\n".join(lines)


def pct(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/m"
    return "<-25% (n/m)" if x < -0.25 else f"{x:.1%}"


def h(txt, lvl=2):
    MD.append("\n" + "#" * lvl + " " + txt + "\n")


def para(txt):
    MD.append(txt + "\n")


def ps(co, scn="base", knobs=None):
    return build(co, scn, knobs).run()["per_share"]


def ai_idx(r, y):
    return r["ai"]["years"].index(y)


def summary_row(co, scn, knobs=None):
    c = build(co, scn, knobs)
    r = c.run()
    A = r["ai"]["total"]
    v = r["ai"]["valuation"]
    fy = r["years"]
    i30 = ai_idx(r, 2030)
    i36 = ai_idx(r, 2036)
    j30 = fy.index(2030)
    row = {
        "Value/share": r["per_share"],
        "vs price": r["upside"],
    }
    for k, val in r["core_values"].items():
        row[k + " ($bn)"] = val
    row["AI layer NPV ($bn)"] = r["ai_value"]
    for k, val in c.nonop.items():
        row[k + " ($bn)"] = val
    row["Net debt ($bn)"] = -c.net_debt
    row["AI program IRR (incl. sunk)"] = v["irr_program"]
    row["AI hurdle"] = c.ai.hurdle
    row["AI rev 2030"] = A["revenue"][i30]
    row["AI rev 2036"] = A["revenue"][i36]
    row["AI econ ROIC 2030"] = A["roic_econ"][i30]
    row["AI econ ROIC 2036"] = A["roic_econ"][i36]
    row["AI book ROIC 2030"] = A["roic_book"][i30]
    row["Capacity util 2030"] = A["util_capacity"][i30]
    row["Group capex/rev 2030"] = r["capex"][j30] / r["revenue"][j30]
    row["FCF 2027"] = r["fcf"][0]
    row["FCF 2030"] = r["fcf"][j30]
    row["EPS 2027"] = r["eps"][0]
    row["EPS 2028"] = r["eps"][1]
    row["EPS 2030"] = r["eps"][j30]
    row["Group ROIC 2030"] = r["roic"][j30]
    row["TV rule (AI)"] = v["tv_rule"]
    return row


def fmt_summary(df):
    out = df.copy().astype(object)
    for c in out.columns:
        for i in out.index:
            v = df.loc[i, c]
            if isinstance(v, str):
                continue
            if c in ("vs price", "AI program IRR (incl. sunk)", "AI hurdle") or "ROIC" in c or "util" in c or "capex/rev" in c:
                out.loc[i, c] = pct(v)
            elif c.startswith("EPS") or c == "Value/share":
                out.loc[i, c] = f"{v:,.2f}"
            else:
                out.loc[i, c] = f"{v:,.0f}"
    return out


def annual_tables(co, scn, knobs=None, tag=None):
    c = build(co, scn, knobs)
    r = c.run()
    A = r["ai"]["total"]
    Y = r["ai"]["years"]
    ai = pd.DataFrame({
        "AI revenue": A["revenue"], "Variable cost": -A["var_cost"], "Power & site ops": -A["power"],
        "AI talent / 3P compute / R&D opex": -A["fixed_opex"], "AI EBITDA": A["ebitda"],
        "Accounting D&A (book)": -A["book_dep"], "Write-offs (early retirement)": -A["writeoff"],
        "Residual value proceeds": A["proceeds"], "AI EBIT (reported)": A["ebit_book"],
        "Economic depreciation": -A["econ_dep"], "AI EBIT (economic)": A["ebit_econ"],
        "Tax depreciation": -A["tax_dep"], "Cash taxes": -A["cash_tax"],
        "Book tax (at ETR)": -(A["ebit_book"] - A["nopat_book"]),
        "AI capex - growth": -A["capex_growth"], "AI capex - refresh/replacement": -A["capex_replacement"],
        "AI capex - total": -A["capex"], "AI FCF": A["fcf"],
        "AI invested capital (book)": A["ic_book"], "AI invested capital (economic)": A["ic_econ"],
        "AI ROIC (book)": A["roic_book"], "AI ROIC (economic)": A["roic_econ"],
        "AI incremental ROIC (vs 2026)": A["incr_roic"], "Monetised capacity utilisation": A["util_capacity"],
    }, index=Y).T
    fy = r["years"]
    core_capex = sum(s["capex"] for s in r["segments"].values())
    core_da = sum(s["da"] for s in r["segments"].values())
    AF = r["ai_forecast"]
    grp = pd.DataFrame({
        "Revenue": r["revenue"], "  of which AI": AF["revenue"],
        "EBIT (reported)": r["ebit"], "EPS (operating, ex interest)": r["eps"],
        "Core (maintenance + non-AI growth) capex": -core_capex,
        "AI capex - growth": -AF["capex_growth"], "AI capex - refresh": -AF["capex_replacement"],
        "Total capex": -r["capex"], "Capex / revenue": r["capex"] / r["revenue"],
        "D&A (core + AI book)": -(core_da + AF["book_dep"] + AF["writeoff"]),
        "FCF": r["fcf"], "FCF / net income": r["fcf_conversion"], "Group ROIC": r["roic"],
    }, index=fy).T
    t = tag or f"{co}_{scn}"
    ai.to_csv(os.path.join(OUT, f"{t}_ai_layer_annual.csv"))
    grp.to_csv(os.path.join(OUT, f"{t}_group_annual.csv"))
    return ai, grp, r


def fmt_annual(df, years):
    d = df[years].copy().astype(object)
    for i in d.index:
        for y in years:
            v = df.loc[i, y]
            if any(s in i for s in ["ROIC", "utilisation", "/ revenue", "/ net income"]):
                d.loc[i, y] = pct(v)
            elif "EPS" in i:
                d.loc[i, y] = f"{v:.2f}"
            else:
                d.loc[i, y] = f"{v:,.1f}"
    return d


def solve(co, knob, lo, hi, base_knobs=None, scn="base"):
    base_knobs = dict(base_knobs or {})
    target = PRICE[co]

    def f(x):
        kk = dict(base_knobs)
        kk[knob] = x
        return ps(co, scn, kk) - target
    try:
        flo, fhi = f(lo), f(hi)
        if flo * fhi > 0:
            return None, (flo + target, fhi + target)
        return brentq(f, lo, hi, xtol=1e-4), None
    except Exception as e:  # pragma: no cover
        return None, str(e)


def implied_metrics(co, knobs):
    c = build(co, "base", knobs)
    r = c.run()
    A = r["ai"]["total"]
    fy = r["years"]
    i36 = ai_idx(r, 2036)
    i26 = ai_idx(r, 2026)
    core_da = sum(s["da"] for s in r["segments"].values())
    da = core_da + r["ai_forecast"]["book_dep"] + r["ai_forecast"]["writeoff"]
    net_inv = (r["capex"] - da)[1:].sum()
    inc_roic = (r["nopat"][-1] - r["nopat"][0]) / net_inv if net_inv > 0 else float("nan")
    rev26 = (META["rev_2026"] if co == "META" else 331.8)
    return {
        "Revenue CAGR 2026-36": (r["revenue"][-1] / rev26) ** (1 / 10) - 1,
        "AI revenue 2036 ($bn)": A["revenue"][i36],
        "AI share of revenue 2036": A["revenue"][i36] / r["revenue"][-1],
        "AI EBIT margin 2036 (book)": A["ebit_book"][i36] / A["revenue"][i36] if A["revenue"][i36] else float("nan"),
        "AI economic ROIC 2036": A["roic_econ"][i36],
        "Group incremental ROIC 2027-36": inc_roic,
        "Capex/revenue avg 2027-31": float(np.mean(r["capex"][:5] / r["revenue"][:5])),
        "FCF conversion avg 2027-36": float(np.mean(r["fcf_conversion"])),
        "AI program IRR": r["ai"]["valuation"]["irr_program"],
    }


# --------------------------------------------------------------------------------------
# 1. scenario valuations
# --------------------------------------------------------------------------------------
def section_scenarios():
    h("1. Scenario valuations (no probabilities assigned)")
    res = {}
    for co in COS:
        rows = {LABEL[s]: summary_row(co, s) for s in SCENARIOS}
        df = pd.DataFrame(rows)
        df.T.to_csv(os.path.join(OUT, f"{co}_scenario_summary.csv"))
        res[co] = df
        h(f"{NAME[co]} - price ${PRICE[co]:.2f}", 3)
        para(md_table(fmt_summary(df.T).T))
    return res


# --------------------------------------------------------------------------------------
# 2. capex / depreciation / FCF decomposition
# --------------------------------------------------------------------------------------
def section_capex():
    h("2. AI capex, accounting D&A vs economic refresh, cash taxes, residual value")
    yrs = [2026, 2027, 2028, 2029, 2030, 2032, 2034, 2036]
    for co in COS:
        for scn in ["base", "bear_lite"]:
            ai, grp, r = annual_tables(co, scn)
            h(f"{NAME[co]} - {LABEL[scn]}: AI layer", 3)
            para(md_table(fmt_annual(ai, yrs)))
            h(f"{NAME[co]} - {LABEL[scn]}: group", 4)
            para(md_table(fmt_annual(grp, [2027, 2028, 2029, 2030, 2032, 2034, 2036])))
        for scn in ["bull", "bull_lite", "bear"]:
            annual_tables(co, scn)


# --------------------------------------------------------------------------------------
# 3. accelerator life tests
# --------------------------------------------------------------------------------------
def section_life():
    h("3. Accelerator life tests (3-6 years)")
    para("*Economic life* = how often GPUs/network are actually refreshed (drives replacement capex, "
         "FCF, value). *Book life* = depreciation policy (drives reported EPS only; tax depreciation "
         "is set by tax law so cash is unaffected).")
    for co in COS:
        rows = {}
        for L in [3, 4, 5, 6]:
            r = build(co, "base", {"econ_life": L}).run()
            A = r["ai"]["total"]
            i30 = ai_idx(r, 2030)
            j30 = r["years"].index(2030)
            rows[f"econ life {L}y"] = {
                "Value/share": r["per_share"], "AI NPV": r["ai_value"],
                "AI IRR": r["ai"]["valuation"]["irr_program"],
                "AI refresh capex 2030": A["capex_replacement"][i30],
                "FCF 2030": r["fcf"][j30], "AI econ ROIC 2030": A["roic_econ"][i30],
                "AI book ROIC 2030": A["roic_book"][i30], "EPS 2030": r["eps"][j30]}
        df = pd.DataFrame(rows).T
        df.to_csv(os.path.join(OUT, f"{co}_econ_life_test.csv"))
        h(f"{NAME[co]} - economic (refresh) life, book life at policy", 3)
        para(md_table(_fmt_mixed(df)))
        rows = {}
        for B in [3, 4, 5, 6]:
            r = build(co, "base", {"book_life": B}).run()
            A = r["ai"]["total"]
            rows[f"book life {B}y"] = {
                "EPS 2027": r["eps"][0], "EPS 2028": r["eps"][1], "EPS 2030": r["eps"][3],
                "AI book D&A 2028": A["book_dep"][ai_idx(r, 2028)] + A["writeoff"][ai_idx(r, 2028)],
                "FCF 2028": r["fcf"][1], "Value/share": r["per_share"]}
        df = pd.DataFrame(rows).T
        df.to_csv(os.path.join(OUT, f"{co}_book_life_test.csv"))
        h(f"{NAME[co]} - accounting life, economic life held at 5y", 3)
        para(md_table(_fmt_mixed(df)))


def _fmt_mixed(df):
    d = df.copy().astype(object)
    for c in d.columns:
        for i in d.index:
            v = df.loc[i, c]
            if "ROIC" in c or "IRR" in c or c.startswith("vs") or "util" in c.lower():
                d.loc[i, c] = pct(v)
            elif "EPS" in c or "share" in c:
                d.loc[i, c] = f"{v:,.2f}"
            else:
                d.loc[i, c] = f"{v:,.1f}"
    return d


# --------------------------------------------------------------------------------------
# 4. capex-elevated-longer and monetisation delay
# --------------------------------------------------------------------------------------
def section_capex_delay():
    h("4. AI capex sensitivity: elevated for longer, and monetisation delay")
    for co in COS:
        for scn, knob, lab in [("base", "capex_extend", "Base demand: capex held at final explicit level for +N years"),
                               ("bear_lite", "capex_extend", "Bear-lite demand: capex held at final explicit level for +N years"),
                               ("base", "delay", "Base: AI monetisation delayed N years (capex unchanged)")]:
            rows = {}
            for n in [0, 1, 2, 3]:
                r = build(co, scn, {knob: n}).run()
                A = r["ai"]["total"]
                i30 = ai_idx(r, 2030)
                rows[f"+{n}y"] = {"Value/share": r["per_share"], "vs price": r["upside"],
                                  "AI NPV": r["ai_value"], "AI IRR": r["ai"]["valuation"]["irr_program"],
                                  "Util 2030": A["util_capacity"][i30],
                                  "AI econ ROIC 2030": A["roic_econ"][i30],
                                  "Cum. FCF 2027-31": r["fcf"][:5].sum(), "EPS 2029": r["eps"][2]}
            df = pd.DataFrame(rows).T
            df.to_csv(os.path.join(OUT, f"{co}_{scn}_{knob}.csv"))
            h(f"{NAME[co]} - {lab}", 3)
            para(md_table(_fmt_mixed(df)))


# --------------------------------------------------------------------------------------
# 5. tornado + grids
# --------------------------------------------------------------------------------------
TORNADO = {
    "META": [
        ("AI monetisation (uplift & new products x0.6 / x1.4)", {"ai_rev_scale": 0.6}, {"ai_rev_scale": 1.4}),
        ("Ads AI uplift share 2031+ (20% / 36%)", {"uplift_terminal": 0.20}, {"uplift_terminal": 0.36}),
        ("Revenue per $/GW of new capacity (x0.7 / x1.3)", {"yield_mult": 0.7}, {"yield_mult": 1.3}),
        ("New AI product revenue (x0.5 / x2)", {"newprod_scale": 0.5}, {"newprod_scale": 2.0}),
        ("Training spend after 2029 (+3%/yr / -12%/yr)", {"train_g": 0.03}, {"train_g": -0.12}),
        ("AI capex, explicit years (x1.2 / x0.8)", {"capex_scale": 1.2}, {"capex_scale": 0.8}),
        ("AI incremental margin (var cost +10pp / -10pp)", {"var_cost_shift": 0.10}, {"var_cost_shift": -0.10}),
        ("Accelerator economic life (4y / 6y)", {"econ_life": 4}, {"econ_life": 6}),
        ("Price erosion per year of age (18% / 6%)", {"erosion": 0.18}, {"erosion": 0.06}),
        ("WACC (+1pp / -1pp)", {"wacc_shift": 0.01}, {"wacc_shift": -0.01}),
        ("Terminal growth (2% / 4%)", {"g_term": 0.02}, {"g_term": 0.04}),
        ("Monetisation timing (2y delay / none)", {"delay": 2}, {"delay": 0}),
        ("Core ad growth (-2pp / +2pp)", {"core_g_shift": -0.02}, {"core_g_shift": 0.02}),
        ("Core margin (-4pp / +4pp)", {"core_margin_shift": -0.04}, {"core_margin_shift": 0.04}),
        ("AI hurdle premium (2pp / 0pp)", {"ai_premium": 0.02}, {"ai_premium": 0.0}),
    ],
    "MSFT": [
        ("AI monetisation (all AI rev growth x0.6 / x1.4)", {"ai_rev_scale": 0.6}, {"ai_rev_scale": 1.4}),
        ("Revenue per $/GW of new Azure AI capacity (x0.7 / x1.3)", {"yield_mult": 0.7}, {"yield_mult": 1.3}),
        ("Copilot/1P AI revenue (x0.5 / x1.5)", {"copilot_scale": 0.5}, {"copilot_scale": 1.5}),
        ("Max utilisation (75% / 97%)", {"u_max": 0.75}, {"u_max": 0.97}),
        ("AI capex, explicit years (x1.2 / x0.8)", {"capex_scale": 1.2}, {"capex_scale": 0.8}),
        ("AI incremental margin (var cost +10pp / -10pp)", {"var_cost_shift": 0.10}, {"var_cost_shift": -0.10}),
        ("Accelerator economic life (4y / 6y)", {"econ_life": 4}, {"econ_life": 6}),
        ("Price erosion per year of age (18% / 6%)", {"erosion": 0.18}, {"erosion": 0.06}),
        ("WACC (+1pp / -1pp)", {"wacc_shift": 0.01}, {"wacc_shift": -0.01}),
        ("Terminal growth (2% / 4%)", {"g_term": 0.02}, {"g_term": 0.04}),
        ("Monetisation timing (2y delay / none)", {"delay": 2}, {"delay": 0}),
        ("Core growth (-2pp / +2pp)", {"core_g_shift": -0.02}, {"core_g_shift": 0.02}),
        ("Core margin (-4pp / +4pp)", {"core_margin_shift": -0.04}, {"core_margin_shift": 0.04}),
        ("MAI training spend after FY31 (+3%/yr / -12%/yr)", {"train_g": 0.03}, {"train_g": -0.12}),
        ("OpenAI demand shortfall (30% from FY28 / none)", {"openai_shortfall": 0.30}, {"openai_shortfall": 0.0}),
        ("AI hurdle premium (2pp / 0pp)", {"ai_premium": 0.02}, {"ai_premium": 0.0}),
    ],
}


def section_tornado():
    h("5. Stress test - what actually drives value (base scenario, one driver at a time)")
    for co in COS:
        base = ps(co)
        rows = {}
        for lab, lo, hi in TORNADO[co]:
            a, b = ps(co, "base", lo), ps(co, "base", hi)
            rows[lab] = {"Downside $/sh": a, "Upside $/sh": b, "Down Δ": a - base, "Up Δ": b - base,
                         "Swing": abs(b - a)}
        df = pd.DataFrame(rows).T.sort_values("Swing", ascending=False)
        df.to_csv(os.path.join(OUT, f"{co}_tornado.csv"))
        h(f"{NAME[co]} - base value ${base:,.0f} vs price ${PRICE[co]:,.0f}", 3)
        para(md_table(df, "{:,.0f}"))

        # grids
        g1 = pd.DataFrame({f"g={g:.1%}": {f"WACC {w:+.1%}": ps(co, "base", {"wacc_shift": w, "g_term": g})
                                          for w in [-0.015, -0.01, -0.005, 0.0, 0.005, 0.01]}
                           for g in [0.02, 0.025, 0.03, 0.035, 0.04]})
        g1.to_csv(os.path.join(OUT, f"{co}_grid_wacc_g.csv"))
        h(f"{NAME[co]} - value/share: WACC shift x terminal growth", 4)
        para(md_table(g1, "{:,.0f}"))
        g2 = pd.DataFrame({f"life {L}y": {f"AI rev x{m}": ps(co, "base", {"ai_rev_scale": m, "econ_life": L})
                                          for m in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]}
                           for L in [3, 4, 5, 6]})
        g2.to_csv(os.path.join(OUT, f"{co}_grid_life_monetisation.csv"))
        h(f"{NAME[co]} - value/share: AI monetisation x accelerator economic life", 4)
        para(md_table(g2, "{:,.0f}"))
        g3 = pd.DataFrame({f"capex x{c}": {f"AI rev x{m}": build(co, "base", {"ai_rev_scale": m, "capex_scale": c}).run()["ai_value"]
                                           for m in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]}
                           for c in [0.7, 0.85, 1.0, 1.15, 1.3]})
        g3.to_csv(os.path.join(OUT, f"{co}_grid_capex_monetisation_ainpv.csv"))
        h(f"{NAME[co]} - AI layer NPV ($bn): explicit AI capex x AI monetisation", 4)
        para(md_table(g3, "{:,.0f}"))


# --------------------------------------------------------------------------------------
# 6. reverse DCF
# --------------------------------------------------------------------------------------
REV_KNOBS = {
    "META": [
        ("AI monetisation scale (x base AI revenue growth)", "ai_rev_scale", 0.0, 6.0),
        ("Ads AI-uplift share of ad revenue (terminal)", "uplift_terminal", 0.05, 0.80),
        ("Core ad growth shift (pp every year)", "core_g_shift", -0.10, 0.10),
        ("Core margin shift (pp)", "core_margin_shift", -0.25, 0.25),
        ("AI variable-cost shift (pp; negative = higher AI margin)", "var_cost_shift", -0.25, 0.60),
        ("Explicit AI capex scale", "capex_scale", 0.2, 2.5),
        ("AI terminal RONIC override", "terminal_ronic", 0.10, 1.50),
        ("WACC shift (pp)", "wacc_shift", -0.05, 0.05),
        ("Terminal growth", "g_term", 0.0, 0.06),
        ("Price erosion per year of age", "erosion", 0.0, 0.40),
        ("Revenue per $/GW of new AI capacity (x base)", "yield_mult", 0.3, 5.0),
        ("Training spend growth after 2029 (policy)", "train_g", -0.40, 0.10),
    ],
    "MSFT": [
        ("AI monetisation scale (x base AI revenue growth)", "ai_rev_scale", 0.0, 6.0),
        ("Copilot / 1P AI revenue scale", "copilot_scale", 0.0, 8.0),
        ("Core growth shift (pp every year)", "core_g_shift", -0.10, 0.10),
        ("Core margin shift (pp)", "core_margin_shift", -0.25, 0.25),
        ("AI variable-cost shift (pp; negative = higher AI margin)", "var_cost_shift", -0.25, 0.60),
        ("Explicit AI capex scale", "capex_scale", 0.2, 2.5),
        ("AI terminal RONIC override", "terminal_ronic", 0.10, 1.50),
        ("WACC shift (pp)", "wacc_shift", -0.05, 0.05),
        ("Terminal growth", "g_term", 0.0, 0.06),
        ("Price erosion per year of age", "erosion", 0.0, 0.40),
        ("Revenue per $/GW of new Azure AI capacity (x base)", "yield_mult", 0.3, 5.0),
        ("MAI training spend growth after FY31 (policy)", "train_g", -0.40, 0.10),
    ],
}


def section_reverse():
    h("6. Reverse DCF - what today's price requires (one assumption at a time, rest at base)")
    out = {}
    for co in COS:
        base_m = implied_metrics(co, {})
        rows = {"(base model)": {"Solved value": "-", **{k: v for k, v in base_m.items()}}}
        for lab, knob, lo, hi in REV_KNOBS[co]:
            x, note = solve(co, knob, lo, hi)
            if x is None:
                rows[lab] = {"Solved value": f"no solution in [{lo}, {hi}] (range {note[0]:.0f}-{note[1]:.0f} $/sh)"
                             if isinstance(note, tuple) else f"error {note}"}
                continue
            m = implied_metrics(co, {knob: x})
            sv = f"{x:.3f}" if abs(x) >= 0.1 or knob.endswith("scale") else f"{x:+.2%}"
            if knob in ("wacc_shift", "core_g_shift", "core_margin_shift", "var_cost_shift"):
                sv = f"{x:+.2%}"
            if knob in ("g_term", "erosion", "uplift_terminal", "terminal_ronic", "train_g"):
                sv = f"{x:.2%}"
            if knob == "wacc_shift":
                w = (META["wacc"] if co == "META" else MSFT["wacc"]) + x
                sv += f" (WACC {w:.2%})"
            rows[lab] = {"Solved value": sv, **m}
        # economic life: integer scan
        lifes = {L: ps(co, "base", {"econ_life": L}) for L in range(3, 11)}
        ok = [L for L, v in lifes.items() if v >= PRICE[co]]
        rows["Accelerator economic life (years)"] = {
            "Solved value": (f">= {min(ok)}y" if ok else f"none <=10y (10y gives ${lifes[10]:,.0f})")}
        df = pd.DataFrame(rows).T
        df.to_csv(os.path.join(OUT, f"{co}_reverse_dcf.csv"))
        out[co] = df
        d = df.copy().astype(object)
        for c in d.columns:
            if c == "Solved value":
                continue
            for i in d.index:
                v = df.loc[i, c]
                if isinstance(v, float) and math.isnan(v):
                    d.loc[i, c] = ""
                elif "($bn)" in c:
                    d.loc[i, c] = f"{v:,.0f}"
                else:
                    d.loc[i, c] = pct(v)
        h(f"{NAME[co]} - price ${PRICE[co]:.2f}", 3)
        para(md_table(d))

        # market-implied value of the AI layer
        c = build(co, "base")
        r = c.run()
        mcap = PRICE[co] * c.shares
        implied_ai = mcap + c.net_debt - sum(c.nonop.values()) - sum(r["core_values"].values())
        wrows = {}
        for w in [-0.01, -0.005, 0.0, 0.005, 0.01]:
            cw = build(co, "base", {"wacc_shift": w})
            rw = cw.run()
            wrows[f"WACC {cw.segments[0].wacc:.2%}"] = {
                "Non-AI segments value": sum(rw["core_values"].values()),
                "Market-implied AI value": mcap + cw.net_debt - sum(cw.nonop.values()) - sum(rw["core_values"].values()),
                "Model AI NPV (base)": rw["ai_value"]}
        wdf = pd.DataFrame(wrows).T
        wdf.to_csv(os.path.join(OUT, f"{co}_implied_ai_value_vs_wacc.csv"))
        para(md_table(wdf, "{:,.0f}"))
        para(f"Market cap ${mcap:,.0f}bn; + net debt ${c.net_debt:,.0f}bn; - non-operating "
             f"${sum(c.nonop.values()):,.0f}bn; - base value of non-AI segments "
             f"${sum(r['core_values'].values()):,.0f}bn => **market-implied AI layer value "
             f"${implied_ai:,.0f}bn** vs base-case AI NPV ${r['ai_value']:,.0f}bn.")
        # combined: what must be true jointly
    return out


def section_roic_defined():
    h("6b. Scenarios as *defined by returns*: what operating assumptions deliver them?")
    para("The Bull/Base/Bear labels were specified in ROIC terms (Bull: incremental AI ROIC comfortably above "
         "WACC; Base: returns converge to reasonable levels; Bear-lite: toward WACC; Bear: below). The "
         "evidence-anchored scenarios above do not reach those return levels. Here the AI monetisation scale "
         "(all AI revenue growth vs base, everything else at base) is solved so that the 2036 economic ROIC "
         "of the whole AI layer hits each target, and the resulting AI revenue and value are shown.")
    for co in COS:
        hurdle = build(co, "base").ai.hurdle
        rows = {}
        for lab, tgt in [("AI ROIC = hurdle - 4pp", hurdle - 0.04), ("AI ROIC = hurdle", hurdle),
                         ("AI ROIC = hurdle + 4pp (Bull as defined)", hurdle + 0.04),
                         ("AI ROIC = hurdle + 8pp", hurdle + 0.08)]:
            def f(m):
                r = build(co, "base", {"ai_rev_scale": m}).run()
                return r["ai"]["total"]["roic_econ"][-1] - tgt
            try:
                m = brentq(f, 0.2, 8.0, xtol=1e-3)
            except Exception:
                rows[lab] = {"AI rev scale": float("nan")}
                continue
            r = build(co, "base", {"ai_rev_scale": m}).run()
            A = r["ai"]["total"]
            i30, i36 = ai_idx(r, 2030), ai_idx(r, 2036)
            rows[lab] = {"AI rev scale": m, "Target ROIC": tgt, "AI rev 2030": A["revenue"][i30],
                         "AI rev 2036": A["revenue"][i36],
                         "AI rev CAGR 2026-36": (A["revenue"][i36] / A["revenue"][ai_idx(r, 2026)]) ** 0.1 - 1,
                         "AI capex 2030": A["capex"][i30], "AI NPV": r["ai_value"],
                         "Value/share": r["per_share"], "vs price": r["upside"]}
        df = pd.DataFrame(rows).T
        df.to_csv(os.path.join(OUT, f"{co}_roic_defined.csv"))
        h(f"{NAME[co]} (AI hurdle {hurdle:.2%})", 3)
        d = df.copy().astype(object)
        for c in d.columns:
            for i in d.index:
                v = df.loc[i, c]
                if c in ("Target ROIC", "AI rev CAGR 2026-36", "vs price"):
                    d.loc[i, c] = pct(v)
                elif c == "AI rev scale":
                    d.loc[i, c] = f"x{v:.2f}"
                elif c == "Value/share":
                    d.loc[i, c] = f"{v:,.0f}"
                else:
                    d.loc[i, c] = f"{v:,.0f}"
        para(md_table(d))


# --------------------------------------------------------------------------------------
# 7. company-specific tests
# --------------------------------------------------------------------------------------
def section_meta_ads():
    h("7a. Meta - how much AI infrastructure can better advertising justify on its own?")
    rows = {}
    for scn in SCENARIOS:
        full = build("META", scn).run()
        ads = build("META", scn, {"ads_only": True}).run()
        sv = full["ai"]["stream_valuation"]
        rows[LABEL[scn]] = {
            "Ads-uplift stream NPV (own compute share)": sv["Ads ranking & recommendation uplift"]["npv"],
            "Ads-uplift stream IRR": sv["Ads ranking & recommendation uplift"]["irr_program"],
            "Training/MSL NPV": sv["Frontier models / MSL training"]["npv"],
            "New products NPV": sv["New AI products & compute resale"]["npv"],
            "Whole AI program NPV": full["ai_value"],
            "AI NPV if ads must pay for everything": ads["ai_value"],
            "Value/share (ads-only)": ads["per_share"]}
    df = pd.DataFrame(rows).T
    df.to_csv(os.path.join(OUT, "META_ads_justification.csv"))
    para(md_table(_fmt_mixed(df)))

    # breakeven capex scale with ads only
    def f(scale):
        return build("META", "base", {"ads_only": True, "capex_scale": scale}).run()["ai_value"]
    lines = []
    try:
        s0 = brentq(f, 0.05, 1.5, xtol=1e-3)
        avg = np.mean(META_capex_explicit("base")) * s0
        rr = build("META", "base").run()
        core_cx = float(np.mean(sum(sg["capex"] for sg in rr["segments"].values())[:3]))
        lines.append(f"- Ads-only break-even: explicit 2027-29 AI capex x{s0:.2f} of base "
                     f"(~${avg:,.0f}bn/yr AI capex, ~${avg + core_cx:,.0f}bn/yr total incl. ~${core_cx:,.0f}bn core) "
                     f"vs base ${np.mean(META_capex_explicit('base')):,.0f}bn/yr AI "
                     f"(post-2029 refresh scales with the smaller installed base).")
    except Exception as e:
        lines.append(f"- Ads-only break-even capex: no root ({e}).")
    # uplift needed for whole programme with no new products
    def g(u):
        return build("META", "base", {"ads_only": True, "uplift_terminal": u}).run()["ai_value"]
    try:
        u0 = brentq(g, 0.10, 0.90, xtol=1e-3)
        lines.append(f"- Ad-revenue AI uplift needed for the full base capex plan with **no** new AI revenue: "
                     f"{u0:.0%} of total ad revenue by 2031 (base assumption 28%; 2026E estimate 15%).")
    except Exception as e:
        lines.append(f"- Uplift needed: no root in range ({e}).")
    # uplift needed for AI NPV=0 with base new products
    def g2(u):
        return build("META", "base", {"uplift_terminal": u}).run()["ai_value"]
    try:
        u1 = brentq(g2, 0.10, 0.90, xtol=1e-3)
        lines.append(f"- Uplift needed for AI NPV = 0 *with* base new-product revenue: {u1:.0%}.")
    except Exception as e:
        lines.append(f"- Uplift needed (with new products): no root ({e}).")
    para("\n".join(lines))


def META_capex_explicit(scn):
    from inputs import META_SCN
    return META_SCN[scn]["capex"]


def section_msft_openai():
    h("7b. Microsoft - does Azure + Copilot + AI services earn back the capex? What does OpenAI change?")
    rows = {}
    for scn in SCENARIOS:
        r = build("MSFT", scn).run()
        sv = r["ai"]["stream_valuation"]
        rows[LABEL[scn]] = {k.split(" (")[0] + " NPV": v["npv"] for k, v in sv.items()}
        rows[LABEL[scn]]["Azure AI IRR"] = sv["Azure AI infrastructure (incl. OpenAI)"]["irr_program"]
        rows[LABEL[scn]]["1P AI IRR"] = sv["First-party AI apps (Copilot, GitHub, agents)"]["irr_program"]
        rows[LABEL[scn]]["AI program NPV"] = r["ai_value"]
        A = r["ai"]["total"]
        rows[LABEL[scn]]["Cum. AI FCF FY27-31"] = A["fcf"][ai_idx(r, 2027):ai_idx(r, 2031) + 1].sum()
        rows[LABEL[scn]]["Cum. AI FCF FY32-36"] = A["fcf"][ai_idx(r, 2032):].sum()
    df = pd.DataFrame(rows).T
    df.to_csv(os.path.join(OUT, "MSFT_ai_streams.csv"))
    para(md_table(_fmt_mixed(df)))

    variants = [
        ("Base", {}),
        ("No OpenAI revenue share", {"revshare_on": False}),
        ("OpenAI takes 30% of Azure AI demand elsewhere from FY28", {"openai_shortfall": 0.30}),
        ("OpenAI demand re-priced 15% lower on new capacity", {"openai_price_cut": 0.15}),
        ("OpenAI stake at $0", {"stake_value": 0.0}),
        ("OpenAI stake at $1.5tn val (no haircut)", {"stake_value": 1500 * MSFT["openai_stake_pct"]}),
        ("Combined OpenAI downside (shortfall 30%, no rev share, stake $35bn)",
         {"openai_shortfall": 0.30, "revshare_on": False, "stake_value": 35.0}),
    ]
    rows = {}
    for lab, kn in variants:
        r = build("MSFT", "base", kn).run()
        c = build("MSFT", "base", kn)
        rows[lab] = {"Value/share": r["per_share"], "AI NPV": r["ai_value"],
                     "OpenAI stake": sum(c.nonop.values()),
                     "AI IRR": r["ai"]["valuation"]["irr_program"],
                     "Util FY30": r["ai"]["total"]["util_capacity"][ai_idx(r, 2030)]}
    df = pd.DataFrame(rows).T
    df.to_csv(os.path.join(OUT, "MSFT_openai_variants.csv"))
    h("OpenAI variants (base scenario)", 3)
    para(md_table(_fmt_mixed(df)))


def section_position():
    h("8. Where does the price sit across the scenario range?")
    for co in COS:
        vals = {LABEL[s]: ps(co, s) for s in SCENARIOS}
        p = PRICE[co]
        srt = sorted(vals.items(), key=lambda kv: kv[1])
        pos = "below Bear" if p < srt[0][1] else "above Bull" if p > srt[-1][1] else None
        if pos is None:
            for (la, va), (lb, vb) in zip(srt[:-1], srt[1:]):
                if va <= p <= vb:
                    pos = f"between {la} (${va:,.0f}) and {lb} (${vb:,.0f}), {(p - va) / (vb - va):.0%} of the way"
        para(f"- **{NAME[co]}** ${p:,.0f}: " + ", ".join(f"{k} ${v:,.0f}" for k, v in vals.items()) + f" -> price is {pos}.")


def section_per_gw():
    h("9. Unit economics translated to revenue per GW and per GPU")
    from inputs import EQUIP_PER_GW
    rows = {}
    y_ms = build("MSFT", "base").meta["azure_yield"]
    from inputs import META_SCN
    for lab, y in [("MSFT Azure AI (calibrated to FY26)", y_ms),
                   ("Meta new AI products - Bull", META_SCN["bull"]["np_yield"]),
                   ("Meta new AI products - Base", META_SCN["base"]["np_yield"]),
                   ("Meta new AI products - Bear", META_SCN["bear"]["np_yield"]),
                   ("Benchmark: Oracle-OpenAI (~$60bn/yr for ~4.5GW)", 60 / 4.5 / EQUIP_PER_GW)]:
        rows[lab] = {"Yield ($ rev per $ equipment, 100% util)": y,
                     "Revenue per GW-year at 100% util ($bn)": y * EQUIP_PER_GW,
                     "At 85% util ($bn)": y * EQUIP_PER_GW * 0.85,
                     "Per GPU-hour (~$70k all-in per GPU)": y * 70000 / 8760}
    df = pd.DataFrame(rows).T
    df.to_csv(os.path.join(OUT, "unit_economics_per_gw.csv"))
    para(md_table(df, "{:,.2f}"))
    para(f"Assumes ~${EQUIP_PER_GW:.0f}bn of accelerator/server/network content per GW (of ~$50-60bn all-in "
         "incl. shell and power). Revenue per GW falls each year a vintage ages (price erosion) and new "
         "vintages earn yield x (1+drift)^(years after 2026).")


def section_calibration():
    h("0. Calibration checks (model vs reported / consensus)")
    rows = {}
    for co in COS:
        c = build(co, "base")
        r = c.run()
        i26 = ai_idx(r, 2026)
        A = r["ai"]["total"]
        rows[NAME[co]] = {
            "Core margin (calibrated, ex-AI)": c.meta["core_margin0"] if co == "META" else c.meta["core_margin0"][0],
            "AI revenue base yr": A["revenue"][i26], "AI EBIT base yr (book)": A["ebit_book"][i26],
            "AI capex base yr": A["capex"][i26], "AI book ROIC base yr": A["roic_book"][i26],
            "AI econ ROIC base yr": A["roic_econ"][i26],
            "Model revenue yr1": r["revenue"][0], "Model EPS yr1": r["eps"][0], "Model EPS yr2": r["eps"][1]}
    df = pd.DataFrame(rows).T
    d = df.copy().astype(object)
    for cidx in d.columns:
        for i in d.index:
            v = df.loc[i, cidx]
            d.loc[i, cidx] = pct(v) if ("margin" in cidx or "ROIC" in cidx) else f"{v:,.2f}"
    para(md_table(d))
    para("Consensus reference: Meta 2027 EPS ~$31-33, revenue growth ~15-16%, 2027 capex ~$190bn; "
         "Microsoft FY27 EPS ~$19.96, revenue growth ~17.9%, FY27 capex ~$175bn reported. "
         "Model EPS is operating EPS (no interest income, simplified tax), so a small gap is expected.")
    para(f"Microsoft Azure AI calibrated revenue yield: {build('MSFT', 'base').meta['azure_yield']:.2f} "
         "$ revenue per $ of AI equipment per year at 100% utilisation (FY26 pricing).")


def main():
    for f in os.listdir(OUT):
        if f.endswith(".csv") or f.endswith(".md"):
            os.remove(os.path.join(OUT, f))
    MD.append("# Model results (auto-generated by analysis.py)\n")
    MD.append("USD bn unless stated. Valuation date 30-Sep-2026. All scenario values are *unweighted*.\n")
    section_calibration()
    section_scenarios()
    section_capex()
    section_life()
    section_capex_delay()
    section_tornado()
    section_reverse()
    section_roic_defined()
    section_meta_ads()
    section_msft_openai()
    section_position()
    section_per_gw()
    with open(os.path.join(OUT, "model_results.md"), "w") as f:
        f.write("\n".join(MD))
    print("wrote", os.path.join(OUT, "model_results.md"))


if __name__ == "__main__":
    main()
