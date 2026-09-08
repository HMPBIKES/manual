#!/usr/bin/env python3
"""
HMP Bikes - Los Angeles store P&L model (Task 3, v1, 2026-09-08).

Monthly P&L and cash over 36 months for three scenarios (conservative / base / aggressive)
x two site configurations (768 Ceres Ave @ $8,000; Pico/Olympic corridor unit @ $7,500),
plus an "SF-equivalent" what-if (SF's ~40 units/month all-SKU pace, ~100 rentals, 300+ battery
subscribers transplanted onto the LA cost base). Five revenue lines:

  1 vehicle sales   retail non-rider FLASH/MK.II ("moto") and e-bike/moped ("ebike") buyers,
                    plus rider purchases that come out of the SOM path
  2 rental          whole-bike rentals to couriers; fleet sized to renters / utilization target
  3 battery swap    subscription (owners); pack float = subscribers x packs per subscriber
  4 service         installed base x $/vehicle-month + walk-in repair
  5 B2B             wholesale to SoCal dealers at a dealer discount; regional service van

Every parameter lives in store_pnl_params.json with lo / base / hi and a tag
(FACT / ESTIMATE / ASSUMPTION); lo = conservative (worse for HMP), hi = aggressive.
Rider-side lines (rental, subscription, rider purchases) are capped by the SOM path from
market_size.py (research/03-market-size.md): ~40 paying riders at month 12, ~72 at month 24.
Retail FLASH/MK.II demand is NOT bounded by the rider SOM - it is the model's largest assumption.

Run:
  python3 store_pnl.py                      scenario x configuration tables, break-even table,
                                            tariff cases, tornado; writes store_pnl_output.csv/.md
  python3 store_pnl.py --json               everything as JSON
  python3 store_pnl.py --set rental_weekly_tier_A=70 --set tariff_rate_moto=1.0
                                            override any parameter (all scenarios) and re-run
  python3 store_pnl.py --scenario base --config ceres_8000 --monthly
                                            print the full 36-month table for one run
"""
import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARAMS_FILE = HERE / "store_pnl_params.json"
OUT_CSV = HERE / "store_pnl_output.csv"
OUT_MD = HERE / "store_pnl_output.md"
SCENARIOS = ("conservative", "base", "aggressive")
MONTHS = 36
WEEKS_PER_MONTH = 52 / 12


# ----------------------------------------------------------------------------- parameters
@dataclass
class P:
    lo: float
    base: float
    hi: float
    tag: str = "ASSUMPTION"
    unit: str = ""
    note: str = ""
    curve: dict | None = None      # month -> value; lo/base/hi is then a multiplier on the curve

    def pick(self, s: str) -> float:
        return {"conservative": self.lo, "base": self.base, "aggressive": self.hi}[s]


def interp(curve: dict, m: float) -> float:
    """Piecewise-linear path through (0, 0) and the curve points, flat after the last point."""
    pts = sorted(curve.items())
    if m <= 0:
        return 0.0
    pm, pv = 0, 0.0
    for cm, cv in pts:
        if m <= cm:
            return pv + (cv - pv) * (m - pm) / (cm - pm)
        pm, pv = cm, cv
    return pts[-1][1]


def load_params():
    raw = json.loads(PARAMS_FILE.read_text())
    params = {}
    for k, v in raw.items():
        if k.startswith("_"):
            continue
        curve = {int(a): float(b) for a, b in v["curve"].items()} if "curve" in v else None
        params[k] = P(v["lo"], v["base"], v["hi"], v.get("tag", "ASSUMPTION"),
                      v.get("unit", ""), v.get("note", ""), curve)
    return params, raw["_configs"], raw.get("_sf_equivalent_overrides", {})


class Values:
    """Scenario-resolved parameter values with optional overrides.
    overrides: {name: number} replaces the scalar (or curve multiplier);
               {name: {"value": x, "curve": {...}}} replaces both."""

    def __init__(self, params: dict, scenario: str, overrides: dict | None = None):
        self.vals = {k: p.pick(scenario) for k, p in params.items()}
        self.curves = {k: p.curve for k, p in params.items()}
        for k, o in (overrides or {}).items():
            if k.startswith("_"):
                continue
            if isinstance(o, dict):
                if "value" in o:
                    self.vals[k] = float(o["value"])
                if "curve" in o:
                    self.curves[k] = {int(a): float(b) for a, b in o["curve"].items()}
            else:
                self.vals[k] = float(o)

    def v(self, k: str) -> float:
        return self.vals[k]

    def c(self, k: str, m: int) -> float:
        cv = self.curves.get(k)
        return self.vals[k] * interp(cv, m) if cv else self.vals[k]


# ----------------------------------------------------------------------------- unit economics
def unit_econ(V: Values) -> dict:
    g = V.v
    asp_m, asp_e = g("price_sale_tier_D_moto"), g("price_sale_tier_A_ebike")
    landed_m = (g("fob_cost_moto") * (1 + g("tariff_rate_moto")) + g("freight_per_unit_moto")
                + g("warranty_reserve_rate") * asp_m)
    landed_e = (g("fob_cost_ebike") * (1 + g("tariff_rate_ebike")) + g("freight_per_unit_ebike")
                + g("warranty_reserve_rate") * asp_e)
    ms = g("rental_fleet_moped_share")
    rental_unit_cost = (1 - ms) * landed_e + ms * landed_e * g("rental_moped_cost_multiplier")
    rental_weekly_list = (1 - ms) * g("rental_weekly_tier_A") + ms * g("rental_weekly_tier_C")
    fee_rate = g("affirm_share_of_retail") * g("affirm_mdr") + (1 - g("affirm_share_of_retail")) * g("card_fee_rate")
    inv_carry_per_unit = landed_m * (g("inventory_days") / 30) * g("inventory_carrying_rate_annual") / 12
    contrib_moto = (asp_m - landed_m - fee_rate * asp_m - g("sales_commission_per_unit")
                    + g("parts_accessory_attach_per_sale") * g("parts_gross_margin") - inv_carry_per_unit)
    contrib_ebike = (asp_e - landed_e - fee_rate * asp_e - g("sales_commission_per_unit")
                     + g("parts_accessory_attach_per_sale") * g("parts_gross_margin")
                     - landed_e * (g("inventory_days") / 30) * g("inventory_carrying_rate_annual") / 12)
    return {
        "asp_moto": asp_m, "asp_ebike": asp_e,
        "cogs_tier_D": landed_m, "cogs_tier_A": landed_e,          # template ids R08 / R05 (DERIVED)
        "gross_margin_moto": (asp_m - landed_m) / asp_m,
        "gross_margin_ebike": (asp_e - landed_e) / asp_e,
        "rental_unit_cost": rental_unit_cost,
        "rental_weekly_list": rental_weekly_list,
        "contribution_per_moto_unit": contrib_moto,
        "contribution_per_ebike_unit": contrib_ebike,
    }


# ----------------------------------------------------------------------------- monthly model
def run(V: Values, cfg: dict) -> dict:
    g, cu = V.v, V.c
    ue = unit_econ(V)
    landed_m, landed_e = ue["cogs_tier_D"], ue["cogs_tier_A"]
    unit_cost_r = ue["rental_unit_cost"]
    ms = g("rental_fleet_moped_share")
    ins_r = (1 - ms) * g("insurance_rental_fleet_per_ebike_month") + ms * g("tier_insurance_per_vehicle_month")
    rent0, sqft = float(cfg["rent_monthly"]), float(cfg["sqft"])
    free_months, sec_mult = int(cfg.get("free_rent_months", 0)), float(cfg.get("security_multiplier", 1.0))
    buildout = (g("tenant_improvements_onetime") + g("security_onetime") + g("fire_code_compliance_onetime")
                + g("dmv_dealer_license_onetime") + g("fixtures_signage_onetime") + g("swap_station_capex_onetime"))
    van_start = int(g("regional_van_start_month"))
    life_r, resid = int(g("vehicle_life_months_rental")), g("vehicle_residual_ratio")
    batt_life = g("battery_life_months_delivery_use")

    rows = []
    rider_prev = 0.0
    fleet_cohorts: list[list] = []      # [month_bought, units]
    fleet = 0.0
    pool_packs = 0.0
    inv_prev = 0.0
    cum_units_installed = g("existing_la_installed_base")
    cum_cash = 0.0
    cum = {"rev": 0.0, "gp": 0.0, "opex": 0.0, "ebitda": 0.0, "op": 0.0, "capex": 0.0,
           "units_moto": 0.0, "units_ebike": 0.0, "units_b2b": 0.0}

    for m in range(1, MONTHS + 1):
        yr = (m - 1) // 12
        # ---- demand
        retail_moto = cu("retail_moto_units_scale", m)
        retail_ebike = cu("retail_ebike_units_scale", m)
        riders = cu("rider_customers_scale", m)
        gross_adds = max(0.0, riders - rider_prev) + g("rider_churn_monthly") * rider_prev
        renters = riders * g("rider_share_rental")
        subs = riders * g("rider_share_battery_sub")
        rider_buys = gross_adds * (1 - g("rider_share_rental")) + renters * g("rental_to_purchase_conversion_la")
        rider_moto = rider_buys * g("rider_buyer_moto_share")
        rider_ebike = rider_buys - rider_moto
        dealers = cu("dealers_active_scale", m)
        b2b_units = dealers * g("dealer_units_per_dealer_month")
        b2b_moto = b2b_units * g("dealer_moto_share")
        b2b_ebike = b2b_units - b2b_moto
        units_moto = retail_moto + rider_moto
        units_ebike = retail_ebike + rider_ebike
        units_retail = units_moto + units_ebike

        # ---- rental fleet (never shrinks; grows to renters / utilization target)
        fleet_needed = math.ceil(renters / g("rental_utilization_target")) if renters > 0 else 0
        target_fleet = max(g("initial_rental_fleet_size"), fleet_needed)
        purchases = max(0.0, target_fleet - fleet)
        if purchases > 0:
            fleet_cohorts.append([m, purchases])
            fleet += purchases
        # end-of-life replacement (residual recovered)
        eol_capex = 0.0
        for coh in fleet_cohorts:
            if m - coh[0] == life_r:
                eol_capex += coh[1] * unit_cost_r * (1 - resid)
                coh[0] = m
        active_rentals = min(renters, fleet)
        theft_units = fleet * g("theft_loss_rate_rental_fleet_annual") / 12

        # ---- battery pool (never shrinks; end-of-life replaced pro rata)
        packs_needed = subs * g("batteries_per_subscriber")
        pack_purch = max(0.0, packs_needed - pool_packs)
        pool_packs += pack_purch
        pack_replace = pool_packs / batt_life

        # ---- revenue
        rev_moto_retail = retail_moto * ue["asp_moto"]
        rev_ebike_retail = retail_ebike * ue["asp_ebike"]
        rev_rider_sales = rider_moto * ue["asp_moto"] + rider_ebike * ue["asp_ebike"]
        rev_b2b = (b2b_moto * ue["asp_moto"] + b2b_ebike * ue["asp_ebike"]) * (1 - g("dealer_discount_b2b"))
        rev_parts = units_retail * g("parts_accessory_attach_per_sale")
        rev_rental = active_rentals * ue["rental_weekly_list"] * g("rental_realized_price_factor") * WEEKS_PER_MONTH
        rev_battery = subs * g("battery_sub_monthly_price")
        installed_base = cum_units_installed
        rev_service = installed_base * g("repair_revenue_per_active_customer_month") + cu("service_walkin_monthly_scale", m)
        rev_sales = rev_moto_retail + rev_ebike_retail + rev_rider_sales
        rev_total = rev_sales + rev_b2b + rev_parts + rev_rental + rev_battery + rev_service

        # ---- COGS
        cogs_vehicles = (units_moto + b2b_moto) * landed_m + (units_ebike + b2b_ebike) * landed_e
        cogs_parts = rev_parts * (1 - g("parts_gross_margin"))
        cogs_service = rev_service * (1 - g("repair_gross_margin"))
        elec_battery = subs * g("swaps_per_subscriber_month") * g("kwh_per_swap") * g("electricity_per_kwh")
        elec_fleet = fleet * g("rental_fleet_kwh_per_unit_month") * g("electricity_per_kwh")
        cogs_total = cogs_vehicles + cogs_parts + cogs_service + elec_battery + elec_fleet
        gross_profit = rev_total - cogs_total

        # ---- opex
        fte_mech = g("fte_mechanic_m1_12") if m <= 12 else g("fte_mechanic_m13_36")
        fte = g("fte_manager") + g("fte_sales_ops") + fte_mech
        staff = ((g("fte_manager") * g("wage_manager_hourly") + g("fte_sales_ops") * g("wage_frontdesk_hourly")
                  + fte_mech * g("wage_technician_hourly")) * g("hours_per_fte_month") * g("payroll_load")
                 + g("sales_commission_per_unit") * units_retail)
        rent = 0.0 if m <= free_months else rent0 * (1 + g("rent_escalation_annual")) ** yr
        nnn = g("rent_nnn_psf_month") * sqft
        occupancy = rent + nnn + g("utilities_monthly")
        insurance = g("insurance_gl_property_monthly") + fleet * ins_r
        security = (g("security_monthly") + g("security_monthly_guard")) * sec_mult
        marketing = g("marketing_monthly") + g("cac_per_rider") * gross_adds + (g("launch_marketing_onetime") if m == 1 else 0.0)
        theft_writeoff = theft_units * unit_cost_r
        fleet_var = (fleet * (g("maintenance_per_rental_vehicle_month") + g("gps_per_vehicle"))
                     + theft_writeoff + g("bad_debt_rate_rental_revenue") * rev_rental)
        rev_retail_all = rev_sales + rev_parts
        fee_affirm = rev_retail_all * g("affirm_share_of_retail") * g("affirm_mdr")
        txns = units_retail + active_rentals * WEEKS_PER_MONTH + subs + rev_service / 60.0
        fee_card = ((rev_retail_all * (1 - g("affirm_share_of_retail")) + rev_rental + rev_battery + rev_service)
                    * g("card_fee_rate") + txns * g("card_fee_per_txn"))
        payments = fee_affirm + fee_card
        gna = g("software_gna_monthly") + g("permits_taxes_monthly")
        van = g("van_running_monthly") if m >= van_start else 0.0
        floor_moto = max(g("min_floor_units_moto"), (units_moto + b2b_moto) * g("inventory_days") / 30)
        floor_ebike = max(g("min_floor_units_ebike"), (units_ebike + b2b_ebike) * g("inventory_days") / 30)
        inv_value = floor_moto * landed_m + floor_ebike * landed_e
        inv_carry = inv_value * g("inventory_carrying_rate_annual") / 12
        opex_total = staff + occupancy + insurance + security + marketing + fleet_var + payments + gna + van + inv_carry
        ebitda = gross_profit - opex_total

        # ---- depreciation and operating profit
        dep_fleet = sum(c[1] * unit_cost_r * (1 - resid) / life_r for c in fleet_cohorts if m - c[0] < life_r)
        dep_batt = pool_packs * g("battery_cost") / batt_life
        dep_van = g("van_capex_onetime") / 36 if m >= van_start else 0.0
        dep_build = buildout / g("buildout_amortization_months")
        depreciation = dep_fleet + dep_batt + dep_van + dep_build
        op_profit = ebitda - depreciation

        # ---- cash
        capex = ((buildout if m == 1 else 0.0) + (g("van_capex_onetime") if m == van_start else 0.0)
                 + (purchases + theft_units) * unit_cost_r + eol_capex
                 + (pack_purch + pack_replace) * g("battery_cost"))
        deposit = g("security_deposit_months") * rent0 if m == 1 else 0.0
        d_wc = inv_value - inv_prev
        net_cash = ebitda + theft_writeoff - capex - d_wc - deposit
        cum_cash += net_cash

        # ---- state
        rider_prev = riders
        inv_prev = inv_value
        cum_units_installed += units_retail
        for k, val in (("rev", rev_total), ("gp", gross_profit), ("opex", opex_total), ("ebitda", ebitda),
                       ("op", op_profit), ("capex", capex), ("units_moto", units_moto),
                       ("units_ebike", units_ebike), ("units_b2b", b2b_units)):
            cum[k] += val

        rows.append({
            "month": m,
            "rev_sales_moto_retail": rev_moto_retail, "rev_sales_ebike_retail": rev_ebike_retail,
            "rev_sales_rider": rev_rider_sales, "rev_b2b_wholesale": rev_b2b, "rev_parts": rev_parts,
            "rev_rental": rev_rental, "rev_battery_sub": rev_battery, "rev_service": rev_service,
            "rev_total": rev_total, "cogs_total": cogs_total, "gross_profit": gross_profit,
            "opex_staff": staff, "opex_occupancy": occupancy, "opex_insurance": insurance,
            "opex_security": security, "opex_marketing": marketing, "opex_fleet_variable": fleet_var,
            "opex_payment_fees": payments, "opex_gna_permits": gna, "opex_van": van,
            "opex_inventory_carry": inv_carry, "opex_total": opex_total, "ebitda": ebitda,
            "depreciation": depreciation, "operating_profit": op_profit, "capex": capex,
            "working_capital_change": d_wc + deposit, "net_cash": net_cash, "cum_cash": cum_cash,
            "units_moto": units_moto, "units_ebike": units_ebike, "units_b2b": b2b_units,
            "rider_customers": riders, "rentals_active": active_rentals, "rental_fleet": fleet,
            "battery_subs": subs, "battery_pool_packs": pool_packs, "installed_base": installed_base,
            "inventory_value": inv_value, "fte": fte,
        })

    # ---- summary
    def first_sustained(key, n=3):
        for i in range(len(rows) - n + 1):
            if all(rows[j][key] >= 0 for j in range(i, i + n)):
                return rows[i]["month"]
        return None

    min_cash = min(r["cum_cash"] for r in rows)
    min_month = next(r["month"] for r in rows if r["cum_cash"] == min_cash)
    r12, r24, r36 = rows[11], rows[23], rows[35]
    summary = {
        "rev_36m": cum["rev"], "gross_profit_36m": cum["gp"], "opex_36m": cum["opex"],
        "ebitda_36m": cum["ebitda"], "operating_profit_36m": cum["op"], "capex_36m": cum["capex"],
        "cum_cash_36m": rows[-1]["cum_cash"], "peak_cash_need": max(0.0, -min_cash), "peak_cash_month": min_month,
        "breakeven_month_op_profit": first_sustained("operating_profit"),
        "breakeven_month_ebitda": first_sustained("ebitda"),
        "units_moto_36m": cum["units_moto"], "units_ebike_36m": cum["units_ebike"], "units_b2b_36m": cum["units_b2b"],
        "m12_rev": r12["rev_total"], "m24_rev": r24["rev_total"], "m36_rev": r36["rev_total"],
        "m24_op_profit": r24["operating_profit"], "m36_op_profit": r36["operating_profit"],
        "m24_rentals": r24["rentals_active"], "m24_battery_subs": r24["battery_subs"],
        "m24_rider_customers": r24["rider_customers"], "m36_fte": r36["fte"],
        "buildout_capex": buildout,
    }
    return {"rows": rows, "summary": summary, "unit_econ": ue}


# ----------------------------------------------------------------------------- analyses
def scenario_grid(params, configs, sf_over, extra_over=None):
    out = {}
    for s in SCENARIOS:
        for ck, cfg in configs.items():
            V = Values(params, s, extra_over)
            out[(s, ck)] = run(V, cfg)
    sfo = dict(sf_over)
    sfo.update(extra_over or {})
    out[("sf_equivalent", "ceres_8000")] = run(Values(params, "base", sfo), configs["ceres_8000"])
    return out


def breakeven_table(params, configs, extra_over=None):
    """FLASH/MK.II units per month needed at month 24 so that operating profit (after
    depreciation of fleet, batteries, van and buildout) is >= 0."""
    rent_levels = [("768 Ceres @ $8,000", "ceres_8000", 8000),
                   ("Corridor unit @ $7,500", "corridor_7500", 7500),
                   ("768 Ceres @ $10,000 (original ask)", "ceres_8000", 10000)]
    rider_levels = [("0 (no rental / subscription)", 0.0), ("SOM-base (72 riders @ M24)", 1.0),
                    ("SOM-high (144 riders @ M24)", 2.0)]
    variants = [("FLASH/MK.II only",
                 {"retail_ebike_units_scale": 0, "dealers_active_scale": 0, "service_walkin_monthly_scale": 0,
                  "existing_la_installed_base": 0}),
                ("plus base e-bike retail, B2B, service", {})]
    table = []
    for rl, ck, rent in rent_levels:
        cfg = dict(configs[ck])
        cfg["rent_monthly"] = rent
        for rn, rscale in rider_levels:
            for vn, vover in variants:
                over = {"retail_moto_units_scale": 0, "rider_customers_scale": rscale}
                if rscale == 0:
                    over["initial_rental_fleet_size"] = 0
                over.update(vover)
                over.update(extra_over or {})
                V = Values(params, "base", over)
                res = run(V, cfg)
                r24 = res["rows"][23]
                uc = res["unit_econ"]["contribution_per_moto_unit"]
                gap = -r24["operating_profit"]
                units = max(0.0, gap) / uc if uc > 0 else float("inf")
                table.append({"rent_level": rl, "rent_monthly": rent, "rider_level": rn, "variant": vn,
                              "m24_fixed_and_uncovered_cost": gap, "m24_rentals": r24["rentals_active"],
                              "m24_battery_subs": r24["battery_subs"],
                              "contribution_per_moto_unit": uc, "moto_units_per_month_needed": units,
                              "moto_revenue_per_month_needed": units * res["unit_econ"]["asp_moto"]})
    return table


def tariff_table(params, configs, extra_over=None):
    out = []
    for t, label in ((0.0, "0% (no China duty / non-China origin)"), (0.25, "25% (Section 301 List 2 only)"),
                     (0.375, "37.5% (current: 25% + 12.5% new Sec. 301 tier) = base"),
                     (1.0, "100% (EV-style Section 301 treatment extended to 8711.60)")):
        over = {"tariff_rate_moto": t, "tariff_rate_ebike": t}
        over.update(extra_over or {})
        V = Values(params, "base", over)
        res = run(V, configs["ceres_8000"])
        be = [r for r in breakeven_table(params, configs, over)
              if r["rent_monthly"] == 8000 and r["rider_level"].startswith("SOM-base")]
        out.append({"tariff": t, "label": label,
                    "gross_margin_moto": res["unit_econ"]["gross_margin_moto"],
                    "gross_margin_ebike": res["unit_econ"]["gross_margin_ebike"],
                    "landed_moto": res["unit_econ"]["cogs_tier_D"], "landed_ebike": res["unit_econ"]["cogs_tier_A"],
                    "cum_cash_36m": res["summary"]["cum_cash_36m"], "peak_cash_need": res["summary"]["peak_cash_need"],
                    "breakeven_month": res["summary"]["breakeven_month_op_profit"],
                    "moto_units_needed_only": be[0]["moto_units_per_month_needed"],
                    "moto_units_needed_with_lines": be[1]["moto_units_per_month_needed"]})
    return out


TORNADO = [
    "retail_moto_units_scale", "retail_ebike_units_scale", "rider_customers_scale", "price_sale_tier_D_moto",
    "fob_cost_moto", "fob_cost_ebike", "rental_weekly_tier_A", "rental_utilization_target",
    "theft_loss_rate_rental_fleet_annual", "battery_sub_monthly_price", "rider_share_battery_sub",
    "rider_share_rental", "dealers_active_scale", "dealer_discount_b2b", "affirm_share_of_retail",
    "repair_revenue_per_active_customer_month", "wage_technician_hourly", "payroll_load",
    "security_monthly_guard", "insurance_gl_property_monthly", "tier_insurance_per_vehicle_month",
    "cac_per_rider", "fire_code_compliance_onetime", "rent_nnn_psf_month", "rider_churn_monthly",
    "battery_life_months_delivery_use", "warranty_reserve_rate", "rental_realized_price_factor",
]


def tornado(params, configs, extra_over=None, ck="ceres_8000"):
    base = run(Values(params, "base", extra_over), configs[ck])["summary"]["cum_cash_36m"]
    out = []
    for k in TORNADO:
        p = params[k]
        vals = {}
        for side, val in (("lo", p.lo), ("hi", p.hi)):
            over = {k: val}
            over.update(extra_over or {})
            vals[side] = run(Values(params, "base", over), configs[ck])["summary"]["cum_cash_36m"]
        out.append({"param": k, "tag": p.tag, "lo_value": p.lo, "hi_value": p.hi,
                    "cash_at_lo": vals["lo"], "cash_at_hi": vals["hi"], "swing": abs(vals["hi"] - vals["lo"])})
    # tariff policy shock (both families), outside the scenario ranges
    vals = {}
    for side, t in (("lo", 1.0), ("hi", 0.25)):
        over = {"tariff_rate_moto": t, "tariff_rate_ebike": t}
        over.update(extra_over or {})
        vals[side] = run(Values(params, "base", over), configs[ck])["summary"]["cum_cash_36m"]
    out.append({"param": "tariff_rate (both families, 100% / 25% policy cases)", "tag": "ESTIMATE",
                "lo_value": 1.0, "hi_value": 0.25, "cash_at_lo": vals["lo"], "cash_at_hi": vals["hi"],
                "swing": abs(vals["hi"] - vals["lo"])})
    out.sort(key=lambda r: -r["swing"])
    return base, out


# ----------------------------------------------------------------------------- formatting
def money(x, k=False):
    if x is None:
        return "n/a"
    if k:
        return f"{x / 1000:,.0f}k" if abs(x) >= 1000 else f"{x:,.0f}"
    return f"{x:,.0f}"


def pct(x):
    return f"{100 * x:.1f}%"


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def scenario_label(s):
    return {"conservative": "Conservative", "base": "Base", "aggressive": "Aggressive",
            "sf_equivalent": "SF-equivalent (what-if)"}[s]


def build_report(params, configs, grid, be, tt, torn_base, torn):
    L = []
    L.append("# HMP Bikes LA store P&L - model output\n")
    L.append("Generated by `la-hub/model/store_pnl.py` from `store_pnl_params.json` (edit the JSON and re-run; "
             "`--set name=value` overrides any parameter). All figures pre-tax, USD, 36-month horizon from opening. "
             "Operating profit = EBITDA minus depreciation of rental fleet, battery float, van and buildout. "
             "Cumulative cash = EBITDA plus non-cash theft write-off, minus capex (buildout, van, fleet, batteries), "
             "floor inventory and the landlord deposit. Scenarios take every parameter at its lo / base / hi corner "
             "(joint corners, not P10/P90); the tornado shows one-at-a-time effects.\n")

    ue = grid[("base", "ceres_8000")]["unit_econ"]
    L.append("## 1. Unit economics (Base)\n")
    L.append(md_table(["Family", "Blended ASP", "Landed COGS (FOB x (1+tariff) + freight + warranty)", "Gross margin",
                       "Contribution / unit after fees, commission, parts attach, carrying"],
                      [["FLASH / MK.II (tier D)", money(ue["asp_moto"]), money(ue["cogs_tier_D"]),
                        pct(ue["gross_margin_moto"]), money(ue["contribution_per_moto_unit"])],
                       ["E-bike / moped (tiers A-B)", money(ue["asp_ebike"]), money(ue["cogs_tier_A"]),
                        pct(ue["gross_margin_ebike"]), money(ue["contribution_per_ebike_unit"])]]))
    L.append(f"\nRental fleet unit cost (blended) {money(ue['rental_unit_cost'])}; blended list rental "
             f"{money(ue['rental_weekly_list'])}/week; base tariff {pct(params['tariff_rate_moto'].base)} "
             "(see section 5).\n")

    L.append("## 2. Scenario x configuration summary (36 months)\n")
    hdr = ["Scenario", "Site", "Revenue 36m", "Gross profit 36m", "Opex 36m", "EBITDA 36m", "Op. profit 36m",
           "Cum. cash M36", "Peak cash need (month)", "Break-even month (op. profit, 3 mo sustained)",
           "Break-even month (EBITDA)", "M24 revenue / mo", "M24 op. profit / mo", "M24 rentals", "M24 battery subs",
           "Units 36m retail moto / ebike / B2B"]
    rows = []
    for (s, ck), res in grid.items():
        sm = res["summary"]
        rows.append([scenario_label(s), configs[ck]["label"], money(sm["rev_36m"], True), money(sm["gross_profit_36m"], True),
                     money(sm["opex_36m"], True), money(sm["ebitda_36m"], True), money(sm["operating_profit_36m"], True),
                     money(sm["cum_cash_36m"], True), f"{money(sm['peak_cash_need'], True)} (M{sm['peak_cash_month']})",
                     sm["breakeven_month_op_profit"] or "none in 36", sm["breakeven_month_ebitda"] or "none in 36",
                     money(sm["m24_rev"], True), money(sm["m24_op_profit"], True), f"{sm['m24_rentals']:.0f}",
                     f"{sm['m24_battery_subs']:.0f}",
                     f"{sm['units_moto_36m']:.0f} / {sm['units_ebike_36m']:.0f} / {sm['units_b2b_36m']:.0f}"])
    L.append(md_table(hdr, rows))
    L.append("")

    res = grid[("base", "ceres_8000")]
    L.append("## 3. Base / 768 Ceres @ $8,000 - monthly P&L (selected months; all 36 in store_pnl_output.csv)\n")
    keys = [("rev_sales_moto_retail", "Sales FLASH/MK.II retail"), ("rev_sales_ebike_retail", "Sales e-bike/moped retail"),
            ("rev_sales_rider", "Sales to riders (SOM)"), ("rev_b2b_wholesale", "B2B wholesale"), ("rev_parts", "Parts/accessories"),
            ("rev_rental", "Rental"), ("rev_battery_sub", "Battery subscription"), ("rev_service", "Service"),
            ("rev_total", "Revenue"), ("gross_profit", "Gross profit"), ("opex_staff", "Staff"),
            ("opex_occupancy", "Rent + NNN + utilities"), ("opex_insurance", "Insurance"), ("opex_security", "Security"),
            ("opex_marketing", "Marketing + CAC"), ("opex_fleet_variable", "Fleet maint/GPS/theft/bad debt"),
            ("opex_payment_fees", "Affirm + card fees"), ("opex_gna_permits", "G&A + permits"), ("opex_van", "Van running"),
            ("opex_inventory_carry", "Inventory carrying"), ("opex_total", "Opex"), ("ebitda", "EBITDA"),
            ("depreciation", "Depreciation"), ("operating_profit", "Operating profit"), ("capex", "Capex"),
            ("working_capital_change", "Working capital + deposit"), ("net_cash", "Net cash"), ("cum_cash", "Cumulative cash"),
            ("units_moto", "Units FLASH/MK.II (retail+rider)"), ("units_ebike", "Units e-bike/moped (retail+rider)"),
            ("units_b2b", "Units B2B"), ("rider_customers", "Rider customers (SOM)"), ("rentals_active", "Rentals active"),
            ("rental_fleet", "Rental fleet owned"), ("battery_subs", "Battery subscribers"), ("installed_base", "Installed base"),
            ("fte", "FTE")]
    sel = [1, 2, 3, 6, 9, 12, 18, 24, 30, 36]
    rows = []
    for k, lab in keys:
        rows.append([lab] + [money(res["rows"][m - 1][k]) if k not in ("fte",) else f"{res['rows'][m - 1][k]:.1f}" for m in sel])
    L.append(md_table(["Line"] + [f"M{m}" for m in sel], rows))
    L.append("")

    L.append("## 4. Break-even: FLASH/MK.II units per month needed at month 24 (Base costs)\n")
    L.append("Units of FLASH/MK.II per month (at the base blended ASP and landed cost) that make month-24 operating profit "
             "zero, for each rent level, given what rental + battery subscription deliver. 'FLASH/MK.II only' = no e-bike "
             "retail, no B2B, no walk-in service; 'plus lines' = base e-bike retail (10/mo at M24), B2B (12/mo) and service "
             "also contribute. Fixed cost at M24 includes 3.5 FTE, rent escalated once, insurance, security, marketing, "
             "G&A, van, min floor stock carrying and depreciation of buildout.\n")
    hdr = ["Rent level", "Rental/subscription level", "M24 rentals / subs", "Uncovered cost / mo (FLASH-only case)",
           "FLASH/MK.II units/mo needed - FLASH only", "FLASH/MK.II units/mo needed - plus lines",
           "Revenue/mo needed (plus lines)"]
    rows = []
    for i in range(0, len(be), 2):
        a, b = be[i], be[i + 1]
        rows.append([a["rent_level"], a["rider_level"], f"{a['m24_rentals']:.0f} / {a['m24_battery_subs']:.0f}",
                     money(a["m24_fixed_and_uncovered_cost"]), f"{a['moto_units_per_month_needed']:.1f}",
                     f"{b['moto_units_per_month_needed']:.1f}", money(b["moto_revenue_per_month_needed"])])
    L.append(md_table(hdr, rows))
    L.append(f"\nContribution per FLASH/MK.II unit used: {money(be[0]['contribution_per_moto_unit'])}. Base plan sells "
             f"{grid[('base', 'ceres_8000')]['rows'][23]['units_moto']:.1f} FLASH/MK.II per month at M24 "
             "(retail + rider).\n")

    L.append("## 5. Tariff cases (Base, 768 Ceres @ $8,000; both families at the same rate)\n")
    L.append("Base = 37.5%: HTS 8711.60.0090 is MFN-free but carries Section 301 List 2 (9903.88.02) +25% (CBP ruling "
             "NY N344662, 2024-12-20); the IEEPA fentanyl/reciprocal layers were struck down 2026-02-20; the 10% Section 122 "
             "surcharge expired 2026-07-24 and secondary sources place China in the 12.5% tier of the replacement "
             "country-differentiated Section 301 action (confirm with a customs broker). 100% is the Section 301 EV rate "
             "(HTS 8703), shown as a policy-shock case. 0% = non-China sourcing or an exclusion.\n")
    hdr = ["Tariff", "Landed FLASH/MK.II", "GM FLASH/MK.II", "Landed e-bike", "GM e-bike", "Cum. cash M36",
           "Peak cash need", "Break-even month", "Units/mo needed (SOM-base, FLASH only)", "Units/mo needed (SOM-base, plus lines)"]
    rows = [[t["label"], money(t["landed_moto"]), pct(t["gross_margin_moto"]), money(t["landed_ebike"]),
             pct(t["gross_margin_ebike"]), money(t["cum_cash_36m"], True), money(t["peak_cash_need"], True),
             t["breakeven_month"] or "none", f"{t['moto_units_needed_only']:.1f}", f"{t['moto_units_needed_with_lines']:.1f}"]
            for t in tt]
    L.append(md_table(hdr, rows))
    L.append("")

    L.append("## 6. Sensitivity tornado - 36-month cumulative cash (Base, 768 Ceres @ $8,000)\n")
    L.append(f"Base cumulative cash at M36: {money(torn_base)}. Each parameter moved alone to its conservative (lo) and "
             "aggressive (hi) value; sorted by swing.\n")
    hdr = ["Parameter", "Tag", "lo value", "hi value", "Cum. cash at lo", "Cum. cash at hi", "Swing"]
    rows = [[t["param"], t["tag"], t["lo_value"], t["hi_value"], money(t["cash_at_lo"], True),
             money(t["cash_at_hi"], True), money(t["swing"], True)] for t in torn]
    L.append(md_table(hdr, rows))
    L.append("")

    sf = grid[("sf_equivalent", "ceres_8000")]
    L.append("## 7. What SF-equivalent performance would look like in LA (768 Ceres @ $8,000, Base costs)\n")
    L.append("SF anchors (founder): >1,000 vehicles in ~25 months (~40/month all-SKU), ~100 whole-bike rentals, 300+ "
             "battery subscribers. Transplanted as: 16 FLASH/MK.II + 4 e-bike retail per month from M6 plus rider "
             "purchases from a rider path of 200 (M12) / 400 (M24) customers with 25% renting and 75% on battery "
             "subscription (~100 rentals and ~300 subscribers at M24). Not a forecast: the market model puts LA's "
             "rider-side SOM at 72 (50-150) by M24, i.e. one-fifth of this.\n")
    sm = sf["summary"]
    r24 = sf["rows"][23]
    L.append(md_table(["Metric", "SF-equivalent in LA", "Base"],
                      [["Revenue 36m", money(sm["rev_36m"], True), money(grid[('base', 'ceres_8000')]['summary']['rev_36m'], True)],
                       ["EBITDA 36m", money(sm["ebitda_36m"], True), money(grid[('base', 'ceres_8000')]['summary']['ebitda_36m'], True)],
                       ["Cum. cash M36", money(sm["cum_cash_36m"], True), money(grid[('base', 'ceres_8000')]['summary']['cum_cash_36m'], True)],
                       ["Peak cash need", money(sm["peak_cash_need"], True), money(grid[('base', 'ceres_8000')]['summary']['peak_cash_need'], True)],
                       ["Break-even month (op. profit)", sm["breakeven_month_op_profit"] or "none",
                        grid[('base', 'ceres_8000')]['summary']['breakeven_month_op_profit'] or "none"],
                       ["M24 revenue / month", money(sm["m24_rev"]), money(grid[('base', 'ceres_8000')]['summary']['m24_rev'])],
                       ["M24 op. profit / month", money(sm["m24_op_profit"]), money(grid[('base', 'ceres_8000')]['summary']['m24_op_profit'])],
                       ["M24 units/mo all-SKU (retail+rider+B2B)",
                        f"{r24['units_moto'] + r24['units_ebike'] + r24['units_b2b']:.0f}",
                        f"{grid[('base', 'ceres_8000')]['rows'][23]['units_moto'] + grid[('base', 'ceres_8000')]['rows'][23]['units_ebike'] + grid[('base', 'ceres_8000')]['rows'][23]['units_b2b']:.0f}"],
                       ["M24 rentals / battery subs", f"{r24['rentals_active']:.0f} / {r24['battery_subs']:.0f}",
                        f"{grid[('base', 'ceres_8000')]['rows'][23]['rentals_active']:.0f} / {grid[('base', 'ceres_8000')]['rows'][23]['battery_subs']:.0f}"]]))
    L.append("")
    L.append("## 8. Reading notes\n")
    L.append("- Conservative and Aggressive are all-corner cases: every ESTIMATE/ASSUMPTION at its worse or better value "
             "at once. Use the tornado for what actually moves the answer.\n"
             "- Rider-side lines are capped by the SOM path (market_size.py); FLASH/MK.II retail demand is an assumption "
             "with no LA evidence - the break-even table expresses the decision in those units.\n"
             "- Every parameter's tag and source is in store_pnl_params.json and store_pnl_notes.md; 'ask_hmp' names the "
             "assumptions_template.csv row whose SF value should replace it.\n")
    return "\n".join(L)


def write_csv(grid):
    keys = list(next(iter(grid.values()))["rows"][0].keys())
    with OUT_CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "config"] + keys)
        for (s, ck), res in grid.items():
            for r in res["rows"]:
                w.writerow([s, ck] + [f"{r[k]:.2f}" if isinstance(r[k], float) else r[k] for k in keys])


def print_monthly(res):
    keys = ["month", "rev_total", "gross_profit", "opex_total", "ebitda", "operating_profit", "capex", "net_cash",
            "cum_cash", "units_moto", "units_ebike", "units_b2b", "rentals_active", "battery_subs", "installed_base"]
    print(" ".join(f"{k[:12]:>12s}" for k in keys))
    for r in res["rows"]:
        print(" ".join(f"{r[k]:>12,.0f}" for k in keys))


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--set", action="append", default=[], help="name=value override (applies to all scenarios)")
    ap.add_argument("--scenario", choices=SCENARIOS)
    ap.add_argument("--config")
    ap.add_argument("--monthly", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()

    params, configs, sf_over = load_params()
    extra = {}
    for s in args.set:
        k, v = s.split("=", 1)
        if k not in params:
            raise SystemExit(f"unknown parameter {k}")
        extra[k] = float(v)

    if args.monthly:
        s, ck = args.scenario or "base", args.config or "ceres_8000"
        res = run(Values(params, s, extra), configs[ck])
        print(f"{s} / {configs[ck]['label']}")
        print_monthly(res)
        for k, v in res["summary"].items():
            print(f"  {k:32s} {v if not isinstance(v, float) else f'{v:,.0f}'}")
        return

    grid = scenario_grid(params, configs, sf_over, extra)
    be = breakeven_table(params, configs, extra)
    tt = tariff_table(params, configs, extra)
    torn_base, torn = tornado(params, configs, extra)

    if args.json:
        out = {"summary": {f"{s}|{ck}": r["summary"] for (s, ck), r in grid.items()},
               "unit_econ": {f"{s}|{ck}": r["unit_econ"] for (s, ck), r in grid.items()},
               "breakeven": be, "tariff": tt, "tornado_base_cash": torn_base, "tornado": torn,
               "monthly": {f"{s}|{ck}": r["rows"] for (s, ck), r in grid.items()}}
        print(json.dumps(out, indent=1, default=str))
        return

    report = build_report(params, configs, grid, be, tt, torn_base, torn)
    print(report)
    if not args.no_write:
        write_csv(grid)
        OUT_MD.write_text(report + "\n")
        print(f"\nwrote {OUT_CSV.name} and {OUT_MD.name}")


if __name__ == "__main__":
    main()
