# CEG & VST — Asset-Based NAV Under AI / Data-Center Demand Scenarios

*Valuation date 30-Sep-2026. Prices: CEG $263.93 (22-Sep-26), VST $138.76 (25-Sep-26). All values in US$, long-run power prices in 2026 dollars.*
*The editable model is `outputs/CEG_VST_NAV_Model.xlsx`. The Python model (`nav_model.py` + `inputs.py`) regenerates the detailed tables and CSVs into `outputs/` when run.*

---

## 0. Bottom line

| | CEG | VST |
|---|---|---|
| Market cap / EV (pro forma) | $93.5bn / **$108.5bn** | $47.3bn / **$73.9bn** |
| EV per kW owned (pro forma MW) | **$2,171/kW** (49.97 GW) | **$1,504/kW** (49.1 GW) |
| **NAV/share — Low / Base / High / Extreme** (generation only) | $77 / **$173** / $270 / $415 | $1 / **$56** / $115 / $204 |
| NAV/share incl. retail platform (valued on earnings, shown separately) | $94 / **$190** / $287 / $432 | $27 / **$82** / $140 / $229 |
| Private-market view (gas marked at deal $/kW, rest at Base), incl. platform | $215 | $97 |
| Price vs Base NAV incl. platform | **+39%** | **+69%** |
| Long-run power price the stock price requires (vs Base) | **+$12–14/MWh** → PJM West ~$72–75 | **+$15–22/MWh** → PJM West ~$76–83, ERCOT ~$66–73 |
| Or, holding heat rates at Base: long-run Henry Hub required | $4.92–5.13 (Base $4.00) | $5.70–6.46 |
| **NAV + FCF generated:** value at end-2030 (cumulative FCF + forward NAV), Low / **Base** / High / Extreme | $128 / **$262** / $399 / $601 | $50 / **$130** / $214 / $342 |
| Implied annual return from today's price, Base / High | **−0.1% / +10.2%** | **−1.6% / +10.7%** |
| **Replacement cost + 5 yrs FCF**, nuclear rebuilt as new nuclear ($12,100/kW), Low / **Base** / High / Extreme | $405 / **$422** / $440 / $468 | $171 / **$184** / $198 / $220 |
| **Replacement cost + 5 yrs FCF**, nuclear replaced by new gas, Low / **Base** / High / Extreme | $177 / **$195** / $213 / $240 | $100 / **$113** / $127 / $148 |

1. **What the assets are worth today.** If long-run prices settle near the cost of building new gas plants (the Base case), the assets support **~$173–190/share for CEG** and **~$55–80/share for VST**. Both stocks trade well above that.
2. **What they could be worth with more AI demand.** The High case (data centers at ~14% of US load by 2030 and new supply held back) gives about CEG $270–287 and VST $115–140. That is roughly today's prices. The Extreme case (PJM's capacity price cap removed, a decade of shortage) gives CEG ~$415–432 and VST ~$205–230.
3. **What the market is paying for.** At today's prices, the market is not paying for the Base case. It is paying for something close to the **High case**: long-run PJM West prices of about **$72–83/MWh in 2026 dollars, held indefinitely**. That is $12–23/MWh above what a new gas plant needs to earn a return (~$60). A price above new-build cost can only last if new plants can't get built fast enough. The two stocks are therefore bets that **new supply stays constrained**, more than bets that AI demand keeps growing.
4. **CEG vs VST.** CEG's price needs less. Its nuclear fleet has long lives and low costs, and its debt is modest (~$15bn net claims against ~$81bn Base asset value). VST's price needs more, for two reasons:
   - **Leverage.** $26.6bn of debt, preferred stock and other claims means small changes in asset value swing the equity a lot. In the Low case VST's equity NAV is near zero.
   - **Fleet mix.** VST's fleet is mostly gas and coal. Their margins widen with scarcity, but they also compress most when new supply arrives.
5. **The biggest single driver is gas, not AI.** A $1/MMBtu change in long-run Henry Hub moves Base NAV from $93 to $253 for CEG and from $25 to $90 for VST. That swing is larger than the gap between Base and High. Nuclear value is effectively a claim on gas price × market heat rate, and AI demand acts mainly on the heat rate.

> In the terms of your framework: *"If long-run PJM prices are ~$75/MWh in 2026 dollars forever, the math says CEG is worth roughly its current price."* That is **not** my forecast. It is what has to be true for the price to be fair. §6 sets out why that is a demanding assumption.

---

## 1. Method (and what this is *not*)

- **This is not a company DCF.** Reported revenue, EPS and guidance are **not** inputs. Each asset group is valued as a standalone plant:
  - Revenue: MWh × captured price, plus capacity MW × capacity price, plus contracted PPA revenue, ZEC payments and the 45U nuclear tax credit.
  - Minus fuel, O&M and sustaining capex.
  - Taxed at a 20% cash rate, discounted at a rate set by each asset's risk, and run to the end of its licensed or assumed life with no terminal value.
- **Gross asset value (GAV)** is the sum of the asset values. From it I deduct capitalised corporate overhead and all debt-like claims. That gives equity NAV.
- **Cross-checks:**
  - Transaction comparables in $/kW (the private-market lens).
  - New-entrant economics: the price at which it pays to build a new CCGT, which caps long-run prices in any market that can still build.
- **Discount rates (after-tax, nominal):**
  - Merchant nuclear 8.0%; nuclear under long-term data-center PPA 6.75%.
  - CCGT 9.5%; peakers 10%; coal 12%; geothermal 7.5%; hydro 8%.
  - Corporate overhead 8.5%.
- **The share price enters only at the end:** in the comparison, and in a solver that finds the long-run power price (or gas price) the market is implicitly paying for.

---

## 2. Asset register (pro forma for announced transactions)

### CEG — ~50.0 GW
| Group | MW | Hub / notes |
|---|---|---|
| Nuclear, PJM East (Limerick, Peach Bottom 50%, Calvert Cliffs, Salem 42.6%) | 6,430 | PJM West |
| Nuclear, PJM ComEd (Byron, Braidwood, LaSalle, Dresden, Quad Cities 75%) | 10,300 | NI Hub (≈15% below West); 920 MW of new 15–20-yr PPAs (Q2-26) |
| Nuclear, Clinton (MISO) | 1,080 | Meta 20-yr PPA (est. ~$70–88/MWh) |
| Nuclear, New York (Nine Mile Pt, Ginna, FitzPatrick) | 3,000 | NY ZEC through 2029 (assumed) |
| Nuclear, South Texas Project 44% | 1,165 | ERCOT |
| Nuclear, Crane (TMI-1) restart | 835 | Microsoft 20-yr PPA (est. ~$98–115/MWh); ~$0.5bn remaining capex (est.) |
| Hydro: Conowingo + Muddy Run | 1,642 | PJM |
| Wind & solar (legacy) | 1,900 | Valued at $450/kW (older wind) |
| Gas, legacy ERCOT CCGT + peakers | 3,577 | |
| Gas/oil peakers, PJM/NE/other | 2,582 | |
| Calpine ERCOT CCGT + peakers | 7,400 | Includes Freestone (CyrusOne 380 MW, up to 760 MW deal) |
| Calpine West CCGT + peakers | 5,800 | CAISO |
| Calpine Geysers geothermal | 750 | Contracted with CCAs (price est.) |
| Calpine East CCGT + RISEC (pending, 609 MW) | 3,509 | ISO-NE / NY / SE |

*Excluded:* the 4.4 GW PJM package sold to LS Power ($5.0bn, $1,142/kW) and Brazos Valley (606 MW, $860mm, $1,419/kW). Both sales are pending, so their proceeds are credited against debt.

*Source for the totals:* the 10-K reports 31,676 MW at YE-2025 (pre-Calpine), of which ~22 GW is nuclear; Calpine brought ~26 GW; the combined company is ~55 GW before divestitures. **The split between plant groups is my estimate** built from ownership shares, because I could not open the filing tables directly (see §8).

### VST — ~49.1 GW (incl. Cogentrix, pending)
| Group | MW | Hub / notes |
|---|---|---|
| Nuclear, Comanche Peak | 2,400 | ERCOT; 1,200 MW 20-yr PPA, ramping from Q4-27 to 2032 (price undisclosed; $80 assumed) |
| Nuclear, Perry + Davis-Besse | 2,176 | PJM ATSI; Meta 20-yr PPAs, full delivery by end-2027 ($85 assumed). The +433 MW of uprates (2031–34) is **excluded** (capex unknown) |
| Nuclear, Beaver Valley | 1,872 | PJM (merchant). Beaver Valley supplies only part of the uprates |
| Gas CCGT (22,167 MW) | ERCOT 9,500 / PJM 8,500 / NY-NE 3,167 / West 1,000 | Regional split estimated |
| Gas peakers + oil (4,822 + 187 MW) | ERCOT 2,300 / East 2,709 | |
| Coal, ERCOT (Martin Lake, Oak Grove, Coleto Creek) | 4,500 | Retirement assumed 2035 |
| Coal, IL/OH (Baldwin, Kincaid, Newton, Miami Fort) | 4,243 | Retiring 2027–28 per WARN notices |
| Solar + batteries | 1,274 | Valued at $700/kW |
| Cogentrix (pending, late 2026) | 5,500 | Modern CCGTs; split assumed 70% PJM / 30% NE |

*Source for the totals:* the 10-K reports 43,641 MW at YE-2025 (gas 26,989, coal 8,743, nuclear 6,448, solar/battery 1,274, oil 187).

### Claims on the assets ($bn)
| | CEG | VST |
|---|---|---|
| Debt (30-Jun-26) | 19.60 | 19.60 |
| Cash | (0.70) | (0.44) |
| Pending deals | −5.00 LS Power, −0.86 Brazos Valley, +0.72 RISEC | +2.30 Cogentrix cash, +1.50 Cogentrix debt assumed |
| Preferred stock | — | 2.48 |
| Pension/OPEB, TRA, NCI, deferred payments (est.) | 1.20 | 1.15 |
| Nuclear decommissioning | Trust assumed to fund the obligation (net 0) | Same |
| **Net claims** | **15.0** | **26.6** |
| Shares (mm) | 354.3 (10-Q cover, 31-Jul-26) | 336 + 5 to Cogentrix sellers = 341 |

---

## 3. AI / data-center demand scenarios

**Demand anchors:**
- **Actual:** 2023 US data-center use was ~176 TWh, 4.4% of US load (LBNL).
- **LBNL:** 325–580 TWh by 2028.
- **EPRI:** 380–790 TWh by 2030, or 9–17% of US load.
- **BNEF (Jul-2026):** ~12% of US load by 2030 and ~20% by 2035.
- **PJM 2026 load forecast:** +32 GW of peak load from 2024 to 2030, ~30 GW of it data centers; peak ~222 GW by 2036.
- **Range of published estimates:** 2030 US data-center forecasts run from ~200 to >1,050 TWh.

**Supply-side anchors:**
- PJM's 2028/29 capacity auction **cleared at its $325/MW-day cap**. It came in 6.8 GW (5.6 points of reserve margin) short of the reliability requirement, and the uncapped price would have been $554.72.
- PJM West on-peak forwards are ~$84–85/MWh for 2027–28 and $81.5 for 2029.
- ERCOT is soft. Solar output is doubling and batteries are heading to ~37 GW by 2027. CEG flagged "ERCOT weakness" in Q2.

### Scenario deck
| Scenario | US DC TWh 2030 | DC share of US load 2030 | US DC TWh 2035 | Extra PJM DC GW by 2030 | PJM West ATC (LR, 2026$) | NI Hub | ERCOT North | PJM capacity ($/MW-day) |
|---|---|---|---|---|---|---|---|---|
| Low | 300 | 7% | 380 | 12 | $47 | $40 | $40 | 120 |
| **Base** | 450 | 10% | 700 | 22 | **$60** | $51 | $50 | 230 |
| High | 650 | 14% | 1,000 | 30 | $73 | $62 | $62 | 325 |
| Extreme | 850 | 17% | 1,400 | 40 | $91 | $78 | $81 | 475 |

In every scenario, 2027–28 are marked to forwards and the capacity prices already set by auction (PJM West ATC ~$72–73, capacity ~$330/MW-day). 2029 is a 50/50 blend of forward and long run. The long-run level applies from 2030.

**How demand turns into prices. This step is a judgment, not an estimate, so I've made it explicit:**
- Power price = market heat rate × regional gas price. AI demand moves the **heat rate** and the **capacity price**:
  - Low: PJM heat rate 13.0.
  - Base: 16.5, which is roughly the heat rate at which a new CCGT breaks even.
  - High: 20.0, about where 2027–28 forwards are today.
  - Extreme: 25.0.
- **The ceiling is the cost of new entry.** A new CCGT at $2,350/kW (GridLab 2025–26 cost data), 8% real return and $230/MW-day capacity needs **~$60/MWh PJM West ATC**. At $2,000/kW it needs $54; at $2,800/kW, $67.
- The Base case assumes demand is met at that cost. High and Extreme assume supply is held back for years by turbine backlogs, the interconnection queue and gas pipeline limits. In any market that can still build, prices well above ~$60–67 attract new plants. So High and Extreme are **supply-constraint** scenarios as much as demand scenarios.
- **Flag:** PJM's historical heat rate (2015–24) was roughly 10–13 (approximate). My Base (16.5) is already above history, and High/Extreme are far above it. Today's forwards (~20) assume the current tightness lasts.

---

## 4. Results — NAV by scenario

### CEG ($bn unless noted)
| | Low | **Base** | High | Extreme |
|---|---|---|---|---|
| Nuclear (22.8 GW) | 34.5 | **58.5** | 82.2 | 116.9 |
| — $/kW | 1,514 | **2,564** | 3,603 | 5,126 |
| Gas CCGT + peakers (22.9 GW) | 7.9 | **16.4** | 25.9 | 40.2 |
| Hydro, geothermal, renewables | 4.6 | **6.1** | 7.5 | 9.6 |
| **Gross asset value** | 47.0 | **81.0** | 115.5 | 166.7 |
| Less overhead / net claims | (4.9) / (15.0) | (4.9) / (15.0) | (4.9) / (15.0) | (4.9) / (15.0) |
| **Equity NAV** | 27.2 | **61.2** | 95.7 | 146.9 |
| **NAV/share (generation)** | **$77** | **$173** | **$270** | **$415** |
| NAV/share incl. platform (+$6.0bn) | $94 | $190 | $287 | $432 |
| Price vs NAV incl. platform | +182% | +39% | −8% | −39% |

### VST ($bn unless noted)
| | Low | **Base** | High | Extreme |
|---|---|---|---|---|
| Nuclear (6.4 GW) | 13.0 | **16.7** | 20.7 | 26.9 |
| — $/kW | 2,012 | **2,592** | 3,216 | 4,166 |
| Gas CCGT + peakers (32.7 GW incl. Cogentrix) | 16.1 | **30.6** | 45.6 | 68.6 |
| Coal (8.7 GW) | 0.9 | **1.4** | 2.1 | 3.3 |
| Solar/storage | 0.8 | **0.9** | 1.0 | 1.1 |
| **Gross asset value** | 30.8 | **49.6** | 69.4 | 99.8 |
| Less overhead / net claims | (3.8) / (26.6) | (3.8) / (26.6) | (3.8) / (26.6) | (3.8) / (26.6) |
| **Equity NAV** | 0.5 | **19.2** | 39.1 | 69.4 |
| **NAV/share (generation)** | **$1** | **$56** | **$115** | **$204** |
| NAV/share incl. platform (+$8.8bn) | $27 | $82 | $140 | $229 |
| Price vs NAV incl. platform | +412% | +69% | −1% | −39% |

**How the two companies are exposed to AI demand:**

| | CEG | VST |
|---|---|---|
| Change in GAV per extra $1/MWh long-run price | ~$2.3bn (~$6.4/share) | ~$1.3bn (~$3.7/share) |
| Leverage (net claims / Base GAV) | ~18% | ~54% |
| Share of NAV already locked in by long-term contracts | ~12% of nuclear MW, at ~$80–100/MWh. This protects Low but gives up upside | ~52% of nuclear MW, at ~$80–85/MWh (assumed). Protects Low; caps upside on those MW |

---

## 4b. Revenue streams — where the asset value comes from

Every asset's cash flow is built from separate revenue and cost lines. Each line is discounted at that asset's rate, and the lines add up exactly to the NAV above. Figures are after-tax PV in $bn; "share" is each stream's share of total revenue PV before costs.

### CEG
| Stream | Low | **Base** | High | Extreme | Base share | Low→Extreme |
|---|---|---|---|---|---|---|
| Merchant energy sales | 125.8 | **151.8** | 178.8 | 218.8 | 77% | +93.0 |
| Capacity payments (PJM / NY / NE / MISO / CA RA) | 14.5 | **22.7** | 30.1 | 41.3 | 12% | +26.8 |
| Long-term PPAs (Meta-Clinton, Microsoft-Crane, 920 MW new deals, Geysers) | 19.9 | **19.9** | 19.9 | 19.9 | 10% | 0 |
| NY ZEC | 0.9 | **0.9** | 0.9 | 0.9 | <1% | 0 |
| 45U nuclear tax credit | 0.2 | **0.0** | 0.0 | 0.0 | 0% | −0.2 |
| Renewables (valued at $/kW) | 0.8 | **0.9** | 0.9 | 1.0 | <1% | +0.2 |
| Nuclear all-in cost (fuel, O&M, capex) | (79.3) | **(79.3)** | (79.3) | (79.3) | | |
| Gas fuel + variable O&M | (24.8) | **(24.8)** | (24.8) | (24.8) | | |
| Fixed O&M + capex (non-nuclear) | (10.7) | **(10.7)** | (10.7) | (10.7) | | |
| Crane restart capex | (0.4) | **(0.4)** | (0.4) | (0.4) | | |
| **Gross asset value** | 47.0 | **81.0** | 115.5 | 166.7 | | |
| Contracted + policy share of revenue | 13% | **11%** | 9% | 7% | | |

### VST
| Stream | Low | **Base** | High | Extreme | Base share | Low→Extreme |
|---|---|---|---|---|---|---|
| Merchant energy sales | 77.6 | **92.3** | 108.2 | 132.5 | 74% | +55.0 |
| Capacity payments | 8.2 | **12.5** | 16.4 | 22.4 | 10% | +14.1 |
| Long-term PPAs (Meta-Perry/Davis-Besse, Comanche Peak) | 18.5 | **18.5** | 18.5 | 18.5 | 15% | 0 |
| 45U nuclear tax credit | 0.2 | **0.0** | 0.0 | 0.0 | 0% | −0.2 |
| Renewables/storage (valued at $/kW) | 0.8 | **0.9** | 1.0 | 1.1 | 1% | +0.3 |
| Nuclear all-in cost | (23.1) | **(23.1)** | (23.1) | (23.1) | | |
| Gas/coal fuel + variable O&M | (39.0) | **(39.0)** | (39.0) | (39.0) | | |
| Fixed O&M + capex (non-nuclear) | (12.5) | **(12.5)** | (12.5) | (12.5) | | |
| Loss-making years avoided by mothballing | 0.2 | **0.0** | 0.0 | 0.0 | | |
| **Gross asset value** | 30.8 | **49.6** | 69.4 | 99.8 | | |
| Contracted + policy share of revenue | 18% | **15%** | 13% | 11% | | |

### Annual asset cash margin, pre-tax and nominal ($bn; unhedged, marked to forwards in 2027)
| | 2027 | Base 2030 | Base 2035 | High 2030 | High 2035 |
|---|---|---|---|---|---|
| CEG: merchant energy / capacity / PPA | 16.4 / 2.7 / 1.8 | 15.5 / 2.2 / 2.5 | 17.1 / 2.5 / 2.5 | 18.9 / 3.1 / 2.5 | 20.9 / 3.5 / 2.5 |
| **CEG asset cash margin** | **10.6** | **8.4** | **8.8** | **12.7** | **13.6** |
| VST: merchant energy / capacity / PPA | 13.9 / 2.4 / 0.8 | 11.4 / 1.4 / 2.0 | 12.4 / 1.6 / 2.3 | 14.1 / 2.0 / 2.0 | 15.2 / 2.2 / 2.3 |
| **VST asset cash margin** | **7.7** | **5.7** | **6.1** | **8.9** | **9.6** |

Asset cash margin is total revenue minus fuel, O&M and capex, before overhead, retail and tax. The full annual series by asset and stream is on the `CEG_Model` / `VST_Model` sheets of the Excel model.

**What the streams show:**
- **All of the AI upside comes through merchant energy and capacity.** From Low to Extreme, energy adds +$93bn and capacity +$27bn for CEG, and +$55bn / +$14bn for VST. The data-center PPAs don't move at all: they are fixed-price, so they protect the Low case and give up upside in High and Extreme. At ~$80–100/MWh they are worth more than merchant sales in Base and less in Extreme.
- **Contracted revenue is still small.** Long-term contracts plus policy support are only ~11% (CEG) and ~15% (VST) of revenue value in Base. Both companies are still mostly merchant, and that share falls as prices rise.
- **Capacity payments matter less than headlines suggest.** They are 10–12% of revenue value. Their spike to ~$330/MW-day in 2027–28 fades by 2030 in Base: CEG capacity revenue goes from $2.7bn to $2.2bn, VST from $2.4bn to $1.4bn.
- **Near-term margins are above the long-run level in Base.** 2027 asset margins ($10.6bn CEG, $7.7bn VST) are marked to today's tight forwards. In Base they fall ~20–25% by 2030 as prices move back toward what a new gas plant needs, and VST also retires its Illinois/Ohio coal. The High case assumes 2027's tightness persists and grows.
- **The cost bases differ.** CEG's costs are mostly fixed nuclear costs ($79bn PV). VST's are mostly gas and coal fuel ($39bn). That's why a gas-price rise helps CEG's NAV proportionally more (§5).
- **Policy support is minor.** The 45U tax credit is worth ~$0.2bn even in Low, because prices stay above its phase-out band. NY ZEC is ~$0.9bn and assumed to end in 2029.
- **Streams not modelled separately:**
  - Ancillary services.
  - Clean-energy attributes (RECs/EACs) on merchant nuclear output.
  - Co-location premiums, e.g. the CyrusOne deal at Freestone, which sits inside the merchant ERCOT gas value.
  - Hedge gains and losses.
  - Retail margin, which is in the separately shown platform value.

*Correction from the first version: the ~$0.5bn remaining Crane restart capex (dated 2027) had been dropped because Crane's cash flows only started in 2028. It is now included, which lowers CEG NAV by ~$1/share in every scenario. VST is unchanged.*

---

## 4c. NAV + FCF generated

**Why this isn't just NAV + FCF.** Today's NAV is already the present value of every future year of cash, including 2027–2030. Adding cumulative FCF on top of it counts those four years twice. The consistent way to put "cash generated" on top of asset value is a **forward NAV**:

> **Value per share at end-2030 = (a) cumulative equity FCF 2027–2030 + (b) equity NAV at end-2030 of the remaining plant life**

- **(a) Equity FCF** starts from asset cash margin (revenue minus fuel, O&M and sustaining capex) and adds retail/platform EBITDA. It then deducts corporate overhead, interest (CEG ~5.3% on $13.8bn net debt; VST ~5.6% on $23.0bn), a 20% cash tax, and VST's preferred dividends (~$0.19bn).
- **What's left out:** growth capex, working capital and hedge gains/losses. FCF is simply accumulated as cash; buybacks aren't modelled.
- **(b)** revalues each plant at end-2030 on its cash flows from 2031 onward, subtracting the same claims.
- **Return:** the end-2030 value compared with today's price gives an implied annual return over the 4.25 years.

### CEG ($263.93)
| $/share | Low | **Base** | High | Extreme |
|---|---|---|---|---|
| Equity FCF 2027 ($bn) / FCF yield on market cap | 8.0 / 8.5% | **8.0 / 8.6%** | 8.1 / 8.7% | 8.2 / 8.8% |
| (a) Cumulative equity FCF 2027–30 | 73 | **88** | 103 | 126 |
| (b) Equity NAV at end-2030 (incl. platform) | 56 | **175** | 295 | 474 |
| **(a)+(b) Value at end-2030** | **128** | **262** | **399** | **601** |
| **Implied annual return from today's price** | **−15.6%** | **−0.1%** | **+10.2%** | **+21.3%** |
| Check: discounted to today at 9% (vs today's NAV incl. platform) | 100 (94) | 194 (190) | 290 (287) | 431 (432) |
| ~~Today's NAV + cumulative FCF~~ (double counts, shown only for contrast) | ~~166~~ | ~~277~~ | ~~390~~ | ~~558~~ |

### VST ($138.76)
| $/share | Low | **Base** | High | Extreme |
|---|---|---|---|---|
| Equity FCF 2027 ($bn) / FCF yield on market cap | 5.8 / 12.3% | **5.9 / 12.5%** | 6.0 / 12.6% | 6.1 / 12.8% |
| (a) Cumulative equity FCF 2027–30 | 48 | **59** | 71 | 89 |
| (b) Equity NAV at end-2030 (incl. platform) | 2 | **70** | 142 | 253 |
| **(a)+(b) Value at end-2030** | **50** | **130** | **214** | **342** |
| **Implied annual return from today's price** | **−21.2%** | **−1.6%** | **+10.7%** | **+23.6%** |
| Check: discounted to today at 9% (vs today's NAV incl. platform) | 43 (27) | 98 (82) | 157 (140) | 247 (229) |
| ~~Today's NAV + cumulative FCF~~ (double counts) | ~~75~~ | ~~141~~ | ~~211~~ | ~~319~~ |

### Base-case equity FCF build ($bn, nominal)
| | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|
| CEG revenue / asset cash margin | 21.4 / 10.2 | 22.4 / 11.2 | 21.1 / 9.5 | 20.2 / 8.4 |
| CEG + platform − overhead − interest − tax | +1.0 −0.5 −0.7 −2.0 | +1.0 −0.5 −0.7 −2.2 | +1.1 −0.5 −0.7 −1.9 | +1.1 −0.5 −0.7 −1.7 |
| **CEG equity FCF** | **8.0** | **8.8** | **7.5** | **6.6** |
| VST revenue / asset cash margin | 17.0 / 7.8 | 15.6 / 7.0 | 14.9 / 6.1 | 14.8 / 5.8 |
| VST + platform − overhead − interest − tax − preferred | +1.5 −0.4 −1.3 −1.5 −0.2 | +1.5 −0.4 −1.3 −1.4 −0.2 | +1.6 −0.4 −1.3 −1.2 −0.2 | +1.6 −0.4 −1.3 −1.1 −0.2 |
| **VST equity FCF** | **5.9** | **5.3** | **4.6** | **4.4** |

**What it adds to the NAV view:**
- **Near-term cash is strong, but it front-loads the value rather than adding to it.** FCF yields of ~8.6% (CEG) and ~12.5% (VST) in 2027 look cheap. But 2027–28 are marked to today's tight forwards in every scenario. In Base, FCF then falls ~25% by 2030 as prices normalise and PJM capacity prices come off the cap. Four years of cash is worth ~$88/share for CEG and ~$59 for VST. After that, the plants' remaining-life NAV is lower than today's.
- **If Base plays out, the return is about zero.** CEG's end-2030 value ($262) roughly equals today's price, a return of about −0.1%/yr. VST's ($130) is about −1.6%/yr.
- **The High case is needed for a normal equity return.** It gives ~+10%/yr for both. Extreme gives ~+21–24%/yr.
- **VST's high FCF yield is levered.** It runs 12–13% only after $1.3bn of interest and $0.2bn of preferred dividends. In the Low case its end-2030 NAV is ~$2/share, so almost all of its value would be the cash it generates before 2030.
- **The near-term FCF may be optimistic.** The model's 2027 VST FCF ($5.9bn, including Cogentrix) compares with Vistra's own 2026 guidance of $3.9–4.7bn free cash flow before growth, which is hedged and excludes Cogentrix. CEG's forward-marked numbers are similarly ~15–20% above its guidance run-rate. **A 20% haircut on 2027–30 FCF lowers the Base annual return to about −1.8% (CEG) and −3.7% (VST).**
- **Reconciliation:** discounted back at 9%, the end-2030 value lands within ~$4/share of today's NAV for CEG. For VST it is ~$16 higher, because the equity view credits the interest tax shield and debt cheaper than the assets' discount rates, which the unlevered NAV doesn't. VST's Base NAV is therefore more like $82–98/share, still well below $139.

In the Excel model: Summary section 2, and the consolidated FCF rows on `CEG_Model` / `VST_Model`. The code is in `fcf.py`.

---

## 4d. Replacement cost + FCF

**The approach:** value the fleet at what it would cost to build it again today, reduced for age, then add the cash the existing plants generate while no one can build replacements.

> **Value/share = [depreciated replacement cost (DRC) − net debt & claims + PV of equity FCF over the replacement lead time] ÷ shares**

- **DRC** = MW × 2026 new-build $/kW × remaining-life fraction. The fraction is years left to the assumed end of life divided by total life. Hydro is set at 50% because dams last 100+ years. DRC uses **no earnings and no power prices**.
- **New-build costs:**
  - Nuclear (next AP1000, EPRI base): $12,100/kW. EPRI's range is $9,700–15,100, and Vogtle 3&4 actually cost ~$17,500–21,700.
  - CCGT: $2,350/kW (GridLab).
  - Peaker: $1,970/kW (recent filing).
  - Pumped storage: $3,500/kW (NREL range $2,000–5,500).
  - Geothermal: $5,500/kW (estimate).
  - Wind/solar/storage: $1,600/kW (estimate).
  - Coal: nobody builds coal, so it is replaced at the CCGT cost.
- **FCF** is equity FCF after overhead, interest, tax and preferred dividends, and includes retail cash. It is discounted at 9%. The headline adds **5 years**, which is roughly when turbine backlogs let new gas reach the grid (GE Vernova's backlog is ~116 GW). New nuclear takes 10+ years. FCF is the only part that changes with the AI scenario.
- **Two bases for nuclear:**
  - **Like-for-like:** rebuild it as new nuclear.
  - **Functional:** replace its capacity with new gas. That costs $2,350 × 0.95/0.78 = $2,862 per kW, adjusting for the higher share of capacity the grid credits nuclear with. It isn't carbon-free.

| | CEG | VST |
|---|---|---|
| Replacement cost new: nuclear as new nuclear / as new gas | $341bn / $130bn | $176bn / $116bn |
| **DRC**: nuclear as new nuclear / as new gas | **$134bn / $54bn** | **$70bn / $45bn** |
| Equity at DRC before FCF: as new nuclear / as new gas | $337 / $109 per share | $126 / $54 per share |
| **+ 5 yrs FCF, as new nuclear**: Low / **Base** / High / Extreme | $405 / **$422** / $440 / $468 | $171 / **$184** / $198 / $220 |
| **+ 5 yrs FCF, as new gas**: Low / **Base** / High / Extreme | $177 / **$195** / $213 / $240 | $100 / **$113** / $127 / $148 |
| Share price | $263.93 | $138.76 |
| Market EV ÷ DRC: as new nuclear / as new gas | 0.81x / 2.02x | 1.06x / 1.64x |
| Nuclear new-build cost the share price implies (Base, 5-yr FCF, same age haircut) | **~$5,700/kW** | **~$6,200/kW** |

In the Excel model: Summary section 3, and the replacement-cost columns on `CEG_Assets` / `VST_Assets`. Change the FCF years and the nuclear basis on Inputs. The code is in `replacement.py`.

**What it shows:**
- **The gas-plant DRC matches what buyers actually pay.** Depreciated CCGTs come to ~$1,040–1,080/kW (45% of $2,350). Recent deals were $1,142/kW for LS Power's PJM package and ~$1,023/kW for Calpine. So for gas, replacement cost and the market agree, which independently supports the approach.
- **For nuclear, the answer depends on the replacement basis:**
  - **Rebuilt as new nuclear,** both stocks look cheap: CEG ~$422 vs $264, VST ~$184 vs $139. CEG's EV is only 0.81x the depreciated cost of rebuilding its fleet.
  - **Replaced by new gas,** both look expensive: CEG ~$195, VST ~$113.
  - **The market sits between the two.** It values nuclear as if new nuclear cost **~$5,700–6,200/kW**. That is roughly the "Nth-of-a-kind" AP1000 cost MIT projects for the 4th plant ($6,200/kW), about half of EPRI's next-plant estimate, and a third of Vogtle.
- **Why new-nuclear replacement cost is a ceiling, not a floor.** Replacement cost only sets value if someone would pay it to replicate the plant. Tobin's q (the cash-flow value from the NAV model divided by DRC on the new-nuclear basis) shows when that happens:
  - CEG: 0.35 Low / 0.60 Base / 0.86 High / 1.24 Extreme.
  - VST: 0.44 / 0.71 / 1.00 / 1.44.
  - A q below 1 means building new nuclear doesn't pay. At the ~$80–100/MWh hyperscalers are paying, that's true: a $12,100/kW reactor needs roughly $130–150/MWh.
  - So the like-for-like figure becomes a real valuation only in the **Extreme** case, or if the US commits to new nuclear and AP1000 costs fall toward $6,000/kW.
  - In Base and High, the functional (gas) basis plus the scarcity cash is the more defensible anchor. On that basis, today's prices already exceed the value.
- **What five years of FCF adds.** About $85/share for CEG (Base) and $59 for VST. That is 20–32% of the like-for-like value and 44–52% of the functional value. From Low to Extreme the value moves only ~$50–65/share, because 2027–28 are marked to today's forwards in every scenario. With this approach, the nuclear replacement basis matters far more than the AI scenario.
- **Caveats:**
  - The in-service years for each asset group are my estimates. Every 10 points of remaining-life fraction on nuclear moves CEG ~$78/share and VST ~$23/share on the like-for-like basis. That makes it the most sensitive input in this approach.
  - The near-term FCF may be ~15–25% high against company guidance (§4c).

## 4e. Management build plans and entry prices

### What management says about building new capacity (as of Q2-2026)
| | CEG | VST |
|---|---|---|
| New nuclear | No large new reactors. Crane (835 MW) restart targeted for 2027; FERC approved the interconnection-rights transfer. Nuclear uprates are part of a 5 GW PJM queue (uprates + gas + batteries). A small venture stake in Blue Energy SMRs. | No new reactors. 433 MW of uprates (Perry, Davis-Besse, Beaver Valley) funded by the Meta PPAs, arriving 2031–34, plus subsequent license renewals at all PJM units. |
| New gas | Pin Oak Creek 460 MW peaker (ERCOT) online Apr-2026; a proposed Harford County, MD plant (pipeline cost is a hurdle). Dominguez: CEG **won't build merchant gas** without policy certainty ("existing generation is the bedrock"). | Permian 860 MW under construction; up to 2 GW ERCOT gas; coal-to-gas conversions. 4.5 GW total additions. $4.5–5bn growth budget, mostly **acquisitions** (Lotus, Cogentrix). |
| Demand view | Data-center customers are waiting on PJM co-location and backstop-auction rules. | Burke: ERCOT load +5–6%/yr and PJM +2–3%/yr through 2030, **below ISO forecasts**. "Both underbuilding and overbuilding have serious consequences." |
| Buying vs building | Sold divested Calpine plants at ~$1,200–1,420/kW against ~$960/kW implied purchase cost. | Bought gas at $731/kW (Lotus) and ~$859/kW (Cogentrix), against ~$2,350/kW new-build. Burke: customers pay "a premium" for existing plants "because it's still a discount to what new build costs." |

**How this bears on the valuation:**
- **Neither company is building new nuclear, and both are buying gas plants rather than building them.** That is management's own vote that existing plants are worth *less* than new-build cost (Tobin's q < 1). It supports treating new-nuclear replacement cost as a ceiling (§4d).
- **Vistra's own PJM load view is weaker than the High case.** At +2–3%/yr (~13–19 GW by 2030) it sits between our Low and Base PJM data-center assumptions. Management's demand view does not support the High case the share prices require.

### Entry prices implied by the model (not derived from the current price)
Method: take the value at end-2030 (FCF generated + forward NAV, §4c) and discount it back 4.25 years at the required return. The "haircut" version cuts 2027–30 FCF by 20% for possible over-optimism against guidance.

| Price at which… | CEG | VST |
|---|---|---|
| High case earns 10%/yr | $252–266 | $133–142 |
| High case earns 15%/yr | $209–220 | $110–118 |
| Base case earns 10%/yr | $163–175 | $79–86 |
| **Base case earns 15%/yr (fat pitch)** | **$135–145** | **$65–72** |
| Hard-asset floor: gas-equivalent replacement + 5 yrs FCF, Low scenario | $177 | $100 |
| Base NAV incl. platform | $190 | $82 (equity view ~$98) |
| **Current price** | **$263.93** | **$138.76** |
| 52-week low / high | $228.63 / $412.70 | $132.66 / $217.10 |

**How to read it:**
- **Today's prices are what you'd pay for ~10%/yr if the High case happens.** At about $264 and $139, both stocks earn roughly a cost-of-equity return only if AI-driven scarcity persists. If Base happens, the return is ~0%/yr (§4c).
- **Fat pitch: CEG ~$135–145, VST ~$65–72.** At those prices the Base case alone earns ~15%/yr. Both prices are also below the hard-asset floor (CEG $177, VST $100), so even a Low outcome is covered by what it would cost to rebuild the fleet with new gas plus five years of cash. Any High/Extreme outcome is free upside.
- **"Good, not fat": CEG ~$165–175, VST ~$80–86.** Here the Base case earns ~10%/yr.
- **If you believe the High case:** CEG below ~$210–220 and VST below ~$110–118 earn 15%/yr. That is "if High is true, the math says…", not a forecast. Vistra's own load outlook argues against leaning on it.
- **Both fat-pitch levels are far below the 52-week lows.** They would need a meaningful de-rating: an AI capex pause, PJM capacity-price reform, or gas below $3.
- **VST's levels are more fragile.** Leverage makes its low-end values swing hard: the Low-case end-2030 value is only ~$50.

## 4f. What VST's high-profile buyers may be seeing (Pelosi, Thiel Macro)

**The trades:**
- **Pelosi:** deep in-the-money Jan-2026 call options ($50 strike), bought Jan-2025 and exercised into 5,000 shares on 16-Jan-2026, disclosed as a $100k–250k transaction.
- **Thiel Macro:** 372,755 shares ($59.1mm, 14% of a $419mm 13F) bought in Q2-2026, worth ~$159/share at quarter-end. The fund's other holdings: Amazon, Vista Energy (an Argentine oil and gas producer), the regulated utilities AEP, DTE, FirstEnergy and CMS, and X-Energy (a nuclear developer). It is a power-demand and energy-price theme basket, not a Vistra valuation call.
- **What the filings don't show:** 13F filings list long positions only and arrive ~6 weeks late, so neither trade shows current holdings or hedges.

**What they would need to believe, measured in the Excel model** (VST, $/share; "levered" = equity FCF to 2030 plus NAV at 2030, discounted at 9%):

| Step | NAV incl. platform | Levered equity value |
|---|---|---|
| Base | $82 | $98 (cheap debt + interest tax shield ≈ +$16) |
| + ERCOT at High, PJM stays Base (Burke expects ERCOT load +5–6%/yr) | $101 | $117 |
| + retail valued at 10x instead of 6x | $118 | $130 |
| Remaining gap to $138.76 | | ~$9/share ≈ $3bn of Helix / site options, growth projects, or higher gas (+$1 HH ≈ +$33) |

The model had two genuine gaps, both now switches in the Excel model:
- **An ERCOT-only scenario.** Texas can now tighten while PJM stays at Base.
- **A levered equity value.** It credits the cheap debt and the interest tax shield.

**What the price requires:**
- Every bull item has to go right at once, and even then the price still needs some unmodelled option value on top.
- The Low case still leaves VST's levered value near $43.
- On the levered Base value (~$98), the $105 entry level discussed in §4e pays roughly for Base plus a little. The Texas and retail upside come without paying for them, but the Low-case downside is not protected.

## 5. Sensitivity: long-run energy price × capacity price (NAV/share, generation only)

**CEG** (current price $263.93)
| LR energy shift \ PJM capacity $/MW-day | 100 | 175 | 230 | 325 | 450 | PJM West ATC |
|---|---|---|---|---|---|---|
| −$20 | 35 | 46 | 54 | 69 | 89 | $40 |
| −$10 | 88 | 100 | 109 | 125 | 146 | $50 |
| **Base** | 151 | 164 | **173** | 189 | 209 | $60 |
| +$10 | 215 | 227 | 237 | 252 | 273 | $70 |
| +$20 | 279 | 291 | 300 | 316 | 337 | $80 |
| +$30 | 343 | 355 | 364 | 380 | 401 | $90 |
| +$40 | 406 | 419 | 428 | 444 | 465 | $100 |

**VST** (current price $138.76)
| LR energy shift \ PJM capacity $/MW-day | 100 | 175 | 230 | 325 | 450 | PJM West ATC |
|---|---|---|---|---|---|---|
| −$20 | −21 | −13 | −8 | 2 | 14 | $40 |
| −$10 | 8 | 15 | 21 | 30 | 42 | $50 |
| **Base** | 43 | 51 | **56** | 66 | 78 | $60 |
| +$10 | 80 | 88 | 93 | 102 | 115 | $70 |
| +$20 | 117 | 124 | 130 | 139 | 151 | $80 |
| +$30 | 153 | 161 | 166 | 176 | 188 | $90 |
| +$40 | 190 | 198 | 203 | 212 | 225 | $100 |

**Reading the grid:** each $10/MWh of long-run price is worth about **$64/share for CEG (~24% of the price)** and **$37/share for VST (~27% of the price)**. Capacity prices matter much less: moving from $230 to $325/MW-day adds only ~$16 and ~$10/share. The conclusion depends heavily on the long-run energy price, and a small change there flips it. That is why I show the solve below rather than a single point estimate.

### Other sensitivities (Base, NAV/share, generation only)
| | CEG | VST |
|---|---|---|
| Base | 173 | 56 |
| Discount rates −1pt / +1pt | 192 / 156 | 66 / 47 |
| Nuclear life ends 2045 (no second license renewals) / extended to 2065 | 149 / 185 | 50 / 60 |
| **Henry Hub −$1 / +$1** (power follows gas through the heat rate) | **93 / 253** | **25 / 90** |
| Data-center PPA prices −$10 / +$10 | 166 / 179 | 50 / 63 |
| Low scenario with / without the 45U floor | 77 / 76 | 1 / 1 |
| High energy, PJM capacity capped at $325 permanently | 270 | 115 |

The 45U credit hardly matters. In most outcomes prices sit above its phase-out band, so it protects only against a deep-trough scenario before 2032.

---

## 6. Market valuation vs asset value — what is priced in?

### (a) What the market is paying for the energy assets
- **CEG:**
  - EV of $108.5bn equals **$2,171 per kW owned**.
  - Take out the gas fleet at recent deal $/kW ($1,142 PJM, $1,419 ERCOT, $1,174 ISO-NE, $1,023 Calpine average) and hydro/geothermal/renewables at Base. Add back overhead and take out the platform.
  - What's left implies the market pays **~$76bn, or ~$3,330/kW, for the nuclear fleet**. My model puts it at $2,564/kW in Base and $3,603/kW in High.
  - So the market values CEG's nuclear at about **70% of the way from Base to High**.
- **VST:**
  - EV of $73.9bn equals **$1,504/kW**.
  - The same calculation leaves $4,824/kW for 6.4 GW of nuclear, above even my Extreme case ($4,166/kW).
  - That residual really says the market values **VST's gas fleet** well above both my model and recent deal prices. Equivalently, it is pricing the whole fleet at a High-case deck.
- **New-build cost is not a valuation anchor.** Replacement cost for new nuclear is >$10,000/kW (Vogtle-class). No one would build new nuclear at these prices, so replacement cost doesn't set what the existing fleet is worth. The real ceiling on nuclear's scarcity value is new gas plus a clean-power premium. Hyperscaler PPAs (~$80–100/MWh) are that premium in practice.

### (b) The assumptions the current price requires
| | Required long-run shift vs Base | Implied PJM West ATC (2026$) | Implied ERCOT | Implied PJM heat rate | Or: Henry Hub at Base heat rate |
|---|---|---|---|---|---|
| CEG, generation only | +$14.3 | $75 | $64 | 20.4 | $5.13 |
| CEG, incl. platform | +$11.6 | $72 | $62 | 19.7 | $4.92 |
| VST, generation only | +$22.5 | $83 | $73 | 22.7 | $6.46 |
| VST, incl. platform | +$15.5 | $76 | $66 | 20.7 | $5.70 |

**Is that defensible?**
- The prices CEG requires are about **where the 2027–28 forward curve already sits** (~$72–73 nominal). The market is effectively extrapolating today's scarcity forever. Three things have to hold:
  1. New CCGTs cost ≥~$2,800–3,000/kW and stay supply-constrained.
  2. Or gas settles near $5.
  3. And PJM's capacity construct is not re-capped again after the current collar. The 2026/27–2028/29 cap exists precisely because of political pushback.
- VST requires a heat rate of ~21–23 or gas near $5.70–6.50. That is **materially above** history, the new-entry ceiling, and the prompt gas price ($2.79 in Sep-26). EIA's STEO does project ~$4.60 for 2027.
- **Private buyers are more bullish than my Base case on gas plants in ERCOT and New England:**
  - Brazos Valley sold at $1,419/kW, against my Base ERCOT CCGT value of ~$690/kW.
  - RISEC sold at $1,174/kW, against my ~$750–820/kW for New England.
  - Either those buyers underwrite a High-type ERCOT outlook, or my ERCOT spark-spread capture (1.20× ATC) is too low.
  - Marking gas at deal prices raises Base NAV to **$215 for CEG and $97 for VST** (incl. platform). Both are still below the share price.

### (c) Probability-weighted
With **illustrative** weights (Low 20% / Base 45% / High 25% / Extreme 10%, my judgment, not a forecast): CEG **$219** (price is +21% above) and VST **$100** (price is +38% above), both incl. platform. Hold Low at 20% and Extreme at 10%, and put **all** of the remaining 70% on High with **zero** on Base: CEG's weighted NAV then roughly equals its price (~$263 vs $264), and VST's reaches only ~$126.

### (d) So — is the market wrong?
- **Assets today (Base):** below the price for both companies.
- **Assets if AI-driven scarcity persists (High):** ≈ the price for both.
- **What the price requires:** long-run PJM prices ~$12–23/MWh above new-entry cost, held indefinitely, **or** gas near $5–6.50.

The market is not obviously wrong, because the High case is plausible. But it is already paying for most of the AI-scarcity upside, **while the Low case (CEG −64% to −71%, VST ≈ equity wipe-out on a generation basis) is not priced as a real risk**. CEG gives the better-balanced exposure: long-life assets, lower leverage, and ~12% contracted at premium prices. VST is a levered bet that spark spreads stay wide.

---

## 7. Key assumptions to challenge (where the answer is fragile)

1. **Long-run heat rate / power price.** This is the dominant driver (±$64/share per $10/MWh for CEG). Base (16.5) is above history, and High (20) is today's forward curve.
2. **Gas price.** ±$1 roughly doubles or halves NAV. If AI demand raises gas burn *and* LNG exports grow, gas and heat rate could rise together. That would support High+.
3. **New-entry cost.** Every $450/kW of CCGT capex moves the ceiling ~$6–7/MWh.
4. **PPA prices are undisclosed.** I used analyst estimates ($80–100). They are worth ±$6–7/share.
5. **Nuclear life.** Losing second license renewals (end 2045) costs CEG ~$24/share.
6. **Forward-marked 2027 economics look rich against guidance.** My 2027 asset EBITDA (unhedged, at forwards) is ~15–20% above the run-rate implied by 2026 guidance. That gap reflects hedges struck at lower prices, and it may mean the forward curve I derived is a little rich. If so, Base NAV is modestly overstated (it has little effect on the long-run solve).
7. **Retail platform.** It is valued at 6× EBITDA (VST $1,463mm reported for FY25; CEG $1.0bn is my estimate because CEG doesn't disclose it). It is earnings-based by construction, which is why it's shown separately.

---

## 8. Data limitations — please read

- **How the data was gathered.** Outbound fetches to SEC EDGAR and the company IR sites were blocked in this environment. Figures come from web search excerpts of those filings and releases, listed below. Before acting on this, **verify** CEG and VST debt and cash, share counts, and the pending-deal terms against the filings themselves.
- **Estimated inputs.** The plant-group MW splits (by hub), PPA prices, pension/TRA/NCI balances, the ERCOT forward ATC and the PJM ATC/on-peak conversion are **estimates**. They are marked `EST` / `ASSUMPTION` in `inputs.py`.
- **Not modelled:**
  - Hedge-book mark-to-market.
  - Working capital and nuclear fuel inventory.
  - Any surplus in the decommissioning trusts. CEG's likely surplus is partly owed to ratepayers under regulatory agreements.
  - VST's 433 MW of uprates and 2 GW of new ERCOT gas, and CEG's uprates and new-build pipeline. These are all **excluded**: the asset NAV covers existing and contracted assets only, with development treated as an option.

---

## Sources
**Company filings and transactions**
- CEG Q2-2026 10-Q: https://www.sec.gov/Archives/edgar/data/0001868275/000186827526000104/ceg-20260630.htm
- CEG Q2-2026 release: https://www.constellationenergy.com/news/2026/08/constellation-reports-second-quarter-2026-results.html
- CEG Q2-2026 call transcript: https://www.theglobeandmail.com/investing/markets/stocks/CEG/pressreleases/3829710/constellation-energy-ceg-q2-2026-earnings-call-transcript/
- CEG 2025 10-K: https://www.sec.gov/Archives/edgar/data/1868275/000186827526000032/ceg-20251231.htm
- Calpine deal terms: https://www.mergersight.com/post/constellation-energy-s-26-6bn-acquisition-of-calpine
- Calpine deal close: https://www.constellationenergy.com/news/2026/01/constellation-completes-calpine-transaction-powering-americas-clean-energy-future.html
- LS Power PJM divestiture: https://www.powermag.com/constellation-to-sell-4-4-gw-of-pjm-gas-power-assets-to-ls-power-for-5b-in-regulatory-divestiture/
- Brazos Valley sale: https://www.powermag.com/ls-power-acquiring-606-mw-texas-gas-fired-plant-from-constellation/
- RISEC purchase (Constellation): https://www.constellationenergy.com/news/2026/09/constellation-to-acquire-rhode-island-state-energy-center-from-shell.html
- RISEC purchase (Motley Fool): https://www.fool.com/investing/2026/09/12/shell-just-sold-a-usd715-million-stake-in-a-major-new-england-asset-to-constellation-energy-here-s-what-investors-need-to-know/
- CEG secondary offering / buyback: https://www.tipranks.com/news/company-announcements/constellation-energy-completes-secondary-offering-and-share-repurchase
- Calpine regional fleet: https://naturalgasintel.com/news/why-calpine-constellations-blockbuster-deal-tied-to-soaring-power-generation-especially-natural-gas/
- Crane / Microsoft PPA: https://www.utilitydive.com/news/constellation-three-mile-island-nuclear-power-plant-microsoft-data-center-ppa/727652/
- Clinton / Meta PPA pricing estimates: https://www.utilitydive.com/news/meta-constellation-ppa-could-be-first-of-many-deals-for-existing-reactors/750567/
- CyrusOne / Freestone: https://www.constellationenergy.com/news/2026/02/constellation-and-cyrusone-announce-agreement-to-support-new-data-center-facility-at-freestone-energy-center-in-texas.html
- VST Q2-2026 10-Q: https://www.sec.gov/Archives/edgar/data/0001692819/000169281926000019/vistra-20260630.htm
- VST Q2-2026 release: https://investor.vistracorp.com/2026-08-07-Vistra-Reports-Second-Quarter-2026-Results
- VST 2025 10-K: https://www.sec.gov/Archives/edgar/data/1692819/000169281926000006/vistra-20251231.htm
- VST FY-2025 results (segment EBITDA): https://investor.vistracorp.com/2026-02-26-Vistra-Reports-Fourth-Quarter-and-Full-Year-2025-Results
- VST preferred stock (2024 10-K): https://www.sec.gov/Archives/edgar/data/1692819/000169281925000013/vistra-20241231.htm
- Cogentrix (Utility Dive): https://www.utilitydive.com/news/vistra-cogentrix-natural-gas-energy-deal-data-centers/808854/
- Cogentrix (POWER): https://www.powermag.com/vistra-to-bolster-gas-fired-fleet-by-5-5-gw-with-4b-cogentrix-acquisition/
- Meta nuclear PPAs with Vistra: https://www.power-eng.com/nuclear/vistra-and-meta-ink-ppa-for-2-6-gw-of-nuclear-power-in-pjm-region/
- Comanche Peak PPA: https://www.power-eng.com/nuclear/vistra-secures-long-term-nuclear-ppa-from-comanche-peak-nuclear-plant/
- Illinois coal retirements: https://finance.yahoo.com/sectors/energy/articles/company-close-three-illinois-power-082338987.html
- Talen / AWS PPA (~$80/MWh implied): https://www.powermag.com/talen-amazon-launch-18b-nuclear-ppa-a-grid-connected-ipp-model-for-the-data-center-era/
- Deloitte power M&A mid-2026 (gas $1,468/kW): https://www.deloitte.com/us/en/insights/industry/power-and-utilities/power-utilities-mergers-and-acquisitions-2026-midyear-update.html

**Market prices**
- CEG share price: https://www.ad-hoc-news.de/boerse/news/corporate-news/constellation-energy-stock-gains-0-70-percent-as-consensus-stays-higher/70158306
- VST share price: https://finance.yahoo.com/quote/VST/
- PJM 2028/29 capacity auction: https://insidelines.pjm.com/pjm-capacity-auction-procures-138318-mw-of-generation-resources-as-work-continues-to-address-growing-electricity-demand/
- PJM 2027/28 capacity auction: https://insidelines.pjm.com/pjm-auction-procures-134479-mw-of-generation-resources/
- PJM West forwards: https://www.engieresources.com/market-insight/pjm-update-storm-driven-swings-2/
- ERCOT outlook (1): https://comparepower.com/texas-electricity-prices/
- ERCOT outlook (2): https://www.energyogre.com/texas-electricity-market-update-q1-2026
- EIA Henry Hub outlook: https://www.eia.gov/todayinenergy/detail.php?id=67004

**Demand and costs**
- EPRI: https://powering-intelligence.epri.com/load-growth.html
- LBNL: https://www.rtoinsider.com/134980-national-lab-projects-sharp-growth-in-data-center-power-demand/
- BNEF: https://www.eenews.net/articles/data-centers-share-of-us-electricity-seen-doubling-by-2030/
- Range of forecasts (WRI): https://www.wri.org/insights/us-data-centers-electricity-demand
- PJM 2026 load forecast: https://www.pjm.com/-/media/DotCom/library/reports-notices/load-forecast/2026-load-report.pdf
- PJM data-center load growth: https://www.datacenterdynamics.com/en/news/pjm-reports-peak-load-growth-of-30gw-through-2030-from-data-center-sector/
- NEI nuclear costs ($36.46/MWh in 2025): https://www.nei.org/getContentAsset/47fa8caa-9b0d-4029-932c-07f902e82f4f/8d8ff8d6-b2ae-401b-a63c-f6b108e809d2/2024-Costs-in-Context-final.pdf?language=en-US
- 45U nuclear credit (CRS): https://www.congress.gov/crs-product/IN12557
- GridLab gas-turbine costs: https://gridlab.org/wp-content/uploads/2025/09/GridLab_Gas-Turbine-Costs-Report-1.pdf

## 9. Vista Energy (VIST) — Thiel Macro's largest energy position

*Editable model: `outputs/VIST_NAV_Model.xlsx` (engine: `vista_nav.py`, builder: `build_vista_excel.py`).*

### Method
Vista is an oil producer, so the asset NAV follows the standard E&P method:
- **PV of the producing base** (wells online at 1-Oct-2026 on their decline, with no new drilling).
- **Plus PV of drilling the proved-undeveloped wells** (~450).
- **Plus a risked PV of the unbooked inventory** (~1,020 further locations, at a 60% chance factor).
- **Minus net debt and other claims.**

Scenarios are long-run Brent decks, the oil equivalent of the AI-demand scenarios. The Argentina risk is carried in the discount rate (12% base).

### Inputs
- **Production and margin:** 156 kboe/d in Q2-26 (guidance 158 for 2026, a 250 target by 2030). EBITDA was $805mm in Q2, a ~70% margin.
- **Costs and prices:** lifting $4.5/boe; realized oil $89.4/bbl.
- **Balance sheet and reserves:** net debt $3.06bn; 1P reserves 588 MMboe at YE-25 (PV-10 $6.61bn at SEC prices, before Equinor).
- **Drilling:** well cost $14.2mm, falling to an $11mm target by 2028. Inventory of >1,320 locations plus the Equinor blocks ($712mm, closed May-26).
- **Oil price deck:** Brent ~$101–105 spot (Hormuz disruption); futures ~$77 by late 2027 and ~$75 in 2028.
- **Calibration:** P1 ~177 kboe/d and ~237 kboe/d by 2030; EBITDA/boe matches Q2.

| Long-run Brent (2026$) | Low $60 | **Base $72** | High $85 | Extreme $100 |
|---|---|---|---|---|
| Risked NAV/ADS | $52 | **$80** | $110 | $144 |
| Unrisked NAV/ADS | $61 | $95 | $133 | $176 |
| Producing-base-only floor/ADS | $20 | $28 | $36 | $45 |
| vs price $73.35 | −30% | **+8%** | +49% | +96% |

**Risked NAV/ADS: long-run Brent (rows) × discount rate (columns)**

| Brent LR | 10% | **12%** | 15% | 18% |
|---|---|---|---|---|
| $55 | 50 | 40 | 28 | 19 |
| $60 | 64 | 52 | 38 | 27 |
| $65 | 78 | 63 | 47 | 35 |
| **$72** | 96 | **80** | 61 | 47 |
| $80 | 117 | 98 | 76 | 59 |
| $85 | 131 | 110 | 85 | 67 |
| $95 | 157 | 133 | 104 | 83 |

**Other levers (Base, NAV/ADS $80):**
- Reinstating an 8% export duty: −$19.
- EUR ±15%: ±$15.
- Well cost +20%: −$10.
- Inventory −30%: −$8.
- Unbooked inventory risked at 100% / 30%: $95 / $68.
- War lasts (Brent $100/95/90 for three years, then Base): $90.

**Market view:**
- **Multiples:** EV $11.5bn equals ~3.4× next-12-month EBITDA, ~$70k per flowing boe/d, $19.5 per 1P boe, and an ~12% unlevered FCF yield.
- **What the price implies:** long-run Brent of **~$69** at a 12% discount rate, or a **~12.9%** discount rate at Base oil. That is roughly the futures curve plus a normal Argentina premium. **VIST is close to fair value on Base, not deeply discounted.**

### What Thiel Macro may be seeing
- **The entry:** ~1.2mm ADS worth $75.9mm at 30-Jun-26, about $63/ADS, bought when Brent had briefly dropped to ~$70.
  - At that price our Base risked NAV (~$80) offered a ~20% discount.
  - At $73 today it offers ~8%.
- **Oil convexity:** the Hormuz disruption. If the war premium persists for three years, VIST is worth ~$90. In the Extreme case, ~$144. VIST is effectively an unhedged call on oil.
- **Argentina normalisation:** each step in country risk is worth a lot. Moving from a 12% to a 10% discount rate adds ~$17/ADS. Reform backsliding to 15% removes ~$19.
- **Portfolio fit:** Vista (oil) sits beside Vistra and four regulated utilities (power) and Amazon (a power buyer). That is a basket built around energy scarcity. VIST is its oil leg, not a standalone valuation call.

### Entry levels (from the model, not the price)
| | $/ADS |
|---|---|
| Base earns ~15%/yr (NAV at a 15% discount rate) | ~$61 |
| 30% margin of safety to Base risked NAV | ~$56 |
| High case earns ~15%/yr | ~$85 |
| Current price | $73.35 |
| Hard floor (producing base only) | ~$28 |

- **Fat pitch: ~$55–61.** At that price the Base case alone earns ~15%/yr.
- **At $73 you are paying fair value for Base plus a moderate premium on oil and Argentina.** It is a reasonable holding if you want oil exposure through the Hormuz risk, not a margin-of-safety buy.
- **Unlike CEG and VST, the downside is not protected by replacement cost.** The producing base covers only ~$28.

