# Intel valuation model: scenario DCF

File: `intel_valuation_model.xlsx`. It is built on the findings in `../intel-competitive-analysis-2026-09.md`.

**Sheets:**
- **README**: how to use the model, the method, and how each scenario maps to the product evidence.
- **Inputs**: every assumption, with its source.
  - Blue cells are inputs.
  - Yellow cells are key judgment calls, or placeholders to verify against the Q2-26 10-Q.
- **Summary**: each scenario's value, the probability-weighted value, and a reverse DCF against today's price.
- **Sensitivity**: live WACC × terminal-growth grids for all three scenarios, plus a Base-case tornado.
- **Bear / Base / Bull / Taiwan**: identical 2026E–2033 forecasts by segment, discounted to 30 Sep 2026.

The file was written without cached values; Excel or Google Sheets recalculates everything on open. The formulas were checked with a Python formula engine (0 errors), because LibreOffice's Calc engine isn't installed in the build environment.

## Results at default inputs, including the China layer (price $123.00 on 25 Sep 2026; about 5.48bn diluted shares; WACC 10.4%; terminal growth 3%)

| | Bear | Base | Bull | Probability-weighted (30/45/25) |
|---|---|---|---|---|
| Value per share | $0 (equity is −$6.9/share before the floor) | ~$22 | ~$53 | ~$23 |
| vs. price | −100% | −82% | −57% | −81% |
| Before the China layer | ~$1 | ~$24 | ~$55 | ~$25 |
| 2033 revenue lost to China localization and trade | $3.8bn | $3.3bn | $2.0bn | |

**China layer.** Take the China-billed share of revenue (FY2025 about 24%, derived) times the fraction that is China *domestic* demand (50%, a judgment call; billings include PCs assembled in China for export). Apply that to DCAI and CCPG revenue, then erode it each year at a scenario rate:

| Scenario | Annual erosion |
|---|---|
| Bear | −20% → −10% (truce lapses, xinchuang widens, origin rule hits 18A US-fabbed parts) |
| Base | −8% → −5% |
| Bull | −3% |

Lost revenue is removed at full gross margin. A Taiwan disruption isn't modeled as a line item: it would hurt Intel too, and the geopolitical second-source upside is already inside the external-foundry drivers.

**Reverse DCF.** Today's roughly $666bn EV requires about **$98bn of normalized 2034 FCF**. That is **6.9×** the Base case, or $325–390bn of revenue at a 25–30% FCF margin, against $125bn in the Bull case. At 8.5% WACC and 4% terminal growth, the Base case reaches only about $38 and the Bull case about $91.

**Tornado (Base, one input at a time):**

| Input flexed | Range of value per share |
|---|---|
| External foundry revenue ×0.5 / ×2 | $17 – $32 |
| DCAI growth ±3 pts per year | $18 – $27 |
| Gross margin ±3 pts | $18 – $26 |
| Capex ±15% | $20 – $24 |
| China erosion 10 pts/yr faster / 5 pts/yr slower | $20 – $24 |

China is a real but second-order valuation driver. It is smaller than foundry, server or margin outcomes, because only an estimated ~12% of revenue (24% × 50%) is China domestic demand. If you believe the domestic fraction is higher, raise `Inputs` "Share of China-billed revenue that is China DOMESTIC end-demand".

## Taiwan scenario (added)

**Condition:** Taiwan's fabs are cut off from Western customers from 2027. This covers an invasion, a blockade, or reunification followed by US export controls that treat Taiwan as China. It is a *conditional* scenario: "if this happens, the math says…".

**What's modeled:**

| Driver | 2027 → 2033 |
|---|---|
| Server revenue | +10%, then +25% as Intel captures AMD's TSMC-dependent share |
| Client revenue | −10% in the 2027 disruption year (Intel's own TSMC tiles are lost), then +20% |
| External foundry + packaging revenue (capacity-limited) | $10bn → $70bn |
| Gross margin | 45% → 62% |
| China revenue | Goes to zero |
| Capex | $40–50bn a year |

**Result.** Revenue reaches about **$155bn in 2033**, operating income about $71bn, and value about **$80/share** at 10.4% WACC.

| | Value per share |
|---|---|
| At 8.5% WACC / 3% growth | ~$116 |
| At 8.5% WACC / 4% growth | ~$139 |
| Foundry revenue ×1.5 | ~$112 |
| Foundry revenue ×1.5 and gross margin +5 pts | ~$127 |

**Break-even test.** At default inputs, no probability of the Taiwan scenario justifies $123, because the Taiwan value itself is below the price. With the most aggressive payoff variant above (foundry ×1.5 and gross margin +5 pts), the price requires about a **95% probability** of a Taiwan cut-off.

**Weights are now:** Bear 28%, Base 43%, Bull 24%, Taiwan 5%. That gives a probability-weighted value of **~$26**.

**Not modeled in the Taiwan scenario, all of which lower it:**
- global recession
- US price controls or Defense Production Act allocation of capacity
- a higher cost of capital in wartime
- damage to Intel's Malaysian assembly and test sites, and to its supply chain

A friendlier outcome (TSMC keeps supplying the West after a peaceful reunification) would sit between Base and Taiwan.

## What to check before trusting this

1. **China inputs.** FY2025 China revenue is a derived residual, and the 50% domestic-demand share is my judgment. Verify both.
2. **Placeholders.** D&A, stock-based comp, non-controlling interests (SCIP fab partners and the Mobileye minority), and Q1-26 external foundry revenue were not sourceable here. NCI is set to 0, which *overstates* value.
3. **Share count.** It is derived as Q2 non-GAAP net income ÷ EPS, plus the August offering shares; verify it against the 10-Q.
4. **Gross capex.** Partner and government offsets are ignored. The effect on value is small; see the tornado.
5. **Consensus comparison.** Consensus 2027 EPS is about $2.04; the Base case gives about $1.59 before SBC. Consensus sits between the Base and Bull cases.
6. **Scenario drivers are hypotheticals.** They are tied to the product evidence and were fixed before the valuation was computed. They were not tuned toward the market price.
