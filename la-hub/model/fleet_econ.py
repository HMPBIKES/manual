#!/usr/bin/env python3
"""Fleet unit economics for HMP Bikes in Los Angeles.

Three ways to "do fleet":
  A. HMP-operated rental fleet (what 415 eBikes does in SF): HMP owns the vehicle, rider pays weekly/monthly.
  B. B2B sale to a fleet operator at a fleet discount: HMP sells 10-50 units, cash up front or via a lessor.
  C. B2B lease: HMP stays the owner and leases to an operator per unit-month (HMP carries the capital).

Every number is a named parameter below; edit or override with --set name=value.
Tags: FACT = sourced, ESTIMATE = derived from a sourced number, ASSUMPTION = judgment.
"""
import argparse, json, sys

P = {
    # ----- vehicles: landed cost to LA, retail ASP, fleet discount -----
    "landed_inno":   {"v": 1300, "tag": "ESTIMATE", "note": "INNO-A Pro landed cost; P&L model blended rental unit cost $1,643 incl. moped share; ASK HMP invoice"},
    "landed_mk2":    {"v": 1900, "tag": "ESTIMATE", "note": "MK.II at ~48% of $3,999 list, same ratio as FLASH ($2,800 / $6,000); ASK HMP"},
    "landed_flash":  {"v": 2800, "tag": "FACT",     "note": "founder: $3,000 landed to SF, ~$2,800 to LA"},
    "asp_inno":      {"v": 2300, "tag": "FACT",     "note": "Shopify 2025-26 net sales / orders for INNO-A Pro"},
    "asp_mk2":       {"v": 3999, "tag": "FACT",     "note": "list"},
    "asp_flash":     {"v": 6000, "tag": "FACT",     "note": "founder: sells $6,000-6,500"},
    "fleet_discount_10":  {"v": 0.10, "tag": "ASSUMPTION", "note": "10-unit order"},
    "fleet_discount_25":  {"v": 0.15, "tag": "ASSUMPTION", "note": "25-unit order"},
    "fleet_discount_50":  {"v": 0.20, "tag": "ASSUMPTION", "note": "50-unit order; powersports fleet/dealer discounts 10-25%"},
    "pdi_and_delivery_per_unit": {"v": 60,  "tag": "ESTIMATE", "note": "assembly, PDI, local delivery labor per unit"},
    "fleet_warranty_reserve_pct": {"v": 0.04, "tag": "ASSUMPTION", "note": "share of fleet price reserved for 24-month fleet warranty claims; delivery duty cycle"},
    "telematics_hw":  {"v": 90,   "tag": "ESTIMATE", "note": "GPS + immobilizer hardware per unit (Monimoto / 4G tracker class)"},
    "telematics_sub": {"v": 12,   "tag": "ESTIMATE", "note": "USD per unit-month subscription (P&L param gps_per_vehicle)"},
    "b2b_sales_cost_per_unit": {"v": 80, "tag": "ASSUMPTION", "note": "share of a B2B salesperson's cost per unit sold (e.g. $8k/mo at 100 units/yr)"},

    # ----- mode A: HMP-operated rental (per owned unit-month) -----
    "rent_sf_monthly_inno":   {"v": 390, "tag": "FACT", "note": "Shopify 2026 YTD: INNO-A Rental Plan Monthly $42,957 / 110 orders; Quarterly-commit $327/mo; Weekly $180/wk"},
    "rent_whizz_sf_monthly":  {"v": 169, "tag": "FACT", "note": "Whizz Storm-2 from $169/mo rent-to-own, $99 buyout after 12 payments (getwhizz.com, 2026-09)"},
    "rent_la_monthly_base":   {"v": 220, "tag": "ASSUMPTION", "note": "LA price if Whizz/Zoomo-class competitors arrive: between Whizz $169 and SF $327 quarterly rate"},
    "realized_price_factor":  {"v": 0.90, "tag": "ASSUMPTION", "note": "promos, free first week (P&L param)"},
    "utilization":            {"v": 0.75, "tag": "ASSUMPTION", "note": "rented / owned (P&L param); SF actual is ASK HMP"},
    "life_months":            {"v": 36,   "tag": "ASSUMPTION", "note": "straight-line to zero for delivery duty (P&L param)"},
    "maint_per_unit_month":   {"v": 30,   "tag": "ASSUMPTION", "note": "parts + outside labor (P&L param)"},
    "insurance_per_unit_month": {"v": 10, "tag": "ESTIMATE", "note": "property/theft rider (P&L param)"},
    "theft_rate_annual":      {"v": 0.08, "tag": "ASSUMPTION", "note": "share of fleet value lost per year net of deposits (P&L param)"},
    "bad_debt_pct":           {"v": 0.05, "tag": "ASSUMPTION", "note": "uncollected billings (P&L param)"},
    "electricity_per_unit_month": {"v": 7, "tag": "ESTIMATE", "note": "30 kWh at $0.25"},
    "battery_sub_monthly":    {"v": 50,   "tag": "FACT", "note": "Shopify 2026 YTD Battery Rental Plan Monthly $29,600 / 583 orders"},
    "parking_monthly":        {"v": 100,  "tag": "FACT", "note": "Shopify 2026 YTD Parking payment $34,773 / 346 orders"},
    "ops_labor_per_unit_month": {"v": 25, "tag": "ESTIMATE", "note": "one fleet tech ($5,500/mo loaded) per ~200 units incl. reconditioning, swaps, repo"},

    # ----- mode C: HMP as lessor to an operator -----
    "lease_term_months":      {"v": 24,   "tag": "ASSUMPTION", "note": ""},
    "lease_residual_pct":     {"v": 0.25, "tag": "ASSUMPTION", "note": "residual value at end of 24 months as share of landed cost"},
    "cost_of_capital_annual": {"v": 0.14, "tag": "ESTIMATE", "note": "small-business equipment finance / revolver in 2026"},
    "lease_markup":           {"v": 1.35, "tag": "ASSUMPTION", "note": "lease payment vs. HMP's own carrying cost (capital + depreciation + service)"},
}


def get(name):
    return P[name]["v"]


def mode_a(price_monthly):
    """Contribution per OWNED unit-month for an HMP-operated rental fleet."""
    rev = price_monthly * get("realized_price_factor") * get("utilization")
    rev_bad = rev * get("bad_debt_pct")
    dep = get("landed_inno") / get("life_months")
    theft = get("landed_inno") * get("theft_rate_annual") / 12
    cost = dep + theft + get("maint_per_unit_month") + get("insurance_per_unit_month") + get("telematics_sub") \
        + get("electricity_per_unit_month") + get("ops_labor_per_unit_month") + rev_bad
    return {"revenue": rev, "cost": cost, "contribution": rev - cost, "capital_per_unit": get("landed_inno") + get("telematics_hw")}


def mode_b(product, n):
    """Contribution per unit for a B2B sale of n units."""
    disc = get("fleet_discount_10") if n <= 10 else get("fleet_discount_25") if n <= 25 else get("fleet_discount_50")
    asp = get(f"asp_{product}")
    price = asp * (1 - disc)
    landed = get(f"landed_{product}")
    cost = landed + get("pdi_and_delivery_per_unit") + price * get("fleet_warranty_reserve_pct") + get("telematics_hw") + get("b2b_sales_cost_per_unit")
    return {"fleet_price": price, "discount": disc, "contribution": price - cost}


def mode_c(product):
    """HMP leases a vehicle to an operator: monthly payment and HMP contribution per unit-month."""
    landed = get(f"landed_{product}") + get("telematics_hw")
    term = get("lease_term_months")
    residual = landed * get("lease_residual_pct")
    dep = (landed - residual) / term
    capital = landed * get("cost_of_capital_annual") / 12
    service = get("maint_per_unit_month") + get("telematics_sub") + get("insurance_per_unit_month")
    carrying = dep + capital + service
    payment = carrying * get("lease_markup")
    return {"lease_payment": payment, "carrying_cost": carrying, "contribution": payment - carrying, "capital_per_unit": landed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", action="append", default=[], help="name=value override")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    for s in a.set:
        k, v = s.split("=", 1)
        if k not in P:
            sys.exit(f"unknown parameter {k}")
        P[k]["v"] = float(v)

    out = {"mode_a": {}, "mode_b": {}, "mode_c": {}}
    for label, price in (("SF price $390/mo", get("rent_sf_monthly_inno")), ("LA base $220/mo", get("rent_la_monthly_base")), ("Whizz-matched $169/mo", get("rent_whizz_sf_monthly"))):
        out["mode_a"][label] = mode_a(price)
    for prod in ("inno", "mk2", "flash"):
        out["mode_b"][prod] = {n: mode_b(prod, n) for n in (10, 25, 50)}
        out["mode_c"][prod] = mode_c(prod)

    if a.json:
        print(json.dumps(out, indent=1))
        return

    print("## Mode A: HMP-operated INNO rental fleet, per OWNED unit-month\n")
    print("| Price point | Revenue | Cost | Contribution | Units for $500k/yr | Capital for that fleet |")
    print("|---|---|---|---|---|---|")
    for label, r in out["mode_a"].items():
        c = r["contribution"]
        units = 500000 / (c * 12) if c > 0 else float("inf")
        cap = units * r["capital_per_unit"] if c > 0 else float("inf")
        print(f"| {label} | ${r['revenue']:.0f} | ${r['cost']:.0f} | ${c:.0f} | {units:,.0f} | ${cap/1e6:.1f}M |")
    print("\nAdd-ons per active rider (not per owned unit): battery subscription ~$50/mo and parking ~$100/mo (SF Shopify 2026 YTD), each near 70-80% margin.\n")

    print("## Mode B: B2B sale at fleet discount, contribution per unit\n")
    print("| Product | 10 units | 25 units | 50 units | Units for $500k (25-unit pricing) |")
    print("|---|---|---|---|---|")
    for prod, rows in out["mode_b"].items():
        c25 = rows[25]["contribution"]
        cells = " | ".join(f"${rows[n]['fleet_price']:,.0f} → ${rows[n]['contribution']:,.0f}" for n in (10, 25, 50))
        print(f"| {prod.upper()} | {cells} | {500000 / c25:,.0f} |")

    print("\n## Mode C: HMP leases to an operator (24 months), per unit-month\n")
    print("| Product | Lease payment | HMP carrying cost | Contribution | Capital tied up per unit | Units for $500k/yr |")
    print("|---|---|---|---|---|---|")
    for prod, r in out["mode_c"].items():
        units = 500000 / (r["contribution"] * 12)
        print(f"| {prod.upper()} | ${r['lease_payment']:.0f} | ${r['carrying_cost']:.0f} | ${r['contribution']:.0f} | ${r['capital_per_unit']:,.0f} | {units:,.0f} (≈ ${units * r['capital_per_unit']/1e6:.1f}M capital) |")

    print("\n## Parameters\n")
    print("| Name | Value | Tag | Note |")
    print("|---|---|---|---|")
    for k, v in P.items():
        print(f"| {k} | {v['v']} | {v['tag']} | {v['note']} |")


if __name__ == "__main__":
    main()
