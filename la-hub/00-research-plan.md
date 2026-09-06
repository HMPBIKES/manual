# HMP LA Delivery Rider Hub — 研究方案（第一步：A–E）

状态：v0.1 草稿，2026-09-06。本文件只回答"怎么研究"，不给结论。

标签约定（贯穿后续所有文件）：

| 标签 | 含义 |
|---|---|
| FACT | 已确认事实（HMP 提供，或有可核对的公开来源） |
| FACT_PENDING | 公开数据可得，但还没去取 |
| ESTIMATE | 由多个来源推算，给范围 |
| ASSUMPTION | 没有直接证据，模型参数，必须做敏感性分析 |
| ASK_HMP | 只有 HMP 内部数据能回答，等你提供 |
| DERIVED | 由其他变量算出 |

---

## A. 研究方法

### A0. 先定"什么会让我们不做"

在收集任何证据前先写下 kill criteria，避免研究过程被"已经倾向于开店"的偏好带偏。初版（待 Task 3 校准数字）：

1. DTLA + Koreatown 每日活跃两轮/可转两轮骑手 SOM 在 Base 情景下撑不起 break-even 所需的租赁台数 + 电池订阅数。
2. 场地 total cost of location（租金 + 安保 + 盗损 + 保险）比替代区域高出的部分，不能被"仓库面积 + 靠近 DTLA"带来的收益覆盖。
3. 目标车型在加州/LA 的法规、平台政策或保险上有硬性障碍（例如 40–50 mph 车型租给无 M1 证的骑手）。
4. SF 的增长主要靠多年积累的社区/转介绍，而这个网络在 LA 第一年不存在，导致 ramp 慢到租约先把现金烧掉。
5. （本轮新增）四个"一票否决"的合规项任一不过：LAFD 不批锂电池集中充电；房东或保险公司不接受该用途；换电电池 / 充电器没有 SB 1271 要求的 UL 认证；没有保险公司愿意承保"出租给外卖骑手的已注册 moped / 摩托车"。这四项都可以在签约前用几个电话和邮件验证。

每条 kill criterion 后续都对应一个可量化的 trigger（见 D 部分和 CSV 的 D01–D07）。

### A1. Task 1 市场容量：四种独立方法取交集

不用单一方法。每种方法各自给 Conservative / Base / Aggressive，最后看交集，而不是取平均。

| 方法 | 逻辑 | 主要数据 | 主要弱点 |
|---|---|---|---|
| ① 餐厅密度法 | 区域餐厅数 × 每百家餐厅对应的活跃骑手数（用 NYC / SF 有实测的城市校准） | LA County DPH 餐厅点位数据（有经纬度，可按 768 Ceres 半径算）；NYC DCWP 骑手研究 | 校准城市的餐厅/骑手比未必适用于 LA（车多） |
| ② 人口 benchmark 法 | 只作交叉验证。用 NYC / Seattle / SF 每千人骑手数做上下限 | ACS、各城市骑手研究 | 就是你指出的"人口 × 比例"陷阱，所以只当边界 |
| ③ 订单量法 | 区域日订单量 ÷ 每骑手日单量 | 平台披露、第三方（Second Measure 等）、Reddit 骑手报的单量 | 区域订单量没有官方口径，只能用代理 |
| ④ 实地计数法 | 在 Koreatown / DTLA 热点餐厅门口做晚高峰 1 小时取车计数，分车型 | 你或 SF 员工去 LA 数 2–3 个晚上 | 样本小，但是唯一直接测"车型占比"的方法 |

车型占比（car / motorcycle-scooter / e-bike / bicycle）只靠方法④ + Reddit/YouTube 证据 + 平台政策（Uber Eats scooter mode 限制等），不靠全国平均。

**本轮批评指出的两个方法论漏洞，已采纳：**

1. 方法①和方法③不是独立的。LA 订单量没有公开数据，只能从"餐厅数 × 每餐厅订单"反推，所以①和③共用输入，是同一个估计穿了两件衣服。真正独立的只有方法④。因此：④ 升级为主方法，①/③ 合并为一个方法，② 只作边界。
2. 所有方法先在 SF 核心区跑一遍，看能否在 ±30% 内还原 SF 已知数字（1,000+ 已售、100 在租、300+ 电池订阅，加上非 HMP 骑手），还原不了就不能用在 LA。方法④的计数协议要在计数前预先登记参数范围（防止事后调参让三个方法"收敛"），周二/周四/周六三个时段（午餐、18–20 点、21–23 点），餐厅门口和汽车停靠点都数，两晚做 capture-recapture 去重。

另外要区分"注册过 / 年内活跃过"和"每日活跃全职"：DoorDash 全国 Dasher 平均每周只做约 4 小时，Seattle 18 个月 92,801 名"覆盖工人"对应每周只有约 20 万个 offer，全职当量可能只有 2–5 千人。HMP 的客户几乎都是全职，所以分母必须是每日活跃全职骑手，任何 headline 数字都要除以 3–20 倍。

TAM / SAM / SOM 定义写死，避免悄悄膨胀：

- TAM = 目标区域每日活跃配送员（去重后）
- SAM = 其中已骑两轮 + 可被说服换两轮的开车骑手 × 愿意到 768 Ceres 的比例
- SOM = SAM × 12 个月内可达的渗透率（用 SF 渗透率做上限）

### A2. Task 2 SF benchmark：核心区对核心区

1. 用 SF 三个 FACT（>1,000 已售、300+ 电池订阅、~100 整车在租）反推 SF active customer 数。反推要问你几个内部数据（见 D），拿不到就用范围。
2. SF 侧同样跑方法①–③，得到 SoMa + Mission + Tenderloin + FiDi/South Beach 的骑手数。
3. LA/SF ratio 只在"核心区对核心区"层面算，并且要拿到 SF 客户地址分布来验证"SF 客户真的主要来自核心区"这个前提，否则比较框架本身就错了。
4. Ramp curve 用 SF 逐年（最好逐月）销量和租赁数，而不是假设线性。M3 / M6 / M12 / M24 三情景都从 SF 实际 ramp 的倍数推。

### A3. Task 3 Unit economics：可调参数的 Python 模型

- 参数全部放在 `la-hub/model/assumptions_template.csv`，模型只读 CSV，不在代码里写死数字。
- 输出：gross margin by line、contribution margin、monthly burn、break-even 的三种表达（需要多少在租车 / 多少电池订阅 / 多少月销量），working capital 曲线。
- 敏感性：tornado 图（每个 ASSUMPTION 单独 ±30%），再加 2–3 个组合坏情景（盗损 × 低利用率 × 慢 ramp）。
- 销售对 break-even 的影响单独建：卖车会削弱整车租赁收入，但增加电池订阅和维修，这是 HMP 模式的核心，要显式建模。

### A4. Task 4 车型组合：由法规矩阵 × 收入 × 盗损 × 维护 决定

先做法规矩阵（每档车型在加州是什么法律类别、要不要 M1/M2、注册、保险、平台是否允许），矩阵里有硬障碍的档位直接降权，然后再谈骑手收入和租金天花板。比例最后由评分决定，不预设。

本轮探测已经把法规矩阵的骨架查清楚了，结论对 Task 4 的前提有实质影响：

| 档位 | 加州法律类别 | 驾照 | 注册/牌照 | 保险 | Uber Eats LA | DoorDash |
|---|---|---|---|---|---|---|
| A 20–25 mph（≤750W，油门 ≤20 mph 或 Class 3 助力 ≤28 mph） | e-bike | 不需要 | 不需要 | 不需要 | bicycle 模式（18 岁+，仅需 ID） | bike 模式 |
| B 28–35 mph 油门 | **不是 e-bike**。moped（CVC 406，<4 bhp，≤30 mph 待核实）或 motor-driven cycle（CVC 405） | M1 或 M2 | 需要（moped $23 一次性） | moped 不强制，405 强制 | scooter 模式要求 <50cc、21 岁、驾照；电动车如何归类未知 | scooter 模式，按市场开放 |
| C 40–50 mph | motor-driven cycle 或 motorcycle | M1 | 需要 | 强制，2025 起 30/60/15 | **无摩托车模式** | Motorcycle dash type，LA 是否开放未确认 |
| D 50–70+ mph（FLASH、MK.II 是 DOT 注册摩托车） | motorcycle | M1 | 需要 | 强制 | 无 | 同上 |

也就是说法律断崖在 A 和 B 之间，不在 B 和 C 之间。B 档拿的是摩托车级合规成本、e-bike 级租金。另外两条与租赁直接相关：CVC 14608 禁止把机动车租给没有对应驾照的人（出租方承担 negligent entrustment 责任，联邦 Graves Amendment 不保护），SB 1271 要求销售和出租的 e-bike / 电池 / 充电器有 UL 2849 / EN 15194 认证。所以 Task 4 的第一步不是算收入，而是：(1) 用 LA 地址实测两个平台各开放哪些车辆模式；(2) 确认 HMP 每个 SKU 的法律类别、能否在加州上牌、有没有 UL 认证；(3) 骑手收入按"平台申报模式"而不是"车速"来测（无照骑手只能用 bike 模式，拿到的是 e-bike 半径的单）。

### A5. Task 5 竞争：逐家表格

Whizz（SF/LA）、Zoomo、Wombi 以及 LA 本地租赁、Facebook Marketplace 非正规租赁。每家的价格/押金/车型/续航/维修/换车/rent-to-own/平台合作/门店/评论。规模数字一律标 `estimate`，除非有公司披露或第三方报道。

### A6. Task 6 场地：total cost of location

768 Ceres 打 0–10 分，并和 Koreatown / Westlake / Fashion District / South Park / Arts District / Historic South Central 比：

租金 + 安保成本 + 盗损预期 + 保险 + 获客优势（离骑手近不近） + 骑手便利 + 车队运营效率。用 LAPD 公开犯罪数据按半径算事件数，不用"感觉治安差"。

本轮补充三点：

1. 治安拆成两个独立风险分别量化：骑手/员工人身安全（影响晚间营业和口碑）用 NIBRS 半径查询 + 夜访 + 骑手问卷；仓库盗窃（电池 40 磅、$500–1,000 转手、无登记、不带 GPS，是最好偷的库存）用 NIBRS 商业盗窃 + 邻居访谈 + 保险人要求的防护条件。两个查询都对 SF 店 261 6th St 做一遍（SFPD 数据），把"Skid Row 边缘"换算成"是 SoMa 的几倍"。
2. 多加一个对照方案：两节点模型（Koreatown / Westlake 800–1,500 SF 换电点 $2.5–5k/月 + Vernon / Boyle Heights 3,000–4,000 SF 仓库 $3.5–5.5k/月）。总租金和 Ceres 差不多，但换电点在骑手所在地、消防重活在便宜空间、可以月租/转租拼出来而不是签 3–5 年。
3. 消防合规单独算：2025 加州消防法典 Sec. 320 超过 15 立方英尺散装锂电池即需运营许可（约 20 块 MK.II 电池就到），Sec. 322 要求只能给有 UL 认证的设备用认证充电器充电、每块可拆电池间隔 18 英寸、每个充电器独立回路、吸气式或辐射能火灾探测。这可能是 $40k–150k 的一次性投入加 3–9 个月许可周期，或者干脆不批。

### A7. 证据分级与交叉验证

- 每个关键数字至少两个独立来源，否则标 ESTIMATE 并给范围。
- 平台自述（DoorDash 新闻稿）、竞争对手自述（Whizz 融资稿里的 fleet size）一律标 company-claimed。
- Reddit / YouTube 只用来找"方向"和"量级"，不当统计。

### A8. 节奏

| 轮次 | 交付 |
|---|---|
| 本轮 | A–E 方案 + 变量模板 |
| 第 2 轮 | 你补 ASK_HMP 数据 → Task 1 + Task 2 数字 + 模型 v1 |
| 第 3 轮 | Task 3 敏感性 + Task 4 车型 + Task 5 竞争 |
| 第 4 轮 | Task 6 场地 + GO / CONDITIONAL GO / NO-GO + triggers |

---

## B. 需要建立的变量

完整清单在 `la-hub/model/assumptions_template.csv`（约 130 个变量，含 status 标签、SF 值、LA 三情景、来源列）。分七个 block：

| Block | 前缀 | 内容 | 数量 |
|---|---|---|---|
| market | M | 人口、餐厅数、骑手数三种方法、车型占比、可达比例、TAM/SAM/SOM | 21 |
| sf_benchmark | S | SF 三个 FACT、运营年数、逐年销量、活跃客户、客户地理分布、租转买、ramp 曲线 | 18 |
| revenue | R | 四档车型售价/COGS/周租/月租、押金、电池订阅、换电、维修、配件、利用率 | 24 |
| cost | C | 租金、NNN、装修、安保、GPS、水电、人力、保险、盗损、坏账、刷卡费、车辆/电池折旧、CAC、许可、库存、初始车队 | 32 |
| fleet | F | 四档车型占比、执照/注册/保险/平台允许、盗损与维护系数、租金天花板、骑手收入提升 | 12 |
| competitor | K | Whizz / Zoomo 价格、押金、LA 车队估计 | 4 |
| site | L | 到 Koreatown / DTLA 餐厅重心距离、半径犯罪数、替代区域租金、试点所需面积 | 9 |
| decision | D | M3 / M6 / M12 触发阈值 | 7 |

模型结构（后续 `la-hub/model/model.py`）：

```
CSV assumptions
   → market sizing (3 methods × 3 scenarios)
   → SF benchmark ratio → LA ramp (M3/M6/M12/M24)
   → revenue lines × cost lines → P&L by month
   → break-even (rental vehicles / battery subs / sales)
   → sensitivity (tornado + combined bad cases)
   → trigger thresholds
```

---

## C. 公开可得的数据

本轮跑了 12 个数据可得性探测（每个只做约 10–15 次检索，确认来源存在、粒度、可靠性和获取方式，不做推算）。完整清单含 URL 和原文数据点见 `la-hub/research/01-public-data-sources.md`，原始 JSON 在 `la-hub/research/raw/scouts/`。

### C.1 按 Task 看公开数据够不够

| Task | 充分性 | 公开能拿到什么 | 拿不到什么 | 替代方案 |
|---|---|---|---|---|
| 1 市场容量 | **不足** | LA County DPH 餐厅点位数据（含经纬度，季度更新，2026-07 版）；LA 市 Active Businesses（NAICS + 经纬度，2026-06）；ACS tract 人口/车辆拥有；DoorDash 各城市两轮配送占比（SF 72%、San Diego 30%，LA 未公布）；NYC 6 万周活跃骑手、Seattle 18 个月 92,801 人；DoorDash 称 "greater LA 是订单量第一大都会区"（无数字）；Prop 22 研究：加州外卖员税后 $5.93/小时（不含小费） | LA 骑手总数（LA 没有 NYC/Seattle 那种最低工资条例产生的平台申报数据）；LA 两轮占比；街区级订单量；car / 摩托 / e-bike / 自行车 分布；Reddit 对当前工具域名级封锁 | 三个真正独立的方法：餐厅比率法（用 SF 已知客户数校准）、NYC/Seattle 比率 × LA 两轮占比（需拿到 DoorDash 2026 报告 PDF 或问 DoorDash LA 团队）、实地计数（先在 SF 跑同一套方法校准） |
| 2 SF 基准 | **部分** | SF 侧分母齐全：Registered Business Locations（g8m3-pdis，含 NAICS 和 Analysis Neighborhood，2026-09-06 更新）、SF DPH 餐厅数据（tvy3-wexg，含经纬度和街区）、ACS；415 Ebikes 工商登记 2024-08-09；Gazetteer 2026-04 报道 "600+ e-moped，目标年底 1,000" | 分子全部是内部数据：逐月销量、租赁起止、电池订阅、客户 ZIP、活跃比例、车型构成、SF 店 vs Davis vs 线上口径 | Shopify / Stripe 直接导出 |
| 3 单位经济 | **部分** | HMP 公开售价（FLASH $4,999 促销 / $5,499；Lightning MK.II $3,999；Lightning 3000 $2,999 / $3,599；INNO-A Pro $2,599；LIVA 7 $1,599；48V 24Ah 电池 $599）；报道中 Inno 套餐 $2,500、rent-to-own 约 $380/月；租赁页盗损条款（$150 找回费、未找回 $500、$25/月保险）；竞品价格天花板（Whizz 全国 $179/月起、LA 索引 $139、押金 $99、保护计划 $19/月、盗损上限 $500、NY 换电 $49/月；Zoomo $39/周起、Uber Eats 专享 $20/周、$790 买断）；租金 $1.20–1.60/SF/月；Central LA 工业 $1.34/SF/月 NNN，LA 工业租金 36 个月跌 32%；保安 $25–40/小时；摄像头监控 $50–150/路/月；GPS $9–45/车/月；加州最低责任险 30/60/15 | 落地成本、利用率、维修成本、盗损率、坏账、押金政策、电池订阅价、保费、NNN、人力、装修、消防合规 capex、流失 | 全部靠 HMP 内部 + 经纪人条款 + 保险报价 + LAFD 预咨询 |
| 4 车型组合 | **部分（法规已清楚）** | 加州 e-bike 定义 ≤750W、油门 ≤20 mph、Class 3 助力 28 mph；moped（CVC 406）<4 bhp 需 M1/M2 + 牌照；motor-driven cycle / motorcycle 需 M1 + 注册 + 保险；SB 1271 销售/出租须 UL 2849 / EN 15194 认证（生效日期 2026 还是 2028 两个探测不一致，需读法条）；AB 875 可扣车；Uber Eats LA 页面：scooter <50cc、21 岁、需驾照，无摩托车模式；DoorDash 有 Motorcycle dash type 但按市场开放；CVC 14608 禁止把机动车租给无照者；2025 加州消防法典 Sec. 320/322 电池存储与充电规则 | LA 骑手车型分布；DoorDash Motorcycle 模式在 LA 是否开放；Uber 是否接受电动 moped 归入 50cc 类；骑手 M1 持证率；FLASH / MK.II 能否在加州上牌（VIN/MCO/FMVSS）；CVC 405/406 原文阈值 | 用 LA 地址实测平台注册；DMV 数据；NHTSA vPIC；HMP SF 客户按车型的平台注册模式 |
| 5 竞争 | **部分** | Whizz 全国条款很清楚（2024 年 2,500 台车、ARR >$8M，公司自述）；Zoomo 美国定价 | Whizz LA 状态（官网 31 家店无 LA，页面是空壳）；Zoomo LA 状态（官网 LA 页显示 NYC 内容）；没发现任何面向骑手的 e-moped / e-motorcycle 租赁商；本地小店和 Facebook Marketplace 非正规租赁未探测；P2P 只有摘要（Riders-Share 称 LA 50+ 台 scooter；FriendWithA moped $520/月） | Whizz app 用 Koreatown 地址 mystery shop；电话 Zoomo；韩语/西语社群和 Marketplace 手工抓取 |
| 6 场地 | **部分** | 挂牌信息（8,443 SF，2015 年建，400A 三相，APN 5146-003-059，两栋孪生楼 768/772 合计 16,887 SF）；ZIP 90021 常住人口 2,897；LAPD NIBRS 犯罪数据集（2020–2024 旧集已冻结，2024-10 起新集双周更新）；Crosstown 电动设备盗窃分析（USC 周边最高，DTLA 未列入）；Skid Row 无家可归者 2026 年 4,215（+23%）；Central Division 加重攻击 +25%；7th St 自行车道到 Main St 为止；Kidder Q2 2026 租金 | ZIMAS 分区与 CofO；净高、门、停车；是否仍在招租（一条 LoopNet 记录显示 "不再挂牌"）；租约类型；半径内事件数；6 个替代区域的租金/治安/骑手距离（只有 LoopNet 挂牌数：Fashion District 31、Arts District 13、Koreatown 10） | ZIMAS 查询；NIBRS 与 SFPD（261 6th St 周边）配对半径查询；经纪人提供替代区域 comps；实地夜访 |

### C.2 探测结果与你 brief 里的前提不一致的地方

这些必须在建模前对齐，否则模型的输入本身是错的：

| 主题 | brief 前提 | 公开证据 | 处理 |
|---|---|---|---|
| 租金 | ~$10,000/月 | PropertyShark $1.20/SF/月 "Full Service" ≈ $10,132（吻合）；LoopNet $19.20/SF/年 ≈ $13,509；768+772 合租 $1.40/SF/月 | 模型里用 $10.1k–$13.5k 区间，并加 NNN 敏感性；要经纪人书面条款 |
| 是否还在招租 | 在考虑 | 一条 LoopNet 记录显示 "no longer advertised"；一个聚合站把 768+772 打包出租 | 先确认 768 单独可租 |
| SF 已售数量 | >1,000 | Gazetteer 2026-04-02："SF 超过 600 台 e-moped，目标年底 1,000" | 你确认口径（SF 店 vs Davis vs 线上；所有车型 vs e-moped；4 月后是否新增 400 台） |
| SF 运营时长 | 未说明 | 415 Ebikes（Mandala Global, LLC）工商登记 2024-08-09，约 25 个月 | ramp 曲线按 25 个月起算，除非你提供更早的销售记录 |
| 公司结构 | HMP / 415 eBikes 一体 | HMP 总部 Davis（2022 年成立），415 eBikes 是 SoMa 的 "dealership / partner"，SF 无 HMP DBA | 你说明 SF 店是自营还是经销；这决定 "复制 SF" 复制的是什么成本结构 |
| Whizz LA | 已有 LA 业务 | 官网 31 家店只有 SF 一家在加州；2026-07 DoorDash 指南列出的城市无 LA；LA 页面是 app 空壳，$139 只在索引标题里 | 视为 "未确认，可能是需求测试页"；mystery shop |
| Zoomo LA | 已有 | 2025 博客和加州 GO-Biz 说有 LA；官网 LA URL 显示 NYC 内容，美国只剩一家纽约店 | 电话确认；如已退出，问原因本身就是数据 |
| SF 骑手车型 | 未说明 | 报道中 SF 骑手车队是 Class 2 的 INNO（20 mph，无需驾照）；FLASH / MK.II 是需 M1 的 DOT 摩托车 | Task 4 的前提要改：SF 验证的是 A 档，不是 C/D 档 |
| 换电站 | 300+ 电池订阅 | 报道：换电站 2026 年 6 月才上线，300+ 订阅主要是家充租赁 | 换电枢纽经济模型在 SF 也没有被验证 |
| 治安与盗窃 | Skid Row 边缘 = 盗窃重灾区 | LAPD 2020–2024 电动设备盗窃前列是 USC、Venice，DTLA 未列入；但 Skid Row 凶杀率是全市 17 倍、Central Division 加重攻击 +25% | 拆成两个风险：骑手人身安全顾虑（证据偏高）vs 仓库盗窃（未量化，用 NIBRS 半径查询） |
| DTLA / Koreatown 人口 | 8–9 万 / 11 万+ | DTLA 6.1–6.5 万（供应商多边形）vs 10 万套住宅（DTLA Alliance 范围）；Koreatown 12.4 万（Mapping L.A. 2008）；Westlake 11.6 万（2024，未核实）且离场地更近 | 边界问题不是数字错误：固定一套 tract 多边形，同一方法算 SF 核心区 |
| SB 1271 生效日 | 未提及 | 一个探测说出租认证要求 2026-01-01 生效，另一个说 2028-01-01 | 读法条原文；无论哪个都在 24 个月窗口内 |
| 数据集新旧 | LAPD "2020 to Present" | 已冻结改名 "2020 to 2024"；LA 市餐厅检查 Socrata 2018 年后停更且无坐标；SF LIVES 2019 年停更；LA County 门户已迁 ArcGIS | 用 NIBRS、LA County 餐厅 inventory、LA Active Businesses、SF tvy3-wexg / g8m3-pdis |

### C.3 本轮工具限制

- Reddit 对当前抓取工具域名级封锁（API 400），骑手社区证据这一块完全没探到，需要人工或官方 API。
- LoopNet、LA Times Mapping L.A.、LA City Planning PDF、Axios、Wayback Machine 返回 403 或不可达，相关数字只来自搜索摘要。
- 所有 "仅搜索摘要" 的数字在建模前必须重新核实。

### C.4 完整性检查补充的遗漏来源（本轮没搜、下一轮应搜）

按决策价值排序，前几项都是免费的：DoorDash 2026 两轮配送报告全文（LA 占比）；韩语和西语骑手渠道（Radio Korea / 중앙일보 分类广告、Naver cafe、KakaoTalk 开放群、西语 Facebook 群）；Craigslist / OfferUp / Marketplace 抓取（非正规租赁 + 二手残值）；加州 DMV 按 ZIP 的摩托车注册与 M1/M2 持证数；NHTSA vPIC 查 FLASH / MK.II 能否上牌；UL Product iQ 查电池和充电器认证；ZIMAS + LADBS 查分区与 CofO；LAFD 预咨询；两家保险经纪报价；SFPD 数据对 261 6th St 做同样的半径查询；LADOT 送餐机器人许可数。

---

## D. 必须向你（HMP）询问的数据

### P0-a：先对齐口径（一封邮件能答）

1. **">1,000 已售" 的口径**：是否只算 SF 店；是否含 Davis 和线上；是否含所有车型；与 2026 年 4 月报道的 "SF 600+ e-moped、目标年底 1,000" 如何对应。
2. **SF 店结构**：415 eBikes（Mandala Global, LLC，2024-08-09 登记）是 HMP 自营还是独立经销；LA 打算复制哪种结构。
3. **SF 骑手业务起点**：2024 年 8 月开店前有没有 SF 销售（pop-up、线上、Davis 发货）；ramp 时钟从哪个月起算。
4. **SF 骑手车队的车型**：在租 ~100 台和 1,000+ 已售里，Class 2 INNO / LIVA、Lightning 3000、FLASH / MK.II 各占多少。这决定 "SF 已验证" 验证的是哪一档。

### P0-b：没有这些，模型只是猜

5. **SF 逐月流量**：每个客户的首次交易日期和类型（买车 / 整车租 / 只租电池）、当前状态（活跃 / 流失 / 被盗 / 转卖）。Shopify + Stripe 导出即可。用来画 ramp、算活跃比例、定 M3/M6/M12 的阈值。
6. **SF 租赁分母**：总租赁车队台数（按状态：在租 / 维修 / 闲置 / 丢失）、每台每月出租天数、租期分布、租转买比例和时间、周租客户第 1→4→8→12 周留存。
7. **SF 客户地理**：所有销售和租赁合同的 ZIP；电池订阅用户到 261 6th St 的距离分布，以及换电频率和流失随距离的变化。这是 LA 场地 catchment 半径的唯一依据。
8. **客户构成**：职业外卖员比例；平台分布；一人几个 app；每周工时；买车前的交通方式（开车 / 燃油 scooter / 便宜 e-bike / 自行车 / 没有）；**持 M1/M2 的比例，以及签约时是否记录驾照类别**；各车型在平台上注册为 bike / scooter / motorcycle 哪种模式。
9. **价格与成本**：各 SKU 售价、落地成本（FOB + 运费 + 关税 + 保修准备）、实际成交周租/月租（扣除折扣和免费周）、押金、电池订阅价、换电费、每用户每周换电次数。网页上的租金表是图片，请直接给。
10. **盗损、坏账、保险**：每 100 车-月的被盗和不归还次数、GPS 找回率、押金没收额、chargeback 和未付尾款比例；现有保单（承保人、险种、保费、免赔、是否排除无照驾驶人和商业配送用途）；261 6th St 的入室盗窃 / 门口客户车辆被盗记录和安保支出。
11. **电池**：每块电池成本；最老的 20 块订阅电池的 BMS 循环数和剩余容量；每用户配几块；订阅月流失；换电站电费；**每个电池和充电器 SKU 的 UL 2271 / 2849 / EN 15194 认证证书**；SFFD 对 SF 店电池存储/充电的许可编号和条件。
12. **SF 固定成本与盈利**：SF 店租金、面积、租约条款；人员配置和时薪；各业务线（销售 / 整车租 / 电池 / 维修 / 配件）的毛利和贡献；SF 毛利第几个月覆盖租金；可用于支撑 LA 12–18 个月亏损的现金。
13. **获客**：每个客户的来源（walk-in / 转介绍 / 线上 / 平台）；转介绍占比和头部推荐人；客户语言和来源国；创始人第一年每周花在 SF 销售上的时间；是否已有任何 LA 询盘或发往 LA ZIP 的订单。
14. **访问时段**：SF 店换电、维修、换车的按小时分布，19 点后占比，晚班员工事故记录。这决定 Ceres 晚间营业是否可行。

### P1：影响精度

15. 客户在"确认能赚钱"那一步展示的收入截图：时薪、日单量、平台、车型。这是 LA 付费能力的最好依据（公开数据只有加州外卖员税后 $5.93/小时这种粗数）。
16. 维修工单：每台在租车每千英里维修成本、平均事故维修账单、停工天数；二手车（12 个月租赁退役）在 HMP 内部和第三方的成交价。
17. 配件/维修的每客户年均消费；每次换电访问顺带产生维修工单的比例（这是合址的价值）。

### P2：场地与租约（问经纪人 / 房东）

18. 768 Ceres 书面条款：base rent 还是 Full Service / NNN（三个镜像给出 $10.1k / $11.8k / $13.5k 三个数）、期限、免租期、TI、押金、个人担保、转租/提前退出条款、768 是否可以单独租（一个聚合站把 768+772 打包）。
19. 房东和房东的保险公司是否书面接受"锂电池充电/换电 + 电动摩托维修"用途；当前 CofO；喷淋设计参数。
20. 用 LA 地址实测 DoorDash 和 Uber Eats 各开放哪些车辆模式（这个你的 SF 员工用手机十分钟能做）。

---

## E. 目前最容易导致判断错误的 5 个假设

（待本轮对抗式评审结果填入）

---

## F. 下一步

1. 你回复 D 部分 P0 数据（有多少给多少，没有的标"没有"）。
2. 我用公开数据填 FACT_PENDING，跑 Task 1 / Task 2，交模型 v1。
