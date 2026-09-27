"""
Asset-based NAV model for Constellation Energy (CEG) and Vistra (VST).

Method (per asset group, per year, per scenario):
    merchant energy margin + capacity revenue + contracted PPA revenue + ZEC/45U support
    - operating cost (fuel, O&M, sustaining capex)   ->  after-tax asset cash flow
    discounted at an asset-risk rate to the valuation date, until end of (licensed/assumed) life.
    Sum of assets = Gross Asset Value (GAV); less capitalised corporate overhead; less net claims
    (debt, preferred, pensions, pending-deal cash) = Equity NAV.

The company's reported revenue/EPS is never used. The market price is used only at the end,
to (a) compare, and (b) solve for the power price the market is implicitly paying for.

Run:  python3 nav_model.py        -> prints summary, writes outputs/*.csv, outputs/nav_model.xlsx, outputs/tables.md
"""
import csv
import copy
import os

import inputs as I

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
PJM_HUBS = {"PJMW", "PJMA", "NIHUB"}


# ---------------------------------------------------------------------------
# Price deck
# ---------------------------------------------------------------------------
class Deck:
    """Scenario price deck. `shift` = additive real $/MWh on long-run ATC prices (all hubs);
    `gas_shift` = additive real $/MMBtu on Henry Hub (flows into power via implied heat rate);
    `pjm_cap` overrides long-run PJM capacity price (2026$/MW-day)."""

    def __init__(self, scen, shift=0.0, gas_shift=0.0, pjm_cap=None):
        self.name = scen
        self.s = I.SCENARIOS[scen]
        self.shift = shift
        self.gas_shift = gas_shift
        self.pjm_cap = pjm_cap if pjm_cap is not None else self.s["pjm_cap"]

    @staticmethod
    def infl(y):
        return (1 + I.INFLATION) ** (y - 2026)

    def hh_real(self, y):
        return I.HENRY_HUB_REAL.get(y, I.HENRY_HUB_LR_REAL) + self.gas_shift

    def gas_nom(self, hub, y):
        return (self.hh_real(y) + I.GAS_BASIS[hub]) * self.infl(y)

    def lr_atc_real(self, hub):
        lr_gas = lambda h: I.HENRY_HUB_LR_REAL + self.gas_shift + I.GAS_BASIS[h]
        if hub == "ERCOT":
            base = self.s["ihr_ercot"] * lr_gas("ERCOT")
        else:
            base = self.s["ihr_pjm"] * lr_gas("PJMW") * I.HUB_RATIO_TO_PJMW[hub]
        return base + self.shift

    def fwd_nom(self, hub, y):
        if hub == "ERCOT":
            return I.FORWARD_ATC["ERCOT"][y]
        return I.FORWARD_ATC["PJMW"][y] * I.HUB_RATIO_TO_PJMW[hub]

    def atc(self, hub, y):
        """Nominal ATC $/MWh."""
        lr = self.lr_atc_real(hub) * self.infl(y)
        if y <= 2028:
            return self.fwd_nom(hub, y)
        if y == 2029:
            return 0.5 * self.fwd_nom(hub, y) + 0.5 * lr
        return lr

    def cap(self, hub, y):
        """Nominal capacity price, $/MW-day."""
        if hub in PJM_HUBS:
            lr = self.pjm_cap * self.infl(y)
            if y in I.PJM_CAPACITY_CY:
                return I.PJM_CAPACITY_CY[y]
            if y == 2029:
                return 5 / 12 * I.PJM_CAPACITY_KNOWN["2028/29"] + 7 / 12 * lr
            return lr
        if hub == "ERCOT":
            return 0.0
        key = "west_cap" if hub == "WEST" else "other_cap"
        real = I.SCENARIOS["Base"][key] if y <= 2028 else self.s[key]
        return real * self.infl(y)


# ---------------------------------------------------------------------------
# Asset valuation
# ---------------------------------------------------------------------------
def contracted_mw(asset, y):
    mw = 0.0
    for c in asset.get("contracts", []):
        if c["start"] <= y <= c["end"]:
            if isinstance(c["mw"], dict):
                known = [v for k, v in c["mw"].items() if k <= y]
                mw += c["mw"].get(y, c["mw_full"] if y > max(c["mw"]) else (known[-1] if known else 0))
            else:
                mw += c["mw"]
    return min(mw, asset["mw"])


def contract_price(asset, y):
    for c in asset.get("contracts", []):
        if c["start"] <= y <= c["end"]:
            return c["price"] * (1 + c.get("esc", 0.0)) ** (y - c["start"])
    return 0.0


def df(rate, y):
    return (1 + rate) ** -(y + 0.5 - I.VALUATION_DATE)


def value_asset(a, deck, opts):
    """Return dict(pv=$mm, first_year_ebitda=$mm, cashflows=list)."""
    tech = a["tech"]
    hub = a["hub"]
    tax = 1 - I.CASH_TAX_RATE
    ppa_adj = opts.get("ppa_adj", 0.0)
    disc_adj = opts.get("disc_adj", 0.0)

    if tech == "renewable":
        base_lr = Deck("Base").lr_atc_real("PJMW")
        rel = deck.lr_atc_real("PJMW") / base_lr - 1
        pv = a["mw"] * 1000 * a["usd_per_kw"] * (1 + 0.4 * rel) / 1e6
        return {"pv": pv, "ebitda27": None, "cfs": []}

    T = I.TECH[tech]
    end = a["end"]
    if tech == "nuclear" and opts.get("nuc_end") is not None:
        end = opts["nuc_end"] if a["end"] >= 2050 else a["end"]
    pv = 0.0
    ebitda27 = None
    cfs = []
    for y in range(max(a["start"], I.FIRST_YEAR), end + 1):
        P = deck.atc(hub, y)
        capp = deck.cap(hub, y)
        infl = Deck.infl(y)
        mw = a["mw"]
        pre_merch = pre_con = post_credit = 0.0

        if tech == "nuclear":
            cf = T["cf"]
            cmw = contracted_mw(a, y)
            mmw = mw - cmw
            gen_m = mmw * 8760 * cf
            gen_c = cmw * 8760 * cf
            cost_mwh = T["cost_mwh"] * (1 + T["cost_esc"]) ** (y - 2026)
            e_rev = gen_m * P * I.NUCLEAR_CAPTURE.get(hub, T["capture"])
            c_rev = mmw * capp * 365 * I.ACCREDITATION["nuclear"]
            zec = gen_m * a["zec"]["price"] if a.get("zec") and y <= a["zec"]["end"] else 0.0
            pre_merch = e_rev + c_rev + zec - gen_m * cost_mwh
            pre_con = gen_c * ((contract_price(a, y) + ppa_adj) - cost_mwh)
            if y <= I.PTC45U["last_year"] and not opts.get("no_45u") and gen_m > 0:
                k = (1 + I.INFLATION) ** (y - I.PTC45U["base_year"])
                gr = (e_rev + c_rev + zec) / gen_m
                credit = max(0.0, I.PTC45U["credit"] * k - 0.8 * max(0.0, gr - I.PTC45U["threshold"] * k))
                post_credit = gen_m * credit
            capex = a.get("capex", {}).get(y, 0.0) * 1e9
            pre_merch -= capex
            r_m = T["disc"] + disc_adj
            r_c = T["disc_contract"] + disc_adj
            cf_after = (pre_merch * tax + post_credit) * df(r_m, y) + pre_con * tax * df(r_c, y)
            ebitda = pre_merch + pre_con + capex

        elif tech in ("ccgt", "peaker", "coal"):
            if tech == "ccgt":
                cf = I.CCGT_CF[hub]
                captured = P * I.CCGT_CAPTURE[hub]
                fuel = a.get("heat_rate", T["heat_rate"]) * (deck.gas_nom(hub, y) + I.FUEL_ADDER * infl)
            elif tech == "peaker":
                cf = T["cf"]
                captured = P * deck.s["scarcity_mult"]
                fuel = T["heat_rate"] * (deck.gas_nom(hub, y) + I.FUEL_ADDER * infl)
            else:
                cf = T["cf"]
                captured = P * T["capture"]
                fuel = T["heat_rate"] * T["fuel"] * infl
            gen = mw * 8760 * cf
            margin = max(captured - fuel - T["vom"] * infl, 0.0) * gen
            c_rev = mw * capp * 365 * I.ACCREDITATION[tech]
            fixed = mw * 1000 * (T["fom_kw"] + T["capex_kw"]) * infl
            ebitda = margin + c_rev - mw * 1000 * T["fom_kw"] * infl
            pre = max(margin + c_rev - fixed, 0.0)  # mothball option: never worse than zero
            cf_after = pre * tax * df(T["disc"] + disc_adj, y)

        elif tech == "hydro":
            gen = mw * 8760 * T["cf"]
            rev = gen * P * T["capture"] + mw * capp * 365 * I.ACCREDITATION["hydro"]
            ebitda = rev - mw * 1000 * T["fom_kw"] * infl
            cf_after = ebitda * tax * df(T["disc"] + disc_adj, y)

        elif tech == "geothermal":
            gen = mw * 8760 * T["cf"]
            cmw = contracted_mw(a, y)
            price = (contract_price(a, y) + ppa_adj) if cmw else P * 1.10
            rev = gen * price + (0 if cmw else mw * capp * 365 * I.ACCREDITATION["geothermal"])
            ebitda = rev - gen * T["cost_mwh"] * (1.025 ** (y - 2026))
            cf_after = ebitda * tax * df(T["disc"] + disc_adj, y)
        else:
            raise ValueError(tech)

        pv += cf_after
        if y == 2027 or (ebitda27 is None and y == a["start"]):
            ebitda27 = ebitda / 1e6 if ebitda27 is None else ebitda27
        cfs.append((y, ebitda / 1e6))
    return {"pv": pv / 1e6, "ebitda27": ebitda27, "cfs": cfs}


def corp_overhead_pv(co, disc_adj=0.0):
    oh = I.CORP_OVERHEAD_MM[co]
    return sum(oh * Deck.infl(y) * (1 - I.CASH_TAX_RATE) * df(0.085 + disc_adj, y) for y in range(2027, 2057))


def company_nav(co, deck, opts=None):
    opts = opts or {}
    assets = I.CEG_ASSETS if co == "CEG" else I.VST_ASSETS
    claims = I.CEG_CLAIMS if co == "CEG" else I.VST_CLAIMS
    rows = []
    for a in assets:
        v = value_asset(a, deck, opts)
        rows.append({"asset": a["name"], "tech": a["tech"], "hub": a["hub"], "mw": a["mw"],
                     "pv_mm": v["pv"], "usd_per_kw": v["pv"] * 1e6 / (a["mw"] * 1000), "ebitda27_mm": v["ebitda27"]})
    gav = sum(r["pv_mm"] for r in rows) / 1000
    oh = corp_overhead_pv(co, opts.get("disc_adj", 0.0)) / 1000
    net_claims = sum(v for _, v in claims)
    eq = gav - oh - net_claims
    shares = I.MARKET[co]["shares_mm"] + I.EXTRA_SHARES_MM[co]
    plat = I.PLATFORM[co]["ebitda_mm"] * I.PLATFORM[co]["multiple"] / 1000
    by_tech = {}
    for r in rows:
        by_tech.setdefault(r["tech"], [0, 0])
        by_tech[r["tech"]][0] += r["mw"]
        by_tech[r["tech"]][1] += r["pv_mm"] / 1000
    return {"rows": rows, "gav": gav, "overhead": oh, "net_claims": net_claims, "equity": eq,
            "shares": shares, "nav_ps": eq / shares * 1000, "platform": plat,
            "nav_ps_plat": (eq + plat) / shares * 1000, "by_tech": by_tech,
            "mw": sum(r["mw"] for r in rows)}


def comps_lens(co, base):
    """GAV with gas marked at transaction $/kW; other assets at Base modelled value ($bn)."""
    assets = I.CEG_ASSETS if co == "CEG" else I.VST_ASSETS
    tot = 0.0
    for a, r in zip(assets, base["rows"]):
        if "Cogentrix" in a["name"]:
            tot += a["mw"] * I.COMP_MARK_COGENTRIX / 1e6
        elif a["tech"] == "ccgt":
            tot += a["mw"] * I.COMP_MARK_CCGT[a["hub"]] / 1e6
        elif a["tech"] == "peaker":
            tot += a["mw"] * I.COMP_MARK_PEAKER / 1e6
        else:
            tot += r["pv_mm"] / 1000
    return tot  # $bn (MW x $/kW / 1e6 = $bn)


def market_view(co):
    m = I.MARKET[co]
    shares = m["shares_mm"] + I.EXTRA_SHARES_MM[co]
    mcap = m["price"] * shares / 1000
    claims = I.CEG_CLAIMS if co == "CEG" else I.VST_CLAIMS
    net_claims = sum(v for _, v in claims)
    mw = sum(a["mw"] for a in (I.CEG_ASSETS if co == "CEG" else I.VST_ASSETS))
    ev = mcap + net_claims
    return {"price": m["price"], "shares": shares, "mcap": mcap, "net_claims": net_claims, "ev": ev,
            "mw": mw, "ev_per_kw": ev * 1e9 / (mw * 1000)}


def solve_shift(co, target_ps, platform=False, scen="Base", lo=-40.0, hi=150.0, param="shift"):
    f = lambda s: (company_nav(co, Deck(scen, **{param: s}))["nav_ps_plat" if platform else "nav_ps"] - target_ps)
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        fm = f(mid)
        if fm * flo > 0:
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def new_entrant_breakeven(capex_kw=2350, real_rate=0.08, life=25, hr=6.4, cf=0.60, cap_mwday=230.0):
    """PJM West ATC (2026$) needed for a new CCGT to earn `real_rate` (pre-tax-equivalent)."""
    crf = real_rate / (1 - (1 + real_rate) ** -life)
    fixed = capex_kw * crf + I.TECH["ccgt"]["fom_kw"] + I.TECH["ccgt"]["capex_kw"]
    capture = I.CCGT_CAPTURE["PJMW"]
    cap_rev = cap_mwday * 365 * I.ACCREDITATION["ccgt"] / 1000
    need_spark = (fixed - cap_rev) * 1000 / (8760 * cf)
    gas = I.HENRY_HUB_LR_REAL + I.GAS_BASIS["PJMW"] + I.FUEL_ADDER
    captured = need_spark + hr * gas + I.TECH["ccgt"]["vom"]
    return captured / capture


# ---------------------------------------------------------------------------
# Runner / reporting
# ---------------------------------------------------------------------------
def fmt(x, d=1):
    return f"{x:,.{d}f}"


def main():
    os.makedirs(OUT, exist_ok=True)
    md = []
    results = {co: {s: company_nav(co, Deck(s)) for s in I.SCENARIO_ORDER} for co in ("CEG", "VST")}
    mkt = {co: market_view(co) for co in ("CEG", "VST")}

    # 1. Scenario price deck
    md.append("### Scenario price deck (2026$, long-run = 2030+)\n")
    md.append("| Scenario | US DC TWh 2030 | DC share of US load 2030 | US DC TWh 2035 | PJM DC GW add'l by 2030 | PJM West ATC $/MWh | NI Hub ATC | ERCOT North ATC | PJM capacity $/MW-day |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for s in I.SCENARIO_ORDER:
        d = Deck(s)
        sc = I.SCENARIOS[s]
        us_2030 = I.US_TOTAL_LOAD_TWH_2024 * (1 + I.NON_DC_LOAD_GROWTH) ** 6 + sc["us_dc_twh_2030"] - 200
        md.append(f"| {s} | {sc['us_dc_twh_2030']} | {sc['us_dc_twh_2030']/us_2030:.0%} | {sc['us_dc_twh_2035']} | {sc['pjm_dc_gw_2030']} | "
                  f"{d.lr_atc_real('PJMW'):.0f} | {d.lr_atc_real('NIHUB'):.0f} | {d.lr_atc_real('ERCOT'):.0f} | {sc['pjm_cap']:.0f} |")
    md.append(f"\nForward-market reference (nominal, all scenarios 2027-28): PJM West ATC ~${I.FORWARD_ATC['PJMW'][2027]:.0f}/${I.FORWARD_ATC['PJMW'][2028]:.0f}, "
              f"ERCOT North ~${I.FORWARD_ATC['ERCOT'][2027]:.0f}/${I.FORWARD_ATC['ERCOT'][2028]:.0f}; PJM capacity CY27 ${I.PJM_CAPACITY_CY[2027]:.0f}, CY28 ${I.PJM_CAPACITY_CY[2028]:.0f}/MW-day.")
    md.append(f"New-entrant CCGT break-even PJM West ATC (2026$, $2,350/kW, 8% real, $230/MW-day capacity): **${new_entrant_breakeven():.0f}/MWh**; "
              f"at $2,000/kW: ${new_entrant_breakeven(capex_kw=2000):.0f}; at $2,800/kW: ${new_entrant_breakeven(capex_kw=2800):.0f}.\n")

    # 2. Asset-level NAV tables
    for co in ("CEG", "VST"):
        md.append(f"### {co} - asset-level NAV ($mm, after-tax PV) by scenario\n")
        md.append("| Asset | Tech | Hub | MW | Low | Base | High | Extreme | Base $/kW | 2027E asset EBITDA |")
        md.append("|---|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(results[co]["Base"]["rows"]):
            vals = [results[co][s]["rows"][i]["pv_mm"] for s in I.SCENARIO_ORDER]
            e27 = r["ebitda27_mm"]
            md.append(f"| {r['asset']} | {r['tech']} | {r['hub']} | {r['mw']:,} | " + " | ".join(fmt(v, 0) for v in vals)
                      + f" | {r['usd_per_kw']:,.0f} | {'' if e27 is None else fmt(e27, 0)} |")
        md.append("")
        md.append(f"#### {co} - NAV by technology ($bn)\n")
        md.append("| Technology | MW | Low | Base | High | Extreme | Base $/kW |")
        md.append("|---|---|---|---|---|---|---|")
        for t in results[co]["Base"]["by_tech"]:
            mw = results[co]["Base"]["by_tech"][t][0]
            vals = [results[co][s]["by_tech"][t][1] for s in I.SCENARIO_ORDER]
            md.append(f"| {t} | {mw:,} | " + " | ".join(fmt(v) for v in vals) + f" | {vals[1]*1e9/(mw*1000):,.0f} |")
        md.append("")

    # 3. NAV bridge + market comparison
    md.append("### NAV bridge and market comparison ($bn except per share)\n")
    for co in ("CEG", "VST"):
        m = mkt[co]
        md.append(f"#### {co} (price ${m['price']:.2f}, {m['shares']:.1f}mm shares pro forma)\n")
        md.append("| Line | Low | Base | High | Extreme |")
        md.append("|---|---|---|---|---|")
        R = results[co]
        line = lambda label, key, d=1: md.append(f"| {label} | " + " | ".join(fmt(R[s][key], d) for s in I.SCENARIO_ORDER) + " |")
        line("Gross asset value (generation)", "gav")
        line("Less: capitalised corporate overhead", "overhead")
        line("Less: net debt, preferred & other claims", "net_claims")
        line("**Equity NAV - generation only**", "equity")
        line("**NAV / share - generation only ($)**", "nav_ps", 0)
        md.append("| Premium(+)/discount(-) of price to NAV | " + " | ".join(f"{m['price']/R[s]['nav_ps']-1:+.0%}" if R[s]["nav_ps"] > 10 else "n.m." for s in I.SCENARIO_ORDER) + " |")
        line("Add: retail/commercial platform (earnings-based, see note)", "platform")
        line("**NAV / share incl. platform ($)**", "nav_ps_plat", 0)
        md.append("| Premium(+)/discount(-) of price to NAV incl. platform | " + " | ".join(f"{m['price']/R[s]['nav_ps_plat']-1:+.0%}" for s in I.SCENARIO_ORDER) + " |")
        md.append(f"| GAV per kW ($) | " + " | ".join(f"{R[s]['gav']*1e9/(R[s]['mw']*1000):,.0f}" for s in I.SCENARIO_ORDER) + " |")
        md.append("")
        md.append(f"Market: market cap ${m['mcap']:.1f}bn; net claims ${m['net_claims']:.1f}bn; **EV ${m['ev']:.1f}bn**; {m['mw']:,} MW pro forma -> **${m['ev_per_kw']:,.0f}/kW**.\n")

    # 4. Market-implied solve
    md.append("### What the market price implies (solve: uniform long-run power price shift vs Base deck)\n")
    md.append("| | Required LR price shift vs Base ($/MWh, 2026$) | Implied PJM West LR ATC | Implied ERCOT LR ATC | Implied PJM heat rate |")
    md.append("|---|---|---|---|---|")
    implied = {}
    for co in ("CEG", "VST"):
        for plat in (False, True):
            s = solve_shift(co, mkt[co]["price"], platform=plat)
            implied[(co, plat)] = s
            label = f"{co} - {'incl. platform' if plat else 'generation only'}"
            if s is None:
                md.append(f"| {label} | outside solver range | | | |")
                continue
            d = Deck("Base", shift=s)
            md.append(f"| {label} | {s:+.1f} | ${d.lr_atc_real('PJMW'):.0f} | ${d.lr_atc_real('ERCOT'):.0f} | "
                      f"{d.lr_atc_real('PJMW')/(I.HENRY_HUB_LR_REAL+I.GAS_BASIS['PJMW']):.1f} |")
    md.append("")
    md.append("Alternative solve - Henry Hub level (Base heat rates unchanged) needed to justify the price:\n")
    md.append("| | Required long-run Henry Hub (2026$/MMBtu) |")
    md.append("|---|---|")
    for co in ("CEG", "VST"):
        for plat in (False, True):
            g = solve_shift(co, mkt[co]["price"], platform=plat, lo=-2.0, hi=6.0, param="gas_shift")
            implied[(co, plat, "gas")] = g
            md.append(f"| {co} - {'incl. platform' if plat else 'generation only'} | "
                      + ("n/a" if g is None else f"${I.HENRY_HUB_LR_REAL + g:.2f} (vs ${I.HENRY_HUB_LR_REAL:.2f} Base)") + " |")
    md.append("")

    # 4b. Private-market lens, implied nuclear value, probability-weighted NAV
    md.append("### Private-market lens: gas marked at transaction $/kW (nuclear/hydro/other at Base)\n")
    md.append("| | Modelled GAV Base $bn | Comps-lens GAV $bn | Equity NAV $bn | NAV/share gen-only $ | NAV/share incl. platform $ | Price $ |")
    md.append("|---|---|---|---|---|---|---|")
    extra = {}
    for co in ("CEG", "VST"):
        B = results[co]["Base"]
        g = comps_lens(co, B)
        eq = g - B["overhead"] - B["net_claims"]
        extra[co] = {"comps_gav": g, "comps_nav_ps": eq / B["shares"] * 1000, "comps_nav_ps_plat": (eq + B["platform"]) / B["shares"] * 1000}
        md.append(f"| {co} | {B['gav']:.1f} | {g:.1f} | {eq:.1f} | {eq/B['shares']*1000:,.0f} | {(eq+B['platform'])/B['shares']*1000:,.0f} | {mkt[co]['price']:.2f} |")
    md.append("")
    md.append("### What the market is paying for the nuclear fleet\n")
    md.append("Implied nuclear value = market EV + capitalised overhead - platform value - non-nuclear assets (gas at transaction comps; hydro/geothermal/renewables/coal at Base).\n")
    md.append("| | Market EV $bn | Non-nuclear assets $bn | Implied nuclear value $bn | Nuclear MW | Implied $/kW | Model $/kW Low | Base | High | Extreme |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")
    for co in ("CEG", "VST"):
        B = results[co]["Base"]
        nuc_mw, nuc_base = B["by_tech"]["nuclear"]
        non_nuc = extra[co]["comps_gav"] - nuc_base
        implied_nuc = mkt[co]["ev"] + B["overhead"] - B["platform"] - non_nuc
        extra[co]["implied_nuc_kw"] = implied_nuc * 1e9 / (nuc_mw * 1000)
        per = [results[co][s]["by_tech"]["nuclear"][1] * 1e9 / (nuc_mw * 1000) for s in I.SCENARIO_ORDER]
        md.append(f"| {co} | {mkt[co]['ev']:.1f} | {non_nuc:.1f} | {implied_nuc:.1f} | {nuc_mw:,} | {extra[co]['implied_nuc_kw']:,.0f} | "
                  + " | ".join(f"{p:,.0f}" for p in per) + " |")
    md.append("")
    md.append("### Probability-weighted NAV (weights are an illustrative JUDGEMENT: " +
              ", ".join(f"{k} {v:.0%}" for k, v in I.SCENARIO_WEIGHTS.items()) + ")\n")
    md.append("| | Weighted NAV/share gen-only $ | incl. platform $ | Price $ | Price vs weighted NAV |")
    md.append("|---|---|---|---|---|")
    for co in ("CEG", "VST"):
        w = sum(I.SCENARIO_WEIGHTS[s] * results[co][s]["nav_ps"] for s in I.SCENARIO_ORDER)
        wp = sum(I.SCENARIO_WEIGHTS[s] * results[co][s]["nav_ps_plat"] for s in I.SCENARIO_ORDER)
        extra[co]["weighted"] = (w, wp)
        md.append(f"| {co} | {w:,.0f} | {wp:,.0f} | {mkt[co]['price']:.2f} | {mkt[co]['price']/wp-1:+.0%} (vs incl. platform) |")
    md.append("")

    # 5. Energy price x capacity price sensitivity
    shifts = [-20, -10, 0, 10, 20, 30, 40]
    caps = [100, 175, 230, 325, 450]
    sens_rows = []
    for co in ("CEG", "VST"):
        md.append(f"### {co} NAV/share sensitivity - long-run energy price shift (rows, $/MWh vs Base) x PJM capacity price (cols, $/MW-day) - generation only\n")
        md.append("| Shift \\ Cap | " + " | ".join(str(c) for c in caps) + " | PJM West ATC |")
        md.append("|---|" + "---|" * (len(caps) + 1))
        for sh in shifts:
            vals = []
            for c in caps:
                n = company_nav(co, Deck("Base", shift=sh, pjm_cap=c))["nav_ps"]
                vals.append(n)
                sens_rows.append({"company": co, "price_shift": sh, "pjm_cap": c, "nav_ps": round(n, 2)})
            md.append(f"| {sh:+d} | " + " | ".join(fmt(v, 0) for v in vals) + f" | ${Deck('Base', shift=sh).lr_atc_real('PJMW'):.0f} |")
        md.append(f"\nCurrent price: ${mkt[co]['price']:.2f}\n")

    # 6. Other sensitivities (Base)
    md.append("### Other sensitivities (Base deck, NAV/share generation only, $)\n")
    md.append("| Sensitivity | CEG | VST |")
    md.append("|---|---|---|")
    other = [
        ("Base case", {}, {}),
        ("Discount rates -1.0pt", {}, {"disc_adj": -0.01}),
        ("Discount rates +1.0pt", {}, {"disc_adj": 0.01}),
        ("Nuclear life ends 2045 (no subsequent license renewals)", {}, {"nuc_end": 2045}),
        ("Nuclear life extended to 2065", {}, {"nuc_end": 2065}),
        ("Henry Hub -$1.00 (power follows via heat rate)", {"gas_shift": -1.0}, {}),
        ("Henry Hub +$1.00", {"gas_shift": 1.0}, {}),
        ("Data-center PPA prices -$10/MWh", {}, {"ppa_adj": -10.0}),
        ("Data-center PPA prices +$10/MWh", {}, {"ppa_adj": 10.0}),
        ("Low scenario (with 45U floor)", {"scen": "Low"}, {}),
        ("Low scenario, no 45U nuclear PTC floor", {"scen": "Low"}, {"no_45u": True}),
        ("PJM capacity cap persists at $325 forever (High energy, capped capacity)", {"scen": "High", "pjm_cap": 325.0}, {}),
    ]
    other_rows = []
    for label, dk, op in other:
        dk = dict(dk)
        scen = dk.pop("scen", "Base")
        v = [company_nav(co, Deck(scen, **dk), op)["nav_ps"] for co in ("CEG", "VST")]
        other_rows.append({"sensitivity": label, "CEG": round(v[0], 2), "VST": round(v[1], 2)})
        md.append(f"| {label} | {v[0]:,.0f} | {v[1]:,.0f} |")
    md.append("")

    # 7. Comps
    md.append("### Transaction comparables ($/kW) vs model\n")
    md.append("| Comparable | $/kW |")
    md.append("|---|---|")
    for n, v, _ in I.COMPS:
        md.append(f"| {n} | {v:,.0f} |")
    for co in ("CEG", "VST"):
        bt = results[co]["Base"]["by_tech"]
        g_mw = bt["ccgt"][0] + bt["peaker"][0]
        g_v = bt["ccgt"][1] + bt["peaker"][1]
        md.append(f"| Model: {co} gas fleet (CCGT+peakers), Base | {g_v*1e9/(g_mw*1000):,.0f} |")
        md.append(f"| Model: {co} nuclear fleet, Base | {bt['nuclear'][1]*1e9/(bt['nuclear'][0]*1000):,.0f} |")
    md.append("")

    with open(os.path.join(OUT, "tables.md"), "w") as f:
        f.write("\n".join(md))

    # CSV outputs
    with open(os.path.join(OUT, "asset_nav_by_scenario.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company", "asset", "tech", "hub", "mw"] + [f"pv_mm_{s}" for s in I.SCENARIO_ORDER] + ["base_usd_per_kw"])
        for co in ("CEG", "VST"):
            for i, r in enumerate(results[co]["Base"]["rows"]):
                w.writerow([co, r["asset"], r["tech"], r["hub"], r["mw"]] +
                           [round(results[co][s]["rows"][i]["pv_mm"], 1) for s in I.SCENARIO_ORDER] + [round(r["usd_per_kw"])])
    with open(os.path.join(OUT, "nav_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company", "scenario", "gav_bn", "overhead_bn", "net_claims_bn", "equity_nav_bn", "nav_ps", "nav_ps_incl_platform",
                    "price", "market_cap_bn", "ev_bn"])
        for co in ("CEG", "VST"):
            for s in I.SCENARIO_ORDER:
                R = results[co][s]
                w.writerow([co, s, round(R["gav"], 2), round(R["overhead"], 2), round(R["net_claims"], 2), round(R["equity"], 2),
                            round(R["nav_ps"], 2), round(R["nav_ps_plat"], 2), mkt[co]["price"], round(mkt[co]["mcap"], 2), round(mkt[co]["ev"], 2)])
    with open(os.path.join(OUT, "sensitivity_price_x_capacity.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["company", "price_shift", "pjm_cap", "nav_ps"])
        w.writeheader()
        w.writerows(sens_rows)

    write_xlsx(results, mkt, sens_rows, other_rows, implied, shifts, caps)

    # console summary
    for co in ("CEG", "VST"):
        m = mkt[co]
        print(f"\n{co}: price ${m['price']:.2f} | mcap ${m['mcap']:.1f}bn | EV ${m['ev']:.1f}bn | ${m['ev_per_kw']:,.0f}/kW")
        for s in I.SCENARIO_ORDER:
            R = results[co][s]
            print(f"  {s:8s} GAV ${R['gav']:6.1f}bn  equity ${R['equity']:6.1f}bn  NAV/sh ${R['nav_ps']:7.0f}  incl platform ${R['nav_ps_plat']:7.0f}")
        print(f"  implied shift gen-only {implied[(co, False)]:.1f}, incl platform {implied[(co, True)]:.1f}")


def write_xlsx(results, mkt, sens_rows, other_rows, implied, shifts, caps):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
    except ImportError:
        print("openpyxl not installed - skipping xlsx")
        return
    wb = Workbook()
    bold = Font(bold=True)
    hdr = PatternFill("solid", fgColor="DDE6F0")

    def sheet(title, header, rows):
        ws = wb.create_sheet(title)
        ws.append(header)
        for c in ws[1]:
            c.font, c.fill = bold, hdr
        for r in rows:
            ws.append(r)
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = max(12, min(70, max(len(str(c.value or "")) for c in col) + 2))
        return ws

    wb.remove(wb.active)
    rows = []
    for co in ("CEG", "VST"):
        m = mkt[co]
        for s in I.SCENARIO_ORDER:
            R = results[co][s]
            rows.append([co, s, round(R["gav"], 2), round(R["overhead"], 2), round(R["net_claims"], 2), round(R["equity"], 2),
                         round(R["nav_ps"], 1), round(R["platform"], 2), round(R["nav_ps_plat"], 1), m["price"],
                         round(m["price"] / R["nav_ps"] - 1, 3) if R["nav_ps"] > 0 else None, round(m["mcap"], 1), round(m["ev"], 1),
                         round(m["ev_per_kw"]), round(R["gav"] * 1e9 / (R["mw"] * 1000))])
    sheet("Summary", ["Company", "Scenario", "GAV $bn", "Overhead $bn", "Net claims $bn", "Equity NAV $bn", "NAV/share $",
                      "Platform $bn", "NAV/share incl platform $", "Share price $", "Price/NAV - 1", "Mkt cap $bn", "EV $bn",
                      "EV $/kW", "GAV $/kW"], rows)
    rows = []
    for co in ("CEG", "VST"):
        for i, r in enumerate(results[co]["Base"]["rows"]):
            rows.append([co, r["asset"], r["tech"], r["hub"], r["mw"]] +
                        [round(results[co][s]["rows"][i]["pv_mm"], 0) for s in I.SCENARIO_ORDER] + [round(r["usd_per_kw"])])
    sheet("Asset NAV", ["Company", "Asset", "Tech", "Hub", "MW"] + [f"PV $mm {s}" for s in I.SCENARIO_ORDER] + ["Base $/kW"], rows)
    rows = []
    for s in I.SCENARIO_ORDER:
        d = Deck(s)
        sc = I.SCENARIOS[s]
        rows.append([s, sc["desc"], sc["us_dc_twh_2030"], sc["us_dc_twh_2035"], sc["pjm_dc_gw_2030"], sc["ihr_pjm"], sc["ihr_ercot"],
                     round(d.lr_atc_real("PJMW"), 1), round(d.lr_atc_real("NIHUB"), 1), round(d.lr_atc_real("ERCOT"), 1),
                     sc["pjm_cap"], sc["other_cap"], sc["west_cap"], sc["scarcity_mult"]])
    sheet("Scenarios", ["Scenario", "Description", "US DC TWh 2030", "US DC TWh 2035", "PJM DC GW 2030", "PJM IHR", "ERCOT IHR",
                        "PJM West ATC (2026$)", "NI Hub ATC", "ERCOT ATC", "PJM cap $/MW-d", "NY/NE/MISO cap", "West RA cap",
                        "Peaker scarcity mult"], rows)
    for co in ("CEG", "VST"):
        grid = [[sh] + [next(r["nav_ps"] for r in sens_rows if r["company"] == co and r["price_shift"] == sh and r["pjm_cap"] == c) for c in caps]
                for sh in shifts]
        sheet(f"Sens {co}", ["LR price shift $/MWh \\ PJM cap $/MW-day"] + caps, grid)
    sheet("Other sens", ["Sensitivity", "CEG NAV/sh", "VST NAV/sh"], [[r["sensitivity"], r["CEG"], r["VST"]] for r in other_rows])
    sheet("Market implied", ["Case", "LR price shift vs Base ($/MWh)"],
          [[f"{co} {'incl platform' if p else 'gen only'}", None if implied[(co, p)] is None else round(implied[(co, p)], 1)]
           for co in ("CEG", "VST") for p in (False, True)]
          + [[f"{co} {'incl platform' if p else 'gen only'} - required LR Henry Hub $/MMBtu",
              None if implied.get((co, p, "gas")) is None else round(I.HENRY_HUB_LR_REAL + implied[(co, p, "gas")], 2)]
             for co in ("CEG", "VST") for p in (False, True)])
    claims = [["CEG", n, v] for n, v in I.CEG_CLAIMS] + [["VST", n, v] for n, v in I.VST_CLAIMS]
    sheet("Claims", ["Company", "Item", "$bn"], claims)
    assets = [[co, a["name"], a["tech"], a["hub"], a["mw"], a.get("start"), a.get("end"),
               "; ".join(f"{c['price']}$/MWh {c['start']}-{c['end']}" for c in a.get("contracts", []))]
              for co, lst in (("CEG", I.CEG_ASSETS), ("VST", I.VST_ASSETS)) for a in lst]
    sheet("Asset register", ["Company", "Asset", "Tech", "Hub", "MW", "Start", "End", "Contracts (EST prices)"], assets)
    wb.save(os.path.join(OUT, "nav_model.xlsx"))


if __name__ == "__main__":
    main()
