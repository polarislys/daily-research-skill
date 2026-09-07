---
形态: 产品剖析
主题: Microsoft Agent Framework
日期: 2026-09-07
---

# Microsoft 把 harness 做成默认产品：plan/execute 不再靠你自己拼

这篇只答一个问题：Microsoft Agent Framework 为什么要在「会调工具的聊天 Agent」外面，再做一个开箱即用的 Harness Agent？官方把它写成产品层，而不是示例代码。[Learn 文档](https://learn.microsoft.com/en-us/agent-framework/agents/harness) 和 [发布博文](https://devblogs.microsoft.com/agent-framework/the-microsoft-agent-framework-harness-is-now-released/) 把模块钉死；本日近窗由头是 [Harness Engineering](https://arxiv.org/abs/2609.00006)（2026-09-01）把十一套生产 coding agent 拆成同一套七子系统——微软这套是框架厂商反向做出的那一类 harness。

发布博文未在页眉标精确日，相邻博文落在 2026-07；文档仍是当前产品说明。框架本身 2026-04-02 到 1.0 GA，见 [BUILD 2026 汇总](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/)。

## 以前为什么每人拼一套环

模型自己只会吐字。要它调工具、记住做过什么、把多步任务做完，外面必须有一层运行时。这层就是 harness：循环、工具、权限、重试和夹具，不是 chatbot 皮肤。2025 年多数团队从聊天客户端起步，自己接 function calling、会话存储、压缩、待办、审批。缺一块，长程任务就在上下文溢出或「下一步该干什么」上停住。

微软把这条缝写成两个产品对象。[博文](https://devblogs.microsoft.com/agent-framework/the-microsoft-agent-framework-harness-is-now-released/) 说得很直：`Agent` / `ChatClientAgent` 是带推理服务、指令、可选工具和工具调用环的基本体验；`create_harness_agent` / `HarnessAgent` 在这之上默认接上规划、模式、compaction、记忆。前者也可以被叫作 harness，但故意留薄，好让人从积木拼；要「开箱像一只会自己列清单的 claw」，走后者。

[Harness Engineering](https://arxiv.org/abs/2609.00006) 给了行业对照：十一套生产系统——Claude Code、Codex CLI、Gemini CLI、Mistral Vibe、OpenHands、Aider、Mini-SWE-Agent、Hermes、Pi、OpenCode、OpenClaw——源码里**没有一套** import LangChain / AutoGen 这类通用框架，全是手写异步环。框架厂商的反应不是劝人改 import，而是自己出荷成套 harness。微软这套走的就是这条路：用框架积木拼出和那些 CLI 同构的运行时，而不是再发明一种「工作流 DSL」。

## 默认夹具怎么转

[Learn 的架构段](https://learn.microsoft.com/en-us/agent-framework/agents/harness) 把 Harness 写成五层组合，不另起一套进程模型。

聊天客户端只负责连模型。聊天管道加上 function invocation、消息注入、**每次模型调用之后**落盘历史，以及可选 compaction。Agent 与 context provider 再注入会话级指令、工具、记忆、todo、plan/execute 模式。中间件补审批、OpenTelemetry、可选的有界 looping。最外是应用 UX：流式输出、展示进度、收集工具批准。拼完仍是普通的 `AIAgent` / `Agent`，会话接口和其他 Agent 一样。崩溃可从「上一次模型调用」而不是「上一次用户回合」恢复——长工具环里这不是细节，是能不能续跑的分界。

指令分两层，顺序写死。[Learn](https://learn.microsoft.com/en-us/agent-framework/agents/harness) 规定 `HarnessInstructions` / `harness_instructions` 在 `ChatOptions.Instructions` / `agent_instructions` 前面；不写则注入 `DefaultInstructions` / `DEFAULT_HARNESS_INSTRUCTIONS`。夹具纪律（何时列 todo、何时切模式、工具要可核查）压在角色人设之上，避免应用侧一句「你是研究助理」把规划环冲掉。`.NET` 用 `AsHarnessAgent` 或直接 `new HarnessAgent`；Python 用 `create_harness_agent`，并建议 `agent.create_session()` 把 plan、todo、历史挂在同一会话上跨回合转。文档还把「后台子 Agent」和「provider 托管的后台响应」拆开：前者把子任务派给命名子 Agent 并行跑，后者用 continuation token 续同一次模型请求。混用这两个词，会把编排层和供应商的长请求 API 收成一件事。

默认打开的能力决定了产品理念。todo 与 plan/execute 默认开：先列出工作项，再切到执行，避免模型一边想一边改。会话级 file memory 默认开，跨回合留下笔记和产物。工具审批默认带「别再问」的常设规则和安全调用的启发式自动批准。OpenTelemetry 默认开。Web search 在底层客户端支持时默认开。.NET 默认开 Agent Skills，Python 要用 provider 或路径选择加入。function invocation 带每请求迭代上限。compaction 要你提供 token 上限或自定义策略才启用——长环溢出不是默认替你管死，是你把预算交进去才管。这些不是插件市场，是**不关就在的夹具**。

明确没放进稳定面的东西同样说明理念。后台子 Agent、共享文件访问、自动 looping 仍标 experimental；shell 来自预发布的 `agent-framework-tools`。[博文](https://devblogs.microsoft.com/agent-framework/the-microsoft-agent-framework-harness-is-now-released/) 说这些已经能用，但会警告，要更多客户反馈再标发布。和 [OpenSandbox](https://github.com/alibaba/OpenSandbox)、Codex 的 OS sandbox 比，微软把「能进 shell / 能写工作区」留在稳定面之外：先把规划、记忆、审批、可观测做成默认，隔离执行另谈。Go 没有打包好的 Harness，要自己组合 provider。

定制方向是减，不是加。`.NET` 一侧是 `DisableTodoProvider`、`DisableAgentModeProvider`、`DisableFileMemory` 这类开关；Python 一侧是 `disable_todo`、`disable_mode`、`disable_file_memory`。Skills、文件访问、后台 Agent、shell、looping 用另一些入口打开。官方示例终端能显示 todo、当前模式、审批提示和 `/todos` `/mode`，但文档写明：控制台是 sample，不是框架组件。Harness 不规定 UI。

[Harness Engineering](https://arxiv.org/abs/2609.00006) 把 coding agent 拆成七块：agent loop、LLM 接入、工具、记忆与上下文、安全与权限、编排、扩展性。微软稳定面覆盖前五块的「薄实现」：loop 是带迭代上限的 function invocation，记忆是 file memory + 可选 compaction，安全是启发式审批而不是 OS sandbox，编排和 shell 留在实验开关。论文里的最大实现分别是 OpenHands 的事件源 loop、Hermes 的多 transport、Claude Code 的四十多个类型化工具、Codex 的跨会话记忆管道和三平台 sandbox。微软没有声称做到最大实现，它声称的是：**七块里你必须先有的那几块，默认已经接上**。

和昨日写过的 [DeepSeek Harness](DeepSeek-Harness-一切皆插件-2026-09-06.md) 对照：dsh 的理念是「一切皆插件」，模型、工具、循环、沙盒都能换；微软是「一切有默认，按需关掉」。和 [Codex](https://github.com/openai/codex) 对照：Codex 把 sandbox 与审批做成产品核心，微软把这两块留在实验或启发式自动批准。和 Claude Code 对照：那边 Skill 是文件系统上的程序性知识，这边 .NET 默认发现、Python 选择加入，格式走 Agent Skills，但文档没有把「改 Skill 必须走 PR」写成产品约束。论文还写 SKILL.md 在十一套里的采用（9/11）已经压过 MCP（8/11）——微软把 Skills 放进默认矩阵，是在跟这条收敛对齐，不是另起炉灶。

## 可复查的边界

这是 SDK 里的 harness，不是托管运行时。[Claude Managed Agents](https://www.anthropic.com/engineering/managed-agents) 那种「脑在云上、手在你机器」不在这套说明里。shell 与文件访问未标发布，就不能把它写成「和 Codex 同级的隔离执行」。文档也没给默认 compaction 策略的数字阈值，只说提供了 token 上限或自定义策略才启用。

[Harness Engineering](https://arxiv.org/abs/2609.00006) 的观察仍然刺：生产 coding agent 不用通用框架。微软把框架和 harness 收成同一 SDK，能不能让下一波生产环真的从 `AsHarnessAgent` 起步，要看 shell / sandbox 稳定之后的仓库，而不是看示例能否跑通一次调研问答。机制上可复查的一点：如果你用的是 `ChatClientAgent` 而不是 Harness Agent，先数缺了哪几块默认夹具——todo、plan/execute、每次调用落盘、compaction、审批、trace。缺的不是「功能列表」，是长程任务停住时无人认领的那一层。

---
**参考** [The Microsoft Agent Framework Harness is now released](https://devblogs.microsoft.com/agent-framework/the-microsoft-agent-framework-harness-is-now-released/) · [Agent Harness | Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/agents/harness) · [Harness Engineering: Anatomy of Eleven Systems](https://arxiv.org/abs/2609.00006) · [microsoft/agent-framework](https://github.com/microsoft/agent-framework) · [BUILD 2026 汇总](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/)
