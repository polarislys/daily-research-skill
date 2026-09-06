---
形态: 产品剖析
主题: Codex
日期: 2026-09-06
---

# Codex Harness 的真正壁垒：worktree 隔离、可查询 observability、机械架构约束

上一篇讲 Codex 三层怎么接；这篇只挖 OpenAI **harness engineering** 里让 Agent 能连跑六小时、早上交 PR 的**环境层**——不是更大模型，而是 **application legibility**：Agent 能否 boot 应用、看见 UI、读自己的 logs 与 metrics，并在 CI 里被 architecture linter 卡住。人类 scarce 的是 attention；harness 要把「可验证」做成默认能力。

## 痛点：吞吐上来之后，瓶颈变成 Agent 看不见系统

OpenAI 小团队在约五个月内合并近 1500 个 PR、产出近百万行代码，且宣称无人工手写代码——数字本身可争议，**机制**值得拆。早期进度慢，主因不是 Codex 不会写，而是 **environment underspecified**：缺工具、缺 abstraction、缺可 enforce 的内部结构。工程师的工作变成 depth-first：把大目标拆成 design、code、review、test 等块，让 Agent 构造块，再解锁更复杂任务。某步失败时，fix 几乎从来不是「再 prompt 一次 harder」，而是问：**缺什么 capability，如何让它对 Agent legible 且 enforceable？**

当 code 吞吐超过 human QA，瓶颈转为 **人类 attention**。若 Agent 只能读 diff、不能 drive 运行中的应用，就会在「编译过了」处 prematurely mark done——Anthropic 长程 harness 文档里 Claude 的同类失败，OpenAI 用 **per-change 全栈实例 + telemetery** 对冲。Fix 方向是把 UI、logs、metrics 变成 Agent 可 inspect 的一等公民，而不是让人类复制粘贴终端输出进 CLI。

## 机制一：git worktree 与 ephemeral observability

每个 change 需要 **独立、可重复、可销毁** 的运行面。OpenAI 让 app **per git worktree bootable**：Codex 为每个分支或 worktree 启动一套完整应用实例，而非多人争抢共享 staging。实例绑定 **Chrome DevTools Protocol**：Agent 用 DOM snapshot、screenshot、navigation 复现 bug、验证 fix，**reason about UI** 时不再只靠静态代码想象。

worktree 思路与「每个 PR 一个 preview environment」类似，但目标不同：preview 给人看，worktree+CDP 给 **Agent 开**。合并前 Agent 可在隔离实例里走完 user journey，把录屏或截图附进 PR description——reviewer Morning triage 时看证据链，而非只看 green CI。shared staging 上常出现「我本地没问题」：Agent 同样会中招，除非 instance 与 change 一一绑定。

**Observability** 同样 **per worktree ephemeral**：本地栈暴露 logs、metrics、traces（文中以 Victoria 系列为例），任务结束即 tear down。Agent 用 **LogQL** 查日志、**PromQL** 查指标、**TraceQL** 查链路。于是「服务启动在 800ms 内完成」「四条关键 user journey 无 span 超过两秒」从口号变成 Agent 可执行的 acceptance——它查数据、改代码、再查，**六小时 loop** 才有 ground truth。这与 sandbox 不同：sandbox 限**权限**，observability 限**可验证性**；缺后者，长程任务必然 drift。

OpenAI 文中的一个细节常被跳过：observability stack 与 app 实例同生共灭，Agent 不会误读他人 branch 的 logs，也不会在 shared staging 上「修好了其实环境不对」的假阳性。Prompt 里写 SLA 时，Agent 应能生成 LogQL/PromQL 查询并贴结果进 PR——这使 review 从「信你说」变成「信数据和截图」。CDP 与 telemetery 组合，相当于给 Agent 同时装上了「用户的眼睛」和「SRE 的仪表盘」。

## 机制二：仓库即 system of record 与机械架构约束

Context 是稀缺资源，**巨型 AGENTS.md** 已证失败——挤占 task、一切重要、难 freshness check、迅速变 graveyard。替代方案：`AGENTS.md` 作短 **map**，正文在 `docs/` 分层：design-docs、exec-plans、generated schema、QUALITY_SCORE、RELIABILITY 等，**progressive disclosure**。Slack 里对齐的架构决定若不进 repo，对 Agent 等同不存在——与「新同事三个月后入职」的盲区相同。

Architecture 靠 **invariant 而非 micromanage**：每个 business domain 固定层（Types → Config → Repo → Service → Runtime → UI），依赖方向机械校验；cross-cutting 只经 **Providers** 注入。Custom linter 与 structural tests 由 Codex 自己编写，**error message 即 remediation instruction**——违例时把修复指南注入 Agent context。边界 parse、structured logging、文件大小上限等 **taste** 亦编码为 lint。文档 alone 不够；**mechanical enforcement** 才让 fully agent-generated codebase 不散架。

OpenAI 举例：不必规定必须用 Zod，但必须在 boundary parse data shape——implementation 自由、invariant 不自由。Agent 在 strict boundary 内反而更快，因为搜索空间被砍掉；这与「给 Agent 无限自由反而 one-shot 烂尾」的长程 harness 观察一致。Providers 作为唯一 cross-cutting 入口，也避免 Agent 随手 import 深层 internal module——dependency linter 报错即带「应经哪个 Provider 暴露」的说明。

CI 不止测 product：**doc-gardening Agent** 扫描 stale docs 开 fix PR；knowledge base 的 cross-link、freshness 有 dedicated CI job。**Evaluation harnesses**、dashboard definition、release scripts 也在「Agent 生成物」清单里——repo 自我维护是 harness 的一部分，而非运维杂项。

**Ralph Wiggum Loop**（OpenAI 文中原名）指 Agent 自 review、请求 cloud/local agent review、迭代直到 reviewer 满意——environment 约束为此服务：没有 worktree+observability，self-review 只剩读 diff，loop 空转。evaluation harness 与 product code 同权，意味着改 benchmark 也要 PR，避免 Agent 过拟合自家测试。release tooling 由 Agent 写，人类 steers 发布策略而非手写脚本——这是「人类 attention 转移」的具体落点。

## 机制三：merge 哲学、自治闭环与 garbage collection

高吞吐下，**长寿命 PR、flake 无限 block** 反productive：在此 harness 下 corrections cheap、waiting expensive——低吞吐团队不宜照搬，但理解 tradeoff 必要。

Martin Fowler 等外部拆解常把 harness engineering 概括为 **context engineering + architectural constraints + feedback loops + observability** 四块——与 OpenAI 原文章节一一对应。落地时可按成熟度分期：第一期 worktree boot + 基础 CI；第二期 LogQL/PromQL 进 Agent toolset；第三期 custom linter 与 doc-gardening Agent。跳过第一期直接追求 six-hour run，通常会得到「跑很久但 merge 不了」的 PR 堆。Agent 可 end-to-end：复现 bug、录屏、fix、再验证、开 PR、respond review、修 CI、仅在需 judgment 时 escalate human、merge——依赖上述环境与 tooling 投资，**不应假设裸 repo 即可复现**。

这段「自治闭环」清单里，**respond review** 与 **agent-to-agent review** 同样重要：OpenAI 团队 push review effort 向 Agent 侧，人类非必须 approve 每一 PR。这与高吞吐 merge 哲学配套——若 human 仍是唯一 gate，six-hour run 产出只会堆积 queue。你的组织若合规要求 human sign-off，可保留最后一跳，但中间 review iteration 仍应尽量 Agent 化，否则环境 legibility 的投资回不了本。

Agent 会复制 repo 里已有 pattern，包括次优的，导致 drift。**Golden principles** 加定期 background Codex 扫偏差、开可快速审的 refactor PR，像 **garbage collection**——human taste 写一次，持续 enforce。OpenAI 坦承 **behavior harness**（Agent 写的代码真满足用户）仍是最难部分；structural harness 大致成形，verifiable domain 仍要 human judgment 作 escalation。

## 对照 Anthropic 长程 harness 与边界

| 维度 | Anthropic 长程 harness | OpenAI harness engineering |
|------|------------------------|----------------------------|
| 状态恢复 | progress.txt + git + feature_list.json | docs/ + exec-plans + worktree 实例 |
| UI 验证 | Puppeteer MCP | CDP + per-worktree app |
| 性能验证 | 较少强调 | LogQL / PromQL / TraceQL |
| 架构 | 增量 feature、commit 清洁 | Domain layering + custom linter |

二者共识：**环境先于单次 prompt**；OpenAI 更激进地把 observability 与 repo 知识库产品化。 transferable 的并非「零手写代码」口号，而是 **worktree 隔离、可查询 telemetery、linter 即 Agent 教材、文档当 code**——模型可换，这几样仍 compounding。若只能抄一件事，优先抄 **per-change 可 boot + 可查询 logs**；没有它，feature list 与 Skill PR 都难以自动验收。OpenAI 内部 product 有 daily power users 与 alpha 外测——environment 约束是为 **真实 deploy/break/fix 循环**服务，不是 demo 一次性 green build。工程师角色从「写代码」转为「设计 environments、specify intent、build feedback loops」——harness 文档读的是这一类岗位描述。

human QA 瓶颈被 worktree + CDP 部分替换后，PR 审查重心从「代码看起来对不对」转向「Agent 是否用 trace 证明过行为」。这改变 reviewer 技能：会读 LogQL 查询与录屏证据的工程师，比只会扫 diff 的人更适配 agent-first repo。OpenAI 描述 Agent 用 `gh`、本地脚本、repo 内 Skills 拉 context——**人类不应复制粘贴进 CLI**，否则 harness 投资被绕开。

**Entropy management** 章节常被忽略：Agent 复制 uneven pattern 导致 drift，周五「清 AI slop」不可 scale 后，才演进为 golden principles 与 background refactor Agent。这与传统 tech debt sprint 不同——规则写进 repo 后由 Agent 自己扫、自己开 PR，human 只做分钟级 approve。文档 gardening 同理：stale doc 不是提醒工程师更新，而是 Agent 开 fix PR，CI 验证 cross-link。

Plans 作为 first-class artifact（active / completed / tech-debt co-located）让跨 session 任务不依赖外部 Notion。Agent 读 exec-plan 继续 half-done 功能，比读 Slack 摘要可靠——again，**in-repo legibility**。QUALITY_SCORE 一类文档给 domain 打分，improver 式 meta loop 可指向「哪层腐化」，OpenAI 未详述是否已自动化，但结构已预留。

收束：Codex Harness 环境约束回答的是「Agent 能否在无人值守时自证正确」；worktree、observability、mechanical architecture 三件套，缺一则长程自治不成立。

## 读者可带走的一个判断

不必复制「零手写代码」，但应复制 **legibility 投资顺序**：先让 change 能 boot 独立实例，再让实例可观测，再把架构 violated 变成带 remediation 的 linter 错误，最后才追求 six-hour unattended run。许多团队卡在第三步——文档很多，却不可 mechanical check；Agent 读到的与代码真相同步靠 luck。OpenAI 与 Anthropic 长程文可对照读：前者偏 telemetery 与 repo 知识库，后者偏 feature list 与 incremental commit；合起来才是完整环境.harness 不是模型促销词，是**人类 attention 的替代品**——投在哪里，决定 Agent 能 unattended 走多远。

OpenAI 估算该内部产品约为手写代码 **1/10 时间**——争议点不在比例，而在前提：million LOC 若缺 architecture linter，维护成本会非线性爆炸。harness engineering 真正卖的是 **可复用的环境配方**：worktree、CDP、Victoria 栈、docs/ 树、golden principles GC。拿走这些，只剩「很多 Agent 写的 PR」，不一定等于 velocity。对小团队而言，even 只实现「每个 feature branch 能 docker compose up + 一条 smoke test Skill」，也已比裸 Codex CLI 稳一个数量级。

举一个 worktree + observability 闭环的微观例子：Agent 改完 checkout 流程，在 **本 worktree** 起 app，CDP 点「应用优惠码」——DOM 有按钮但 network 层 404；Agent 不猜，用 LogQL 查 `path="/api/coupon"` 的 404 span，改路由注册，再跑 PromQL 看 p99 是否回到两秒内。PR 描述附查询结果与截图，morning reviewer 审的是 **证据链**，不是「Agent 说修好了」。若用 shared staging，邻居 branch 的 deploy 可能污染 logs，Agent 会「修好了其实环境不对」——per-worktree ephemeral stack 就是为消除这类 false positive。这与 Replit Agent 3 的浏览器自测同目标、不同介质：OpenAI 偏 **SRE 可查询**，Replit 偏 **用户路径点击**；二者都说明 harness 竞争点已从「会不会写代码」移到「会不会自证行为」。

custom linter 的 remediation instruction 也值得单独记：违例不是「Layer violation」，而是「`OrderService` 不得直接 import `PaymentRepo`，请经 `PaymentProvider` 注入」——Agent 下一轮读 error message 即知怎么改，等同 **可执行的 harness 文档**。这与 BASM 的 boundary 字段同哲学：约束要可 gate、可修复，不能只剩 prose 原则。六小时 unattended run 的前提是 **失败可观测、违例可机械拦截**；缺 linter 与 observability，Agent 只会产出「编译过、行为未证」的 PR 堆。

---
**参考**
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform)
- [openai/codex](https://github.com/openai/codex)
