"""
Inputs for the CEG / VST asset-based NAV model.

Every number here is either (a) sourced (see SOURCES keys / REPORT.md), or
(b) an explicit modelling assumption marked "ASSUMPTION" / "EST". Nothing is
back-solved from the share price: the market price is only used in the final
comparison step (nav_model.py -> market-implied solve).

Units: MW, $/MWh, $/MW-day, $/kW-yr, $bn. Prices in 2026 dollars unless noted.
"""

VALUATION_DATE = 2026.75          # 30-Sep-2026 (fractional year used for discounting)
FIRST_YEAR = 2027
INFLATION = 0.02                  # ASSUMPTION: long-run escalator for prices and costs
CASH_TAX_RATE = 0.20              # ASSUMPTION: effective cash tax on asset cash flow (21% fed + state, less depreciation shield)

# ---------------------------------------------------------------------------
# Market data (as of late Sep-2026)
# ---------------------------------------------------------------------------
MARKET = {
    "CEG": {"price": 263.93, "price_date": "2026-09-22", "shares_mm": 354.307},  # shares: 10-Q cover, 31-Jul-2026
    "VST": {"price": 138.76, "price_date": "2026-09-25", "shares_mm": 336.0},    # ~336mm as of 3-Aug-2026 (Q2 release)
}

# ---------------------------------------------------------------------------
# Power & gas price deck
# ---------------------------------------------------------------------------
# Liquid forward years (nominal $/MWh, around-the-clock). PJM West ATC is DERIVED from
# on-peak forwards reported 8-Sep-2026 (Cal-27 $83.90, Cal-28 $85.35, Cal-29 $81.50) using an
# ATC/on-peak ratio of ~0.86 (EST). ERCOT North ATC: EST from EIA STEO reference ($47.39 for 2027)
# and reported "forwards above $50" for 2027-28.
FORWARD_ATC = {
    "PJMW":  {2027: 72.0, 2028: 73.0, 2029: 70.0},
    "ERCOT": {2027: 49.0, 2028: 51.0, 2029: 52.0},
}
# Other hubs priced as a ratio to PJM West (EST, reflects typical basis):
HUB_RATIO_TO_PJMW = {
    "PJMW": 1.00,   # PJM West / eastern PJM nuclear (Limerick, Peach Bottom, Calvert, Salem, Crane, Beaver Valley)
    "PJMA": 0.97,   # ATSI zone (Perry, Davis-Besse)
    "NIHUB": 0.85,  # PJM Northern Illinois hub (ComEd nuclear: Byron, Braidwood, LaSalle, Dresden, Quad Cities)
    "MISO": 0.83,   # Clinton (MISO Zone 4)
    "NY": 0.90,     # NYISO upstate (Nine Mile, Ginna, FitzPatrick)
    "NE": 1.08,     # ISO-NE Mass Hub
    "WEST": 0.92,   # CAISO NP15/SP15
}
# ERCOT is modelled on its own gas/heat-rate basis.

HENRY_HUB_REAL = {2027: 3.90, 2028: 3.90}   # 2026$/MMBtu; EIA STEO projects ~$4.60 for 2027, prompt was $2.79 in Sep-26 -> ASSUMPTION midpoint
HENRY_HUB_LR_REAL = 4.00                   # ASSUMPTION long-run real
GAS_BASIS = {"PJMW": -0.35, "PJMA": -0.35, "NIHUB": -0.25, "MISO": -0.20, "NY": 0.00,
             "NE": 1.40, "WEST": 0.60, "ERCOT": -0.15}   # EST annual-average basis to Henry Hub

# PJM capacity (RTO clearing price, $/MW-day, nominal). Delivery years run Jun-May.
PJM_CAPACITY_KNOWN = {"2026/27": 329.17, "2027/28": 333.44, "2028/29": 325.00}   # 28/29 cleared at the cap; uncapped would be $554.72
# Calendar-year blend (5/12 of prior DY + 7/12 of new DY)
PJM_CAPACITY_CY = {2027: 5/12*329.17 + 7/12*333.44, 2028: 5/12*333.44 + 7/12*325.00}

# Capacity accreditation (share of nameplate paid capacity revenue). EST from PJM ELCC class ratings.
ACCREDITATION = {"nuclear": 0.95, "ccgt": 0.78, "peaker": 0.60, "coal": 0.83, "hydro": 0.70, "geothermal": 0.90}

# ---------------------------------------------------------------------------
# AI / data-center demand scenarios
# ---------------------------------------------------------------------------
# Demand anchors (US data-center consumption, TWh):
#   2023 actual ~176 TWh (4.4% of US load, LBNL Dec-2024)
#   LBNL 2028: 325-580 TWh; EPRI 2030: 380-790 TWh (9-17%); BNEF (Jul-2026): ~12% by 2030, ~20% by 2035
#   PJM 2026 load forecast: +32 GW peak 2024->2030, of which ~30 GW data centers; peak 222 GW by 2036
#
# Mapping demand -> prices is a JUDGEMENT, bounded by two economic anchors:
#   (1) Liquid forwards / capacity auctions already clearing at the cap (2027-2029), and
#   (2) the cost of new entry. A new CCGT at ~$2,200-2,500/kW needs roughly $58-62/MWh PJM ATC
#       (with ~$230/MW-day capacity) to earn a 9% return (see nav_model.new_entrant_breakeven).
#       Prices can only stay above that level while new supply is physically constrained
#       (turbine backlog, interconnection queue, gas pipelines, permitting).
SCENARIOS = {
    "Low": {
        "desc": "AI capex cycle cools / efficiency gains; announced load largely does not materialise",
        "us_dc_twh_2030": 300, "us_dc_twh_2035": 380, "pjm_dc_gw_2030": 12,
        "ihr_pjm": 13.0, "ihr_ercot": 10.5,           # market implied heat rate (MMBtu/MWh)
        "pjm_cap": 120.0, "other_cap": 60.0, "west_cap": 150.0,  # $/MW-day, 2026$
        "scarcity_mult": 2.0,
    },
    "Base": {
        "desc": "Data centers ~10% of US load by 2030 (mid of LBNL/EPRI); new gas arrives ~2030 and caps prices near new-entry cost",
        "us_dc_twh_2030": 450, "us_dc_twh_2035": 700, "pjm_dc_gw_2030": 22,
        "ihr_pjm": 16.5, "ihr_ercot": 13.0,
        "pjm_cap": 230.0, "other_cap": 110.0, "west_cap": 220.0,
        "scarcity_mult": 2.5,
    },
    "High": {
        "desc": "~14% of US load by 2030 (EPRI-high-ish); supply chain constrains new build -> prices persistently above new-entry cost",
        "us_dc_twh_2030": 650, "us_dc_twh_2035": 1000, "pjm_dc_gw_2030": 30,
        "ihr_pjm": 20.0, "ihr_ercot": 16.0,
        "pjm_cap": 325.0, "other_cap": 170.0, "west_cap": 280.0,
        "scarcity_mult": 3.0,
    },
    "Extreme": {
        "desc": "~18% of US load by 2030 (above EPRI high); chronic shortage, PJM cap lifted, scarcity pricing for a decade",
        "us_dc_twh_2030": 850, "us_dc_twh_2035": 1400, "pjm_dc_gw_2030": 40,
        "ihr_pjm": 25.0, "ihr_ercot": 21.0,
        "pjm_cap": 475.0, "other_cap": 250.0, "west_cap": 350.0,
        "scarcity_mult": 3.6,
    },
}
SCENARIO_ORDER = ["Low", "Base", "High", "Extreme"]
US_TOTAL_LOAD_TWH_2024 = 4100      # EST (EIA retail sales + direct use)
NON_DC_LOAD_GROWTH = 0.01          # ASSUMPTION

# ---------------------------------------------------------------------------
# Technology operating assumptions (2026$)
# ---------------------------------------------------------------------------
TECH = {
    # NEI "Nuclear Costs in Context" (Aug-2026): 2025 total generating cost $36.46/MWh avg; multi-unit $34.36; single-unit $45.77
    "nuclear":    {"cf": 0.935, "cost_mwh": 35.5, "cost_esc": 0.025, "capture": 0.99, "disc": 0.080, "disc_contract": 0.0675},
    "ccgt":       {"cf": 0.55, "heat_rate": 7.2, "vom": 3.5, "fom_kw": 32.0, "capex_kw": 12.0, "disc": 0.095},
    "peaker":     {"cf": 0.06, "heat_rate": 10.5, "vom": 5.0, "fom_kw": 18.0, "capex_kw": 5.0, "disc": 0.100},
    "coal":       {"cf": 0.50, "heat_rate": 10.4, "fuel": 2.30, "vom": 4.5, "fom_kw": 50.0, "capex_kw": 15.0, "capture": 1.02, "disc": 0.120},
    "hydro":      {"cf": 0.20, "fom_kw": 40.0, "capture": 1.30, "disc": 0.080},
    "geothermal": {"cf": 0.85, "cost_mwh": 38.0, "disc": 0.075},
}
# Region-specific CCGT capacity factors and price capture vs ATC (EST). Dispatchable plants capture a premium to ATC
# where solar depresses midday prices (ERCOT, CAISO); flat baseload nuclear captures slightly less in ERCOT.
CCGT_CF = {"ERCOT": 0.55, "PJMW": 0.50, "PJMA": 0.50, "NE": 0.45, "NY": 0.45, "WEST": 0.45}
CCGT_CAPTURE = {"ERCOT": 1.20, "WEST": 1.15, "PJMW": 1.02, "PJMA": 1.02, "NE": 1.05, "NY": 1.05}
NUCLEAR_CAPTURE = {"ERCOT": 0.95}          # default TECH["nuclear"]["capture"] elsewhere
FUEL_ADDER = 0.30                          # $/MMBtu delivered-fuel adder for gas plants (transport, winter fuel/power mismatch) - EST

# Section 45U nuclear PTC (through 2032). Max credit $15/MWh and $25/MWh gross-receipts threshold
# in 2024$, inflation-adjusted; credit reduced by 80% of gross receipts above threshold.
PTC45U = {"credit": 15.0, "threshold": 25.0, "base_year": 2024, "last_year": 2032}

# ---------------------------------------------------------------------------
# Asset registers (owned MW, pro forma for announced transactions)
# ---------------------------------------------------------------------------
# contracts: list of dicts {mw: {year: MW} or float, start, end, price (nominal $/MWh, bundled), esc}
# PPA prices are NOT disclosed; figures are analyst estimates (Clinton ~$70-88, Crane ~$98-115,
# Talen/AWS ~$80) -> ASSUMPTION, see sensitivity.

CEG_ASSETS = [
    # --- Nuclear (~22 GW owned share per CEG; plant split EST from ownership shares) ---
    {"name": "Nuclear - PJM East (Limerick, Peach Bottom 50%, Calvert Cliffs, Salem 42.6%)", "tech": "nuclear", "hub": "PJMW",
     "mw": 6430, "start": 2027, "end": 2055},
    {"name": "Nuclear - PJM ComEd (Byron, Braidwood, LaSalle, Dresden, Quad Cities 75%)", "tech": "nuclear", "hub": "NIHUB",
     "mw": 10300, "start": 2027, "end": 2055,
     "contracts": [{"mw": 920, "start": 2027, "end": 2046, "price": 85.0, "esc": 0.0}]},   # 920 MW new 15-20yr PPAs (Q2-26); price ASSUMPTION
    {"name": "Nuclear - Clinton (MISO) - Meta 20-yr PPA", "tech": "nuclear", "hub": "MISO",
     "mw": 1080, "start": 2027, "end": 2055,
     "contracts": [{"mw": 1080, "start": 2027, "end": 2046, "price": 80.0, "esc": 0.0}]},
    {"name": "Nuclear - New York (Nine Mile Pt, Ginna, FitzPatrick)", "tech": "nuclear", "hub": "NY",
     "mw": 3000, "start": 2027, "end": 2055, "zec": {"price": 18.0, "end": 2029}},       # NY ZEC ~$18/MWh EST
    {"name": "Nuclear - South Texas Project 44% (ERCOT)", "tech": "nuclear", "hub": "ERCOT",
     "mw": 1165, "start": 2027, "end": 2055},
    {"name": "Nuclear - Crane restart (TMI-1) - Microsoft 20-yr PPA", "tech": "nuclear", "hub": "PJMW",
     "mw": 835, "start": 2028, "end": 2054, "capex": {2027: 0.5},                         # remaining restart spend EST $0.5bn
     "contracts": [{"mw": 835, "start": 2028, "end": 2047, "price": 100.0, "esc": 0.0}]},
    # --- Hydro / renewables (legacy CEG) ---
    {"name": "Hydro - Conowingo + Muddy Run pumped storage (PJM)", "tech": "hydro", "hub": "PJMW",
     "mw": 1642, "start": 2027, "end": 2055},
    {"name": "Wind & solar (legacy CEG, ~1.9 GW)", "tech": "renewable", "hub": "PJMW", "mw": 1900, "usd_per_kw": 450},
    # --- Legacy CEG gas/oil ---
    {"name": "Gas - ERCOT CCGT (Colorado Bend II, Wolf Hollow II, etc.)", "tech": "ccgt", "hub": "ERCOT",
     "mw": 2300, "start": 2027, "end": 2050},
    {"name": "Gas/oil - ERCOT peakers & steam (legacy CEG)", "tech": "peaker", "hub": "ERCOT",
     "mw": 1277, "start": 2027, "end": 2038},
    {"name": "Gas/oil - PJM/NE/other peakers & oil (legacy CEG)", "tech": "peaker", "hub": "PJMW",
     "mw": 2582, "start": 2027, "end": 2038},
    # --- Calpine (retained after DOJ/FERC divestitures; split EST) ---
    {"name": "Calpine - ERCOT CCGT (Deer Park, Freestone, Channel, Baytown, etc.)", "tech": "ccgt", "hub": "ERCOT",
     "mw": 7000, "start": 2027, "end": 2045},
    {"name": "Calpine - ERCOT peakers/cogen", "tech": "peaker", "hub": "ERCOT", "mw": 400, "start": 2027, "end": 2040},
    {"name": "Calpine - West CCGT (CAISO)", "tech": "ccgt", "hub": "WEST", "mw": 5000, "start": 2027, "end": 2045},
    {"name": "Calpine - West peakers", "tech": "peaker", "hub": "WEST", "mw": 800, "start": 2027, "end": 2040},
    {"name": "Calpine - The Geysers geothermal", "tech": "geothermal", "hub": "WEST", "mw": 750, "start": 2027, "end": 2055,
     "contracts": [{"mw": 750, "start": 2027, "end": 2035, "price": 85.0, "esc": 0.0}]},    # CCA contracts, price EST
    {"name": "Calpine - East CCGT (NE/NY/PJM residual/SE)", "tech": "ccgt", "hub": "NE", "mw": 2900, "start": 2027, "end": 2045},
    {"name": "RISEC (609 MW CCGT, ISO-NE) - pending, $715mm", "tech": "ccgt", "hub": "NE", "mw": 609, "start": 2027, "end": 2050},
]

VST_ASSETS = [
    # --- Nuclear (6,448 MW per 10-K) ---
    {"name": "Nuclear - Comanche Peak (ERCOT) - 1,200 MW 20-yr PPA", "tech": "nuclear", "hub": "ERCOT",
     "mw": 2400, "start": 2027, "end": 2053,
     "contracts": [{"mw": {2028: 300, 2029: 500, 2030: 700, 2031: 900}, "mw_full": 1200, "start": 2028, "end": 2047,
                    "price": 80.0, "esc": 0.0}]},
    {"name": "Nuclear - Perry + Davis-Besse (PJM ATSI) - Meta 20-yr PPAs", "tech": "nuclear", "hub": "PJMA",
     "mw": 2176, "start": 2027, "end": 2055,
     "contracts": [{"mw": {2027: 1100}, "mw_full": 2176, "start": 2027, "end": 2047, "price": 85.0, "esc": 0.0}]},
    {"name": "Nuclear - Beaver Valley (PJM)", "tech": "nuclear", "hub": "PJMW", "mw": 1872, "start": 2027, "end": 2055},
    # --- Gas (26,989 MW: 22,167 CCGT + 4,822 peakers; regional split EST) ---
    {"name": "Gas - ERCOT CCGT", "tech": "ccgt", "hub": "ERCOT", "mw": 9500, "start": 2027, "end": 2045},
    {"name": "Gas - ERCOT peakers", "tech": "peaker", "hub": "ERCOT", "mw": 2300, "start": 2027, "end": 2040},
    {"name": "Gas - PJM CCGT (incl. Lotus)", "tech": "ccgt", "hub": "PJMW", "mw": 8500, "start": 2027, "end": 2045},
    {"name": "Gas - NY/NE CCGT", "tech": "ccgt", "hub": "NE", "mw": 3167, "start": 2027, "end": 2045},
    {"name": "Gas - West CCGT (CAISO)", "tech": "ccgt", "hub": "WEST", "mw": 1000, "start": 2027, "end": 2040},
    {"name": "Gas/oil - East peakers", "tech": "peaker", "hub": "PJMW", "mw": 2709, "start": 2027, "end": 2038},
    # --- Coal (8,743 MW) ---
    {"name": "Coal - ERCOT (Martin Lake, Oak Grove, Coleto Creek)", "tech": "coal", "hub": "ERCOT", "mw": 4500, "start": 2027, "end": 2035},
    {"name": "Coal - IL/OH (Baldwin, Kincaid, Newton, Miami Fort) - retiring ~2027", "tech": "coal", "hub": "PJMW", "mw": 4243, "start": 2027, "end": 2027},
    # --- Renewables / storage (1,274 MW incl. Moss Landing battery) ---
    {"name": "Solar & batteries (Vistra Zero)", "tech": "renewable", "hub": "ERCOT", "mw": 1274, "usd_per_kw": 700},
    # --- Pending: Cogentrix (5.5 GW modern gas; closing late-2026) ---
    {"name": "Cogentrix (pending) - modern CCGT, PJM", "tech": "ccgt", "hub": "PJMW", "mw": 3850, "start": 2027, "end": 2050, "heat_rate": 6.9},
    {"name": "Cogentrix (pending) - modern CCGT, NE", "tech": "ccgt", "hub": "NE", "mw": 1650, "start": 2027, "end": 2050, "heat_rate": 6.9},
]

# ---------------------------------------------------------------------------
# Claims on the assets ($bn). Pro forma for announced/pending transactions.
# ---------------------------------------------------------------------------
CEG_CLAIMS = [
    ("Long-term debt incl. current (30-Jun-26; $14.6bn CEG Gen + $5.0bn Calpine)", 19.60),
    ("Cash (30-Jun-26)", -0.697),
    ("Proceeds: 4.4 GW PJM sale to LS Power (pending)", -5.00),
    ("Proceeds: Brazos Valley (606 MW ERCOT CCGT) sale to LS Power (pending; final DOJ divestiture)", -0.86),
    ("Purchase: RISEC from Shell (pending)", 0.715),
    ("Pension/OPEB net underfunding - EST", 0.90),
    ("Noncontrolling interests - EST", 0.30),
    ("Nuclear decommissioning: NDT assumed to cover ARO (net zero) - ASSUMPTION", 0.00),
]
VST_CLAIMS = [
    ("Long-term debt incl. current (30-Jun-26)", 19.595),
    ("Cash (30-Jun-26)", -0.435),
    ("Cogentrix: cash consideration (pending)", 2.30),
    ("Cogentrix: assumed debt (pending)", 1.50),
    ("Preferred stock (Series A $1.0bn, B $1.0bn, C $0.476bn liquidation pref.)", 2.476),
    ("Tax receivable agreement - EST", 0.45),
    ("Vistra Vision buyout deferred payments remaining - EST", 0.40),
    ("Pension/OPEB net - EST", 0.30),
    ("Nuclear decommissioning: NDT assumed to cover ARO (net zero) - ASSUMPTION", 0.00),
]
EXTRA_SHARES_MM = {"CEG": 0.0, "VST": 5.0}   # 5mm VST shares to Cogentrix sellers

# Unallocated corporate overhead (pre-tax, 2026$ $mm/yr) - EST, capitalised in NAV
CORP_OVERHEAD_MM = {"CEG": 450.0, "VST": 350.0}

# Non-generation platform (retail / commercial). Earnings-based, therefore shown SEPARATELY.
# VST Retail segment adj. EBITDA 2025 = $1,463mm (reported). CEG does not report retail separately -> EST $1,000mm.
PLATFORM = {"CEG": {"ebitda_mm": 1000.0, "multiple": 6.0, "note": "EST - CEG does not disclose retail EBITDA"},
            "VST": {"ebitda_mm": 1463.0, "multiple": 6.0, "note": "Retail segment adj. EBITDA FY2025 (reported)"}}

# Transaction comparables ($/kW) for cross-checking
COMPS = [
    ("CEG -> LS Power: 4.4 GW PJM gas (Mar-2026)", 1142, "gas"),
    ("Shell -> CEG: RISEC 609 MW CCGT ISO-NE (Sep-2026)", 715e6 / 609e3, "gas"),
    ("Vistra <- Cogentrix: 5.5 GW gas (Dec-2025 signing)", (2.3e9 + 1.5e9 + 5e6 * 185) / 5.5e6, "gas"),
    ("Vistra <- Lotus: 2.6 GW gas (Oct-2025)", 1.9e9 / 2.6e6, "gas"),
    ("US gas M&A average H1-2026 (Deloitte)", 1468, "gas"),
    ("New-build CCGT cost 2025-26 (GridLab)", 2350, "gas"),
    ("CEG -> LS Power: Brazos Valley 606 MW ERCOT CCGT (Aug-2026)", 860e6 / 606e3, "gas"),
    ("CEG <- Calpine: ~26 GW (Jan-2026 close, $26.6bn EV)", 26.6e9 / 26.0e6, "gas"),
]

# Private-market lens: mark gas at observed transaction $/kW (by hub) instead of modelled cash flows.
COMP_MARK_CCGT = {"ERCOT": 860e6 / 606e3,    # Brazos Valley (Aug-2026)
                  "PJMW": 1142,              # LS Power PJM package (Mar-2026)
                  "NE": 715e6 / 609e3,       # RISEC (Sep-2026)
                  "WEST": 26.6e9 / 26.0e6}   # Calpine average EV/kW as proxy
COMP_MARK_PEAKER = 0.5 * 1142                 # ASSUMPTION: peakers at ~50% of CCGT $/kW
COMP_MARK_COGENTRIX = (2.3e9 + 1.5e9 + 5e6 * 185) / 5.5e6   # price Vistra agreed to pay

# Illustrative scenario weights (JUDGEMENT, not a forecast) used only for a probability-weighted NAV
SCENARIO_WEIGHTS = {"Low": 0.20, "Base": 0.45, "High": 0.25, "Extreme": 0.10}
