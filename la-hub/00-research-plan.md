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

### A5. Task 5 竞争：逐家表格

Whizz（SF/LA）、Zoomo、Wombi 以及 LA 本地租赁、Facebook Marketplace 非正规租赁。每家的价格/押金/车型/续航/维修/换车/rent-to-own/平台合作/门店/评论。规模数字一律标 `estimate`，除非有公司披露或第三方报道。

### A6. Task 6 场地：total cost of location

768 Ceres 打 0–10 分，并和 Koreatown / Westlake / Fashion District / South Park / Arts District / Historic South Central 比：

租金 + 安保成本 + 盗损预期 + 保险 + 获客优势（离骑手近不近） + 骑手便利 + 车队运营效率。用 LAPD 公开犯罪数据按半径算事件数，不用"感觉治安差"。

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

（待本轮数据可得性探测结果填入：来源、URL、粒度、可靠性、覆盖哪个 Task）

---

## D. 必须向你（HMP）询问的数据

### P0：没有这些，模型只是猜

1. **SF 时间线**：骑手业务从哪年开始；逐年（最好逐月）整车销量、在租台数、电池订阅数。用来画 ramp curve，这是 M3/M6/M12/M24 预测的唯一可靠依据。
2. **SF 租赁车队分母**：在租 ~100 台对应的总租赁车队多少台（利用率）；平均租期；租转买比例；周租客户的月流失。
3. **SF 客户地理分布**：CRM 里客户地址落在 SoMa / Mission / Tenderloin / FiDi 的比例，以及有多少来自 SF 以外（Oakland、Daly City）。这决定"核心区对核心区"的比较框架是否成立。
4. **客户构成**：客户中职业外卖员比例；DoorDash vs Uber Eats vs 其他；e-bike vs moped vs motorcycle 的销售占比；持 M1/M2 证的比例。
5. **价格与成本**：四档车型的售价、落地 COGS、周租/月租、押金、电池订阅价、换电费、平均每订阅用户每月换电次数。
6. **盗损与坏账**：SF 租赁车队年度被盗/不归还率、坏账占租赁收入比例、目前保险（险种、保费、是否覆盖租赁车队）。
7. **电池经济**：电池成本、实际在外卖使用下的寿命（月）、每订阅用户配几块电池、订阅月流失率。
8. **SF 运营基线**：人员配置（角色、人数、时薪）、SF 门店面积和租金（用来判断 8,443 sqft 是否远大于试点所需）、每台在租车每月维护成本。
9. **获客**：SF 新客中转介绍占比；主要语言社群；单客获客成本（哪怕是粗估）。
10. **SF 盈利性**：至少各条业务线的毛利率；最好一份 SF 月度 P&L。没有它，"复制 SF"到底复制的是什么并不清楚。

### P1：影响精度

11. 客户口述的日均单量、时薪（分车型），用于校准方法③。
12. SF 客户里有多少人是"先租后买"路径，占已售 1,000 台的比例。
13. 配件/维修的每客户年均消费。

### P2：场地相关

14. 768 Ceres 租约条款：NNN 还是 gross、期限、免租期、TI 补贴、转租/提前退出条款。
15. 房东和保险公司对锂电池集中充电/存储的态度（这可能是硬障碍）。
16. 你是否已经有 LA 的客户或询盘（哪怕几十个），以及他们在哪个区域。

---

## E. 目前最容易导致判断错误的 5 个假设

（待本轮对抗式评审结果填入）

---

## F. 下一步

1. 你回复 D 部分 P0 数据（有多少给多少，没有的标"没有"）。
2. 我用公开数据填 FACT_PENDING，跑 Task 1 / Task 2，交模型 v1。
