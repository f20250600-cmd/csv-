# CEG / VST asset-based NAV model

Asset-by-asset NAV for Constellation Energy (CEG) and Vistra (VST) under four AI/data-center demand scenarios.

- `inputs.py` holds every assumption: fleet register, contracts, price decks, scenarios and claims. Items marked `EST` / `ASSUMPTION` are judgments.
- `nav_model.py` is the valuation engine, sensitivities and market-implied solves.
- `replacement.py` is the replacement-cost + FCF layer: depreciated replacement cost of each fleet, less claims, plus PV of FCF over the replacement lead time.
- `fcf.py` is the "NAV + FCF generated" layer: equity FCF 2027-2030 plus the forward NAV at end-2030, and the implied return. Run `python3 nav_model.py` (needs `openpyxl` for the xlsx output).
- `REPORT.md` is the investment memo.
- `outputs/` keeps only the Excel model. Running `nav_model.py` regenerates detailed tables, CSVs and a values-only workbook there; they are git-ignored.

To test a view, edit the scenario heat rates, capacity prices or gas deck in `inputs.py` and re-run. The market price is used only in the final comparison and solve.

## Editable Excel model
`outputs/CEG_VST_NAV_Model.xlsx` is a fully formula-driven version of the model (~40k formulas, no hard-coded results).
- **Inputs:** control panel (scenario, price/gas shifts, nuclear replacement basis, horizon, target return), tech defaults, hubs, company inputs (revenue/fuel/O&M/capex/PPA adjustments, FCF haircut, price-target weights), and claims.
- **CEG_Assets / VST_Assets:** one row per plant group; edit MW, dates, contracts, costs, discount rates, replacement cost.
- **Prices:** annual price deck (formulas).
- **CEG_Model / VST_Model:** annual revenue → gross margin → EBITDA → cash flow → PV for every asset, plus consolidated FCF.
- **Summary:** NAV, FCF + NAV at the horizon, replacement cost + FCF, **price target**, fat-pitch entry, and revenue/margin/FCF by year.
Rebuild with `python3 build_excel.py && python3 excel_snapshot.py` (needs LibreOffice Calc for the recalc and snapshot).
