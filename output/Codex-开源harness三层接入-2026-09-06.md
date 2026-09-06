---
形态: 产品剖析
主题: Codex
日期: 2026-09-06
---

# Codex 开源 harness 的三层接入：模型之上是 runtime，runtime 之上才是你的规则

这篇只答一件事：如果你要在自己的产品里嵌入 Agent，该接 Codex 的哪一层，以及「你的规则」应放在 harness 之外还是之内、放在文件系统的哪一层。OpenAI 把 CLI、IDE 插件、Codex App 背后的同一套执行系统开源了——关键不是又多一个 chat 窗口，而是可 inspect、可 fork 的 **agent loop** 与分层集成面。

## 痛点：每个团队都在重造 agent loop

一个能上岗的 Agent 远不止「prompt + 模型回复」。它要在多轮对话里维护 state，调用工具，在 **sandbox** 里执行命令，在敏感操作前 **request approval**，失败时重试，还要把进度 **stream** 给 UI。若每个垂直产品各自实现这套 **surrounding execution system**，很快会在 conversation 管理、权限模型、MCP 接入、approval 回调上重复踩坑，且难以对齐安全边界。

OpenAI 在官方文里把这套系统称为 **harness**——包在模型外的循环、工具、权限与重试，不是 chatbot 皮肤。同一 harness 设计曾让 GPT-5.6 Sol 在 ARC-AGI-3 上从 13.3% 提到 38.3%，output token 还降六倍，说明**环的质量**可独立于单次模型能力产生杠杆。

更深的问题在 **ownership**。安全调查台、客服控制台、物流调度盘各自有不同的 record、approval flow、专有 MCP tool。强迫用户离开业务界面进通用 coding chat，context 与 UX 都是反模式。Codex 的命题是：**应用拥有业务界面与 system of record，harness 拥有 agent loop**；二者通过 documented protocol 衔接，而不是把产品逻辑塞进 CLI。

## 机制：三层接入与规则该落在哪里

OpenAI 文档给出三条集成路径，深度递增、控制粒度递增，可按「Agent 在产品里有多常驻」来选。

**第一层：`codex exec`**——非交互、有界任务。适合 CI、cron、一次性脚本：传入任务描述，跑完返回 structured output，不持有长对话。这是「把 Agent 当批处理函数」的入口；**bounded** 意味着 sandbox 与 approval policy 在启动时已定，适合 merge gate、夜间批处理或「跑完即走」的自动化。你不需要在应用里维护 thread，只需消费最终结果。许多团队的第一步应是：在现有 CI 里用 exec 跑「根据 diff 写 release note」「对迁移脚本做静态审查」等有界任务，验证 sandbox 与 output schema，再考虑更深集成。

**第二层：Codex SDK**（TypeScript `@openai/codex-sdk`、Python `openai-codex`）——应用代码以 programmatic 方式 start、resume、stream task。SDK 与本地 **app-server** 进程对话，适合 backend 服务内嵌 Agent，而不必 shell out CLI。官方 Python 包 pin 兼容 CLI 版本，减轻生产环境 **version skew**。这层适合「我的服务要在用户操作时触发 Agent，但 UI 仍是我自己的」——例如内部工单系统后台跑修复建议，或微服务在队列 consumer 里 resume 昨晚未完成的 thread。

**第三层：Codex app-server**——Agent 成为产品的一等功能。基于 **JSON-RPC 2.0**（stdio 或 WebSocket）暴露 **thread / turn / item** 生命周期：`thread/start`、`turn/start`、`turn/interrupt`、`item/permissions/requestApproval` 等大量方法。应用创建 thread、订阅 streamed events、在 filesystem 或 network 升级前渲染 approval UI。**Relay** 示例即此模式：用户选中 shipment 点「Compare recovery」，应用注入业务 context，Codex 经**应用自有 MCP** 拉运营数据，解释选项；任何写回必须人批。harness 管 loop 与 sandbox；产品管 dashboard、record 与按钮。

app-server 还有 **backpressure** 语义：队列饱和时返回 `-32001 Server overloaded`，客户端应 jitter 退避——产品级集成必须处理，否则 peak 时 UI 静默失败。Thread 可 `fork`、`archive`，turn 可 `steer` 中途改向；这些原语让「常驻协作者」体验区别于一次性 exec。MCP tool call、OAuth login flow 与 plugin tool 共用同一 protocol surface，减少集成分叉。

三层之下是 **model access**（API、订阅），与开源 harness **刻意分离**。三层之上是 **your rules**——这才是多数团队真正该投资的层。

OpenAI **harness engineering** 实验表明：把全部规则塞进巨型 **AGENTS.md** 会 predictable 地失败——挤占 task context、一切「重要」、无法机械验证、迅速腐烂。更稳的做法是分层：**AGENTS.md** 约百行，作 **table of contents**，指向 `docs/` 下 design-docs、exec-plans、product-specs 等 **system of record**；**.codex/config.toml** 管 model profile、sandbox、approval 档位；**.codex/rules/** 与 hooks 管可执行的 allow/deny；**.agents/skills/** 放 **SKILL.md** 做 progressive disclosure。社区 harness 脚手架常把 `shared/rules/` 与 `.codex/agents/` 生成链对齐——**共享策略必须进 Git**，凭证与本地 state 不进版本库。mandatory 约束应能在 CI 里校验 syntax 与引用，而非只存在于工程师口头 tradition。

「三层接入」与「规则分层」是正交的两个维度：前者回答 **Agent runtime 嵌多深**，后者回答 **意图与约束放哪**。新手常混为一谈，把 business rule 写进 SDK 调用参数，导致换 integration tier 时规则丢失。正确心智模型是：model 提供推理；Codex harness 提供 loop 与 sandbox；你的 Git repo（或产品配置）提供 **map + rules + skills**；你的应用提供 **UI + MCP + approval UX**。四层各守边界，才可替换其中一层而不推倒重来。

## 对照、选型与边界

选层口诀：**脚本与 CI 用 exec，服务内自动化用 SDK，Agent 在 UI 里常驻、要 interrupt 与 approval 用 app-server**。勿把社区带 harness 名字的脚手架 repo 误当作官方 runtime——**openai/codex** 才是 agent loop 本体；其余多是 AGENTS.md 与 hooks 模板。

与 Cursor、Claude Code 等集成型产品比：它们同样依赖 harness 思想，但未必开放 app-server 级协议。Codex 开源层的差异是 **可 fork、可 audit、可嵌进垂直 SaaS**——Cisco App Builder、Thrive 税务流程等公开案例都是同一 pattern：应用供 context、tools、approvals；Codex 跑 loop。与 Warp 双 Skill 进化比：Codex 默认不把「改进」建模为 improver PR，但 **Skills** 目录与 repository skills 机制兼容同一开放格式方向。

Thrive 案例值得一句：7k 份回报、准备时间约减三分之一——说明 harness 嵌入垂直 workflow 时，**practitioner feedback** 仍在环内，只是不必然走 Skill PR。Codex 提供的是 loop 与 sandbox 标准件；领域闭环仍要产品定义。Cisco App Builder 则展示 IDE 内嵌 SDK 路径：开发者不离开 Cloud Control，Agent 在 familiar UI 里跑——对应第二层而非第三层，但 harness 仍是同一份开源 core。

边界须如实写：开源 harness **不含** OpenAI 托管算力与 ChatGPT 订阅权益；app-server 的 approval 策略——全自动 Guardian subagent、严格人审、或 CI 内 auto-accept——需产品自定，官方只提供 RPC 挂点。Relay 用虚构 seed 数据，集成 pattern 可泛化，落地仍要投 sandbox 契约与 MCP schema。**Model 是栈里最易替换的一层**；环境设计、规则分层与 integration tier 选择才是 compounding 部分——这与 OpenAI 内部「人类 steer、Agent execute」的长期结论一致。

把三层与 **your rules** 叠在一起看，典型栈如下：最底是 model API；其上 Codex harness 管 thread、tool、sandbox、stream；再上是应用的 MCP 与 UI；最外是 Git 里的 AGENTS.md 地图、rules、Skills 与 CI。错层是最常见失败——把 business rule 写进 prompt 模板而非 rules 文件，或该用 exec 却拉 app-server 加重 ops。app-server 的 **item 生命周期**（started → delta → completed）让 UI 能细粒度渲染 tool call 与 file change，这是 exec 给不了的 product 体验，也是第三层存在理由。

OpenAI 强调 harness 与 **managed services 分离**，对企业意味着：可 auditable 的自建部署与合规边界，但 model 账单与 SLA 仍另算。与 **Temporal Agent Harness** 等「 durable 外层」比，Codex 更偏单进程 local loop；长事务、跨天 human wait 可能要外层 workflow 包一层，而非指望 harness 全能。

Figure 1 的架构图（官方文）用一句话概括：**Your application owns product context, business rules, and tools; Codex app-server provides the agent loop and sandboxed execution.** 读文时盯住这条分界线，就不会把 Relay 当成「又一个 Codex App 皮肤」。integration 越深，application 侧要写的 MCP 与 approval UI 越多，但 product differentiation 也越大——通用 chat 无法替代 shipment dashboard 上的 contextual action button。

收束：**选 integration tier 是产品架构决策，选 rules 放哪是工程治理决策**；两层都做对，才谈得上「在自家产品里长 Agent」，而不是给 chat 换皮。

## 读者可带走的一个判断

先画产品边界：Agent 是批处理、后台服务，还是界面里的常驻协作者？答案直接映射 exec / SDK / app-server。再画规则边界：什么必须进 Git、什么必须进 config.toml、什么只能留在运行时 secret。Codex 开源的是中间 **harness** 层，不是替你写 AGENTS.md；但若三层选对，你可以像 Relay 那样把 shipment context、MCP 与 approval 留在产品里，而把 loop 交给同一套可审计 runtime。2026 年的重复建设，多半发生在「又写了一个 while tool_call loop」——Inspect `openai/codex` 再决定自研范围，通常更省。

官方 **open-source components guide** 列出 CLI、app-server、SDK 各自仓库路径——集成前先确认用的是哪一件，避免 npm 上同名脚手架。model access 单独计费意味着 harness 选型不应绑死 vendor：rules 与 MCP 契约才是迁移时要带的 assets。对国内团队，Relay 式运维台、Thrive 式文档密集型 workflow 比复刻 Codex App 更有参考价值，因前者强调 **embed** 而非 **replace IDE**。

把 Relay 案例再推一步：运营在 shipment dashboard 选中延误批次，点「Compare recovery」——应用经 **自有 MCP** 注入当前 SLA、承运商约束与历史索赔记录，再 `thread/start` 让 Codex 跑 loop；模型提议 reroute 或 partial refund，任何 **写回 TMS** 的操作走 `item/permissions/requestApproval`，人在同一 dashboard 批。harness 不知道什么是 shipment，它只知道 thread、turn、tool；业务规则在 Git 的 `docs/product-specs/` 与 `.codex/rules/`，不在 SDK 参数里。若团队从 exec 升级到 app-server，**rules 文件不用搬家**——这是「三层接入」与「规则分层」正交的好处。错层典型反例：把「超过 10 万美元须 VP 审批」写进一次性 prompt，换 integration tier 或换模型 profile 时规则静默丢失；应进 `.codex/rules/` 并在 CI 校验引用。

第三层 app-server 的 **backpressure**（`-32001 Server overloaded`）常被忽略：peak 时若不 jitter 退避，UI 会静默失败——产品级集成必须处理，与模型能力无关。`thread/fork` 适合「从当前方案分支试 alternative」；`turn/steer` 适合用户中途改需求——这些原语是 exec 给不了的 **常驻协作者** 体验。与 DeepSeek dsh JSON-RPC SDK 比：Codex 强调 app-server 协议与 OpenAI 托管 loop；dsh 强调 Cordis patch 可换 loop——选型看你要 **fork harness** 还是 **embed harness**，rules 与 Skills 格式仍可互通。

---
**参考**
- [Codex as a platform: build on the open agent harness](https://developers.openai.com/blog/codex-as-a-platform)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [openai/codex](https://github.com/openai/codex)
- [Codex App Server API overview](https://openai-codex.mintlify.app/api/overview)
