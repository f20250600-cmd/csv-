"""
Formula-driven Excel model for Vista Energy (VIST): outputs/VIST_NAV_Model.xlsx
Mirrors vista_nav.py. Edit blue / yellow cells on 'Inputs'; everything else is formulas.
"""
import json
import os
import subprocess

from openpyxl import Workbook, load_workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as L
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

import vista_nav as V

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs", "VIST_NAV_Model.xlsx")
RECALC = "/root/.claude/skills/synced/259bac5f-5645-4e19-ad23-31ee399e7c06_bc96653a-afc7-48e6-bcc3-3e49cadaee29/xlsx/scripts/recalc.py"
N = V.YEARS
C0 = 7
PC = [L(C0 + i) for i in range(N)]           # G .. AI
FIRST, LAST = PC[0], PC[-1]
BLUE, BLACK, GREEN = "0000FF", "000000", "008000"
YEL = PatternFill("solid", fgColor="FFFF00")
HDR = PatternFill("solid", fgColor="DDE6F0")
SEC = PatternFill("solid", fgColor="F2F2F2")
USD, USD1, USD2, PCT = '#,##0;(#,##0);"-"', '#,##0.0;(#,##0.0);"-"', '#,##0.00;(#,##0.00);"-"', '0.0%;(0.0%);"-"'
wb = Workbook()


def F(c=BLACK, b=False, i=False):
    return Font(name="Arial", size=10, color=c, bold=b, italic=i)


def put(ws, cell, v, c=BLACK, fmt=None, b=False, fill=None, i=False, note=None):
    x = ws[cell]
    x.value = v
    x.font = F(c, b, i)
    if fmt:
        x.number_format = fmt
    if fill:
        x.fill = fill
    if note:
        x.comment = Comment(note, "model")


def nm(name, ref):
    wb.defined_names[name] = DefinedName(name, attr_text=ref)


# ------------------------------------------------------------------ README
rd = wb.active
rd.title = "README"
for i, t in enumerate([
    "Vista Energy (VIST) - asset-based NAV model (E&P method), editable",
    "",
    "NAV = PV(producing base, no new wells) + PV(proved undeveloped wells) + risk factor x PV(unbooked inventory) - net debt & other claims.",
    "Edit blue cells / yellow levers on 'Inputs'. 'Model' holds annual periods (P1 = Oct-26..Sep-27), 'Cohorts' the well-by-vintage production, 'Summary' the results.",
    "Colours: blue = input, yellow = key lever, green = link, black = formula.",
    "Units: $mm unless stated; production MMboe per period and kboe/d; prices nominal $/bbl (long-run inputs in 2026$).",
    "Main levers: Scenario (Brent long run), Brent shift, discount rate (Argentina risk), unbooked-inventory risk factor, export duty, EUR, well-cost multiplier, inventory.",
    "Calibration: P1 ~177 kboe/d and ~237 kboe/d by 2030 (guidance 158 kboe/d 2026, target 250 by 2030); EBITDA/boe matches Q2-26 (~$56.7 at ~$95 Brent).",
    "Sources: Vista Q2-26 results/call (production, net debt $3.06bn, lifting $4.5/boe, realized $89.4/bbl), YE-25 reserves (588 MMboe 1P, PV-10 $6.61bn),",
    "well cost $14.2mm (Q4-25) -> $11mm target 2028, >1,320 locations, Equinor deal ($712mm, closed May-26); Brent futures Sep-26. Other items are estimates (see comments).",
], 1):
    rd.cell(row=i, column=1, value=t).font = F(b=(i == 1))
rd.column_dimensions["A"].width = 160

# ------------------------------------------------------------------ INPUTS
ws = wb.create_sheet("Inputs")
ws.column_dimensions["A"].width = 58
for c in "BCDEF":
    ws.column_dimensions[c].width = 13
ws.column_dimensions["G"].width = 70
r = 1
put(ws, "A1", "INPUTS - blue = input, yellow = key lever", b=True)
r = 3


def sec(t):
    global r
    for c in range(1, 8):
        ws.cell(row=r, column=c).fill = SEC
    put(ws, f"A{r}", t, b=True)
    r += 1


def inp(label, name, v, fmt=None, lever=False, src=""):
    global r
    put(ws, f"A{r}", label)
    put(ws, f"B{r}", v, BLUE, fmt, fill=YEL if lever else None)
    if src:
        put(ws, f"G{r}", src, i=True)
    nm(name, f"Inputs!$B${r}")
    r += 1


sec("Control panel")
inp("Scenario (Low / Base / High / Extreme)", "Scenario", "Base", lever=True, src="Selects long-run Brent from the scenario table")
dv = DataValidation(type="list", formula1='"Low,Base,High,Extreme"')
ws.add_data_validation(dv)
dv.add(f"B{r-1}")
inp("Long-run Brent shift ($/bbl, 2026$)", "BrentShift", 0.0, USD1, True)
inp("Discount rate (unlevered, Argentina-risked)", "Disc", V.DISC, PCT, True, "10% = investment-grade path; 15%+ = macro relapse / capital controls")
inp("Risk factor on unbooked inventory (beyond proved wells)", "UnbRisk", V.UNBOOKED_RISK, PCT, True, "Industry practice ~50-75% for unproved locations")
inp("Export duty on crude", "ExportDuty", V.EXPORT_DUTY, PCT, True, "0% today; historically up to 8%")
inp("Net EUR per well (MMboe)", "EUR", V.EUR, USD2, True, "Calibrated to guidance; Vaca Muerta type curves ~1.0-1.5 MMboe gross")
inp("Well-cost multiplier", "WellCostMult", 1.0, USD2, True)
inp("Total drilling inventory (net wells)", "Inventory", V.INVENTORY, USD, True, ">1,320 ready-to-drill (company) + ~150 net Equinor (estimate)")
inp("Wells to develop proved undeveloped (PUD) reserves", "PUDWells", V.PUD_WELLS, USD, False, "355.7 MMboe PUD (YE-25) + Equinor, at ~0.9 MMboe/well")
r += 1
sec("Brent deck (nominal $/bbl)")
put(ws, f"A{r}", "Futures: P1 (Oct-26..Sep-27), P2, P3")
for j in range(3):
    put(ws, f"{L(2+j)}{r}", V.FUTURES[j + 1], BLUE, USD1)
    nm(f"Fut{j+1}", f"Inputs!${L(2+j)}${r}")
put(ws, f"G{r}", "Spot ~$101-105 late Sep-26 (Hormuz); Aug-27 $78.4; 2028 ~$75-76", i=True)
r += 1
inp("Inflation / escalator", "Infl", V.INFL, PCT)
r += 1
put(ws, f"A{r}", "Scenario", b=True)
for j, s in enumerate(V.ORDER):
    put(ws, f"{L(2+j)}{r}", s, b=True, fill=HDR)
hdr = r
r += 1
put(ws, f"A{r}", "Long-run Brent (2026$/bbl)")
for j, s in enumerate(V.ORDER):
    put(ws, f"{L(2+j)}{r}", V.SCENARIOS[s]["brent_lr"], BLUE, USD1)
put(ws, f"F{r}", f"=INDEX(B{r}:E{r},MATCH(Scenario,B{hdr}:E{hdr},0))+BrentShift", fmt=USD1, b=True)
nm("BrentLR", f"Inputs!$F${r}")
nm("BrentLRBase", f"Inputs!$C${r}")
put(ws, f"G{r}", "Active = scenario + shift", i=True)
r += 1
put(ws, f"A{r}", "Scenario description")
for j, s in enumerate(V.ORDER):
    put(ws, f"{L(2+j)}{r}", V.SCENARIOS[s]["desc"], i=True)
r += 2
sec("Operations and costs")
inp("Oil share of production", "OilShare", V.OIL_SHARE, PCT)
inp("Realized oil discount to Brent ($/bbl)", "OilDisc", V.OIL_DISCOUNT, USD1, src="Q2-26 realized $89.4/bbl")
inp("Gas price ($/boe, 2026$)", "GasBoe", V.GAS_PRICE_BOE, USD1, src="~$3.5/MMBtu - estimate")
inp("Royalties (% revenue)", "Royalty", V.ROYALTY, PCT, src="Neuquen 12% + extension premia - estimate")
inp("Provincial turnover tax (% revenue)", "Turnover", V.TURNOVER_TAX, PCT)
inp("Lifting cost ($/boe, 2026$)", "Lifting", V.LIFTING, USD2, src="Q2-26 $4.5; Q1 $4.3")
inp("Transport, storage & selling ($/boe)", "Transport", V.TRANSPORT, USD2, src="Estimate")
inp("G&A ($/boe)", "GNA", V.GNA, USD2, src="Estimate")
inp("Cost escalator", "CostEsc", V.COST_ESC, PCT)
inp("Facilities / infrastructure capex ($/boe)", "Facilities", V.FACILITIES, USD2, src="Estimate")
put(ws, f"A{r}", "Well cost ($mm/well): P1, P2, P3 (then escalates)")
for j in range(3):
    put(ws, f"{L(2+j)}{r}", V.WELL_COST[j + 1], BLUE, USD1)
    nm(f"WC{j+1}", f"Inputs!${L(2+j)}${r}")
put(ws, f"G{r}", "$14.2mm Q4-25; company targets $11mm by 2028", i=True)
r += 1
inp("Production at 1-Oct-2026 from existing wells (kboe/d)", "BaseRate", V.BASE_RATE, USD1, src="Q3 guide 160, Q4 170")
put(ws, f"A{r}", "Base decline by period: P1..P5, then terminal")
for j, d in enumerate(V.BASE_DECLINE + [V.TERMINAL_DECLINE]):
    put(ws, f"{L(2+j)}{r}", d, BLUE, PCT)
decl_row = r
r += 1
put(ws, f"A{r}", "New-well profile (share of EUR by period of life): P1..P10, then tail decline below")
for j, x in enumerate(V.WELL_PROFILE):
    ws.column_dimensions[L(2 + j)].width = max(ws.column_dimensions[L(2 + j)].width or 0, 9)
    put(ws, f"{L(2+j)}{r}", x, BLUE, PCT)
prof_row = r
r += 1
inp("Well profile tail decline (after P10)", "TailDecl", V.TAIL_DECLINE, PCT)
r += 1
sec("Tax and balance sheet")
inp("Income tax rate", "TaxRate", V.TAX_RATE, PCT)
inp("Existing tax basis ($bn, amortised over 7 periods)", "TaxBasis", V.EXISTING_TAX_BASIS, USD2, src="Estimate")
inp("Tax life of new capex (periods)", "TaxLife", V.TAX_LIFE, "0")
inp("Net debt ($bn, 30-Jun-26)", "NetDebt", V.NET_DEBT, USD2, src="Q2-26 results")
inp("Other claims ($bn: leases, abandonment)", "OtherClaims", V.OTHER_CLAIMS, USD2, src="Estimate")
inp("ADS outstanding (mm)", "Shares", V.SHARES, USD2, src="incl. ADS issued to Equinor")
inp("Share price ($/ADS)", "Price", V.PRICE, USD2, src="18-Sep-2026")
inp("Flowing production for EV/boe (kboe/d)", "FlowRate", 165.0, USD1)

# ------------------------------------------------------------------ MODEL
ms = wb.create_sheet("Model")
ms.column_dimensions["A"].width = 44
ms.column_dimensions["B"].width = 10
for c in "CDEF":
    ms.column_dimensions[c].width = 3
for c in PC:
    ms.column_dimensions[c].width = 9
put(ms, "A1", "VIST - annual model ($mm unless stated; P1 = Oct-26..Sep-27). Formulas only.", b=True)
row = {}
rr = 3


def line(key, label, fn, fmt=USD1, bold=False):
    global rr
    row[key] = rr
    put(ms, f"A{rr}", label, b=bold)
    for i, c in enumerate(PC):
        put(ms, f"{c}{rr}", fn(i + 1, c), fmt=fmt, b=bold)
    rr += 1


line("t", "Period", lambda t, c: t, "0", True)
line("yr", "Ends Sep-", lambda t, c: 2026 + t, "0", True)
line("infl", "Escalator (mid-period)", lambda t, c: f"=(1+Infl)^({c}{row['t']}-0.5)", "0.000")
line("cesc", "Cost escalator (mid-period)", lambda t, c: f"=(1+CostEsc)^({c}{row['t']}-0.5)", "0.000")


def brent(t, c):
    lr = f"BrentLR*{c}{row['infl']}"
    lrb = f"BrentLRBase*{c}{row['infl']}"
    if t == 1:
        return "=Fut1"
    if t == 2:
        return f"=Fut2+0.5*({lr}-{lrb})"
    if t == 3:
        return f"=Fut3+({lr}-{lrb})"
    return f"={lr}"


line("brent", "Brent ($/bbl, nominal)", brent, USD1, True)
line("revboe", "Revenue per boe ($)", lambda t, c: f"=OilShare*({c}{row['brent']}-OilDisc)+(1-OilShare)*GasBoe*{c}{row['cesc']}", USD2)
line("ebboe", "EBITDA per boe ($)", lambda t, c: f"={c}{row['revboe']}*(1-Royalty-Turnover-ExportDuty)-(Lifting+Transport+GNA)*{c}{row['cesc']}", USD2, True)
line("wc", "Well cost ($mm/well)", lambda t, c: f"=WC{t}*WellCostMult" if t <= 3 else f"=WC3*(1+CostEsc)^({c}{row['t']}-3)*WellCostMult", USD2)
line("plan", "Well plan (net wells per period) - EDIT", lambda t, c: V.WELLS[t - 1] if t <= len(V.WELLS) else 135, USD)
for c in PC:
    ms[f"{c}{row['plan']}"].font = F(BLUE)
    ms[f"{c}{row['plan']}"].fill = YEL
line("decl", "Base decline", lambda t, c: f"=Inputs!${L(1+min(t,6))}${decl_row}", PCT)
line("rate", "Base rate at start of period (kboe/d)", lambda t, c: "=BaseRate" if t == 1 else f"={PC[t-2]}{row['rate']}*(1-{PC[t-2]}{row['decl']})", USD1)
line("basevol", "Base production (MMboe)", lambda t, c: f"={c}{row['rate']}*(1-{c}{row['decl']}/2)*365/1000", USD2)
line("prof", "Well profile by age (share of EUR)", lambda t, c: f"=Inputs!${L(1+t)}${prof_row}" if t <= 10 else f"={PC[t-2]}{row['prof']}*(1-TailDecl)", PCT)
rr += 1

blocks = [("pdp", "PRODUCING BASE ONLY (no new wells)", "0"), ("pud", "PRODUCING + PROVED UNDEVELOPED WELLS", "MIN(PUDWells,Inventory)"), ("all", "PRODUCING + FULL INVENTORY", "Inventory")]
coh = wb.create_sheet("Cohorts")
coh.column_dimensions["A"].width = 30
for c in PC:
    coh.column_dimensions[c].width = 8
put(coh, "A1", "New-well production by vintage (MMboe) = wells in vintage x EUR x profile(age)", b=True)
crow = 3
brow = {}
for key, title, cap in blocks:
    rr += 1
    put(ms, f"A{rr}", title, b=True)
    for cc in range(1, C0 + N):
        ms.cell(row=rr, column=cc).fill = SEC
    rr += 1
    b = {}

    def bl(k, label, fn, fmt=USD1, bold=False):
        global rr
        line(f"{key}_{k}", label, fn, fmt, bold)
        b[k] = row[f"{key}_{k}"]

    bl("wells", "Wells tied in", lambda t, c: f"=MAX(0,MIN({c}${row['plan']},{cap}-SUM(${FIRST}{rr}:{PC[t-2]}{rr})))" if t > 1 else f"=MAX(0,MIN({c}${row['plan']},{cap}))", USD)
    # cohort matrix for this block
    put(coh, f"A{crow}", title, b=True)
    crow += 1
    first_c = crow
    for k in range(1, N + 1):
        put(coh, f"A{crow}", f"Vintage P{k}")
        for t in range(1, N + 1):
            c = PC[t - 1]
            if t < k:
                put(coh, f"{c}{crow}", 0, fmt=USD2)
            else:
                put(coh, f"{c}{crow}", f"=Model!${PC[k-1]}${b['wells']}*EUR*Model!{PC[t-k]}${row['prof']}", fmt=USD2)
        crow += 1
    last_c = crow - 1
    crow += 1
    bl("newvol", "New-well production (MMboe)", lambda t, c: f"=SUM(Cohorts!{c}{first_c}:{c}{last_c})", USD2)
    bl("vol", "Total production (MMboe)", lambda t, c: f"={c}${row['basevol']}+{c}{b['newvol']}", USD2)
    bl("kboed", "Production (kboe/d)", lambda t, c: f"={c}{b['vol']}/0.365", USD1, True)
    bl("rev", "Revenue ($mm)", lambda t, c: f"={c}{b['vol']}*{c}${row['revboe']}", USD)
    bl("ebitda", "EBITDA ($mm)", lambda t, c: f"={c}{b['vol']}*{c}${row['ebboe']}", USD, True)
    bl("capex", "Capex: wells + facilities ($mm)", lambda t, c: f"={c}{b['wells']}*{c}${row['wc']}+{c}{b['vol']}*Facilities*{c}${row['cesc']}", USD)
    bl("dda", "Tax depreciation ($mm)",
       lambda t, c: f"=IF({c}${row['t']}<=7,TaxBasis*1000/7,0)+SUM({PC[max(0, t - V.TAX_LIFE)]}{rr - 1}:{c}{rr - 1})/TaxLife", USD)
    bl("tax", "Cash tax ($mm)", lambda t, c: f"=TaxRate*MAX(0,{c}{b['ebitda']}-{c}{b['dda']})", USD)
    bl("fcf", "Unlevered free cash flow ($mm)", lambda t, c: f"={c}{b['ebitda']}-{c}{b['capex']}-{c}{b['tax']}", USD, True)
    bl("pv", "PV at discount rate ($mm)", lambda t, c: f"={c}{b['fcf']}*(1+Disc)^-({c}${row['t']}-0.5)", USD)
    put(ms, f"B{b['pv']}", f"=SUM({FIRST}{b['pv']}:{LAST}{b['pv']})", fmt=USD, b=True)
    brow[key] = b
ms.freeze_panes = f"{FIRST}3"

# ------------------------------------------------------------------ SUMMARY
sm = wb.create_sheet("Summary", 1)
sm.column_dimensions["A"].width = 60
for c in "BCDEFGHI":
    sm.column_dimensions[c].width = 14
put(sm, "A1", "VIST - SUMMARY (recalculates from Inputs)", b=True)
put(sm, "A2", '="Scenario: "&Scenario&"  |  long-run Brent $"&TEXT(BrentLR,"0")&" (2026$)  |  discount "&TEXT(Disc,"0.0%")&"  |  unbooked risk "&TEXT(UnbRisk,"0%")', i=True)
srow = {}
r = 4


def s_add(key, label, f, fmt=USD, bold=False, fill=None):
    global r
    put(sm, f"A{r}", label, b=bold)
    put(sm, f"B{r}", f, fmt=fmt, b=bold, fill=fill)
    srow[key] = r
    r += 1


pv = {k: f"Model!$B${brow[k]['pv']}" for k in brow}
s_add("pdp", "PV producing base ($mm)", f"={pv['pdp']}")
s_add("pud", "PV proved undeveloped wells ($mm)", f"={pv['pud']}-{pv['pdp']}")
s_add("unb", "PV unbooked inventory, unrisked ($mm)", f"={pv['all']}-{pv['pud']}")
s_add("unbr", "PV unbooked inventory, risked ($mm)", f"=B{r-1}*UnbRisk")
s_add("gav", "Gross asset value, risked ($mm)", f"=B{srow['pdp']}+B{srow['pud']}+B{srow['unbr']}", bold=True)
s_add("claims", "Less: net debt & other claims ($mm)", "=(NetDebt+OtherClaims)*1000")
s_add("eq", "Equity NAV, risked ($mm)", f"=B{srow['gav']}-B{srow['claims']}", bold=True)
s_add("nav", "NAV per ADS - risked ($)", f"=B{srow['eq']}/Shares", USD2, True, YEL)
s_add("navu", "NAV per ADS - unrisked inventory ($)", f"=({pv['all']}-B{srow['claims']})/Shares", USD2)
s_add("pdpps", "Hard floor: producing base only, per ADS ($)", f"=({pv['pdp']}-B{srow['claims']})/Shares", USD2)
s_add("price", "Share price ($/ADS)", "=Price", USD2)
s_add("updown", "Upside / (downside) to risked NAV", f"=B{srow['nav']}/B{srow['price']}-1", PCT, True, YEL)
s_add("mos", "Entry at 30% margin of safety to risked NAV ($)", f"=0.7*B{srow['nav']}", USD2)
r += 1
s_add("mcap", "Market cap ($mm)", "=Price*Shares")
s_add("ev", "Enterprise value ($mm)", f"=B{srow['mcap']}+B{srow['claims']}")
s_add("evebitda", "EV / P1 EBITDA (full plan)", f"=B{srow['ev']}/Model!{FIRST}{brow['all']['ebitda']}", '0.0"x"')
s_add("evflow", "EV per flowing boe/d ($)", f"=B{srow['ev']}*1000/FlowRate", USD)
s_add("ev1p", "EV per boe of 1P reserves (588 MMboe YE-25) ($)", f"=B{srow['ev']}/588.1", USD2)
s_add("fcfy", "P1 equity-level FCF yield (unlevered FCF / market cap)", f"=Model!{FIRST}{brow['all']['fcf']}/B{srow['mcap']}", PCT)
r += 1
put(sm, f"A{r}", "Production, EBITDA and FCF (full plan)", b=True)
r += 1
for j, t in enumerate([1, 2, 3, 4, 6, 9]):
    put(sm, f"{L(2+j)}{r}", f"P{t} (Sep-{2026+t})", b=True)
r += 1
for k, lab, fmt in (("kboed", "Production (kboe/d)", USD1), ("rev", "Revenue ($mm)", USD), ("ebitda", "EBITDA ($mm)", USD),
                    ("capex", "Capex ($mm)", USD), ("fcf", "Unlevered FCF ($mm)", USD)):
    put(sm, f"A{r}", lab)
    for j, t in enumerate([1, 2, 3, 4, 6, 9]):
        put(sm, f"{L(2+j)}{r}", f"=Model!{PC[t-1]}{brow['all'][k]}", GREEN, fmt)
    r += 1
put(sm, f"A{r}", "Brent ($/bbl)")
for j, t in enumerate([1, 2, 3, 4, 6, 9]):
    put(sm, f"{L(2+j)}{r}", f"=Model!{PC[t-1]}{row['brent']}", GREEN, USD1)
r += 2
snap_row = r
wb.move_sheet("Summary", offset=-1)
wb.save(OUT)

# ------------------------------------------------------------------ recalc, verify, snapshots
def recalc(path):
    out = json.loads(subprocess.run(["python3", RECALC, path, "300"], capture_output=True, text=True).stdout)
    assert out.get("status") == "success" and out["total_errors"] == 0, out
    return out


def setn(w, name, val):
    sh, cell = w.defined_names[name].attr_text.split("!")
    w[sh][cell.replace("$", "")] = val


def read(path):
    s = load_workbook(path, data_only=True)["Summary"]
    return {k: s[f"B{srow[k]}"].value for k in ("nav", "navu", "pdpps", "updown", "gav")}


tmp = os.path.join(HERE, "outputs", ".vtmp.xlsx")
snap = {}
for scen in V.ORDER:
    w = load_workbook(OUT)
    setn(w, "Scenario", scen)
    w.save(tmp)
    recalc(tmp)
    snap[scen] = read(tmp)
grid = {}
rates = [0.10, 0.12, 0.15, 0.18]
lrs = [55, 60, 65, 72, 80, 85, 95]
for lr in lrs:
    for d in rates:
        w = load_workbook(OUT)
        setn(w, "BrentShift", lr - 72)
        setn(w, "Disc", d)
        w.save(tmp)
        recalc(tmp)
        grid[(lr, d)] = read(tmp)["nav"]
os.remove(tmp)

w = load_workbook(OUT)
s = w["Summary"]
r = snap_row
s[f"A{r}"] = "Scenario snapshot at default inputs (STATIC - rerun build_vista_excel.py to refresh)"
s[f"A{r}"].font = F(b=True)
r += 1
for j, h in enumerate(["Scenario", "Risked NAV/ADS", "Unrisked NAV/ADS", "Producing-base floor", "Up/(down)side"]):
    c = s.cell(row=r, column=1 + j, value=h)
    c.font = F(b=True)
r += 1
for scen, v in snap.items():
    s.cell(row=r, column=1, value=scen).font = F()
    for j, k in enumerate(["nav", "navu", "pdpps", "updown"]):
        c = s.cell(row=r, column=2 + j, value=round(v[k], 4))
        c.font = F()
        c.number_format = PCT if k == "updown" else USD2
    r += 1
r += 1
s[f"A{r}"] = "Risked NAV/ADS: long-run Brent (2026$, rows) x discount rate (cols) - STATIC"
s[f"A{r}"].font = F(b=True)
r += 1
s.cell(row=r, column=1, value="Brent LR \\ discount").font = F(b=True)
for j, d in enumerate(rates):
    c = s.cell(row=r, column=2 + j, value=d)
    c.font = F(b=True)
    c.number_format = PCT
r += 1
for lr in lrs:
    s.cell(row=r, column=1, value=lr).font = F(b=True)
    for j, d in enumerate(rates):
        c = s.cell(row=r, column=2 + j, value=round(grid[(lr, d)], 2))
        c.font = F()
        c.number_format = USD2
    r += 1
w.save(OUT)
print(recalc(OUT))
print(json.dumps({k: {kk: round(vv, 2) for kk, vv in v.items()} for k, v in snap.items()}, indent=1))
print({f"{k[0]}@{k[1]:.0%}": round(v, 1) for k, v in grid.items()})
