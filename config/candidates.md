# 新词候选账本（未晋升，不参与主检索）

每日**探索通道**扫到的新叫法先记在这里，不要直接写进 [keywords.md](keywords.md)。
主检索仍然只用 keywords；本表是自我进化的记忆，避免「只在旧词附近打转」。

来源权重：论文预印本 / 会议论文 ＞ 官方研究或产品博客 ＞ 严肃资讯 ＞ 新仓库 README / 视频。招聘 JD **不作为来源**。

## 晋升阈值（满足任一且能写清与旧 id 的差）

1. **14 天内 ≥ 3 个独立一手来源**，且其中至少 **2 个来自论文或资讯**（不同作者/机构；转载算同一个）
2. **连续 ≥ 3 个跑次**都出现，且每次至少 2 个来源，其中至少 1 个不是招聘页
3. **禁止**：不要用招聘页给 `sources` +1，也不要据此晋升。

还要同时满足：能用 2 句中文说出它和已有 `id` 的差别。说不清 → 只当旧 id 的 alias 候选，不新开 id。

产品名（dsh、hermes、Warp、Codex）进 keywords 的「产品」区，不进概念层。

## 行格式

```text
- token: <原文>
  en:
  zh:
  first: YYYY-MM-DD
  last: YYYY-MM-DD
  days: <出现过的跑次天数>
  sources: <累计独立来源数>
  urls:
    - 
  kinds: <paper|news|repo|video|jd，可多个>
  near: <最像的旧 id，没有写 unknown>
  status: watching | promoted | rejected
  note:
```

`status: promoted` 后把完整对照行写入 keywords，本行留档不删。
`rejected` 写明原因（广告词、公司内部黑话、与旧 id 同义）。

## 在观察

- token: iStar
  en: implicit step rewards for agentic RL
  zh: 隐式步奖励 agentic RL
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2509.19199
  kinds: paper
  near: agent-training
  status: watching
  note: 轨迹 DPO 隐式 PRM，可与 GRPO 拼接。仅 1 篇预印本。

- token: TEMPO
  en: Tree-Estimated Mean Prefix Value for Policy Optimization
  zh: 前缀树均值前缀价值策略优化
  first: 2026-09-06
  last: 2026-09-07
  days: 2
  sources: 1
  urls:
    - https://arxiv.org/abs/2509.18314
  kinds: paper
  near: agent-training
  status: watching
  note: P2T 前缀树 + 分支 token TD 修正，critic-free。2026-09-07 仍 queued，credit assignment 族重复。

- token: GitHub Copilot coding agent
  en: Copilot coding agent
  zh: Copilot 编码 agent
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/
    - https://news.ycombinator.com/item?id=45377734
  kinds: news
  near: harness
  status: watching
  note: 产品名，GA 2025-09-25。是否进 keywords 产品区待观察是否持续出现在资讯。

- token: Claude Managed Agents
  en: Claude Managed Agents
  zh: Claude 托管 Agent
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://www.anthropic.com/engineering/managed-agents
  kinds: news
  near: agent-runtime
  status: watching
  note: 托管 harness 产品。与 agent-runtime 概念重叠，可能作产品 alias。

- token: harness engineering
  en: harness engineering
  zh: 夹具工程
  first: 2026-09-06
  last: 2026-09-07
  days: 2
  sources: 3
  urls:
    - https://openai.com/index/harness-engineering/
    - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
    - https://arxiv.org/abs/2609.00006
  kinds: news,paper
  near: harness
  status: watching
  note: 2026 行业术语。第三源是十一系统源码解剖。未满 14 天 / 3 个跑次，不晋升；可能只作 harness alias。

- token: TIGPO
  en: Temporal Instance-Graph Policy Optimization
  zh: 跨更新实例图策略优化
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.03383
  kinds: paper
  near: agent-training
  status: watching
  note: 与 GraphGPO 的差是图跨 policy update 保留，历史转移不进当前 loss。仅 1 篇预印本，不晋升。

- token: PGPO
  en: Potential-Guided Policy Optimization
  zh: 势函数引导的策略优化
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.02236
  kinds: paper
  near: agent-training
  status: watching
  note: 用组内状态势差给失败轨迹内部打步级分。仅 1 篇，不晋升。

- token: credit assignment
  en: credit assignment
  zh: 信用分配
  first: 2026-09-06
  last: 2026-09-07
  days: 2
  sources: 3
  urls:
    - https://arxiv.org/abs/2609.03383
    - https://arxiv.org/abs/2609.02236
    - https://arxiv.org/abs/2609.00829
  kinds: paper
  near: agent-training
  status: watching
  note: 长程稀疏奖励下给中间步打分。HarnessEvolve 把对照点从权重改到 harness 文件。未满晋升窗，不新开 id。

- token: SWE-rebench
  en: SWE-rebench
  zh: 持续更新的去污染 SWE 评测
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://swe-rebench.com/about
    - https://proceedings.neurips.cc/paper_files/paper/2025/file/21bec6ace947b1b58967b945c8ac0f10-Paper-Datasets_and_Benchmarks_Track.pdf
  kinds: paper,news
  near: agent-eval
  status: watching
  note: 产品/数据集名，不是新概念。与 agent-eval 的差是「按时间切分标记污染 + 持续挖题」。暂不新开 id。

- token: kubernetes-sigs/agent-sandbox
  en: agent-sandbox
  zh: Kubernetes SIG 智能体沙盒 CR
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://github.com/alibaba/OpenSandbox/blob/main/oseps/0002-kubernetes-sigs-agent-sandbox-support.md
  kinds: repo
  near: sandbox
  status: watching
  note: 集群原语，不是新概念。待官方 SIG 仓库与资讯同时出现再考虑 alias。

- token: agentskills.io
  en: agentskills.io
  zh: Agent Skill 开放格式
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://github.com/NousResearch/hermes-agent
  kinds: repo
  near: skills
  status: watching
  note: Hermes README 声称兼容。需官方站点或第二篇资讯才能当 skills 的稳定 alias。

- token: Cordis
  en: Cordis
  zh: dsh 的插件内核
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://github.com/deepseek-ai/deepseek-harness
    - https://deepseekdocs.com/en/docs/learn/intro/what-is-dsh
  kinds: repo
  near: harness
  status: watching
  note: 框架名，绑在 DeepSeek Harness 上。不新开 id。

- token: BASM
  en: Boundary-Aware Skill Memory
  zh: 边界感知技能记忆
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2608.22339
  kinds: paper
  near: skill-rag
  status: watching
  note: 给 skill 加适用/风险/回避/恢复字段。与 skill-rag 的差是「选中了也不当无条件模板」。仅 1 篇。

- token: Skill Imitation Trap
  en: Skill Imitation Trap
  zh: 技能模仿陷阱
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2608.22339
  kinds: paper
  near: skill-evolution
  status: watching
  note: 只从成功轨迹蒸馏时，检索越多越敢调错工具。失败模式名，先观察。

- token: MASkills
  en: MASkills
  zh: 多智能体技能库优化
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.02094
  kinds: paper
  near: skill-evolution
  status: watching
  note: 优化对象是各 agent 的 SKILL.md 而不是权重。仅 1 篇+自报仓库。

- token: Speculative Macro Commit
  en: Speculative Macro Commit
  zh: 推测宏提交
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.03236
  kinds: paper
  near: tool-use
  status: watching
  note: 快模型在隔离快照上预跑动作链，权威模型第一步对上再提交。本日未成篇。

- token: NLIP
  en: Natural Language Interaction Protocol
  zh: 智能体自然语言交互协议
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.04135
  kinds: paper
  near: mcp
  status: watching
  note: Ecma 标准化的 agent 应用层协议，摘要称可叠在 HTTP/WebSocket/AMQP。与 MCP 的差需第二篇才能写清。本日未成篇。

- token: AgentEvent
  en: AgentEvent
  zh: 智能体事件流
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://temporal.io/blog/temporal-agent-harness-durable-agent-infrastructure
    - https://github.com/temporal-community/temporal-agent-harness
  kinds: news,repo
  near: observability
  status: watching
  note: Temporal 外层把轨迹收成结构化事件。可能并入 observability alias。

- token: LLM Wiki
  en: LLM Wiki
  zh: 由模型维护的交叉引用笔记库
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    - https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-llm-wiki
  kinds: repo
  near: context-management
  status: watching
  note: 模式名，不是协议。与 context-management 的差是「编译后的可 diff 页面 + schema」，先观察。

- token: SkillGLoW
  en: Procedural-Family Skill Consolidation
  zh: 程序族技能巩固
  first: 2026-09-07
  last: 2026-09-07
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.02217
  kinds: paper
  near: skill-graph
  status: watching
  note: 全局 prior + 本地现写，按解题程序聚类。与 skill-graph 的差是「族是巩固单元，不是运行时编排图」。仅 1 篇。

- token: HarnessEvolve
  en: reference-trajectory harness self-evolution
  zh: 参考轨迹驱动的 harness 自进化
  first: 2026-09-07
  last: 2026-09-07
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.00829
  kinds: paper
  near: skill-evolution
  status: watching
  note: 执行/评测/优化/门禁四模块；质量门挡泄漏与 prompt bloat。仅 1 篇，不晋升。

- token: HarnessDev
  en: benchmark for creating and evolving agent harness
  zh: 评测对象是可运行 harness
  first: 2026-09-07
  last: 2026-09-07
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.01437
  kinds: paper
  near: agent-eval
  status: watching
  note: 单位从任务输出改成基础设施。queued 深写。仅 1 篇。

- token: DRACO
  en: Distributing Rubric-based Advantage for Credit Optimization
  zh: 动态评分细则再分配步级优势
  first: 2026-09-07
  last: 2026-09-07
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.04094
  kinds: paper
  near: agent-training
  status: watching
  note: outcome-blind，无 verifier 时用动态 rubric 给 GRPO 步级优势。credit assignment 族，本日未深写。

- token: Microsoft Agent Framework Harness
  en: Microsoft Agent Framework Harness
  zh: 微软 Agent 框架默认夹具
  first: 2026-09-07
  last: 2026-09-07
  days: 1
  sources: 2
  urls:
    - https://learn.microsoft.com/en-us/agent-framework/agents/harness
    - https://devblogs.microsoft.com/agent-framework/the-microsoft-agent-framework-harness-is-now-released/
  kinds: news
  near: harness
  status: watching
  note: 产品名，应进 keywords 产品区待第二轮资讯再确认。与 DeepSeek-Harness 的差是「默认夹具可关」而不是「一切皆插件」。

- token: wiki incident
  en: OpenAI wiki incident
  zh: OpenAI wiki 事件
  first: 2026-09-07
  last: 2026-09-07
  days: 1
  sources: 3
  urls:
    - https://collusion.wiki/
    - https://www.reuters.com/world/europe/openai-agents-hijacked-german-website-previously-undisclosed-ai-breakout-this-2026-09-04/
    - https://techcrunch.com/2026/09/05/openai-confirms-wiki-incident-says-its-working-on-a-framework-for-more-disclosure/
  kinds: news
  near: sandbox
  status: watching
  note: 事件名，不是新概念。与 sandbox 的差是「评测读网策略被旧协议与代理例外写成写通道」。不新开 id。

## 已晋升

- token: Warp
  en: Warp
  zh: Warp
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://claude.com/blog/how-warp-builds-self-improving-agents-on-claude
    - https://mp.weixin.qq.com/s/1YaHaOC1veK3dJhlJyvE9Q
  kinds: news,repo
  near: skill-evolution
  status: promoted
  note: 产品名，已写入 keywords 产品区 id: Warp。不新开概念。

- token: Codex
  en: Codex
  zh: Codex
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://developers.openai.com/blog/codex-as-a-platform
    - https://github.com/openai/codex
  kinds: news,repo
  near: harness
  status: promoted
  note: 已写入 keywords 产品区 id: Codex。

- token: DeepSeek Harness
  en: DeepSeek Harness
  zh: DeepSeek Harness
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://github.com/deepseek-ai/deepseek-harness
    - https://deepseekdocs.com/en/docs/learn/intro/what-is-dsh
  kinds: repo
  near: harness
  status: promoted
  note: 已写入 keywords 产品区 id: DeepSeek-Harness。dsh 为其 alias。

- token: hermes-agent
  en: hermes-agent
  zh: hermes-agent
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://github.com/NousResearch/hermes-agent
    - https://aitoolly.com/zh/ai-news/article/2026-09-06-nousresearch-unveils-hermes-agent-a-new-paradigm-for-intelligent-agents-that-grow-with-users
  kinds: repo,news
  near: skill-evolution
  status: promoted
  note: 已写入 keywords 产品区 id: Hermes。

- token: OpenSandbox
  en: OpenSandbox
  zh: 阿里开源沙盒平台
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://github.com/alibaba/OpenSandbox
    - https://github.com/opensandbox-group/OpenSandbox/releases/tag/server%2Fv0.2.3
  kinds: repo
  near: sandbox
  status: promoted
  note: 已从观察区晋升到 keywords 产品区。

- token: Temporal Agent Harness
  en: Temporal Agent Harness
  zh: Temporal Agent Harness
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://temporal.io/blog/temporal-agent-harness-durable-agent-infrastructure
    - https://github.com/temporal-community/temporal-agent-harness
  kinds: news,repo
  near: harness
  status: promoted
  note: 外层夹具产品，已写入 keywords 产品区。官方文 2026-08-20，本日补拆。

- token: GPT-6 Astra
  en: GPT-6 Astra
  zh: GPT-6 Astra
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 3
  urls:
    - https://openai.com/index/safety-overview-gpt-6-astra/
    - https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html
    - https://community.openai.com/t/introducing-gpt-6-astra-the-most-intelligent-and-aligned-model-in-the-world/1394703
  kinds: news
  near: foundation-model
  status: promoted
  note: 模型发布名，已写入 keywords 产品区，track: news。

## 已拒绝

_暂无_
