# Translation Style Guide and Master Glossary

Source: 《覺海慈航度香江——宣化上人事跡·香港篇》 (Traditional Chinese, ~150,000 characters, 1,716 numbered paragraphs P0001–P1716).
Target: English, for an English-reading Buddhist audience, following the conventions of the Dharma Realm Buddhist Association (DRBA) / Buddhist Text Translation Society (BTTS).

The client's decisions (binding):
1. **Faithful and fluent.** Translate every sentence and clause. Do not add, drop, summarize, or merge content. It should read as natural English, not "translationese".
2. **Names:** use the DRBA/BTTS established spellings for the names they have fixed (Hsuan Hua, Hsu Yun, An Tse, To Lun, Heng Sure, etc.). Use **Hanyu Pinyin** for all other people. Use the **official Hong Kong English names** for Hong Kong places and institutions.
3. **Brief translator's notes** in square brackets the first time a Buddhist or cultural term needs explaining (see §4). A Chinese–English glossary will be appended to the book (it is built from this file plus your new-term lists).
4. **Verses (偈, poems, couplets):** translate them as lineated verse. The assembler automatically prints the Chinese original under every paragraph you tag as verse (see §2).
5. **Source errors:** the source has many typos (wrong homophones, OCR-like errors). Translate the *intended* meaning and log every correction in your errata file. Keep the source's chapter numbering exactly as written, even where it is wrong.

---

## 1. Files and output format

Your batch source file has one paragraph per line:

```
[P0123|P] 原文……
```

The type code after `|` is one of:
TITLE, SUBTITLE, AUTHOR, PART (part heading), PARTINFO (age/year line under a part), CH (chapter heading), SUB (sub-section heading), PB (short bold line), P (normal paragraph).

**Your translation file** must contain exactly one entry for every source ID, in the same order, as follows:

```
[P0123] English translation of the whole paragraph.

[P0124|V] First line of verse / second line of verse

```

Rules:
- One entry per ID with no merging, splitting, skipping, or reordering. Leave a blank line between entries. The paragraph text goes on the same line as its ID tag.
- Do not repeat the type code. Add `|V` after the ID **only** for paragraphs that are verse (偈, poems, couplets, inscriptions in verse form). Inside a verse paragraph, separate verse lines with ` / `.
- No Chinese characters in the English, apart from the rare case where a Chinese term is deliberately shown inside a translator's note (see §4).
- Italics: write book, sutra, magazine, and newspaper titles as `*Title*`. No other Markdown.
- Use straight double quotes `"…"` for speech and single quotes `'…'` for quotes inside quotes.
- For dialogue lines that are separate paragraphs in the source, keep them as separate entries.

---

## 2. Recurring structural formulas (use exactly)

| Chinese | English |
|---|---|
| 上人自述： | In the Venerable Master's own words: |
| 上人有偈： | The Venerable Master wrote a verse: |
| 上人說： | The Venerable Master said: |
| 上人開示 / 上人XXXX年X月X日開示 | Instructional talk by the Venerable Master / From the Venerable Master's instructional talk of [Month Day, Year] |
| 【後記】 / 【後記1】 / 【後記一】 | [Addendum] / [Addendum 1] / [Addendum 1] (always Arabic numerals; keep any title after it, e.g. 【後記2】蛇來聽法 → [Addendum 2] Snakes Come to Hear the Dharma) |
| XXX居士敘述： | Upasika/Upasaka XXX recounted: |
| XXX口述： | XXX's oral account: |
| XXX記述： | XXX wrote: |
| XXX居士日記： | From the diary of Upasika/Upasaka XXX: |
| 時代背景： | Historical background: |
| 編按：/（編按：……） | Editor's note: / (Editor's note: …) |
| 篇按 (typo for 編按) | Editor's note (log in errata) |
| 內容略 / （略） | (content omitted) / (omitted) |
| 節錄 | (excerpt) |
| 楔子 | Prologue |
| 轉自台灣學佛網 http://www.xuefo.tw | Reproduced from the Taiwan Xuefo website (http://www.xuefo.tw) |

**Headings:**
- Chapter heading `01、 隨緣赴港` → `01. <English title>`. Keep the source number **exactly** as written, including the leading zero, duplicates and gaps (64 appears twice; 96 appears twice; 60, 65 and 95 are missing). Log them in errata but do **not** renumber.
- Sub-section `（1） 聽法歡喜` → `(1) <English title>`.
- Part headings (fixed):
  - 第一篇 赴港與待緣 → Part One: Coming to Hong Kong and Awaiting Conditions
  - 第二篇 建廟與弘法 → Part Two: Building Monasteries and Propagating the Dharma
  - 第三篇 慈興與安僧 → Part Three: Cixing Monastery and Providing for the Sangha
  - 第四篇 講堂與度眾 → Part Four: The Lecture Hall and Helping Living Beings Cross Over
- PARTINFO: 三十二歲至三十四歲 → Ages 32 to 34; 公元一九四九至一九五一年 → 1949 to 1951 CE.
- Book front matter (fixed):
  - P0001 → Crossing Hong Kong on the Ship of Compassion in the Sea of Awakening — Records of the Life of the Venerable Master Hsuan Hua (title of the English serial in *Vajra Bodhi Sea*)
  - P0002 → The Hong Kong Years
  - P0003 → Compiled by the Editorial Committee for the Records of the Life of the Venerable Master Hsuan Hua

---

## 3. Style rules

- **Faithfulness first.** Every factual element must survive: names, numbers, dates, ages, amounts, places, sequence of events, who said what. When a sentence is ambiguous, choose the most plausible reading and note it in your queries file.
- **Voice.** Much of the book is the Master's own spoken Mandarin: colloquial, humorous, with rhetorical questions ("你說怎麼了？"). Keep that spoken flavour in plain, natural English. Do not make it stiff or overly formal. The disciples' accounts are plain narrative. The eulogies and letters to Elder Masters are formal classical Chinese: use a dignified register for those.
- **Classical / literary passages** (letters, eulogies, prefaces, 4-character phrases): render the meaning accurately in dignified English. Do not leave allusions unexplained if the meaning would be lost; a short [Tr.: …] note is allowed.
- **Chinese idioms/proverbs** (e.g. 捨不了假，成不了真): translate the meaning, keeping the image where it works in English. Proverbs in quotation marks stay in quotation marks.
- **Dates:** 民國三十八年（1949年） → in the thirty-eighth year of the Republic (1949). 農曆八月十六日 → the sixteenth day of the eighth lunar month. Gregorian dates → "October 7, 1949". Write years as numerals. Keep ages as given (Chinese reckoning); do not convert them.
- **Numbers:** spell out one to ten in narrative and use numerals for 11 and above, for dates, ages with "years old", money, and measurements. Keep the source's units (尺 → feet / Chinese feet; 里 → li; 斤 → catties) with a short note on first occurrence if needed.
- **Money:** 港幣/港元 → HK$; 美金 → US$; 塊錢 → dollars.
- **Pronouns:** use the gender table in §6. If you cannot tell, use the person's name or "they".
- **Translator's notes:** `[Tr.: …]`, kept short (one clause, max ~25 words). Source parentheses stay parentheses; source editor's notes stay "(Editor's note: …)".

---

## 4. Translator's-note policy (avoid duplicates across batches)

Add a short `[Tr.: …]` note **only** at the paragraph ID listed below for that term (its first occurrence in the whole book). If that ID is not in your batch, do NOT add the note; just use the English term. For any other term that you feel truly needs a note, add it at its first occurrence in your batch, and list it in your new-terms file with the ID so the editor can de-duplicate.

| Term | English rendering | Note goes at |
|---|---|---|
| 業風 | karmic winds | P0006 |
| 掛單 | stay (as a visiting monk) at …; lodge | P0013 (note: monastic custom of lodging temporarily at a monastery while traveling) |
| 十方叢林 | public monastery of the ten directions | P0015 (open to all monastics, as opposed to a private hereditary temple) |
| 皈依 | take refuge (with the Master); refuge disciple (皈依弟子) | P0018 (formally becoming a Buddhist disciple by taking refuge in the Buddha, Dharma, and Sangha) |
| 夜不倒單 | never lying down to sleep | P0034 (note: never lying down, remaining seated even when asleep) |
| 日中一食 | eating one meal a day, at midday | P0034 |
| 托缽 | go on alms rounds | P0036 |
| 打七 | hold a seven-day session | P0041 (an intensive seven-day period of meditation or recitation) |
| 參禪 | investigate Chan | P0042 |
| 坐龕 | meditation box | P0047 (a wooden box-seat in which a monk sits in meditation day and night) |
| 功德 | merit and virtue | P0071 |
| 偈 | verse (gatha) | P0071 |
| 放焰口 / 焰口 | perform the Flaming Mouth ceremony | P0075 (a ritual for feeding hungry ghosts) |
| 千壇焰口 | a thousand Flaming Mouth ceremonies | (same paragraph) |
| 天龍八部 | the gods, dragons, and the rest of the eightfold division | P0076 |
| 韋陀菩薩 | Weituo Bodhisattva | P0093 (Dharma-protector Bodhisattva, guardian of monasteries) |
| 衲袍 | patched robe | P0039 |
| 袈裟 | kashaya (precept sash) | P0120 |
| 華嚴七 | Avatamsaka session | P0168 |
| 通善壇 | Tung Sin Tan | P0163 (a Taoist hall of the Quanzhen school in Hong Kong) |
| 扶乩 | planchette writing (spirit writing) | P0184 |
| 三步一拜 | three steps, one bow | P0280 |
| 幽冥戒 | precepts for the deceased | P0405 (precepts transmitted on behalf of the departed) |
| 阿闍梨 | Acharya | P0508 |
| 般舟 / 般舟七 | Pratyutpanna Samadhi practice / Pratyutpanna session | P0993 (practice of constant walking and standing, without sitting or lying down, for a set period) |
| 嗣法 / 溈仰宗 | receive Dharma transmission / Weiyang lineage | P1019 (one of the five houses of Chan) |
| 持午 / 過午不食 | keep the rule of not eating after noon | P1699 |
| 開光 | Opening-the-Light ceremony (consecration) | P0256 (note: a ceremony consecrating Buddha images) |
| 舍利 / 捨利 | sharira (relics) | P0769 |

---

## 5. Master glossary (use these renderings consistently)

### 5.1 The Venerable Master and forms of address
| Chinese | English |
|---|---|
| 上人 | the Venerable Master |
| 宣化上人 | the Venerable Master Hsuan Hua |
| 宣公上人 / 宣公 | the Venerable Master Hua |
| 師父 (referring to Master Hua) | the Master (third person); "Shifu" (direct address in speech) |
| 安慈 | An Tse (the Master's Dharma name) |
| 度輪 / 度輪法師 / 度輪長老 / 度輪禪師 | To Lun / Dharma Master To Lun / Elder To Lun / Chan Master To Lun |
| 度老 / 度公 / 度公上人 | Elder To Lun / the Venerable To Lun / the Venerable Master To Lun |
| 安慈大師 | Great Master An Tse |
| 山僧 / 乞士 (self-reference) | this mountain monk / this mendicant |
| 師公 | Grand Master |
| 師兄 / 師弟 | Dharma brother |
| 師侄 | Dharma nephew |
| 徒弟 / 弟子 | disciple |
| 皈依弟子 | refuge disciple |
| 出家弟子 / 在家弟子 | monastic disciple / lay disciple |
| 法師 | Dharma Master |
| 老和尚 | Elder Master |
| 長老 | Elder |
| 大師 | Great Master |
| 老法師 | elder Dharma Master |
| 和尚 (generic) | monk |
| 比丘 / 比丘尼 | Bhikshu / Bhikshuni |
| 沙彌 / 沙彌尼 | shramanera (novice monk) / shramanerika (novice nun) |
| 居士 (after a name) | Upasaka (man) / Upasika (woman), placed before the name: "Upasika Tan Guo Zheng" |
| 居士 (generic) | layperson / lay Buddhist |
| 老居士 | elderly Upasaka/Upasika |
| 出家人 | monastic / left-home person |
| 在家人 | layperson |
| 善信 / 信眾 | faithful devotees / devotees |
| 護法 (a lay supporter) | Dharma protector |
| 施主 | donor |
| 方丈 | abbot |
| 住持 | abbot |
| 當家 | manager (of a monastery) |
| 知客 | guest prefect |
| 僧團 | Sangha (monastic community) |
| 釋X (monastic surname) | Shi X |

### 5.2 People – monastics
| Chinese | English |
|---|---|
| 虛雲老和尚 / 虛老 / 雲公 / 雲公老人 / 虛雲老人 / 虛雲和尚 | Elder Master Hsu Yun / Elder Hsu / the Venerable Yun / the Venerable Elder Yun / Elder Hsu Yun / Master Hsu Yun |
| 來果老和尚 / 來果大師 | Elder Master Lai Guo / Great Master Lai Guo |
| 倓虛老和尚 | Elder Master Tan Xu |
| 茂峰法師 / 茂峰老和尚 | Dharma Master Mao Feng / Elder Master Mao Feng |
| 慧德法師 | Dharma Master Hui De |
| 知定長老 / 知定法師 | Elder Zhi Ding / Dharma Master Zhi Ding |
| 成元法師 | Dharma Master Cheng Yuan |
| 續行法師 | Dharma Master Xu Xing |
| 融秋法師 (also mis-typed 融法師) | Dharma Master Rong Qiu |
| 旭朗法師 / 旭朗老和尚 / 旭朗老法師 | Dharma Master Xu Lang / Elder Master Xu Lang |
| 明觀法師 / 明觀和尚 | Dharma Master Ming Guan |
| 聖一老和尚 / 聖一法師 | Elder Master Sheng Yi / Dharma Master Sheng Yi |
| 樂觀法師 | Dharma Master Le Guan |
| 親覺法師 / 比丘 | Dharma Master Qin Jue |
| 法藏法師 | Dharma Master Fa Zang |
| 法傳大師 / 法傳法師 | Great Master Fa Chuan / Dharma Master Fa Chuan |
| 清嚴和尚 / 法師 | Master Qing Yan / Dharma Master Qing Yan |
| 玄智老法師 / 老和尚 | Elder Dharma Master Xuan Zhi / Elder Master Xuan Zhi |
| 定西老法師 | Elder Dharma Master Ding Xi |
| 紹雲老法師 | Elder Dharma Master Shao Yun |
| 永惺法師 | Dharma Master Yong Xing |
| 寬運法師 | Dharma Master Kuan Yun |
| 博山和尚 | Master Boshan |
| 憨山大師 | Great Master Hanshan |
| 永嘉大師 | Great Master Yongjia |
| 六祖大師 / 慧能大師 | the Sixth Patriarch / Great Master Huineng |
| 二祖 | the Second Patriarch |
| 達摩 | Bodhidharma |
| 濟公 | Jigong |
| 玉琳國師 | National Master Yulin |
| 恆定法師 (果一) | Dharma Master Heng Ding (Guo Yi), male |
| 恆越法師 | Dharma Master Heng Yue, male |
| 恆智法師 | Dharma Master Heng Zhi, male |
| 恆益法師 (釋果利) | Dharma Master Heng Yi (Shi Guo Li), **female (Bhikshuni)** |
| 恆起法師 (釋果忍) | Dharma Master Heng Qi (Shi Guo Ren), **female** |
| 近慈法師 (果森, 親仁) | Dharma Master Jin Ci (Guo Sen; Qin Ren), **female** |
| 恆貴法師 | Dharma Master Heng Gui |
| 恆興法師 | Dharma Master Heng Xing |
| 恆偉法師 | Dharma Master Heng Wei, **female** (比丘尼) |
| 恆和法師 | Dharma Master Heng He, **female** (比丘尼) |
| 恆實法師 | Dharma Master Heng Sure (established spelling) |
| 恆持法師 | Dharma Master Heng Chih (established spelling) |
| 恆具 / 恆由 | Heng Ju / Heng Yo (established spellings; American monks) |
| 恆寂 (果能) / 恆禹 (果舜) / 果維 | Heng Ji (Guo Neng) / Heng Yu (Guo Shun) / Guo Wei |
| 恆來 / 恆授 / 恆守 / 恆祥 / 恆福 / 恆順 / 恆相 / 恆靜 | Heng Lai / Heng Shou / Heng Shou / Heng Xiang / Heng Fu / Heng Shun / Heng Xiang / Heng Jing |

Other monastic names not listed: Pinyin, each syllable capitalized and separated ("Dharma Master Ci Hang"). Write Pinyin without tone marks.

### 5.3 People – lay disciples (surname first, then the Dharma name as two capitalized syllables)
| Chinese | English | Gender |
|---|---|---|
| 譚果正 | Tan Guo Zheng | F (elder sister of Guo Shi) |
| 譚果式 (譚慕潔) | Tan Guo Shi (Tan Mujie) | F |
| 譚果璞 (譚璞才) | Tan Guo Pu (Tan Pucai), father of the Tan sisters | M |
| 甘果彥 | Gan Guo Yan, mother of the Tan sisters | F |
| 文果蜜 | Wen Guo Mi | M |
| 余果滿 | Yu Guo Man | F |
| 余果興 | Yu Guo Xing (her son) | M |
| 薛果鳳 | Xue Guo Feng (Yu Guo Man's daughter-in-law) | F |
| 劉果娟 | Liu Guo Juan (also rendered Lau Kuo Kuen) | F |
| 羅果明 (黃太太) | Luo Guo Ming (Mrs. Huang) | F |
| 黃果松 | Huang Guo Song (daughter of Luo Guo Ming) | F |
| 黃果君 | Huang Guo Jun (son of Luo Guo Ming) | M |
| 王果海 (王太太) | Wang Guo Hai (Mrs. Wang) | F |
| 陳寬滿 | Chen Kuan Man | F |
| 謝寬輝 | Xie Kuan Hui | — |
| 郭寬普 | Guo Kuan Pu | — |
| 袁果祥 / 袁果珍 | Yuan Guo Xiang / Yuan Guo Zhen (sisters) | F |
| 袁果林 (陳瑞昌夫人) | Yuan Guo Lin (Mrs. Chen Ruichang) | F |
| 陳瑞昌 | Chen Ruichang (Hong Kong businessman, 大光公司 Daguang Company) | M |
| 李果遠 (李大華) | Li Guo Yuan (Li Dahua) | M |
| 黎果合 | Li Guo He | M |
| 果殊 | Guo Shu | F |
| 果平 | Guo Ping | F |
| 蔡果夙 / 薛果夙 | Cai Guo Su / Xue Guo Su | F |
| 果宏 | Guo Hong | F |
| 果全 / 果根 | Guo Quan / Guo Gen | F |
| 胡果為 | Hu Guo Wei | F |
| 裴果鑒 (裴有明, 裴證慧) | Pei Guo Jian (Pei Youming; Pei Zhenghui) | M |
| 梅妙玲 | Mei Miaoling | F |
| 許湘君 | Xu Xiangjun | F |
| 鐘美薇 (果迦) | Zhong Meiwei (Guo Jia) | F |
| 伍英才 (果棟) | Wu Yingcai (Guo Dong) | M |
| 阮果霓 | Ruan Guo Ni | F |
| 詹勵吾 | Zhan Liwu | M |
| 唐果善 / 麥果蓮 / 陳果發 / 葉果慶 / 董果耆 / 湯果雲 / 姚果白 / 何果章 / 洪果宏 / 陳果升 / 馬果仙 | Tang Guo Shan / Mai Guo Lian / Chen Guo Fa / Ye Guo Qing / Dong Guo Qi / Tang Guo Yun / Yao Guo Bai / He Guo Zhang / Hong Guo Hong / Chen Guo Sheng / Ma Guo Xian | gender from context |

Non-Dharma personal names (birth names): Pinyin with the given name joined, e.g. 譚慕潔 → Tan Mujie, 李大華 → Li Dahua. Public figures: established English forms, e.g. 於右任 Yu Youren, 閻錫山 Yan Xishan, 俞大維 Yu Ta-wei, 李漢魂 Li Hanhun. 貝納祺 → Brook Bernacchi (British barrister and Urban Council member in Hong Kong).

### 5.4 Places and institutions
**Hong Kong (official English names):**
| Chinese | English |
|---|---|
| 香港 / 香江 | Hong Kong |
| 九龍 / 新界 | Kowloon / the New Territories |
| 大嶼山 / 嶼山 | Lantau Island |
| 荃灣 | Tsuen Wan |
| 芙蓉山 | Fu Yung Shan |
| 觀音洞 | Guanyin Cave |
| 跑馬地 | Happy Valley |
| 筲箕灣 / 西灣河 / 馬山村 | Shau Kei Wan / Sai Wan Ho / Ma Shan Village |
| 萬丈瀑 / 萬丈布 | Man Cheung Po |
| 靈會山 | Ling Wui Shan |
| 昂坪 | Ngong Ping |
| 大澳 / 石壁 / 長沙 | Tai O / Shek Pik / Cheung Sha |
| 北角 / 中環 / 西環 / 香港仔 / 半山 / 山頂 | North Point / Central / Sai Wan / Aberdeen / the Mid-Levels / the Peak |
| 沙田 / 元朗 / 青山 / 鑽石山 / 黃大仙 / 啟德 | Sha Tin / Yuen Long / Castle Peak / Diamond Hill / Wong Tai Sin / Kai Tak |
| 東普陀寺 | Tung Po Tor Monastery |
| 竹林禪院 | Chuk Lam Sim Yuen (Bamboo Grove Monastery) |
| 寶蓮寺 / 寶蓮禪寺 | Po Lin Monastery |
| 寶林禪寺 | Po Lam Monastery |
| 志蓮淨苑 | Chi Lin Nunnery |
| 東蓮覺苑 | Tung Lin Kok Yuen |
| 正覺蓮社 | Ching Kok Lin Association |
| 東林念佛堂 | Tung Lin Buddha Recitation Hall |
| 鹿野苑 | Luk Ye Yuen |
| 西林寺 / 凌雲寺 / 圓通寺 / 妙法寺 | Sai Lam Monastery / Ling Wan Monastery / Yuen Tung Monastery / Miu Fat Monastery |
| 通善壇 | Tung Sin Tan |
| 大會堂 | City Hall |
| 香港佛教聯合會 | Hong Kong Buddhist Association |
| 東華 (三院) | Tung Wah (Group of Hospitals) |
| 市政局 / 市政局議員 | Urban Council / Urban Council member |

**The Master's own establishments (DRBA names):**
| Chinese | English |
|---|---|
| 西樂園寺 / 西樂園 | Western Bliss Gardens Monastery / Western Bliss Gardens |
| 慈興寺 / 慈興禪寺 | Cixing Monastery / Cixing Chan Monastery (add "(known locally as Tsz Hing Monastery)" once only, at its first occurrence in the book, P0218) |
| 國清禪院 / 國清寺 | Guoqing Chan Monastery / Guoqing Monastery (Cixing's predecessor) |
| 佛教講堂 / 香港佛教講堂 | the Buddhist Lecture Hall / the Hong Kong Buddhist Lecture Hall |
| 三藩市佛教講堂 / 金山佛教講堂 | the San Francisco Buddhist Lecture Hall |
| 金山寺 / 金山聖寺 | Gold Mountain Monastery / Gold Mountain Sagely Monastery |
| 萬佛城 / 萬佛聖城 | the City of Ten Thousand Buddhas |
| 金輪寺 / 金聖寺 / 金佛寺 / 長堤聖寺 | Gold Wheel Monastery / Gold Sage Monastery / Gold Buddha Monastery / Long Beach Monastery |
| 法界佛教總會 (法總) | Dharma Realm Buddhist Association (DRBA) |
| 法界佛教印經會 | Dharma Realm Buddhist Books Distribution Society |
| 中美佛教總會 | Sino-American Buddhist Association |

**Mainland China and elsewhere:**
| Chinese | English |
|---|---|
| 東北 | Manchuria (Northeast China) |
| 南華寺 / 曹溪 | Nanhua Monastery / Caoxi |
| 雲門大覺寺 / 雲門 | Dajue Monastery at Yunmen / Yunmen |
| 雲居山 / 真如禪寺 | Mount Yunju / Zhenru Chan Monastery |
| 韶關 / 馬壩 | Shaoguan / Maba |
| 六榕寺 | Liurong Monastery |
| 普陀山 | Mount Putuo |
| 靈巖山 | Lingyan Mountain |
| 高旻寺 | Gaomin Monastery |
| 三緣寺 | Sanyuan Monastery |
| 古德寺 | Gude Monastery |
| 鼓山 / 湧泉寺 | Gushan / Yongquan Monastery |
| 五台山 | Mount Wutai |
| 雲棲 | Yunqi |
| 瀋陽 (mis-typed 潘陽) | Shenyang |
| 龍蓮寺 / 龍蓮禪寺 | Wat Mangkon Kamalawat (Longlian Monastery), Bangkok |
| 暹羅 | Siam |
| 緬甸 / 仰光 | Burma / Rangoon |
| 檀香山 | Honolulu |
| 舊金山 / 三藩市 | San Francisco |
| 檀香山中華佛教會 | Chinese Buddhist Association of Hawaii |
| 台灣佛教會 | the Buddhist Association of Taiwan |
| 世界佛教僧伽大會 / 第三屆世界佛教僧伽大會 | World Buddhist Sangha Council / the Third General Conference of the World Buddhist Sangha Council |

### 5.5 Texts and publications
| Chinese | English |
|---|---|
| 《地藏經》 / 《地藏菩薩本願經》 | *Earth Store Sutra* / *Sutra of the Past Vows of Earth Store Bodhisattva* |
| 《楞嚴經》 / 《楞嚴》 | *Shurangama Sutra* |
| 《六祖壇經》 | *Sixth Patriarch's Dharma Jewel Platform Sutra* (short: *Sixth Patriarch Sutra*) |
| 《法華經》 / 《妙法蓮華經》 | *Dharma Flower Sutra* / *Wonderful Dharma Lotus Flower Sutra* |
| 《金剛經》 / 《金剛般若波羅蜜經》 | *Vajra Sutra* / *Vajra Prajna Paramita Sutra* |
| 《大般若經》 | *Great Prajna Sutra* |
| 《華嚴經》 / 《大方廣佛華嚴經》 | *Avatamsaka Sutra* / *Great Means Expansive Buddha Flower Adornment Sutra* |
| 〈賢首品〉 | "Worthy Leader Chapter" |
| 《普門品》 | *Universal Door Chapter* |
| 《彌陀經》 / 《阿彌陀經》 | *Amitabha Sutra* |
| 《心經》 / 《般若波羅蜜多心經》 | *Heart Sutra* |
| 《金光明經》 | *Golden Light Sutra* |
| 《梵網經》 / 《梵網菩薩戒經》 | *Brahma Net Sutra* / *Brahma Net Bodhisattva Precepts Sutra* |
| 《大悲心陀羅尼經》 | *Great Compassion Heart Dharani Sutra* |
| 《因果經》 | *Sutra of Cause and Effect* |
| 《大藏經》 | the Tripitaka (Buddhist Canon) |
| 《阿含》 | the *Agamas* |
| 《高僧傳》 | *Biographies of Eminent Monks* |
| 大悲咒 / 楞嚴咒 / 往生咒 | Great Compassion Mantra / Shurangama Mantra / Rebirth Mantra |
| 大悲懺 / 藥師懺 / 消災延壽藥師寶懺 / 水懺 | Great Compassion Repentance / Medicine Master Repentance / Jeweled Repentance of the Medicine Master for Eradicating Disasters and Lengthening Life / Water Repentance |
| 《心法》 (magazine) | *Mind Dharma* magazine (*Hsin Fa*; give "*Hsin Fa* (*Mind Dharma*)" at first occurrence) |
| 《金剛菩提海》 | *Vajra Bodhi Sea* |
| 《宣化上人開示錄》 | *Venerable Master Hua's Talks on Dharma* |
| 《虛雲老和尚畫傳集》 | *Pictorial Biography of Elder Master Hsu Yun* |
| 《增訂佛祖道影》 / 《再增訂佛祖道影》 | *Images and Biographies of the Buddhas and Patriarchs (Expanded Edition)* / *(Further Expanded Edition)* |
| 《佛祖道影白話解》 | *Vernacular Commentary on the Images and Biographies of the Buddhas and Patriarchs* |
| 《虛雲老和尚涅槃專刊》 | *Special Commemorative Issue on the Nirvana of Elder Master Hsu Yun* |
| 《虛雲老和尚法彙》 | *Collected Dharma Talks of Elder Master Hsu Yun* |
| 《虛雲老和尚年譜》 | *Chronicle of Elder Master Hsu Yun* |
| 《度輪禪師事跡》 / 《度輪法師事跡》 | *Records of Chan Master To Lun* / *Records of Dharma Master To Lun* |
| 《工商日報》 / 《華僑日報》 / 《華僑晚報》 / 《星島日報》 / 《成報》 | *Kung Sheung Daily News* / *Wah Kiu Yat Po* / *Wah Kiu Man Po* / *Sing Tao Daily* / *Sing Pao* |
| 《金山時報》 | *Chinese Times* (San Francisco) |
| 《道德經》 / 《老子》 / 《孟子》 / 《古文觀止》 | *Tao Te Ching* / *Laozi* / *Mencius* / *Guwen Guanzhi* |
| 《聖經》 | the Bible |
| 《維基百科》 | Wikipedia |

Other titles: give an English translation in italics. Add Pinyin in parentheses only for periodicals or obscure works.

### 5.6 Buddhist and monastic terms
| Chinese | English |
|---|---|
| 佛法 / 法 | the Buddhadharma / the Dharma |
| 弘法 / 弘揚佛法 | propagate the Dharma |
| 講經 / 講經說法 | lecture on the sutras / lecture on the sutras and speak the Dharma |
| 法會 | Dharma assembly |
| 開示 | instructional talk; to instruct |
| 度眾生 / 度人 | help living beings cross over / save people |
| 眾生 | living beings |
| 因緣 / 緣 | causes and conditions / affinity, conditions |
| 業 / 業障 | karma / karmic obstacles |
| 業力 | karmic power |
| 因果 | cause and effect |
| 魔 / 魔障 / 魔考 / 天魔 | demon(s) / demonic obstacles / demonic test / heavenly demons |
| 鬼 / 餓鬼 | ghost / hungry ghost |
| 鬼神 | ghosts and spirits |
| 護法神 / 護法善神 | Dharma-protecting spirits |
| 菩薩 / 佛 / 阿羅漢 / 獨覺 | Bodhisattva / Buddha / Arhat / Solitary Enlightened One (pratyekabuddha) |
| 觀世音菩薩 / 觀音 | Guanshiyin Bodhisattva / Guanyin |
| 地藏菩薩 | Earth Store Bodhisattva |
| 阿彌陀佛 | Amitabha Buddha |
| 釋迦牟尼佛 | Shakyamuni Buddha |
| 藥師佛 | Medicine Master Buddha |
| 西方三聖 | the Three Sages of the West |
| 大乘 / 小乘 | Mahayana / Small Vehicle (Hinayana) |
| 南傳佛教 | Theravada (Southern) Buddhism |
| 禪宗 / 淨土宗 / 律宗 / 天台宗 | the Chan School / the Pure Land School / the Vinaya School / the Tiantai School |
| 宗門 | the Chan lineage |
| 末法 | the Dharma-Ending Age |
| 正法 | the Proper Dharma |
| 正知正見 | proper knowledge and views |
| 慈悲喜捨 | kindness, compassion, joy, and giving (the Four Unlimited Minds; "giving" = equanimity) |
| 假名 | provisional designation |
| 入室弟子 | close disciple |
| 龍象 | dragons and elephants (outstanding monastics) |
| 堅固子 | relics (sharira) |
| 戒定慧 | precepts, samadhi, and wisdom |
| 三無漏學 | the Three Non-Outflow Studies |
| 七菩提分 | the Seven Shares of Bodhi |
| 三十七道品 | the Thirty-seven Wings of Enlightenment |
| 四念處 | the Four Applications of Mindfulness |
| 六度 | the Six Perfections |
| 五戒 / 菩薩戒 | the five precepts / the Bodhisattva precepts |
| 受戒 / 傳戒 | receive the precepts / transmit the precepts |
| 受具足戒 | receive full ordination |
| 出家 | leave the home-life (become a monastic) |
| 剃度 | shave the head and leave home (tonsure) |
| 還俗 | return to lay life |
| 修行 / 修道 | cultivate / cultivate the Way |
| 用功 | apply effort (in practice) |
| 參禪 / 坐禪 / 打坐 | investigate Chan / sit in Chan meditation / sit in meditation |
| 雙盤 | full lotus |
| 入定 / 定力 | enter samadhi / samadhi power |
| 經行 | walking meditation |
| 念佛 | recite the Buddha's name |
| 念佛堂 | Buddha Recitation Hall |
| 禪七 / 佛七 | Chan session / Buddha Recitation session (seven days; say "seven-day" where the length is not otherwise clear) |
| 早晚課 | morning and evening recitation |
| 拜懺 | bow in repentance |
| 回向 | dedicate (merit) / transfer of merit |
| 超度 | rescue (the deceased) to rebirth |
| 加持 | aid with spiritual power; bless |
| 放生 | liberate life |
| 供養 | make offerings; offering |
| 化緣 | seek alms / seek donations |
| 結緣 | establish affinities |
| 法供養 | Dharma offering |
| 善知識 | Good and Wise Advisor |
| 傳法 / 法脈 | transmit the Dharma / Dharma lineage |
| 衣缽 | robe and bowl |
| 祖師 | Patriarch |
| 開山祖師 | founding Patriarch |
| 頭陀 / 頭陀行 | dhuta / ascetic (dhuta) practices |
| 苦行 | ascetic practice |
| 涅槃 | Nirvana |
| 圓寂 / 示寂 | enter perfect stillness / manifest stillness |
| 往生 | pass away (lit. be reborn) |
| 荼毗 | cremation (jhapita) |
| 化身爐 | cremation furnace |
| 舍利 / 靈骨 | sharira / remains (bone relics) |
| 法相 | photo of the Master / Dharma image |
| 法座 | Dharma seat |
| 大殿 | Buddha Hall |
| 齋堂 | dining hall |
| 靜室 | quiet hut / hermitage |
| 茅蓬 / 茅棚 | thatched hut |
| 精舍 | vihara / hermitage |
| 道場 | Way-place (monastery / practice center) |
| 寺 / 禪寺 / 禪院 | Monastery / Chan Monastery |
| 磬 / 引磬 / 木魚 | bell (qing) / hand bell / wooden fish |
| 法器 | Dharma instruments |
| 海青 | robe (haiqing) |
| 搭衣 | put on the sash |
| 念珠 | recitation beads |
| 吃素 / 茹素 | be vegetarian |
| 齋 / 齋飯 | vegetarian meal |
| 盂蘭盆 | Ullambana |
| 佛誕 / 浴佛 | the Buddha's birthday / bathing the Buddha |
| 觀音誕 | Guanyin's birthday |
| 安居 | summer retreat |
| 打七 / 華嚴七 / 般舟七 / 彌陀七 | seven-day session / Avatamsaka session / Pratyutpanna session / Amitabha session |
| 扶乩 / 乩童 | planchette writing / spirit medium |
| 外道 | non-Buddhist path / externalist |
| 道教 / 全真派 / 呂純陽祖師 | Taoism / the Quanzhen school / Patriarch Lü Chunyang |
| 風水 / 八字 | fengshui / birth chart (eight characters) |
| 冤親債主 | karmic creditors |
| 南閻浮提眾生，其性剛強，難調難伏 | "The beings of Jambudvipa are stubborn and difficult to tame and subdue." |

### 5.7 Epithets / phrases of the Master that recur
| Chinese | English |
|---|---|
| 凍死不攀緣，餓死不化緣，窮死不求緣 | Freezing, we do not scheme. Starving, we do not beg. Dying of poverty, we ask for nothing. |
| 隨緣不變，不變隨緣 | We accord with conditions, yet do not change; we do not change, yet accord with conditions. |
| 抱定我們三大宗旨 | We hold firmly to our three great principles |
| 不爭、不貪、不求、不自私、不自利、不打妄語 | no fighting, no greed, no seeking, no selfishness, no pursuit of personal advantage, and no lying |
| 打妄想 | have idle thoughts; 妄想 false thinking |
| 業風 | karmic winds |

---

## 6. Gender table (for pronouns and Upasaka/Upasika)
Female: Tan Guo Zheng, Tan Guo Shi, Gan Guo Yan, Yu Guo Man, Xue Guo Feng, Liu Guo Juan, Luo Guo Ming, Huang Guo Song, Wang Guo Hai, Chen Kuan Man, Yuan Guo Xiang, Yuan Guo Zhen, Yuan Guo Lin, Guo Shu, Cai/Xue Guo Su, Guo Hong, Guo Quan, Guo Gen, Hu Guo Wei, Mei Miaoling, Xu Xiangjun, Zhong Meiwei, Ruan Guo Ni, Jin Ci (Guo Sen), Heng Yi (Guo Li), Heng Qi (Guo Ren), Heng Wei, Heng He, Heng Chih.
Male: the Venerable Master, Tan Guo Pu, Wen Guo Mi, Yu Guo Xing, Huang Guo Jun, Chen Ruichang, Li Guo Yuan, Li Guo He, Guo Ping, Pei Guo Jian, Wu Yingcai, Zhan Liwu, Heng Ding, Heng Yue, Heng Zhi, Heng Sure, Heng Ju, Heng Yo.
Anyone else: decide from context. If the context does not tell you, avoid gendered words and log the person in your queries file.

---

## 7. Errata, queries, and new terms (each translator writes these)

- `errata_XX.md`: one line per source error you corrected, in the form `P0123 | source: 也風 | intended: 業風 | rendered as "karmic winds"`. Also log heading-number anomalies, apparent omissions in the source, and garbled passages.
- `queries_XX.md`: genuine uncertainties, in the form `P0123 | issue | what you chose`.
- `newterms_XX.md`: every proper noun or technical term **not** in this glossary, in the form `Chinese | English chosen | first ID in your batch | note added? (y/n)`.
