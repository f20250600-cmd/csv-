# CEG / VST asset-based NAV model

Asset-by-asset NAV for Constellation Energy (CEG) and Vistra (VST) under four AI/data-center demand scenarios.

- `inputs.py` holds every assumption: fleet register, contracts, price decks, scenarios and claims. Items marked `EST` / `ASSUMPTION` are judgments.
- `nav_model.py` is the valuation engine, sensitivities and market-implied solves. Run `python3 nav_model.py` (needs `openpyxl` for the xlsx output).
- `REPORT.md` is the investment memo.
- `outputs/` holds the generated tables (`tables.md`), CSVs and `nav_model.xlsx`.

To test a view, edit the scenario heat rates, capacity prices or gas deck in `inputs.py` and re-run. The market price is used only in the final comparison and solve.
