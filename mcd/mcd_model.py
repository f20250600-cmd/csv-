"""
McDonald's (MCD) path-exploration model.

Purpose: value MCD under several explicitly-stated operating paths, show what the
current price implies, and decompose where per-share value creation comes from
(business growth vs. NEXT items vs. leverage/buybacks).

Everything is in $ billions unless noted; per-share values in $.
Pure Python (no numpy) so it runs anywhere:  python3 mcd/mcd_model.py

The 2026E starting point is anchored on reported H1-2026 results and 2026
guidance; 2027-2031 are driver-based projections. Items marked [EST] are my
estimates where the company has not disclosed the number (e.g. the year-by-year
rent-relief schedule; management disclosed only cumulative amounts).
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field, replace

# ---------------------------------------------------------------------------
# Market / balance-sheet inputs (as of ~Sep 25-26, 2026)
# ---------------------------------------------------------------------------
PRICE = 236.50          # MCD close ~Sep 25/26 2026 (Morningstar / Yahoo quotes)
SHARES0 = 713.0         # diluted shares, M (~711M basic at Q2-26)
NET_DEBT0 = 39.1        # $39.9B debt - $0.8B cash at Q2-26 (financial debt only)
DPS_RATE0 = 7.72        # annualized dividend after Sep-2026 4% raise ($1.93/qtr)
TEN_YEAR = 0.0517       # UST 10y close Sep 25 2026

# ---------------------------------------------------------------------------
# 2026E anchor (derived from Q1+Q2 2026 actuals and FY26 guidance)
# ---------------------------------------------------------------------------
SWS_2026 = 148.0        # systemwide sales: Q1 ~$34B + Q2 $37B + H2 ~$77B
OI_2026 = 13.20         # adj. operating income (mid/high-40s% margin on ~$28.3B rev)
REV_2026 = 28.3         # consolidated revenue
FRAN_REV_2026 = 17.6    # franchised revenues (rent + royalties + fees)
COOP_SALES_2026 = 9.8   # company-operated sales (~5% of units)
OTHER_REV_2026 = 0.9    # tech fees, brand licensing, etc.
DA_2026 = 2.35
CAPEX_2026 = 3.8        # guidance $3.7-3.9B
INTEREST_2026 = 1.62    # guidance: +4-6% y/y
NONOP_2026 = 0.06       # small nonoperating income (calibrates to EPS)
TAX = 0.215             # guidance 21-23% -> use 21.5%
OTHER_FCF_DRAG = 0.30   # SBC / working capital / other (calibrates FCF to ~$7.4B)

LEVERAGE = NET_DEBT0 / (OI_2026 + DA_2026)   # hold net debt/EBITDA constant (~2.5x)
RATE_2026 = INTEREST_2026 / NET_DEBT0        # avg cost on net debt (~4.1%)
RATE_STEP = 0.0012      # +12bp/yr: maturing ~3-4% coupons refinanced near ~5.5-6%

YEARS = [2027, 2028, 2029, 2030, 2031, 2032]   # 2032 = normalization year for terminal

# NEXT items (management: ~$5B support through 2030 of which ~60-70% rent relief,
# $1.5-2B cumulative capital support 2027-30, $8.5B through 2036).
# [EST] ~= $3.25B thru 2030, back-loaded (BMO: plan cuts EPS ~1% in 27-28, 2-3% by 2030;
# JPM: rent relief may exceed G&A savings in 2028-30)
RENT_RELIEF_PLAN = {2027: 0.30, 2028: 0.70, 2029: 1.00, 2030: 1.25, 2031: 0.90}
CAP_SUPPORT = {2027: 0.44, 2028: 0.44, 2029: 0.44, 2030: 0.44, 2031: 0.20, 2032: 0.0}
BASE_CAPEX_2027 = 3.0   # management: ~ $3B/yr baseline 2027-2030
GNA_RATIO = {2026: 0.022, 2027: 0.02125, 2028: 0.0205, 2029: 0.01975, 2030: 0.019, 2031: 0.019, 2032: 0.019}

# Refranchising 95% -> 98% by end-2028 [EST effects]
REFR_OI = {2027: -0.10, 2028: -0.18}          # lost co-op margin > new rent/royalty
REFR_PROCEEDS = {2027: 0.8, 2028: 0.8}        # sale proceeds (return to holders)
COOP_SHRINK = {2027: 0.75, 2028: 0.62}        # co-op sales multiplier from refranchising
REFR_FRAN_TAKE = 0.17                          # rent+royalty on refranchised sales (US/IOM)

PAYOUT_FLOOR = 0.60     # dividend rate >= 60% of EPS (target range 50-60%)
DIV_MIN_GROWTH = 0.02   # 50-year streak: assume rate never grows < 2%

# Operating-income sensitivities (calibrated to 2024-25: see write-up)
K_COMP = 1.30           # %chg OI per 1% global comp (rent/royalty on top line, fixed occupancy)
K_UNIT = 0.90           # %chg OI per 1% SWS from new units (DL-heavy mix -> lower take)
FRAN_UNIT_TAKE = 0.75   # franchised revenue grows slower than SWS from units (DL royalty ~4-5%)


@dataclass
class Scenario:
    name: str
    comps: dict                  # year -> global comparable sales growth
    units: dict                  # year -> contribution of net new units to SWS growth
    cost_drag: float             # structural annual drag on OI growth (co-op inflation, tech, D&A)
    gna_achieved: float          # share of the 2.2% -> 1.9% G&A target actually achieved
    rent_factor: float           # scale on the rent-relief schedule
    rent_longrun: float          # $B/yr of rent relief that persists into the terminal year
    g_terminal: float            # perpetual nominal growth after 2032
    exit_pe: float               # forward P/E used for the IRR view
    note: str = ""


def flat(v, years=YEARS):
    return {y: v for y in years}


MGMT_UNITS = {2027: 0.025, 2028: 0.025, 2029: 0.0225, 2030: 0.020, 2031: 0.020, 2032: 0.020}

SCENARIOS = [
    Scenario(
        "A. Value problem persists",
        comps={2027: 0.005, 2028: 0.010, 2029: 0.015, 2030: 0.015, 2031: 0.015, 2032: 0.015},
        units={2027: 0.020, 2028: 0.020, 2029: 0.0175, 2030: 0.015, 2031: 0.015, 2032: 0.015},
        cost_drag=-0.010, gna_achieved=0.33, rent_factor=1.25, rent_longrun=0.90,
        g_terminal=0.020, exit_pe=15.0,
        note="Traffic keeps falling, discounting without payback, franchisees need more help, "
             "slower openings; rent relief becomes a permanent take-rate cut."),
    Scenario(
        "B. Mature floor",
        comps=flat(0.020),
        units={2027: 0.0225, 2028: 0.0225, 2029: 0.020, 2030: 0.0175, 2031: 0.0175, 2032: 0.0175},
        cost_drag=-0.0075, gna_achieved=0.50, rent_factor=1.00, rent_longrun=0.70,
        g_terminal=0.025, exit_pe=16.5,
        note="Flat traffic, ~2% price, unit plan slightly haircut, half the G&A savings, "
             "most rent relief sticks. No NEXT payoff."),
    Scenario(
        "C. Units carry it, comps modest",
        comps=flat(0.020), units=MGMT_UNITS,
        cost_drag=-0.0075, gna_achieved=1.00, rent_factor=1.00, rent_longrun=0.40,
        g_terminal=0.030, exit_pe=17.5,
        note="Management's unit plan and G&A plan delivered, but comps stay ~2%."),
    Scenario(
        "D. NEXT works (mgmt plan)",
        comps=flat(0.030), units=MGMT_UNITS,
        cost_drag=-0.005, gna_achieved=1.00, rent_factor=1.00, rent_longrun=0.30,
        g_terminal=0.030, exit_pe=19.0,
        note="Traffic turns modestly positive (+0.5-1%) on top of ~2-2.5% check; "
             "efficiency eases cost drag; relief fades after the remodel wave."),
    Scenario(
        "E. NEXT + value leadership restored",
        comps={2027: 0.035, 2028: 0.040, 2029: 0.040, 2030: 0.040, 2031: 0.035, 2032: 0.035},
        units={y: v + 0.0025 for y, v in MGMT_UNITS.items()},
        cost_drag=-0.005, gna_achieved=1.00, rent_factor=1.00, rent_longrun=0.20,
        g_terminal=0.0325, exit_pe=21.0,
        note="Share gains in chicken/beverage, traffic +1.5-2%, healthier franchisees open more."),
]


@dataclass
class YearRow:
    year: int
    sws: float
    oi_core: float
    gna_sav: float
    rent: float
    refr: float
    oi: float
    rev: float
    op_margin: float
    take_rate: float
    ebitda: float
    net_debt: float
    interest: float
    ni: float
    capex: float
    fcf: float
    fcfe: float
    div_paid: float
    buyback: float
    shares_end: float
    shares_avg: float
    eps: float
    dps_paid: float


def project(s: Scenario, buyback_pe: float | None = None, price0: float = PRICE):
    """Project 2026E-2032E. Buybacks executed at buyback_pe x EPS (default: today's P/E)."""
    eps_2026 = (OI_2026 - INTEREST_2026 + NONOP_2026) * (1 - TAX) * 1000 / SHARES0
    if buyback_pe is None:
        buyback_pe = price0 / eps_2026

    sws, oi_core = SWS_2026, OI_2026
    fran_rev, coop, other = FRAN_REV_2026, COOP_SALES_2026, OTHER_REV_2026
    da, nd = DA_2026, NET_DEBT0
    shares = SHARES0
    rate = RATE_2026
    div_rate_prev = DPS_RATE0
    base_capex = BASE_CAPEX_2027
    other_drag = OTHER_FCF_DRAG
    eps_prev = eps_2026
    rows = []

    ni_2026 = (OI_2026 - INTEREST_2026 + NONOP_2026) * (1 - TAX)
    rows.append(dict(year=2026, sws=SWS_2026, oi=OI_2026, rev=REV_2026, eps=eps_2026,
                     ni=ni_2026, fcf=ni_2026 + DA_2026 - CAPEX_2026 - OTHER_FCF_DRAG,
                     net_debt=NET_DEBT0, shares_avg=SHARES0, op_margin=OI_2026 / REV_2026,
                     take_rate=OI_2026 / SWS_2026))

    for y in YEARS:
        c, u = s.comps[y], s.units[y]
        sws_prev = sws
        sws = sws * (1 + c + u)
        oi_core = oi_core * (1 + K_COMP * c + K_UNIT * u + s.cost_drag)

        # G&A savings vs. holding G&A at 2.2% of SWS
        gna_sav = (GNA_RATIO[2026] - GNA_RATIO[y]) * sws * s.gna_achieved
        # rent relief: plan schedule through 2031, long-run level in the 2032 normalization year
        rent = RENT_RELIEF_PLAN.get(y, s.rent_longrun) * s.rent_factor if y <= 2031 else s.rent_longrun
        refr = REFR_OI.get(y, -0.18 * sws / SWS_2026) if y >= 2027 else 0.0
        oi = oi_core + gna_sav - rent + refr

        # revenue build (for margin % only; valuation uses OI dollars)
        coop_prev = coop
        coop = coop * (1 + c + 0.5 * u) * COOP_SHRINK.get(y, 1.0)
        refranchised_sales = coop_prev * (1 + c + 0.5 * u) - coop if y in COOP_SHRINK else 0.0
        fran_rev = fran_rev * (1 + c + FRAN_UNIT_TAKE * u) + refranchised_sales * REFR_FRAN_TAKE
        other = other * (1 + c + u)
        rev = fran_rev - rent + coop + other

        da = da * 1.04
        ebitda = oi + da
        nd_prev = nd
        nd = LEVERAGE * ebitda
        rate = rate + RATE_STEP if y <= 2031 else rate
        interest = rate * (nd_prev + nd) / 2
        ni = (oi - interest + NONOP_2026) * (1 - TAX)

        if y >= 2028:
            base_capex *= 1.03
        capex = base_capex + CAP_SUPPORT[y]
        other_drag *= 1.03
        fcf = ni + da - capex - other_drag
        fcfe = fcf + (nd - nd_prev) + REFR_PROCEEDS.get(y, 0.0)

        # dividends + buybacks; iterate to resolve EPS <-> share count
        shares_begin = shares
        eps = ni * 1000 / shares_begin
        for _ in range(4):
            div_rate = max(div_rate_prev * (1 + DIV_MIN_GROWTH), PAYOUT_FLOOR * eps)
            dps_paid = 0.75 * div_rate_prev + 0.25 * div_rate
            div_paid = dps_paid * shares_begin / 1000
            buyback = fcfe - div_paid
            bb_price = buyback_pe * eps
            shares_end = shares_begin - buyback * 1000 / bb_price
            shares_avg = (shares_begin + shares_end) / 2
            eps = ni * 1000 / shares_avg
        shares = shares_end
        div_rate_prev = div_rate

        rows.append(dict(year=y, sws=sws, oi_core=oi_core, gna_sav=gna_sav, rent=rent, refr=refr,
                         oi=oi, rev=rev, op_margin=oi / rev, take_rate=oi / sws, ebitda=ebitda,
                         net_debt=nd, interest=interest, ni=ni, capex=capex, fcf=fcf, fcfe=fcfe,
                         div_paid=div_paid, buyback=buyback, shares_end=shares_end,
                         shares_avg=shares_avg, eps=eps, dps_paid=dps_paid, div_rate=div_rate))
        eps_prev = eps
    return rows


# ---------------------------------------------------------------------------
# Valuation
# ---------------------------------------------------------------------------
T0 = 2026.75   # valuation date ~ Oct 1 2026


def dcf_value(s: Scenario, r: float, rows=None):
    """Equity DCF on FCFE (FCF + net borrowing at constant leverage + refranchising proceeds).
    Divided by today's share count: buybacks at fair value don't change per-share value."""
    rows = rows or project(s)
    r26 = rows[0]
    pv = 0.25 * (r26["fcf"] + 0.02 * NET_DEBT0 / 4) / (1 + r) ** 0.125   # Q4-2026 cash
    for row in rows[1:]:
        if row["year"] > 2031:
            break
        t = row["year"] + 0.5 - T0
        pv += row["fcfe"] / (1 + r) ** t
    # terminal: normalized 2032 FCFE with borrowing at g_T (not at the 2032 EBITDA jump)
    r32, r31 = rows[-1], rows[-2]
    fcfe_32 = r32["fcf"] + s.g_terminal * r31["net_debt"]
    tv = fcfe_32 / (r - s.g_terminal)
    pv_tv = tv / (1 + r) ** (2032 - T0)
    equity = pv + pv_tv
    return dict(value_ps=equity * 1000 / SHARES0, pv_explicit=pv, pv_tv=pv_tv,
                tv_share=pv_tv / equity, implied_exit_pe=(tv * 1000 / r31["shares_end"]) / r32["eps"])


def irr_at_price(s: Scenario, price: float = PRICE, exit_pe: float | None = None, rows=None):
    """Per-share IRR: buy today, collect dividends, sell end-2031 at exit_pe x 2032E EPS."""
    rows = rows or project(s)
    exit_pe = exit_pe if exit_pe is not None else s.exit_pe
    flows = [(0.21, 1.93)]                          # Dec-15-2026 dividend
    for row in rows[1:]:
        if row["year"] <= 2031:
            flows.append((row["year"] + 0.5 - T0, row["dps_paid"]))
    flows.append((2032 - T0, exit_pe * rows[-1]["eps"]))

    def npv(rate):
        return -price + sum(cf / (1 + rate) ** t for t, cf in flows)

    lo, hi = -0.5, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def eps_cagr(rows, y0=2026, y1=2031):
    e0 = next(r["eps"] for r in rows if r["year"] == y0)
    e1 = next(r["eps"] for r in rows if r["year"] == y1)
    return (e1 / e0) ** (1 / (y1 - y0)) - 1


def decompose(s: Scenario):
    """Split 2026->2031 EPS growth (annualized, log-additive) into sources."""
    rows = project(s)
    a, b = rows[0], next(r for r in rows if r["year"] == 2031)
    n = 5
    # counterfactuals for OI pieces
    oi_core_31 = b["oi_core"]
    g_core = math.log(oi_core_31 / a["oi"]) / n
    g_next = math.log((oi_core_31 + b["gna_sav"] - b["rent"]) / oi_core_31) / n
    g_refr = math.log(b["oi"] / (oi_core_31 + b["gna_sav"] - b["rent"])) / n
    pretax_a = a["oi"] - INTEREST_2026 + NONOP_2026
    pretax_b = b["ni"] / (1 - TAX)
    g_interest = math.log((pretax_b / b["oi"]) / (pretax_a / a["oi"])) / n
    g_shares = math.log(a["shares_avg"] / b["shares_avg"]) / n
    total = math.log(b["eps"] / a["eps"]) / n
    # split share shrink by funding source (cumulative 2027-31)
    yrs = [r for r in rows[1:] if r["year"] <= 2031]
    fcf_after_div = sum(r["fcf"] - r["div_paid"] for r in yrs)
    debt_funded = sum(r["net_debt"] for r in yrs[-1:]) - NET_DEBT0
    proceeds = sum(REFR_PROCEEDS.values())
    bb_total = sum(r["buyback"] for r in yrs)
    return dict(core=g_core, next_items=g_next, refranchising=g_refr, interest=g_interest,
                buybacks=g_shares, total=total,
                bb_from_fcf=fcf_after_div / bb_total if bb_total else 0,
                bb_from_debt=debt_funded / bb_total if bb_total else 0,
                bb_from_proceeds=proceeds / bb_total if bb_total else 0)


def solve_comps_for_price(template: Scenario, r: float, price: float = PRICE):
    """Constant global comp (2027-2032) that makes DCF value == price."""
    lo, hi = -0.03, 0.08
    for _ in range(80):
        mid = (lo + hi) / 2
        s = replace(template, comps=flat(mid))
        if dcf_value(s, r)["value_ps"] < price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def solve_gT_for_price(template: Scenario, r: float, price: float = PRICE):
    lo, hi = -0.02, r - 0.005
    for _ in range(80):
        mid = (lo + hi) / 2
        if dcf_value(replace(template, g_terminal=mid), r)["value_ps"] < price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def pct(x, d=1):
    return f"{x * 100:.{d}f}%"


def main():
    out = []
    p = out.append
    eps26 = project(SCENARIOS[1])[0]["eps"]
    fcf26 = project(SCENARIOS[1])[0]["fcf"]
    mcap = PRICE * SHARES0 / 1000
    p("# MCD model output\n")
    p(f"Price ${PRICE:.2f} | diluted shares {SHARES0:.0f}M | mkt cap ${mcap:.0f}B | "
      f"net debt ${NET_DEBT0:.1f}B | EV ${mcap + NET_DEBT0:.0f}B")
    p(f"2026E: SWS ${SWS_2026:.0f}B, OI ${OI_2026:.1f}B (take {pct(OI_2026 / SWS_2026, 2)} of SWS), "
      f"EPS ${eps26:.2f}, FCF ${fcf26:.2f}B")
    p(f"P/E 2026E {PRICE / eps26:.1f}x | FCF yield {pct(fcf26 / mcap)} | dividend yield "
      f"{pct(DPS_RATE0 / PRICE, 2)} | earnings yield {pct(eps26 / PRICE, 2)} vs 10y UST {pct(TEN_YEAR, 2)}")
    p(f"EV/EBITDA 2026E {(mcap + NET_DEBT0) / (OI_2026 + DA_2026):.1f}x | "
      f"net debt/EBITDA {LEVERAGE:.2f}x\n")

    # --- scenario summary
    p("## Scenario summary (r = 8.5% unless stated)\n")
    p("| Scenario | Comps | SWS CAGR 26-31 | OI CAGR 26-31 | EPS 2027 | EPS 2031 | EPS CAGR | "
      "Adj. op margin 2030 | OI/SWS 2031 | DCF @8% | DCF @8.5% | DCF @9% | Implied exit P/E | "
      "IRR @ $236.50 (exit P/E) |")
    p("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for s in SCENARIOS:
        rows = project(s)
        r26, r27 = rows[0], rows[1]
        r30 = next(r for r in rows if r["year"] == 2030)
        r31 = next(r for r in rows if r["year"] == 2031)
        sws_cagr = (r31["sws"] / r26["sws"]) ** 0.2 - 1
        oi_cagr = (r31["oi"] / r26["oi"]) ** 0.2 - 1
        v8, v85, v9 = (dcf_value(s, r)["value_ps"] for r in (0.08, 0.085, 0.09))
        ipe = dcf_value(s, 0.085)["implied_exit_pe"]
        comps_desc = f"{pct(min(s.comps.values()))}-{pct(max(s.comps.values()))}" \
            if min(s.comps.values()) != max(s.comps.values()) else pct(s.comps[2027])
        p(f"| {s.name} | {comps_desc} | {pct(sws_cagr)} | {pct(oi_cagr)} | ${r27['eps']:.2f} | "
          f"${r31['eps']:.2f} | {pct(eps_cagr(rows))} | {pct(r30['op_margin'])} | "
          f"{pct(r31['take_rate'], 2)} | ${v8:.0f} | ${v85:.0f} | ${v9:.0f} | {ipe:.1f}x | "
          f"{pct(irr_at_price(s))} ({s.exit_pe:.1f}x) |")
    p("")

    # --- EPS decomposition
    p("## Where per-share growth comes from (annualized, 2026E->2031E, log-additive)\n")
    p("| Scenario | Core business (comps+units-drag) | NEXT items (G&A saves - rent relief) | "
      "Refranchising | Interest drag | Buybacks | = EPS growth | Buybacks funded by FCF / new debt / "
      "refranchise proceeds |")
    p("|---|---|---|---|---|---|---|---|")
    for s in SCENARIOS:
        d = decompose(s)
        p(f"| {s.name} | {pct(d['core'])} | {pct(d['next_items'])} | {pct(d['refranchising'])} | "
          f"{pct(d['interest'])} | {pct(d['buybacks'])} | {pct(d['total'])} | "
          f"{pct(d['bb_from_fcf'], 0)} / {pct(d['bb_from_debt'], 0)} / {pct(d['bb_from_proceeds'], 0)} |")
    p("")

    # --- IRR grid vs exit multiple
    p("## IRR at $236.50 by exit forward P/E (end-2031)\n")
    pes = [14, 16, 18, 20, 22]
    p("| Scenario | " + " | ".join(f"{x}x" for x in pes) + " |")
    p("|---|" + "---|" * len(pes))
    for s in SCENARIOS:
        p(f"| {s.name} | " + " | ".join(pct(irr_at_price(s, exit_pe=x)) for x in pes) + " |")
    p("")

    # --- what's priced in
    p("## What the current price implies\n")
    for r in (0.08, 0.085, 0.09):
        c_units = solve_comps_for_price(SCENARIOS[2], r)
        c_floor = solve_comps_for_price(SCENARIOS[1], r)
        g_floor = solve_gT_for_price(SCENARIOS[1], r)
        p(f"- r = {pct(r)}: constant comps needed = {pct(c_units, 2)} with management's unit & G&A plan "
          f"(template C), or {pct(c_floor, 2)} on the floor template (B). Floor template needs "
          f"terminal growth {pct(g_floor, 2)}.")
    p("")

    # --- sensitivities around the floor
    p("## Sensitivities (template B = Mature floor, r = 8.5%)\n")
    base = dcf_value(SCENARIOS[1], 0.085)["value_ps"]
    tests = [
        ("+1pt comps every year", replace(SCENARIOS[1], comps=flat(0.03))),
        ("-1pt comps every year", replace(SCENARIOS[1], comps=flat(0.01))),
        ("+0.5pt unit contribution", replace(SCENARIOS[1], units={y: v + 0.005 for y, v in SCENARIOS[1].units.items()})),
        ("rent relief fades to $0 long-run", replace(SCENARIOS[1], rent_longrun=0.0)),
        ("rent relief 1.5x plan, $1.2B permanent", replace(SCENARIOS[1], rent_factor=1.5, rent_longrun=1.2)),
        ("full G&A savings", replace(SCENARIOS[1], gna_achieved=1.0)),
        ("no cost drag", replace(SCENARIOS[1], cost_drag=0.0)),
        ("terminal growth 3.0% (vs 2.5%)", replace(SCENARIOS[1], g_terminal=0.03)),
        ("terminal growth 2.0%", replace(SCENARIOS[1], g_terminal=0.02)),
    ]
    p(f"Floor value @8.5%: ${base:.0f}\n")
    p("| Change | Value/share | Delta |")
    p("|---|---|---|")
    for label, s in tests:
        v = dcf_value(s, 0.085)["value_ps"]
        p(f"| {label} | ${v:.0f} | {v - base:+.0f} ({(v / base - 1) * 100:+.0f}%) |")
    for r in (0.075, 0.08, 0.09, 0.095):
        v = dcf_value(SCENARIOS[1], r)["value_ps"]
        p(f"| discount rate {pct(r)} | ${v:.0f} | {v - base:+.0f} ({(v / base - 1) * 100:+.0f}%) |")
    p("")

    # --- deeper stress: a 2014-15 style US traffic slump on top of path A
    stress = replace(SCENARIOS[0], name="A'. Deep stress",
                     comps={2027: -0.01, 2028: -0.005, 2029: 0.01, 2030: 0.015, 2031: 0.015, 2032: 0.015})
    v_st = dcf_value(stress, 0.085)["value_ps"]
    p(f"Deep stress (comps -1% / -0.5% in 2027-28, then 1-1.5%, path-A everything else): "
      f"${v_st:.0f} @8.5%, EPS 2031 ${project(stress)[5]['eps']:.2f}, "
      f"IRR at 14x exit {pct(irr_at_price(stress, exit_pe=14))}\n")

    # --- what mix of paths does the price imply?
    p("## Price as a mix of paths (r = 8.5%)\n")
    vals = {s.name: dcf_value(s, 0.085)["value_ps"] for s in SCENARIOS}
    a, b, c, d, e = (vals[s.name] for s in SCENARIOS)
    w_ad = (PRICE - d) / (a - d)
    w_bd = (PRICE - d) / (b - d)
    w_ae = (PRICE - e) / (a - e)
    p(f"- A vs D: price = {pct(w_ad, 0)} A + {pct(1 - w_ad, 0)} D")
    p(f"- B vs D: price = {pct(w_bd, 0)} B + {pct(1 - w_bd, 0)} D")
    p(f"- A vs E: price = {pct(w_ae, 0)} A + {pct(1 - w_ae, 0)} E")
    p(f"- Equal weight A-E: ${(a + b + c + d + e) / 5:.0f}")
    p("")

    # --- detailed path for each scenario
    for s in SCENARIOS:
        rows = project(s)
        p(f"### {s.name}\n")
        p(f"_{s.note}_\n")
        p("| Year | SWS | Core OI | G&A save | Rent relief | Refran. | Adj. OI | Revenue | Op margin | "
          "OI/SWS | Interest | Net income | FCF | Buyback | Shares (avg) | EPS | DPS paid |")
        p("|---|" + "---|" * 16)
        for row in rows:
            if row["year"] == 2026:
                p(f"| 2026E | {row['sws']:.0f} | {row['oi']:.2f} | - | - | - | {row['oi']:.2f} | "
                  f"{row['rev']:.1f} | {pct(row['op_margin'])} | {pct(row['take_rate'], 2)} | "
                  f"{INTEREST_2026:.2f} | {row['ni']:.2f} | {row['fcf']:.2f} | - | {row['shares_avg']:.0f} | "
                  f"{row['eps']:.2f} | 7.17->7.72 |")
                continue
            if row["year"] > 2031:
                break
            p(f"| {row['year']}E | {row['sws']:.0f} | {row['oi_core']:.2f} | {row['gna_sav']:.2f} | "
              f"{-row['rent']:.2f} | {row['refr']:.2f} | {row['oi']:.2f} | {row['rev']:.1f} | "
              f"{pct(row['op_margin'])} | {pct(row['take_rate'], 2)} | {row['interest']:.2f} | "
              f"{row['ni']:.2f} | {row['fcf']:.2f} | {row['buyback']:.2f} | {row['shares_avg']:.0f} | "
              f"{row['eps']:.2f} | {row['dps_paid']:.2f} |")
        p("")

    text = "\n".join(out)
    print(text)
    return text


if __name__ == "__main__":
    import pathlib
    txt = main()
    pathlib.Path(__file__).with_name("model_output.md").write_text(txt + "\n")
