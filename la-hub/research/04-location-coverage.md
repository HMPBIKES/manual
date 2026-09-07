# 在 LA 哪里选址最能覆盖外卖骑手（选址覆盖分析）

版本：v2，2026-09-07（v1 在帖子层分析后写成；v2 加入 37,225 条评论的七读者分析和一轮反证评审，并据此收窄结论）。问题：如果目标是"让尽可能多的两轮外卖骑手顺路到店"，地址应该放在 LA 的哪里；768 Ceres Ave 在这个标准下排第几。

三层证据，互相独立：

| 层 | 回答什么 | 数据 | 脚本 / 文件 |
|---|---|---|---|
| A. 骑手自述 | 骑两轮的骑手说自己在哪里跑单、哪里赚钱、哪里危险 | 用真实浏览器（headless Chromium）抓 Reddit 公共 JSON：20 个子版 × 60 组关键词，约 6,600 帖 + 相关帖的评论 | `raw/reddit/reddit_scrape.py`、`reddit_tally.py`、`raw/reddit/*.jsonl` |
| B. 需求密度 | 骑手接单点（餐厅）在地理上怎么分布，候选地址 1–3 英里能覆盖多少 | LA County 公共卫生局餐厅清单（约 2.8 万家去重）+ ACS 人口 / 无车家庭 | `raw/market/site_coverage.py` → `site_coverage.csv` |
| C. 治安 | 候选地址周边抢劫、伤害、自行车被盗的密度 | LAPD 2020–present 犯罪数据，取 2023-01 至 2024-03（LAPD 2024-03 换系统后数据不全） | `raw/market/site_crime.py` → `site_crime.csv` |
| D. 场地 | 各区现在租得到什么、多少钱 | PropertyShark / CommercialCafe / Craigslist 挂牌（LoopNet 等 CoStar 站点 403） | `raw/market/listings.json` |

标签沿用前几份报告：FACT 可核对；ESTIMATE 有数据但要换算；ASSUMPTION 我定的参数，可替换。

## 0. 一句话答案

**地址应该放在 DTLA 的西南缘到 Pico-Union 之间（Pico / Olympic 走廊，Figueroa 到 Vermont），而不是 768 Ceres 所在的东南仓库区；如果开两个点，卫星点放 Koreatown 北缘的 Vermont / Beverly 到 Wilshire 一线。** 这是骑手作业三角（DTLA–Koreatown–Hollywood）的南边，2–3 英里能同时够到 DTLA 核心、Koreatown 和 USC，语料里唯一被完整描述的候单路线（Pico-Union，Home Depot Wilshire + 7th St）就在这里，街区级犯罪密度只有 Historic Core / MacArthur Park 的十分之一，工业 / 灵活空间的租金是 Koreatown 临街的一半。

这个结论经过一轮专门的反证评审（6.4）后有三处收窄：(1) 走廊的优势在 2–3 英里，**1 英里内它比 768 Ceres 和 DTLA 核心都稀**（18th St 370 家 vs Ceres 544 vs Historic Core 830），所以它押的是"骑手愿意为换电 / 维修绕 1–2 英里"，这要用 HMP SF 的客户距离数据验证；(2) 走廊内部，Pico / Vermont（2474 W Pico）和 1824 S Magnolia 在 2–3 英里覆盖和治安上都优于 18th St，18th St 的优势只是一条匿名、低于市价、面积前后不一致的 Craigslist 广告，必须先实地核实；(3) 两点方案里主店选 18th St 还是 Ceres 对并集覆盖影响不到 2%（2,641 vs 2,597），差别在租金、Skid Row 邻近和地铁，不在覆盖。

| 方案 | 具体街区 | 目前能租到的例子 | 2 英里餐厅 | 半英里抢劫（14 个月） | 月租 |
|---|---|---|---|---|---|
| **单点主店（首选走廊）** | Pico / Olympic 走廊，Figueroa 到 Vermont（South Park 南段 + Pico-Union），三个现成候选按数字排序：2474 W Pico（Pico / Vermont）、1824 S Magnolia、18th St（Grand–Olive） | 2474 W Pico 4,100 sf 临街（面议）；1824 S Magnolia 7,515 sf 仓库（折算 ~$14,400，待核）；18th St 7,644 sf 仓库，卷帘门 + 装卸台 + 800A（$6,900，匿名广告，待核） | 1,435 / 1,521 / 1,410 | 78 / 68 / 96 | 面议 / ~$14,400 / $6,900 |
| 单点主店（治安最好的备选） | Pico-Union 西段 / Koreatown 南缘：Pico–Venice，Vermont–Normandie | 1738 Cordova St 5,000 sf，平地门 + 装卸台 | 1,206（3 英里 2,331） | 50 | ~$9,900 |
| **两点方案的卫星点** | Koreatown 北缘 Vermont / Beverly 到 Wilshire / Vermont–Western 一线，红线站周边；East Hollywood（Vermont / Sunset）为备选 | 3651 Beverly Blvd 4,434 sf 独栋灵活（面议）；856 S Vermont 3,549 sf 临街，15 车位（~$9,760） | 1,401（3 英里 2,588）/ 1,342（3 英里 2,680） | 57 / 108 | 面议 / ~$9,760 |
| 对照：768 Ceres | Warehouse District 东南角 | 8,443 sf | 1,217（1 英里 544，高于走廊各点） | 156（伤害 285；0.25 英里 27 / 51，与走廊各点相当） | $10,000 |

如果只开一个点，选 Pico / Olympic 走廊那一格，三个候选地址里先核实 18th St 的广告，核实不了就按 2474 W Pico、1824 S Magnolia 的顺序谈；如果开两个点，主店放走廊、卫星点放 3651 Beverly Blvd 一类的 Koreatown 北缘位置，两点 2 英里并集 2,641 家餐厅（18th St + Beverly），是 768 Ceres 单点（1,217）的 2.2 倍。评论级证据（1.8）把卫星点从 Olympic / Vermont 往北推到了 Beverly–Wilshire 一线：Koreatown 的骑行重心在 Wilshire / Western 到 Wilshire / Vermont，语料里唯一的候单点 Home Depot Wilshire（Wilshire & Union）离这里 1.1–1.7 英里，DoorDash 把 Koreatown 划在 Hollywood-Silverlake 区里、单量向东半边倾斜，而 3651 Beverly 是所有中心候选里抢劫 / 伤害最低的（57 / 85）。768 Ceres 不适合做唯一的面向骑手的门店（1.5 英里外掉队、东南半圆是仓库、无地铁、骑手对 Skid Row 的描述全是负面）；但"Ceres 做仓库 + Beverly 做前台"的并集是 2,597，只比最优组合少 2%，所以如果房东只肯整租 8,443 sf，这个配置是可行的第二选择，代价是每月多 $3,100 租金和骑手对 Skid Row 邻近的抵触。

三层证据各自指向什么、哪里不一致，见第 6 节；Reddit 数据的偏差（英文、开车骑手占 97%、Koreatown / Westlake / Pico-Union 几乎无声）见 1.7 和第 8 节。

---

## 1. Reddit 骑手自述（层 A）

### 1.1 怎么抓、抓到什么

用 headless Chromium（Playwright，走代理，TLS 1.2）先访问 old.reddit.com 拿 cookie，再调 Reddit 的公共 JSON 端点（`/r/<sub>/search.json`、`/comments/<id>.json`），限速 3.5 秒一请求，撞到 429 就退避重来。范围：

| 子版组 | 子版 | 关键词 | 用途 |
|---|---|---|---|
| 骑手版 | r/doordash_drivers、r/UberEATS、r/doordash、r/grubhubdrivers、r/couriersofreddit、r/Sparkdriver | "los angeles"、"LA bike / ebike / scooter / moped / motorcycle"、DTLA、koreatown、hollywood、santa monica、westwood、USC、silver lake、skid row 等 39 组 | 骑手在哪里跑、用什么车、赚多少 |
| LA 本地版 | r/LosAngeles、r/AskLosAngeles、r/Koreatown、r/DTLA、r/LosAngelesBikes、r/UCLA、r/USC、r/LAlist | "doordash bike"、"delivery ebike"、"delivery scooter" 等 14 组 | 居民视角看到的骑手、治安 |
| 车辆版 | r/ebikes、r/ElectricScooters、r/Surron、r/electricmopeds、r/Ebike、r/mopeds | "doordash los angeles"、"delivery LA"、"koreatown" 等 7 组 | 车型、续航、租赁需求 |

结果：7,764 帖 + 37,225 条评论（帖子层分析在 7,742 帖时做的），其中经严格 LA 校验的 3,095 帖（要求出现明确的 LA 标记，并剔除 Hollywood FL、Venice FL、Glendale AZ、Pasadena TX、Long Beach NY、Westlake TX 和 Louisiana 的 "LA"）。**其中发帖人自己骑两轮送外卖的只有 80 帖（含转帖 112 条）**，其余 3,000 帖是开车的。每条引用都经脚本核对为原帖原文（`raw/reddit/analysis_posts.json`）。

### 1.2 按区域：两轮骑手在哪里说话

| 区域 | LA 校验帖 | 两轮骑手帖 | 汽车骑手帖 | 两轮倾向 | 关键证据 |
|---|---|---|---|---|---|
| **DTLA** | 103 | **29** | 23 | 混合 | 全语料最高票帖（1,172 赞）是"从开车改骑电动滑板车，Downtown LA"；r/dtla 一位自行车骑手说 DTLA 的单比 Beverly Hills 和 Hollywood 都多；唯一被点名的自行车热点是 **6th & Spring**；但 DoorDash 自行车模式几乎没单，切到 scooter 模式又被派到核心区外很远；Bunker Hill 坡累；Skid Row 送单不安全；2020 后单量薄 |
| Hollywood / East Hollywood | 136 | 14 | 36 | 偏正面 | 2019–20 一位电动滑板车骑手在 Hollywood 挑 10:1（美元 / 英里）"独角兽"单（71 赞）；开车骑手说 DoorDash 的 **Hollywood-Silverlake 区"单多到淹"而 Hollywood-Beverly Hills 区"天天死"**；停车难让开车的想换两轮；2024–25 出现 $8 / 小时的饱和抱怨 |
| Santa Monica / Venice | 93 | 6 | 22 | 正面 | 平、有自行车道；两位 2024 年 e-bike 骑手的理由是不用养车 + Prop 22 活跃时段保底（约 $20–21 / 小时；注意这个保底是全加州同一规则、按当地最低工资 × 1.2，LA 市 2025 年为 $21.44 + $0.35 / 英里，并不偏向西区）；开车的说这里是"最差的地方"（堵、没车位、警察多），2024–25 有 5–7.5 小时只赚 $14–15 的帖 |
| Valley（SFV） | 89 | 5 | 25 | 混合 | 全语料最资深的两轮骑手（Unagi 滑板车 + 公交，5,500 单）在西 Valley，以商场旁的麦当劳为"指挥中心"充电；Valley 骑手会跑进 Hollywood / WeHo |
| Pasadena | 73 | 4 | 20 | 正面 | 2018 电动滑板车"很顺"；不在候选名单 |
| Glendale / Burbank | 63 | 4 | 22 | 混合 | Glendale 一位 49cc 踏板车骑手计划进 downtown 跑单；不在候选名单 |
| West Hollywood | 71 | 3 | 14 | 混合 | 2018 一位晚 6 点到 12 点的自行车信使在 BH / WeHo 反复被 LAPD 拦；热门餐厅门口 20 个骑手排队 |
| Westwood / UCLA | 26 | 3 | 4 | 混合 | 第二个被点名的自行车热点 **Westwood Blvd & Ohio Ave**；学生外卖公司 Duffl 用 Ninebot G30P 站立滑板车跑 3 小时班次，"路烂坡多，车经常坏" |
| **Koreatown** | 15 | **3** | 2 | 偏负面 | 2020 "Koreatown 早上自行车模式，惨"（截图）；2023 刚搬到 K-town 问骑车送单行不行；开车的说 Koreatown 在 Hollywood-Silverlake 区里，会派到 DTLA；信号差、tip bait、"downtown 或 koreatown 这种高单区不值" |
| Beverly Hills / Century City | 78 | 2 | 17 | 负面 | 大部分时间是死区；有人观察"Beverly Hills 的骑手用 Bird" |
| Culver City | 32 | 2 | 9 | 混合 | 开车的说 Culver City 区慢；Culver City Cuisine 幽灵厨房是取餐点 |
| Silver Lake / Echo Park | 24 | 2 | 7 | 混合 | 自行车骑手说 Silver Lake 小费差、"那些弯坡不是开玩笑的" |
| USC / Exposition | 7 | 1 | 1 | 无 | 一位 USC 研究生打算骑车送单问安全；开车的说 USC "至少有单"但学生小费约 $1；2019 DoorDash 曾单独划过 "USC island" 区 |
| Long Beach / South LA / East LA / Mid-City | 16–66 | 0 | 4–20 | 无 | 全是开车帖；Mid-City 2026 有一起 Olympic & Cochran 送酒被持械抢劫（74 赞） |
| **Westlake / MacArthur Park** | 1 | **0** | 1 | 无 | 骑手版里只有一条开车路过；r/AskLosAngeles 一位准住户担心 MacArthur Park 附近自行车被偷（2017） |
| **Pico-Union** | 1 | **0** | 0 | 无 | 没有骑手自述；但两条帖点名 **1842 W Washington Blvd 的 CloudKitchens（约 30 家餐厅）是各平台骑手扎堆等单的热点**（2018，"mostly Ubereats, postmates, grubhub, and doordash drivers there"） |

读法：

- **DTLA 是两轮送外卖被尝试最多的区**：29 帖，其他所有区加起来 51 帖，与层 B 的餐厅密度一致。但反证评审指出，这 29 帖里多数是"能不能骑车送"的提问，有经历的正面帖集中在 2018–2021，2020 之后每一条有经历的帖都在说没单或饱和（"太多 dasher 在线，一小时没单，天天如此"，2021）。所以 DTLA 是两轮骑手的入口，不是稳定的需求高地；这反而支持把店放在骑手被派往的方向（Koreatown / USC）上，而不是核心区深处。
- **Koreatown 在英文 Reddit 上几乎没有两轮骑手的声音（3 帖，全是问题或抱怨）**，Westlake 和 Pico-Union 是零。这不等于那里没有骑手，而是那里的骑手（西语移民为主）不在英文 Reddit 上说话。见 1.6。
- 骑手心里的"区"是 DoorDash 的 zone，不是行政区：**"Hollywood-Silverlake" 区包含 Koreatown，且经常把人派到 DTLA**。DTLA–Koreatown–Hollywood 这个三角在骑手眼里是一个作业区。
- 被点名的物理聚集点全是幽灵厨房：615 N Western Ave（Melrose Food Co，Koreatown 北缘）、1842 W Washington Blvd（CloudKitchens，Pico-Union / West Adams 交界）、358 W 38th St（Grand Food Depot，USC 南）、11419 Santa Monica Blvd（Colony，West LA）。一位 138 赞的骑手说"这些是我每天开工的起点，停在旁边马上有单，相当于 Uber 司机去机场排队"。

候选地址到这些聚集点的距离（英里）：

| 候选地址 | 615 N Western | 1842 W Washington | 358 W 38th |
|---|---|---|---|
| 768 Ceres | 4.9 | 3.1 | 2.5 |
| DTLA Historic Core（6th / Spring） | 4.2 | 2.8 | 2.7 |
| DTLA South Park（Pico / Flower） | 3.9 | 1.9 | 1.9 |
| Westlake（7th / Alvarado） | 2.6 | 1.8 | 2.9 |
| Pico-Union（Pico / Union） | 3.2 | **1.2** | 1.9 |
| Koreatown East（6th / Vermont） | 1.6 | 1.7 | 3.4 |
| Koreatown South（Olympic / Normandie） | 2.1 | **0.9** | 2.9 |
| Koreatown Core（Wilshire / Western） | 1.4 | 1.6 | 3.7 |
| USC（Figueroa / Jefferson） | 4.3 | 1.5 | 0.7 |

### 1.3 车型与产品规格（骑手原话）

| 车型 | LA 两轮骑手帖 | 骑手说什么 |
|---|---|---|
| E-bike | 19 | "至少 20–25 mph、续航 40–50 英里、取餐时好锁"（DTLA，2022）；"我的 e-bike 能跑 40+ mph、续航 40 英里，**App 里登记成汽车**以拿更多单"（2025）；"e-bike 爬坡轻松了，但一小时只有两单"（2024）；"LA 的 Ebike Dash 还能用吗？一周一单"（2025） |
| 站立式电动滑板车 | 13 | DTLA 从汽车换滑板车（1,172 赞）；Hollywood 独角兽单（71 赞）；西 Valley 5,500 单；Duffl 的 G30P "经常坏" |
| 摩托车 | 8 | "DoorDash 终于给了摩托车班次，而且优先给摩托车……摩托在 LA 比汽车快 20 倍"（2019） |
| 49cc 踏板车 / 轻便摩托 / Ruckus | 6 | Glendale 49cc 进城；Uber 导航把轻便摩托导上高速 |
| Sur-Ron / Talaria | **0** | 没有任何一条 LA 骑手帖提到用 Sur-Ron 送外卖 |
| 脚踏自行车 | 63（含询问） | 大量"骑车送单行不行"的新手提问；DTLA 坡、Silver Lake 坡、Hollywood Hills 坡是共同抱怨 |

对 HMP 的直接含义：(1) 骑手自己给出的规格就是 e-moped 级（20–25+ mph、40+ 英里），而且他们已经在把快车登记成"汽车"以拿单量和 Prop 22 里程补贴；(2) Grubhub 在 LA 报名时没有 e-bike 选项（2022），DoorDash 自行车模式在 DTLA "几乎没单"，怎么登记是骑手需要的服务；(3) 有明确的租赁需求信号：2023 r/ebikes "请推荐 LA 的 e-bike 租赁公司，用于送外卖不是自用"，2024 一位 DTLA 国际学生问买什么 e-bike 跑 DoorDash，2024 一位中文骑手在 r/ebikes / r/doordash 发了约 25 条 "Ubereats, Doordash, Grabhub Ebike Adventure Los Angeles" 第一视角视频。

### 1.4 骑手住哪、从哪来

有自述的：住 DTLA 送 DTLA（3 帖）；住 Koreatown（2 帖，其中一位女性骑手"几次不好的经历后不再夜间跑单"）；住 Thai Town / East Hollywood，远到 Santa Monica、Pico-Union、Pasadena、Burbank（16 赞）；Valley / NoHo / Burbank 边缘的骑手骑进 Hollywood / WeHo（5 帖）；Glendale 49cc 进 downtown；Pasadena 自行车骑手"一路骑到 Santa Monica 跑单"；Riverside 无车骑手计划公交 + 自行车到 DTLA。**没有任何帖描述一个西语 / 移民骑手社群、聚点或群组**，这是英文 Reddit 的盲区。

### 1.5 治安（骑手原话）

- 约 1,950 条 LA 校验帖里只有**一条第一人称的送餐两轮车被盗**（DTLA，DoorDash 骑手车胎被偷，2024，100 赞；帖子层漏掉、评论层补回）；其余是"想要好锁的车"这种预防性担忧，以及车里手机被偷。
- 暴力事件全是开车骑手：DTLA 取餐送到 West Adams 被 6 人从面包车里冲出来（2023，17 赞）；Olympic & Cochran 送酒被抢（2026，74 赞）；Skid Row 送单"第一要务是赶紧离开别被缠上"（2022）；"DTLA 停自行车道上的是垃圾人，害每个骑车送餐的"（2021）。
- 女性骑手在 Koreatown / Hollywood-Silverlake 区和 South LA 不跑夜单（2024）。
- 2019 年 349 赞的 r/LosAngeles 帖：LAPD 严查滑板车骑人行道，"K-town / DTLA 人行道骑行比马路骑行多 5 倍"。

### 1.6 收入（自报，未审计，多为税前）

| 区 / 车型 | 年份 | 数字 |
|---|---|---|
| DTLA 自行车 / 步行 | 2021 | Uber Eats 5–6 小时 $95–100（约 $16–20 / 小时）；DoorDash 同时长 $62.75（约 $10–12 / 小时） |
| Hollywood 电动滑板车 | 2019–20 | 挑单后"大赚"，峰时 $5 加价"全在滑板车上做" |
| Santa Monica e-bike | 2024 | Prop 22 保底约 $20–21 / 小时活跃时间（"缺点是骑手太多"；保底全州同规则，LA 市 2025 年 $21.44 + $0.35 / 英里） |
| West Hollywood 汽车 | 2024 | "通常 $18–30 / 小时"（53 赞） |
| Hollywood / WeHo 汽车（Grubhub） | 2021→2022 | 每天 8–9 小时 $200 → $120–150 → $50–70 |
| Santa Monica 区汽车 | 2024–25 | 5 小时 $15；7.5 小时 $14 |
| LA 峰时 | 2024 | "$8 / 小时" |

### 1.7 这层证据的局限

英文 Reddit 只覆盖说英语、会上 Reddit 的骑手，开车的占 97%；两轮帖 80 条里 29 条 DTLA，其余各区都 < 15，Koreatown 3、Westlake 0、Pico-Union 0，只能当轶事不能当比率；正面帖集中在 2019–21（饱和前）；Sur-Ron / e-moped 骑手在这些子版上几乎隐形，所以这层数据对 HMP 最核心的 e-moped 细分无法计数；子区粒度差（骑手只说 "DTLA"，几乎不说 Arts District / Fashion District / South Park），所以 DTLA 内部选点靠层 B–D。

### 1.8 评论级分析（37,225 条评论；7 个分区 / 主题读者 + 1 个反证读者）

抓取完成后语料为 7,764 帖 + 37,225 条评论，其中提到 LA 地名的 4,604 条。按区域和主题切成 28 个子集（`raw/reddit/reddit_subsets.py`），由 7 个读者分别通读并输出带原文引用的 JSON（`raw/reddit/analysis_comments/*.json`，每条引用都经脚本核对为原文），再由一个反证读者专门推翻第 0 节的结论（见 6.4）。

#### 1.8.1 加上评论后，各区的骑手声音

| 区域 | 文档数 | 两轮送单骑手自述 | 观察到他人两轮送单 | 汽车骑手 | 读者结论 |
|---|---|---|---|---|---|
| DTLA | 938 | 两轮语境 179 条；按车型：脚踏车 22、站立滑板车 11、e-bike 2、49cc 1、摩托 1（全 LA 口径，DTLA 占多数） | — | 多数 | 两轮送单被尝试最多的区，但 2020 后的亲历帖多为饱和 / 没单；自行车模式没单、scooter 模式有单但派得远（Koreatown / Silver Lake / USC） |
| Koreatown | 208 | 6（全是脚踏车，2018–2023，低分） | 10 | 8（另 8 条车型不明） | 骑手声音仍薄，但 19 位非骑手居民因停不了车而骑电动滑板车 / e-bike / Surron，是卫星点的 B2C 池 |
| Westlake / MacArthur Park | 11（另 10 条是 Westlake Village / TX 误匹配） | 0 | 0 | 2 | 无骑手事故报告；一位 2026 年开车骑手在 Home Depot Wilshire（Wilshire & Union）候单 |
| Pico-Union | 10 | 0 | 0 | 2 | 一位 2026 年开车骑手以 Pico-Union 为基地；三条房源广告说"街趴极难，建议骑车" |
| USC / Exposition | 104 | 2（研究生，计划中） | 7 | 6 | "LA 县骑自行车最多的地方之一"；学生小费 $1 但夜间单多 |
| Hollywood / East Hollywood | 740 | 10（7 条在 2018–21） | 22 | 174 | Hollywood-Silverlake 区单多、Hollywood-Beverly Hills 区"天天死"；偷车"100% 会发生" |
| West Hollywood | 265 | 3 | 9 | 74 | 平、小，但区死或饱和；夜间自行车信使被 LAPD 反复拦 |
| Silver Lake / Echo Park | 357 | 3 | 13 | 24 | 坡"比 SF 还陡"，脚踏车不可行，e-bike / 滑板车是唯一办法 |
| 西区五区合计（SM / Venice、Westwood、Culver、BH、Mid-City） | 1,540 | 10（5 脚踏车、2 e-bike、1 Duffl 车队、2 不明） | 8 | 约 156 | 211 条"两轮"文档 95% 是居民、通勤者、游客；两位 e-bike 骑手都靠 Prop 22 保底，且都说"骑手太多" |
| Valley / Glendale-Burbank / Pasadena / South Bay / Long Beach / East LA / South LA / SGV | 1,709 | 4 / 4 / 4 / 1 / 1 / 0 / 0 / 0 | — | 多数 | 外围两轮骑手几乎都朝核心区跑（Glendale 49cc → DTLA，Pasadena 自行车 → Santa Monica，Valley → Hollywood / WeHo） |

#### 1.8.2 评论层新增的、直接影响选址的事实

1. **语料里唯一被完整描述的候单路线，就在 v1 推荐的走廊上。** 一位 2026 年的 DoorDash 骑手（开车）："我待在 Pico-Union，不进高速环里的那个 downtown，不去 Vermont 以西；在 Home Depot（Wilshire & Union）和 7th St 的 Hammy's / Little Caesars 附近转就够了……0.9–1.5 英里的单能拿 $7.5。" 另一条评论独立证实 Home Depot Wilshire 是"downtown 上班族下单时段"的候单点。Home Depot Wilshire 离 South Park 18th St 1.6 英里、离 856 S Vermont 1.1 英里、离 7th & Alvarado 0.2 英里。
2. **DoorDash 2019 年的自行车热点是 6th & Spring（Historic Core）和 Westwood Blvd & Ohio。** 骑手仍然会在那里等单。这不改变主店选址，但意味着核心区需要一个"能锁车的点"（合作咖啡店 / 储物柜），而不是把核心区完全放弃。
3. **DTLA 自行车模式没单是高置信结论（8 条）**：骑手只能切 scooter 模式，单子会派到核心区外 3 英里（Koreatown、Silver Lake、USC）；Grubhub 2022 年报名只有汽车 / 摩托车两个选项；Uber 会把轻便摩托导上高速。这三条一起说明：HMP 的骑手会以 scooter / 摩托车模式接单，作业范围是 DTLA–Koreatown–USC 轴线，枢纽应在轴线上而不是核心区深处。
4. **Skid Row / 仓库区的描述全是负面且一致（10 条）**："Main St 以东是自行车荒漠，全是卡车"；被盗 e-bike 靠 AirTag 在 Skid Row 找回（2026）；"警察根本不来"（收容所保安，2026）；骑手送到 Skid Row 的第一要务是"赶紧离开"。没有任何两轮骑手在那一带候单或停车。但也没有任何一条点名 Ceres Ave 本身；否定 Ceres 的依据是邻近性，不是该地址的事故。
5. **纠正帖子层的结论：确实有第一人称的两轮送餐车被盗**——一位在 DTLA 跑 DoorDash 的骑手（住 South LA）车胎被偷（2024，100 赞）。Hollywood 的骑手说 e-bike 放公寓车库"100% 会被偷或被砸"，Koreatown 街上有"被拆件的自行车墙"。安全的室内停放 + 换电，是所有区都成立的产品需求。
6. **DoorDash 的 Hollywood-Silverlake 区包含 Koreatown 并会派到 DTLA（9 条，高置信）**；同一区里东半边（Silver Lake、Chinese Theatre 以东）单多，西半边（WeHo、The Grove、Beverly Hills）"天天死"。单量向东、向 Koreatown 倾斜，不支持 WeHo 选址。
7. **Koreatown 的骑行重心在 Wilshire / Western 到 Wilshire / Vermont 一带，而不是 Olympic / Vermont**（Critical Mass 从 Wilshire / Western 出发、Little Bangladesh 的滑板车通勤者、Wilshire / Normandie 的公交道执法）；Koreatown 没有自行车道、Wilshire 上人行道骑行罚 $200、2019 年手机信号差到 App 反复崩溃。
8. **East Hollywood（Vermont / Sunset 到 Western / Santa Monica）是卫星点的另一个候选**：Hollywood-Silverlake 区的地理枢纽，红线两站，Sunset 自行车道直达 DTLA（30 分钟），Western 上有幽灵厨房，被居民称为最适合无车生活的地段。反面：Hollywood 偷车最严重；Pico-Union 的骑手"不去 Vermont 以西"。
9. **幽灵厨房是汽车骑手的取餐磁石，不是两轮骑手的聚点**（"停好车马上有单"）。NoHo 的 Lankershim 幽灵厨房骑手多到把路中央停满、市政府装了护柱。它们是"骑手在哪"的证据，但要在那里做换电柜需要先实地看两轮比例。
10. **西区不是主店候选**：1,540 条文档里只有 10 条是骑两轮的骑手；两位 e-bike 骑手的理由是不用养车和 Prop 22 活跃时段保底（≈ $20–21 / 小时；反证读者指出这个保底全州同规则，LA 市 2025 年 $21.44 + $0.35 / 英里，并不偏向西区），且都说"骑手太多"；2023–2026 每个西区 zone 都崩（SM 7.5 小时 $14，BH / Westwood 2 小时 $5–7，Venice / MdR / Culver 8.5 小时 3 单）；西区骑手住西区、说东边"远"，没有人提到去 DTLA / Koreatown 的店。若将来开第三个点，应在 West LA（Sawtelle / Pico–Sepulveda / Westwood，靠 Colony 幽灵厨房、UCLA 和 E 线），不是 Santa Monica 市区。
11. **外围区域是骑手来源，不是选址对象**：Prop 22 的活跃时段保底在 LA 市内各处相同（2025 年 $21.44 / 小时 + $0.35 / 英里），区域间收入差异来自单密度和空转时间；外围两轮骑手朝核心区跑；一位 Pasadena 电动滑板车骑手因为 DoorDash 培训点在 25 英里外、没车而没法注册——**枢纽位置本身就是无车骑手的招募门槛**。
12. **骑手对"基地"的定义已经有人写出来了**：西 Valley 那位 5,500 单的滑板车骑手把商场旁的麦当劳叫"指挥中心"——插座、Wi-Fi、水、厕所、便宜零食，"理想的枢纽"。商家拒绝骑手用厕所是被反复提到的怨气（WeHo、Torrance、Crenshaw）。三位女性骑手（South LA、WeHo-BH-Hollywood、Koreatown）都说天黑后不跑，缺的是照明和有人的基地，不是单。
13. **车型**：LA 可见的电动送餐车是站立式滑板车（11 条自述）和脚踏车（22 条）；语料里没有任何一位在 28–40 mph 车上送单的第一人称骑手；但骑手的愿望清单正是这一档（"28 mph 的 e-bike 是甜点"，"至少 20–25 mph、40–50 英里续航、好锁"）；可拆电池和可带进室内是明确的购买标准；没有人提到换电或带备用电池；Wombi（Tern 载货 e-bike 月租 $135–175，面向家庭）是唯一被点名的租赁竞品，Whizz / Zoomo / Joco / Revel / HMP 零提及。
14. **执法**：LAPD 拦两轮骑手集中在 Beverly Hills / WeHo（夜间自行车信使一周被拦 3 次以上）；DTLA 对两轮几乎不执法（Surron 50 mph 无罚单）；Pasadena / Glendale 罚的是汽车。
15. **配送机器人**已在 DTLA、Koreatown（2026 年三位评论者提到短途送餐）、Hollywood / WeHo、Santa Monica / Westwood、Glendale 出现，直接吃掉最短的两轮单。

#### 1.8.3 评论层对 v1 的修正

| v1 说法 | 评论层结论 | 处理 |
|---|---|---|
| 主店放 Pico / Olympic 走廊 | **支持**：唯一的候单路线描述就在这里；Pico-Union 110 以西可免费停车；11th St 比 7th St 更适合骑行进出 | 保留 |
| 卫星点放 Koreatown 南 / 东（Olympic–6th & Vermont） | **部分修正**：Koreatown 骑行重心在 Wilshire 一线（Western 到 Vermont）；Home Depot Wilshire 是候单点；East Hollywood 的 Vermont / Sunset 是另一个自然枢纽 | 卫星点搜索范围改为 **Vermont 走廊（Olympic 到 Beverly）+ Wilshire（Vermont 到 Western）**，优先 Wilshire / Vermont 地铁站周边；East Hollywood 作为备选 |
| 不在 Historic Core 开店 | **部分支持**：骑手仍在 6th & Spring 等单，需要在核心区有一个能锁车的点 | 加一个"核心区合作锁车点"，不是门店 |
| 否定 768 Ceres | **支持**：Skid Row 边缘是被盗车的去处、"自行车荒漠"、无人候单；但没有针对该地址的事故 | 保留，措辞改为"邻近性风险" |
| 没有第一人称两轮被盗 | **纠正**：DTLA 有一起（车胎） | 已改 |
| Hollywood 两轮收入最好 | **降级**：证据是 2019–20 一位滑板车骑手的约 5 帖；2023–26 全是 $8 / 小时和"骑手太多" | 已改 |
| 西区 = Prop 22 经济学 | **部分确认**：西区 e-bike 的理由是省车费 + 接单保底，但保底全州同规则、LA 市反而更高，所以它不是西区优势；补充：西区开车骑手因停车 / 罚单想换 e-bike，是转化池；若开第三点应在 West LA 不是 Santa Monica | 已改 |
| 幽灵厨房是骑手聚点 | **修正**：是汽车骑手的取餐磁石 | 6.3 第 3 条改为"先实地数两轮比例" |

---

## 2. 餐厅覆盖：31 个候选地址（层 B，FACT + ASSUMPTION 权重）

方法：以候选点为圆心数半径 1 / 1.5 / 2 / 3 英里内的餐厅（DPH 清单，PE 含 RESTAURANT，按名称+地址去重，全县 28,059 家）。另算一个"两轮指数"：3 英里内每家餐厅乘所在区的两轮骑手占比（ASSUMPTION：DTLA 0.50、Westlake / Pico-Union 0.45、Hollywood 0.45、Koreatown 0.35、USC 0.30、其他 0.30）再乘距离衰减 exp(−d / 1.5 mi)。指数只用于排序，绝对值无意义。

| 候选地址（路口） | 1 mi | 1.5 mi | 2 mi | 3 mi | 两轮指数 | 1.5 mi 人口 | 1.5 mi 无车家庭 |
|---|---|---|---|---|---|---|---|
| DTLA Financial（7th / Figueroa） | 716 | **1,136** | 1,531 | 2,537 | **465** | 165k | 34% |
| DTLA Historic Core（6th / Spring） | **825** | 1,068 | 1,345 | 2,279 | 441 | 128k | 33% |
| Westlake / MacArthur Park（7th / Alvarado） | 333 | 1,014 | **1,736** | **2,746** | 416 | 222k | 28% |
| DTLA South Park（Pico / Flower） | 545 | 981 | 1,491 | 2,510 | 402 | 146k | 35% |
| Fashion District（9th / Santee） | 656 | 1,010 | 1,347 | 2,222 | 398 | 108k | 31% |
| Koreatown East（6th / Vermont） | 553 | 974 | 1,339 | 2,742 | 383 | **245k** | 26% |
| Little Tokyo（1st / Central） | 632 | 997 | 1,290 | 1,987 | 380 | 107k | 29% |
| Pico-Union（Pico / Union） | 275 | 929 | 1,661 | 2,702 | 379 | 182k | 31% |
| **768 Ceres Ave（基准）** | 547 | 975 | 1,217 | 2,022 | 344 | 87k | 31% |
| Koreatown South（Olympic / Normandie） | 591 | 922 | 1,190 | 2,537 | 336 | 215k | 25% |
| Koreatown Core（Wilshire / Western） | 536 | 859 | 1,161 | 2,476 | 326 | 191k | 21% |
| Arts District（Traction / Alameda） | 326 | 906 | 1,250 | 1,910 | 318 | 94k | 30% |
| Chinatown（Broadway / College） | 207 | 664 | 1,181 | 1,844 | 289 | 83k | 25% |
| Echo Park（Sunset / Echo Park Ave） | 170 | 293 | 805 | 2,504 | 282 | 111k | 18% |
| Hollywood（Hollywood / Vine） | 396 | 641 | 869 | 1,723 | 262 | 106k | 20% |
| USC / Exposition（Figueroa / Jefferson） | 195 | 411 | 868 | 2,223 | 255 | 128k | 25% |
| West Hollywood（Santa Monica / La Cienega） | 348 | 555 | 894 | 1,606 | 240 | 78k | 11% |
| East Hollywood（Sunset / Vermont） | 314 | 494 | 748 | 1,895 | 226 | 125k | 18% |
| Silver Lake（Sunset / Silver Lake Blvd） | 157 | 419 | 661 | 1,914 | 201 | 101k | 12% |
| Santa Monica（Wilshire / 4th） | 305 | 427 | 546 | 927 | 177 | 69k | 12% |
| Westwood（Westwood / Wilshire） | 204 | 462 | 658 | 1,074 | 150 | 103k | 12% |
| Boyle Heights（Cesar Chavez / Soto） | 143 | 298 | 662 | 1,467 | 171 | 100k | 15% |
| Mid-City（Pico / Fairfax） | 108 | 312 | 676 | 1,591 | 151 | 103k | 10% |
| Culver City（Venice / Culver） | 214 | 319 | 406 | 1,076 | 105 | 82k | 8% |
| Vernon 工业区（Vernon / Santa Fe） | 41 | 113 | 307 | 1,077 | 90 | 57k | 13% |

其余 6 个点（Lincoln Heights、Glendale、Historic South Central、Pasadena、Long Beach 等）见 `raw/market/site_coverage.csv`。Pasadena 和 Long Beach 有自己的卫生局，不在县清单里，数字为 0 不代表没餐厅。

读法：

- **1–1.5 英里（e-bike 顺路距离）DTLA 核心最密**：Financial District 1.5 英里 1,136 家，Historic Core 1 英里 825 家，是全 LA 最高的两个点。
- **2–3 英里（e-moped / 摩托距离）Westlake 反超**：7th / Alvarado 2 英里 1,736 家、3 英里 2,746 家，都是第一，因为它同时吃到 DTLA 和 Koreatown 两个团。Pico-Union（Pico / Union）同理，2 英里 1,661。
- **768 Ceres 在 1 英里内并不差（547，31 个点里第 7，高于 Pico 走廊的所有挂牌地址），从 1.5 英里开始掉队**：1.5 英里 975（第 9），2 英里 1,217（比 Westlake 少 30%），3 英里 2,022（比 Westlake 少 26%）。它在 Warehouse District 的东南角，东边和南边 1–2 英里是仓库和铁路，半个圆是空的。哪个半径重要，取决于骑手愿意为换电 / 维修绕多远：SF 的经验（客户从 SoMa / Mission / Tenderloin / FiDi 到店）说明 1–2 英里是可接受的，但这要用 HMP 自己的客户地址数据（`00-research-plan.md` D 节 P0-a）验证，本报告没有这份数据。
- **Koreatown 单点 1–1.5 英里并不比 DTLA 密**（Wilshire / Western 1.5 英里 859 家），但 1.5 英里内住着 19–25 万人、无车家庭 21–26%，是骑手居住地而不是接单地。

## 3. 两节点组合（层 B）

如果开两个点（一个主店 + 一个小服务点），哪两个点 2 英里覆盖并集最大：

| 组合 | 2 mi 并集餐厅 | 1.5 mi 并集 | 两轮指数 |
|---|---|---|---|
| Historic Core（6th / Spring）+ Koreatown East（6th / Vermont） | 2,450 | 2,015 | **609** |
| Financial（7th / Figueroa）+ Hollywood（Hollywood / Vine） | 2,400 | 1,777 | 603 |
| Financial + Koreatown East | **2,470** | 1,963 | 600 |
| Financial + Koreatown Core（Wilshire / Western） | 2,467 | 1,995 | 599 |
| Historic Core + Koreatown Core | 2,427 | 1,927 | 599 |
| Historic Core + Koreatown South（Olympic / Normandie） | 2,357 | 1,990 | 586 |
| Koreatown East + Little Tokyo | 2,517 | 1,971 | 577 |
| 768 Ceres + Koreatown East | 2,477 | — | 542 |
| 单点参考：Westlake（7th / Alvarado） | 1,736 | 1,014 | 416 |
| 单点参考：768 Ceres | 1,217 | 975 | 344 |

结论：**DTLA 核心 + Koreatown 东侧（Vermont 一带）两点 2 英里并集约 2,450 家，是 768 Ceres 单点的两倍，是 Westlake 单点的 1.4 倍**。Ceres + Koreatown East 的并集餐厅数（2,477）与 Financial + Koreatown East 差不多，但两轮指数低 10%，因为 Ceres 那一半覆盖的是东南工业区。

反证评审指出上表用的是路口坐标，推荐的具体挂牌地址没有算过并集。补算（`raw/market/listing_pairs.json`，按地理编码后的挂牌地址）：

| 主店 + 卫星点（具体地址） | 2 mi 并集 | 1.5 mi 并集 | 两点距离 |
|---|---|---|---|
| 18th St（Grand–Olive）+ **3651 Beverly Blvd** | **2,641** | 1,728 | 3.2 mi |
| 785 E 14th St + 3651 Beverly | 2,628 | 1,793 | 3.7 mi |
| **768 Ceres + 3651 Beverly** | **2,597** | 1,814 | 3.7 mi |
| 121 E 6th St（Historic Core）+ 3651 Beverly | 2,592 | 1,909 | 3.1 mi |
| 768 Ceres + Wilshire / Vermont（路口） | 2,477 | 1,948 | 3.3 mi |
| 18th St + Wilshire / Vermont（路口） | 2,443 | 1,806 | 2.5 mi |
| 18th St + 856 S Vermont | 2,281 | 1,769 | 2.1 mi |
| 1824 S Magnolia + 3651 Beverly | 2,276 | 1,417 | 2.4 mi |
| 2474 W Pico + 3651 Beverly | 2,029 | 1,376 | 2.0 mi |
| 2474 W Pico + 856 S Vermont | 1,555 | 1,091 | 0.7 mi |

三条读法：(1) **卫星点选 3651 Beverly（Vermont / Beverly）比 856 S Vermont 好**：并集多 360 家，抢劫 / 伤害只有后者的一半（57 / 85 vs 108 / 164），且离 Hollywood-Silverlake 区的幽灵厨房（615 N Western）1.3 英里。(2) **主店选 18th St 还是 Ceres，对两点并集影响不到 2%**（2,641 vs 2,597），因为两者都在 DTLA 南侧、离 Beverly 都是 3 英里多；差别在租金、Skid Row 邻近和地铁，不在覆盖。(3) 走廊西端（2474 W Pico、Magnolia）离 Koreatown 太近，与卫星点重叠大，只适合单点方案；走廊东端（18th St）适合两点方案。

---

## 4. 治安：候选地址周边的街头犯罪密度（层 C，FACT，有口径限制）

LAPD 公开数据，2023-01-01 至 2024-03-07（14.2 个月），只取四类：抢劫（210 + 220）、持械 / 严重伤害（230）、自行车被盗（480）、机动车被盗（510）。"× 全市"= 该半径内每平方英里每月的密度除以全市平均密度（全市抢劫 1.54 / sq mi / 月，伤害 2.23，自行车被盗 0.21）。Santa Monica、West Hollywood、Culver City、Pasadena、Glendale、Long Beach、Vernon 有自己的警局，不在表内。

| 候选地址 | 0.5 mi 抢劫 | 0.5 mi 伤害 | 0.5 mi 自行车被盗 | 抢劫密度 × 全市（0.5 mi） | 1 mi 抢劫 | 1 mi 伤害 | 抢劫密度 × 全市（1 mi） | 暴力案件夜间占比（1 mi） |
|---|---|---|---|---|---|---|---|---|
| Koreatown West（Wilshire / Crenshaw） | 13 | 11 | 0 | 0.8 | 100 | 112 | 1.5 | 47% |
| Silver Lake | 17 | 9 | 5 | 1.0 | 71 | 63 | 1.0 | 45% |
| Westwood | 17 | 24 | 14 | 1.0 | 39 | 60 | 0.6 | 39% |
| Mid-City（Pico / Fairfax） | 13 | 35 | 4 | 0.8 | 82 | 139 | 1.2 | 40% |
| Echo Park | 43 | 55 | 7 | 2.5 | 113 | 145 | 1.6 | 48% |
| Arts District | 43 | 80 | 12 | 2.5 | 401 | 759 | 5.8 | 38% |
| East Hollywood（Sunset / Vermont） | 58 | 74 | 2 | 3.4 | 161 | 203 | 2.3 | 46% |
| USC / Exposition | 60 | 80 | **136** | 3.5 | 217 | 333 | 3.2 | 38% |
| Pico-Union（Pico / Union） | 79 | 107 | 3 | 4.6 | 459 | 601 | 6.7 | 43% |
| Koreatown South（Olympic / Normandie） | 69 | 123 | 5 | 4.0 | 353 | 494 | 5.1 | 43% |
| Koreatown Core（Wilshire / Western） | 78 | 129 | 10 | 4.5 | 280 | 375 | 4.1 | 41% |
| DTLA South Park（Pico / Flower） | 140 | 174 | 34 | 8.2 | 625 | 738 | 9.1 | 41% |
| Fashion District（9th / Santee） | 151 | 180 | 12 | 8.8 | 854 | 1,152 | 12.4 | 39% |
| Hollywood（Hollywood / Vine） | 142 | 201 | 9 | 8.3 | 361 | 480 | 5.3 | 46% |
| Koreatown East（6th / Vermont） | 148 | 196 | 6 | 8.6 | 543 | 765 | 7.9 | 43% |
| **768 Ceres Ave** | 156 | **285** | 2 | 9.1 | 626 | 927 | 9.1 | 39% |
| Little Tokyo | 162 | 316 | 27 | 9.4 | 600 | 989 | 8.7 | 39% |
| DTLA Financial（7th / Figueroa） | 339 | 339 | 54 | 19.7 | 898 | 1,194 | 13.1 | 41% |
| Westlake / MacArthur Park（7th / Alvarado） | 334 | 449 | 14 | 19.4 | 701 | 895 | 10.2 | 42% |
| DTLA Historic Core（6th / Spring） | **431** | **662** | 39 | **25.1** | 819 | 1,146 | 11.9 | 39% |

读法与口径限制：

- 这是"每平方英里的案件数"，不是"每个在场的人的风险"。DTLA 核心白天有几十万人流，密度高一部分是人多。但对一个要放几十台车、晚上关门的门店来说，绝对密度才是它要面对的东西。
- **Historic Core（6th / Spring）和 Westlake（7th / Alvarado）是候选里最差的两个**：0.5 英里内抢劫 330–430 起 / 14 个月，是全市平均密度的 19–25 倍。6th / Spring 东边三个街区就是 Skid Row；7th / Alvarado 就是 MacArthur Park。
- **768 Ceres 是中上**：抢劫密度 9 倍全市，伤害 285 起（仅次于 Historic Core 和 Little Tokyo）。Ceres 所在的 7th / 8th & Ceres 离 Skid Row 中心（5th / San Pedro）约 0.6 英里。
- **Koreatown Core / South 是高覆盖候选里治安最好的一档**（抢劫 4–5 倍全市，伤害 120–130 起），Koreatown East（6th / Vermont）比 Core 差一倍，因为 6th / Vermont 往东 0.5 英里就进 Westlake。
- USC 自行车被盗 0.5 英里 136 起，是所有点的 3–10 倍（学生自行车）；对"存车"业务是负面，对"防盗 / 换车"需求是正面。
- 夜间占比各点差不多（38–48%），说明各区的昼夜风险结构类似，差别在总量。

---

## 5. 各区现在租得到什么（层 D，挂牌数据，2026-09-07 抓取）

来源限制：LoopNet / Showcase / CityFeet（CoStar 系）全部 403，所以下表缺了最大的一块库存；PropertyShark / CommercialCafe 的索引页把月租显示成真实值的 1/12（已在两处详情页验证），标"折算"的租金是索引值 × 12，需要向经纪确认；标"已验证"的来自详情页或 Craigslist 帖里的明确数字。HMP 的目标是约 4,000–8,000 sf、有卷帘门、月租一万以内。

| 区 | 地址 | 面积 sf | 月租（约） | $/sf/月 | 类型 | 车辆相关设施 | 状态 |
|---|---|---|---|---|---|---|---|
| DTLA South Park | 18th St（Grand 与 Olive 之间，帖内隐去门牌） | 7,644 | **$6,900** | $0.90 | 仓库 | 大卷帘门 + 装卸台、后巷、800A 三相电、12–14 ft 顶 | 已验证（Craigslist 2026-08-12） |
| Pico-Union | 1738 Cordova St（Budlong / Cordova，Pico 以南） | 5,000 | ~$9,900 | $1.98 NNN | 仓库 / 灵活 | 1 个平地门 + 1 个装卸台、全 HVAC | 已验证（详情页） |
| Koreatown | 856 S Vermont Ave（Vermont / 8th） | 3,549 | ~$9,760 | $2.75 NNN | 临街零售 | 15 个车位；卷帘门未说明 | 已验证（详情页） |
| Koreatown 北 / East Hollywood | 3651 Beverly Blvd（Beverly / Vermont） | 4,434 | 面议 | — | 独栋灵活 / 工业 | 独栋单租户 | 索引 |
| Westlake | 710 S Alvarado St（7th / Alvarado，Langer's 旁） | 14,200 | 面议 | — | 多用途商业 | HVAC、喷淋、3 车围栏停车；现为摊位布局 | Craigslist |
| Westlake | 1900 Beverly Blvd | 2,000 | ~$4,100 | $2.04 折算 | 临街 | 未说明 | 索引 |
| Pico-Union | 2474 W Pico Blvd（Pico / Vermont） | 4,100 | 面议 | — | 临街 | 未说明 | 索引 |
| Pico-Union | 1824 S Magnolia Ave | 7,515 | ~$14,400 | $1.92 折算 | 仓库 | 未说明 | 索引 |
| Historic Core | 525 S Los Angeles St（Toy District） | 2,600 | $5,200 | $2.00 | 临街 | 无 | 已验证（Craigslist） |
| Historic Core | 121–129 E 6th St（Santa Fe Lofts 商铺） | 3,840 | ~$4,150 | $1.08 折算 | 临街 | 无 | 索引 |
| Fashion District | 726 E 12th St | 5,765 | ~$7,200 | $1.25–2.25 | 商铺 / 展厅 | 未说明 | 索引（数值本身合理） |
| Fashion District | 951 Crocker St | 4,380 | ~$5,000 | $1.15 | 商业 loft | 未说明；Crocker 在 Skid Row 南缘 | 索引 |
| Warehouse District | 785 E 14th St / 796 E 14th Pl（离 Ceres 6 个街区） | 4,160 / 3,820 | ~$5,200 / 面议 | $1.26 | 仓库 | 未说明 | 索引 |
| Arts District 南 | 2473 Hunter St（Hunter / Santa Fe） | 5,450 | $7,500 | $1.38 | 仓库 | 14 ft 顶、装卸台、A/C | 已验证（Craigslist） |
| Boyle Heights（后场） | 1312 S Boyle Ave | 3,612 | ~$4,800 | $1.32 折算 | 仓库 | 未说明 | 索引 |
| Boyle Heights（后场） | 2832 E Olympic Blvd | 4,141 | ~$6,200 | $1.50 折算 | 临街仓库 | 未说明 | 索引 |
| Boyle Heights（后场） | 159 S Anderson St | 9,476 | ~$10,900 | $1.15 gross | 仓库 | 未说明 | 标题已注明 |
| Central-Alameda（后场） | 1350 E 41st St | 5,232 | ~$4,700 | $0.90 | 仓库 | 未说明 | 索引（标注疑似错位） |
| Lincoln Heights（后场） | 2440 Daly St | 3,778 | ~$5,900 | $1.56 折算 | 仓库 | 未说明 | 索引 |
| Vernon（后场） | 2960 Leonis Blvd | 9,276 | ~$8,900 | $0.96 折算 | 仓库 | 未说明 | 索引 |

市场行情（Q2 2026，经纪报告）：LA 工业 $1.17–1.37 NNN 且连续 12 个季度下降；Koreatown 临街零售 $2.52–3.95；DTLA 底商 $1.08–2.25；Boyle Heights 工业 $1.15–1.92。全部 60 条挂牌见 `raw/market/listings.json`。

读法：

- **Koreatown 临街是最贵的一档（$2.5–4 / sf），一万预算只能租 2,500–4,000 sf，而且几乎没有卷帘门**。Koreatown 更适合做小服务点（换电 + 小修 + 提车），不适合做仓储主店。
- **Pico-Union / South Park 南段是"离 DTLA 和 Koreatown 都近、有卷帘门、一万以内"的交集**：18th St（South Park）7,644 sf $6,900 和 1738 Cordova 5,000 sf $9,900 是目前找到的最好的两个主店候选。
- Westlake 几乎没有合适库存（710 S Alvarado 太大且是摊位格局），这一区的挂牌需要经纪去挖。
- 768 Ceres 的 $10,000 / 8,443 sf = $1.18 / sf，在工业行情里是中位价，不便宜也不贵；同区 6 个街区外有 4,000 sf 级的 $1.26 单位。

---

## 6. 综合排序与推荐

### 6.1 三层证据各说什么

| | 层 A 骑手自述 | 层 B 餐厅覆盖 | 层 C 治安 | 层 D 场地 |
|---|---|---|---|---|
| 指向 | DTLA 核心（29 帖）；Hollywood-Silverlake 区（含 Koreatown）有单量；聚点在幽灵厨房（Pico-Union / West Adams、Koreatown 北、USC 南） | 1–1.5 英里 DTLA Financial / Historic Core 最密；2–3 英里 Westlake / Pico-Union 最广；两点 DTLA + Koreatown 并集最大 | Historic Core、Westlake、Financial 最差（19–25 倍全市）；Koreatown Core / South、Pico-Union、South Park 中等（4–8 倍）；Boyle Heights 最好 | 一万以内带卷帘门的只在 South Park 南段、Pico-Union、Warehouse District、Boyle Heights；Koreatown 临街 $2.5–4 且无卷帘门 |
| 一致 | 都说 DTLA 是需求中心，Koreatown 是第二中心 | | | |
| 冲突 | 骑手最常点名的 6th & Spring，恰好是治安最差、场地最不合适的点；覆盖最广的 7th & Alvarado 同样治安最差且无合适挂牌 | | | |

把冲突处理掉的办法是往 DTLA 核心的西南方向退 1–1.5 英里：到 Pico / Olympic 走廊后，2 英里圈仍能装下 Historic Core、Financial District 和 Koreatown 南部，犯罪密度降到核心区的三分之一，租金降到工业价，而且 Figueroa 的保护式自行车道（7th St 到 Exposition）正好把 DTLA 核心、这一格和 USC 串起来。

### 6.2 候选点打分（0–10，初步；Task 6 会用 HMP 数据和实地踏勘重做）

权重是 ASSUMPTION：骑手可达 35%、治安 20%、租金 15%、通勤便利 15%、运营条件 15%。骑手可达综合层 A + B（2 英里餐厅、到骑手聚点的距离、是否有骑手声音）；治安用层 C 半英里数字；租金用层 D 的 $/sf 和总额；通勤看地铁 / 自行车道 / 公交；运营看面积、卷帘门、装卸、电力、停车。

治安分同时看半英里和 0.25 英里（街区级）的抢劫 / 伤害，以及自行车被盗；骑手可达分以 2–3 英里覆盖为主（骑手作业半径），另算一个以 1 英里为主的"walk-in 变体"，因为反证评审指出走廊在 1 英里内最稀。

| 候选（具体挂牌） | 骑手可达 | 治安 | 租金 | 通勤 | 运营 | **加权** | 备注（抢劫 / 伤害：半英里；括号内 0.25 英里） |
|---|---|---|---|---|---|---|---|
| **South Park 南段：18th St（Grand–Olive），7,644 sf** | 7 | 5 | 9 | 7 | 8 | **7.1** | 1 / 2 / 3 英里 370 / 1,410 / 2,435；Pico Station 0.4 英里；$6,900 但广告匿名、面积前后不一（8,744 vs 7,644）、低于市价，**必须先核实**；96 / 122（20 / 35）；半英里自行车被盗 19 起，但都在 Pico / Flower 一带的高层车库，街区内 1 起 |
| **Koreatown 北缘：3651 Beverly Blvd，4,434 sf 独栋灵活** | 7 | 7 | 5 | 7 | 6 | **6.6** | 236 / 1,401 / 2,588；所有中心候选里最安全（57 / 85；24 / 41）；Vermont / Beverly 红线站 0.3 英里；离 615 N Western 幽灵厨房 1.3 英里；面议；既可做卫星点也可做面向骑手的主店 |
| Pico-Union 西段：1738 Cordova St，5,000 sf | 6 | 8 | 5 | 6 | 7 | 6.4 | 214 / 1,206 / 2,331；前台点里治安最好（50 / 83；10 / 14）；$1.98 NNN 偏贵；2 英里覆盖最低 |
| Pico-Union：1824 S Magnolia Ave，7,515 sf 仓库 | 7 | 7 | 3 | 5 | 8 | 6.3 | 213 / 1,521 / 2,563（走廊里 2 英里最高）；68 / 104（14 / 26）；折算租金 ~$14,400 超预算，若索引页数字本身就是月租则便宜一半，待核 |
| Pico-Union：2474 W Pico Blvd（Pico / Vermont），4,100 sf | 7 | 6 | 5 | 6 | 5 | 6.1 | 322 / 1,435 / 2,591；78 / 119（23 / 51）；离 1842 W Washington 幽灵厨房 0.7 英里；面议；后门 / 卷帘门未知 |
| Koreatown：856 S Vermont Ave，3,549 sf | 8 | 5 | 3 | 8 | 4 | 6.1 | 572 / 1,342 / 2,680（3 英里最高）；108 / 164（34 / 56）；Wilshire / Vermont 站 0.5 英里；无卷帘门，$2.75 NNN，只能做卫星点 |
| Boyle Heights（后场）：159 S Anderson St，9,476 sf | 4 | 8 | 7 | 5 | 7 | 5.9 | 22 / 44（8 / 21）最安全；$1.15 gross；没有骑手会顺路来 |
| Warehouse District 南：785 E 14th St，4,160 sf | 5 | 5 | 8 | 4 | 6 | 5.5 | 339 / 1,260 / 2,030；106 / 102（24 / 14）；~$5,242（索引标注疑似错位，待核）；离 Ceres 6 个街区，说明仓库区内部治安是逐街区变化的 |
| Historic Core：121 E 6th St / 525 S Los Angeles St | 8 | 1 | 5 | 8 | 2 | 5.3 | 1 英里 831 / 824，全 LA 最密；骑手点名的 6th & Spring 就在旁边；但 418 / 677（178 / 267），自行车被盗 35，无卷帘门 |
| Westlake：710 S Alvarado St，14,200 sf | 8 | 1 | 3 | 8 | 4 | 5.3 | 2 英里 1,793 最广；345 / 462（93 / 132）；摊位格局、面积过大 |
| **768 Ceres Ave，8,443 sf** | 5 | 4 | 5 | 4 | 8 | **5.1** | 544 / 1,217 / 2,022（1 英里高于走廊各点）；156 / 285（27 / 51）——半英里数字被 Skid Row 南端抬高，街区级与走廊相当；自行车被盗 2；无地铁；"Main St 以东是自行车荒漠" |

敏感性（`raw/market/site_scores.json`）：治安 10% / 可达 45%：18th St 7.3，Beverly 6.6，856 Vermont 6.4，Magnolia 6.3，Ceres 5.2。治安 30% / 租金 5%：**Beverly 第一（6.8）**，Cordova 6.7，18th St 6.7，Magnolia 6.7，Ceres 5.0。五项等权：18th St 7.2，Cordova / Beverly 6.4，Ceres 5.2。**以 1 英里覆盖为主的 walk-in 变体：18th St 6.4，856 Vermont 6.1，Historic Core 6.0，Beverly / Anderson 5.9，Ceres 5.8，Cordova 5.7**——在这个变体下 Ceres 与走廊各点只差 0.5 分，说明"Ceres 不如走廊"这个结论依赖于"骑手愿意为服务绕 1–2 英里"这个假设。去掉 18th St 未核实的租金优势（租金分改成 5），它的加权降到 6.5，与 Beverly、Cordova、Magnolia 并列。

### 6.3 推荐

1. **单点方案：主店放 Pico / Olympic 走廊（邮编 90015 / 90007 / 90006，Pico–Washington，Figueroa–Vermont）。** 三个现成候选：18th St（Grand–Olive）7,644 sf $6,900（比 Ceres 便宜 $3,100 / 月、2 英里多覆盖 16%、半英里抢劫少 40%，但 1 英里内比 Ceres 少 32%，且广告匿名、面积前后不一、低于市价，**先实地核实再算数**）；2474 W Pico（Pico / Vermont）4,100 sf 面议（2–3 英里覆盖和治安都优于 18th St，离 1842 W Washington 幽灵厨房 0.7 英里，在 Pico-Union 骑手"不进高速环"的活动范围内）；1824 S Magnolia 7,515 sf 仓库（走廊里 2 英里覆盖最高、治安第二好，租金待核）。同格里还有 1508–1530 W Pico（2,550 sf）、1419 W Pico（1,100 sf）、1600 S Broadway（3,200 sf）、122 E Pico（1,100 sf）可做小店备选。
2. **两点方案：主店放走廊东端（18th St 一类），卫星点放 Koreatown 北缘的 Vermont / Beverly 到 Wilshire / Vermont–Western 一线（邮编 90004 / 90005 / 90010 / 90020），红线站周边，1,500–4,500 sf，做换电 + 小修 + 试骑 + 交车。** 首选 3651 Beverly Blvd（4,434 sf 独栋灵活，所有中心候选里抢劫 / 伤害最低 57 / 85，Vermont / Beverly 红线站 0.3 英里，离 615 N Western 幽灵厨房 1.3 英里）：与 18th St 的 2 英里并集 2,641 家，是所有组合里最高的；856 S Vermont（3,549 sf，15 车位，Wilshire / Vermont 站 0.5 英里）覆盖相近但并集少 360 家、治安差一倍、租金更贵，退为备选。East Hollywood 的 Vermont / Sunset（红线站、Sunset 自行车道直达 DTLA）是第三备选，代价是 Hollywood 的偷车率和离 Pico-Union 骑手的活动边界（"不去 Vermont 以西"）更远。治安提醒：Vermont 走廊越往南、越靠 Westlake 越差（6th / Vermont 半英里抢劫 148，Wilshire / Western 78，Beverly / Vermont 57）。
3. **核心区不开店，但要有一个能锁车的点。** DoorDash 的自行车热点在 6th & Spring，骑手会在那里等单；跟一家咖啡店 / 停车场谈几个带监控的锁车位（或一个换电柜），比在 Historic Core 租店便宜且规避治安问题。
4. **幽灵厨房是汽车骑手的取餐磁石（"停好车马上有单"），不是两轮骑手的聚点。** 1842 W Washington Blvd（CloudKitchens，约 30 家餐厅）、615 N Western Ave（Melrose Food Co）、358 W 38th St（Grand Food Depot）值得去数一数两轮比例；如果两轮骑手确实在那里取餐，一个换电柜 + 每周固定时段的移动维修，比第二个门店便宜一个数量级。先数人再谈合作（见第 8 节）。
5. **不建议把主店放在 Historic Core 或 Westlake 7th & Alvarado**，尽管它们分别是骑手点名的热点和覆盖最广的点：半英里抢劫 330–430 起 / 14 个月，是 South Park 南段的 3.5–4.5 倍，对一个存放几十台车、需要夜间安全的门店是硬伤；而且两处都没有带卷帘门、一万以内的挂牌。Reddit 上没有骑手在 MacArthur Park 遇袭的报告，也没有人抱怨 Home Depot Wilshire 候单不安全，所以这一条的依据是 LAPD 密度，不是骑手自述。
6. **不建议 Arts District 做主店**（临街 $3.75，2 英里覆盖 1,250 且一半是河和铁路）；**Boyle Heights / Central-Alameda / Vernon 只做后场**（安全、便宜，但没有骑手会顺路来）；**西区现在不开**，将来若开第三点放 West LA（Sawtelle / Westwood）而不是 Santa Monica。

给经纪的搜索指令（按优先级）：(a) 90015 / 90007 内 Pico 到 Washington、Figueroa 到 Hoover，4,000–8,000 sf 工业或灵活空间，卷帘门，月租 ≤ $9,000；(b) 90006 内 Pico 到 Venice、Vermont 到 Normandie，同上；(c) 90005 / 90010 / 90020 内 Vermont 走廊 Olympic 到 Beverly、Wilshire 走廊 Vermont 到 Western，1,500–3,500 sf 临街，有后门或停车场，优先 Wilshire / Vermont 站 0.5 英里内；(d) 只在 (a)(b) 找不到时看 Warehouse District（含 768 Ceres）和 Boyle Heights，并同时找 (c)。

### 6.4 反证评审：一个读者专门推翻上面的结论，结果如何

让一个读者只做一件事：用同一份语料和地理数据推翻第 0 节的六条主张（`raw/reddit/analysis_comments/adversarial.json`）。结论和处理：

| 主张 | 反证读者的判定 | 反证要点 | 本报告的处理 |
|---|---|---|---|
| C1 主店放 Pico / Olympic 走廊（18th St） | **被削弱（反证强）** | 走廊在 1–1.5 英里最稀（18th St 370 家，Ceres 544，Historic Core 830）；走廊内 2474 W Pico 和 1824 Magnolia 在 2–3 英里覆盖和所有治安指标上都优于 18th St；18th St 半英里自行车被盗 19 起；"犯罪密度是核心区的三分之一"只是和最差的两个点比，对全市仍是 5.6 倍；语料里没有任何骑手提到这条走廊；唯一的 Pico-Union 骑手"不进高速环"，而 18th & Grand 在环内；整个推荐押在一条匿名、低于市价、面积前后不一的 Craigslist 广告上 | 接受：第 0 节改为"走廊 + 三个候选地址"，18th St 标为"待核实"；自行车被盗 19 起查过，集中在 Pico / Flower 高层车库，街区内 1 起，已注明；1 英里稀是真实代价，明确写为"押在骑手愿绕 1–2 英里"这个待验证假设上 |
| C2 卫星点 856 S Vermont，两点并集 2,450 | **被削弱（中）** | 2,450 是 Historic Core + Ktown East 的路口并集，推荐的具体地址对没算过；856 S Vermont 比主店贵、抢劫比 18th St 高、无卷帘门；3651 Beverly 在治安和成本上都更好；Koreatown 骑手文本是混合的（无自行车道、午间无单） | 接受：补算了挂牌地址级并集（第 3 节），卫星点首选改为 3651 Beverly（并集 2,641） |
| C3 768 Ceres 在每个骑手可达指标上都更差 | **被削弱（中）** | Ceres 在 1 英里（+47%）和 1.5 英里都胜过 18th St，自行车被盗最少（2）；半英里犯罪数字被 Skid Row 南端抬高，6 个街区外的 785 E 14th 与 18th St 无异；Ceres + Ktown East 并集 2,477 > 2,450；没有骑手点名 Ceres 或仓库区 | 接受一半："每个指标都差"改为"1 英里内不差，1.5 英里外掉队；街区级治安与走廊相当，半英里内因 Skid Row 邻近更差"；"Ceres 仓库 + Beverly 前台"（2,597）写为可行的第二配置 |
| C4 不在 Historic Core / Westlake 开主店 | **成立（反证弱）** | 犯罪数字真实且有骑手被盗佐证；但报告低估了放弃的覆盖（121 E 6th 1 英里 831，是 18th St 的 2.2 倍）；"没有卷帘门库存"只是 60 条挂牌、5 条核实的结果，应写成"没找到" | 接受措辞修正："没有"改为"没找到"；加了核心区锁车点 |
| C5 DTLA 是唯一"两轮正常"的区；Hollywood-Silverlake 有量；西区靠 Prop 22 | **被削弱（反证强）** | DTLA 29 帖里多数是"能不能骑车送"的提问；有经历的正面帖都在 2018–21，2020 后每一条有经历的帖都说没单；1,172 赞的帖没有正文，帖内唯一的自行车骑手说 DTLA 饱和、建议去 K-town / Hollywood；Prop 22 保底是全州规则、LA 市反而更高，不是西区优势；语料混入 Surrey BC、Westlake TX、Normandy 法国 | 接受：1.2 和 1.8 的 DTLA 表述改为"两轮送单被尝试最多的区，2020 后的亲历帖多为饱和"；Prop 22 已改；非 LA 泄漏已在第 8 节注明（各读者在通读时已剔除） |
| C6 骑手规格 = e-moped 级；自行车模式没单；幽灵厨房是聚点 | **被削弱（中）** | 规格证据 n=2；真正跑出量的骑手用站立滑板车 + 公交；2024 一位 e-bike vs 轻便摩托的帖列出停车、保险、考试、注册作为不选摩托级的理由；自行车模式没单成立，但派单半径远超 1–2 英里，反而支持把店放在长单去的环上；所有幽灵厨房证据都是开车骑手 | 接受：1.3 和 1.8 已注明 28–40 mph 无第一人称骑手；幽灵厨房改为"汽车骑手取餐磁石，需实地数两轮比例"；派单半径远的事实与"走廊而非核心区"一致，保留 |

反证读者的总评："18th St 没有被推翻，但比报告呈现的弱：它的地理数据只在 2 英里圈上成立；最大的弱点是整个方案押在一条未核实的广告和一个没算过的并集上，而同一批文件里有更容易辩护的替代方案（Ceres + Beverly，2,477）。" 补算后 18th St + Beverly（2,641）确实高于 Ceres + Beverly（2,597），但差距只有 2%；所以两点方案里主店的选择应由租金、Skid Row 邻近、地铁和实地核实决定，而不是由覆盖数字决定。

## 7. 768 Ceres 在这个标准下的位置

| 指标 | 768 Ceres | South Park 18th St | Pico-Union 2474 W Pico | Koreatown N 3651 Beverly | Ceres 排名（11 个打分点） |
|---|---|---|---|---|---|
| 1 英里餐厅 | **544** | 370 | 322 | 236 | 2（仅次于 Historic Core 和 856 S Vermont） |
| 1.5 英里餐厅 | 974 | 888 | 866 | 840 | 4 |
| 2 英里餐厅 | 1,217 | 1,410 | 1,435 | 1,401 | 8 |
| 3 英里餐厅 | 2,022 | 2,435 | 2,591 | 2,588 | 10 |
| 半英里抢劫 / 伤害（14 个月） | 156 / 285 | 96 / 122 | 78 / 119 | 57 / 85 | 8 / 9 |
| 0.25 英里抢劫 / 伤害（街区级） | 27 / 51 | 20 / 35 | 23 / 51 | 24 / 41 | 与走廊相当 |
| 半英里自行车被盗 | **2** | 19（高层车库） | 4 | 7 | 最少 |
| 到候单点最近距离（Home Depot Wilshire / 幽灵厨房） | 2.1 / 2.5 mi | 1.6 / 1.9 mi | 1.3 / 0.7 mi | 1.7 / 1.3 mi | 最远 |
| Reddit 骑手提到本街区 | 0（Skid Row 全负面："自行车荒漠"、被盗车在此找回、"警察不来"） | 0 | 0（Pico-Union 候单路线 1 条） | 0（615 N Western 幽灵厨房 3 条） | — |
| 地铁站 | 无（最近 Pico Station 1.3 mi） | Pico Station 0.4 mi | Wilshire / Vermont 1.1 mi | Vermont / Beverly 0.3 mi | 最差 |
| 面积 / 月租 / $ per sf | 8,443 / $10,000 / $1.18 | 7,644 / $6,900（待核）/ $0.90 | 4,100 / 面议 | 4,434 / 面议 | 面积最大 |
| 1.5 英里人口 / 无车家庭 | 87k / 31% | 146k / 35% | 190k / 28% | 200k / 20% | 最低 |
| 两点并集（+ 3651 Beverly，2 mi） | 2,597 | 2,641 | 2,029 | — | 差 2% |

经反证评审后对 Ceres 的公平评价：

- **它不是"每个指标都差"。** 1 英里内它是所有可租地址里第二密的（544），自行车被盗最少，街区级（0.25 英里）抢劫 / 伤害与走廊各点相当，做两点方案时与最优主店的并集只差 2%。
- **它的真实问题有四个**：(1) 从 1.5 英里开始掉队，因为东、南半圆是仓库、铁路和 Vernon；(2) 半英里内的犯罪密度被 Skid Row 南端抬高——这不是统计假象，骑手往西北进出都要穿过或贴着 Skid Row，Reddit 上对这一带的描述全是负面（"Main St 以东是自行车荒漠"、被盗 e-bike 靠 AirTag 在 Skid Row 找回、"警察根本不来"、"赶紧离开"）；(3) 没有地铁，骑手的居住地（Koreatown、Westlake、Pico-Union）和候单点全在它西北 2–5 英里外；(4) 比走廊的仓库贵 $3,100 / 月（如果 18th St 的广告是真的）。
- **结论不变但措辞收窄**：Ceres 不适合做唯一的面向骑手的门店；作为"仓库 + Koreatown 北缘前台点"的后场是可行的第二配置。第一份报告（`00-research-plan.md`）把"Ceres 单点能够到的两轮骑手不多"列为最危险的假设之一，本报告的结论是这个风险可以通过换地址或加一个前台点来消除，不需要换城市。

## 8. 数据局限与下一步

局限：

1. **Reddit 是英文、开车骑手的世界**：3,095 条 LA 帖里两轮骑手 80 条；加上评论后 Koreatown 6 条（全是脚踏车）、Westlake 0、Pico-Union 0。这三区的骑手（大量为西语移民、骑 e-bike / 踏板摩托）不在英文 Reddit 上，所以层 A 对 Koreatown 系统性低估，对 DTLA 系统性高估。层 B（餐厅）和 C（犯罪）不受这个偏差影响。
2. **时间偏差**：DTLA 两轮送单的正面亲历帖集中在 2018–2021（疫情单量高峰、Prop 22 之前），2020 后每一条有经历的 DTLA 两轮帖都在说没单或饱和；本报告把 DTLA 描述为"两轮送单被尝试最多的区"，不是"需求最旺的区"。这一点同样影响 `03-market-size.md` 里 DTLA 的两轮占比假设（0.50），应下调重跑。
3. **Sur-Ron / e-moped 骑手在语料里是零**，层 A 无法为 HMP 最核心的车型细分提供区域信号；28–40 mph 的"骑手规格"是愿望清单（n≈3），不是使用记录。
4. **语料有非 LA 泄漏**：地名正则把 Surrey BC、Roanoke / Westlake（TX）、Normandy（法国，匹配 "Normandie"）、Toronto、Phoenix 等混进了 `corpus_la.jsonl`；帖子层分析和各读者在通读时逐条剔除了（Westlake 21 条里剔了 10 条），但 1.2 的自动统计表（`reddit_tally.json`）没有剔，2–5 条量级的区域计数在噪声以内。
5. **犯罪数据**是 2023-01 到 2024-03 的密度，不是人均风险；LAPD 2024-03 换系统后数据不全，所以看不到 Historic Core 近两年是否变好；半英里圆会被相邻热点（Skid Row）抬高，所以第 6 节同时给了 0.25 英里；没有覆盖 Santa Monica、WeHo、Culver、Pasadena 等有独立警局的城市。
6. **挂牌**缺了 CoStar 系（LoopNet 等）库存，索引页租金要 × 12 修正，60 条里只有 856 S Vermont、1738 Cordova、2473 Hunter、525 S Los Angeles 四处租金是从详情页或明确报价核实的；**18th St 的 $6,900 来自一条匿名 Craigslist 广告，标题 8,744 sf、正文 7,644 sf、单价低于市场，未核实**；"Historic Core 没有卷帘门库存"应读作"没找到"。
7. **两轮指数和打分权重是 ASSUMPTION**（`site_coverage.py` 的 `TW_SHARE_BY_AREA`、`site_scores.json` 的分数），Ceres 与走廊的排名在"以 1 英里为主"的变体下只差 0.5 分。
8. 餐厅覆盖用的是直线距离，不是骑行时间；对 e-moped 影响不大，对 e-bike 在有坡的方向（Bunker Hill、Silver Lake）会高估。
9. **没有 HMP 自己的数据**：客户到店距离衰减（P0-a）是决定"1 英里 vs 2–3 英里哪个重要"的关键，本报告只能假设 SF 的 1–2 英里经验可迁移。

下一步（都在 `00-research-plan.md` 的 8 项租前测试之内，这里只列跟选址直接相关的）：

1. **实地数骑手（两天，每天午晚各一小时）**：1842 W Washington Blvd、615 N Western Ave、358 W 38th St 三个幽灵厨房门口 + 6th & Spring + Pico / Vermont，记车型（e-bike / e-moped / 摩托 / 站立滑板车 / 汽车）。这是唯一能校正层 A 偏差的办法，成本几乎为零。
2. 拿到实地数据后把 `site_coverage.py` 的 `TW_SHARE_BY_AREA` 权重替换成实测比例，重跑覆盖和两点组合。
3. 让经纪按 6.3 的搜索指令拉 CoStar 库存，重点是 90015 / 90007 / 90006 三个邮编。
4. 用 HMP SF 的客户地址数据（`00-research-plan.md` D 节 P0-a）验证"客户到店距离衰减"，决定卫星点是否必要。
