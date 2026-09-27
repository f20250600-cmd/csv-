# Is the market pricing the AI buildout correctly? Meta and Microsoft

**Valuation date:** 30-Sep-2026. **Prices:** META $747.82, MSFT $516.17 (26/27-Sep closes).
USD bn unless stated. The full auto-generated tables are in [`outputs/model_results.md`](outputs/model_results.md), with a CSV for each.

> **How to read this.** Every number in the scenario and reverse-DCF sections is an output of the model
> in this folder, and every input carries a source tag in `inputs.py`. When I write "if X, the model says
> Y", that is arithmetic. When I write "I think X is (un)likely", that is my judgement, and I say which
> evidence it rests on. No input was set to produce a target price; §2.7 lists every revision made
> while building the model and why.

---

## 0. Bottom line

| | Meta | Microsoft |
|---|---|---|
| Value per share: Bull / Bull-lite / **Base** / Bear-lite / Bear | 832 / 499 / **522** / 340 / 276 | 513 / 380 / **335** / 266 / 235 |
| Where the price sits | 73% of the way from Base to Bull | At the Bull case |
| Value of the non-AI business (core + Reality Labs) | $1,984bn (≈ market cap) | $2,869bn (≈ 75% of market cap) |
| **Market-implied value of the AI layer** | **≈ −$34bn** (AI roughly NPV-neutral) | **≈ +$861bn** (AI strongly value-creating) |
| Model Base-case AI layer NPV | −$612bn | −$486bn |
| AI economic ROIC in 2036, Base (hurdle) | −5.0% (10.5%) | 0.2% (9.75%) |
| AI ROIC the price requires (monetisation solve) | ≈ 6.5% (hurdle − 4pp) | ≈ 15–16% (hurdle + 6pp) |

**Meta.** The price does *not* assume AI creates value. It is roughly what the existing ad business
(ex-AI uplift) plus Reality Labs is worth, with the ~$175–190bn/yr AI programme treated as close to
zero NPV. My Base says the programme destroys about $600bn. The AI ranking and recommendation uplift
to ads is clearly value-creating: IRR about 24% on its own compute. The destruction comes from two
things. Frontier-model/MSL training is a permanent, un-monetised cost of about $80bn a year on an
economic basis. New AI products don't reach enough scale to cover their capacity. To justify today's
price the market needs roughly one of the following:
- AI revenue about 2× my Base (≈ $405bn by 2036), or
- AI responsible for about 40% of ad revenue by 2031 (my Base is 28%; my estimate for today is about 15%), or
- Meta cutting explicit AI capex to about 40% of plan, or
- a WACC of about 8.0% (CAPM with Meta's beta gives ~10.6%).

The most defensible combination is "the ads machine keeps compounding *and* management disciplines the
long-duration bet". For example, an uplift share of 36% plus training spend falling 12% a year after
2029 gets to about $707. **That is plausible, but it is not Base.**

**Microsoft.** The price needs the AI layer to be worth about $860bn, and my Bull case ($513) only
just delivers that. The reason is that my Base AI economics sit around, not above, the cost of capital.
I calibrate revenue per dollar of AI equipment to FY26: about $26bn per GW-year at full utilisation,
which is already about 2× the Oracle–OpenAI contract benchmark. On top of that come 12%/yr price
erosion on ageing GPUs, a 5-year refresh cycle, a ~45% long-lived facility share, a permanent MAI
training cost, and Copilot not earning back its roughly 22% share of AI compute. The price requires
one of the following:
- AI ROIC of about 15–16% (AI revenue ≈ $530bn by FY36 at software-like margins), or
- Copilot/1P AI revenue about 5× my Base (≈ $290bn, more than all of today's Office/commercial ex-AI), or
- core growth 5pp higher every year, or
- a WACC of about 6.9%.

Taken one at a time, each of those is aggressive against history, peers and CAPM. A *combination*
gets to about $528:
- 30% more revenue per GW than FY26,
- 2× Copilot,
- a 6-year economic GPU life,
- 75bp lower WACC.

**The market is paying for Microsoft's AI to be a high-return software business, not a
cost-of-capital infrastructure business.** Today's disclosures don't yet show that, but they don't
rule it out either.

**The key asymmetry.** Meta's price rests on its existing business and largely ignores the AI bet.
Microsoft's price rests on the AI bet paying off at returns well above what current GPU unit
economics show.

---

## 1. Data and provenance

* **Meta:**
  * Q1-26 revenue $56.31bn; Q2-26 revenue $60.8bn (+28%).
  * Q2: FoA OI $23.4bn, RL loss $4.62bn, capex $31.1bn, FCF $0.8bn.
  * Q3 revenue guide $61–64bn.
  * FY26 guidance: expenses $165–169bn; capex $130–145bn, incl. finance-lease principal.
  * FY25: revenue $201.0bn, OI $83.3bn, capex $72.2bn, FCF $43.6bn, RL loss $19.2bn.
  * Balance sheet at 30-Jun-26: cash and securities $90.3bn, LT debt $83.7bn.
  * Plus a $25bn bond in May and the $27bn Hyperion JV.
  * Consensus 2027: capex ~$190bn, EPS ~$31–33.
* **Microsoft:**
  * FY26: revenue $331.8bn, OI $155.2bn.
  * Segments: P&BP $140.0bn / OI $83.9bn; IC $137.8bn / OI $57.0bn; MPC by difference.
  * Azure above $100bn (+41%); Q4 Azure +43%.
  * Capex: $115.9bn cash plus $24.6bn finance leases; FY27 guide ~$175bn reported, after about $15bn moves to operating leases.
  * Datacentre life extended from 15 to 25 years from FY27.
  * Commercial RPO $678bn (+84%), about a third from OpenAI; 30m+ paid M365 Copilot seats.
  * OpenAI: about 27% post-recap, diluted by the $122bn raise at $852bn.
  * Cash and ST investments $76.8bn. Consensus FY27 EPS about $19.96.
* **Benchmarks** (from my knowledge / press, approximate):
  * Oracle–OpenAI: about $60bn/yr for about 4.5 GW.
  * Accelerator content per GW: about $35bn of a roughly $50–60bn all-in cost.
  * H100 rental: about $8/hr in 2023, about $2/hr by 2025.
  * Oracle's reported GPU-rental gross margin: mid-teens.
  * Server book lives: MSFT 6y, GOOGL 6y, AMZN cut to 5y in 2025, META 5.5y.

**Caveat:** SEC/IR sites were blocked from the build environment, so reported figures come from search
summaries of those filings. Items tagged `[R]` should be verified against the 10-Q/10-K.
The least certain of them:
- Meta finance-lease liabilities (assumed $20bn);
- MSFT debt and lease liabilities (assumed $43bn + $70bn);
- MSFT FY26 AI revenue split (my estimate).

---

## 2. Method: the modelling decisions, step by step

### 2.1 Separate the existing business from the AI bet (counterfactual approach)
Each company is valued as **(non-AI core segments) + (Reality Labs, Meta only) + (AI layer) + (non-operating) − (net debt)**.

* **Core** = the business as it would look on its pre-AI trajectory, carrying only maintenance and
  non-AI growth capex.
  * Meta core: ads *minus* the share attributable to AI ranking/recommendation, plus FoA other.
  * Microsoft core has four segments:
    * Azure & server products ex-AI;
    * Office/Commercial ex-Copilot;
    * Windows, devices & search;
    * Gaming.
* **AI layer** = incremental AI revenue, minus every incremental AI cost, minus all AI capex.
  * Meta streams:
    * ads uplift;
    * frontier training / MSL;
    * new AI products and compute resale.
  * Microsoft streams:
    * Azure AI infrastructure, including OpenAI;
    * OpenAI revenue share;
    * first-party AI (Copilot, GitHub, agents);
    * MAI models and training.
* **Calibration.** Core margins are solved so that core EBIT plus modelled AI EBIT reproduces
  2026E/FY26 operating income:
  * Meta: normalised FoA OI of about $107.7bn;
  * Microsoft: IC OI of $57.0bn and P&BP OI of $83.9bn.
  * Result: Meta core margin 58.7%; MSFT Azure-core 47.9% and Office-core 61.6%.
* **Most judgemental input: how much of today's revenue is "AI".**
  * Meta: 15% of 2026 ads, about $37bn. This rests on Meta ads growing about 27% against a digital ad
    market growing about 11%, with roughly 60% of the excess credited to AI.
  * MSFT: Azure AI about $38bn, first-party AI about $7bn, OpenAI revenue share about $3.6bn.
  * Attribution moves value between core and AI. It does not create value.
* **Defensive value is not modelled.** If the core would erode *without* AI spending, part of the AI
  layer's negative NPV is really the price of protecting the core. The break-even is:
  * Meta: AI must be protecting **31%** of core value;
  * Microsoft: **17%**.
  * This is the single most important caveat to the Base results (see §5).

### 2.2 Separate AI capex from maintenance capex, and split AI capex by use and component
* **Core capex vs AI capex.** Core capex is a fixed share of core revenue:
  * Meta: 7% capex, 5.5% D&A. Meta's *total* 2025 D&A was only about 9.7% of revenue.
  * MSFT by segment: Azure-core 24%, Office 6%, Windows 2%, Gaming 3%.
  * AI capex is the rest of reported capex, including finance leases. For MSFT FY27+ it also includes
    capacity that moved to operating leases, because that is still capital employed.
* **AI capex by use.**
  * Meta: 35% ads, 40% training, 25% new products.
  * MSFT: 60% Azure AI, 22% first-party, 18% MAI/R&D.
  * This reflects Hood's comment that first-party and R&D get GPU priority. None of these splits is
    disclosed.
* **AI capex by component.**
  * Meta: accelerators/servers 58%, network 12%, facility 28%, land 2%.
  * MSFT: 45% / 10% / 42% / 3%. Management says about half of FY25–26 spend went to long-lived assets.
  * Refresh capex buys equipment only, into existing shells. Growth capex buys shells too.

### 2.3 Four separate depreciation concepts per vintage
Every year of AI capex is tracked as its own vintage:
- **Book D&A.** Straight line over company policy: servers 5.5y at Meta and 6y at MSFT; facilities
  25y. Shells sit in construction-in-progress for a year before depreciation starts. This drives
  reported EBIT and EPS.
- **Economic depreciation.** Equipment over its *economic* (refresh) life, 3–6y by scenario, net of
  residual value. This drives economic NOPAT and ROIC. If book life is longer than economic life, the
  remaining book value is written off at retirement, which is the EPS hit you'd eventually see.
- **Tax depreciation.** 100% bonus depreciation on equipment (OBBBA) and 39-year straight line on
  buildings. This drives cash taxes. The AI layer's tax losses shelter group profits, so they are
  credited as a cash benefit.
- **Residual value.** Accelerator resale of 2–10% of cost at retirement, depending on scenario.

### 2.4 Capacity, utilisation and demand
* **Capacity streams** (Azure AI; Meta new products / compute resale). Revenue is
  **min(demand, max utilisation × potential)**, where
  potential = Σ vintages × *yield* × ramp × (1 − erosion)^age.
  * *Yield* is revenue per $ of equipment per year at 100% utilisation.
    * MSFT is calibrated to FY26 at 0.74, about $26bn per GW-year, or about $5.9 per GPU-hour at $70k all-in.
    * Meta new products: 0.50 in Base, between the Oracle–OpenAI (0.38) and MSFT (0.74) benchmarks.
  * *Erosion* is the annual price decline of an ageing vintage: 8% in Bull to 22% in Bear.
  * *Drift* changes the yield of new vintages: +2%/yr in Bull, 0% in Base, −6%/yr in Bear.
  * Idle capacity still costs power (fixed part), depreciation and capital. So capex that runs ahead
    of demand shows up as **low utilisation and low ROIC, not as revenue**.
  * Demand that can't be served is lost, not banked.
  * After the explicit period, capex is whatever keeps capacity at an 85% utilisation target.
* **Demand-driven streams** (Meta ads uplift, MSFT Copilot). Revenue comes from the scenario. Compute
  intensity (alive equipment per $ of revenue) is held at its end-of-explicit-period level and improves
  3–5% a year.
* **Cost streams** (training). These are refreshed on a policy after the explicit period: +3%/yr in
  Bull, −5% in Base, −15% in Bear. They carry AI talent and third-party compute contracts:
  * Meta: CoreWeave, Google Cloud, Nebius;
  * MSFT: neocloud leases (Nebius, IREN, Nscale, Lambda), which also add Azure capacity.
* **Power and site operations:** 1.5% of alive equipment cost, plus 2.5% × utilisation. That matches
  about $1.3bn per GW-year.

### 2.5 Returns metrics
* **Book ROIC:** NOPAT on reported D&A ÷ average net book capital.
* **Economic ROIC:** NOPAT on economic depreciation ÷ economic capital.
* **Incremental ROIC:** ΔNOPAT since 2026 ÷ Δcapital.
* **Programme IRR:** all AI cash flows from 2022, *including sunk capex*, plus terminal value.
* **Forward AI NPV** at the AI hurdle: this is the value driver.

### 2.6 Discounting and terminal values
* **Meta:** WACC 9.5%, AI hurdle 10.5%.
* **MSFT:** WACC 8.75%, AI hurdle 9.75%.
* Both WACCs are *below* plain CAPM using the reported betas: 1.28 gives about 10.6% cost of equity
  for Meta, and 1.11 gives about 9.8% for MSFT. That is a deliberately generous choice.
* The +1pp AI premium reflects shorter-lived assets and customer concentration. Removing it *lowers*
  value in Base: when a programme is value-destroying, a lower discount rate makes it worse.
* **Terminal value per stream, with g = 3%:**
  * Revenue streams:
    * value-driver formula if economic RONIC is above the hurdle;
    * no-growth perpetuity if it is between zero and the hurdle;
    * abandonment (zero) if NOPAT ≤ 0.
  * Training: a **permanent cost** growing at g, because staying at the frontier is an ongoing R&D
    expense and the other streams' terminal values assume models keep improving.
  * Reality Labs: zero once losses end. A "losses forever" stress test is available.

### 2.7 Calibration against consensus, and a log of revisions made while building
* **Model year-1 EPS versus consensus:**
  * Meta 2027: $28.76 vs roughly $31–33;
  * MSFT FY27: $18.63 vs about $19.96.
* My Base is about 7–12% below consensus on near-term EPS. It carries more AI cost (talent,
  third-party compute, write-offs) than the Street appears to. It uses operating EPS: no interest
  income and a simplified tax rate.
* **Year-1 revenue** is in line: Meta +15%, MSFT +17%.

**Revisions made during the build:**

| # | Change | Why (evidence, not price) | Direction |
|---|---|---|---|
| 1 | MSFT AI equipment share 70% → 55% | Mgmt: ~half of FY25–26 capex long-lived | Raises calibrated yield (↑) |
| 2 | Meta new-product yield 0.35 → 0.50 | I had derived per-GW revenue from total rather than equipment capex; 0.50 is the midpoint of the 0.38–0.74 benchmarks | ↑ |
| 3 | Demand-driven streams refresh via compute intensity instead of copying explicit capex forever | The old rule locked in any overbuild permanently | ↑ |
| 4 | Azure AI Base growth 42% → 65% in FY27 | Consensus Azure growth in the mid-30s implies AI growing about 65% if non-AI Azure grows 16–17% | ↑ |
| 5 | MSFT Base capex explicit through FY31 (normalising) | The demand rule produced a ~$415bn FY30 spike, which contradicts "Base = capex gradually normalising" | ↓ |
| 6 | Base yield drift −2% → 0% | −2% had no anchor; flat revenue per $ across GPU generations is the neutral assumption | ↑ |
| 7 | Unserved demand is lost, not banked | Avoids an artificial capex catch-up spike | ~ |
| 8 | Per-stream terminal values; training as a permanent cost | A single total-layer "abandon" rule zeroed the profitable ads uplift | ↓ Meta |
| 9 | Meta core capex/D&A 11%/9.5% → 7%/5.5% | Total 2025 D&A was ~9.7% of revenue, so core can't be 9.5% | ~ |
| 10 | MSFT neocloud lease opex scaled to contract sizes | Nebius/IREN/Nscale/Lambda total ~$40–50bn over ~5 years | ↑ |

**Effect of the revisions:** Base moved from $447 to $522 for Meta, and from $335 to $335 for
Microsoft (the revisions offset). Both remain well below the price, so none of this closed the gap.

---

## 3. Meta Platforms

### 3.1 Scenario inputs (the operating assumptions that differ)

| | Bull | Bull-lite | Base | Bear-lite | Bear |
|---|---|---|---|---|---|
| Core ad growth vs Base path (9.5% → 4%) | +1pp | +0.5pp | 0 | −1pp | −2.5pp (plus a 2027–28 ad recession) |
| AI share of ad revenue by 2031 (2026: 15%) | 38% | 33% (by 2033) | 28% | 21% | 12% |
| Explicit AI capex 2027–29 ($bn) | 184 / 216 / 236 | 179 / 216 / 241 | 174 / 186 / 191 | 174 / 180 / 170 | 169 / 134 / 110 |
| New AI product revenue 2030 / 2036 ($bn) | 32 / 110 | 20 / 85 | 17 / 60 | 10 / 32 | 5 / 13 |
| New-product yield / erosion / drift | 0.60 / 8% / +2% | 0.55 / 10% / +1% | 0.50 / 12% / 0% | 0.42 / 16% / −3% | 0.35 / 22% / −6% |
| GPU economic life / residual | 6y / 10% | 5y / 7% | 5y / 5% | 4y / 3% | 4y / 2% |
| Training spend growth after 2029 | +3% | 0% | −5% | −10% | −15% |
| Reality Labs loss 2027 → 2036 ($bn) | −17 → +9 | −18 → +4 | −19 → −2 | −19 → −5 | −20 → −6 |

### 3.2 What each scenario is worth (no probabilities)

| | Bull | Bull-lite | Base | Bear-lite | Bear |
|---|---|---|---|---|---|
| **Value / share** | **$832** | **$499** | **$522** | **$340** | **$276** |
| vs $748 | +11% | −33% | −30% | −55% | −63% |
| Core ads ex-AI ($bn) | 2,278 | 2,146 | 2,051 | 1,853 | 1,521 |
| Reality Labs ($bn) | +5 | −33 | −67 | −79 | −85 |
| AI layer NPV ($bn) | −117 | −801 | −612 | −868 | −695 |
| AI revenue 2030 / 2036 ($bn) | 201 / 371 | 135 / 285 | 123 / 211 | 81 / 126 | 39 / 53 |
| AI economic ROIC 2030 / 2036 | −0.4% / 8.1% | −11.7% / −3.9% | −11.8% / −5.0% | −21.5% / −18.6% | −26% / −25% |
| Monetised utilisation 2030 (new-product capacity) | 46% | 34% | 39% | 38% | 35% |
| Group FCF 2027 / 2030 ($bn) | −42 / 94 | −49 / 24 | −47 / 60 | −54 / 8 | −63 / 6 |
| EPS 2027 / 2030 | 34.2 / 54.1 | 29.3 / 29.8 | 28.8 / 30.7 | 25.1 / 14.0 | 20.0 / 5.7 |

Three things stand out.
- **Bull-lite comes out *below* Base.** Strong demand doesn't help if capex runs ahead of monetisation
  and training spend isn't normalised. That is exactly the "revenue grows but value falls" case.
- **Even Bull doesn't clear the hurdle.** AI economic ROIC is 8.1% by 2036 against a 10.5% hurdle. So
  your Bull definition ("ROIC comfortably above WACC") isn't reached on consensus-anchored inputs.
  §3.6 solves for what that definition requires.
- **Reported EPS and FCF tell different stories.** Base EPS is about flat 2027–29 while FCF is negative
  for three years.

### 3.3 The AI layer in Base: book vs economic, cash taxes, refresh, residual

| $bn | 2026 | 2027 | 2028 | 2029 | 2030 | 2032 | 2036 |
|---|---|---|---|---|---|---|---|
| AI revenue | 37.4 | 55.4 | 76.1 | 99.0 | 122.7 | 158.5 | 211.0 |
| AI EBITDA | 9.2 | 14.0 | 24.2 | 37.4 | 52.6 | 77.1 | 112.6 |
| Book D&A + write-offs | −26.7 | −45.5 | −69.1 | −95.6 | −120.2 | −137.8 | −149.1 |
| **Economic depreciation** | −34.3 | −57.0 | −81.3 | −105.2 | −120.3 | −133.2 | −142.3 |
| AI EBIT, reported | −17.1 | −31.0 | −44.2 | −56.4 | −64.0 | −55.2 | −30.8 |
| Cash-tax benefit (bonus dep.) vs book-tax benefit | 11.6 vs 2.6 | 16.4 vs 4.7 | 16.2 vs 6.6 | 14.8 vs 8.5 | 8.9 vs 9.6 | 9.7 vs 8.3 | 3.1 vs 4.6 |
| AI capex: growth / refresh | 112 / 11 | 161 / 13 | 166 / 20 | 149 / 42 | 80 / 54 | 31 / 119 | 6 / 128 |
| AI FCF | −101 | −143 | −145 | −137 | −68 | −58 | −12 |
| AI economic ROIC | −15.9% | −15.5% | −14.0% | −13.1% | −11.8% | −9.6% | −5.0% |

* **Book life flatters EPS.** Meta's 5.5-year book life against a 5-year economic life overstates
  2027–28 EPS by about **$4 a share (≈14%)** relative to economic depreciation.
* **Bonus depreciation front-loads cash.** It is worth about $9–12bn a year of cash taxes deferred in
  2026–28. It doesn't change economic ROIC.
* **Refresh becomes the dominant capex line.** By 2032, refresh ($119bn) exceeds growth capex. Meta
  does not return to pre-AI capex intensity: capex/revenue is 26% in 2036 against about 20% pre-AI.

### 3.4 How much AI infrastructure can better advertising justify on its own?

| | Bull | Base | Bear-lite |
|---|---|---|---|
| Ads-uplift stream NPV on its own 35% compute share | +$869bn (IRR 40%) | **+$279bn (IRR 24%)** | −$111bn |
| Training/MSL NPV | −933 | −715 | −539 |
| New-products NPV | −52 | −176 | −218 |
| Whole-programme NPV if ads must pay for everything | −184 | −542 | −750 |

* **Ads alone can justify roughly half of the planned AI capex.** The ads-only break-even is about
  **$87bn a year of explicit AI capex, about $105bn total** including core, against the planned
  ~$184bn of AI capex. **The other ~$95bn a year is the long-duration bet.**
* **For the full Base capex plan to pay off with *no* new AI revenue stream**, AI would have to account
  for **39% of ad revenue by 2031**. My Base is 28%, and my estimate for today is about 15%.
* **In Base, new AI products *reduce* value.** At about $4/GPU-hr-equivalent revenue with 12%/yr
  erosion, serving that demand needs more incremental capacity than it pays for. The idle capacity
  bought in 2026–29 is the main cost. Monetised utilisation of that capacity is 9–25% through 2029.

### 3.5 Reality Labs, kept separate
* **Base value is −$67bn.** Losses fall from $19bn to $2bn by 2036, then stop.
* **If losses persist at $15bn a year forever**, subtract about another $50bn. Use the
  `rl_perpetual_loss` knob to test this.
* **Bull RL (+$5bn)** needs glasses/wearables revenue of about $40bn and profitability by 2033.
  **There is no management evidence for this**: 2026 losses are guided "similar to 2025".
* RL is small relative to the AI question: ±$30–40 a share between scenarios.

### 3.6 Reverse DCF: what $748 requires (one assumption at a time, the rest at Base)

| Solve for | Required | Base | Benchmark | Verdict |
|---|---|---|---|---|
| AI monetisation (uplift + new products) | **×2.1** of Base growth: AI revenue $405bn by 2036 (50% of revenue), AI ROIC 6.5% | ×1.0, $211bn | No disclosed AI revenue; Advantage+ run-rate $60bn is gross, not incremental | Aggressive |
| AI share of ad revenue by 2031 | **40%** | 28% | ~15% today (est.); GEM +3–5% conversions, Andromeda +8% ad quality | Aggressive but not absurd |
| Core ad growth, every year | **+2.75pp** (≈ 12% → 7%) | 9.5% → 4% | Digital ad market ~10–12%; Meta 2019–25 CAGR 19% including AI | Aggressive for an *ex-AI* core |
| Explicit AI capex | **×0.42** (~$75bn/yr AI) | ~$184bn/yr | Guidance $130–145bn in 2026; consensus ~$190bn in 2027 | Contradicts guidance |
| WACC | **7.96%** | 9.5% | CAPM at β 1.28 ≈ 10.6% | Aggressive |
| Terminal growth | **5.8%** | 3% | Nominal GDP ~4% | Implausible |
| Core margin | +17pp | 58.7% | — | Implausible |
| Revenue per GW, AI margin, GPU life, erosion, training policy, terminal AI RONIC | No solution alone (max $531–653) | | | These can't close the gap by themselves |

* **Market-implied AI value by WACC:** −$407bn at 8.5%, −$34bn at 9.5%, +$239bn at 10.5%. *The
  market's view of Meta's AI is highly sensitive to what discount rate you think the market uses for
  the core.*
* **Returns-defined scenarios** (§6b of the results file):
  * **Price ≈ AI ROIC 6.5%**, needing AI revenue of about $406bn.
  * AI ROIC at the hurdle (10.5%) gives $866.
  * **Your "Bull as defined" (hurdle + 4pp) needs AI revenue of about $588bn by 2036 and is worth $1,003.**
* **Combinations that reach the price:**
  * uplift 36% + training −12%/yr after 2029 → **$707**;
  * uplift 33% + WACC −50bp → **$673**.

### 3.7 Capex elevated for longer; monetisation delayed

| Change | Value/share (Δ vs Base $522) |
|---|---|
| Capex held at the 2029 level +1 / +2 / +3 years (Base demand) | 485 (−37) / 442 (−80) / 435 (−87) |
| Same, with Bear-lite demand | −19 / −31 / −53 vs Bear-lite |
| Monetisation delayed 1 / 2 / 3 years (capex unchanged) | 478 (−44) / 408 (−114) / 322 (−200) |

**Delay is far more expensive than extra capex.** A 2-year delay costs as much as 3 extra years of
peak capex, because capacity ages and erodes while idle.

### 3.8 GPU life: economic (cash) vs accounting (EPS)
* **Economic life 3 / 4 / 5 / 6 years** → $400 / $458 / $522 / $570. AI refresh capex in 2030 goes
  from $122bn to $27bn.
* **Accounting life 3 → 6 years** → 2027 EPS goes from $20.97 to $29.58, with **FCF and value
  unchanged**. The 5.5-year policy is worth about $8 of reported EPS against a 3-year policy and
  nothing in value.

### 3.9 What actually drives value (tornado, Base, $/share swing)
- Core ad growth ±2pp: **$297**.
- AI share of ads 20% / 36%: $250.
- WACC ±1pp: $227.
- Explicit AI capex ±20%: $156.
- Training policy: $132.
- AI monetisation ×0.6 / ×1.4: $131.
- 2-year delay: $114.
- GPU economic life 4y / 6y: $112.
- Core margin ±4pp: $105.
- AI incremental margin ±10pp: $102.
- Terminal growth ±1pp: $93.
- New-product revenue: $64.
- AI hurdle premium: $26.
- GPU price erosion: $23.

**What this ranking means.** Meta's value is mostly about **(a) the durability of the core ad engine**
and **(b) how much of the ad engine's growth AI can claim**. The GPU-level technicals (erosion,
utilisation) matter much less, because most of Meta's AI spend isn't sold by the GPU-hour.

### 3.10 Assumption scorecard, Meta

| Assumption (Base) | Support | Flag |
|---|---|---|
| 2027 revenue +15%, capex ~$190bn | Consensus / guidance | ✔ consensus |
| Core margin ex-AI 58.7% | Calibrated to 2026E FoA OI; FoA margin was 53.6% in 2024 including early AI cost | Depends on the 15% attribution |
| 15% of 2026 ads due to AI | Meta ads +27% vs market ~11%; GEM/Andromeda test results | **Judgement: undisclosed** |
| Uplift reaching 28% by 2031 | Extrapolation of current excess growth | Judgement; the price needs 40% |
| Capex split 35/40/25 (ads/training/new) | Zuckerberg: "significant portion" to training | **Judgement: undisclosed** |
| Training spend −5%/yr after 2029 | Scenario definition ("normalising") | Judgement; the price is more consistent with ~−12%/yr |
| New-product yield $17.5bn/GW-yr | Oracle–OpenAI ~$13bn; MSFT calibrated ~$26bn | Mid-range |
| 5-year economic life vs 5.5-year book | AMZN cut to 5y; frontier training fleets refresh in 3–4y | Book life is at the generous end |
| 12%/yr price erosion | H100 spot fell ~40%/yr in 2023–25; contracted pricing is stickier | Mild |
| WACC 9.5% | CAPM ≈ 10.6% | Generous to the stock |

### 3.11 Verdict, Meta
* **If** my Base AI economics hold, the math says ~$520: 30% below the price.
* **The market is not wildly optimistic.** It is pricing the ad engine at its current trajectory and
  the AI programme at roughly break-even.
* **I think** the most likely way the price is right is not a new AI revenue stream. It is AI pushing
  the ads share toward 35–40%, together with management capping the long-duration spend after 2028.
  Both are plausible. Neither is in current guidance: capex guidance is still rising, and no uplift
  is disclosed.
* **The unpriced risk is the reverse**: capex elevated past 2029 *and* monetisation delayed
  (−$80 to −$200 a share), which is what Bull-lite looks like.
* **The market is roughly right if you believe management will discipline capex; it is too high if you
  don't.**

---

## 4. Microsoft

### 4.1 Scenario inputs

| | Bull | Bull-lite | Base | Bear-lite | Bear |
|---|---|---|---|---|---|
| Azure AI demand growth FY27 / FY28 / FY30 / FY36 (FY26 ≈ $38bn) | 80 / 55 / 30 / 7% | 70 / 48 / 28 / 6% | 65 / 45 / 24 / 6% | 55 / 28 / 10 / 4% | 45 / 10 / −6 / 3% |
| Copilot / 1P AI revenue FY30 / FY36 ($bn; FY26 ≈ $7bn) | 48 / 100 | 34 / 78 | 32 / 62 | 21 / 38 | 15 / 22 |
| AI capex (explicit, $bn) | 154 / 200, then demand-led | 154 / 195, then demand-led | 154 / 175 / 185 / 190 / 190 | 154 / 160 / 150 | 154 / 125 / 100 |
| Yield drift / erosion / max utilisation | +2% / 8% / 95% | +1% / 10% / 92% | 0% / 12% / 92% | −3% / 16% / 90% | −6% / 22% / 88% |
| GPU economic life / residual | 6y / 10% | 5y / 7% | 5y / 5% | 4y / 3% | 4y / 2% |
| OpenAI revenue share (peak), ends | $27bn, FY33 | $20bn, FY32 | $19bn, FY32 | $10bn, FY32 | $5bn, FY31 |
| OpenAI valuation (stake 23%, 25% haircut) | $1.5tn | $1.1tn | $852bn | $450bn | $150bn |

### 4.2 Scenario values

| | Bull | Bull-lite | Base | Bear-lite | Bear |
|---|---|---|---|---|---|
| **Value / share** | **$513** | **$380** | **$335** | **$266** | **$235** |
| vs $516 | −1% | −26% | −35% | −48% | −55% |
| Non-AI segments ($bn) | 3,184 | 2,973 | 2,869 | 2,547 | 2,218 |
| AI layer NPV ($bn) | +412 | −295 | −486 | −606 | −463 |
| OpenAI stake ($bn) | 259 | 190 | 147 | 78 | 26 |
| AI revenue FY30 / FY36 ($bn) | 252 / 501 | 215 / 415 | 178 / 283 | 123 / 169 | 69 / 81 |
| AI economic ROIC FY30 / FY36 | 6.6% / 12.1% | 1.7% / 5.4% | 3.7% / 0.2% | −6.2% / −9.2% | −10.8% / −13.1% |
| Group FCF FY27 / FY30 ($bn) | 33 / 102 | 26 / 68 | 24 / 93 | 17 / 5 | 10 / 70 |
| EPS FY27 / FY30 | 19.8 / 31.1 | 18.8 / 26.0 | 18.6 / 25.7 | 17.1 / 18.2 | 16.0 / 13.5 |

**Growth without value.** Base AI revenue grows about 6× from FY26 to FY36 ($48bn to $283bn), yet AI
economic ROIC ends near 0%. Over FY27–31 the AI layer consumes $394bn of FCF. Growth at returns at or
below the cost of capital destroys value, and it does so while reported EPS compounds at about 11% a year through FY30.

### 4.3 The AI layer in Base

| $bn | FY26 | FY27 | FY28 | FY29 | FY30 | FY32 | FY36 |
|---|---|---|---|---|---|---|---|
| AI revenue | 48.6 | 80.2 | 116.9 | 150.7 | 178.5 | 225.3 | 283.4 |
| AI EBITDA | 30.2 | 48.9 | 74.6 | 100.6 | 122.9 | 158.6 | 197.7 |
| Book D&A + write-offs | −17.4 | −31.8 | −51.6 | −71.5 | −94.0 | −130.0 | −213.6 |
| **Economic depreciation** | −24.9 | −42.5 | −62.5 | −81.5 | −98.5 | −141.4 | −195.9 |
| AI EBIT: reported / economic | 12.9 / 5.3 | 17.4 / 6.4 | 23.7 / 12.1 | 30.5 / 19.2 | 31.4 / 24.4 | 32.5 / 17.2 | −6.4 / 1.8 |
| AI capex: growth / refresh | 110 / 3 | 149 / 6 | 157 / 18 | 153 / 32 | 128 / 62 | 256 / 92 | 0 / 219 |
| AI FCF | −77 | −98 | −95 | −82 | −67 | −171 | −7 |
| AI ROIC: book / economic | 7.5% / 3.3% | 5.7% / 2.3% | 5.2% / 2.9% | 5.1% / 3.5% | 4.3% / 3.7% | 3.2% / 1.8% | −0.5% / 0.2% |
| Capacity utilisation | 92% | 89% | 91% | 92% | 92% | 87% | 74% |

* **Book vs economic depreciation.** A 6-year book life against a 5-year economic life overstates
  FY27–28 EPS by about **$1.2–1.3 a share (~6%)**.
* **Bonus depreciation.** It defers about $7–10bn a year of cash taxes in FY27–29.
* **Reported vs economic returns.** Reported AI ROIC (5–7%) looks acceptable. Economic ROIC (2–4%)
  doesn't. The FY32 capex bump is the utilisation rule moving from the capped 92% down to its 85%
  target once the explicit period ends. That is a modelling transition, not a forecast of lumpiness.

### 4.4 Does Azure + Copilot + AI services earn back the capex?

| Stream NPV ($bn) | Bull | Bull-lite | Base | Bear-lite | Bear |
|---|---|---|---|---|---|
| Azure AI infrastructure (incl. OpenAI) | +551 (IRR 21%) | +89 (9.5%) | −103 (−5%) | −269 | −210 |
| OpenAI revenue share | +70 | +48 | +45 | +30 | +15 |
| First-party AI (Copilot, GitHub, agents) | +83 (14%) | −152 | −99 | −178 | −130 |
| MAI models & training (permanent cost) | −292 | −280 | −329 | −189 | −138 |
| **Total AI** | **+412** | −295 | **−486** | −606 | −463 |

**Only in Bull do Azure + Copilot generate enough incremental FCF to cover the capex and the MAI
training cost.** The swing factor in Azure AI is **revenue per GW, not demand**. In Base, Azure AI is
capacity-constrained through FY31 (92% utilisation). More demand therefore just means more capex at
the same thin return, which is why the "AI monetisation ×0.6 / ×1.4" bar moves value by only
$22 a share. Revenue per $ of new capacity ±30% moves it by $80.

### 4.5 Does OpenAI change the economics?

| Base variant | Value/share | Δ |
|---|---|---|
| Base | $335 | — |
| No OpenAI revenue share | $329 | −6 |
| OpenAI moves 30% of Azure AI demand elsewhere from FY28 | $332 | −3 |
| OpenAI demand re-priced 15% lower on new capacity | $312 | **−23** |
| Stake worth $0 / at $1.5tn with no haircut | $315 / $362 | −20 / +27 |
| Combined downside (30% shortfall, no rev share, stake $35bn) | $311 | −24 |

**Counter-intuitive but important.** If Azure AI earns close to its cost of capital, losing OpenAI
*volume* barely changes value: capex falls with revenue. What matters is **OpenAI's pricing power over
Microsoft**. OpenAI is about a third of RPO and can now shop compute (Microsoft lost its right of first
refusal), so it can push new-capacity pricing down. That hits every future vintage. The stake
($147bn after haircut, ~$20 a share) and the revenue share (~$45bn, ~$6 a share) are real but small
relative to the $860bn the market implies for AI.

### 4.6 Reverse DCF: what $516 requires

| Solve for | Required | Base | Benchmark | Verdict |
|---|---|---|---|---|
| All AI revenue growth | **×5.1**: AI revenue $526bn by FY36 (49% of revenue), AI ROIC 15.4% | $283bn, ROIC 0.2% | — | Aggressive |
| Copilot / 1P AI | **×5.1**: ≈ $290bn by FY36 | $62bn | 30m paid seats today; ~$290bn > all of Office/commercial ex-AI ($133bn) | **Very aggressive** |
| Core growth, every year | **+5.1pp** (Office ≈ 16%, Azure-core ≈ 17% early) | 11–12% fading to 5% | FY19–26 total revenue CAGR 14.9% *including* AI | Aggressive |
| WACC | **6.86%** | 8.75% | CAPM at β 1.11 ≈ 9.8%; 6.9% needs β ≈ 0.5 | Aggressive |
| Terminal growth | **5.9%** | 3% | — | Implausible |
| Revenue per GW, AI margin, capex scale, GPU life, erosion, training policy, core margin, terminal AI RONIC | No single solution (maximum $341–515) | | | Nothing closes the gap alone |

* **Market-implied AI value by WACC:** $257bn at 7.75%, **$861bn at 8.75%**, $1,285bn at 9.75%.
* **Returns-defined scenarios:**
  * AI ROIC at the hurdle gives $446;
  * **"Bull as defined" (hurdle + 4pp) gives $495**;
  * hurdle + 8pp gives $546.
  * **The price needs AI ROIC of about 15–16%.**
* **A realistic combination that reaches the price:**
  * revenue per GW +30%,
  * Copilot 2×,
  * 6-year economic GPU life,
  * WACC −75bp.
  * Together these give **$528**.

### 4.7 Capex elevated for longer; delay
* **Holding FY31 capex for 1–3 more years barely moves value:** +$8 / +$3 / −$2. Base is
  capacity-constrained, so the extra capacity finds demand, but at about cost-of-capital returns.
* **In Bear-lite the same test gives −$1 to +$1.** This is because the demand rule cuts later capex.
* **Monetisation delayed 1 / 2 / 3 years:** −$17 / −$30 / −$42.
* **Microsoft is less exposed to timing than Meta.** It is more exposed to *pricing*.

### 4.8 GPU life
* **Economic life 3 / 4 / 5 / 6 years** → $310 / $328 / $335 / $363 a share.
* **Accounting life 3 → 6 years** → FY27 EPS goes from $16.37 to $18.63, with value unchanged.
* **Microsoft's 6-year book life is at the top of the peer range.** Amazon moved to 5 years in 2025.

### 4.9 What drives value (tornado, Base, $/share swing)
- WACC ±1pp: **$131**.
- Core growth ±2pp: $117.
- **Revenue per GW of new capacity ±30%: $80.**
- Terminal growth: $63.
- Core margin ±4pp: $58.
- AI incremental margin: $49.
- Explicit capex ±20%: $43.
- GPU economic life: $35.
- Delay: $30.
- Copilot ×0.5 / ×1.5: $26.
- AI demand ×0.6 / ×1.4: $22.
- Erosion: $21.
- MAI training policy: $16.
- OpenAI 30% demand shortfall: $3.
- Max utilisation: $1.

### 4.10 Assumption scorecard, Microsoft

| Assumption (Base) | Support | Flag |
|---|---|---|
| FY27 revenue +17%, capex ~$175bn reported (+$15bn op leases) | Consensus / guidance | ✔ |
| Azure AI ≈ $38bn in FY26, +65% in FY27 | Azure >$100bn (+41%) disclosed; AI split undisclosed; consistent with consensus Azure growth | **Estimate** |
| Revenue per GW ≈ $26bn/yr (yield 0.74) | Calibrated to FY26 | **~2× the Oracle–OpenAI benchmark**: generous |
| Copilot/1P AI $62bn by FY36 | 30m seats; ~33% penetration of ~450m seats at ~$25–30/month | Plausible; the price needs 5× |
| 22% of AI compute to 1P, 18% to MAI/R&D | Hood: 1P and R&D get GPU priority | **Judgement: undisclosed** |
| 5-year economic life, 6-year book | Peers moving to 5y | Book is at the generous end |
| OpenAI stake $147bn (23% × $852bn × 0.75) | Last round $852bn; talks at up to $1.5tn | Judgement on haircut |
| WACC 8.75% | CAPM ≈ 9.8% | Generous to the stock |

### 4.11 Verdict, Microsoft
* **If** Microsoft's AI earns what current GPU-rental economics imply, even at a revenue/GW about 2×
  the Oracle–OpenAI benchmark, the math says ~$335 a share. That is 35% below the price.
* **Today's price equals my Bull case.** It needs the AI layer to become a **high-margin software
  business**: Copilot/agents at several times my Base, *or* materially higher revenue per GW than
  today, *and* longer GPU lives, *and* a discount rate below CAPM.
* **I think** each piece is individually possible. Management's own signals point that way: Azure
  +43% and accelerating, RPO +84%, Copilot seat adds +250%, "efficiency gains" in Azure margins.
  But the **combination** is what's priced.
* **The disclosed evidence** doesn't yet separate AI margins from the rest:
  * Microsoft Cloud gross margin fell to ~66%;
  * AI revenue is no longer broken out;
  * a third of the backlog is one customer who can now buy elsewhere.
* **The market is pricing the optimistic end of a range whose centre, on observable unit economics, is
  well below it.**

---

## 5. What would make this analysis wrong

1. **Defensive value (biggest).** If, *without* AI, Meta's engagement or Microsoft's Office/Azure
   franchises would erode, the right comparison is total value with AI versus total value without it.
   * The AI NPVs here break even if AI is protecting **31% (Meta)** / **17% (Microsoft)** of core value.
   * That is a real possibility, especially for Office in a world of AI-native competitors.
2. **AI pull-through to the core isn't credited.** For example, storage and databases attached to AI
   workloads, or AI-driven E5→E7 upgrades if those sit in core growth. This favours the AI case.
3. **Attribution.** The 15% (Meta) and $49bn (MSFT) of "AI revenue today" are my estimates. More AI
   attribution raises AI value but lowers core value by a similar amount.
4. **Compute fungibility.** Idle new-product capacity at Meta could replace some training refresh.
   Not modelled; my rough estimate is on the order of $10–20 a share.
5. **Inference efficiency.** Compute per $ of revenue improves 5% a year in Base. Faster gains lower
   refresh capex.
6. **Near-term EPS.** My Base is 7–12% below consensus year-1 EPS, so my cost load is heavier than the
   Street's.
7. **Data.** Several balance-sheet items are estimates (see §1).

## 6. Where the model points you to look next (the disclosures that would move it most)

* **Meta**
  * Any quantification of AI-driven ad revenue: conversion lift × share of spend.
  * The 2027 capex guide and whether training compute gets carved out or capped.
  * Monetisation of Meta AI (ads in AI surfaces, business agents).
  * Compute-resale pricing if the cloud business launches.
* **Microsoft**
  * Azure AI gross margin, or revenue per GW if disclosed.
  * Copilot ARPU and seat growth.
  * The pricing terms on OpenAI's $250bn commitment and the RPO ex-OpenAI.
  * The split of long-lived vs short-lived capex going forward.
  * Any change to server useful lives.
* **Both:** the actual GPU refresh cadence (economic life), which is the one "technical" input that
  moves value by $35–170 a share.
