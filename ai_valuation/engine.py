"""
Core valuation engine.

Three building blocks:

1. AIProgram   - vintage-based model of the AI infrastructure investment.
                 Every year of AI capex is a "vintage" split into accelerators/servers,
                 networking, facilities (shell, power, cooling) and land. Each vintage is
                 tracked separately for:
                   * accounting (book) depreciation   -> reported EBIT / EPS
                   * economic depreciation / refresh  -> economic NOPAT, replacement capex
                   * tax depreciation (bonus)         -> cash taxes
                   * residual (resale) value          -> cash at retirement
                 Revenue attaches to capacity through "streams" (e.g. Azure AI, ads uplift,
                 Copilot, frontier-model training). Capacity streams earn
                 min(demand, max-utilisation x potential capacity), so capex beyond
                 demand shows up as low utilisation instead of automatic revenue.

2. Segment     - plain driver-based DCF for an existing (non-AI) business line.

3. Company     - sum of the parts: core segments + Reality Labs + AI program + non-operating
                 assets - net debt.

All money in USD billions. Year labels are fiscal years (calendar for Meta, June FY for MSFT).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
from scipy.optimize import brentq


# ----------------------------------------------------------------------------------------
# AI infrastructure program
# ----------------------------------------------------------------------------------------
@dataclass
class Assets:
    # capex mix of a greenfield AI build (share of total $)
    accel: float = 0.58      # GPUs / accelerators / servers / memory
    network: float = 0.12    # back-end + front-end networking, optics
    facility: float = 0.28   # shell, electrical, cooling, power infrastructure
    land: float = 0.02
    # accounting (book) lives - company policy
    book_life_equip: float = 5.5
    book_life_fac: float = 25.0
    # economic life of accelerators+network (refresh cycle) - scenario assumption
    econ_life: int = 5
    # tax
    bonus: float = 1.0          # share of equipment expensed in year placed in service (OBBBA 100%)
    tax_life_equip: float = 5.0
    tax_life_fac: float = 39.0
    # resale value of retired equipment, % of original cost
    residual: float = 0.05
    # share of a vintage's capacity that is productive in its purchase year
    ramp0: float = 0.35
    # power + site operations, % of alive equipment gross cost per year
    power_fixed: float = 0.015
    power_var: float = 0.025    # scales with utilisation

    @property
    def equip(self) -> float:
        return self.accel + self.network

    @property
    def fac_ratio(self) -> float:
        """facility+land $ required per $ of equipment for *new* (growth) capacity."""
        return (self.facility + self.land) / self.equip


@dataclass
class Stream:
    name: str
    kind: str                                 # 'capacity' | 'exogenous' | 'cost'
    share: Dict[int, float]                   # year -> share of total AI capex (hist + explicit)
    share_default: float
    revenue: Dict[int, float] = field(default_factory=dict)   # demand (capacity) or revenue (exog)
    var_cost: float = 0.0                     # % of revenue
    fixed_opex: Dict[int, float] = field(default_factory=dict)
    # capacity-stream economics
    yield_: float = 0.0            # revenue per $ of equipment per year at 100% util, 2026 prices
    yield_drift: float = 0.0       # annual change in yield for vintages bought after base year
    erosion: float = 0.0           # annual price decline per year of vintage age
    u_max: float = 0.92            # max monetisable utilisation
    u_target: float = 0.85         # utilisation targeted by post-explicit capex rule
    internal_util: float = 0.85    # utilisation used for power cost on non-capacity streams
    post_growth: Dict[int, float] = field(default_factory=dict)  # cost streams: capacity growth
    lease_opex: Dict[int, float] = field(default_factory=dict)   # 3rd-party capacity rented (opex)
    lease_markup: float = 0.0      # revenue potential per $ of rented capacity
    fwd_yield_mult: float = 1.0    # one-off price level change for vintages after base year
    intensity_decline: float = 0.05  # exogenous streams: annual fall in equipment $ per $ revenue


@dataclass
class AIProgram:
    years: List[int]
    first_forecast: int
    explicit_end: int
    base_year: int
    capex_total: Dict[int, float]
    streams: List[Stream]
    assets: Assets
    tax_rate: float
    hurdle: float
    g_term: float
    val_offset: float
    terminal_ronic_override: Optional[float] = None

    # --------------------------------------------------------------------------
    def _disc(self, y: int, k: float) -> float:
        return (1 + k) ** -((y - self.first_forecast) + self.val_offset)

    def run(self) -> dict:
        a = self.assets
        Y = self.years
        n = len(Y)
        L = int(a.econ_life)
        acc_share = a.accel / a.equip
        res_eff = a.residual * acc_share      # resale value as % of equipment cost
        out_streams = {}
        tot = {k: np.zeros(n) for k in [
            "revenue", "var_cost", "power", "fixed_opex", "ebitda", "book_dep", "writeoff",
            "proceeds", "tax_dep", "econ_dep", "capex", "capex_equip", "capex_fac",
            "capex_replacement", "capex_growth", "ic_book", "ic_econ", "potential",
            "alive_equip"]}

        for s in self.streams:
            equip = np.zeros(n)   # equipment $ by vintage
            fac = np.zeros(n)     # facility $ by vintage
            land = np.zeros(n)
            repl = np.zeros(n)
            grow = np.zeros(n)
            rev = np.zeros(n)
            pot = np.zeros(n)
            util = np.zeros(n)

            def yld(v: int) -> float:
                fwd = s.fwd_yield_mult if Y[v] > self.base_year else 1.0
                return s.yield_ * fwd * (1 + s.yield_drift) ** max(0, Y[v] - self.base_year)

            def potential_at(t: int, upto: int) -> float:
                """capacity revenue potential in year index t from vintages v<=upto"""
                p = 0.0
                for v in range(0, min(upto, t) + 1):
                    age = t - v
                    if age >= L or equip[v] == 0:
                        continue
                    ramp = a.ramp0 if age == 0 else 1.0
                    p += equip[v] * yld(v) * (1 - s.erosion) ** age * ramp
                yr = Y[t] if t < n else Y[-1] + (t - n + 1)
                p += s.lease_opex.get(yr, 0.0) * s.lease_markup
                return p

            def path(yr: int) -> float:
                if yr in s.revenue:
                    return s.revenue[yr]
                last = max(s.revenue)
                return s.revenue[last] * (1 + self.g_term) ** (yr - last)

            def path_growth(yr: int) -> float:
                p0 = path(yr - 1)
                return path(yr) / p0 if p0 > 0 else 1.0

            dem = np.zeros(n)   # demand actually available (unserved demand is lost, not banked)

            for t, y in enumerate(Y):
                if s.kind == "capacity":
                    if y <= self.base_year or t == 0:
                        dem[t] = path(y)
                    else:
                        dem[t] = rev[t - 1] * path_growth(y) if rev[t - 1] > 0 else path(y)
                # ---- capex for this stream -------------------------------------------
                retiring = equip[t - L + 1] if t - L + 1 >= 0 else 0.0   # last alive year = t
                if y <= self.explicit_end:
                    c = self.capex_total.get(y, 0.0) * s.share.get(y, s.share_default)
                    equip[t] = c * a.equip
                    fac[t] = c * a.facility
                    land[t] = c * a.land
                    repl[t] = min(equip[t], retiring)
                    grow[t] = c - repl[t]
                else:
                    if s.kind == "capacity":
                        p0 = potential_at(t + 1, t - 1)
                        need = dem[t] * path_growth(y + 1) / s.u_target - p0
                        e_new = max(0.0, need) / (yld(t) * (1 - s.erosion)) if need > 0 else 0.0
                    elif s.kind == "exogenous":
                        # hold compute intensity (alive equipment per $ revenue) at its level at
                        # the end of the explicit period, improving by intensity_decline a year
                        te = Y.index(self.explicit_end)
                        alive_te = sum(equip[v] for v in range(max(0, te - L + 1), te + 1))
                        r_te = s.revenue.get(self.explicit_end, 0.0)
                        inten = alive_te / r_te if r_te > 0 else 0.0
                        r1 = s.revenue.get(y + 1, s.revenue.get(y, 0.0) * (1 + self.g_term))
                        target = r1 * inten * (1 - s.intensity_decline) ** (y + 1 - self.explicit_end)
                        surviving = sum(equip[v] for v in range(max(0, t + 1 - L + 1), t))
                        e_new = max(0.0, target - surviving)
                    else:
                        # cost centre (training): refresh retiring capacity x (1+g) policy
                        alive_prev = sum(equip[v] for v in range(max(0, t - L), t))
                        g = s.post_growth.get(y, self.g_term)
                        e_new = max(0.0, retiring + g * alive_prev)
                    growth_equip = max(0.0, e_new - retiring)
                    equip[t] = e_new
                    fac[t] = growth_equip * a.facility / a.equip
                    land[t] = growth_equip * a.land / a.equip
                    repl[t] = min(e_new, retiring)
                    grow[t] = equip[t] + fac[t] + land[t] - repl[t]

                # ---- revenue ----------------------------------------------------------
                pot[t] = potential_at(t, t)
                if s.kind == "capacity":
                    rev[t] = min(dem[t], s.u_max * pot[t]) if pot[t] > 0 else 0.0
                    util[t] = rev[t] / pot[t] if pot[t] > 0 else 0.0
                elif s.kind == "exogenous":
                    rev[t] = s.revenue.get(y, 0.0)
                    util[t] = s.internal_util
                else:
                    util[t] = s.internal_util

            # ---- depreciation, tax, residual, invested capital by vintage ------------
            book_dep = np.zeros(n)
            writeoff = np.zeros(n)
            proceeds = np.zeros(n)
            tax_dep = np.zeros(n)
            econ_dep = np.zeros(n)
            ic_book = np.zeros(n)
            ic_econ = np.zeros(n)
            alive = np.zeros(n)
            B = a.book_life_equip
            for v in range(n):
                ce, cf, cl = equip[v], fac[v], land[v]
                if ce > 0:
                    acc = 0.0
                    for t in range(v, n):
                        age = t - v
                        if age < L:
                            alive[t] += ce
                            d = ce / B * (0.5 if age == 0 else 1.0)
                            d = min(d, ce - acc)
                            book_dep[t] += d
                            acc += d
                            econ_dep[t] += ce * (1 - res_eff) / L
                            # tax: bonus in year 0, remainder straight line
                            td = ce * a.bonus if age == 0 else 0.0
                            if age < a.tax_life_equip:
                                td += ce * (1 - a.bonus) / a.tax_life_equip
                            tax_dep[t] += td
                            if age == L - 1:
                                # retire at end of last economic year: write off NBV, sell
                                writeoff[t] += ce - acc
                                acc = ce
                                proceeds[t] += ce * res_eff
                                ic_econ[t] += 0.0
                            else:
                                ic_econ[t] += ce * (1 - (age + 1) / L * (1 - res_eff))
                            ic_book[t] += ce - acc
                if cf > 0:
                    for t in range(v, n):
                        age = t - v
                        d = cf / a.book_life_fac if 1 <= age <= a.book_life_fac else 0.0
                        book_dep[t] += d
                        econ_dep[t] += d
                        tax_dep[t] += cf / a.tax_life_fac if 1 <= age <= a.tax_life_fac else 0.0
                        nbv = cf - cf / a.book_life_fac * min(max(age, 0), a.book_life_fac)
                        ic_book[t] += nbv
                        ic_econ[t] += nbv
                if cl > 0:
                    for t in range(v, n):
                        ic_book[t] += cl
                        ic_econ[t] += cl

            var = s.var_cost * rev
            power = alive * (a.power_fixed + a.power_var * util)
            fixed = np.array([s.fixed_opex.get(y, 0.0) + s.lease_opex.get(y, 0.0) for y in Y])
            ebitda = rev - var - power - fixed
            capex = equip + fac + land
            st = dict(revenue=rev, var_cost=var, power=power, fixed_opex=fixed, ebitda=ebitda,
                      book_dep=book_dep, writeoff=writeoff, proceeds=proceeds, tax_dep=tax_dep,
                      econ_dep=econ_dep, capex=capex, capex_equip=equip, capex_fac=fac + land,
                      capex_replacement=repl, capex_growth=grow, ic_book=ic_book,
                      ic_econ=ic_econ, potential=pot, alive_equip=alive, util=util,
                      demand=dem if s.kind == "capacity" else rev.copy())
            st.update(self._derive(st))
            out_streams[s.name] = st
            for k in tot:
                tot[k] = tot[k] + st[k]

        tot.update(self._derive(tot))
        pot = tot["potential"]
        cap_rev = sum(out_streams[s.name]["revenue"] for s in self.streams if s.kind == "capacity")
        tot["util_capacity"] = np.divide(cap_rev, pot, out=np.zeros(n), where=pot > 0)
        res = dict(years=Y, total=tot, streams=out_streams)
        kinds = {s.name: s.kind for s in self.streams}
        sv = {k: self._value(v, kind=kinds[k]) for k, v in out_streams.items()}
        res["stream_valuation"] = sv
        tv_T = sum(v["tv"] for v in sv.values())
        flows = list(tot["fcf"])
        flows[-1] += tv_T
        res["valuation"] = dict(
            pv_fcf=sum(v["pv_fcf"] for v in sv.values()),
            pv_tv=sum(v["pv_tv"] for v in sv.values()),
            npv=sum(v["npv"] for v in sv.values()), tv=tv_T,
            tv_rule="; ".join(f"{k.split(' (')[0]}: {v['tv_rule']}" for k, v in sv.items()),
            terminal_ronic=(tot["nopat_econ"][-1] / tot["avg_ic_econ"][-1]
                            if tot["avg_ic_econ"][-1] > 0 else float("nan")),
            irr_program=_irr(flows))
        return res

    # --------------------------------------------------------------------------
    def _derive(self, d: dict) -> dict:
        tr = self.tax_rate
        ebit_book = d["ebitda"] - d["book_dep"] - d["writeoff"] + d["proceeds"]
        ebit_econ = d["ebitda"] - d["econ_dep"]
        taxable = d["ebitda"] - d["tax_dep"] + d["proceeds"]
        cash_tax = tr * taxable
        nopat_book = ebit_book * (1 - tr)
        nopat_econ = ebit_econ * (1 - tr)
        fcf = d["ebitda"] - cash_tax - d["capex"] + d["proceeds"]
        ic_b, ic_e = d["ic_book"], d["ic_econ"]
        avg_b = np.concatenate([[ic_b[0]], (ic_b[1:] + ic_b[:-1]) / 2])
        avg_e = np.concatenate([[ic_e[0]], (ic_e[1:] + ic_e[:-1]) / 2])
        roic_b = np.divide(nopat_book, avg_b, out=np.zeros_like(avg_b), where=avg_b > 1e-9)
        roic_e = np.divide(nopat_econ, avg_e, out=np.zeros_like(avg_e), where=avg_e > 1e-9)
        # incremental ROIC since the base year: change in economic NOPAT / change in capital
        inc = np.full_like(roic_e, np.nan)
        b = self.years.index(self.base_year)
        for t in range(b + 1, len(roic_e)):
            dic = avg_e[t] - avg_e[b]
            if dic > 1e-6:
                inc[t] = (nopat_econ[t] - nopat_econ[b]) / dic
        return dict(ebit_book=ebit_book, ebit_econ=ebit_econ, cash_tax=cash_tax,
                    nopat_book=nopat_book, nopat_econ=nopat_econ, fcf=fcf,
                    roic_book=roic_b, roic_econ=roic_e, incr_roic=inc, avg_ic_econ=avg_e)

    def terminal(self, d: dict, k: float, kind: str = "exogenous") -> dict:
        g = self.g_term
        nopat = d["nopat_econ"][-1]
        ic = d["avg_ic_econ"][-1]
        ronic = self.terminal_ronic_override if self.terminal_ronic_override is not None else (
            nopat / ic if ic > 1e-9 else 0.0)
        if kind == "cost":
            # training / frontier R&D: a permanent cost of staying at the frontier, growing at g
            return dict(tv=nopat * (1 + g) / (k - g), rule="permanent cost", ronic=float("nan"),
                        nopat_T=nopat)
        if abs(nopat) < 1e-9:
            return dict(tv=0.0, rule="ended", ronic=0.0, nopat_T=0.0)
        if nopat <= 0:
            tv, rule = 0.0, "abandon (NOPAT<=0)"
        elif ronic > k:
            tv, rule = nopat * (1 + g) * (1 - g / ronic) / (k - g), "value-driver growth"
        else:
            tv, rule = nopat / k, "no-growth (RONIC<=k)"
        return dict(tv=tv, rule=rule, ronic=ronic, nopat_T=nopat)

    def _value(self, d: dict, k: Optional[float] = None, kind: str = "exogenous") -> dict:
        k = self.hurdle if k is None else k
        Y = self.years
        pv = 0.0
        for t, y in enumerate(Y):
            if y >= self.first_forecast:
                pv += d["fcf"][t] * self._disc(y, k)
        term = self.terminal(d, k, kind)
        pv_tv = term["tv"] * (1 + k) ** -((Y[-1] - self.first_forecast) + self.val_offset + 0.5)
        # program IRR including sunk (historical) capex, TV at horizon
        flows = list(d["fcf"])
        flows[-1] += term["tv"]
        irr = _irr(flows)
        return dict(pv_fcf=pv, pv_tv=pv_tv, npv=pv + pv_tv, tv=term["tv"], tv_rule=term["rule"],
                    terminal_ronic=term["ronic"], irr_program=irr)


def _irr(flows) -> float:
    f = np.array(flows, dtype=float)

    def npv(r):
        return sum(c / (1 + r) ** i for i, c in enumerate(f))
    try:
        if npv(-0.9) * npv(2.0) > 0:
            return float("nan")
        return brentq(npv, -0.9, 2.0)
    except Exception:
        return float("nan")


# ----------------------------------------------------------------------------------------
# Core (non-AI) business segment
# ----------------------------------------------------------------------------------------
@dataclass
class Segment:
    name: str
    rev0: float
    growth: List[float]
    margin: List[float]
    capex_pct: float
    da_pct: float
    tax: float
    ic0: float
    g_term: float
    ronic_term: float
    wacc: float
    val_offset: float
    nwc_pct: float = 0.0
    ebit_override: Optional[List[float]] = None   # e.g. Reality Labs operating loss path
    rev_override: Optional[List[float]] = None

    def run(self) -> dict:
        N = len(self.growth)
        rev = np.zeros(N)
        r = self.rev0
        for i in range(N):
            r = self.rev_override[i] if self.rev_override is not None else r * (1 + self.growth[i])
            rev[i] = r
        ebit = np.array(self.ebit_override) if self.ebit_override is not None else rev * np.array(self.margin)
        nopat = ebit * (1 - self.tax)
        capex = rev * self.capex_pct
        da = rev * self.da_pct
        prev = np.concatenate([[self.rev0], rev[:-1]])
        dnwc = (rev - prev) * self.nwc_pct
        fcf = nopat + da - capex - dnwc
        ic = self.ic0 + np.cumsum(capex - da + dnwc)
        disc = np.array([(1 + self.wacc) ** -(i + self.val_offset) for i in range(N)])
        pv = float((fcf * disc).sum())
        nT = nopat[-1]
        if nT <= 0:
            tv = 0.0
        else:
            tv = nT * (1 + self.g_term) * (1 - self.g_term / self.ronic_term) / (self.wacc - self.g_term)
        pv_tv = tv * (1 + self.wacc) ** -(N - 1 + self.val_offset + 0.5)
        return dict(revenue=rev, ebit=ebit, nopat=nopat, capex=capex, da=da, fcf=fcf, ic=ic,
                    pv_fcf=pv, pv_tv=pv_tv, value=pv + pv_tv, tv=tv)


# ----------------------------------------------------------------------------------------
# Company = sum of the parts
# ----------------------------------------------------------------------------------------
@dataclass
class Company:
    name: str
    price: float
    shares: float
    net_debt: float
    nonop: Dict[str, float]
    segments: List[Segment]
    ai: AIProgram
    tax: float
    forecast_years: List[int]
    other_income_after_tax: Dict[int, float] = field(default_factory=dict)  # EPS-only items
    meta: dict = field(default_factory=dict)

    def run(self) -> dict:
        segs = {s.name: s.run() for s in self.segments}
        ai = self.ai.run()
        fy = self.forecast_years
        idx = [self.ai.years.index(y) for y in fy]
        A = {k: v[idx] for k, v in ai["total"].items() if isinstance(v, np.ndarray)}
        N = len(fy)
        rev = sum(s["revenue"] for s in segs.values()) + A["revenue"]
        ebit = sum(s["ebit"] for s in segs.values()) + A["ebit_book"]
        nopat = sum(s["nopat"] for s in segs.values()) + A["nopat_book"]
        fcf = sum(s["fcf"] for s in segs.values()) + A["fcf"]
        capex = sum(s["capex"] for s in segs.values()) + A["capex"]
        ic = sum(s["ic"] for s in segs.values()) + A["ic_book"]
        other = np.array([self.other_income_after_tax.get(y, 0.0) for y in fy])
        net_income = nopat + other
        eps = net_income / self.shares
        core_val = {k: v["value"] for k, v in segs.items()}
        ai_val = ai["valuation"]["npv"]
        ev = sum(core_val.values()) + ai_val
        equity = ev - self.net_debt + sum(self.nonop.values())
        ps = equity / self.shares
        avg_ic = np.concatenate([[ic[0]], (ic[1:] + ic[:-1]) / 2])
        return dict(
            segments=segs, ai=ai, years=fy, revenue=rev, ebit=ebit, nopat=nopat, fcf=fcf,
            capex=capex, ic=ic, roic=nopat / avg_ic, eps=eps, net_income=net_income,
            fcf_conversion=np.divide(fcf, net_income, out=np.zeros(N), where=net_income != 0),
            core_values=core_val, ai_value=ai_val, ev=ev, equity=equity, per_share=ps,
            upside=ps / self.price - 1, ai_forecast=A)
