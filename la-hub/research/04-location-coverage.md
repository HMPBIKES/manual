# 在 LA 哪里选址最能覆盖外卖骑手（选址覆盖分析）

版本：v1 draft，2026-09-07。问题：如果目标是"让尽可能多的两轮外卖骑手顺路到店"，地址应该放在 LA 的哪里；768 Ceres Ave 在这个标准下排第几。

三层证据，互相独立：

| 层 | 回答什么 | 数据 | 脚本 / 文件 |
|---|---|---|---|
| A. 骑手自述 | 骑两轮的骑手说自己在哪里跑单、哪里赚钱、哪里危险 | 用真实浏览器（headless Chromium）抓 Reddit 公共 JSON：20 个子版 × 60 组关键词，约 6,600 帖 + 相关帖的评论 | `raw/reddit/reddit_scrape.py`、`reddit_tally.py`、`raw/reddit/*.jsonl` |
| B. 需求密度 | 骑手接单点（餐厅）在地理上怎么分布，候选地址 1–3 英里能覆盖多少 | LA County 公共卫生局餐厅清单（约 2.8 万家去重）+ ACS 人口 / 无车家庭 | `raw/market/site_coverage.py` → `site_coverage.csv` |
| C. 治安 | 候选地址周边抢劫、伤害、自行车被盗的密度 | LAPD 2020–present 犯罪数据，取 2023-01 至 2024-03（LAPD 2024-03 换系统后数据不全） | `raw/market/site_crime.py` → `site_crime.csv` |
| D. 场地 | 各区现在租得到什么、多少钱 | PropertyShark / CommercialCafe / Craigslist 挂牌（LoopNet 等 CoStar 站点 403） | `raw/market/listings.json` |

标签沿用前几份报告：FACT 可核对；ESTIMATE 有数据但要换算；ASSUMPTION 我定的参数，可替换。

## 0. 一句话答案

（待 Reddit 全量分析完成后填写。）

---

## 1. Reddit 骑手自述（层 A）

（待填：抓取完成后由 `reddit_tally.py` 与分析代理输出。）

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
- **768 Ceres 在每个半径上都不是最优**：1.5 英里 975（第 9），2 英里 1,217（比 Westlake 少 30%），3 英里 2,022（比 Westlake 少 26%）。它在 Warehouse District 的东南角，东边和南边 1–2 英里是仓库和铁路，半个圆是空的。
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

（待 Reddit 分析完成后填写：把层 A 的骑手自述热区叠到层 B–D 上，给出单点 / 两节点方案与具体街区。）

## 7. 768 Ceres 在这个标准下的位置

（待填。）

## 8. 数据局限

（待填。）
