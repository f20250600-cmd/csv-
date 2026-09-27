import json, shutil, subprocess
from openpyxl import load_workbook
RECALC="/root/.claude/skills/synced/259bac5f-5645-4e19-ad23-31ee399e7c06_bc96653a-afc7-48e6-bcc3-3e49cadaee29/xlsx/scripts/recalc.py"
SRC="outputs/CEG_VST_NAV_Model.xlsx"; lay=json.load(open("outputs/.xlsx_layout.json")); sr=lay["srow"]
keys=["navps","navpsp","fwdps","irr","entry","rcps","pt","updown"]
def run(scen, shift=0.0):
    wb=load_workbook(SRC); wb["Inputs"]["B4"]=scen; wb["Inputs"]["B5"]=shift; wb.save("outputs/.tmp.xlsx")
    out=json.loads(subprocess.run(["python3",RECALC,"outputs/.tmp.xlsx","300"],capture_output=True,text=True).stdout)
    assert out.get("status")=="success" and out["total_errors"]==0, out
    s=load_workbook("outputs/.tmp.xlsx",data_only=True)["Summary"]
    return {k:(s[f"B{sr[k]}"].value, s[f"C{sr[k]}"].value) for k in keys}
res={sc:run(sc) for sc in ["Low","Base","High","Extreme"]}
res["Base +14.3 shift (lever test)"]=run("Base",14.3)
json.dump(res,open("outputs/.snap.json","w"),indent=1)
for k,v in res.items(): print(k,{kk:(round(a,3),round(b,3)) for kk,(a,b) in v.items()})

# ---- write static snapshot table into Summary, then final recalc (Base)
from openpyxl.styles import Font, PatternFill
wb = load_workbook(SRC)
s = wb["Summary"]
r = lay["snap_row"]
A = lambda **k: Font(name="Arial", size=10, **k)
s[f"A{r}"] = "6. Scenario snapshot at default inputs (STATIC values - rerun excel_snapshot.py or switch the Scenario cell to update)"
s[f"A{r}"].font = A(bold=True)
for col in "ABCDEFGHIJ":
    s[f"{col}{r}"].fill = PatternFill("solid", fgColor="F2F2F2")
r += 1
labels = {"navps": "NAV/sh gen-only", "navpsp": "NAV/sh incl. platform", "fwdps": "FCF + NAV at horizon", "irr": "Implied return/yr",
          "entry": "Fat-pitch entry", "rcps": "Replacement + FCF", "pt": "Price target", "updown": "Up/(down)side"}
for co_i, co in enumerate(("CEG", "VST")):
    s[f"A{r}"] = co
    s[f"A{r}"].font = A(bold=True)
    for j, k in enumerate(labels):
        c = s.cell(row=r, column=2 + j, value=labels[k]); c.font = A(bold=True)
    r += 1
    for scen, v in res.items():
        s[f"A{r}"] = scen; s[f"A{r}"].font = A()
        for j, k in enumerate(labels):
            c = s.cell(row=r, column=2 + j, value=round(v[k][co_i], 4))
            c.font = A(); c.number_format = '0.0%;(0.0%);"-"' if k in ("irr", "updown") else '#,##0.00;(#,##0.00);"-"'
        r += 1
    r += 1
for col in "DEFGHI":
    s.column_dimensions[col].width = 15
wb.save(SRC)
out = json.loads(subprocess.run(["python3", RECALC, SRC, "300"], capture_output=True, text=True).stdout)
print("final recalc:", out)
import os; os.remove("outputs/.tmp.xlsx")
