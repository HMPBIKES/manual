# Shopify 订单地理分布：FLASH / Lightning MK.II（2026-09-08 从 www.hmpbikes.com 后台拉取）

方法：Shopify Admin GraphQL `orders(query:"FLASH created_at:>=2026-01-01")` 和 `"Lightning created_at:>=2026-01-01"`，逐单读取收货 / 账单地址、来源（web / pos / draft）、状态和行项目。POS 订单没有地址，默认为 SF 店（261 6th St）到店成交。

## FLASH 整车（2026-07-11 首单至 2026-09-08）

| 订单 | 日期 | 渠道 | 收货 / 账单地 | 州 | 配置 | 金额 | 状态 |
|---|---|---|---|---|---|---|---|
| #12820 | 07-11 | web | Virginia Beach 23454 | VA | 黑 双电池 | $5,999 | 已付已发 |
| #12829 | 07-12 | web | Las Vegas 89179 | NV | 灰 双电池 | $6,499 | 已付已发 |
| #12876 | 07-15 | web | Renton 98058 | WA | 黑 双电池 | $6,499 | 已付已发 |
| #12914 | 07-17 | POS | SF 店（24 个月分期） | CA | 黑 | $7,227 | 已付 |
| #12921 | 07-18 | web | Augusta 30904 | GA | 黑 双电池 + 车载充电 | $6,659 | 已付已发 |
| #12939 | 07-19 | web | Riverside 64150 | MO | 灰 双电池 × 2 | $12,098 | **作废** |
| #12959 | 07-21 | web | Tigard 97224 | OR | 黑 双电池 | $6,299 | 已付已发 |
| #12961 | 07-21 | POS | SF 店 | CA | 灰 | $6,408 | 已付 |
| #13067 | 07-28 | web | Galveston 77550 | TX | 灰 双电池 | $6,398 | 已付已发 |
| #13101 | 07-30 | web | Grand Junction 81507 | CO | 灰 双电池 | $6,498 | 已付已发 |
| #13111 | 07-31 | web | **San Diego 92154** | CA | 灰 双电池 | $6,541 | 已付已发 |
| #13125 | 08-01 | web | 账单 Stillwater OK，SF 店自提 | OK / CA | 灰 双电池 | $6,407 | 已付 |
| #13138 | 08-01 | web | Anderson 96007（Shasta County，北加） | CA | 灰 双电池 | $6,648 | 已付已发 |
| #13185 | 08-05 | web | Ramona 92065（San Diego County） | CA | 灰 双电池 | $6,541 | **作废** |
| #13204 | 08-06 | web | Kailua Kona 96740 | HI | 黑 双电池 | $6,399 | 已付已发 |
| #13210 | 08-06 | POS | SF 店（24 个月分期） | CA | 黑 | $7,307 | 已付 |
| #13290 | 08-10 | web | Portland 97203 | OR | 黑 双电池 | $6,299 | 已付已发 |
| #13306 | 08-11 | web | Gainesville 32608 | FL | 黑 单电池 | $5,399 | 已付已发 |

**已完成 16 台**（web 13 + SF POS 3），作废 2 单（MO 2 台、Ramona CA 1 台）。8 月 11 日之后没有新的整车订单，只有预订定金。

按地区：

| 地区 | 台数 | 说明 |
|---|---|---|
| 外州 | 10 | VA、NV、WA、GA、OR × 2、TX、CO、HI、FL |
| 北加（SF 店成交 + 自提 + Shasta） | 5 | 3 单 POS、1 单 SF 自提（账单 OK）、1 单 Anderson |
| **南加** | **1** | San Diego 92154（另一单 Ramona 作废） |
| **LA County** | **0** | |

成交均价（13 单 web）约 $6,300；15 台为双电池，1 台单电池。

## FLASH 预订定金（$200，可退，8 月起）

有效（已付或已授权）：Daly City CA、Mountain View CA、Hayward CA、**Los Angeles 90066（Mar Vista）**、Iowa City IA、Quinn SD、Brecksville OH、Manor TX、Nashville TN、North Aurora IL、Tulsa OK、Round Rock TX、Queens Village NY（$100）、Colorado Springs CO、Edwards CO（草稿单）。作废 / 退款：Brighton MI、Evans GA、Phoenix AZ、**Santa Clarita CA**。

有效定金 15 个：湾区 3、**LA 1**、外州 11。

## Lightning MK.II 整车（2026-06 起）

| 订单 | 日期 | 收货地 | 州 | 金额 |
|---|---|---|---|---|
| #12461 | 06-19 | Methuen | MA | $4,126 |
| #12806 | 07-10 | Serena | IL | $3,499 |
| #13142 | 08-02 | **Vista 92083（账单 Escondido，San Diego County）** | CA | $4,659 |
| #13156 | 08-03 | Chicago | IL | $4,628 |
| #13589 | 08-29 | Mayfield | KY | $4,499 |
| #13649 | 09-01 | Aventura | FL | $4,628 |

6 台：外州 5、南加 1（SD County）、LA 0。Lightning 3000 Plus 2026 年 6 台：TX × 2、FL、MI、NH、SF POS 1。

## 对 LA 判断的含义

1. **Shopify 里没有任何一台 FLASH 或 MK.II 卖到 LA County**；南加合计 2 台（都在 San Diego County），另有 LA 一个 $200 定金（Mar Vista）和一个作废的 Santa Clarita 定金。创始人记忆中的"3 台 SD、2 台 LA"与后台不符，除非有 Shopify 之外的成交。
2. FLASH 的买家是全国性的：16 台里 10 台外州，8 个州；这是 DTC 在起作用，与"要靠门店才能卖"相反。
3. 北加 5 台 vs 南加 1 台：有店的地方确实卖得多（SF 店 3 单 POS 都是 24 个月分期的到店成交），这是"实体存在有用"的证据，但它说明的是"店在哪里，车就在哪里成交"，而不是"南加已经比北加多"。
4. 8 月 11 日之后 FLASH 整车零订单、只有定金，说明库存或交付节奏（等下一柜）在限制销量；LA 仓库作为收货点缩短的正是这一段。
5. 按目前节奏（约 8 周 16 台 ≈ 8 台 / 月全国），LA 店 Base 情景要求的第 24 个月 11–14 台 / 月是全国现有销量的 1.5 倍，需要靠南加增量而不是既有需求转移。
