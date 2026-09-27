# AI infrastructure valuation model: Meta & Microsoft

Scenario-based SOTP / segment DCF that separates each company's existing business from its
AI infrastructure investment and values the AI layer on **incremental AI ROIC vs cost of capital**.

* **Read first:** [`AI_VALUATION_REPORT.md`](AI_VALUATION_REPORT.md): method, results, reverse DCF, assumption scorecards, verdicts.
* **All tables:** [`outputs/model_results.md`](outputs/model_results.md) (auto-generated), plus a CSV per table in `outputs/`.

## Run

```bash
pip install numpy scipy pandas
python3 analysis.py          # ~3s; rewrites outputs/
```

## Files

| File | What it is |
|---|---|
| `engine.py` | Vintage-based AI capex engine (`AIProgram`), core segment DCF (`Segment`), SOTP (`Company`) |
| `inputs.py` | All inputs with source tags `[R]` reported, `[G]` guidance, `[C]` consensus, `[E]` estimate, `[B]` benchmark; five scenarios per company; knobs for every sensitivity |
| `analysis.py` | Scenario valuations, capex/D&A/tax/residual tables, life tests, capex & delay tests, tornado, grids, reverse DCF, ROIC-defined scenarios, Meta ads-only test, Microsoft OpenAI tests, $/GW translation |

## Changing an assumption

Every sensitivity is a "knob" (see `DEFAULT_KNOBS` in `inputs.py`):

```python
from inputs import build
build("MSFT", "base", {"econ_life": 6, "yield_mult": 1.2, "wacc_shift": -0.005}).run()["per_share"]
build("META", "bear_lite", {"delay": 2, "train_g": -0.10}).run()["ai_value"]
```

Scenario operating assumptions live in `META_SCN` / `MSFT_SCN`. Company-level inputs (price, shares,
net debt, 2026 base year, capex history) live in `META` / `MSFT`.

## Data caveat

Inputs for Q2-CY26 (Meta) and FY26 (Microsoft) came from web-search summaries of filings and press
coverage, because direct access to SEC/IR sites was blocked in the build environment. Items tagged `[R]`
should be checked against the 10-Q/10-K before relying on them. Items tagged `[E]` are modelling
judgements and are the ones to challenge.
