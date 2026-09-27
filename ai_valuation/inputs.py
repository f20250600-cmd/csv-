"""
Company inputs, scenario definitions and model builders for Meta and Microsoft.

Every hard-coded number carries a source tag:
  [R]  reported (10-K/10-Q/press release, via search summaries - verify against filings)
  [G]  company guidance / management commentary
  [C]  sell-side consensus (search summaries, Sep-2026)
  [E]  my estimate / modelling judgement (the numbers most worth challenging)
  [B]  industry benchmark (GPU rental prices, $/GW build cost, etc.)

USD billions unless stated. Valuation date: 30-Sep-2026.
"""
from __future__ import annotations

import copy
from functools import lru_cache

from engine import AIProgram, Assets, Company, Segment, Stream

SCENARIOS = ["bull", "bull_lite", "base", "bear_lite", "bear"]
LABEL = {"bull": "Bull", "bull_lite": "Bull-lite", "base": "Base", "bear_lite": "Bear-lite",
         "bear": "Bear"}

DEFAULT_KNOBS = dict(
    ai_rev_scale=1.0,      # scales forecast AI revenue *growth* above the 2026 level
    core_g_shift=0.0,      # additive shift to every core growth rate
    core_margin_shift=0.0,
    wacc_shift=0.0,        # shifts WACC and AI hurdle together
    ai_premium=None,       # AI hurdle = WACC + premium
    g_term=None,           # terminal growth, core and AI
    capex_scale=1.0,       # scales explicit-period AI capex
    capex_extend=0,        # hold final explicit capex level for N more years
    delay=0,               # monetisation delay (years) - AI revenue paths shifted right
    econ_life=None,        # accelerator economic (refresh) life
    book_life=None,        # accelerator accounting life
    residual=None,
    var_cost_shift=0.0,    # AI variable cost (% revenue) shift -> incremental margin
    u_max=None,
    erosion=None,
    yield_drift=None,
    bonus=None,
    terminal_ronic=None,   # override AI terminal RONIC
    # Meta specific
    uplift_terminal=None,
    newprod_scale=1.0,
    ads_only=False,        # zero out new-AI-product revenue (ads must pay for everything)
    rl_perpetual_loss=None,
    # Microsoft specific
    azure_scale=1.0,
    copilot_scale=1.0,
    revshare_on=True,
    openai_shortfall=0.0,  # % of Azure AI demand lost from FY28 (OpenAI renegotiation/default)
    openai_price_cut=0.0,  # yield haircut on new Azure AI vintages (replacement at lower price)
    stake_value=None,
    train_g=None,          # post-explicit growth of training/frontier compute (policy)
    yield_mult=1.0,        # revenue per $ (per GPU / per MW) of NEW capacity vs base-year level
)

EQUIP_PER_GW = 35.0   # [B] ~$35bn of accelerator/server/network content per GW (of ~$50-60bn all-in)


def _k(knobs):
    k = dict(DEFAULT_KNOBS)
    if knobs:
        unknown = set(knobs) - set(k)
        if unknown:
            raise KeyError(f"unknown knobs {unknown}")
        k.update(knobs)
    return k


def _path(start_year, values):
    return {start_year + i: v for i, v in enumerate(values)}


def _scale_growth(path, base_year, m):
    b = path.get(base_year, 0.0)
    return {y: (b + m * (v - b) if y > base_year else v) for y, v in path.items()}


def _delay(path, base_year, d):
    if d <= 0:
        return dict(path)
    out = {}
    for y, v in path.items():
        if y <= base_year:
            out[y] = v
        else:
            src = y - d
            out[y] = path[src] if src > base_year else path[base_year]
    return out


def _capex_path(hist, explicit, first_forecast, scale, extend):
    cap = dict(hist)
    ys = list(range(first_forecast, first_forecast + len(explicit)))
    for y, c in zip(ys, explicit):
        cap[y] = c * scale
    last = ys[-1]
    for e in range(1, extend + 1):
        cap[last + e] = cap[last]
    return cap, last + extend


# ======================================================================================
# META
# ======================================================================================
META = dict(
    price=747.82,            # [R] close 26-Sep-2026 (search summary)
    shares=2.56,             # [R] diluted shares, bn
    # net debt: LT debt 83.7 [R] - cash & securities 90.3 [R] + finance leases ~20 [E]
    #           + Hyperion JV obligation ~22 (80% Blue Owl share of $27bn, residual value guarantee) [E]
    net_debt=83.7 - 90.3 + 20.0 + 22.0,
    tax=0.15,                # [E] post-OBBBA effective rate
    wacc=0.095,              # [E] rf 4.25% + beta 1.2 x ERP 5% ~ 10.25% CoE, ~5% debt -> 9.5%
    ai_premium=0.01,         # [E] AI infra is riskier than the ad franchise
    g_term=0.03,
    # 2026E build: Q1 56.31 [R] + Q2 60.8 [R] + Q3 guide mid 62.5 [G] + Q4 ~72.0 [E]
    rev_2026=251.6,
    rl_rev_2026=2.0,         # [R/E]
    foa_other_2026=3.6,      # [E] (FoA other +73% y/y in Q2)
    # FoA operating income 2026E: total OI (251.6 - 167 expense guide mid [G]) + RL loss 19.5 [G: 'similar to 2025']
    #   + one-offs 3.6 (legal 2.4 + severance 1.2) [R]  -> normalised FoA OI
    foa_oi_2026_norm=251.6 - 167.0 + 19.5 + 3.6,
    ad_rev_hist={2022: 113.6, 2023: 131.9, 2024: 160.6, 2025: 196.2},   # [R]
    # share of ad revenue attributable to AI ranking/recs vs a no-AI counterfactual [E]
    uplift_hist={2022: 0.02, 2023: 0.05, 2024: 0.09, 2025: 0.12, 2026: 0.15},
    # AI capex = total capex (incl. finance-lease principal) - core capex (~11% of core rev) [E]
    # totals: 2022 31.4, 2023 28.1, 2024 39.2, 2025 72.2 [R], 2026 137.5 (guide mid $130-145bn) [G]
    # core capex ~7% / D&A ~5.5% of core revenue: Meta's *total* 2025 D&A was only ~9.7% of revenue [R/E]
    ai_capex_hist={2022: 15.0, 2023: 19.0, 2024: 28.5, 2025: 60.0, 2026: 122.6},
    core_capex_pct=0.07, core_da_pct=0.055, core_ic0=80.0,
    # capex allocation across uses [E]: (ads ranking/recs, frontier training/MSL, new AI products)
    alloc={2022: (0.8, 0.2, 0.0), 2023: (0.8, 0.2, 0.0), 2024: (0.65, 0.35, 0.0),
           2025: (0.45, 0.45, 0.10)},
    alloc_fwd=(0.35, 0.40, 0.25),
    # AI talent (MSL comp) + 3rd-party compute contracts (CoreWeave, Google Cloud, Nebius...) [E]
    ai_opex_hist={2022: 2.0, 2023: 3.0, 2024: 4.0, 2025: 7.0, 2026: 15.0},
    newprod_rev_2026=0.5,
    book_life=5.5,           # [R] servers & network useful life since Jan-2025
)

META_SCN = {
    #            core growth shift / margin shift, AI uplift share of ads at terminal & year reached
    "bull": dict(core_dg=0.01, core_dm=0.01, upl_T=0.38, upl_year=2031, upl_margin=0.82,
                 capex=[184, 216, 236],
                 np_demand=[4, 10, 20, 32, 46, 60, 74, 88, 100, 110],
                 np_yield=0.60, np_drift=0.02, erosion=0.08, u_max=0.92,
                 econ_life=6, residual=0.10,
                 ai_opex=[20, 22, 23, 24, 25, 26, 27, 28, 29, 30], train_g=0.03, int_decl=0.05,
                 rl_rev=[3, 5, 8, 12, 16, 21, 26, 31, 36, 40],
                 rl_ebit=[-17, -15, -12, -9, -6, -3, 0, 3, 6, 9], core_ronic=0.40),
    "bull_lite": dict(core_dg=0.005, core_dm=0.0, upl_T=0.33, upl_year=2033, upl_margin=0.80,
                      capex=[179, 216, 241],
                      np_demand=[2, 5, 11, 20, 31, 43, 55, 66, 76, 85],
                      np_yield=0.55, np_drift=0.01, erosion=0.10, u_max=0.92,
                      econ_life=5, residual=0.07,
                      ai_opex=[21, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5, 29.5, 30.5, 31.5], train_g=0.0, int_decl=0.05,
                      rl_rev=[2.5, 3.5, 5, 7, 9, 12, 15, 18, 21, 24],
                      rl_ebit=[-18, -17, -15, -12, -9, -6, -3, 0, 2, 4], core_ronic=0.35),
    "base": dict(core_dg=0.0, core_dm=0.0, upl_T=0.28, upl_year=2031, upl_margin=0.80,
                 capex=[174, 186, 191],
                 np_demand=[2, 5, 10, 17, 25, 33, 41, 48, 54, 60],
                 np_yield=0.50, np_drift=0.0, erosion=0.12, u_max=0.92,
                 econ_life=5, residual=0.05,
                 ai_opex=[21, 23.5, 24.5, 25, 25, 25.5, 26.5, 27.5, 28.5, 29.5], train_g=-0.05, int_decl=0.05,
                 rl_rev=[2.2, 2.6, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5],
                 rl_ebit=[-19, -18, -16, -14, -12, -10, -8, -6, -4, -2], core_ronic=0.30),
    "bear_lite": dict(core_dg=-0.01, core_dm=-0.01, upl_T=0.21, upl_year=2031, upl_margin=0.77,
                      capex=[174, 180, 170],
                      np_demand=[1, 3, 6, 10, 14, 18, 22, 26, 29, 32],
                      np_yield=0.42, np_drift=-0.03, erosion=0.16, u_max=0.90,
                      econ_life=4, residual=0.03,
                      ai_opex=[20, 21, 20, 19, 19, 19, 19.5, 20, 20.5, 21], train_g=-0.10, int_decl=0.03,
                      rl_rev=[2.0, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8],
                      rl_ebit=[-19, -19, -18, -17, -15, -13, -11, -9, -7, -5], core_ronic=0.25),
    "bear": dict(core_dg=-0.025, core_dm=-0.025, upl_T=0.12, upl_year=2030, upl_margin=0.75,
                 capex=[169, 134, 110],
                 np_demand=[1, 2, 3, 5, 7, 9, 10, 11, 12, 13],
                 np_yield=0.35, np_drift=-0.06, erosion=0.22, u_max=0.88,
                 econ_life=4, residual=0.02,
                 ai_opex=[19, 17, 14, 12, 12, 12, 12, 12.5, 13, 13.5], train_g=-0.15, int_decl=0.03,
                 rl_rev=[1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8, 1.8],
                 rl_ebit=[-20, -20, -20, -18, -16, -14, -12, -10, -8, -6], core_ronic=0.20),
}
META_CORE_G = [0.095, 0.085, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05, 0.045, 0.04]  # [E] ~digital ad market


def _meta_core_ads(scn, k):
    p = META_SCN[scn]
    g = [x + p["core_dg"] + k["core_g_shift"] for x in META_CORE_G]
    if scn == "bear":   # cyclical ad downturn 2027-28 on top of structural slowdown
        g[0] -= 0.03
        g[1] -= 0.02
    core_ads0 = (META["rev_2026"] - META["rl_rev_2026"] - META["foa_other_2026"]) * (1 - META["uplift_hist"][2026])
    ads, r = {}, core_ads0
    for i, y in enumerate(range(2027, 2037)):
        r *= 1 + g[i]
        ads[y] = r
    return core_ads0, g, ads


def build_meta(scn="base", knobs=None, _calib=True):
    k = _k(knobs)
    p = META_SCN[scn]
    fy = list(range(2027, 2037))
    years = list(range(2022, 2037))
    wacc = META["wacc"] + k["wacc_shift"]
    prem = META["ai_premium"] if k["ai_premium"] is None else k["ai_premium"]
    g_term = META["g_term"] if k["g_term"] is None else k["g_term"]

    core_ads0, g_core, core_ads = _meta_core_ads(scn, k)

    # ---- ads uplift stream: uplift share path (share of *total* ad revenue) ----------
    upl_T = p["upl_T"] if k["uplift_terminal"] is None else k["uplift_terminal"]
    u0 = META["uplift_hist"][2026]
    share = dict(META["uplift_hist"])
    for y in fy:
        x = min(1.0, (y - 2026) / (p["upl_year"] - 2026))
        share[y] = u0 + (upl_T - u0) * (1 - (1 - x) ** 1.6)
    share = _scale_growth(share, 2026, k["ai_rev_scale"])
    share = _delay(share, 2026, k["delay"])
    uplift_rev = {y: META["ad_rev_hist"][y] * share[y] for y in range(2022, 2026)}
    ads26_total = META["rev_2026"] - META["rl_rev_2026"] - META["foa_other_2026"]
    uplift_rev[2026] = ads26_total * u0
    for y in fy:
        s = min(share[y], 0.95)
        uplift_rev[y] = core_ads[y] * s / (1 - s)

    # ---- new AI products (Meta AI, business agents, compute resale) -----------------
    np_dem = {y: 0.0 for y in range(2022, 2026)}
    np_dem[2026] = META["newprod_rev_2026"]
    np_dem.update(_path(2027, p["np_demand"]))
    np_dem = _scale_growth(np_dem, 2026, k["ai_rev_scale"] * k["newprod_scale"])
    np_dem = _delay(np_dem, 2026, k["delay"])
    if k["ads_only"]:
        np_dem = {y: 0.0 for y in np_dem}

    ai_opex = dict(META["ai_opex_hist"])
    ai_opex.update(_path(2027, p["ai_opex"]))

    alloc = {y: META["alloc"].get(y, META["alloc_fwd"]) for y in years}
    s_ads = Stream("Ads ranking & recommendation uplift", "exogenous",
                   {y: a[0] for y, a in alloc.items()}, META["alloc_fwd"][0],
                   revenue=uplift_rev,
                   var_cost=max(0.0, 1 - p["upl_margin"] + k["var_cost_shift"]),
                   internal_util=0.85, intensity_decline=p["int_decl"])
    s_train = Stream("Frontier models / MSL training", "cost",
                     {y: a[1] for y, a in alloc.items()}, META["alloc_fwd"][1],
                     fixed_opex=ai_opex, internal_util=0.85,
                     post_growth={y: (p["train_g"] if k["train_g"] is None else k["train_g"])
                                  for y in range(2027, 2037)})
    s_new = Stream("New AI products & compute resale", "capacity",
                   {y: a[2] for y, a in alloc.items()}, META["alloc_fwd"][2],
                   revenue=np_dem, var_cost=max(0.0, 0.25 + k["var_cost_shift"]),
                   yield_=p["np_yield"],
                   yield_drift=p["np_drift"] if k["yield_drift"] is None else k["yield_drift"],
                   erosion=p["erosion"] if k["erosion"] is None else k["erosion"],
                   u_max=p["u_max"] if k["u_max"] is None else k["u_max"], u_target=0.80,
                   fwd_yield_mult=k["yield_mult"])

    capex, explicit_end = _capex_path(META["ai_capex_hist"], p["capex"], 2027,
                                      k["capex_scale"], k["capex_extend"])
    assets = Assets(book_life_equip=META["book_life"] if k["book_life"] is None else k["book_life"],
                    econ_life=p["econ_life"] if k["econ_life"] is None else int(k["econ_life"]),
                    residual=p["residual"] if k["residual"] is None else k["residual"],
                    bonus=1.0 if k["bonus"] is None else k["bonus"])
    ai = AIProgram(years=years, first_forecast=2027, explicit_end=explicit_end, base_year=2026,
                   capex_total=capex, streams=[s_ads, s_train, s_new], assets=assets,
                   tax_rate=META["tax"], hurdle=wacc + prem, g_term=g_term, val_offset=0.75,
                   terminal_ronic_override=k["terminal_ronic"])

    m0 = meta_core_margin0() if _calib else 0.55
    dm = p["core_dm"] + k["core_margin_shift"]
    margins = [m0 + dm * min(1.0, (i + 1) / 3) for i in range(10)]
    core_other0 = META["foa_other_2026"]
    core_rev0 = core_ads0 + core_other0
    core = Segment("Core advertising (ex-AI uplift) + FoA other", core_rev0, g_core, margins,
                   META["core_capex_pct"], META["core_da_pct"], META["tax"], META["core_ic0"],
                   g_term, p["core_ronic"], wacc, 0.75)
    rl_ebit = list(p["rl_ebit"])
    if k["rl_perpetual_loss"] is not None:
        rl_ebit = [min(e, -k["rl_perpetual_loss"]) for e in rl_ebit]
    rl = Segment("Reality Labs", META["rl_rev_2026"], [0.0] * 10, [0.0] * 10, 0.0, 0.0, META["tax"],
                 0.0, g_term, 0.20, wacc, 0.75, ebit_override=rl_ebit, rev_override=p["rl_rev"])
    segs = [core, rl]
    comp = Company("Meta Platforms", META["price"], META["shares"], META["net_debt"], {}, segs, ai,
                   META["tax"], fy, meta=dict(scenario=scn, knobs=k, core_margin0=m0,
                                               rl_perpetual=k["rl_perpetual_loss"]))
    if k["rl_perpetual_loss"] is not None:
        # value of losses continuing forever (Reality Labs never shut down)
        comp.nonop["RL perpetual-loss TV"] = -k["rl_perpetual_loss"] * (1 - META["tax"]) / wacc * \
            (1 + wacc) ** -(10.25)
    return comp


@lru_cache(maxsize=None)
def meta_core_margin0():
    """Calibrate the counterfactual core margin so that core EBIT + AI-layer EBIT(2026)
    reproduces normalised 2026E Family-of-Apps operating income."""
    c = build_meta("base", _calib=False)
    r = c.ai.run()
    i = r["years"].index(2026)
    ai_ebit = r["total"]["ebit_book"][i]
    core_ads0, _, _ = _meta_core_ads("base", _k(None))
    core_rev0 = core_ads0 + META["foa_other_2026"]
    return (META["foa_oi_2026_norm"] - ai_ebit) / core_rev0


# ======================================================================================
# MICROSOFT (fiscal years ending June)
# ======================================================================================
MSFT = dict(
    price=516.17,            # [R] 26/27-Sep-2026 (search summary)
    shares=7.44,             # [R/E] diluted shares, bn
    # net debt: debt ~43 [E] + finance-lease liabilities ~70 [E] - cash & ST inv 76.8 [R]
    net_debt=43.0 + 70.0 - 76.8,
    tax=0.18,
    wacc=0.0875,             # [E] rf 4.25% + beta ~0.95 x 5% -> ~9.0% CoE; tiny debt; 8.75%
    ai_premium=0.01,
    g_term=0.03,
    # FY26 [R]: revenue 331.8; P&BP 140.0 / OI 83.9; IC 137.8 / OI 57.0; MPC 54.0 / OI 14.3 (by difference)
    pbp_oi=83.9, ic_oi=57.0,
    azure_ai_fy26=38.0,      # [E] Azure >$100bn in FY26 [R]; AI ~35-40% of it; OpenAI ~$24bn of related rev [R-ish]
    revshare_fy26=3.6,       # [E] ~20% of OpenAI revenue (OpenAI ~$18bn Jul25-Jun26)
    firstparty_fy26=7.0,     # [E] M365 Copilot (30m+ paid seats [R]), GitHub Copilot, Dynamics/Security AI
    # economic AI capex = capex incl. finance leases - core capex (~33) [E]
    # totals: FY24 55.7, FY25 88.2 [R]; FY26 ~146 [R/E]; FY27 guide ~175 reported + ~15 moved to op leases [G]
    ai_capex_hist={2022: 5.0, 2023: 10.0, 2024: 33.0, 2025: 58.0, 2026: 113.0},
    alloc={2022: (0.85, 0.05, 0.10), 2023: (0.85, 0.05, 0.10), 2024: (0.80, 0.10, 0.10),
           2025: (0.65, 0.20, 0.15)},
    alloc_fwd=(0.60, 0.22, 0.18),     # (Azure AI infra, first-party AI apps, MAI models/training) [E]
    azure_ai_hist={2022: 0.3, 2023: 1.0, 2024: 6.0, 2025: 17.0, 2026: 38.0},
    firstparty_hist={2022: 0.0, 2023: 0.0, 2024: 0.5, 2025: 2.5, 2026: 7.0},
    revshare_hist={2022: 0.0, 2023: 0.3, 2024: 0.8, 2025: 2.0, 2026: 3.6},
    mai_opex_hist={2022: 0.5, 2023: 0.5, 2024: 1.0, 2025: 2.0, 2026: 3.0},
    # neocloud capacity contracts (Nebius, IREN, Nscale, Lambda...) - opex that adds Azure AI capacity [E]
    # Nebius ~$17-19bn, IREN ~$9.7bn, Nscale, Lambda... ~$40-50bn over ~5y [R/E]
    lease_opex={2025: 1.0, 2026: 5.0, 2027: 9.0, 2028: 11.0, 2029: 11.0, 2030: 10.0,
                **{y: 8.0 for y in range(2031, 2038)}},
    lease_markup=1.3,
    book_life=6.0,           # [R] servers & network 6 years (since FY23)
    fac_book_life=25.0,      # [G] datacentres 15 -> 25 years from FY27
    # OpenAI: ~27% post-recap [R] diluted by $122bn raise at $852bn post [R] -> ~23% [E]
    openai_stake_pct=0.23,
    stake_haircut=0.25,      # [E] illiquidity, preference stack, governance
    openai_val={"bull": 1500, "bull_lite": 1100, "base": 852, "bear_lite": 450, "bear": 150},
    # equity-method share of OpenAI losses (EPS only, non-cash) [E]
    openai_eq_loss={2027: -4.0, 2028: -6.0, 2029: -5.0, 2030: -2.0},
)

MSFT_SEG = dict(   # FY26 base revenue, growth path (base), margin, capex%, D&A%, IC0, terminal RONIC
    azure_core=dict(name="Azure & server products (ex-AI)", rev0=137.8 - 38.0 - 3.6,
                    g=[0.12, 0.115, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.045],
                    capex=0.24, da=0.20, ic0=90.0, ronic=0.25),
    office=dict(name="Office / Commercial (ex-Copilot)", rev0=140.0 - 7.0,
                g=[0.11, 0.10, 0.09, 0.08, 0.075, 0.07, 0.065, 0.06, 0.055, 0.05],
                capex=0.06, da=0.05, ic0=120.0, ronic=0.40),
    windows=dict(name="Windows, devices & search", rev0=32.0,
                 g=[-0.04, 0.02, 0.03, 0.03, 0.03, 0.025, 0.025, 0.02, 0.02, 0.02],
                 margin=12.5 / 32.0, capex=0.02, da=0.02, ic0=20.0, ronic=0.30),
    gaming=dict(name="Gaming", rev0=22.0, g=[0.0] + [0.03] * 9,
                margin=1.8 / 22.0, capex=0.03, da=0.03, ic0=85.0, ronic=0.10),
)

MSFT_SCN = {
    "bull": dict(dg=dict(azure_core=0.015, office=0.01, windows=0.0, gaming=0.01), dm=0.01,
                 gaming_m=0.15, capex=[154, 200],   # bull: capex follows demand from FY29
                 azure_g=[0.80, 0.55, 0.40, 0.30, 0.24, 0.18, 0.14, 0.11, 0.09, 0.07],
                 revshare=[6.5, 10, 14, 18, 22, 25, 27, 0, 0, 0],
                 copilot=[14, 24, 36, 48, 60, 70, 80, 88, 95, 100],
                 drift=0.02, erosion=0.08, u_max=0.95, econ_life=6, residual=0.10,
                 mai=[5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10], train_g=0.03, int_decl=0.05),
    "bull_lite": dict(dg=dict(azure_core=0.005, office=0.005, windows=0.0, gaming=0.0), dm=0.0,
                      gaming_m=0.12, capex=[154, 195],
                      azure_g=[0.70, 0.48, 0.36, 0.28, 0.22, 0.17, 0.13, 0.10, 0.08, 0.06],
                      revshare=[5.5, 8.5, 12, 15, 18, 20, 0, 0, 0, 0],
                      copilot=[11, 17, 25, 34, 43, 52, 60, 67, 73, 78],
                      drift=0.01, erosion=0.10, u_max=0.92, econ_life=5, residual=0.07,
                      mai=[5, 6, 6.5, 7, 7.3, 7.6, 8, 8.4, 8.8, 9.2], train_g=0.0, int_decl=0.05),
    "base": dict(dg=dict(azure_core=0.0, office=0.0, windows=0.0, gaming=0.0), dm=0.0,
                 gaming_m=0.12, capex=[154, 175, 185, 190, 190],
                 azure_g=[0.65, 0.45, 0.32, 0.24, 0.18, 0.14, 0.11, 0.09, 0.07, 0.06],
                 revshare=[5.5, 8, 11, 14, 17, 19, 0, 0, 0, 0],
                 copilot=[12, 18, 25, 32, 39, 45, 50, 54, 58, 62],
                 drift=0.0, erosion=0.12, u_max=0.92, econ_life=5, residual=0.05,
                 mai=[5, 6, 6.3, 6.6, 6.9, 7.2, 7.6, 8, 8.4, 8.8], train_g=-0.05, int_decl=0.05),
    "bear_lite": dict(dg=dict(azure_core=-0.01, office=-0.015, windows=-0.01, gaming=-0.01), dm=-0.01,
                      gaming_m=0.08, capex=[154, 160, 150],
                      azure_g=[0.55, 0.28, 0.15, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04],
                      revshare=[5, 6.5, 8, 9, 10, 10, 0, 0, 0, 0],
                      copilot=[10, 13, 17, 21, 25, 28, 31, 34, 36, 38],
                      drift=-0.03, erosion=0.16, u_max=0.90, econ_life=4, residual=0.03,
                      mai=[5, 5, 4.5, 4.5, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0], train_g=-0.10, int_decl=0.03),
    "bear": dict(dg=dict(azure_core=-0.025, office=-0.03, windows=-0.03, gaming=-0.02), dm=-0.02,
                 gaming_m=0.05, capex=[154, 125, 100],
                 azure_g=[0.45, 0.10, -0.08, -0.06, 0.02, 0.03, 0.03, 0.03, 0.03, 0.03],
                 revshare=[4.5, 5, 5, 4, 3, 0, 0, 0, 0, 0],
                 copilot=[9, 11, 13, 15, 17, 18, 19, 20, 21, 22],
                 drift=-0.06, erosion=0.22, u_max=0.88, econ_life=4, residual=0.02,
                 mai=[5, 4, 3.5, 3.5, 3.5, 3.5, 3.6, 3.7, 3.8, 3.9], train_g=-0.15, int_decl=0.03),
}


def _msft_ai_program(scn, k, yield_=1.0, lease_markup=None):
    p = MSFT_SCN[scn]
    years = list(range(2022, 2037))
    wacc = MSFT["wacc"] + k["wacc_shift"]
    prem = MSFT["ai_premium"] if k["ai_premium"] is None else k["ai_premium"]
    g_term = MSFT["g_term"] if k["g_term"] is None else k["g_term"]

    az = dict(MSFT["azure_ai_hist"])
    r = az[2026]
    for i, y in enumerate(range(2027, 2037)):
        r *= 1 + p["azure_g"][i]
        az[y] = r
    az = _scale_growth(az, 2026, k["ai_rev_scale"] * k["azure_scale"])
    az = _delay(az, 2026, k["delay"])
    if k["openai_shortfall"]:
        az = {y: (v * (1 - k["openai_shortfall"]) if y >= 2028 else v) for y, v in az.items()}

    cp = dict(MSFT["firstparty_hist"])
    cp.update(_path(2027, p["copilot"]))
    cp = _scale_growth(cp, 2026, k["ai_rev_scale"] * k["copilot_scale"])
    cp = _delay(cp, 2026, k["delay"])

    rs = dict(MSFT["revshare_hist"])
    rs.update(_path(2027, p["revshare"]))
    if not k["revshare_on"]:
        rs = {y: (0.0 if y >= 2027 else v) for y, v in rs.items()}

    mai = dict(MSFT["mai_opex_hist"])
    mai.update(_path(2027, p["mai"]))

    alloc = {y: MSFT["alloc"].get(y, MSFT["alloc_fwd"]) for y in years}
    drift = p["drift"] if k["yield_drift"] is None else k["yield_drift"]
    s_az = Stream("Azure AI infrastructure (incl. OpenAI)", "capacity",
                  {y: a[0] for y, a in alloc.items()}, MSFT["alloc_fwd"][0],
                  revenue=az, var_cost=max(0.0, 0.12 + k["var_cost_shift"]),
                  yield_=yield_, yield_drift=drift,
                  erosion=p["erosion"] if k["erosion"] is None else k["erosion"],
                  u_max=p["u_max"] if k["u_max"] is None else k["u_max"], u_target=0.85,
                  lease_opex=MSFT["lease_opex"],
                  lease_markup=MSFT["lease_markup"] if lease_markup is None else lease_markup)
    s_rs = Stream("OpenAI revenue share", "exogenous", {y: 0.0 for y in years}, 0.0,
                  revenue=rs, var_cost=0.0)   # no compute: pure royalty-like stream
    s_cp = Stream("First-party AI apps (Copilot, GitHub, agents)", "exogenous",
                  {y: a[1] for y, a in alloc.items()}, MSFT["alloc_fwd"][1],
                  revenue=cp, var_cost=max(0.0, 0.20 + k["var_cost_shift"]), internal_util=0.80,
                  intensity_decline=p["int_decl"])
    s_mai = Stream("MAI models & training", "cost", {y: a[2] for y, a in alloc.items()},
                   MSFT["alloc_fwd"][2], fixed_opex=mai,
                   post_growth={y: (p["train_g"] if k["train_g"] is None else k["train_g"])
                                for y in range(2027, 2037)})
    capex, explicit_end = _capex_path(MSFT["ai_capex_hist"], p["capex"], 2027,
                                      k["capex_scale"], k["capex_extend"])
    assets = Assets(accel=0.45, network=0.10, facility=0.42, land=0.03,   # [G] ~half long-lived
                    book_life_equip=MSFT["book_life"] if k["book_life"] is None else k["book_life"],
                    book_life_fac=MSFT["fac_book_life"],
                    econ_life=p["econ_life"] if k["econ_life"] is None else int(k["econ_life"]),
                    residual=p["residual"] if k["residual"] is None else k["residual"],
                    bonus=1.0 if k["bonus"] is None else k["bonus"])
    return AIProgram(years=years, first_forecast=2027, explicit_end=explicit_end, base_year=2026,
                     capex_total=capex, streams=[s_az, s_rs, s_cp, s_mai], assets=assets,
                     tax_rate=MSFT["tax"], hurdle=wacc + prem, g_term=g_term, val_offset=0.25,
                     terminal_ronic_override=k["terminal_ronic"])


def _calibrate_azure_yield(scn, k):
    """Solve the Azure AI revenue yield so that FY26 modelled revenue = estimated actual
    at 92% utilisation (Microsoft has said it is capacity constrained)."""
    prog = _msft_ai_program(scn, k, yield_=1.0, lease_markup=0.0)
    r = prog.run()
    i = r["years"].index(2026)
    S = r["streams"]["Azure AI infrastructure (incl. OpenAI)"]["potential"][i]
    target_pot = MSFT["azure_ai_fy26"] / 0.92 - MSFT["lease_opex"][2026] * MSFT["lease_markup"]
    return target_pot / S


def build_msft(scn="base", knobs=None, _calib=True):
    k = _k(knobs)
    p = MSFT_SCN[scn]
    fy = list(range(2027, 2037))
    wacc = MSFT["wacc"] + k["wacc_shift"]
    g_term = MSFT["g_term"] if k["g_term"] is None else k["g_term"]
    y0 = _calibrate_azure_yield(scn, k)
    prog = _msft_ai_program(scn, k, yield_=y0)
    prog.streams[0].fwd_yield_mult = (1 - k["openai_price_cut"]) * k["yield_mult"]

    m_ic, m_off = msft_core_margins0() if _calib else (0.45, 0.60)
    segs = []
    for key, sd in MSFT_SEG.items():
        g = [x + p["dg"][key] + k["core_g_shift"] for x in sd["g"]]
        if scn == "bear" and key == "windows":
            g[0] -= 0.04
        if key == "azure_core":
            m0 = m_ic
        elif key == "office":
            m0 = m_off
        else:
            m0 = sd["margin"]
        dm = p["dm"] + k["core_margin_shift"]
        if key == "gaming":
            margins = [m0 + (p["gaming_m"] - m0) * min(1.0, (i + 1) / 4) + k["core_margin_shift"]
                       for i in range(10)]
        else:
            margins = [m0 + dm * min(1.0, (i + 1) / 3) for i in range(10)]
        segs.append(Segment(sd["name"], sd["rev0"], g, margins, sd["capex"], sd["da"], MSFT["tax"],
                            sd["ic0"], min(g_term, 0.02) if key == "gaming" else g_term,
                            sd["ronic"], wacc, 0.25))
    stake_v = (MSFT["openai_val"][scn] * MSFT["openai_stake_pct"] * (1 - MSFT["stake_haircut"])
               if k["stake_value"] is None else k["stake_value"])
    comp = Company("Microsoft", MSFT["price"], MSFT["shares"], MSFT["net_debt"],
                   {"OpenAI stake (haircut)": stake_v}, segs, prog, MSFT["tax"], fy,
                   other_income_after_tax=dict(MSFT["openai_eq_loss"]),
                   meta=dict(scenario=scn, knobs=k, core_margin0=(m_ic, m_off), azure_yield=y0))
    return comp


@lru_cache(maxsize=None)
def msft_core_margins0():
    c = build_msft("base", _calib=False)
    r = c.ai.run()
    i = r["years"].index(2026)
    st = r["streams"]
    ic_ai = sum(st[n]["ebit_book"][i] for n in ["Azure AI infrastructure (incl. OpenAI)",
                                                 "OpenAI revenue share", "MAI models & training"])
    cp_ai = st["First-party AI apps (Copilot, GitHub, agents)"]["ebit_book"][i]
    m_ic = (MSFT["ic_oi"] - ic_ai) / MSFT_SEG["azure_core"]["rev0"]
    m_off = (MSFT["pbp_oi"] - cp_ai) / MSFT_SEG["office"]["rev0"]
    return m_ic, m_off


def build(company, scn="base", knobs=None):
    return build_meta(scn, knobs) if company == "META" else build_msft(scn, knobs)
