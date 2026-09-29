"""
Vista Energy (VIST) - asset-based NAV (E&P method).

NAV = PV of the existing producing base (no new wells)
    + PV of developing the drilling inventory (new wells - their capex)
    - net debt & other claims.
Annual periods start 1-Oct-2026 (P1 = Oct-26..Sep-27), discounted mid-period.
Scenarios are long-run Brent decks (the oil analogue of the AI-demand scenarios) plus an Argentina
country-risk discount rate. The share price is only used at the end (market-implied solve).
"""
import copy

# ---------------------------------------------------------------- market / balance sheet
PRICE = 73.35            # $/ADS, 18-Sep-2026
SHARES = 110.62          # mm ADS
NET_DEBT = 3.06          # $bn, 30-Jun-2026 (Q2-26 release)
OTHER_CLAIMS = 0.30      # $bn, leases / abandonment / other - ESTIMATE

# ---------------------------------------------------------------- price deck
# Brent by period (nominal $/bbl). P1-P3 follow the futures curve in every scenario's "Base";
# scenarios blend toward their long-run level from P2.
FUTURES = {1: 90.0, 2: 77.0, 3: 75.5}      # P1 ~ Q4-26 spot ~$100-105 falling to ~$80 by Sep-27; Aug-27 $78.4, 2028 ~$75-76
SCENARIOS = {
    "Low":     {"brent_lr": 60.0, "desc": "War premium fully unwinds; OPEC+ spare capacity returns; pre-war 2025 levels"},
    "Base":    {"brent_lr": 72.0, "desc": "Futures curve: ~$75 in 2028, roughly flat real thereafter"},
    "High":    {"brent_lr": 85.0, "desc": "Lasting risk premium + post-war underinvestment"},
    "Extreme": {"brent_lr": 100.0, "desc": "Prolonged Hormuz disruption / structural shortage"},
}
ORDER = ["Low", "Base", "High", "Extreme"]
INFL = 0.02

# ---------------------------------------------------------------- operations (calibrated to Q2-26: rev ~$81/boe, EBITDA ~$56.7/boe, 70% margin)
OIL_SHARE = 0.87
OIL_DISCOUNT = 5.0        # realized oil vs Brent, $/bbl (Q2-26 realized $89.4) - EST
GAS_PRICE_BOE = 21.0      # $/boe (~$3.5/MMBtu) - EST
ROYALTY = 0.15            # Neuquen 12% + extension premia - EST
TURNOVER_TAX = 0.03       # provincial gross-receipts tax - EST
EXPORT_DUTY = 0.0         # 0% currently - policy risk lever
LIFTING = 4.5             # $/boe (Q2-26 $4.5; Q1 $4.3)
TRANSPORT = 4.0           # $/boe transport, storage & selling - EST
GNA = 1.5                 # $/boe - EST
COST_ESC = 0.02

BASE_RATE = 165.0         # kboe/d from wells on line at 1-Oct-2026 (Q3 guide 160, Q4 170)
BASE_DECLINE = [0.35, 0.24, 0.18, 0.14, 0.12]   # then terminal
TERMINAL_DECLINE = 0.09

WELLS = [110, 125, 135, 135, 135, 135, 135, 135, 135, 135, 135, 135]   # net wells tied in per period until inventory runs out
PUD_WELLS = 450           # wells needed to develop 1P PUD (355.7 MMboe YE25 + Equinor) at ~0.9 MMboe - EST
UNBOOKED_RISK = 0.6       # chance factor applied to value of locations beyond the proved (PUD) wells - EST
INVENTORY = 1470          # net locations: >1,320 ready-to-drill (company) + ~150 net from Equinor blocks - EST
EUR = 0.9                 # net MMboe per well - EST, calibrated so output tracks guidance (158 kboe/d 2026, ~250 by 2030)
WELL_PROFILE = [0.15, 0.19, 0.12, 0.09, 0.07, 0.06, 0.05, 0.045, 0.04, 0.035]   # share of EUR by period; P1 low because tie-ins are spread through the year
TAIL_DECLINE = 0.10
WELL_COST = {1: 14.0, 2: 12.5, 3: 11.0}   # $mm per well; company targets $11mm by 2028
FACILITIES = 3.0          # $/boe infrastructure capex - EST

TAX_RATE = 0.35
EXISTING_TAX_BASIS = 7.0  # $bn, amortised over 7 periods - EST
TAX_LIFE = 5              # new capex amortised over 5 periods
YEARS = 29                # to Sep-2055
DISC = 0.12               # Argentina-risked unlevered discount rate (base)


def well_profile():
    p = list(WELL_PROFILE)
    while len(p) < YEARS:
        p.append(p[-1] * (1 - TAIL_DECLINE))
    return p


def brent(scen, t, shift=0.0):
    lr = (SCENARIOS[scen]["brent_lr"] + shift) * (1 + INFL) ** (t - 0.5)
    if t == 1:
        return FUTURES[1]
    if t in (2, 3):
        # futures in Base; other scenarios move halfway (P2) and fully (P3+) toward their own long run
        w = 0.5 if t == 2 else 1.0
        base_lr = SCENARIOS["Base"]["brent_lr"] * (1 + INFL) ** (t - 0.5)
        return FUTURES[t] + w * (lr - base_lr)
    return lr


def run(scen="Base", shift=0.0, disc=DISC, eur=EUR, inventory=INVENTORY, well_cost_mult=1.0, export_duty=EXPORT_DUTY,
        new_wells=True, detail=False):
    prof = well_profile()
    wells = []
    left = inventory if new_wells else 0
    for t in range(1, YEARS + 1):
        w = min(WELLS[t - 1] if t <= len(WELLS) else 135, left)
        wells.append(w)
        left -= w
    rows, pv = [], 0.0
    capex_hist = []
    rate = BASE_RATE
    for t in range(1, YEARS + 1):
        d = BASE_DECLINE[t - 1] if t <= len(BASE_DECLINE) else TERMINAL_DECLINE
        base_vol = rate * (1 - d / 2) * 365 / 1000           # MMboe
        rate *= (1 - d)
        new_vol = sum(wells[k] * eur * prof[t - 1 - k] for k in range(t))   # well tied in period k+1 produces prof[0] in its first period
        vol = base_vol + new_vol
        b = brent(scen, t, shift)
        esc = (1 + COST_ESC) ** (t - 0.5)
        rev_boe = OIL_SHARE * (b - OIL_DISCOUNT) + (1 - OIL_SHARE) * GAS_PRICE_BOE * esc
        cash_cost = (LIFTING + TRANSPORT + GNA) * esc
        ebitda_boe = rev_boe * (1 - ROYALTY - TURNOVER_TAX - export_duty) - cash_cost
        revenue = vol * rev_boe / 1000                          # $bn
        ebitda = vol * ebitda_boe / 1000
        wc = WELL_COST.get(t, WELL_COST[3] * (1 + COST_ESC) ** (t - 3)) * well_cost_mult
        capex = (wells[t - 1] * wc + vol * FACILITIES * esc) / 1000
        capex_hist.append(capex)
        dda = (EXISTING_TAX_BASIS / 7 if t <= 7 else 0) + sum(capex_hist[max(0, t - TAX_LIFE):t]) / TAX_LIFE
        tax = TAX_RATE * max(0.0, ebitda - dda)
        fcf = ebitda - capex - tax
        df = (1 + disc) ** -(t - 0.5)
        pv += fcf * df
        rows.append(dict(t=t, year=2026 + t, brent=b, kboed=vol / 0.365, wells=wells[t - 1], revenue=revenue, ebitda=ebitda,
                         ebitda_boe=ebitda_boe, capex=capex, tax=tax, fcf=fcf, df=df))
    eq = pv - NET_DEBT - OTHER_CLAIMS
    out = dict(gav=pv, equity=eq, nav_ps=eq / SHARES * 1000, rows=rows)
    return out


def tranches(scen="Base", **kw):
    """Split NAV into producing base, proved-undeveloped wells and unbooked inventory (risked)."""
    inv = kw.pop("inventory", INVENTORY)
    pdp = run(scen, new_wells=False, **kw)["gav"]
    pud = run(scen, inventory=min(PUD_WELLS, inv), **kw)["gav"] - pdp
    allw = run(scen, inventory=inv, **kw)["gav"]
    unb = allw - pdp - pud
    gav = pdp + pud + UNBOOKED_RISK * unb
    eq = gav - NET_DEBT - OTHER_CLAIMS
    return dict(pdp=pdp, pud=pud, unbooked=unb, unbooked_risked=UNBOOKED_RISK * unb, gav=gav, equity=eq, nav_ps=eq / SHARES * 1000,
                unrisked_ps=(allw - NET_DEBT - OTHER_CLAIMS) / SHARES * 1000, pdp_ps=(pdp - NET_DEBT - OTHER_CLAIMS) / SHARES * 1000)


def solve(target_ps, key="shift", lo=-40.0, hi=80.0, **kw):
    f = lambda x: tranches(**{**kw, key: x})["nav_ps"] - target_ps
    a, b = lo, hi
    fa = f(a)
    for _ in range(60):
        m = (a + b) / 2
        fm = f(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b) / 2


if __name__ == "__main__":
    r = run()
    for x in r["rows"][:8]:
        print(f"P{x['t']} {x['year']}: Brent {x['brent']:.0f}  prod {x['kboed']:.0f} kboe/d  wells {x['wells']}  "
              f"EBITDA ${x['ebitda']:.2f}bn ({x['ebitda_boe']:.1f}/boe)  capex ${x['capex']:.2f}  tax ${x['tax']:.2f}  FCF ${x['fcf']:.2f}")
    for s in ORDER:
        t = tranches(s)
        print(f"{s:8s} risked NAV/ADS ${t['nav_ps']:.1f} | PDP ${t['pdp']:.1f}bn PUD ${t['pud']:.1f}bn unbooked ${t['unbooked']:.1f}bn (risked {t['unbooked_risked']:.1f}) | unrisked ${t['unrisked_ps']:.1f} | PDP-only equity ${t['pdp_ps']:.1f}")
    print("market-implied Brent LR shift at 12%:", round(solve(PRICE), 1))
    print("market-implied discount rate at Base:", round(solve(PRICE, key="disc", lo=0.04, hi=0.30), 4))
