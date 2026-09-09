## Mode A (contrast only): HMP-operated INNO rental fleet, per OWNED unit-month

| Price point | Revenue | Cost | Contribution | Units for $500k/yr | Capital for that fleet |
|---|---|---|---|---|---|
| SF price $390/mo | $263 | $147 | $116 | 358 | $0.5M |
| LA base $199/mo | $134 | $140 | $-6 | not reachable | — |
| Whizz-matched $169/mo | $114 | $139 | $-25 | not reachable | — |

Add-ons per active rider (not per owned unit): battery subscription ~$50/mo and parking ~$100/mo (SF Shopify 2026 YTD), each near 70-80% margin.

## Mode B: B2B sale at fleet discount, contribution per unit

| Product | 10 units | 25 units | 50 units | Units for $500k (25-unit pricing) |
|---|---|---|---|---|
| INNO | $2,070 → $396 | $1,955 → $288 | $1,840 → $180 | 1,738 |
| MK2 | $3,599 → $1,233 | $3,399 → $1,045 | $3,199 → $857 | 478 |
| FLASH | $5,400 → $2,026 | $5,100 → $1,744 | $4,800 → $1,462 | 287 |

## Mode C: HMP leases to an operator (24 months), per unit-month

| Product | Lease payment | HMP carrying cost | Contribution | Capital tied up per unit | Units for $500k/yr |
|---|---|---|---|---|---|
| INNO | $151 | $112 | $39 | $1,410 | 1,068 (≈ $1.5M capital) |
| MK2 | $246 | $182 | $64 | $2,010 | 653 (≈ $1.3M capital) |
| FLASH | $298 | $221 | $77 | $2,910 | 539 (≈ $1.6M capital) |

## Parameters

| Name | Value | Tag | Note |
|---|---|---|---|
| landed_inno | 1300 | ESTIMATE | INNO-A Pro landed cost; P&L model blended rental unit cost $1,643 incl. moped share; within the $1,500-3,000 fleet-grade e-bike band operators cite (Levy Fleets 2026); ASK HMP invoice |
| landed_mk2 | 1900 | ESTIMATE | MK.II at ~48% of $3,999 list, same ratio as FLASH ($2,800 / $6,000); ASK HMP |
| landed_flash | 2800 | FACT | founder: $3,000 landed to SF, ~$2,800 to LA |
| asp_inno | 2300 | FACT | Shopify 2025-26 net sales / orders for INNO-A Pro |
| asp_mk2 | 3999 | FACT | list |
| asp_flash | 6000 | FACT | founder: sells $6,000-6,500 |
| fleet_discount_10 | 0.1 | ASSUMPTION | 10-unit order |
| fleet_discount_25 | 0.15 | ASSUMPTION | 25-unit order |
| fleet_discount_50 | 0.2 | ASSUMPTION | 50-unit order; Zero clears at up to $5,000 off (30-40%) but FLASH at $4,800 is already ~30% under Zero's cheapest; compete on price level not percent |
| pdi_and_delivery_per_unit | 60 | ESTIMATE | assembly, PDI, local delivery labor per unit |
| fleet_warranty_reserve_pct | 0.06 | ASSUMPTION | share of fleet price reserved for a 24-month delivery-duty warranty; 6% until 100 fleet units have 12 months of claims history (Cake: two recalls preceded its 2024 bankruptcy) |
| telematics_hw | 110 | ESTIMATE | wired 4G module with immobilizer relay $45-120 in quantity (Atom Mobility 2025) plus install labor; battery trackers (Monimoto $179) cannot immobilize |
| telematics_sub_a | 12 | ESTIMATE | Mode A: HMP pays connectivity + fleet SaaS seat per bike |
| telematics_sub_bc | 6 | ESTIMATE | Mode B/C: connectivity $2-5/mo (Trackimo $60/yr, Monimoto $49/yr); buyer runs the platform |
| b2b_sales_cost_per_unit | 80 | ASSUMPTION | share of a B2B salesperson's cost per unit sold (e.g. $8k/mo at 100 units/yr) |
| rent_sf_monthly_inno | 390 | FACT | Shopify 2026 YTD: INNO-A Rental Plan Monthly $42,957 / 110 orders; Quarterly-commit $327/mo; Weekly $180/wk |
| rent_whizz_sf_monthly | 169 | FACT | Whizz Storm-2 from $169/mo rent-to-own, $99 buyout after 12 payments (getwhizz.com, 2026-09) |
| rent_la_monthly_base | 199 | ASSUMPTION | LA rider price if Whizz/Zoomo-class competitors arrive: Levy all-in operator subscription $149, Whizz $169; $199 needs a battery/service bundle |
| realized_price_factor | 0.9 | ASSUMPTION | promos, free first week (P&L param) |
| utilization | 0.75 | ASSUMPTION | rented / owned (P&L param); SF actual is ASK HMP |
| life_months | 36 | ASSUMPTION | straight-line to zero for delivery duty (P&L param) |
| maint_per_unit_month | 30 | ASSUMPTION | parts + outside labor (P&L param) |
| insurance_inno_month | 15 | ESTIMATE | e-bike fleet property/theft $5-26 per bike-month on 15-25 bike fleets (lendcontrol 2026); delivery use at the high end |
| insurance_moto_month | 60 | ESTIMATE | commercial rental/delivery e-motorcycle is surplus-lines (XInsurance); no public rate; $40-100 per unit-month assumed |
| theft_rate_annual | 0.08 | ASSUMPTION | share of fleet value lost per year net of deposits (P&L param); insurers price on storage, locks and trackers, so this should fall with wired immobilizers |
| bad_debt_pct | 0.05 | ASSUMPTION | uncollected billings (P&L param) |
| electricity_per_unit_month | 7 | ESTIMATE | 30 kWh at $0.25 |
| battery_sub_monthly | 50 | FACT | Shopify 2026 YTD Battery Rental Plan Monthly $29,600 / 583 orders |
| parking_monthly | 100 | FACT | Shopify 2026 YTD Parking payment $34,773 / 346 orders |
| ops_labor_per_unit_month | 25 | ESTIMATE | one fleet tech ($5,500/mo loaded) per ~200 units incl. reconditioning, swaps, repo |
| lease_term_months | 24 | ASSUMPTION |  |
| lease_residual_pct | 0.25 | ASSUMPTION | residual value at end of 24 months as share of landed cost |
| cost_of_capital_annual | 0.14 | ESTIMATE | HMP's own small-business equipment finance / revolver in 2026; customer-side alternative (Clicklease-type lease-to-own) runs an implied 35-60% effective APR |
| lease_markup | 1.35 | ASSUMPTION | lease payment vs. HMP's own carrying cost (capital + depreciation + service) |
