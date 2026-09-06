---
形态: 产品剖析
主题: Claude-Managed-Agents
日期: 2026-09-06
---

# Claude Managed Agents：把 brain 和 hands 拆开，TTFT 才能下来

这篇只读 Anthropic 2026 年 4 月工程文里的架构选择：**脑手分离**、session 作为上下文对象、以及对 **TTFT（time-to-first-token）** 的影响。值得看，是因为 harness 里的「贴心假设」会随模型变强而过期——Managed Agents 试图用**接口稳定性**换**实现可替换**，回答「programs as yet unthought of」的老问题。

## 痛点：一体化容器是 pet，不是 cattle

Lance Martin 等人描述的第一版架构：session、harness、sandbox **同容器**。好处直观——文件编辑是直接 syscall，服务边界少，早期迭代快。团队可以先把「Claude 能改 repo」做出来，再谈 scale——典型 startup 路径。代价很快暴露：

容器挂则 **session 丢**；卡死只能工程师 shell 进去 nursing，而 WebSocket 事件流分不清 harness bug、网络丢包还是容器 offline——**缺乏可调试性**。用户看到「agent 没响应」，后台可能是 harness 死锁、也可能是 sandbox OOM，但对外只有一个 stuck 状态。更糟的是**安全**：不可信代码与凭证同容器，prompt injection 读环境变量就能用 token 开 unrestricted session 再委派任务；「缩小 token 权限」仍是假设模型不够聪明，而模型在变强，攻击面随能力一起涨。

第二痛点是 **harness baked-in 拓扑**：默认 Claude 操作的东西都在容器旁边。客户要接自家 VPC，只能 network peer 或把 harness 搬到客户环境——产品假设变成集成障碍。VPC 场景里，容器里的 harness 还假设能直接 `git clone` 用户 repo；一旦 repo 只在客户私网，要么扩 peer，要么放弃托管——都不是 product-scale 解。

同时 **TTFT** 被容器启动绑架：每个 session 先 clone repo、boot 进程、拉 pending events，**才开始 inference**；即使用户这轮只想问一句不改代码，也付全量容器成本。官方把 TTFT 定义为用户从「提交工作」到「第一个 response token」的等待——这是体感 latency 的核心指标，比 total job time 更敏感。many brains 意味着 many 容器，scaling 贵且 cold start 方差大。

## 机制：三个虚拟化接口

Managed Agents 把 agent 拆成三个可替换抽象，类比 OS 把硬件虚拟成 process/file：

**Session**——append-only **事件日志**，durable 存于 harness 外。它不是 Claude 的 context window；长程任务常超窗口，compaction、memory tool、trimming 都是**不可逆**的保留/丢弃决策——难知未来 turn 需要哪些 token。Prior work 把 context 存成 REPL 外 object 让 LLM 写代码 slice；Managed Agents 的 session 是同类哲学：**完整事件在 session，窗口里只是当前视图**。Harness 可 organization context 换高 prompt cache hit rate——分离因未来模型需要什么 compaction 无法预判。

**Brain（harness + Claude）**——无状态 orchestrator。循环中 `emitEvent(id, event)` 写 session；崩溃则 `wake(sessionId)` + `getSession` 从最后事件续跑。Harness **离开容器**；调 sandbox 与调 MCP **同形**：`execute(name, input) → string`。这意味着 Claude Code 若作 inner harness，其 tool call 在 Managed 眼里仍是 execute 的一种 backend——meta-harness 不绑定某一种 loop 实现。

**Hands（sandbox / tools）**——cattle。容器死则 tool error 回 brain，Claude 决定是否 `provision({resources})` 新实例。标准 recipe 化 provision 意味着新 container 不继承旧 container 的脏状态——每次执行环境可重现，利于 debug 与安全。Git：clone 时注入 repo token 到 remote，sandbox 内 push/pull 不碰 token。Custom tools：OAuth 存 vault，MCP 经 session-scoped proxy 取凭证——**structural fix** 是 sandbox 够不着 secret，而非信模型不读 env。两种模式：**凭证 bundled 在资源初始化**（如 git remote）与 **vault + proxy**（如第三方 SaaS OAuth）——对应不同 exfiltration 路径。

Anthropic 在文里承认：narrow scoping token 是 mitigation，不是 structural fix——Claude 越来越聪明，limited token 也可能被滥用去 spawn 新 session。因此 hands 必须在 trust zone 外。

**TTFT 是用户体感的杠杆。** 脑手分离后，不需 sandbox 的 session **立即起 brain**；容器仅在 tool 路径 **lazy provision**。官方数据：p50 TTFT 降约 **60%**，p95 降超 **90%**——p95 改善更大，说明 tail latency 里「等容器」占比极高；问答型 session 受益最明显。Scaling many brains = 起多个无状态 harness，而非 N 个宠物容器；brain 本身也可水平扩，session log 在共享存储上成为唯一 coordination 点。

这与 Claude Managed Agents 文档入口强调的「Get started with docs」一致：产品边界是 platform API（session、execute、provision），不是某一种 Claude Code 版本——客户集成应绑接口，不绑实现。

**Many hands** 随之可行：brain 在容器、手机、私网 MCP、自定义 tool 间路由——比单 shell 全能更难 cognitively，但单容器 SPOF 消除；一 hand 挂不拖死全部 state。Brain 之间也可传递 hand：一个 research agent 把 sandbox 句柄交给 coding agent——接口统一在 execute，拓扑可演进。

工程文还强调 **don't adopt a pet**：一体化设计让调试窗口只剩 WebSocket，工程师 shell 进容器又触碰用户数据——合规与 observability 双输。Decouple 之后，brain 日志与 hand 健康度可分开监控。

## 落地时怎么选：一张表画清责任

搭栈时建议画四列：**harness（brain）**、**OpenSandbox（hand 执行环境）**、**Vault（凭证）**、**Temporal（跨天编排）**。Managed Agents 解决「session 与 sandbox 拓扑、首字延迟」；Temporal 解决「这笔退款三天后还要接着跑」。二者可叠：Managed 的 `execute` 背后创建 OpenSandbox 实例跑代码，Temporal workflow 在 tool 缝上挂审批策略。若你只跑本地 Claude Code、没有跨天审批，Managed 与 Temporal 都可能过重——这不是产品不好，是威胁模型没长到那一步。

对国内团队，还要注意 **数据驻留**：Managed 是 Anthropic 托管云；本地 Hermes 式 `.hermes` 目录则 learning 全在磁盘。选平台前问：进化发生在文件里还是发生在 vendor session 里？文件层可 git 备份，session 层靠 SLA 与导出 API——两条合规故事不同。

从成本看，**lazy provision** 省的不只是钱，还有调度排队：问答型 session 不必为「可能根本不会执行的 bash」预付整台容器。官方 p95 TTFT 降幅大于 p50，说明长尾里「干等环境」占比极高——这类优化对交互式产品比批处理更敏感。若你的产品形态是「用户盯着屏幕等第一个字」，Managed 的脑手分离比换更大模型更划算。

集成时别把 **meta-harness** 理解成「又一个 Claude Code」：Code 是跑在 Managed 上的一种 domain harness；你绑的是 session、execute、provision 接口，不是某次 Claude Code 版本。模型换代时，该删的 context reset、该改的 compaction 策略，由 Anthropic 在 brain 实现里替换——你的集成代码不应写死「每 N 轮清空上下文」这类假设。

## 对照：meta-harness，不是又一个 Claude Code

Anthropic 称 Managed Agents 为 **meta-harness**：对 Claude 未来需要多少 brain/hand **不预判**，对 session 与 execute **强意见**。Claude Code 仍是优秀 domain harness，可跑在 Managed 之上；工程文举例：Sonnet 4.5 有「context anxiety」早收尾，harness 加强制 reset；Opus 4.5 行为消失，reset 成 **dead weight**——这正是为什么要接口稳定、实现可换。Effective harnesses for long-running agents 那篇里的 compaction、memory tool，在 Managed 里变成 session + harness transform 的分工，而不是删掉历史事件。

Managed Agents 也是 Anthropic 对「harness engineering 会持续过时」的产品级回应：模型升一代，pet container 里绑死的优化就要审计一遍；meta-harness 把过时的成本限制在 brain 实现，不波及 session 与客户集成。

对平台客户而言，Managed 卖的是 **长程 SLA + 安全默认 + 接口稳定**；你仍可在 execute 背后接 OpenSandbox 作 hand、接 Temporal 作跨天 Saga——meta-harness 不垄断编排，只垄断 Claude 如何 durable 读 session、如何无凭证调 hand。这与「Claude Code 很强所以不需要平台」不矛盾：Code 是 harness 的一种，Managed 是跑 harness 的 OS。

与 Temporal outer harness 比：Managed 偏 **Anthropic 托管平台的 brain/hands/session 拓扑** 与凭证代理；Temporal 偏 **workflow durability、turn、AgentEvent**——客户可 Managed 跑 Claude、Temporal 管退款 Saga。与 Hermes 比：Managed 云托管、enterprise SLA；Hermes 本地 learning loop。与 OpenSandbox 比：Managed 的 hand 可以是 OpenSandbox 创建的实例——execute 抽象允许 sandbox 在后端替换。

边界：托管意味 durability、调度、vault 交平台；regulated 深度定制仍可能自建。误区：decouple 后 harness 变简单——multi-hand 路由、provision 失败重试、session slice 策略，complexity 只是搬家。另一误区：TTFT 优化等于「不要 sandbox」——lazy provision 是按需创建，不是取消隔离。

可带走的一句判断：**Managed Agents 把 session 从 context window 里解放出来，把 sandbox 从 harness 进程里解放出来——TTFT 下降是副产品，真正买的是 harness 假设可随模型换代而换掉，而不丢长程状态与安全边界。**

把 lazy provision 落到一次真实交互：用户打开 session 问「这个 repo 的 README 讲什么」——brain 立刻起 inference，**不**先 clone、不 boot 容器，p50 TTFT 因此下来；同一 session 下一句「帮我在 src/utils 加个单测」，brain 才 `provision` sandbox，`execute("bash", ...)` 跑测试。若 sandbox OOM，event 流里记 tool error，brain 读 session 决定重试或换 resources——session log 完整，用户侧仍是一个 thread。对比旧架构：第一句问候也要付容器冷启动，且容器挂则 **整 session 丢**；现在 session 在 harness 外 durable，hands 可死可换。与 Warp 双 Skill 进化对照：Managed 不管 domain 知识怎么 PR 合入，它管 **brain 如何无状态地读 session、调 hand**；你在 execute 背后接 OpenSandbox 或 Temporal，接口形状不变。

Session 作为 append-only 日志还有一层对 **DPO / 偏好学习** 的隐含价值：完整 event 序列可导出成 trajectory，供 offline 偏好对构造——哪次 execute 导致人类 thumbs down，不必靠模型回忆。Enterprise 场景里，session 导出 + vault 代理凭证，比「把 API key 塞进 sandbox env」更符合 audit；这也是文里说的 structural fix：hands 够不着 secret，攻击者即使 prompt injection 成功，也拿不到 OAuth refresh token 去 spawn  unrestricted session。落地时先画 trust zone：brain 在 Anthropic 云、hand 在客户 VPC、session 在共享存储——三线分离后，再谈要不要 Hermes 式本地 `.hermes` learning；Managed 解决的是 **托管拓扑**，不是 personal skill 进化。

再补 **crash recovery** 的一帧：worker 在处理 turn 中途 OOM，新 worker `wake(sessionId)` 读最后 event——可能是「tool 已提交、结果未写回」；harness 从该点续跑，不重复已完成的 inference。这与 Temporal Event History replay 同族，但 Managed 的粒度是 **session event** 而非 business workflow step；二者可叠：Managed 管 Claude 怎么 durable 读上下文，Temporal 管退款 Saga 跨天等审批。many hands 路由时，同一 session 里先 `execute("local-bash")` 再 `execute("customer-vpc-mcp")`，失败隔离在 hand 层——brain 状态仍在 session，用户侧仍是单 thread 体验。

---
**参考**
- [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)
