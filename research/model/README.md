# Intel valuation model: scenario DCF

File: `intel_valuation_model.xlsx`. It is built on the findings in `../intel-competitive-analysis-2026-09.md`.

**Sheets:**
- **README**: how to use the model, the method, and how each scenario maps to the product evidence.
- **Inputs**: every assumption, with its source.
  - Blue cells are inputs.
  - Yellow cells are key judgment calls, or placeholders to verify against the Q2-26 10-Q.
- **Summary**: each scenario's value, the probability-weighted value, and a reverse DCF against today's price.
- **Sensitivity**: live WACC × terminal-growth grids for all three scenarios, plus a Base-case tornado.
- **Bear / Base / Bull**: identical 2026E–2033 forecasts by segment, discounted to 30 Sep 2026.

The file was written without cached values; Excel or Google Sheets recalculates everything on open. The formulas were checked with a Python formula engine (0 errors), because LibreOffice's Calc engine isn't installed in the build environment.

## Results at default inputs (price $123.00 on 25 Sep 2026; about 5.48bn diluted shares; WACC 10.4%; terminal growth 3%)

| | Bear | Base | Bull | Probability-weighted (30/45/25) |
|---|---|---|---|---|
| Value per share | ~$1 | ~$24 | ~$55 | ~$25 |
| vs. price | −99% | −80% | −55% | −80% |
| Terminal value as % of EV | 28% | 83% | 82% | |

**Reverse DCF.** Hold the Base explicit years fixed. Today's roughly $666bn EV then requires about **$97bn of normalized 2034 free cash flow**. That is **6.2×** the Base case and about 3× the Bull case (about $34bn in 2033). At a 25–30% FCF margin, that means **$325–390bn of revenue** in 2034, against $128bn in the Bull case.

The market is pricing an outcome well beyond my Bull scenario, or it is using a much lower discount rate. Neither the Base nor the Bull case reaches $123/share even at an 8.5% WACC and 4% terminal growth:

| Case at 8.5% WACC / 4% growth | Value per share |
|---|---|
| Base | $41 |
| Bull | $94 |

**Tornado (Base, one input at a time):**

| Input flexed | Range of value per share | Swing |
|---|---|---|
| External foundry revenue ×0.5 / ×2 | $19 – $37 | $18 |
| DCAI growth ±3 pts per year | $20 – $29 | $9 |
| Gross margin ±3 pts | $20 – $29 | $9 |
| Capex ±15% | $22 – $27 | $5 |

## What to check before trusting this

1. **Placeholders.** D&A, stock-based comp, non-controlling interests (SCIP fab partners and the Mobileye minority), and Q1-26 external foundry revenue were not sourceable here. NCI is set to 0, which *overstates* value.
2. **Share count.** It is derived as Q2 non-GAAP net income ÷ EPS, plus the August offering shares; verify it against the 10-Q.
3. **Gross capex.** Partner and government offsets are ignored. The effect on value is small; see the tornado.
4. **Consensus comparison.** Consensus 2027 EPS is about $2.04; the Base case gives about $1.59 before SBC. Consensus sits between the Base and Bull cases.
5. **Scenario drivers are hypotheticals.** They are tied to the product evidence and were fixed before the valuation was computed. They were not tuned toward the market price.
