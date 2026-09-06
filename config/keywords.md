# JD 关键词表（中英对照，随岗位演进更新）

每日调研**只认本文件的概念行**。不要只搜一列：国内源用「中文检索」，国外源用「英文检索」，文章里用「规范名」做标题和术语解释。

- `<!--` 开头的行忽略
- `首次` 用 `YYYY-MM`
- 同义词只写检索会用到的别称，不要堆翻译腔

读者：AI 应用研发 / 应用优化 / Agent 优化 / Agent 训练与优化。目标是端到端 Agent 架构师与垂域落地，要比业务负责人看得更多、更远。

## 怎么搜

| 来源 | 用哪一列 | 例子 |
|---|---|---|
| 英文：论文、官方博客、HN、GitHub、YouTube | `en` + `en_aliases` | `agent harness`, `eval pipeline` |
| 中文：论文译介、厂技术号、知乎/公众号、B 站 | `zh` + `zh_aliases` | `智能体运行基座`, `评测流水线` |
| 产品名、协议名、仓库名 | 专有名词原样 | `MCP`, `Codex`, `dsh`, `hermes` |

一条概念 = 一层能力。中英文是**同一概念的检索面**，不是两个主题。

## 概念对照（规范名用英文，便于和美厂 JD 对齐）

格式：

```text
- id: <规范名>
  en: <英文主检索>
  en_aliases: <英文同义，逗号分隔>
  zh: <中文主检索>
  zh_aliases: <中文同义>
  首次: YYYY-MM
```

### 环与夹具

- id: harness
  en: agent harness
  en_aliases: harness, agent loop, scaffolding
  zh: Agent Harness
  zh_aliases: 智能体运行基座, 执行环, 智能体夹具
  首次: 2026-09

- id: loop-engineer
  en: loop engineer
  en_aliases: agent loop, execution loop
  zh: 循环工程师
  zh_aliases: Agent Loop, 执行环设计
  首次: 2026-09

- id: tool-use
  en: tool use
  en_aliases: tool calling, function calling, tool routing
  zh: 工具调用
  zh_aliases: 工具编排, Function Calling
  首次: 2026-09

- id: skills
  en: agent skills
  en_aliases: SKILL.md, skill system
  zh: Agent Skill
  zh_aliases: 技能模块, Skills
  首次: 2026-09

- id: mcp
  en: MCP
  en_aliases: Model Context Protocol
  zh: MCP
  zh_aliases: 模型上下文协议
  首次: 2026-09

- id: skill-rag
  en: skill-rag
  en_aliases: skill retrieval, retrieve skills
  zh: skill-rag
  zh_aliases: 技能检索, Skill RAG
  首次: 2026-09

- id: skill-graph
  en: skill-graph
  en_aliases: skill graph, skill orchestration
  zh: skill-graph
  zh_aliases: 技能图谱, Skill 编排
  首次: 2026-09

- id: skill-evolution
  en: skill self-evolution
  en_aliases: self-improving skills, evolving skills
  zh: skill自进化
  zh_aliases: 技能自进化, Skill 自我迭代
  首次: 2026-09

### 运行时与观测

- id: agent-runtime
  en: agent runtime
  en_aliases: execution engine, agent orchestration
  zh: Agent Runtime
  zh_aliases: 执行引擎, 智能体运行时
  首次: 2026-09

- id: sandbox
  en: sandbox
  en_aliases: sandboxed execution, isolation
  zh: 沙盒
  zh_aliases: 沙箱, 隔离执行
  首次: 2026-09

- id: observability
  en: agent observability
  en_aliases: tracing, trajectory, OpenTelemetry
  zh: 可观测性
  zh_aliases: 轨迹追踪, Trace, 链路回放
  首次: 2026-09

- id: context-management
  en: context management
  en_aliases: context engineering, context construction, compaction, memory
  zh: 上下文管理
  zh_aliases: 上下文工程, 长上下文, 记忆管理
  首次: 2026-09

- id: long-horizon
  en: long-horizon
  en_aliases: long-running tasks, long-horizon agents
  zh: 长程任务
  zh_aliases: 长程执行, 长时程 Agent
  首次: 2026-09

- id: computer-use
  en: computer use
  en_aliases: browser use, GUI agent
  zh: computer use
  zh_aliases: 浏览器操控, 图形界面智能体
  首次: 2026-09

### 评测

- id: agent-eval
  en: agent eval
  en_aliases: agent evaluation, eval pipeline, evaluation harness
  zh: Agent 评测
  zh_aliases: 智能体评估, EVAL 流水线, 评测体系
  首次: 2026-09

- id: regression-eval
  en: regression eval
  en_aliases: regression detection, eval regression
  zh: 评测回归
  zh_aliases: 回归检测, 版本回归
  首次: 2026-09

### 模型与训练

- id: foundation-model
  en: foundation model
  en_aliases: LLM, frontier model
  zh: 大模型
  zh_aliases: 基础模型, 大语言模型
  首次: 2026-09

- id: agent-training
  en: agent training
  en_aliases: agentic RL, RL environments, post-training
  zh: agent模型训练
  zh_aliases: 智能体训练, 后训练, Agent 强化学习
  首次: 2026-09

- id: post-training
  en: post-training
  en_aliases: SFT, RLHF, RLAIF
  zh: 后训练
  zh_aliases: SFT, RLHF, 对齐训练
  首次: 2026-09

### 落地与工作模式

- id: fde
  en: FDE
  en_aliases: Forward Deployed Engineer, deployed engineer, applied AI engineer
  zh: FDE
  zh_aliases: 前线部署工程师, 现场交付工程师
  首次: 2026-09

- id: vertical-agent
  en: vertical agent
  en_aliases: domain agent, industry agent
  zh: agent垂域
  zh_aliases: 垂域智能体, 业务 Agent
  首次: 2026-09

- id: work-mode-shift
  en: model plus harness
  en_aliases: harness engineering, good model plus harness
  zh: 优秀模型加harness
  zh_aliases: 工作模式变化, 从最强模型到工程闭环
  首次: 2026-09

## 产品与赛道（专有名词，中英都用原名搜）

- id: new-harness-product
  en: new agent harness product
  en_aliases: dsh
  zh: 新harness产品
  zh_aliases: dsh
  首次: 2026-09

- id: new-agent-product
  en: new agent product
  en_aliases: hermes
  zh: 新agent产品
  zh_aliases: hermes
  首次: 2026-09

- id: funding-track
  en: AI agent funding
  en_aliases: agentic AI investment, startup funding
  zh: 智能体融资
  zh_aliases: Agent 投资赛道, 大模型融资
  首次: 2026-09

## 维护规则

- **不要在每日开采里直接加新 id。** 新叫法先记 [candidates.md](candidates.md)，达到那里的晋升阈值再写入本文件。
- 写入必须同时有 `en` / `zh` 和常用同义词。
- 只是旧概念的别称 → 只加 aliases，不新开 id。
- 连续 30 天无命中且被更精确的 id 替代 → 移到「降权」，写明替代 id。
- 产品名证实后写入「产品与赛道」的 aliases。
- 不要为了凑数发明词。

## 降权

_暂无_
