"""Independent check of the INTU / ADBE / ADSK / CRM valuation grid (prices as of ~2026-09-26).

Run:  python3 valuation_check.py

Sections
  1. Reverse-engineer the original grid (what multiple of trailing FCF/share each column applies).
  2. Independent going-concern DCF on owner FCF (FCF minus stock-based comp), with net debt and
     current share counts, plus the market-implied starting growth (reverse DCF).
  3. Sensitivity: discount rate x starting growth, and terminal growth.
  4. Durability test: what probability of "stays a durable grower" the price implies versus a
     structural-decline case.

Inputs marked EST are analyst estimates, not reported figures -- change them and re-run.
"""

# --- Original grid as supplied: price, Harsh, SBC Harsh, 10/15/20/25/30% start ------------------
GRID = {
    "INTU": (275.79, 241, 185, [293, 346, 388, 456, 548]),
    "ADBE": (235.47, 197, 158, [240, 283, 318, 373, 448]),
    "ADSK": (209.40, 84, 59, [103, 122, 137, 161, 194]),
    "CRM": (234.02, 104, 73, [134, 164, 188, 226, 279]),
}
GRID_G = [10, 15, 20, 25, 30]

# --- Inputs ($B unless noted; shares in millions) ---------------------------------------------
# fcf      : run-rate FCF used for valuation
# fcf_trail: trailing FCF the original grid appears to use
# sbc      : annual stock-based compensation
# nd       : net debt (debt minus cash & investments)
# g        : base-case starting growth (anchored to guidance, fades to terminal)
INPUTS = {
    "INTU": dict(
        price=275.79, shares=267, nd=0.5, fcf=7.5, fcf_trail=8.62, sbc=1.9, g=0.09,
        notes="FY26 (Jul) OCF $8.84B, capex $221M -> FCF $8.62B, but OCF +42% on revenue +14% "
              "includes one-time cash-tax catch-up from 2025 R&D-expensing law; normalized FCF "
              "~$7.5B is EST. Cash+inv $7.2B, debt $7.7B. FY27 revenue guide +9-10%. SBC ~1.7-2.1B.",
    ),
    "ADBE": dict(
        price=235.47, shares=396, nd=0.72, fcf=10.5, fcf_trail=10.5, sbc=2.1, g=0.10,
        notes="TTM FCF ~$10.3-10.5B; SBC ~$2.1B/yr (H1 $1.045B). Aug-28 cash+ST inv $5.64B, "
              "debt $6.36B. FY26 revenue guide ~$26.6B (+~12%), ARR +11.2%.",
    ),
    "ADSK": dict(
        price=209.40, shares=214, nd=2.2, fcf=2.74, fcf_trail=2.40, sbc=0.85, g=0.12,
        notes="FY26 (Jan) FCF $2.40B; FY27 FCF guide $2.725-2.75B. SBC FY26 $788M (FY27 EST 0.85B). "
              "Jul-31 cash $4.36B vs debt $2.98B, then paid $3.53B for MaintainX (Aug 3) with "
              "$1.0B term loan -> net debt ~$2.2B EST. FY27 revenue guide ~+15%.",
    ),
    "CRM": dict(
        price=234.02, shares=821, nd=29.6, fcf=16.0, fcf_trail=14.4, sbc=3.6, g=0.09,
        notes="FY26 (Jan) FCF $14.4B; FY27 FCF guide +4-5% (~$15.05B) after interest on new debt; "
              "unlevered ~$16.0B is EST. $25B debt-funded ASR cut diluted shares 962M -> 821M. "
              "Debt ~$39.5B, cash+securities $11.4B, +$1.5B Contentful pending. FY27 revenue "
              "+11-12% incl ~3pts Informatica -> organic ~8-9%.",
    ),
}

TERMINAL_G = 0.03
YEARS = 10


def dcf(fcf0, g0, r, g_term=TERMINAL_G, years=YEARS, terminal=True):
    """PV of cash flows growing g0 in year 1, fading linearly to g_term by the final year."""
    f, pv = fcf0, 0.0
    for t in range(1, years + 1):
        g = g0 + (g_term - g0) * (t - 1) / (years - 1)
        f *= 1 + g
        pv += f / (1 + r) ** t
    if terminal:
        pv += f * (1 + g_term) / (r - g_term) / (1 + r) ** years
    return pv


def per_share(t, fcf0, g0, r, g_term=TERMINAL_G, terminal=True):
    d = INPUTS[t]
    return (dcf(fcf0, g0, r, g_term, terminal=terminal) - d["nd"]) * 1000 / d["shares"]


def solve(fn, target, lo, hi):
    """Bisection for x where fn(x) == target (fn increasing in x)."""
    for _ in range(100):
        mid = (lo + hi) / 2
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return mid


def owner(t):
    d = INPUTS[t]
    return d["fcf"] - d["sbc"]


def section_grid():
    print("1. ORIGINAL GRID, EXPRESSED AS MULTIPLES OF TRAILING FCF/SHARE")
    print(f"   {'':5} {'FCF/sh':>7} {'Harsh':>7} {'10%':>7} {'20%':>7} {'30%':>7} {'Price':>7}  SBC haircut")
    for t, (p, harsh, sbc_harsh, vals) in GRID.items():
        d = INPUTS[t]
        fps = d["fcf_trail"] * 1000 / d["shares"]
        print(f"   {t:5} {fps:7.2f} {harsh / fps:6.2f}x {vals[0] / fps:6.2f}x {vals[2] / fps:6.2f}x "
              f"{vals[4] / fps:6.2f}x {p / fps:6.2f}x  grid {1 - sbc_harsh / harsh:.0%} vs "
              f"reported {d['sbc'] / d['fcf_trail']:.0%}")
    print("   CRM at the pre-ASR 962M share count: 10% column = "
          f"{GRID['CRM'][3][0] / (14.4 * 1000 / 962):.2f}x (fits the others; 821M does not unless ~$30B net debt is deducted)")
    base = dcf(1, 0.10, 0.10, terminal=False)
    ratios = [dcf(1, g / 100, 0.10, terminal=False) / base for g in GRID_G]
    print("   Best-fit template: 10-yr DCF, ~10% discount rate, NO terminal value.")
    print("   Template column ratios vs 10%: " + ", ".join(f"{g}%={x:.3f}" for g, x in zip(GRID_G, ratios)))
    print("   Grid column ratios vs 10%:     " + ", ".join(
        f"{g}%={GRID['INTU'][3][i] / GRID['INTU'][3][0]:.3f}" for i, g in enumerate(GRID_G)))
    harsh_g = solve(lambda g: dcf(1, g, 0.10, terminal=False) / base, 0.82, -0.2, 0.2)
    print(f"   Harsh (0.82x the 10% column) ~= {harsh_g:.0%} starting growth in that template.\n")


def section_dcf():
    print("2. GOING-CONCERN DCF ON OWNER FCF (FCF - SBC), 10-yr fade to 3% terminal")
    for t, d in INPUTS.items():
        own = owner(t)
        ev = d["price"] * d["shares"] / 1000 + d["nd"]
        print(f"   {t}: price {d['price']}, EV ${ev:.1f}B, EV/FCF {ev / d['fcf']:.1f}x, "
              f"EV/owner FCF {ev / own:.1f}x, SBC = {d['sbc'] / d['fcf']:.0%} of FCF")
        for r in (0.085, 0.095, 0.105):
            fv = per_share(t, own, d["g"], r)
            imp_own = solve(lambda g: per_share(t, own, g, r), d["price"], -0.3, 0.6)
            imp_pre = solve(lambda g: per_share(t, d["fcf"], g, r), d["price"], -0.3, 0.6)
            print(f"     r={r:5.1%}  fair value @ {d['g']:.0%} start: {fv:6.0f}   "
                  f"market-implied start growth: owner {imp_own:6.1%} | pre-SBC {imp_pre:6.1%}")
    print()


def section_sensitivity():
    print("3. SENSITIVITY (owner FCF, $/share)")
    gs = [-0.05, 0.0, 0.05, 0.09, 0.13]
    for t, d in INPUTS.items():
        print(f"   {t} (price {d['price']})   r \\ start g " + "".join(f"{g:>7.0%}" for g in gs))
        for r in (0.085, 0.095, 0.105, 0.115):
            print(f"   {'':24}{r:6.1%}   " + "".join(f"{per_share(t, owner(t), g, r):7.0f}" for g in gs))
        print(f"   {'':24}terminal g 2% / 3% / 3.5% @9.5%: " + " / ".join(
            f"{per_share(t, owner(t), d['g'], 0.095, gt):.0f}" for gt in (0.02, 0.03, 0.035)))
    print()


def section_durability():
    print("4. DURABILITY: implied probability of the going-concern case vs structural decline")
    print("   (bear = owner FCF shrinks 5%/yr from now, forever)")
    for r in (0.095, 0.105):
        for t, d in INPUTS.items():
            bull = per_share(t, owner(t), d["g"], r)
            bear = (owner(t) * 0.95 / (r + 0.05) - d["nd"]) * 1000 / d["shares"]
            p = (d["price"] - bear) / (bull - bear)
            print(f"   r={r:.1%} {t:5} bear {bear:5.0f}  going-concern {bull:5.0f}  price {d['price']:6.1f}"
                  f"  -> implied P(durable) {p:4.0%}")
    print()


if __name__ == "__main__":
    section_grid()
    section_dcf()
    section_sensitivity()
    section_durability()
    print("INPUT NOTES")
    for t, d in INPUTS.items():
        print(f"   {t}: {d['notes']}")
