---
形态: 新闻动态
主题: Replit-Agent-3
日期: 2026-09-06
---

# Replit Agent 3 用浏览器自测闭环，对抗的是「看起来像能用的 Potemkin UI」

这篇只答一个问题：Agent 3 宣称 10 倍自主、200 分钟以上无人值守，**浏览器自测环在其中到底做了什么**——相对 V2 与 Computer Use 路线差在哪，边界又在哪。

## 发布本身：自测不是附加功能，是 autonomy 的底座

Replit 对外称 Agent 3 相对 V2 **10 倍更自主**：单次可 productive 工作从约 20 分钟拉到 **200 分钟以上**（Max Autonomy Beta）。数字本身需要 harness 语境：200 分钟不是「连续写代码 200 分钟」，而是 **在自测环能拦住重大回归的前提下**，Agent 可以更长地无人值守——测挂了自己修，而不是把半成品交给用户。

核心产品开关是 **App Testing**：默认开启，可在 Agent Tools 里关；另有 Max Autonomy 给目标清晰的长任务。官方描述的自测行为是：Agent **周期性**判断「改动是否够多该测了」——不是每条 user message 后都测，避免把交互变成 endless QA。触发后在 Agent 面板开 **真实浏览器预览**，光标点击表单、按钮，测 API 与数据源；Built with Replit Auth 的应用可自动走登录流。测完汇总问题并 **自行修复**。Agent 3 还能生成其他 agents 与 automations——若没有同一套自测环，衍生自动化只会复制 Potemkin 风险；官方把 App Testing 写成默认 on，是在产品层声明 **verify 不是高级用户彩蛋**。

支持范围写得很窄：Full Stack JavaScript 与 Streamlit Python web app；Lite 模式不开 App Testing，Economy/Power 模式在 Advanced settings 里开。用户可 Take over 测试预览完成必要步骤，或 Skip；10 分钟无响应 Agent 当 Skip 继续——说明 **自测环也承认有 Agent 过不去的 gate**（验证码、外部 OAuth 等）。

Replit 博客《automated self-testing》把技术栈说透：**不是纯 Computer Use 截图点按**，而是 **REPL 持久化加浏览器自动化** 的混合验证——median 成本约 **0.20 美元/session**，官方称比 Computer Use 模型 **3 倍更快、10 倍更便宜**（具体对比 workload 未完全公开，读时应留余地）。

## 机制：REPL 把「测试状态」从 token 里搬回代码

AI 写 UI 的经典失败是 **Potemkin interface（Potemkin 界面）**：样式完整、按钮存在，点击后逻辑或 API 全断。用户第一眼「能点」；第二眼「数据没存」；第三眼发现 Agent 早已 declare done。静态 lint、单元测试往往覆盖不了「用户路径上的真实行为」——单测 mock 了 fetch，集成环境 CORS 炸掉，界面仍绿。Replit 博客把这种界面命名为 Potemkin interfaces——借历史隐喻说 ** façade 与功能脱节**；Agent 3 的自测环就是专门戳 façade 的。

Agent 3 的闭环分三层，环是闭合的：

**持久 REPL。** 变量跨步保留；浏览器 session 不重置——Agent 可以「先下单拿 order ID，再用同一 session 查订单状态」。关键设计选择：**上下文留在代码里，不塞进对话 token**。长链路测试若靠 summarization 传 order ID，测到第 50 步 ID 已被压扁，自测形同虚设。Replit 把 notebook 式 REPL 语义搬回 Agent harness，是为 **多 hundred step 测试** 存状态。

**浏览器子 Agent。** Headless Chromium 加 Chrome DevTools Protocol；`@replit/agent-core` 管 session persistence、tool registration、错误处理；`replit-browser` 暴露 click、type 等高层动作。主 Agent 写测试代码并在 REPL 执行，子 Agent 像用户一样导航——分工是 **主 Agent 定断言逻辑，子 Agent 执行交互**。既能 validate（页上有没有 role=button 的元素），也能 manipulate（真的点、填）。这比「一个大模型看屏幕猜坐标」更 structured，也更便宜。

**自修正环。** 执行信号——runtime error、断言失败、DOM 状态不符——回到主 Agent，改代码再跑，直到通过或触发 Take over。失败信息走代码执行通道，不全靠自然语言「我觉得按钮坏了」。Notebook 式迭代在这里复活：Agent 可以先 `assert page.locator(...).count() > 0` 探路，再决定要不要点—— **validate 与 manipulate 在同一代码单元里交替**，比纯对话式「请帮我看看按钮在不在」省 token、可复现。

这跟「让 frontier 模型看屏幕点像素」路线不同。Replit 赌的是 **自家沙箱、REPL、结构化 browser tool** 在 app builder 场景里成本与可控性更优。200 分钟 autonomy 的 claim 里，**自测环是长 horizon 的安全网**——允许 Agent 在无人值守时自己发现「看起来完成其实没完成」，否则模型会过早交卷。

对比 V2：V2 约 20 分钟 autonomy 的瓶颈往往不是生成慢，而是 **无人验证就 drift**——代码堆叠、界面漂移、用户中途接手成本高。Agent 3 把测试从「用户验收」前移到 **Agent 内部环**，Max Autonomy 才敢把时间预算拉长一个数量级。官方还说 Agent 3 可生成其他 agents 与 automations——自测环同样适用于那些衍生产物，否则「Agent 生 Agent」只会放大 Potemkin 表面积。

浏览器自动化路线里，纯截图策略每步都要 multimodal 推理；Replit 用 CDP 拿 DOM 与 accessibility tree，断言写在 Python/JS 测试代码里——**感知降维成结构化查询**，成本曲线完全不同。博客提到的「Putting the REPL back into Replit」不是 slogan：品牌名里的 REPL 被重新绑回验证闭环，这是产品叙事与工程叙事罕见对齐的一次。

## 论坛与评测怎么说

**真用过（官方与文档可核对）**：Replit 文档写清 App Testing 触发是智能择机；Take over/Skip 流程明确。博客给出 200 分钟与 0.20 美元/session 的 median narrative，但未公开失败率分布、也未给出与 Agent V2 同任务的公开 A/B 表格。

**二手解读**：科技博客复述 Potemkin UI 问题与 REPL 混合架构，提到 `@replit/agent-core` 开源方向与 headless Chromium 栈；缺独立第三方在同一 app 套件上的长时 autonomy 对照。DriftSeas 一类文章偏架构科普，非 benchmark。

**本日未见** 大规模、可复现的「Agent 3 对 Cursor/Devin/Codex」同任务耗时与成功率长评——产品刚推，社区反馈集中在「浏览器预览很直观」与「非 web、非 JS/Streamlit 用不了 App Testing」。负面声音较少攻击生成质量，更多指向 **范围窄** 与 **测不测由 Agent 自决、用户不能强制每步全测**。Positive 反馈里，「看见光标在点我的 app」被反复提到——可视化自测降低用户焦虑，也让 Potemkin 界面更难糊弄过去：按钮假亮但点不动，预览里一眼穿帮。

## 收束：一个判断与边界

Agent 3 的真正增量不是「又会写代码了」，而是 **把 verify 纳入默认 harness**：生成、执行、浏览器走用户路径、修复，四步成环。读者该记住：**没有自测的 coding Agent 天然偏向交付「像 finished 的半成品」**——优化目标函数是「用户停止追问」，不是「用户真能用」。

Replit 用 REPL 持久化降低长测的状态成本，用子 Agent 分离「写测试逻辑」与「像用户点界面」——这两点比堆更多生成 token 更能压 Potemkin 风险。若你在 Replit 外自建 Agent，可抄的核心不是 Chromium 本身，而是 **状态在 REPL、断言在浏览器、失败回写代码** 三段式。官方称自测 median 成本 0.20 美元/session、比 Computer Use 便宜一个数量级——若你团队正在评估 browser agent 路线，应把 **结构化 CDP 断言** 与 **像素策略** 分开算账，再决定 harness 选型。

边界也要写清：仅 web；仅 JS full stack 与 Streamlit Python；200 分钟与 0.20 美元/session 是官方 median，你的 app 复杂度可能远高于 median；Computer Use 在通用桌面任务上或许更灵活，但在 Replit 垂直场景里 Agent 3 选择的是 **structured tool 优先于 pixel policy**。

Take over 与 Skip 说明 Replit 没假装全自动：人机共测仍是出口。文档写 App Testing 在 Economy/Power 开、Lite 关——算力档与验证档绑定，暗示自测是 **有成本的 compute line item**，不是魔法开关。自建 harness 的团队应预期：浏览器 session 占内存、长测占 wall time，median 0.20 美元/session 是 Replit 垂直整合后的数，换到自建 K8s 未必同价。

最终判断：**浏览器自测不是 demo 功能，而是 Agent 3 敢 claim 10 倍自主的前提——没有这条环，200 分钟只会产出 200 分钟的 Potemkin。** 下一代 coding Agent 的竞争点， increasingly 不在「谁能多写两行 Tailwind」，而在 **谁默认把 verify 写进 loop**。

Potemkin 界面如何被戳穿：Agent 生成带「提交订单」按钮的 checkout 页，Tailwind 完整、hover 态齐全；用户肉眼觉得能点——子 Agent 用 CDP 真点，断言 `POST /api/orders` 返回 201，实际 500 且 REPL 里 `lastOrderId` 仍为 null。失败信号走 **代码执行通道** 回主 Agent，改 API route 再跑同一 browser session——`lastOrderId` 跨步保留，不靠 summarization 传状态。对比纯 Computer Use：每步 multimodal 猜坐标，median 成本官方称约 0.20 美元/session 且快一个数量级——Replit 赌 **结构化 CDP 断言** 在 app builder 垂直场景更稳。与 OpenAI Codex harness 的 worktree+CDP 对照：Codex 偏 merge 前 SRE 证据，Replit 偏 **用户路径默认 on**；二者共识是 **verify 不能是高级彩蛋**。Take over 与 Skip 说明验证码、外部 OAuth 等 gate 仍要人——自测环诚实承认边界，而非假装 200 分钟全自动。

App Testing 触发是 **智能择机** 而非每改一行就测——避免交互变 endless QA，也控制 compute line item。Lite 不开、Economy/Power 在 Advanced settings 开，说明自测与算力档绑定；自建 harness 应预期 browser session 占内存与 wall time，median 0.20 美元/session 是垂直整合后的数，换自建 K8s 未必同价。范围窄（JS full stack + Streamlit）是诚实边界——非 web 场景别硬套 REPL+CDP 三段式。

---
**参考** [Introducing Agent 3: Our Most Autonomous Agent Yet](https://replit.com/blog/introducing-agent-3-our-most-autonomous-agent-yet) · [Enabling Agent 3 to Self-Test at Scale with REPL-Based Verification](https://replit.com/blog/automated-self-testing) · [App Testing | Replit Docs](https://docs.replit.com/features/agent/app-testing)
