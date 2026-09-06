---
name: daily-research
description: 按三类通道检索 Agent / 模型 / 方法动态，写成产品剖析、新方法原理或新闻动态文章，扁平落在 output/ 并推送到 GitHub。用于每日定时调研、手动补跑，或用户提到跑 daily-research、补跑雷达、产品拆解、新方法、发布评测时。
---

# 每日调研

把过去约 24 小时里值得讲透的东西写成文章，推到 https://github.com/polarislys/daily-research-skill 。只写 git，禁止写本机桌面。

**不要写岗位。** 读者要看懂产品怎么构成、新方法怎么转、新闻里的模型/发布到底改了什么。不要写「对 XX 岗意味着什么」「明天这个岗位该动手哪一层」「JD 怎么变」。

检索轴是 [config/keywords.md](../../../config/keywords.md)。过滤规则是 [config/profile.md](../../../config/profile.md)、[config/sources.md](../../../config/sources.md)、[config/rejected.md](../../../config/rejected.md)。词会变，不要把旧词写死在本文件里。

## 何时使用

- Cursor Automation 每天 10:00（Asia/Shanghai）启动本仓库
- 用户说「跑每日调研」「daily research」「补跑雷达」或用 `/daily-research`
- 用户要按当前关键词扫过去 24 小时的产品 / 方法 / 新闻

## 三种产物，分类检索

每天**按形态分开搜**，不要用同一串词扫完全网再硬塞进一篇。命中不够就少写该形态，不要凑篇。

| 形态 | 落盘 | 写什么 | 检索通道（优先这个形态的源） |
|---|---|---|---|
| 产品剖析 | `output/<短标题>-YYYY-MM-DD.md` | 把一个已经能摸到的产品讲透：模块怎么拼、核心理念是什么、环怎么转 | 官方博客 / 架构文 / 文档 / GitHub README 与 RFC；中文深度博文只当问题入口，必须回到一手源 |
| 新方法 | 同上 | 讲清一个较新的名词或算法：它解决哪类失败、步骤怎么走、和旧方法差在哪 | arXiv 近窗、实验室博客、会议页 |
| 新闻动态 | 同上 | 一次发布或事件：改了什么、论坛/用户怎么评 | 官方发布、HN、论坛、评测 |

**output 下不要子文件夹**，只有文章 md 和 `收件箱-YYYY-MM-DD.md`。同一产品多篇用不同短标题区分（如两篇 Codex 用两个文件名）。

一篇文章只讲 **1～2 个问题点**，**约 2000 汉字**，机制写透。参考口吻：[宝玉《Warp》](https://mp.weixin.qq.com/s/1YaHaOC1veK3dJhlJyvE9Q)；写作细则见 [STYLE.md](STYLE.md)。

## 每日流程（两阶段）

日期用 **Asia/Shanghai 当天**。检索窗口约 **过去 24 小时**；产品剖析允许引用稍早的官方架构文，但必须标明日期，且当天要有新由头才开写或续写。

### Phase 1 — Filter（先写收件箱）

1. 读 [config/keywords.md](../../../config/keywords.md)、[config/profile.md](../../../config/profile.md)、[config/sources.md](../../../config/sources.md)、[config/rejected.md](../../../config/rejected.md)。无有效 keywords 行也要写收件箱说明。
2. **分形态检索**（与下表通道一致），收集候选，不要立刻深写：
   - 产品剖析：产品专名 + `architecture` / `how we built` / `拆解` / `开源`
   - 新方法：`we introduce`、`preprint`、方法名
   - 新闻动态：`announcing`、`released`、`发布`、`评测`、`hands-on`
   - 国外源用 `en` + `en_aliases`；国内源用 `zh` + `zh_aliases`
3. 对每条候选打分（规则见 profile 的「综合分」），分为 **通过 / 待定 / 丢弃**。遵守 `inbox_max`。
4. 落盘收件箱：

   ```text
   output/收件箱-<YYYY-MM-DD>.md
   ```

   结构用 [templates/inbox.md](templates/inbox.md)。**链接必须写成 Markdown `[文字](https://...)`**，深写链到相对路径；禁止把 URL 放在代码块里。

### Phase 2 — 深写（按预算）

5. 从收件箱「建议深写: yes」按 score 排序，取前 **`deep_write_max`** 条（见 profile）。其余标 `queued` 写回待定区。
6. 对选中项写长文。一篇 **1～2 个问题点、约 2000 汉字**，机制写透。没有材料就少写，禁止注水凑字数。
7. 落盘（**不要子文件夹**）：

   ```text
   output/<短标题>-<YYYY-MM-DD>.md
   ```

   - 短标题去掉 `/ \ : * ? " < > |`
   - 文首 YAML frontmatter 写 `形态`、`主题`、`日期`
   - 同日同题更新原文件
8. 在收件箱文末填「深写链接」；更新 [output/README.md](../../../output/README.md)。
9. 跑「自我进化」：更新 [config/candidates.md](../../../config/candidates.md)；达标再改 keywords。
10. 提交并推送 **main**。说明：`Daily research: YYYY-MM-DD`。不要开 PR。暂存 `output/`、`config/candidates.md`，以及本次改过的 `config/keywords.md`、`config/rejected.md`。

## 选材

优先同时满足：

- 有可打开的一手 URL（官方文、论文、仓库、可核对的行情）
- 能讲清一个机制，而不是形容词
- 对产品 / 方法 / 发布三者之一有增量

丢掉：营销通稿、无数字的「赋能」、重复转载、标题党、岗位/招聘综述。

中文深度博文（如公众号）可以当**问题入口**：用它圈住 1 个问题，再回到官方英文源把机制写全。不要只编译公众号。

## 每篇文章

先判断，再机制，最后证据。禁止时间线流水账。

字数：**目标约 2000 汉字**（1800～2500）。写透 1～2 个问题；机制篇幅应占全文一半左右。超过 3000 就拆成两篇不同短标题的文件。禁止注水。

结构按形态选用模板（**落盘前必读** [STYLE.md](STYLE.md)）：

- 产品剖析 → [templates/product.md](templates/product.md)
- 新方法 → [templates/method.md](templates/method.md)
- 新闻动态 → [templates/news.md](templates/news.md)

写作标杆：[宝玉《Warp 如何让 Agent 自我进化》](https://mp.weixin.qq.com/s/1YaHaOC1veK3dJhlJyvE9Q)——问题驱动、有叙事、术语在句子里解释，不要 wiki 填表体。

三条共用底线：

- 标题是判断句，不要「日报」「观察」
- **专业词保留英文或行业固定叫法**（harness、DPO、GRPO、PRM、MCP、Skill、TTFT、credit assignment 等），不要用「夹具」「执行环」等白话替换它们
- 专业词**第一次出现**用 2～5 句白话解释它解决哪类失败；**其余段落**尽量短句、好懂
- 每条事实带 URL
- 不写「对岗位的动作」；需要收束时写**机制上可复查的一点**（例如「改进 Skill 必须走 PR」），不要写「你明天去改简历」

## 术语底线（出现就要解释）

| 词 | 抓住的差 |
|---|---|
| harness | 包在模型外的循环、工具、权限、重试、夹具；不是 chatbot 皮肤 |
| agent runtime | 一次跑起来时的进程 / 状态 / 工具总线 |
| sandbox | 不信任代码跑在哪、隔离到哪一级；MCP 协议本身不是沙盒 |
| skill | 文件化的程序性知识（怎么做），可 diff、可评审 |
| 记忆 / memory | 推理时自动写入、一直在变；和 skill 不是同一个东西 |
| skill 自进化 | 根据反馈改 skill 文件，要有写入和人审 |
| credit assignment | 稀疏终局奖励下，给中间每一步打功过 |

产品名（dsh、hermes、Warp、Codex）证实后再写，不要把传闻写成已发布。

## 自我进化

只靠旧词会漏新叫法。每日：**开采**（用 keywords 挖共现）+ **探索**（不靠旧 id 找叫法）。新词先记账，达标再晋升。

### 开采

用已有 id 的中英词搜 24h。从论文摘要、资讯标题、官方博客、README 摘共现新串。招聘 JD **不要搜、不要当来源**。

### 探索（按形态各至少跑一轮开放句式）

1. **新方法 / 论文（最高）**：arXiv `cs.AI` / `cs.CL` / `cs.SE` / `cs.LG` 近 24h；抽自造方法名
2. **产品与资讯（最高）**：HN、OpenAI / Anthropic / Google / DeepSeek 等官方博客、机器之心 / 量子位 / 36氪 的「发布 / 开源 / 拆解」
3. **仓库与视频（高）**：GitHub 近 24h 含 `agent` / `智能体`；YouTube / B 站评测与架构讲解
4. **新闻与市场（仅新闻动态形态）**：发布稿、论坛评价、公开股价/融资；没有公开数据就写「未见」，不要编

开放句式：`announcing`、`we introduce`、`preprint`、`发布`、`开源`、`拆解`、`评测`。不要用招聘语。

### 记账与晋升

规则见 [config/candidates.md](../../../config/candidates.md)。说不清与旧 id 的差 → 只加 alias。产品名进 keywords 的「产品」区，不新开概念 id。

不要改本 SKILL.md，除非用户明确要求改写作或目录规则。

## 硬性规则

- 简体中文；一篇 1～2 个问题点
- 事实带可打开的 URL；禁止编造仓库、视频、融资、股价
- 不写岗位、JD、简历、职级
- 不写密钥、Cookie、本机路径
- 文件夹是大主题，文件名带日期
