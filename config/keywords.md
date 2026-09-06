# 检索轴（中英对照）

每日调研**只认本文件的概念行和产品行**。国内源用中文列，国外源用英文列，文章里用 `id` 做规范名。

- `<!--` 开头的行忽略
- `首次` 用 `YYYY-MM`
- `track`：`product` 走产品剖析，`method` 走新方法，`news` 走新闻动态；可写多个，逗号分隔
- 同义词只写检索会用到的别称

本表是**检索轴**，不是岗位词表。不要为了对齐 JD 加词。

## 怎么搜

| 形态 | 源 | 用哪一列 |
|---|---|---|
| 产品剖析 | 官方博客、文档、GitHub、架构长文 | 产品专名 + 该产品相关概念的 `en`/`zh` |
| 新方法 | arXiv、实验室博客、会议 | 概念的 `en`/`zh` + 开放句式 `we introduce` |
| 新闻动态 | 发布稿、HN、论坛、评测、公开行情 | 产品/模型专名 + `released` / `发布` / `评测` |

## 格式

```text
- id: <规范名>
  en: <英文主检索>
  en_aliases: <英文同义，逗号分隔>
  zh: <中文主检索>
  zh_aliases: <中文同义>
  track: product | method | news
  首次: YYYY-MM
```

## 概念

### 环与文件化知识

- id: harness
  en: agent harness
  en_aliases: harness, agent loop, scaffolding, inner harness, outer harness
  zh: Agent Harness
  zh_aliases: 智能体运行基座, 执行环, 智能体夹具, 内层夹具, 外层夹具
  track: product, method
  首次: 2026-09

- id: tool-use
  en: tool use
  en_aliases: tool calling, function calling, tool routing
  zh: 工具调用
  zh_aliases: 工具编排, Function Calling
  track: product, method
  首次: 2026-09

- id: skills
  en: agent skills
  en_aliases: SKILL.md, skill system, Agent Skills
  zh: Agent Skill
  zh_aliases: 技能模块, Skills
  track: product, method
  首次: 2026-09

- id: mcp
  en: MCP
  en_aliases: Model Context Protocol
  zh: MCP
  zh_aliases: 模型上下文协议
  track: product, method
  首次: 2026-09

- id: skill-rag
  en: skill-rag
  en_aliases: skill retrieval, retrieve skills
  zh: skill-rag
  zh_aliases: 技能检索, Skill RAG
  track: method
  首次: 2026-09

- id: skill-graph
  en: skill-graph
  en_aliases: skill graph, skill orchestration
  zh: skill-graph
  zh_aliases: 技能图谱, Skill 编排
  track: method
  首次: 2026-09

- id: skill-evolution
  en: skill self-evolution
  en_aliases: self-improving skills, evolving skills, self-improving agents
  zh: skill自进化
  zh_aliases: 技能自进化, Skill 自我迭代
  track: product, method
  首次: 2026-09

### 运行时与上下文

- id: agent-runtime
  en: agent runtime
  en_aliases: execution engine, agent orchestration
  zh: Agent Runtime
  zh_aliases: 执行引擎, 智能体运行时
  track: product
  首次: 2026-09

- id: sandbox
  en: sandbox
  en_aliases: sandboxed execution, isolation
  zh: 沙盒
  zh_aliases: 沙箱, 隔离执行
  track: product
  首次: 2026-09

- id: observability
  en: agent observability
  en_aliases: tracing, trajectory, OpenTelemetry
  zh: 可观测性
  zh_aliases: 轨迹追踪, Trace, 链路回放
  track: product, method
  首次: 2026-09

- id: context-management
  en: context management
  en_aliases: context engineering, context construction, compaction, memory
  zh: 上下文管理
  zh_aliases: 上下文工程, 长上下文, 记忆管理
  track: method, product
  首次: 2026-09

- id: long-horizon
  en: long-horizon
  en_aliases: long-running tasks, long-horizon agents
  zh: 长程任务
  zh_aliases: 长程执行, 长时程 Agent
  track: method
  首次: 2026-09

- id: computer-use
  en: computer use
  en_aliases: browser use, GUI agent
  zh: computer use
  zh_aliases: 浏览器操控, 图形界面智能体
  track: product, news
  首次: 2026-09

### 评测与训练

- id: agent-eval
  en: agent eval
  en_aliases: agent evaluation, eval pipeline, evaluation harness
  zh: Agent 评测
  zh_aliases: 智能体评估, EVAL 流水线, 评测体系
  track: method, product
  首次: 2026-09

- id: regression-eval
  en: regression eval
  en_aliases: regression detection, eval regression
  zh: 评测回归
  zh_aliases: 回归检测, 版本回归
  track: method
  首次: 2026-09

- id: foundation-model
  en: foundation model
  en_aliases: LLM, frontier model
  zh: 大模型
  zh_aliases: 基础模型, 大语言模型
  track: news, method
  首次: 2026-09

- id: agent-training
  en: agent training
  en_aliases: agentic RL, RL environments, post-training
  zh: agent模型训练
  zh_aliases: 智能体训练, 后训练, Agent 强化学习
  track: method
  首次: 2026-09

- id: post-training
  en: post-training
  en_aliases: SFT, RLHF, RLAIF
  zh: 后训练
  zh_aliases: SFT, RLHF, 对齐训练
  track: method
  首次: 2026-09

- id: vertical-agent
  en: vertical agent
  en_aliases: domain agent, industry agent
  zh: agent垂域
  zh_aliases: 垂域智能体, 业务 Agent
  track: product, news
  首次: 2026-09

## 产品

专有名词，中英都用原名搜。证实后加 aliases，不要把未发布传闻写进来。

- id: Codex
  en: Codex
  en_aliases: Codex harness, Codex app-server
  zh: Codex
  zh_aliases: Codex 夹具
  track: product, news
  首次: 2026-09

- id: DeepSeek-Harness
  en: DeepSeek Harness
  en_aliases: dsh, deepseek-harness
  zh: DeepSeek Harness
  zh_aliases: dsh
  track: product
  首次: 2026-09

- id: Hermes
  en: hermes-agent
  en_aliases: hermes, Nous Hermes Agent
  zh: hermes-agent
  zh_aliases: Hermes
  track: product, news
  首次: 2026-09

- id: Warp
  en: Warp
  en_aliases: Warp agent, Warp terminal
  zh: Warp
  zh_aliases: Warp 终端
  track: product
  首次: 2026-09

- id: OpenSandbox
  en: OpenSandbox
  en_aliases: Alibaba OpenSandbox
  zh: OpenSandbox
  zh_aliases: 阿里开源沙盒
  track: product
  首次: 2026-09

- id: Temporal-Agent-Harness
  en: Temporal Agent Harness
  en_aliases: outer harness, Temporal workflow agent
  zh: Temporal Agent Harness
  zh_aliases: Temporal 外层夹具
  track: product
  首次: 2026-09

- id: GPT-6-Astra
  en: GPT-6 Astra
  en_aliases: gpt-6-astra, Astra
  zh: GPT-6 Astra
  zh_aliases: Astra
  track: news
  首次: 2026-09

- id: funding-track
  en: AI agent funding
  en_aliases: agentic AI investment, startup funding
  zh: 智能体融资
  zh_aliases: Agent 投资赛道, 大模型融资
  track: news
  首次: 2026-09

## 维护规则

- **不要在每日开采里直接加新 id。** 新叫法先记 [candidates.md](candidates.md)。
- 写入必须同时有 `en` / `zh` 和 `track`。
- 只是旧概念的别称 → 只加 aliases。
- 连续 30 天无命中且被更精确的 id 替代 → 移到「降权」。
- 不要为了凑数发明词。不要加岗位/职级词。

## 降权

- id: loop-engineer
  替代: harness
  原因: 岗位称谓，产物已剥离岗位

- id: fde
  替代: vertical-agent
  原因: 岗位称谓

- id: work-mode-shift
  替代: harness
  原因: 工作模式/岗位叙事，不再作为检索主轴

- id: new-harness-product
  替代: DeepSeek-Harness
  原因: 已落到具体产品名

- id: new-agent-product
  替代: Hermes
  原因: 已落到具体产品名
