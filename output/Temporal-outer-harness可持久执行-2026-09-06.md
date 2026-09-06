---
形态: 产品剖析
主题: Temporal
日期: 2026-09-06
---

# Temporal Agent Harness：外层管责任，内层管推理

这篇只拆 Temporal 2026 年公开的 **Temporal Agent Harness**——**outer harness** 与常见 **inner harness** 各管什么、环怎么转。值得看，是因为 agent 工具已 commoditize，但「把 LLM 放进真实业务流程」时的责任（identity、审批、 durable state、失败恢复）仍缺标准件；再套一层框架容易惹烦，可业务 agent 又绕不开。

## 痛点：全功能 harness 太大，SDK 太小

Cornelia Davis 在官方文里描述两极困境。一端是 Claude Code、Cowork 等**全功能 harness**：agent loop、会话、MCP、skill 开箱即用，个人场景很香；但一旦 agent 要接 CRM、库存、退款——「只能查当前客户订单」「超阈值退款须人审」这类 **business invariant** 很难硬编码进它的执行与权限模型，你只能靠 prompt 祈祷模型守规矩。更麻烦的是这类 harness 的 session 模型面向「人坐在前面」，不是面向「订单号 8842 在支付网关 hang 了六小时」。

另一端是 OpenAI Agents SDK、PydanticAI、LangGraph、AWS Strands、Google ADK 等 **inner harness/SDK**：loop、tool calling、MCP、tracing 已成 commodity，团队往往已选型并积累 expertise；**完全自控**，但 durable execution、跨天等待、crash 后续跑、结构化审计轨迹——大量**无差异化 infra** 得自己造。你会写 agent loop，不等于你想写第七版「等人批完再 resume」的状态机。

对个人助手，inner 够用；对**业务 agent**（客服、运维、风控），规则必须在「模型决定调用工具」与「工具真执行」之间的**缝**上 enforced，且 worker deploy、进程 crash 不能丢半张订单。Anthropic 与 OpenAI 的 harness engineering 长文也在讲同一命题：长程 agent 的 checkpoint、身份、工具权限——SDK 给你 hook，但不给你 SLA。

中间地带长期空白：在 inner 上手工加 Redis queue、加 approval webhook、自己写 event bus，每个团队重复造「durable agent infra」——Temporal 想把这个收成 **outer harness** 产品。它的卖点不是「Temporal 也会调 OpenAI了」，而是：**把 agent 放进 Workflow 语义**，让 agent 继承你们已经在用的 durable execution、visibility、retry policy——对已有 Temporal 客户的边际成本低于 greenfield agent startup。

## 机制：outer harness 补什么

Temporal Agent Harness **不替换** inner loop，而是用 **Temporal Workflow** 包一层，durability 是地基而非事后 bolt-on。

**Bring your own inner harness。** 已集成 Google Gemini、OpenAI Agents SDK、PydanticAI；你 program 内层 ReAct，Temporal 在外层 deliver durability。企业可能因采购政策锁定某 SDK——outer capitalize 现有集成，而非强迫迁移。Inner 里的 MCP、structured output、tracing 继续用；outer 不 duplicate 这些 commodity 能力。

**Durable execution 是地基。** 每个 agent 是 Temporal Workflow：worker crash、部署滚动、等三天的人审，都从 Event History 精确 resume，已完成 step 不重跑。这不只包 inner loop——**outer loop、tool call、等人、Code Mode sandbox** 都在 durability 语义里。对跨 CRM/支付/物流边界的流程，这是 table stakes，不是 edge case。

**Turn 高于 loop。** familiar ReAct loop 仍在一 turn 内跑多步 tool；但 harness 引入更高层 **turn**：一次 turn = 调用 inner harness 一次，到达 terminal state 不等于任务结束。客户问「订单在哪」是一 turn；回「改地址」是**新 turn**，上下文由外层 stitch。Turn 也可由审批到达、timer、外部系统事件触发——不限于 chat message。长程交互因此不必塞进单次 context window，也不必 hack 成「一个 giant loop 里 while True 等人」——那在 process crash 时全丢。

**Tool 缝上的 policy layer。** Tool calling 是 agent 从「推理」切到「改世界」的边界。Harness 提供 `ToolApprovalPolicy`：查单可 `allow_inherently_safe`，退款 pause，等人 hours/days 后 resume——**等待本身 durable**，不占 worker 进程。示例代码里 `approval_policy_default=ToolApprovalPolicy.allow_inherently_safe()` 表明默认策略可声明式配置，再按 tool 名 override。Policy 可分层、运行时改、按 tool/session scope——seam 在「模型选中 capability」与「capability 执行」之间，正是应用 controls 该在的位置；也是合规官能听懂的层。

**AgentEvent 与 event-sourced 地基。** Turn、model interaction、tool call/result、approval、handoff、response 收成 **AgentEvent** 流，built on Workflow Event History——不是事后打日志。前端渲染进度、审批服务订阅、analytics/eval/audit 独立消费；换 inner harness，事件模型稳定。官方 demo 强调 **playback**：非确定性 agent 出问题时，你要查的是事件路径，不是让模型「解释」自己做了什么——这与 OpenTelemetry trace 互补：trace 看 latency，AgentEvent 看业务语义级轨迹。

**Callback tools 与多运行时。** 工具不必与 agent 同进程：用户笔记本上的文件、手机相机、私网 API——agent 发 typed request，durable wait，执行端 callback。Approval、lifecycle 与 inner tool 一致——harness 统一「能力怎么被 invoke」，不统一「能力跑在哪」。

**Code Mode、callback tools、强类型与组合。** Code Mode 让模型写 Python 编排多 tool（loop、branch、filter），仍受 approval 约束，sandbox 执行纳入 durable 语义——比「每步 tool 都回 LLM 想一遍」省 token，也比单次 giant JSON tool call 更表达力。强类型 operation 让 incident、order、fraud review 以 schema 进出 agent，而不是 prose 来回粘贴；composition 则允许专门 agent 暴露 toolset 给编排 agent，multi-agent 不必退化成 prompt 里互相粘贴聊天记录。

项目自称 **early**（比 public preview 还早），API 会变；但原则已写清：durable execution、meet developers where they are、strong control points、agents 具 first-class application semantics。社区反馈渠道明确要听「哪些 inner harness 下一优先」——说明 outer 层仍在找最小完备抽象，不是封闭成品。

从责任链看，Temporal 回答的是 Cornelia Davis 文首那句：**给 agent capability 容易，给 responsibility 难。** Outer harness 把 identity、authorization、invariant、failure handling 从 prompt 层拉到 workflow 层——模型仍不可预测，但系统对预测的响应可预测：该 pause 就 pause，该 resume 就 resume，该留下 AgentEvent 就留下。

## 用中文把环再串一遍

没有 outer harness 时，工程师常在 inner loop 外包一层 Redis：状态键是 session id，值是「等到审批」。进程重启后要自己扫键、防重复执行、把「已完成步骤」和「待执行步骤」对齐——每个团队第七次写歪。Temporal 把这套语义收成 **Workflow**：历史在 Event History 里，resume 是平台能力，不是业务代码里的 while 循环。

**Turn** 也值单独理解：用户先说「查物流」，再说「改地址」，在聊天产品里像两轮对话；在只有 inner harness 的实现里，容易变成同一个 ReAct loop 里上下文越来越长，或在 crash 后无法区分「哪一轮改地址已经调过支付接口」。outer harness 把每一轮 turn 收成可审计单元，和 AgentEvent 一一对应——运营后台能显示「卡在退款审批」，而不是「Agent 没响应」。

若你已经在用 Temporal 做订单、理赔、开户等非 AI workflow，把 agent 接进同一套 ops（重试策略、可见性、权限）比另起一套 agent 编排器便宜。若还没有 Temporal，先问业务要不要「等三天」：不要，就别为 outer harness 付学习成本。

## 对照、误区与边界

与 Hermes（runtime 文件型 learning + 个人 gateway）比，Temporal 面向 **multi-worker、跨服务、SLA 敏感** 的业务 agent——复杂度换可靠性与可观测性；Hermes 的 background review 写本地 skill，Temporal 的 AgentEvent 写 workflow history，审计粒度不同。与 Claude Managed Agents 的 meta-harness 比，Temporal 不托管 model inference，强调 **workflow 编排**；可组合：Managed 提供 brain/hands/session 拓扑，Temporal 包 customer refund 等多 turn  Saga。

与 OpenSandbox 比：Temporal Code Mode 里的 Python 需要 sandbox，但 sandbox 选型不是 Temporal 核心——OpenSandbox 或自建 runtime 接在 tool executor 即可。

误区：把 outer harness 当成 duplicate inner loop。边界：无 Temporal 运维经验则 learning curve 陡；policy + approval + multi-turn 调试需同时读 Workflow 与 inner trace。项目 early，API 会变——现在接入应视为共同塑造抽象，而非消费稳定 GA。

可带走的一句判断：**inner harness 管模型怎么推理与调 tool；outer harness 管推理之外的责任——durability、审批、事件边界与跨 turn 上下文；业务 agent 缺的是后者，不是第三个 ReAct 实现。** 若你已在用 Temporal 做业务 workflow，outer harness 是把 agent 纳入现有 ops 习惯的最短路径；若还没有 Temporal，先问清楚你的 agent 要不要「等三天」——要，才值得付这层复杂度。

用一个退款 Saga 把缝上的 policy 说具体：客户说「订单 8842 要退 500 元」。inner harness 在一 turn 里调 `get_order`、`calculate_refund`，模型选中 `execute_refund`——这是推理结束、世界即将被改写的边界。`ToolApprovalPolicy` 发现金额超阈值，workflow **pause**，AgentEvent 记 `approval_requested`；合规官手机点批准，**同一 workflow** 从 Event History resume，已完成查询不重跑，只执行退款。若 deploy 滚动 kill worker，新 worker replay 历史到 pause 点继续等——这不是「Redis 里有个 waiting flag」，而是平台级 durable wait。对比 Warp 用 DPO 改权重、Hermes 用 background review 改 SKILL.md：Temporal 的「进化」发生在 **policy 配置与 workflow 定义** 的 Git diff，不在 model logits；三者可叠——Hermes 个人侧沉淀 pitfall，Temporal 企业侧 enforce 退款 invariant，互不替代。

再补一层 **credit assignment** 视角：多 turn 客服里，哪一步 tool call 导致投诉升级，事后审计读 AgentEvent 流比读 chat log 可靠——每个 turn 有 terminal state、每个 tool 有 approval 记录，运营可问「第几 turn 的 `update_address` 未经审批就写了支付库」。这与 MASkills 的 skill trace 同构，只是粒度在 workflow event 而非 SKILL.md invocation；若你的 compliance 要求 **逐步可追责**，outer harness 提供的不是更聪明模型，而是 **把责任从 prompt 拉到事件日志** 的标准件。Demo 阶段 API 会变，但「等待 durable、resume 精确、policy 在缝上」这三条原则不太会回滚——评估是否接入，先看业务有没有「等三天仍要接着跑」的硬需求，而不是看 inner loop 缺不缺第三个 ReAct 实现。

Code Mode 再举一个省 token 的用法：模型写 Python 在 sandbox 里 loop 调三个只读 API、filter 结果，再决定是否 escalate 到需审批的写操作——比「每步都回 LLM 想下一 tool」便宜，且整段脚本纳入 durable 语义：crash 后从 AgentEvent 知脚本执行到哪一行。callback tools 则把「用户笔记本上的本地文件」接进同一 approval 模型——harness 统一 invoke 语义，不统一 runtime 位置。已有 Temporal 客户把 agent 接进现有 retry/visibility 控制台，边际成本低于 greenfield agent startup——这是 Cornelia Davis 文里 **meet developers where they are** 的产品含义。

Bring your own inner harness 意味着 PydanticAI 的 structured output、LangGraph 的 checkpoint hook 可保留——outer 不 duplicate commodity 能力，只补 **durable turn、AgentEvent、ToolApprovalPolicy**。调试时要同时读 Workflow History 与 inner trace：前者答「卡在哪条 business invariant」，后者答「模型为何选中该 tool」。项目 early，接入宜共同塑造抽象；若无「等三天」硬需求，inner + Redis 手工包一层可能仍够用——outer 复杂度是为 SLA 与 audit 付的价。

---
**参考**
- [Temporal Agent Harness 官方博客](https://temporal.io/blog/temporal-agent-harness-durable-agent-infrastructure)
- [temporal-community/temporal-agent-harness](https://github.com/temporal-community/temporal-agent-harness)
