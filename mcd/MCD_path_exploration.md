# McDonald's (MCD): exploring the paths before picking a thesis

*As of Sep 27, 2026. Price used: **$236.50** (close Sep 25/26). Model: [`mcd_model.py`](mcd_model.py), full output: [`model_output.md`](model_output.md).*

This note does not start from a view. It shows where the business stands, what the franchise economics are, what a "no heroics" floor is worth, what each path would need to be true, and what the current price already assumes. Where a number is my estimate and not a disclosed figure it is marked **[EST]**.

---

## 0. Findings in brief

1. **The stock is about 31% below its all-time high** ($341.75 on Mar 2, 2026), and it dropped 4.8% on the Sep 23 NEXT investor day. The multiple fell from ~26x to ~18.5x 2026E EPS. Earnings didn't collapse. Three things changed: US traffic weakened (US comps went +6.8% → +3.9% → +0.8% → "slightly negative" in Q3), management put in a multi-year reinvestment that is mostly **rent relief to franchisees**, and the **10-year Treasury is at 5.17%**.
2. **The franchise is a toll on ~$148B of system sales.** MCD keeps roughly **8.9 cents of operating income per system-sales dollar**. That toll is protected on the way down: rent and royalties are a percent of sales, and franchisees absorb cost inflation. The past 2–3 years showed its limit. Franchisee cash flow eroded until MCD had to hand some of the toll back. **NEXT is that hand-back**: ~$5B through 2030 and $8.5B through 2036.
3. **Mature floor (flat traffic, ~2% comps, management's unit plan trimmed slightly, most rent relief sticky): ~$223/share at an 8.5% required return.** The range is $206–$243 across 9%–8%. The price is about 6% above that floor midpoint.
4. **The current price does not require heroics.** At an 8.5% hurdle, $236.50 ≈ management's unit + G&A plan delivered with only **~1.1% average comps**. On the stricter floor template it needs ~2.7% comps. But it offers **no margin of safety versus the floor unless you accept a hurdle of ~8% or less**, and with a 5.2% risk-free rate that is a real question.
5. **"Margin expansion" to low-to-mid-50s% is mostly accounting mix.** Refranchising from 95% to 98% on its own lifts operating margin % by roughly 7–8 points [EST]. In every path I modeled, **operating income per dollar of system sales falls through 2030**, because rent relief outweighs the G&A savings. The 250 bp restaurant-level efficiency mostly goes to franchisees. For MCD shareholders NEXT pays off only if it lifts sales.
6. **Per-share growth is about half business, half capital structure.** In the "mature + plan delivered" path, EPS grows ~5%/yr. Roughly 3.8 pts come from the core business, 2.2 pts from buybacks (about a third of them debt-funded), and about –1.0 pt from rent relief net of G&A savings, refranchising and higher interest. The 2015–2019 era of 13% EPS CAGR on 6% operating income growth can't repeat: leverage is already ~2.5x EBITDA, taxes are at 21%, and new debt costs ~5.5–6%.
7. **Value swings on three things.** The discount rate: ±0.5 pt ≈ ±9%. Comps: ±1 pt/yr ≈ ±9%. Terminal growth: ±0.5 pt ≈ ±8%. Unit growth, G&A and the rent-relief schedule each move value only 2–4%. **The debate is really about US traffic and the right hurdle rate.**

---

## 1. Where the business actually stands

### Scale and model
- **45,356 restaurants** at end-2025, now >46,000. About **95% are franchised**.
- **Systemwide sales (SWS) >$139B** in 2025, up 5% in constant currency. My 2026E is ~$148B: Q1 ~$34B, Q2 $37B.
- There are three franchise structures, and each gives MCD a very different take:

| Structure | Who owns real estate | What MCD collects | Approx. take of that sales $ |
|---|---|---|---|
| Conventional franchise (US, IOM) | MCD mostly owns or leases land/building | Rent + royalty (4% historically, **5% on new/renewed US agreements**) | ~15–19% of sales [EST from 2025 segment franchised revenue] |
| Developmental licensee (IDL, incl. China at 48% equity stake) | Licensee | Royalty only | ~4–5% of sales [EST] |
| Company-operated (~5% of units) | MCD | Full restaurant P&L | ~15–16% restaurant margin |

- 2025 franchised revenues were **$16.55B** (US $7.37B, IOM $7.28B, IDL $1.90B). Company-operated sales were **$9.25B** (US $3.12B, IOM $6.13B). Franchised margins are roughly 82–83% of franchised revenue and **~90% of restaurant margin dollars**.

### Recent results

| | FY2025 | Q1-26 | Q2-26 | Q3-26 (guided) |
|---|---|---|---|---|
| Global comps | ~+3% (Q4: +5.7%) | +3.8% | +1.3% | — |
| US comps | +2.1% (Q4: +6.8%) | +3.9% | +0.8% (guest counts negative) | "slightly negative" (Jul–Aug negative, Sep expected positive) |
| Revenue | $26.9B | $6.51B | $7.10B | |
| Operating income | $12.4B (46.1%) | +12% | $3.34B (+3%) | |
| Diluted EPS | $11.95 GAAP / $12.20 adj. | $2.78 | $3.32 GAAP / $3.38 adj. | |
| FCF | $7.2B (CFO $10.6B – capex $3.4B) | | | |
| Returned | $7.1B ($5.1B dividends, $2.0B buybacks) | | ~4.2M shares bought in H1 (Q2 at ~$289 avg) | |

- **Loyalty:** $40B trailing-twelve-month sales to loyalty members (+20%), with nearly 220M 90-day active users. The old 2027 target was 250M users and $45B.
- **Consumer:** low-income traffic has fallen nearly double digits for two years. Management blames elevated gas prices, which it tied to the US–Iran conflict, and "sticky" inflation. **The CEO's baseline is "industry traffic growth in our wholly owned markets will be flat while inflation remains elevated."**
- **The value push has been costly.** The McValue platform with an under-$3 menu launched with franchisees resisting. The National Owners Association (NOA) survey found 95% of operators saw lower Q1-26 profitability. About 8 in 10 said cash flow can't fund required reinvestment. They also estimated discounts cost the system ~$310M in one quarter. The franchise disclosure document (FDD) figure for a $3.2M-sales traditional restaurant, operating income before occupancy, slipped from $812K to $795K.

### 2026 guidance (from Q4-25 and reiterated)
- ~2,600 openings / ~2,100 net adds. Units add **~2.5% to SWS growth**.
- Operating margin **mid-to-high 40s%**.
- Capex **$3.7–3.9B**.
- Interest expense +4–6%, tax rate 21–23%, G&A ~2.2% of SWS.
- FX tailwind +$0.20–0.30/share.
- My 2026E adjusted EPS is **~$12.80**. Consensus was ~$13.0 before Q3 guidance.

### Valuation snapshot

| Metric | Value |
|---|---|
| Market cap / EV | ~$169B / ~$208B (net financial debt $39.1B) |
| P/E 2026E | **18.5x** (10-yr avg trailing ~26x) |
| EV/EBITDA 2026E | 13.4x; net debt/EBITDA ~2.5x |
| FCF yield 2026E | 4.4% |
| Dividend yield | **3.26%** ($7.72 run-rate after the 50th consecutive raise, +4%) |
| Earnings yield vs 10-yr UST | **5.4% vs 5.17%**. In 2019 it was ~4% vs ~1.9%. |

The last row matters. **On P/E the stock is at a 4-year low, but measured against bond yields it is more expensive than in 2019.** The de-rating tracks rates as much as MCD-specific news.

---

## 2. NEXT: what management actually committed to (Sep 22–23, 2026 investor day)

| Area | Commitment |
|---|---|
| Margin | Adj. operating margin **low-to-mid 50s% by 2030** (from mid-to-high 40s) |
| Cash | FCF conversion **mid-to-high 80s% by 2030** (from low-to-mid 80s) |
| G&A | **2.2% → ~1.9% of SWS by 2030** (tech/AI) |
| Units | Net unit growth **~4.5% in 2027, ~3–3.5%/yr 2028–30**. SWS contribution **~2.5% → ~2% by 2030**. **>550 US+IOM openings/yr** (vs ~750 in 2026). 50,000 units now in 2028 (was 2027). RBC called the unit outlook *below* consensus. |
| Mix | Franchised **95% → ~98% by end-2028** |
| Capex | **~$3B/yr baseline 2027–30** plus **$1.5–2B cumulative capital support** |
| Franchisee support | **~$8.5B through 2036, ~$5B through 2030**. Roughly **60–70% of the 2030 amount is rent relief** (forgone revenue), the rest capital. |
| Restaurant economics | **~250 bp gross restaurant-level efficiency ≈ $100K/yr cash flow per avg US restaurant**. Franchisee payback ~4 yrs after support (on ~$800K incremental investment). **MCD's own payback 5–6 yrs.** |
| Demand | +1.5 pts share in chicken **and** beverage by 2030 while holding beef leadership. Hand-breaded chicken, protein/GLP-1 items, new design, ArchIQ/Archy AI ordering, largest crew retraining ever. |
| Returns | Dividend payout **50–60% of EPS**. Buybacks from the remaining FCF. |
| Franchise terms | New 20-yr terms "**earned, not given**". Following pricing recommendations is expected to count at renewal. |

**What was not given** (in the reporting I could access): an explicit comp target, an EPS growth algorithm, and the year-by-year rent-relief schedule. Analysts' reads: BMO sees EPS dilution of ~1% in 2027–28 and 2–3% by 2030. JPM says rent relief "may more than offset" the G&A savings in 2028–30. JPM cut its target to $260, RBC to $285, and BTIG and UBS also cut.

**The honest read of NEXT:** management is *not* assuming a traffic recovery in its baseline. It is spending part of MCD's toll to restore franchisee economics, betting that healthier operators with better restaurants win share. That is a defensive reinvestment with an offensive option attached.

---

## 3. Franchise economics: what you are actually paying for

### A typical US restaurant (~$4.0M AUV), approximate split

| Line | $/yr | % sales | Note |
|---|---|---|---|
| Rent + royalty to MCD | ~$600K | ~15% | top-line based; minimum rents |
| Marketing co-op | ~$160K | ~4% | |
| **Franchisee cash flow** | **~$500K** | **~12.5%** | per investor day; before debt service and reinvestment |
| Food & paper, labor, other opex | ~$2.7M | ~68% | where inflation hits |

**MCD collects more per restaurant than the operator keeps.** That drives three dynamics:

1. **Asymmetric downside protection for MCD.** A 3% sales decline costs MCD ~3% of that store's rent and royalty, about $18K. With ~40% contribution margin, the franchisee's cash flow falls ~$50K, roughly **–10%**.
2. **Price-led comps pay MCD in full; franchisees gain only if price beats cost inflation.** From 2022–25, menu prices rose ~40% vs 2019, which lifted MCD's take. Franchisee margins were squeezed, and value perception broke ("Big Mac inflation").
3. **The toll has a ceiling set by franchisee viability.** Once ~80% of operators say cash flow can't fund required remodels, the franchisor has to reinvest (rent relief, capital) or accept slower openings and weaker execution. **NEXT is that ceiling being hit.**

### What NEXT does to the split [EST]
- Rent relief at peak is ~$1.0–1.25B/yr. That is ~1% of US+IOM system sales, which lifts franchisee cash-flow margin by roughly 1 pt, from about 12.5% to 13.5%.
- The 250 bp efficiency target adds another 2.5 pts if delivered, taking franchisee cash flow to ~$600K+ per restaurant. **Franchisee cash flow could rise ~25–30%. MCD's operating income falls ~7–8% at the peak before any sales lift, or ~5% net of G&A savings.**
- **MCD's payback needs a sales lift.** ~$5B across ~25K US+IOM restaurants is about $200K each. At a ~16% take, a 5–6 year payback needs **~$220–240K/yr of extra sales per restaurant, ~5–6% of AUV** versus the counterfactual. That is **~1–1.5 pts of extra comps per year for ~4–5 years**, which is exactly the gap between paths C and D below.

### Unit economics: why unit growth is worth less than it looks
- **US/IOM new units:** MCD funds land and building, ~$3.5–4M each (most of 2026's $3.7–3.9B capex covers ~750 openings). At ~$4M AUV × ~15% take, less occupancy/depreciation, the pre-tax return is ~11–12%, about **9% after tax vs ~7–7.5% WACC**. That creates value, but the spread is modest.
- **Developmental-licensee units:** no MCD capital. ~4–5% royalty on a lower AUV (China-heavy) is ~$75–100K/yr each, plus 48% of China JV profit.
- So 4.5% unit growth becomes only ~2.5% SWS growth, and roughly ~2% operating income growth (model: 0.9x the SWS contribution). Per point, comps are worth ~1.5x units to MCD because they need no capital and carry operating leverage.
- **Flag:** management's plan of 2–2.5% SWS from units is well **above MCD's 2015–2019 history of ~1–1.5%/yr net unit growth**. It relies heavily on China and licensees.

---

## 4. The base floor: a very good, mature franchise, no heroics

**Path B assumptions:**
- Comps 2.0%/yr, i.e. flat traffic and ~2% price, which is below MCD's long-run ~3–4%.
- Management's unit contribution trimmed by 0.25 pt.
- Half the G&A savings.
- Rent relief as planned, with $0.7B/yr of it permanent.
- A structural cost drag of 0.75%/yr (calibrated to 2024–25).
- Terminal growth 2.5% nominal.

| | 2026E | 2027E | 2028E | 2030E | 2031E |
|---|---|---|---|---|---|
| SWS ($B) | 148 | 154 | 161 | 174 | 180 |
| Adj. operating income ($B) | 13.2 | 13.4 | 13.5 | 14.1 | 14.9 |
| Op margin % | 46.6% | 49.7% | 53.9% | 53.7% | 54.5% |
| OI / SWS (take) | 8.92% | 8.67% | 8.38% | 8.11% | 8.30% |
| EPS | $12.82 | $13.08 | $13.42 | $14.48 | $15.76 |
| FCF ($B) | 7.4 | 7.9 | 8.0 | 8.3 | 9.1 |

| Required return | 8.0% | 8.5% | 9.0% |
|---|---|---|---|
| **Floor value/share** | **$243** | **$223** | **$206** |

- IRR if bought at $236.50: **6.7%** with a 16.5x exit, 8.3% at 18x.
- If management's unit and G&A plan is fully delivered with comps still at 2% (path C), the "mature floor with plan delivered" is **$254** ($233–$280).

**Why the floor isn't much lower:** even with flat traffic, ~2% price plus ~2% from units gives ~4% SWS growth, and MCD's cut is top-line. The real floor risks:
- **Franchisee economics break further**, forcing more relief and a permanent take-rate cut (path A).
- **A 2014–15-style traffic slump.** The deep-stress case, with comps –1%/–0.5% in 2027–28, gives **~$171**.

**Flag:** the floor is more sensitive to the discount rate than to anything operational. Moving from 8.5% to 8% adds $20. With the 10-yr at 5.17%, an 8.5% hurdle is only a ~3.3 pt premium.

---

## 5. The paths: what would have to be true

Each line reads "*if* X, the math says Y." None of these is a forecast. My read on the current evidence is labeled separately.

| Path | What has to be true | EPS 2027 / 2031 | EPS CAGR | Value @8 / 8.5 / 9% | IRR @ $236.50 (exit P/E) |
|---|---|---|---|---|---|
| **A. Value problem persists** | Comps 0.5% → 1.5%, traffic keeps falling, discounts don't pay back, relief 25% above plan with $0.9B permanent, openings slow | $12.60 / $13.75 | 1.4% | $198 / **$182** / $169 | 2.2% (15x) |
| **A′. Deep stress** | As A, but comps –1% / –0.5% in 2027–28 | — / $12.83 | ~0% | **$171** @8.5% | ~0% (14x) |
| **B. Mature floor** | Comps 2%, units slightly below plan, half G&A savings, most relief permanent | $13.08 / $15.76 | 4.2% | $243 / **$223** / $206 | 6.7% (16.5x) |
| **C. Units carry it, comps modest** | Management's unit and G&A plan fully delivered, comps stay ~2% | $13.18 / $16.35 | 5.0% | $280 / **$254** / $233 | 9.0% (17.5x) |
| **D. NEXT works (≈ mgmt plan)** | Comps 3%: traffic +0.5–1% plus ~2–2.5% check. Relief fades after the remodel wave. | $13.42 / $18.00 | 7.0% | $310 / **$281** / $258 | 13.1% (19x) |
| **E. NEXT + value leadership** | Comps 3.5–4%: traffic +1.5–2%, share gains in chicken and beverage, healthier franchisees open more | $13.56 / $19.45 | 8.7% | $351 / **$318** / $290 | 17.1% (21x) |

**IRR at today's price by exit P/E (end-2031, on 2032E EPS):**

| | 14x | 16x | 18x | 20x | 22x |
|---|---|---|---|---|---|
| A | 1.0% | 3.4% | 5.5% | 7.5% | 9.3% |
| B | 3.7% | 6.1% | 8.3% | 10.3% | 12.2% |
| C | 4.8% | 7.3% | 9.5% | 11.6% | 13.5% |
| D | 7.2% | 9.7% | 12.0% | 14.1% | 16.0% |
| E | 9.0% | 11.6% | 13.9% | 16.1% | 18.0% |

### 5a. What if unit growth drives growth? (path C)
- *If* management delivers 4.5% → 3% net unit growth, the math gives ~2.5% → 2% of SWS, ~2% of operating income growth a year, and ~$254/share with comps at only 2%.
- Adding **+0.5 pt to unit contribution is worth only ~+3% of value.** Most new units are licensee units at ~4–5% royalty, and US/IOM units need MCD capital at ~9% after-tax returns.
- *Evidence today:* management *cut* the US/IOM opening pace (>550/yr vs ~750) and pushed 50K units to 2028. Licensee growth, China especially, has been reliable. Unit growth looks **necessary but not sufficient**: it keeps the floor intact but can't carry a re-rating on its own.

### 5b. What if comps remain modest? (paths B/C)
- *If* comps average 2%, EPS grows ~4–5%/yr and total return is ~7–9%, depending on the exit multiple.
- Each **±1 pt of comps every year ≈ ±$20/share (±9%)**, and ≈ ±$0.20–0.22 of EPS per year of impact. Comps are the single most valuable operating variable.
- **Flag:** 2% comps is below MCD's long-run average of ~3–4% and roughly in line with its 2024–26 run-rate. **This is the path management's own "flat traffic" baseline points to.**

### 5c. What if NEXT improves restaurant productivity and margins? (path D)
- *If* NEXT adds ~1 pt/yr of comps (traffic back to +0.5–1%), MCD earns its 5–6 yr payback and the value is ~$281. EPS compounds ~7% even after rent relief.
- The **250 bp efficiency goes to franchisees**, not MCD's P&L (company-operated units are going to ~2%). For MCD shareholders NEXT only pays through **sales**: traffic, share, and pricing power that franchisees can finally afford.
- *Evidence today:* none yet. The program starts in 2027–28 and the remodel cycle runs ~10 years. MCD has a record of operational turnarounds: around the 2015 all-day-breakfast relaunch, global comps went from about –2% in early 2015 to about +5% by Q4 2015. The counter-evidence is that the 2024–26 value pushes (the $5 meal deal, McValue, under-$3) bought traffic only briefly, and franchisees say the discounts didn't pay back.

### 5d. What if consumer weakness and value perception stay a problem? (paths A/A′)
- *If* traffic keeps eroding and MCD has to pay more to keep operators whole, the take rate falls to ~7.7–7.9% of SWS by 2030 (from 8.9%). EPS barely grows (1.4%/yr) and the value is **$171–$182** (–23% to –28%). At a 15x exit, the 5-yr IRR is ~2%.
- *Evidence today:* this is what the last 12 months looked like. Low-income traffic is down ~double digits for two years, US comps went from +6.8% to slightly negative in three quarters, franchisee surveys are dire, and the CEO says conditions are "not expected to change." There are also GLP-1 headwinds to frequency. **The stock has already priced part of this path; it has not priced all of it.**

### 5e. What if NEXT plus value leadership work together? (path E)
- *If* traffic returns to +1.5–2% and share gains in chicken and beverage land, the value is ~$318 and the IRR is ~17%. Even here, the March-2026 high (~$342) is only regained around end-2028 or 2029 at a 21x multiple. That high was pricing this path, or better.
- **Flag:** traffic of +1.5–2% has not been sustained in the US since the late-2010s refresh. This path needs a *demand* inflection that hasn't started.

---

## 6. How much can margin expansion contribute?

**Less than the headline suggests. In operating-income dollars, NEXT is a net cost through 2030 in every path I modeled.**

| Component (2030E, path C) | Operating income effect | Op margin % effect |
|---|---|---|
| Refranchising 95% → 98% | ~–$0.2B/yr (lost company-op margin > new rent/royalty) | **~+7–8 pts** (removes ~$5–6B of low-margin company-op sales from revenue) |
| G&A 2.2% → 1.9% of SWS | **+$0.53B** | +2 pts |
| Rent relief | **–$1.25B** | –2 to –3 pts |
| Net NEXT items | **–$0.7B (~–5% of OI)** | margin % still rises to ~55% |

- The model reproduces management's **low-to-mid-50s% margin** in the *modest-comp* paths B and C (54–55%). That means **the margin target doesn't require a turnaround, and hitting it tells you little about the business.**
- The number to watch is **OI ÷ SWS**, the toll rate. It falls from **8.92% (2026E) to ~8.1–8.5% (2030E)** in paths B–D and only recovers partly in 2031 as relief peaks and fades.
- The only *true* margin lever for MCD's own dollars is G&A (~+4% of OI if fully delivered). There is a slower lever as well: the royalty rising from 4% to 5% as 20-year agreements renew, worth ~+$25M/yr per year of renewals [EST], about 1% of OI by 2031.
- Margin expansion lifts value only if management gets G&A down without the rent relief becoming permanent. That is the difference between "rent relief fades to $0" (+4% value) and "1.5x plan, $1.2B permanent" (–4%).

---

## 7. Business growth vs buybacks, dividends and financial engineering

### Forward (2026E → 2031E), annualized contributions to EPS growth

| Path | Core business | NEXT items (G&A – rent relief) | Refranchising | Interest drag | Buybacks | **EPS growth** | Buybacks funded by FCF / new debt / refranchise proceeds |
|---|---|---|---|---|---|---|---|
| A | 2.1% | –1.3% | –0.3% | –0.4% | 1.4% | **1.4%** | 73 / 15 / 12% |
| B | 3.6% | –0.8% | –0.3% | –0.4% | 2.0% | **4.1%** | 65 / 28 / 8% |
| C | 3.8% | –0.4% | –0.3% | –0.4% | 2.2% | **4.9%** | 62 / 31 / 7% |
| D | 5.3% | –0.4% | –0.3% | –0.3% | 2.5% | **6.8%** | 57 / 37 / 6% |
| E | 6.5% | –0.3% | –0.3% | –0.3% | 2.7% | **8.3%** | 54 / 41 / 5% |

The core business line is comps plus units minus the cost drag. The buyback line assumes buybacks at a constant ~18.5x P/E.

How to read it:
- **Buybacks are not a separate source of value.** At a fair price they only turn the FCF yield into per-share growth. The real value sources are:
  1. the **FCF yield (~4.4%)**;
  2. **growth of that cash flow (the business)**;
  3. **leverage**, i.e. debt growing with EBITDA at ~2.5x, which adds ~0.8–1 pt/yr of distributable cash;
  4. any **re-rating**.
- **Total return in path C** ≈ 3.3% dividend yield + ~5% EPS growth + the multiple change. About 0.8–0.9 pt of the EPS growth comes from debt-funded buybacks and asset-sale proceeds, which is the "financial engineering" share. That is ~38% of the 2.2 pt buyback contribution.
- **Rates matter more now.** Debt-funded buybacks earn the spread between the earnings yield (~5.4%) and the after-tax cost of new debt (~5.6% × 0.785 ≈ 4.4%). That is a thin ~1 pt spread, versus ~3 pts in 2015–19. MCD's ~3.9% average cost of debt also reprices upward as bonds mature (modeled at +12 bp/yr), which costs ~0.3–0.4 pt/yr of EPS growth.
- **Buyback price discipline:** MCD bought ~4.2M shares in H1-26 at ~$290 (~22–23x). The same dollars now buy ~23% more shares.

### History: the 8–10% EPS "compounder" memory was partly one-off

| Period | Operating income CAGR | EPS CAGR | Share count/yr | What else happened |
|---|---|---|---|---|
| 2015 → 2019 | ~6% ($7.1B → $9.1B) | **~13%** ($4.80 → $7.88) | **~–5%** | Refranchising 81% → 93%, US tax cut (~31% → ~25%), debt ~$24B → ~$34B at ~3% rates |
| 2019 → 2025 | ~5.3% ($9.1B → $12.4B) | ~7.2% ($7.88 → $11.95) | ~–1% | ~40% menu price inflation, debt ~$34B → ~$40B |
| 2026E → 2031E (paths B–D) | ~2.5–4.7% | ~4–7% | ~–2% | NEXT rent relief, 95% → 98% refranchising, rising debt costs |

The business has compounded operating income at ~5–6% nominally, with the help of an unusually inflationary 2021–24. None of the three EPS boosters from 2015–19 (big refranchising, a tax cut, cheap re-leveraging) is available at the same scale today.

---

## 8. What the current price already assumes

1. **Multiple:** 18.5x 2026E and ~18x my 2027E (~$13.1–13.2). An earnings yield of ~5.4% roughly equals the 10-yr Treasury. My 2027E is ~5–6% below the pre-investor-day consensus of ~$14.0. The gap is my rent relief (~$0.3B in 2027), refranchising dilution and a calibrated cost drag. If the Street converges to ~$13.3–13.5, the true forward multiple is ~17.5–18x, not ~17x.
2. **Reverse DCF:** the constant comps that equate the DCF to $236.50:

| Required return | With mgmt unit & G&A plan (template C) | On the floor template (B) | Terminal growth needed on floor template |
|---|---|---|---|
| 8.0% | **~0%** | 1.7% | 2.3% |
| 8.5% | **~1.1%** | 2.7% | 2.9% |
| 9.0% | **~2.2%** | 3.6% | 3.4% |

3. **The price as a mix of paths (at 8.5%):** ≈ 45% "value problem persists" + 55% "NEXT works", or ≈ 77% floor + 23% NEXT works. An equal weighting of A–E gives ~$252.
4. **In plain terms:** the market is pricing **roughly the mature-floor-to-modest path at an ~8–8.5% required return**. It is not paying for NEXT to work, and it is not pricing a structural decline. **Whether the market is wrong comes down to two questions:**
   - **Do you believe average comps over 2027–31 will be meaningfully above ~2%?** That requires US traffic to stop falling. Management's own baseline says it won't while inflation stays high.
   - **What return do you require from a low-beta franchise when Treasuries yield 5.2%?** At 8% the stock is modestly cheap to the floor; at 9% it is modestly expensive to it.

### Flags (per your rules)
- **Assumptions materially above history:** management's unit contribution (2–2.5% vs ~1–1.5% historically); path E traffic (+1.5–2%); any exit multiple ≥20x while the 10-yr is above 5% (the 10-yr average P/E of ~26x came with a ~2–3% 10-yr).
- **Assumptions materially below history:** 2% comps (paths B/C) and the ~0–1% comps the reverse DCF implies at an 8–8.5% hurdle.
- **Small changes that flip the conclusion:** the discount rate. At 8% the floor ($243) is above the price; at 9% ($206) it is 13% below. A 1 pt/yr comp change moves value ~9%. An 18x vs 16x exit multiple changes the floor IRR from 6.1% to 8.3%.

---

## 9. Signposts that separate the paths (next 4–6 quarters)

| Signal | Points toward A/B | Points toward D/E |
|---|---|---|
| US **guest counts** (not comps) in Q4-26, which laps +6.8% | Negative again; check growth from mix and price only | Flat to positive without a deeper discount |
| Franchisee health (NOA surveys, remodel uptake, openings pace) | Continued "cash flow insufficient"; openings below 550 | Operators opting in early; US/IOM openings ≥550 |
| **Rent relief in franchised margins** (2027+) | Bigger or earlier than ~$0.3B in 2027; extended | In line with plan and tied to remodels with an end date |
| OI ÷ SWS (toll rate) | Falling below ~8.3% before 2029 | Holding ~8.5%+ |
| G&A % of SWS | Stuck ~2.2% | Tracking to 2.0% by 2028 |
| Chicken/beverage share, loyalty actives | Stalled below ~230M | Clear share gains; loyalty toward 250M |
| 10-yr Treasury | Stays >5% (caps the multiple) | Falls toward 4% (supports re-rating even on path C) |
| Capital allocation | Debt-funded buybacks at a thin spread; payout creeping above 60% | Buybacks funded mostly by FCF growth |

---

## 10. Model mechanics and limitations

- **Operating income:** core operating income grows at 1.3 × comps + 0.9 × unit contribution + cost drag. The coefficients come from the franchised revenue structure (rent/royalty on the top line against largely fixed occupancy costs) and were roughly calibrated so 2024–25 reproduce actual operating income growth. Rent relief, G&A savings and refranchising are layered on explicitly in dollars.
- **Balance sheet and cash:**
  - Net debt is held at ~2.5x EBITDA.
  - The interest rate on net debt rises 12 bp/yr.
  - Tax is 21.5%.
  - Dividends are ≥60% of EPS with at least 2% annual growth.
  - Buybacks are the residual of FCF + net borrowing + refranchising proceeds − dividends, executed at a constant P/E.
- **Valuation:** an equity DCF on FCFE (FCF + net borrowing + refranchise proceeds) with a normalized 2032 terminal, divided by today's share count. The IRR view uses dividends plus an exit at a forward P/E.
- **[EST] items** that management has not disclosed:
  - the annual rent-relief schedule (I used $0.3 / 0.7 / 1.0 / 1.25 / 0.9B for 2027–31, ~$3.25B through 2030, consistent with "60–70% of $5B");
  - the refranchising P&L effect and proceeds;
  - segment take rates;
  - the franchisee P&L split.
  Each is stress-tested in the model's sensitivities table.
- **Data access:** direct fetches of SEC and company pages were blocked by this environment's network policy. Figures come from search-result excerpts of company releases, filings and press coverage, cross-checked across sources where possible. Re-verify the numbers that drive the conclusion (price, share count, net debt, 2026E EPS) against the 10-Q before acting.
- **Not modeled:** FX beyond 2026, one-time refranchising gains, China JV equity income beyond royalties, M&A, and a recession scenario outside path A′.

---

## Sources
- Q2-2026 results: [McDonald's mediaroom](https://mcdonalds.mediaroom.com/2026-08-04-McDONALDS-REPORTS-SECOND-QUARTER-2026-RESULTS), [10-Q Q2-26](https://www.sec.gov/Archives/edgar/data/0000063908/000006390826000073/mcd-20260630.htm), [TradingView summary](https://www.tradingview.com/news/tradingview:63e3720751ff0:0-mcdonalds-reports-q2-2026-revenue-7-10b-net-income-2-36b-diluted-eps-3-32/), [Business Model Analyst Q2](https://businessmodelanalyst.com/mcdonalds-q2-2026-guest-counts-landlord-margin/)
- Q1-2026: [McDonald's Q1-26](https://corporate.mcdonalds.com/corpmcd/our-stories/article/Q1-2026-results.html), [Restaurant Dive](https://www.restaurantdive.com/news/mcdonalds-q1-2026-positive-comp-sales-value-menu-innovation/819554/), [PYMNTS](https://www.pymnts.com/earnings/2026/mcdonalds-ceo-consumer-caution-drives-demand-value/)
- FY2025: [Q4/FY25 release](https://www.prnewswire.com/news-releases/mcdonalds-reports-fourth-quarter-and-full-year-2025-results-302685288.html), [10-K FY25](https://www.sec.gov/Archives/edgar/data/63908/000006390826000035/mcd-20251231.htm), [2026 outlook exhibit](https://www.sec.gov/Archives/edgar/data/63908/000006390826000032/exhibit992-12312025.htm), [Q4-25 call (Motley Fool)](https://www.fool.com/earnings/call-transcripts/2026/02/11/mcdonalds-mcd-q4-2025-earnings-call-transcript/)
- Investor day / NEXT: [Investor update 8-K](https://www.sec.gov/Archives/edgar/data/0000063908/000006390826000076/exhibit991-investorupdate2.htm), [McDonald's NEXT release](https://corporate.mcdonalds.com/corpmcd/our-stories/article/NEXT-growth-strategy-advances.html), [Benzinga: 98% franchise mix & 2030 targets](https://www.benzinga.com/trading-ideas/movers/26/09/61974494/mcdonalds-targets-98-franchise-mix-higher-margins-through-2030), [TipRanks: ~4.5% unit growth 2027](https://www.tipranks.com/news/the-fly/mcdonalds-sees-net-new-unit-growth-of-about-4-5-in-2027-thefly-news), [Zacks via Yahoo: 50% margin](https://finance.yahoo.com/markets/stocks/articles/mcds-next-strategy-lift-operating-135500852.html), [Reuters via Investing.com: flat traffic](https://www.investing.com/news/stock-market-news/mcdonalds-outlines-85-billion-plan-to-support-franchisees-4912916), [CNBC investor day](https://www.cnbc.com/2026/09/23/mcdonalds-investor-day-remodels-training-chicken-growth-plans.html), [CNBC: CEO on inflation](https://www.cnbc.com/2026/09/23/mcdonalds-investor-day-ceo-chris-kempczinksi-inflation.html), [Fortune](https://fortune.com/2026/09/24/mcdonalds-bets-8-5-billion-productivity-makeover-across-more-than-46000-restaurants/), [Business Model Analyst: mostly a rent cut](https://businessmodelanalyst.com/mcdonalds-8-5-billion-franchisee-support-rent-relief/), [BMA: renewal terms](https://businessmodelanalyst.com/mcdonalds-investor-day-remodel-check-franchise-renewal/), [The Crypto Basic: CFO 5–6 yr payback](https://thecryptobasic.com/2026/09/24/mcdonalds-stock-fell-4-8-amid-investor-day-cfo-puts-next-company-payback-at-5-6-years/), [Forbes](https://www.forbes.com/sites/jimosman/2026/09/25/mcdonalds-stock-fell-29-its-turnaround-plan-could-make-things-worse/), [Restaurant Business: investors not convinced](https://www.restaurantbusinessonline.com/financing/mcdonalds-just-put-forth-bold-plan-investors-are-not-convinced)
- Analysts: [JPM cut to $260](https://www.investing.com/news/analyst-ratings/jpmorgan-cuts-mcdonalds-stock-price-target-on-reinvestment-plan-93CH-4915585), [RBC to $285](https://www.gurufocus.com/news/9095638/mcd-maintains-by-rbc-capital-price-target-lowered-to-285), [BTIG](https://www.investing.com/news/analyst-ratings/btig-cuts-mcdonalds-stock-price-target-on-sales-pressures-investment-costs-93CH-4917081), [Benzinga: timing and level of investment](https://www.benzinga.com/analyst-stock-ratings/analyst-color/26/09/61979951/mcdonalds-stock-hits-four-year-low-analyst-says-timing-and-level-of-required-investment-weighs-on-growth)
- Stock and market: [Bloomberg: selloff hits 30%](https://www.bloomberg.com/news/articles/2026-09-26/mcdonald-s-sell-off-hits-30-as-big-mac-inflation-spurs-pushback), [24/7 Wall St: 52-week low](https://247wallst.com/investing/2026/09/24/mcdonalds-breaks-to-a-new-52-week-low-after-the-ceo-says-things-are-not-getting-better/), [Morningstar quote](https://www.morningstar.com/stocks/xnys/mcd/quote), [FinanceCharts 52-wk high](https://www.financecharts.com/stocks/MCD/summary/price), [Dividend: 50th raise](https://mcdonalds.mediaroom.com/2026-09-17-McDONALDS-MARKS-50-CONSECUTIVE-YEARS-OF-DIVIDEND-INCREASES,-JOINING-THE-RANKS-OF-DIVIDEND-KINGS), [10-yr Treasury Sep 25](https://www.advisorperspectives.com/dshort/updates/2026/09/25/treasury-yields-snapshot-september-25-2026), [P/E history](https://www.financecharts.com/stocks/MCD/value/pe-ratio), [Consensus EPS (TipRanks)](https://www.tipranks.com/news/mcd-stock-offers-a-reasonable-valuation-after-recent-declines)
- Franchisees and value: [Restaurant Business: franchisee profitability](https://www.restaurantbusinessonline.com/financing/mcdonalds-franchisee-profitability-takes-hit-just-company-eyes-remodels), [Survey: operators worried](https://www.restaurantbusinessonline.com/financing/survey-mcdonalds-operators-worried-about-their-finances), [CNBC: value tensions](https://www.cnbc.com/2026/02/11/mcdonalds-value-franchisees.html), [NBC: prices +40% vs 2019](https://www.nbcnews.com/business/consumer/mcdonalds-exec-says-average-menu-item-costs-40-percent-more-than-2019-rcna154593), [Trefis: low-income customer](https://www.trefis.com/stock/mcd/articles/615678/why-has-mcdonalds-gone-quiet-on-its-low-income-customer/2026-09-17)
- History: [FY2019 results](https://corporate.mcdonalds.com/corpmcd/our-stories/article/q4-and-2019-results.html), [FY2015 10-K](https://www.sec.gov/Archives/edgar/data/0000063908/000006390816000103/mcd-12312015x10k.htm), [China stake to 48%](https://www.cnbc.com/2023/11/20/mcdonalds-increases-minority-stake-in-china-business-.html)
