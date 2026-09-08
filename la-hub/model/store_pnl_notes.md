# store_pnl.py 假设说明（自动从 store_pnl_params.json 生成）

每个参数带 lo / base / hi 和 FACT / ESTIMATE / ASSUMPTION 标签；`ask_hmp` 指向 assumptions_template.csv 里应由 HMP 的 SF 数据替换的行。改 JSON 重跑 `python3 store_pnl.py`，或 `--set name=value` 临时覆盖。

## 决定答案的 6 个参数（按 36 个月累计现金的敏感性排序）

1. `tariff_rate_moto` / `tariff_rate_ebike`（关税：25% / 37.5% / 100%）— 摆动 $1.48M
2. `retail_moto_units_scale`（FLASH / MK.II 零售销量倍数 0.5–1.6）— $0.53M
3. `fob_cost_moto`（FLASH / MK.II 出厂价 $1,800–2,300，无公开数据，必须由 HMP 提供）— $0.45M
4. `retail_ebike_units_scale` — $0.27M；`fob_cost_ebike` — $0.23M
5. `price_sale_tier_D_moto`（FLASH / MK.II 混合成交价 $4,350–4,750）— $0.21M
6. `rider_customers_scale`（骑手侧 SOM 倍数 0.65–2.0，来自 market_size.py）— $0.16M；`security_monthly_guard`（是否需要夜间保安 $0–4,500 / 月）— $0.16M

## 全部参数

| 参数 | base | lo | hi | 标签 | 来源 / 说明 |
|---|---|---|---|---|---|
| `retail_moto_units_scale` | 1.0 | 0.5 | 1.6 | ASSUMPTION | Commuter / enthusiast / car-replacement buyers across the LA metro, NOT bounded by the rider SOM. Anchor: SF ~40 units/month all-SKU with founder on site, walk- |
| `retail_ebike_units_scale` | 1.0 | 0.5 | 1.6 | ASSUMPTION | Students, commuters, non-courier buyers. Rider (courier) purchases are modelled separately from the SOM path. |
| `rider_customers_scale` | 1.0 | 0.65 | 2.0 | ESTIMATE | SOM from la-hub/model/market_size.py (research/03-market-size.md): month 12 = 40 (credible 30-65), month 24 = 72 bottom-up / 105 SF-anchored (credible 50-150).  |
| `rider_churn_monthly` | 0.04 | 0.06 | 0.03 | ASSUMPTION | Drives gross adds (CAC) and replacement sales. No SF figure yet. |
| `rider_share_rental` | 0.35 | 0.45 | 0.3 | ASSUMPTION | SF: ~100 rentals of ~400 recurring-paying customers = 0.25; LA early years more rental-heavy (cash-constrained, no trust). lo = more renters = more fleet capita |
| `rider_share_battery_sub` | 0.4 | 0.25 | 0.55 | ASSUMPTION | SF: 300+ of ~400 recurring = 0.75, but assumption register A01/E1: attach falls to 5-15% beyond ~1.5 mi; Ceres is 3-6 mi from Koreatown/Westlake/USC. Remainder  |
| `rider_buyer_moto_share` | 0.15 | 0.1 | 0.25 | ASSUMPTION | Couriers mostly buy Class 2 / moped tier (no M1 needed; SF fleet is INNO-based per Gazetteer 2026-04). M1 holders are a minority of LA couriers (register A11). |
| `rental_to_purchase_conversion_la` | 0.03 | 0.02 | 0.05 | ASSUMPTION | SF rent-to-own funnel (~$380/mo Inno package per Gazetteer). LA assumed slower (register A16). |
| `existing_la_installed_base` | 60 | 20 | 150 | ASSUMPTION | Feeds service revenue from month 1. |
| `dealers_active_scale` | 1.0 | 0.4 | 1.6 | ASSUMPTION | No dealers exist yet. Wholesale revenue booked through the LA store at dealer price; intercompany treatment with Davis HQ is ASK HMP. |
| `dealer_units_per_dealer_month` | 2 | 1 | 3 | ASSUMPTION | Small powersports dealers typically move a few units of a new brand per month. |
| `dealer_moto_share` | 0.5 | 0.5 | 0.5 | ASSUMPTION |  |
| `dealer_discount_b2b` | 0.2 | 0.25 | 0.15 | ASSUMPTION | Powersports dealer margins commonly 10-25% of MSRP. HMP wholesale price = ASP x (1 - discount). |
| `regional_van_start_month` | 6 | 6 | 6 | ASSUMPTION | Van bought when the first dealer signs. |
| `van_capex_onetime` | 30000 | 40000 | 20000 | ESTIMATE | Used cargo van + racking/tie-downs + wrap. hi = older van or lease. |
| `van_running_monthly` | 700 | 900 | 550 | ESTIMATE | Fuel, commercial auto insurance, maintenance, parking for ~1,000 mi/month of regional service runs. |
| `price_sale_tier_D_moto` | 4600 | 4350 | 4750 | ESTIMATE | FACT list prices (founder brief / hmpbikes.com): FLASH $4,799 single / $5,799 dual, +$200 charger; MK.II $3,999. Blend assumes ~60% FLASH (70% single, 50% charg |
| `price_sale_tier_A_ebike` | 2500 | 2300 | 2700 | ESTIMATE | FACT list: INNO-A Pro $2,599, LIVA 7 $1,599, Lightning 3000 $2,999 / 3000 Plus $3,599, Delivery Combo $2,499 (hmpbikes.com 2026-09). |
| `fob_cost_moto` | 2000 | 2300 | 1800 | ASSUMPTION | No public data. Assumed ~43% of blended ASP before duty/freight (3.3 kWh single / 6.6 kWh dual packs are the main cost; MK.II lighter). Implies ~32% gross margi |
| `fob_cost_ebike` | 1000 | 1150 | 900 | ASSUMPTION | Assumed ~40% of blended ASP; INNO-A Pro / LIVA 7 48V packs, Lightning 3000 30-45Ah. |
| `freight_per_unit_moto` | 220 | 300 | 170 | ESTIMATE | Crated motorcycle ~1.2 CBM; LA/LB port is the destination so no inland leg. |
| `freight_per_unit_ebike` | 100 | 140 | 80 | ESTIMATE |  |
| `tariff_rate_moto` | 0.375 | 0.375 | 0.25 | ESTIMATE | FACT: MFN Free; Section 301 List 2 (9903.88.02) +25% (CBP ruling NY N344662, 2024-12-20). FACT: IEEPA fentanyl/reciprocal layers struck down by SCOTUS 2026-02-2 |
| `tariff_rate_ebike` | 0.375 | 0.375 | 0.125 | ESTIMATE | Same stack as moto. hi = 12.5% if the Section 301 e-bike exclusion (extended to 2026-11-10 per search summary, unverified for this subheading) applies. |
| `warranty_reserve_rate` | 0.03 | 0.05 | 0.02 | ESTIMATE | MK.II page: 1 yr / 10,000 mi warranty; site banner claims 3-year. Ask HMP for SF claim rate. |
| `parts_accessory_attach_per_sale` | 120 | 80 | 180 | ASSUMPTION | Locks ($49.95), racks, bags, phone mounts, second battery ($599) on some sales. |
| `parts_gross_margin` | 0.45 | 0.4 | 0.5 | ASSUMPTION |  |
| `sales_commission_per_unit` | 50 | 75 | 50 | ASSUMPTION | Sales incentive on top of hourly pay. |
| `affirm_share_of_retail` | 0.45 | 0.55 | 0.35 | ASSUMPTION | $4-5k tickets to cash-constrained buyers; hmpbikes.com advertises financing. |
| `affirm_mdr` | 0.055 | 0.065 | 0.045 | ESTIMATE | Affirm merchant fees are individually negotiated; typical 2-8%, commonly ~5-6% incl. 0% APR promos (Affirm business hub; chargeflow.io 2026). |
| `card_fee_rate` | 0.029 | 0.031 | 0.027 | ESTIMATE | Shopify Payments / Stripe standard 2.9% + $0.30. |
| `card_fee_per_txn` | 0.3 | 0.3 | 0.3 | ESTIMATE | Rentals billed weekly (4.33 txn/month), subscriptions monthly, sales once. |
| `rental_weekly_tier_A` | 60 | 50 | 80 | ASSUMPTION | Founder range $50-80. Ceiling: Whizz LA $139-169/mo all-in (~$35-40/wk), Zoomo from $39/wk (register A02). SF rate card is an image on 415ebike.com/pages/rental |
| `rental_weekly_tier_C` | 105 | 90 | 130 | ASSUMPTION | Founder range $90-130. No LA comparable. |
| `rental_fleet_moped_share` | 0.2 | 0.1 | 0.3 | ASSUMPTION | CVC 14608 / M1 check limits the licensed-tier renter pool (register A11/A13). |
| `rental_realized_price_factor` | 0.9 | 0.8 | 0.95 | ASSUMPTION | Monthly-billing discount, free first week, promos. SF realized price net of discounts is ASK HMP. |
| `rental_utilization_target` | 0.75 | 0.65 | 0.85 | ASSUMPTION | Register A16: realistic 60-75% vs 85-90% assumed; units in repair, reconditioning, impound, idle. |
| `initial_rental_fleet_size` | 15 | 25 | 10 | ASSUMPTION | lo = larger idle fleet is worse; fleet then grows with demand / utilization target. |
| `rental_moped_cost_multiplier` | 1.3 | 1.3 | 1.3 | ASSUMPTION | Lightning 3000 ($2,999-3,599 list) vs INNO ($2,599). |
| `vehicle_life_months_rental` | 36 | 24 | 48 | ASSUMPTION | Register A18: 36-month straight line to 20-30% residual is itself an assumption for 10 hr/day delivery use. |
| `vehicle_residual_ratio` | 0.25 | 0.15 | 0.35 | ASSUMPTION |  |
| `maintenance_per_rental_vehicle_month` | 30 | 45 | 20 | ASSUMPTION | Tyres, brakes, crash repair; in-house labor is in staff cost. |
| `gps_per_vehicle` | 12 | 15 | 9 | ESTIMATE | Fleet GPS $8.95-45/vehicle/month (Spytec/One Step GPS 2026); Monimoto ~$3.50/mo; hardware amortized. |
| `insurance_rental_fleet_per_ebike_month` | 10 | 15 | 6 | ESTIMATE | Small rental fleets: $1,200-3,100/yr for 15-25 bikes (lendcontrol.com 2026) = $5-11/bike/month; delivery use and LA likely higher. |
| `tier_insurance_per_vehicle_month` | 75 | 150 | 40 | ESTIMATE | Register A15: specialty programs $60-200/vehicle/month or declined for delivery use (Revel exit). CA minimum 30/60/15 since 2025. |
| `theft_loss_rate_rental_fleet_annual` | 0.08 | 0.15 | 0.04 | ASSUMPTION | Register A15: double-digit annual loss reported by delivery-rental operators in high-theft US cities; Whizz claims <1% (marketing); LA motorized-device thefts + |
| `bad_debt_rate_rental_revenue` | 0.05 | 0.08 | 0.03 | ASSUMPTION | No-credit-check weekly renters: chargebacks, unpaid final weeks. |
| `battery_sub_monthly_price` | 80 | 60 | 100 | ASSUMPTION | Founder range $60-100. The public $150 / $500 / $25-per-month figures on 415ebike.com are theft-retrieval / loss / optional-insurance terms, not the subscriptio |
| `batteries_per_subscriber` | 1.5 | 2.0 | 1.2 | ASSUMPTION | Register A17 cites ~1.5 in SF. |
| `battery_cost` | 400 | 500 | 320 | ESTIMATE | Retail 48V 24Ah = $599 (hmpbikes.com); moped 74V 45Ah (3.3 kWh) retail unknown. Assumes ~50% of retail landed incl. tariff. |
| `battery_life_months_delivery_use` | 24 | 18 | 36 | ASSUMPTION | Register A17: consumer-guide lifetimes overstate delivery-cycle life (12-16 swaps/month). |
| `swaps_per_subscriber_month` | 12 | 16 | 8 | ASSUMPTION |  |
| `kwh_per_swap` | 1.5 | 1.8 | 1.2 | ESTIMATE | 48V 24Ah = 1.15 kWh; 74V 45Ah = 3.3 kWh; blended toward e-bike packs. |
| `electricity_per_kwh` | 0.24 | 0.28 | 0.2 | ESTIMATE |  |
| `rental_fleet_kwh_per_unit_month` | 30 | 35 | 25 | ESTIMATE | Renters mostly home-charge; store tops up returns and swaps. |
| `swap_station_capex_onetime` | 12000 | 25000 | 6000 | ESTIMATE |  |
| `repair_revenue_per_active_customer_month` | 12 | 8 | 18 | ASSUMPTION | Installed base = existing LA vehicles + vehicles sold by the store (retail + rider); rentals get free service. Warranty work is in warranty_reserve_rate. |
| `repair_gross_margin` | 0.55 | 0.45 | 0.65 | ASSUMPTION |  |
| `service_walkin_monthly_scale` | 1.0 | 0.4 | 1.8 | ASSUMPTION | Couriers on other brands; DTLA has few e-moped repair shops. |
| `wage_manager_hourly` | 30 | 34 | 27 | ESTIMATE | ~$62k/yr base; works the floor and sells. |
| `wage_technician_hourly` | 28 | 32 | 25 | ESTIMATE | LA motorcycle / e-bike technician; verify against BLS OES 49-3052 LA MSA. |
| `wage_frontdesk_hourly` | 21 | 23 | 19 | ESTIMATE | FACT floor: City of LA minimum wage $18.42/hr from 2026-07-01 (wagesla.lacity.gov memo 2026-01-30). |
| `payroll_load` | 1.28 | 1.35 | 1.22 | ESTIMATE | FICA 7.65%, CA UI/ETT/SDI ~3%, workers comp (mechanic class ~6-10%), small benefits stipend. |
| `hours_per_fte_month` | 173 | 173 | 173 | FACT | 2,080 / 12. |
| `fte_manager` | 1 | 1 | 1 | ASSUMPTION |  |
| `fte_sales_ops` | 1 | 1 | 1 | ASSUMPTION | 7-day cover needs the manager on the floor; a second front-desk FTE would add ~$4.6k/month. |
| `fte_mechanic_m1_12` | 1 | 1 | 1 | ASSUMPTION |  |
| `fte_mechanic_m13_36` | 1.5 | 1.5 | 1.5 | ASSUMPTION | Total 3.0 -> 3.5 FTE; founder brief allows 2-4. |
| `rent_escalation_annual` | 0.03 | 0.04 | 0.03 | ESTIMATE | LA industrial rents fell 32% over 36 months (CBRE Q2 2026); 3% fixed bumps are standard in LOIs. |
| `rent_nnn_psf_month` | 0.15 | 0.3 | 0.0 | ESTIMATE | hi = Full Service as two Ceres listing mirrors state; lo = full NNN pass-through $0.20-0.40/sf (register A19). |
| `security_deposit_months` | 2 | 3 | 1 | ESTIMATE |  |
| `utilities_monthly` | 900 | 1300 | 700 | ESTIMATE |  |
| `insurance_gl_property_monthly` | 1800 | 3000 | 1200 | ESTIMATE | No public premium found; small powersports dealer packages typically $15-35k/yr; lithium inventory at a Skid-Row-adjacent address may add protective conditions  |
| `security_monthly` | 500 | 800 | 350 | ESTIMATE | Remote video monitoring $50-150/camera/month; alarm monitoring from ~$10-30 (Guardian Integrated 2026). |
| `security_monthly_guard` | 0 | 4500 | 0 | ESTIMATE | Unarmed guard $25-40/hr in LA (GNS Guard 2026); 4 hrs x 30 days x $35 = $4,200. Base assumes cameras + gate suffice. |
| `marketing_monthly` | 2000 | 3000 | 1500 | ASSUMPTION |  |
| `cac_per_rider` | 200 | 350 | 100 | ASSUMPTION | Register A03: LA first-6-month CAC $150-400 vs SF ~$0-50 organic. |
| `launch_marketing_onetime` | 8000 | 12000 | 5000 | ASSUMPTION |  |
| `software_gna_monthly` | 1200 | 1500 | 1000 | ESTIMATE |  |
| `permits_taxes_monthly` | 250 | 350 | 200 | ESTIMATE | CA dealer renewal $125 + plates $94 each + bond; LA gross-receipts tax. |
| `inventory_days` | 45 | 60 | 30 | ASSUMPTION |  |
| `min_floor_units_moto` | 6 | 6 | 6 | ASSUMPTION | Demo + display FLASH/MK.II. |
| `min_floor_units_ebike` | 10 | 10 | 10 | ASSUMPTION |  |
| `inventory_carrying_rate_annual` | 0.12 | 0.15 | 0.1 | ASSUMPTION |  |
| `tenant_improvements_onetime` | 15000 | 30000 | 8000 | ESTIMATE |  |
| `security_onetime` | 12000 | 20000 | 8000 | ESTIMATE |  |
| `fire_code_compliance_onetime` | 35000 | 90000 | 15000 | ESTIMATE | Register A21: $40-150k if aspirating detection / dedicated circuits / sprinkler work required; hi = simple circuits only. Ceres has 400A 3-phase and sprinklers  |
| `dmv_dealer_license_onetime` | 3000 | 5000 | 2000 | ESTIMATE | Motorcycle dealer bond $10,000 (premium ~$100-500/yr), application ~$175, New Motor Vehicle Board fee $425/location, pre-licensing course, plates $94 each, sign |
| `fixtures_signage_onetime` | 8000 | 12000 | 5000 | ESTIMATE |  |
| `buildout_amortization_months` | 36 | 36 | 36 | ASSUMPTION |  |
| `lease_term_months` | 36 | 36 | 36 | ASSUMPTION | Model horizon = 36 months; lease exposure beyond that is not modelled. |
