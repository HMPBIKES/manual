# Whizz LA 落地页调查 & HMP 洛杉矶选址报告
**Whizz LA Landing Page Investigation & HMP Site Search ($5,000/mo Industrial)**

- 调研日期:2026 年 8 月 14 日
- 方法:8 个并行研究智能体(Wayback Machine 档案取证、公司注册记录、新闻/招聘核查、同行选址测绘、工业地产行情、在租房源扫描、合规研究),关键结论经独立验证智能体复核
- 用途:HMP 计划在 LA 开设 industrial 门店,推出 FLASH / Lightning / INNO 租赁 + 换电 + 充电,预算 $5,000/月

---

## 第一部分:Whizz 为什么有 LA 落地页却没有门店?

### 直接答案

**这是一个纯 SEO 获客页,Whizz 从未在 LA 运营过,也没有"开了又撤"——LA 店从未存在过。**

### 落地页是什么时候做的?

- Wayback Machine 首次快照:**2025 年 3 月 22 日 21:39 UTC**(全档案仅两次快照:2025-03-22 和 2025-11-11,之前之后都没有)。实际上线时间应在 2025 年 Q1。
- 它是**同一晚批量上线的模板页之一**:姊妹页 `/cities/deliver/chicago` 首次快照在 47 分钟后(同晚 22:26 UTC)。同模板的 `$139/mo` 页面还有 **Miami、Seattle、Houston——全部是 Whizz 没有开店的城市**,都推同一个字面意义上叫 "GEO" 的促销码。这是典型的程序化 geo-SEO 打法:先收割各城市骑手的搜索流量、攒注册名单,为未来扩张探路。
- **现状:该项目已被废弃。** `/cities/deliver/*` 已从 Whizz 的 sitemap 移除,今天访问该 URL 只返回一个空的 Nuxt 应用壳(soft-404,标题 "Whizz Personal Account"),服务端不再输出任何 LA 内容。Google 索引里残留的旧标题 "Get the best delivery e-bike in Los Angeles from $139/mo" 是滞后的"孤儿页"痕迹。

### 为什么确定 LA 从未运营过?(证据链)

1. **Whizz 自己的运营 API**(`getwhizz.com/api/base/info/cities/`)截至 2026-08-14 只有 6 个市场:New York、New Jersey、Philadelphia、Washington DC、Chicago、San Francisco——没有 LA。
2. **LA 页正文自己就说了**:让顾客去 NY/NJ/Philly/DC/SF/Chicago 的门店取车;门到门送车服务只覆盖 NY/NJ($35)——Whizz 无法远程履约 LA 客户。
3. **所有融资/扩张公告都没有 LA**:TechCrunch(2024-06-05,$12M Series A)列出的扩张目标是 Boston、Chicago、Miami、Philadelphia、DC;CEO 采访同样只提东岸城市;DoorDash 合作是逐城市推进(Chicago → SF/Philly/DC),不含 LA。
4. **从未有过 LA 招聘**:Indeed/Glassdoor/LinkedIn/官方 hiring 页的城市切换器都只有 6 个运营城市,岗位在 NY/NJ/Philly/Oakland。
5. **工商注册对照**:旧金山官方注册库显示 "My Device, Inc." dba "Whizz"(证书 1173414)于 **2025-08-06** 在 1231 Stevenson St 注册——证明 Whizz 真进入加州城市时会本地注册;而 **LA 市 active business 数据库里没有任何 Whizz / My Device 记录**。

### Whizz 现有全部门店地址(2026-08-14 官网核实)

| 城市 | 地址 |
|---|---|
| NYC Union Sq(总部) | 229 W 13th St, New York, NY 10011 |
| NYC Harlem | 206 E 116th St, New York, NY 10029 |
| Brooklyn | 745 Flushing Ave, Brooklyn, NY 11206 |
| NYC Midtown | 407 W 39th St, New York, NY 10018 |
| Jersey City | 498 Johnston Ave, Jersey City, NJ 07304 |
| Philadelphia | 308 Market St, Philadelphia, PA 19106 |
| Chicago | 641 W Grand Ave, Chicago, IL 60654 |
| Washington DC | 502 23rd St NW, Washington, DC 20037 |
| San Francisco(唯一加州店) | 1231 Stevenson St, Suite 101, SF, CA 94103 |
| **Los Angeles** | **无,从未有过** |

### 对 HMP 的意义

- LA 骑手搜索 "delivery e-bike rental Los Angeles" 的需求是真实存在的(否则 Whizz 不会做这个页),但**至今没有人接盘**——Zoomo 2023 年撤出(原店:DTLA Fashion District, 827 S Los Angeles St)、Whizz 只做了个网页就停在纸面上。窗口仍然敞开。
- Whizz 留下的价格锚:**$139/月**(SEO 标题)/ 搜索摘要显示全包约 **$219/月**。HMP 租赁定价可direct对标。
- Whizz 的扩张路径(NYC→NJ→Philly→DC→Chicago→SF)显示它迟早会到 LA("more cities on the roadmap")——**先占位者优势有时效性**。

---

## 第二部分:HMP 洛杉矶选址($5,000/月,industrial,租赁+换电+充电)

### 市场时机:现在是十年最好的谈判窗口

- LA 工业地产处于**租户市场**:全县均价 $1.33–1.37/SF/月 NNN,较 2022-23 峰值累计下跌 20–32%(CBRE:36 个月跌 32.4%,全美最深调整);空置率十年新高(5.0–6.5%)。
- 房东普遍可谈:成交价低于要价 5–10%,5 年约可谈 3–5 个月免租,TI(装修补贴)$1–25/SF 随租期浮动。
- 但 2026 年吸纳量已连续三个季度转正——**最大议价窗口正在关闭**。
- 典型条款:3–5 年租期、NNN 结构、年涨 3–4%、小租户通常要个人担保(可谈成 24 个月后失效的 good-guy guaranty)。

**$5,000/月能租到多大(含 NNN 分摊 $0.15–0.40/SF/月):**

| 子市场 | 面积范围 |
|---|---|
| Vernon / Commerce / Huntington Park | 3,100–3,700 SF |
| South LA(USC 以南) | 2,900–3,300 SF |
| DTLA / Boyle Heights / Lincoln Heights | 2,600–3,200 SF |
| NoHo / Van Nuys | 2,100–2,900 SF |
| Glendale / Mid-City | 2,000–2,600 SF |
| West LA / Culver City | 仅 1,200–2,200 SF |

### 同行怎么选址(踩过的点就是坐标)

- **Zoomo 前 LA 旗舰店:827 S Los Angeles St(DTLA Fashion District)**——正是我们 T1 热区走廊的东缘;另在 Leimert Park(4319 Degnan Blvd)有过 LACI 试点租赁点。
- Wombi(现存):8586 Washington Blvd, Culver City;Fly E-Bike(骑手向):1660 Ocean Ave, Santa Monica。
- 骑手向车店聚集在四条走廊:① DTLA Fashion District/South Park;② Wilshire/Western 韩国城—Westlake 轴线;③ Broadway Historic Core;④ 西区(Culver City/Santa Monica)。
- **LA 目前没有任何换电网络**(PopWheels 在 NYC/DC,Swobbee 在 NYC/NJ,Gogoro 无美国网络)——HMP 若落地换电,是 LA 第一家。

### 候选房源清单(2026-08-14 扫描,房源流动快,仅作起点)

**A 档:核心推荐(中央走廊,租赁+换电+充电一体)**

| 地址 | 区域 | 面积 | 租金 | 亮点 |
|---|---|---|---|---|
| 1499 E 4th St #101 | Boyle Heights / Arts District 边缘 | 2,600 SF | **$4,000/月全包**(水电垃圾,≈$1.54/SF) | 一层、卷帘门、夹层;最佳性价比 |
| 1312 S Boyle Ave, Unit A | Boyle Heights | 3,612 SF | $1.35/SF ≈ **$4,876/月** | 24' 层高、前后装卸、6 停车位、2002 年建(大概率带喷淋,需确认) |
| 2222 S Figueroa St 各单元 | USC / Exposition Park 旁 | 1,043–2,073 SF | $2.50/SF full service($2,608–5,183/月) | 临街、独立卫生间、HVAC;学生+骑手客群 |
| 1180 E 58th St, Unit E | South LA(Slauson 附近) | 1,400 SF(可并两单元) | **$3,000/月** | **MR1 轻制造分区**,明确允许车辆/焊接类用途,对充电架最友好 |

**B 档:韩国城门面(骑手可见度打法)**

| 地址 | 面积 | 租金 | 亮点 |
|---|---|---|---|
| 3619 W 3rd St | 1,500 SF | $2.50/SF = $3,750/月 full service | 信号灯路口、超高人流、大招牌位 |
| Solair, 3785 Wilshire Blvd #106/#107F/#103AB | 765 / 1,110 / 1,604 SF | $3.00/SF NNN($2,295 / $3,330 / $4,812/月) | **紫线 Wilshire/Western 地铁口**,K-town 心脏 |
| 269-275 S Western Ave | 800–2,250 SF | $2.20–3.24/SF | 需在 CityFeet/LoopNet 核实现况 |

**C 档:低价卫星仓/充电中枢**

| 地址 | 区域 | 面积 | 租金 |
|---|---|---|---|
| 1729 S Santee St | Fashion District | 1,000 SF | $2,400/月全包 |
| 6725 Salt Lake Ave, Bell | Vernon/HP 子市场 | 1,950 SF | $1.65/SF ≈ $3,218/月 |
| 2865 Gundry Ave, Signal Hill | Long Beach | 2,500 SF | **$3,595/月**(20' 层高、15' 电动卷帘门;空间性价比第一) |
| Slauson/Western, Hyde Park | Inglewood 相邻 | 2,000 SF | $3,950/月,**带 10 车 gated yard**(车队停放理想),C2 分区 |
| 7754 Balboa Blvd, Van Nuys | 山谷 | 1,450 SF | $2,700/月,带喷淋 |
| 14015 Crenshaw Blvd, Hawthorne | 南湾 | 925 SF | $1,395/月(最便宜的卷帘门单元) |

**组合方案(在 $5k 预算内同时要"可见度"和"仓储")**:Solair 765 SF 门面($2,295)+ 1729 Santee 仓库($2,400)= **$4,695/月**,K-town 地铁口展示租赁 + Fashion District 充电履约,两点相距约 4 英里。

> 注:多数房源来自 Craigslist/CommercialCafe 直接核实,LoopNet/Crexi 反爬只能取搜索摘要;所有房源需经纪人带看核实现况。上表价格标注 full service(全包)/NNN 口径。

### 合规要点(直接影响选址决策)

**分区(Zoning)——选 C2 以上或 M1 最稳:**
- "Motorcycle or Motor Scooter Rental"、"Bicycle Rental"、"Bicycle Repair Shop"、"Battery Service" 在 **C2、C5、CM、M1、M2、M3 均为 by-right 允许用途**(无需 CUP)。
- **电池重组/再制造(rebuilding)只允许在 M1–M3**——不要在 C 区门店拆修电芯。

**消防(最大的隐性成本,看房时第一优先确认)——**
- 存储 >15 立方英尺锂电池(约 **45–60 块**电动摩托电池包)需 **LAFD 许可** + 消防安全计划(LA Fire Code 105.5.53)。
- 室内批量存储:容器最大 7.5 cu ft、间隔 3 英尺、离出口 5 英尺;超限需 **2 小时防火分隔 + 自动喷淋** + 吸气式/辐射能感烟探测(LAMC 57.322)。
- 固定换电柜聚合 **>20 kWh(约 12+ 块电池)按储能系统(ESS)监管**(LAMC 57.1207 / NFPA 855)。50 块电池的换电墙约 90 kWh,超过所有室内基准——需拆分为多个防火分区。
- NYC FDNY 是最严基准(LA 正在跟进):单一防火分区充电聚合 ≤50 kWh、电池间隔 2–3 英尺、6 台以上设备室内充电需专用 1 小时防火房(喷淋+感烟)。
- **选址铁律:优先选已带喷淋(sprinklered)的建筑**——为电池仓补装喷淋和 2 小时防火墙是整个 buildout 最大的成本项。

**SB 1271(2026-01-01 已生效,直接约束租赁车队):**
- 在加州**销售、分销、租赁**的 e-bike/PMD、电池和充电器必须经认可实验室认证 **UL 2849 / UL 2271 / UL 2272**(或 EN 等效)。FLASH / Lightning / INNO 上租赁车队前必须确认认证状态——这既是合规要求,也是对抗低价无认证竞品的卖点。

**电力(看房必问):**
- 每个充电器约 0.5–1.2 kW:20 个 ≈ 12–18 kW,50 个 ≈ 30–50 kW(NEC ×1.25 连续负载)。
- **200A/240V 服务够 20–30 个充电位;50 个需 400A 或三相**。LADBS Express Permit 在线当天可批(≤400A 升级免 plan check)。

**营业与租车合规:**
- LA 市 BTRC 营业税登记 + CDTFA seller's permit(租金收入是应税 continuing sales,除非购车时已缴税并选择前置)。
- 保险:garage liability($1M/$2M)+ garagekeepers($50k–250k);投保时须披露锂电充电业务。
- **CVC 14608:出租机动车前必须查验驾照并核对照片/签名**并留档(CVC 14609)。Moped 类(CVC 406)租客需持 M1/M2、戴头盔、车辆一次性 $23 DMV 上牌。
- **Class 1–3 e-bike 无需驾照/注册/保险**——产品组合启示:INNO 若以 Class 2/3 e-bike 形态出租,可覆盖大量没有 M 牌的骑手(移民骑手群体的主力),FLASH/Lightning 摩托形态服务有牌骑手,两条腿走路。

### 推荐行动顺序

1. **先锁走廊再看房**:首选 Boyle Heights/DTLA 东缘(承接 K-town–DTLA 热区、租金 $1.3–1.6/SF、同行验证过的选址),次选 USC 旁 Figueroa 走廊(学生市场 + 南 LA 价格)。
2. 看房清单三问:**有无喷淋?电力服务多大(200A+)?分区是否 C2/M1?**
3. 用租户市场行情谈判:对标 $1.35/SF、要 3 个月免租、good-guy guaranty、CAM 封顶。
4. 确认 FLASH / Lightning / INNO 及电池/充电器的 UL 认证文件(SB 1271)。
5. 换电柜按 <20 kWh/防火分区模块化设计,避免触发 ESS 全套审批;首期 20 充电位按 200A 规划。

---

## 附录:关键来源

**Whizz 调查**
- Wayback 首次快照(2025-03-22):http://web.archive.org/web/20250322213909/https://www.getwhizz.com/cities/deliver/los-angeles
- Whizz 运营城市 API(6 城无 LA):https://www.getwhizz.com/api/base/info/cities/
- Whizz 门店列表:https://www.getwhizz.com/locations
- TechCrunch $12M Series A(扩张目标无 LA):https://techcrunch.com/2024/06/05/whizz-wants-to-own-the-delivery-e-bike-subscription-space-starting-with-nyc
- SF 工商注册(My Device, Inc. dba Whizz,2025-08-06):https://data.sfgov.org(certificate 1173414)
- DoorDash 合作四城公告:https://www.getwhizz.com/blog/for-delivery/whizz-expands-doordash-partnership-across-four-cities-to-power-delivery-riders-with-smarter-mobility

**市场与房源**
- Cushman & Wakefield / CBRE / Kidder Mathews LA 工业市场报告(2025 Q4–2026 Q2)
- 房源:CommercialCafe、Craigslist LA、CityFeet/LoopNet 搜索摘要(2026-08-14 扫描,详见正文链接)

**合规**
- LA City Planning List of Uses(ZA 2003-4842);LA Fire Code 105.5.53;LAMC 57.322 / 57.1207;NFPA 855-2023
- NYC Fire Code FC 309.3 / Local Law 39 of 2023(基准)
- California SB 1271(UL 2849/2271/2272 认证强制)
- CVC 14608/14609(租车查驾照)、CVC 406(moped 定义)
- LADBS Express Permit(IB-P-GI 2020-003)
