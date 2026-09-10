# LA 车队客户在哪里：九类客户逐一核实、数字与打法（2026-09-09）

问题：**在 LA 找谁来做我们的车队客户**（企业或组织一次买 / 租 10–50 台），而不是把 SF 的自营骑手租赁店复制过去。

方法：三路研究代理（骑手端客户、摩托车端客户、政府项目与融资 / 保险 / 报价）共 72 次检索、约 40 次原始页面抓取，每条 FACT 带来源与日期；原始 JSON 见 `raw/fleet/`。单位经济见 `la-hub/model/fleet_econ.py`（v2，参数已按研究结果修正）。标签：FACT 有来源，ESTIMATE 由来源推算，ASSUMPTION 判断。

## 0. 一句话结论

**LA 和南加目前不存在"一次买 10–50 台无名品牌电动两轮车"的车队客户。** 九类客户逐一查过：平台不买车只做挂牌；餐厅和 K-town 配送公司用汽车；骑手租赁运营商已退出 LA（Zoomo）或尚未进入（Whizz）；保安 / 商圈巡逻要踏板助力山地车；驾校只用 125–250cc 汽油手动挡；警用需要警用套件和合作采购合同；政府项目 2026–27 没有开放的车辆采购且要求 UL 2849 认证；影视道具车行一次买 1–3 台；摩托租赁靠 OEM 合作而不是招标。

第一年车队线的现实规模：**基数约 30 台（INNO 为主）、高情景约 120 台，贡献 $2 万–$15 万**。它撑不起 $8,000 / 月的租约，更到不了 $50 万。车队在 LA 第一年是"渠道 + 关系"生意，值得做，但要按第 5 节的 90 天清单去做，不要为它配专职销售。

**2026-09-10 更新（创始人）**：INNO 的 UL 认证（整车系统与电池一起）预计 **9 月底到手**。这是本文最大的门槛（第 4 节第 1 条），10 月起 2.1（平台挂牌）和 2.10（政府 / 代金券项目）两类从"关着"变成"可以申请"；GoSGV 的秋季评审窗口正好赶得上。它不改变基数（没有开放的整批采购），但把高情景从"取决于认证"变成"取决于执行"。到手后先核对证书写的是 **UL 2849（系统）+ UL 2271（电池）**、型号和电池 SKU 与在售车一致，因为项目方按型号名核对。

## 1. 先看数字：一台车卖给车队能赚多少

（`fleet_econ.py` v2 输出，参数表见 `la-hub/model/fleet_econ_output.md`）

### 1.1 对照：自营骑手租赁（每台**自有**车每月，INNO）

| 定价 | 收入 | 成本 | 贡献 |
|---|---|---|---|
| SF 现价 $390/月（FACT，Shopify 2026 YTD） | $263 | $147 | **$116** |
| LA 基准 $199/月（ASSUMPTION） | $134 | $140 | **−$6** |
| 对标 Whizz $169/月（FACT） | $114 | $139 | **−$25** |

SF 的自营租赁靠 $390 / 月才赚钱。Whizz 2026 年 4 月随 DoorDash 合作进入 SF，$129–219 / 月租购、12 期后 $99 买断；SF 的租赁 + 电池 + 停车收入从 2025 年 11 月 $48.8k / 月跌到 2026 年 8 月 $15.1k / 月（Shopify，FACT）。这是不复制 SF 模式的第一个理由，也是第 1.2 节为什么只算 B2B。

### 1.2 B2B 整批销售（每台贡献 = 车队价 − 落地成本 − PDI − 6% 保修准备金 − $110 带断电的 4G 追踪器 − 销售成本）

| 产品 | 10 台 | 25 台 | 50 台 | 按 25 台价要赚 $50 万需要 |
|---|---|---|---|---|
| INNO | $2,070 → **$396** | $1,955 → **$288** | $1,840 → **$180** | 1,738 台 |
| MK.II | $3,599 → **$1,233** | $3,399 → **$1,045** | $3,199 → **$857** | 478 台 |
| FLASH | $5,400 → **$2,026** | $5,100 → **$1,744** | $4,800 → **$1,462** | 287 台 |

### 1.3 B2B 租赁（HMP 做出租方，24 个月，每台每月）

| 产品 | 月租 | HMP 持有成本（含保险 INNO $15 / 电摩 $60） | 贡献 | 每台压资金 |
|---|---|---|---|---|
| INNO | $151 | $112 | $39 | $1,410 |
| MK.II | $246 | $182 | $64 | $2,010 |
| FLASH | $298 | $221 | $77 | $2,910 |

三个结论不变：**利润在 FLASH / MK.II，INNO 整批卖只剩 $180–400；HMP 不要自己当出租方；$50 万 ≈ 290 台 FLASH 或 480 台 MK.II 整批卖出。** 第 2 节回答有没有人买。

融资现实（FACT，见 `raw/fleet/fleet-enablers-economics.json`）：没有找到愿意以 HMP 品牌资产做抵押放款的第三方租赁公司。小客户可用 Clicklease 类销售点租购（$500–20k，24–60 期，任何信用分；用户评价总还款常超过本金 2 倍）；超过约 $20k 的单子要么现金，要么 HMP 自己的资产负债表。Zoomo 自己靠 $30M 风险债务养车队。

## 2. 九类客户逐一核实

汇总表（12 个月内 HMP 车辆台数：低 / 基 / 高；来源见各小节）。

| # | 客户类型 | 存在吗 | 买什么 | 低 / 基 / 高 | 第一步 |
|---|---|---|---|---|---|
| 2.1 | 外卖平台（DoorDash、Uber Eats、饭团、熊猫） | 存在，但**不买车**，只给骑手挂折扣 | INNO（骑手个人买 / 租） | 5 / 15 / 40 | 邮件 eco-doordash@doordash.com；邮件 business@hungrypanda.co；中文直接找饭团 LA 城市经理 |
| 2.2 | 餐厅 / 幽灵厨房 / K-town 配送公司 | 存在，但以汽车为主 | INNO 2–5 台试点 | 0 / 5 / 15 | 电话 JQS Delivery 213-905-0441 问车辆构成 |
| 2.3 | 骑手租赁运营商（Zoomo、Whizz） | LA **空白**：Zoomo 退出，Whizz 未进入 | 不是客户，是竞争者 / 风险 | 0 | 监测 Whizz 城市列表 |
| 2.4 | 末端物流 / 电动货运（AxleHire、URB-E） | 证据停在 2022；URB-E 2023 年改名 Llama | 货运三轮 / 拖车，不是 INNO | 0 | 不投入 |
| 2.5 | 保安公司 / 商圈 BID 巡逻 / 校园 | 存在且多（DTLA Alliance、Fashion District、Hollywood 等） | 踏板助力山地车；INNO / 电摩不合适 | 0 / 0 / 5 | 不投入 |
| 2.6 | 摩托租赁 / P2P / 旅游 | 存在；EagleRider 靠 OEM 合作选车 | FLASH / MK.II 寄售或自挂 | 3 / 6 / 15 | 自己上架 Riders Share / Twisted Road；向 EagleRider 提寄售 |
| 2.7 | 影视道具车行 | 存在（Malibu Autobahn、Cinema Vehicles、Angel City、Galpin） | FLASH 1–3 台或按日租 | 0 / 2 / 5 | 发一页规格单 + 日租价 |
| 2.8 | 驾校（CMSP、Harley Riding Academy） | 存在，但只用 125–250cc 汽油手动挡 | 无 | 0 | 不投入 |
| 2.9 | 警用 / 市政车队 | 存在（LAPD 有 Zero），需警用套件 + 合作采购合同 | 无 | 0 | 不投入 |
| 2.10 | 政府 / 基金资助车队（LACI、GoSGV、Mobility Wallet、LA28） | 存在，但 2026–27 无开放采购；全部要 UL 2849（INNO 认证 9 月底到手，创始人 2026-09-10） | INNO | 0 / 0 / 40 | 注册 RAMP LA + SupplierOne；10 月带证书申请 GoSGV 指定店、回访 LACI |
| 2.11 | 南加其他城市小运营商 / "车队主" | 未能完成核实（研究被中断；Craigslist 不可抓取；4,604 条 LA 骑手 Reddit 语料无一提及） | INNO 批发 | 未知 | 用 `hmp-develop-b2b-market` 技能按 SD / OC 单独跑一批 |
| | **合计** | | | **8 / 28 / 120** | |

### 2.1 外卖平台：是渠道，不是买家

- DoorDash 的 Bike Dashing 页面（FACT，2026-09-09 抓取）只列三家车辆伙伴：Dirwin（全国购车 8 折 + 免运费装配）、Whizz（NYC、SF、DC、费城、芝加哥、Jersey City 租赁 85 折）、Swobbee（NYC / JC 换电）。**没有 LA 伙伴**。页面给的唯一联系方式是 eco-doordash@doordash.com，没有申请表。Dirwin 的做法是模板：自己网站上做一个 Dasher 身份验证表 + 折扣，DoorDash 在页面挂链接。来源：dasher.doordash.com/en-us/about/bike-dashing；dirwinbike.com/pages/delivery-partnerships。
- Uber 的 Vehicle Marketplace 是汽车市场，美国没有两轮供应商入口；两轮只有英国的 Zenion 电动轻摩（£75 / 周含换电）。LA 骑手注册要求自备车（FACT）。
- 饭团（Fantuan）把 LA 列为一线市场，有 @la_fantuan 账号（FACT）。**前一批研究说"饭团在 LA 给骑手租电动车"，第二批三次中英文检索无法证实**，唯一有记录的 LA 饭团骑手（世界日报 2025-12-01）骑的是自己从中国运来的九号踏板车。当未证实处理。
- 熊猫外卖（HungryPanda）在 LA 运营，公开合作邮箱 business@hungrypanda.co；给骑手的是"熊猫关怀箱"和骑手站，不供车；美国车辆要求未公开（FACT）。

平台的价值：把 HMP 挂进骑手看得到的折扣页，把个人骑手引到 Ceres Ave。收入形态是**一个个骑手的零售 / 租赁**，不是采购单。这一类的"车队"其实就是零售引流。

### 2.2 餐厅、幽灵厨房、K-town 配送公司：以汽车为主

- CloudKitchens 在 LA 有 7+ 处设施但只出租厨房，不养骑手（FACT，前一批）。
- Domino's：2019 年全美电动自行车项目由 Rad Power 独家供货；Benzina Zero HAULeR 的"Domino's 批准"只对澳新的 Domino's Pizza Enterprises 有效，不是美国；LA 加盟店招的 "Delivery Biker" 是自带车（FACT）。美国加盟商不太可能买未获批品牌。
- JQS Delivery（K-town，2010 年起，213-905-0441，jqsdelivery.com）是真实的自营配送公司，但不公开车辆和车队规模；韩语检索没有任何 LA 公司宣传踏板车车队，K-town 配送看起来是汽车（ESTIMATE）。LA Joy Quick Service 同理。
- 药品 / 鲜花 / 大麻配送在加州合法但以汽车为主（未逐一核实，ESTIMATE）。

能做的：2–5 台 INNO 给一两家 K-town / 圣盖博配送公司做路线试点。先打电话确认车辆构成，再谈。

### 2.3 骑手租赁运营商：LA 是空白，也是风险

- Zoomo 的 LA 计划页现在只显示 NYC 的价格（Zoomo Zero $39 / 周；Uber Eats 价 $20 / 周；双电池 $65 / 周；买断 $790）和一家 NYC 门店，**没有 LA 门店、营业时间或价格**；Trustpilot 有"LA 门店关闭客户无处维修"的差评（FACT，2026-09-09）。
- Whizz 2026-07-22 的城市列表：NYC、NJ、费城、DC、芝加哥、SF；2025–26 年借 DoorDash 合作新开四城，**LA 随时可能是下一个**（FACT）。
- 西语检索只找到 Santa Monica 的游客租车，没有 LA 骑手租赁运营商（FACT）。
- 4,604 条 LA 骑手 Reddit 帖子和评论里，Zoomo、Whizz、JOCO 零提及（FACT，本项目语料）。

解读：LA 没有品牌化骑手租赁不是没人试过（Zoomo 试过），而是两轮骑手池太薄（核心区约 740 人，ESTIMATE）。这一类不是客户；Whizz 进 LA 是对 HMP 骑手线的直接威胁。

### 2.4 末端物流：不是 HMP 的产品

AxleHire（现 Jitsu）2022 年在 LA 开四个微型枢纽用 URB-E 拖集装箱车配送；URB-E 2023 年 12 月改名 Llama 转向物流基础设施；两者 2025–26 状态无公开信息（FACT / 缺失）。这一类要的是货运拖车和三轮，不是 INNO。不投入。

### 2.5 保安、商圈 BID、校园：要的是踏板助力山地车

DTLA Alliance、Fashion District、Industrial District、Arts District、Century City、Hollywood Media District、Downtown Santa Monica、Downtown Long Beach、WeHo 的 BID 都通过承包商（Allied Universal、Block by Block、AGS、Patrol Solutions）跑自行车巡逻；LAPD 约 500 辆脚踏车 + 20 辆 BULLS Sentinel Class 3 电动车（FACT，前一批）。巡逻买家要踏板助力、能上人行道、能推着走的山地车；油门式踏板造型的 INNO 和 56 / 75 mph 的摩托车不合适。第二批没有找到任何 BID 采购轻摩 / 摩托巡逻车。**0 台。**

### 2.6 摩托租赁、P2P、旅游：唯一能立刻做的"车队"是自己的展示车

- Riders Share：车主分成 75%（Standard）或 60%（Premium，平台承担行程中机械维修和停运损失）；Lloyd's 承保每次租赁最高 $3 万；有 Zero 品牌页"先试骑再买"；没有公开的经销商计划，车行作为多车车主上架即可（FACT，2026-09-09 抓取）。LA 约 210 条车源，$31–320 / 天（前期）。
- Twisted Road：LiveWire 在 LA 约 $199 / 天；车主保障 $10 万责任 / $2.5 万车损（FACT，2019 年新闻，平台仍在运营）。
- 按 LiveWire $199 和 125–300cc 汽油车 $31–60 定价，FLASH / MK.II 展示车合理日租 $60–120；每月 8 个租赁日、75% 分成，**每台每月约 $400–700**（ESTIMATE）。5–8 台展示车 = 每月 $2–5k，同时是付费试骑漏斗，可仿照 Zero 在 EagleRider 的做法给 $300 租金抵购车款。
- EagleRider（总部 11860 S La Cienega Blvd, Hawthorne）：2021 年起与 Zero 合作出租 SR/F、SR/S，LiveWire 在部分门店；电动品牌是通过 **OEM 合作**（联合营销 + 购车抵扣）进入，不是招标（FACT / ESTIMATE）。对 HMP 可行的是寄售：HMP 提供 3–5 台 FLASH Plus，EagleRider 收租金，HMP 拿试骑漏斗。加盟页面经代理不可读，车队归属结构未核实。
- 游客租车（Vespa Santa Barbara 等）用自动挡轻型踏板车；MK.II 物理上合适但要 M1 驾照，过滤掉大部分游客（FACT / ASSUMPTION）。"Tony's DMV M1 Scooter Rental"（Yelp）专门租车给考 M1 的人，MK.II 可能有吸引力，地址和规模未核实。

### 2.7 影视道具车行：1–3 台的零星生意

Malibu Autobahn（4,000+ 道具车，自有摩托库存，无电动车；310-776-5163，contactus@malibuautobahn.com）、Cinema Vehicles（1,600+ 车）、Angel City Motorcycles（LA 唯一只租摩托给剧组的公司，含运输、现场管理和特技替身）、Galpin Rentals、Venice Vintage、Glory Motorworks（FACT，ProductionHub 目录与官网）。没有一家挂电动摩托。它们按剧本需要一次买 1–3 台，动作戏要成对的特技车。做法：一页规格单（尺寸、重量、极速、充电时间、静音、成对供应、现场充电方案）+ 日租价，并把 HMP 自己登到 ProductionHub 和 LA 411。

### 2.8 驾校：结构性关闭

CMSP 由 CHP 通过 Total Control Training 运营，2025 年 6 月累计培训 150 万人；场地提供 125–250cc 汽油手动挡训练车（Golden State Moto、2 Wheel Safety 等 FAQ）；"eRider" 只是线上课堂，没有任何场地用电动车（FACT）。75 mph 的 FLASH 不适合初学者，无离合的 MK.II 教不了 MTC 要考的离合换挡。Harley Riding Academy（Glendale、Huntington Beach）只用 H-D 车。**0 台。**

### 2.9 警用 / 市政：需要警用套件和合同载体

LAPD 2014 年起用 6 辆 Zero MMX 越野电摩，2020 年新增全电摩托（FACT）；2023–26 没有搜到 LAPD / LASD / Metro 的新采购或 Sourcewell 合作合同授标。警用需要灯光警报器、电台支架、防撞杠、服务培训和竞标 / 合作合同，HMP 都没有（ASSUMPTION）。**12 个月内 0 台。**

### 2.10 政府 / 基金资助车队：2026–27 没有开放采购，且全部要 UL 2849

- LACI South Central Power Up：2024-04-16 启动，250 辆"全新定制"踏板助力电动车，7 个站点，两年试点，CARB STEP 资金经 LADOT；**供应商在任何公开页面都没有署名**；laincubator.org/pilots 没有车辆 RFP；southcentralpowerup.com 2026 年 8 月仍是 2024 年的文案（FACT）。
- Clean Mobility Options：官方页面写"额外资助机会目前已关闭"（FACT）。CARB STEP 2026 年没有 LA 轮次浮出。
- **唯一开放的钱**：SGVCOG GoSGV 电动货运车 $2,000 代金券（第二轮 450 张 2026-04-29 开放，约 900 张待发，下一次评审 2026 年秋）。要求 Class 1–3、≤750W、≥330 lb 载重、**UL 2849 或 EN 15194**，且只能在 7 家圣盖博谷指定店兑换（FACT）。Ceres Ave 不在其中；INNO 要先拿到证书和载重标定，再进一家指定店（Montebello Bicycles 离 DTLA 最近）。
- Mobility Wallet 第三期 2026 年启动（Caltrans + 联邦 ATTAIN）：$150 / 月预付卡可在自行车店消费。HMP 只能做**商户**，不能做车队供应商（FACT）。
- LA28（2026 年 3 月采购计划，全文见 `raw/fleet/la28_procurement.txt`）：75% 本地 / 25% 小企业目标；HMP 在 768 Ceres 属于 Hyper-Local + Micro；**没有两轮 / 微出行类别**，最近的是 Fleet Management Services（2026 Q2–Q3）、Vehicle Rental or Leasing（2027 Q2、2028 Q2）。注册 La28.SupplierOne.co 和 RAMP LA 免费，之后只能作为车队总包的两轮分包（FACT）。

这一类的门槛不是关系，是**UL 2849 系统认证**（SB 1271 之后加州零售同样要求）。没有证书，所有项目都关着门。**更新 2026-09-10**：创始人确认 INNO 的 UL 认证（系统 + 电池）9 月底到手。到手后的顺序：(1) 10 月第一周向 GoSGV 提交零售商表单，或把 INNO 放进 Montebello Bicycles 等指定店，赶 2026 年秋季评审；(2) 带证书拜访 LACI 问 Power Up 更新窗口；(3) 用同一份合规包去 DoorDash 挂牌。基数仍是 0（没有开放的整批采购），但高情景 40 台从"不可能"变成"看执行"。

### 2.11 南加其他城市小运营商与"车队主"：未完成

计划中的第 7 路（SD / OC / IE 的配送导向车店、非正式"车队主"、社区组织）因账户用量上限中断，未能重跑。已有的旁证：LA 骑手语料无一提及租车；西语检索无 LA 骑手租赁；Craigslist 页面经代理不可读。这一类的正确工具是 `hmp-develop-b2b-market` 技能，按 San Diego / Orange County 各跑一批经销商 + 租赁运营商名单（需要销售主工作簿做去重）。

## 3. 加总：车队线第一年值多少

| 情景 | 台数 | 构成 | 贡献（按 1.2 节 25 台价；展示车按每台每月 $500 × 8 个月） |
|---|---|---|---|
| 低 | 8 | 5 INNO 骑手 + 3 展示车 | ≈ $1.4k + $12k 展示车租金 |
| 基 | 28 | 15 INNO 渠道引流 + 5 INNO 配送公司试点 + 6 展示车 + 2 FLASH 影视 | ≈ $5.8k + $3.5k + $24k + $3.5k ≈ **$37k** |
| 高 | 120 | 40 INNO 渠道 + 15 配送公司 + 40 政府项目（需 UL 2849） + 15 展示 / 寄售 + 5 影视 + 5 游客租车 MK.II | ≈ $27k + $60k 展示租金 + $9k + $5k ≈ **$100k–150k** |

对照：768 Ceres 36 个月租约总额约 $30 万；$50 万目标需要约 290 台 FLASH 整批卖出。**车队线在第一年是 $3–15 万的补充，不是主引擎。**

## 4. 要做车队生意，先要有的东西（按重要性）

1. **INNO / LIVA 的 UL 2849 系统证书（或 EN 15194）和书面 330 lb 载重标定。** 没有它：DoorDash 挂牌大概率不过、GoSGV 不能兑换、任何 CARB 子项目不能评分；SB 1271 之后加州零售也要。**状态（2026-09-10，创始人）：INNO 的 UL 认证（系统 + 电池）预计 9 月底到手。** 到手 48 小时内做一页合规包：证书 PDF（核对 UL 2849 + UL 2271、型号与电池 SKU）、330 lb 载重标定、SB 1271 合规声明、电池储存与充电说明；LIVA 是否同批认证需确认。
2. **DMV 经销商执照**（卖 FLASH / MK.II 给任何加州企业都需要），以及一家能做商业电摩车队（surplus lines，XInsurance 类）的保险经纪，报价拿到手再对外报车队价。
3. **车队报价单**（详见 `raw/fleet/fleet-enablers-economics.json` 的 offer_sheet）：INNO $2,070 / 1,955 / 1,840（10 / 25 / 50 台）、MK.II $3,599 / 3,399 / 3,199、FLASH $5,400 / 5,100 / 4,800；24 个月保修（电池 24 个月至 70%，明确覆盖配送工况）；带断电的 4G 模块（25 台以上含在价内，$6 / 月连接费另计）；48 小时借用车 SLA（Ceres Ave 15 英里内）；30% 定金、放车前付清；Clicklease 作为小客户的分期入口并**如实披露成本**。
4. **零件延续承诺信 + 托管备件**：每个车队买家都会问 Cake（2024 年破产，两次召回）和 Ubco（2025 年接管，拿到澳洲邮政 175 台订单五个月后）——你怎么证明两年后还有零件。
5. **5–10 台上牌、投保、装追踪器的 FLASH / MK.II 展示车**，日租价卡，租金抵购车政策；ProductionHub 和 LA 411 供应商登记。
6. **注册**：RAMP LA、La28.SupplierOne.co、Cal eProcure、SAM.gov；SBA 小企业自认证；LA 市营业税证（768 Ceres）；$1M / $2M 责任险 COI 模板。
7. 中西双语骑手物料 + 安全培训模块（GoSGV 和 Power Up 都要求培训）。

## 5. 90 天打法：先打谁、发什么、看什么

按"成本低、能在 90 天内出结果"排序。不要为车队线招专职销售；由 LA 店长和创始人兼做。

| 周 | 动作 | 对象与联系方式 | 90 天验收 |
|---|---|---|---|
| 1 | 注册 RAMP LA / SupplierOne / Cal eProcure；准备合规包模板，等 9 月底 UL 证书一到就填入（核对 UL 2849 + UL 2271、型号、电池 SKU；330 lb 载重标定；SB 1271 声明） | 内部；la28.supplierone.co；rampla.org | 四处注册完成；10 月第一周合规包成稿 |
| 1–2 | 在 hmpbikes.com 上做 Dasher 验证表 + LA 折扣页（照 Dirwin 模板），发一页 LA 方案 | eco-doordash@doordash.com | 60 天内进入 Dasher Deals 或收到明确拒绝 |
| 1–2 | 中英文邮件提 LA 骑手福利合作（INNO 折扣租购 + Ceres Ave 换电） | business@hungrypanda.co；饭团 LA 城市经理（@la_fantuan，创始人中文直谈） | 两家之一给出 LA 骑手数与车辆构成；一家签合作 |
| 2–4 | 5–8 台展示 FLASH / MK.II 上架 Riders Share（Standard 75%）和 Twisted Road，$60–120 / 天，租金 $300 抵购车 | riders-share.com/pages/new-owners；twistedroad.com | 月租金 ≥ $2k；试骑转定金 ≥ 2 单 |
| 2–4 | 电话 JQS Delivery 问车辆构成，提 2–3 台 INNO 路线试点 | 213-905-0441（韩语更好） | 一家配送公司试点 |
| 3–6 | 一页规格单 + 日租价发影视道具车行；登 ProductionHub / LA 411 | Malibu Autobahn 310-776-5163 / contactus@malibuautobahn.com；Cinema Vehicles；Angel City；Galpin | 一次剧组租用或 1 台成交 |
| 4–8 | 向 EagleRider 总部提 3–5 台 FLASH Plus 寄售（HMP 保留所有权，对方收租，HMP 拿试骑漏斗） | eaglerider.com/franchise 合作入口；LA 店前台 | 一次会面 |
| 4–12 | 拜访 LACI（La Kretz，步行 20 分钟），问 Power Up 更新时间表和现供应商；申请孵化器 | laincubator.org；213-358-6500 | 知道供应商是谁、更新窗口何时 |
| 4–6（10 月上旬，证书到手后） | 申请 GoSGV 指定店或让 Montebello Bicycles 上架 INNO；对接 Mobility Wallet 商户；带证书回访 LACI | sgvcog.org/gosgv 零售商表单；mobilitywallet@metro.net；laincubator.org | 2026 年秋季评审前进入 GoSGV 名单 |
| 任意 | 用 `hmp-develop-b2b-market` 按 SD / OC 各跑一批经销商 + 租赁运营商 | 需销售主工作簿 | 两批各 ≥ 10 条 pursue 线索 |

**不做的**：驾校、警用、BID 巡逻、末端物流。这四类在产品和合同结构上对 HMP 关着门，销售时间投进去是浪费。

**杀线**：第 6 个月末，如果 Dasher Deals 没挂上、饭团 / 熊猫没有一家合作、展示车月租金 < $1.5k，车队线降级为"只做展示车 + 政府项目关系"，不再占用店长时间。

## 6. 没查到、需要创始人核实的

1. ~~INNO / LIVA 是否已有 UL 2849 系统认证~~ **已答（2026-09-10）**：创始人确认 INNO 的 UL 认证（系统 + 电池）9 月底到手。剩余核对：证书标准号（UL 2849 系统 + UL 2271 电池）、型号与电池 SKU 是否与在售一致、LIVA 是否同批。
2. 饭团是否真的在 LA 给骑手租车（前一批说有、第二批证不了）。创始人一个中文电话就能定。
3. Power Up 250 辆车的供应商是谁（LACI / LADOT 页面未署名；可查 LADOT 议会档案采购单）。
4. JQS Delivery 和 LA Joy Quick Service 的车辆构成与司机数。
5. Riders Share LA 电动车源数与实际成交日租（页面 JS 渲染，代理不可读，需在普通浏览器打开）。
6. EagleRider 的加盟 / 自营车队归属，以及是否接受寄售。
7. 南加其他城市运营商与"车队主"（2.11）尚未系统核实。

## 7. 对创始人的直话

- 你问的"车队客户在哪"，答案是：**在 LA，一次买 10–50 台的客户今天不存在**。存在的是三种小东西：平台挂牌带来的个人骑手、影视和租赁的零星台数、以及一年后可能开放的政府项目更新。
- 车队线第一年最好的结果是 $10–15 万贡献，基数只有 $3–4 万。它不能作为签 768 Ceres 的理由；如果租约的逻辑需要车队来撑，那个逻辑不成立。
- 真正有车队级利润的只有 FLASH（每台 $1,700–2,000）。但 FLASH 的买家是有 M1 驾照的个人和零星企业，不是车队。车队生意在 HMP 现在的产品线里，本质上是 **FLASH 零售的试骑漏斗**（P2P 展示车、EagleRider 寄售）加 **INNO 的渠道引流**。按这个定位做，它值得每周两小时；按"$50 万靠车队"做，会重复 Ubco 的故事。
- 最值钱的一件事不是找客户，是 UL 2849。它同时打开 DoorDash 挂牌、GoSGV、CARB 子项目，也是加州零售的合规底线。**创始人确认 9 月底到手**：那么 10 月的头两周就是这条线的窗口期（合规包、DoorDash 邮件、GoSGV 表单、LACI 回访四件事一起做），错过秋季评审要再等一轮。

---

来源：`raw/fleet/courier-side.json`（16 次检索）、`raw/fleet/motorcycle-side.json`（14 次）、`raw/fleet/public-grant-funded-fleets.json`（18 次）、`raw/fleet/fleet-enablers-economics.json`（24 次）、`raw/fleet/la28_procurement.txt`；给研究代理的上下文见 `raw/fleet/00-context-given-to-researchers.md`。

## 8. UL 2849 + UL 2271 到手后的优势，以及竞争者的认证状态（2026-09-10）

两个标准的分工：**UL 2849** 是整车电气系统认证（电池、充电器、电机、控制器、线束、充电口作为一个系统测试）；**UL 2271** 是电池包认证（过充、短路、高低温、冲击、挤压）。证书按型号和配置发，换电池供应商、换充电器或改控制器都要重新认证，所以证书上的型号和电池 SKU 必须和在售车一致。

### 8.1 它带来什么

| 维度 | 没有认证 | 有认证 | 来源 |
|---|---|---|---|
| 加州合法销售 | SB 1271：2026-01-01 起禁止销售、分销、出租未经认可实验室按 UL 2849 / UL 2271 / EN 15194 测试的新电动自行车和电池；自营租赁车队的宽限到 2028-01-01 | INNO 在加州零售、租购、批发给企业全部合法；大量未认证的踏板造型进口车被清出市场 | bikelegalfirm.com SB 1271 解读；SB 1271 立法分析 2024-06-24 |
| 纽约 | Local Law 39（2023-09）禁售未认证车；**Local Law 95（2026-01-26 起）** 把要求从"卖"扩展到"用"：外卖平台的骑手所骑车辆必须 UL 2849 + UL 2271，责任落在 DoorDash / Uber Eats / Grubhub 等平台 | 若做纽约或任何平台合作，这是准入门票；平台为骑手车辆合规负责的趋势会向其他城市扩散 | council.nyc.gov 2025-08-14；getwhizz.com NYC 2026 指南 |
| 联邦 | CPSC 2026-06-24 发布拟议规则（16 CFR 1265），把 UL 2849-20 / UL 2271-23 / UL 2272-24 加修改项设为全国强制；评论期至 2026-08-24；最终规则公布后 180 天生效 | 已认证的车最接近合规；但拟议规则加了防拆电池外壳、反接测试、标签和说明书要求，**现有证书大概率要补测或改标签** | federalregister.gov 2026-12749 |
| 电商平台 | Amazon 要求 UL 2849 测试报告由授权实验室直接提交（DV 验证），Walmart 类似 | INNO 可以上 Amazon / Walmart，多一条全国零售渠道 | goatconsulting.com；gdestl.com Amazon DV 指南 |
| 政府补贴 | 加州 E-Bike Incentive Project（$1,750–2,000 / 张，要求 UL 2849 或 EN 15194、≤750W、可用脚踏、集成车灯、电气件 1 年保修、经批准零售商）、GoSGV $2,000（UL 2849 / EN 15194 + 330 lb 载重）、CARB 子项目全部关门 | 全部可申请；INNO $2,300 的价位让州补贴覆盖 75–85% 车价，是对低收入骑手最强的购车理由 | ww2.arb.ca.gov；sgvcog.org/gosgv |
| 外卖平台挂牌 | DoorDash 现有三家车辆伙伴 Whizz（Storm-2 UL 2849 + TÜV）、Dirwin（UL 2849 / 2271）、Swobbee 都有认证 | 达到进入 Dasher Deals 的事实门槛 | getwhizz.com；dirwinbike.com/pages/faqs |
| 保险与消防 | 车队保险和产品责任险按认证状态定价；768 Ceres 的锂电池储存 / 充电（2025 CFC §320）要过 LAFD 和业主 | 报价更容易拿到、更便宜；对业主和 LAFD 的说明材料有据可依；出事时的责任抗辩基础 | lendcontrol.com 保险指南（经纪按存储、锁具、追踪器和认证定价） |
| 骑手居住 | 纽约公房和越来越多公寓禁止非 UL 车进楼充电；LA 的物业跟进中 | 骑手能在家充电，是租购转化的隐性条件 | ulse.org NYC 火灾死亡下降报告 |

一句话：**UL 认证在加州是准入门槛（没有就不能卖），在补贴、平台、电商、保险四条线上是加速器。** 它把 INNO 和"自己从中国运来的九号踏板车"、未认证的踏板造型进口车区分开；但它不能把 INNO 和已认证的主流品牌区分开（见 8.2）。

### 8.2 Infinite Machine Olto 有没有 UL 认证

**有。** Olto 的官方技术规格页写明 "UL 2849 (vehicle) & UL 2271 (battery) Certified"（FACT，2026-09-10 抓取 infinitemachine.com/olto/tech-spec）。其他参数：Class 2 电动自行车、限速 20 mph、1.2 kWh（25 Ah）可拆电池、整车约 176 lb（电池 20 lb）、售价 $3,495（RoostMode 2026 评测标题）。

含义：Olto 是 INNO 在"踏板造型 Class 2"这个品类里的高价对手，认证上已经和 HMP 打平。HMP 拿到 UL 之后与 Olto 的差异不在认证，而在：价格（$2,300 对 $3,495）、面向骑手的配置（货架、外卖箱、备用电池、换电订阅）、本地服务网点（Ceres Ave 维修 + 借用车）、以及 FLASH / MK.II 的高速产品线（Olto 没有摩托车级产品）。营销上不要把 UL 当卖点打 Olto，要打价格和服务；UL 用来打未认证的低价进口车和平台 / 补贴门槛。

### 8.3 到手后 48 小时的合规包（重复第 4 节第 1 条，便于执行）

证书 PDF（核对标准号 UL 2849 + UL 2271、发证实验室、型号、电池 SKU、充电器型号）；330 lb 载重书面标定；SB 1271 合规声明；电池储存与充电说明（给业主、LAFD、保险经纪）；Amazon DV 验证由实验室直接提交；加州 E-Bike Incentive 批准零售商申请（ebikeincentives.org/retailers 页面 2026-09-10 返回 404，需从主站重新定位入口）。
