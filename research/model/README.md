# Intel valuation model: scenario DCF

File: `intel_valuation_model.xlsx`. It is built on the findings in `../intel-competitive-analysis-2026-09.md`.

**Sheets:**
- **README**: how to use the model, the method, and how each scenario maps to the product evidence.
- **Inputs**: every assumption, with its source.
  - Blue cells are inputs.
  - Yellow cells are key judgment calls, or placeholders to verify against the Q2-26 10-Q.
- **Summary**: each scenario's value, the probability-weighted value, and a reverse DCF against today's price.
- **Sensitivity**: live WACC × terminal-growth grids for all three scenarios, plus a Base-case tornado.
- **Deals**: values the Apple, Tesla/Terafab and OpenAI deals as extra cash flow on top of the Base case, and tests whether they explain the price.
- **Bear / Base / Bull / Taiwan / TaiwanMax**: identical 2026E–2033 forecasts by segment, discounted to 30 Sep 2026.

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

## Deal overlay: Apple, Tesla/Terafab, OpenAI (added)

Each deal is valued as extra free cash flow *on top of* the Base case. That is generous, because Base already includes $15bn of external foundry revenue by 2033, some of it Apple.

| Deal | Status (Sep 2026) | Peak revenue assumed | Value if certain | Probability | Weighted |
|---|---|---|---|---|---|
| Apple (low-end M-series, 18A-P) | Preliminary deal (WSJ, May 2026) | ~$10bn/yr by 2030 (BofA estimate) | $4.72/share | 70% | $3.30 |
| Tesla/SpaceX/xAI Terafab (14A) | Intel named foundry partner (7 Apr 2026); revenue model undisclosed | ~$6bn/yr by 2033 | $2.88/share | 40% | $1.15 |
| OpenAI | Unconfirmed "design win" report only; its first chip is on TSMC N3 via Broadcom | ~$9bn/yr by 2033 | $2.86/share | 25% | $0.72 |
| **Total** | | | **$10.46** | | **$5.17** |

**Results:**

| | Value per share |
|---|---|
| Base + all three deals at 100% probability | ~$33 |
| Current price | $123 |
| **Gap still unexplained** | **~$90/share (about $496bn)** |

- To close that gap, the deals would need to be **about 9.6×** the sizes assumed here.
- Put another way: the gap equals a new foundry business earning about $59bn a year of FCF from 2031. At TSMC-like 35% FCF margins, that is about **$167bn of extra annual revenue, roughly 104% of TSMC's entire current revenue**.

## China tailwinds (added, switchable on Inputs)

These are the China-related forces that *help* Intel, modeled alongside the China headwinds above:

| Tailwind | Evidence | How it's modeled | Base | Bull |
|---|---|---|---|---|
| 1. China AI-server demand | China server CPU prices up 40%+ since Jan 2026; 6-month lead times; Intel and AMD signing multi-year supply deals with Chinese AI data centers; domestic CPUs can't fill AI-server demand near-term | Extra growth added to China domestic revenue, fading as Hygon/Kunpeng scale | +8% in 2027, +4% in 2028 | +15%, +10%, +5%, +2% |
| 2. US onshoring response to China | Section 232 25% tariff on advanced chips made outside the US (Jan 2026); Phase 2 "build in America or pay" with a 1:1 rule and tariff offsets (Sep 2026) | Extra US-fab foundry revenue. Intel shares this demand with TSMC Arizona and Samsung Taylor | → $5bn/yr by 2032 | → $12bn/yr by 2033 |
| 3. US fab subsidies | 48D 35% refundable credit for fabs started by 31 Dec 2026; SCIP partner co-funding | 10% of gross capex offset (conservative) | All scenarios | All scenarios |

**Impact on value per share:**

| | Bear | Base | Bull | Taiwan | Weighted |
|---|---|---|---|---|---|
| Without tailwinds | $0 | $22.1 | $53.3 | $80.4 | $26.3 |
| + Tailwinds 1 and 2 (China demand, onshoring) | — | $26.1 | $65.1 | — | — |
| + Tailwind 3 (capex offset) alone | — | $23.7 | $55.3 | — | — |
| **All tailwinds (new default)** | **$0** | **$27.7** | **$67.1** | **$83.4** | **$32.2** |

**With tailwinds on:**

| | Value per share |
|---|---|
| Base + all deals certain | ~$38 |
| Base at 8.5% WACC | ~$39 |
| Bull at 8.5% WACC | ~$96 |

The reverse DCF now needs 5.7× Base terminal FCF (it was 6.9×).

To see the model without the tailwinds, set "Tailwind switch" to 0 and the capex offset to 0% on Inputs.

## TaiwanMax scenario (added): Taiwan falls, TSMC Arizona goes to Intel, TSMC engineers join Intel

**Condition.** Taiwan's fabs are destroyed or seized from 2027. The US government transfers TSMC Arizona to Intel, and a large share of TSMC's engineers join Intel. This builds on the Taiwan scenario.

**TSMC Arizona today [R]:**
- Fab 1 makes 10–30k N4 wafers a month.
- Fab 2 (N3) starts volume production in H2 2027. Fab 3 (N2/A16) has had tools going in since Q3 2026.
- TSMC has committed $265bn to six fabs and employs about 3,000 people on site.
- **All Arizona chips are still packaged in Taiwan.** US advanced packaging arrives only in 2028–29 (Amkor, then TSMC). ([TrendForce](https://www.trendforce.com/news/2026/03/24/news-tsmc-reportedly-eyes-2h27-3nm-mass-production-at-arizona-fab-2-four-u-s-fabs-said-to-be-fully-booked/), [Tweaktown](https://www.tweaktown.com/news/106094/tsmc-arizona-chips-being-flown-back-to-in-taiwan-for-advanced-packaging/index.html), [TechTimes](https://www.techtimes.com/articles/316921/20260520/tsmc-arizona-fab-posts-514m-year-one-profit-q1-2026-earnings-surpass-full-2025-figure.htm))

**What's modeled (on top of Taiwan):**

| Driver | Taiwan | TaiwanMax |
|---|---|---|
| External foundry revenue, 2027 → 2033 | $10bn → $70bn | $18bn → $130bn (Intel fabs plus Arizona at crisis pricing; 2027 is packaging-bound) |
| Client revenue in 2027 | −10% | −5% (TSMC-made tiles move to Arizona) |
| Gross margin by 2030 | 62% | 65% (TSMC talent speeds yield and cost) |
| Capex per year | $35–50bn | $55–75bn (finishing the Arizona fabs) |
| Opex growth | 6% | 8% (integrating TSMC Arizona and its staff) |
| Payment for TSMC Arizona | — | $0 by default (government transfer); editable input |

**Results:**

| | Value per share |
|---|---|
| TaiwanMax at 10.4% WACC | **~$130** (above the $123 price) |
| At 8.5% WACC | ~$189 |
| At 12.5% WACC (wartime cost of capital) | ~$93 |
| If Intel pays $100bn for Arizona | ~$112 |
| If Intel pays $150bn for Arizona | ~$103 |
| If foundry revenue is 30% lower | ~$93 |

Revenue reaches about $218bn in 2033, with operating income of about $114bn. FCF is −$32bn in 2027 and −$15bn in 2028, turns positive in 2029, and reaches about $83bn by 2033.

**Break-even test.** The current price requires about a **93% probability** of the TaiwanMax outcome, with the other four scenarios taking the rest.

**Weights:** Bear 28%, Base 43%, Bull 24%, Taiwan 3%, TaiwanMax 2%. That gives a probability-weighted value of **~$33**.

**Not modeled, all of which lower it:**
- a global depression and demand collapse
- US price controls, or Defense Production Act allocation of output
- export bans on ASML and Japanese tools and materials to a war zone
- how long the Taiwan packaging gap would halt Arizona output (the real bottleneck in 2027–28)
- dilution if Intel issues shares for the assets

## What to check before trusting this

1. **China inputs.** FY2025 China revenue is a derived residual, and the 50% domestic-demand share is my judgment. Verify both.
2. **Placeholders.** D&A, stock-based comp, non-controlling interests (SCIP fab partners and the Mobileye minority), and Q1-26 external foundry revenue were not sourceable here. NCI is set to 0, which *overstates* value.
3. **Share count.** It is derived as Q2 non-GAAP net income ÷ EPS, plus the August offering shares; verify it against the 10-Q.
4. **Gross capex.** Partner and government offsets are ignored. The effect on value is small; see the tornado.
5. **Consensus comparison.** Consensus 2027 EPS is about $2.04; the Base case gives about $1.59 before SBC. Consensus sits between the Base and Bull cases.
6. **Scenario drivers are hypotheticals.** They are tied to the product evidence and were fixed before the valuation was computed. They were not tuned toward the market price.
