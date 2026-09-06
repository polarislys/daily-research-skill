---
name: daily-research
description: 按 config/keywords.md 检索过去 24 小时的 Agent 工程、训练、评估与垂域动态，写成金字塔结构的约 2000 字深挖文章，存到 output/主题-日期/ 并推送到 GitHub。用于每日定时调研、补跑简报，或用户提到 harness、loop engineer、agent runtime、agent eval、skill-rag、skill-graph、FDE、垂域落地、岗位 JD 演进时。
---

# 每日 Agent 岗位雷达

读者是 AI 应用研发 / 应用优化 / Agent 优化 / Agent 训练与优化工程师，目标是端到端 Agent 架构师：能搭、能跑、能评、能训、能垂域落地。文章要帮他比老板看得更多、更远。JD 会变，检索轴是 [config/keywords.md](../../../config/keywords.md)，不是写死在 skill 里的旧词。

产物只写 git，推到 https://github.com/polarislys/daily-research-skill 。禁止写本机桌面。

## 何时使用

- Cursor Automation 每天 10:00（Asia/Shanghai）启动本仓库
- 用户说「跑每日调研」「daily research」「补跑昨天的雷达」
- 用户要按当前 JD 关键词扫过去 24 小时的仓库 / 博客 / 视频 / 公司动态

## 每日流程

1. 读 [config/keywords.md](../../../config/keywords.md) 的**概念行**（`id` + 中英检索列）。无有效概念则在 `output/检索失败-YYYY-MM-DD/article.md` 写明原因，仍提交推送。
2. 日期用 **Asia/Shanghai 当天**。检索窗口是 **过去约 24 小时**。
3. **分语种检索，按同义词对齐，不要当成两个主题：**
   - 国外源（GitHub、美厂博客/careers、HN、YouTube）：用该概念的 `en` + `en_aliases`
   - 国内源（厂官网、招聘站、知乎/公众号、B 站）：用 `zh` + `zh_aliases`
   - 产品名、协议名（MCP、dsh、hermes）中英都用原名
   - 一篇文章只讨论 **一个 id**（或紧密相关的两个），中英命中合并写，规范名用 `id`
4. 对每个概念收集素材（有就收，没有在文末写「未覆盖」）：
   - 新工程代码仓库
   - 知识博客 / 论文解读
   - 视频讲解（YouTube、Bilibili 等）
   - 大佬常看的公司动态：新技术、新训练模型、新 harness（如 dsh）、新 agent 产品（如 hermes）、新投资赛道
   - 工程师工作模式变化：堆最强模型 → 优秀模型 + harness 工程 → 垂域落地
5. **不要写总览流水账。** 从命中里只挑 **2～4 个真正值得挖的问题点**，合并成 **2～4 篇文章**。每篇只分析 **1～2 个问题点**，约 **1800～2200 汉字**。
6. 每篇文章写入独立目录：

   `output/<主题>-<YYYY-MM-DD>/article.md`

   主题用短中文或英文词，去掉 `/ \ : * ? " < > |`。同日同主题加 `-2`。目录内可另放 `sources.md`（链接清单）。
7. 更新 [output/README.md](../../../output/README.md)：最新日期在上，链到各篇文章。
8. **先开探索通道，再维护词表**（见「自我进化」）。更新 [config/candidates.md](../../../config/candidates.md)；达到阈值再改 [config/keywords.md](../../../config/keywords.md)（中英两列一起补）。
9. 提交并推送到 **main**。说明：`Daily research: YYYY-MM-DD`。不要开 PR。只暂存 `output/`、`config/candidates.md`，以及本次晋升过的 `config/keywords.md`。

检索失败也要留下当天一篇说明文并推送，让日程有痕迹。

## 选材：宁少挖深

优先选同时满足的信号：

- 24 小时内有可核对的一手来源
- 碰到岗位能力的其中一截：runtime / harness / eval / 训练 / 上下文 / skill 体系 / 垂域落地 / FDE
- 能往下挖两层（是什么 → 怎么做/为何现在出现 → 对工作方式的含义）

丢掉：营销通稿、无仓库无数字的「赋能」、重复转载、无法解释术语的标题党。

国内外都要扫。英文源保留原名，中文里给译法。

## 每篇文章：金字塔，向下两层

先给判断，再给证据，最后才是细节。禁止按时间线记流水账。禁止一篇里摊开 5 个无关新闻。

```markdown
# <判断句标题，不要「日报」「观察」这种空标题>

日期：YYYY-MM-DD（Asia/Shanghai）  
问题点：<1 个，最多 2 个>  
关键词：<来自 keywords.md>

## 结论

用 8～12 行先回答：发生了什么、为什么值得这个岗位现在理清、若属实下一步该动手的是哪一层（搭 / 跑 / 评 / 训 / 垂域）。

## 问题界定

只圈住 1～2 个问题。写清「不讨论什么」，避免滑成行业综述。

## 第一层：对象是什么

对文中每个关键术语给 **2～5 句可执行的概念解释**（它解决哪类失败、和相邻词差在哪）。至少解释本文真正用到的词，例如：harness、loop engineer、agent runtime、agent eval、FDE、上下文管理、skill 自进化、skill-rag、skill-graph。
然后写清过去 24 小时里**具体出现了什么**（产品名、仓库、模型、融资），不要只写形容词。

## 第二层：机制与岗位含义

再往下挖一层，只选一条主线：

- 工程：runtime / harness / 循环 / 评估怎么接
- 训练：数据、反馈、和评测闭环
- 落地：垂域约束、上下文预算、skill 如何长
- 工作模式：为何从「最强模型」挪到「够用模型 + harness」或「垂域」

必须落到「我明天能做的一个具体动作」，不要「持续关注」。

## 证据（24h）

分类列出，每条：事实一句话 + URL + 时间（若有）。没有的类别写「本日未见」。

- 仓库：
- 博客 / 文档：
- 视频：
- 公司 / 产品 / 融资：

## 未证实

矛盾说法、只有二手转述、无法打开的链接。
```

## 术语底线（出现就要解释，不要当读者已会）

| 词 | 解释时抓住的差 |
|---|---|
| harness | 包在模型外的循环、工具、权限、重试、评测夹具；不是又一个 chatbot 皮肤 |
| loop engineer | 设计「模型 → 行动 → 观察 → 再进入」的人，优化的是环，不是单次 prompt |
| agent runtime | 一次 agent 跑起来时的进程/沙箱/状态/工具总线 |
| agent eval | 对轨迹、任务成功率、成本、回归的测量，不是 chatbot 打分 |
| FDE | Forward Deployed Engineer：把能力嵌进客户现场流程的人，不是只交 API |
| 上下文管理 | 决定进窗口的是记忆、检索、摘要还是 skill，以及何时丢弃 |
| skill 自进化 | skill 根据失败轨迹改自身说明书/脚本，要有写入与评审，不是模型自己变聪明 |
| skill-rag | 用检索选/填 skill，而不是只检索文档片段 |
| skill-graph | skill 之间的依赖、互斥、调用边，用来编排而不是平铺一堆 SKILL.md |

用户点名的例（dsh、hermes）只当「产品信号」检索，证实后再写，不要把传闻写成已发布。

## 自我进化：旧词开采 + 新词探索

只靠 keywords 检索，新词出现概率会偏低——这是闭环，不是疏忽。每日必须做两件事：**用旧词挖深（开采）**，**不靠旧词找叫法（探索）**。新词先记账，达标再晋升，禁止「今天看到一次就改主词表」。

### 开采（依赖 keywords）

用已有 `id` 的中英检索词搜 24h 材料。从标题、JD 原文、README、论文摘要里**摘共现新串**（岗位名、方法名、产品名）。已在 keywords 或 candidates 的跳过。其余写入 candidates，`near` 填最像的旧 id。

### 探索（禁止只用旧 id 当查询）

每天至少跑完下面 4 条，查询用**角色/渠道/时间**，不要复制 keywords 列表：

1. **招聘页**：OpenAI、Anthropic、Cursor、字节、腾讯、阿里、月之暗面 careers 近 24h/「最新」列表。抽出岗位标题和职责里的新名词。
2. **新仓库**：GitHub 近 24h，主题或描述含 `agent` / `agentic` / `智能体`（不要再加 harness 等旧词收窄）。看 README 自造词和产品名。
3. **时间线**：HN、arXiv（cs.AI / cs.CL / cs.SE）、机器之心/36 氪首页里和 Agent、模型、评测相关的新标题。
4. **开放句式**（中英各搜一轮）：`we're hiring agent`、`announcing agent`、`招聘 Agent 工程师`、`发布 智能体`、`new job title agent`。

探索命中若能成篇，可以写进当天 2～4 篇里的一篇，主题用新词，并在文内标明「候选，尚未进主词表」。

### 记账与晋升

更新 [config/candidates.md](../../../config/candidates.md)：

- 已有 `token`：刷新 `last`、`days`、`sources`、`urls`
- 新 `token`：`status: watching`，补 en/zh（能猜到的对照）
- 达到该文件里的**晋升阈值**，且能写清与旧 id 的差别 → 写入 keywords 完整对照行，candidates 标 `promoted`
- 只是旧 id 的别称 → 加到该 id 的 `en_aliases` 或 `zh_aliases`，candidates 标 `rejected`，note 写「并入 id: …」
- 旧 keywords id 连续 30 天开采+探索都无命中、且已被更精确 id 替代 → 移到 keywords「降权」

不要改本 SKILL.md，除非用户明确要求改写作或进化规则。

## 硬性规则

- 简体中文；每篇 1800～2200 汉字；不够就少写一篇，禁止注水
- 事实必须带可打开的 URL；禁止编造仓库、视频、融资
- 一篇 1～2 个问题点，必须有「第一层 + 第二层」
- 不写密钥、Cookie、本机路径
- 同日目录已存在则更新该篇，不另开「最终版」副本
