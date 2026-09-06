---
形态: 产品剖析
主题: Warp
日期: 2026-09-06
---

# Warp 把 Agent 进化拆成两条 Skill，中间只留人类反馈

这篇只回答一个问题：Warp 怎么让 code review、issue triage 这类 Agent 不靠反复改 prompt、也不靠 session 记忆，就能在真实协作里越用越准。Anthropic 官方博客与宝玉的解读都指向同一条可复查的机制——**两条 Skill** 夹一个**人类反馈环**，把经验沉淀成可 diff 的文件，而不是让它随对话蒸发。

## 痛点：反馈在 session 结束时蒸发

Warp 的 code review Agent 初版能跑，但工程师普遍抱怨评论噪音大、建议缺乏领域价值。团队最初走两条弯路：一是盯着失败样本人工改 prompt，输出确实变「能用」，却无法 scale，每次 regression 都要有人重新教；二是扩充 AGENTS.md 等 context 文件，有帮助，但离「从反馈中学习」仍差一整环。

Zach Lloyd 在 Anthropic 访谈里把根因说透了：无论 Agent 承担什么任务，人类对输出的纠正——点赞、驳回、补充理由——通常随 **session 结束**而消失，critical context 进不了 **agentic loop**。这和长程 coding Agent「换窗就失忆」是同一类问题，只是 Warp 选择用 **procedural Skill** 而不是 inference-time memory 来承接。

宝玉在《Warp 如何让 Agent 自我进化》里把对比讲得清楚：**memory** 是 Agent 在推理过程中自动写入、持续漂移的状态；**Skill** 则是稳定的「怎么做 X」， deliberate 修改、走 PR、可审计。Warp 押后者，因为 file-based Skill 既能被 Agent 读写，又能被 git 历史约束，且 **improver Skill** 的 observer 逻辑可以跨 domain 复用——code review 与 triage 共用同一套「读反馈、提议最小改动」骨架。

## 机制：inner Skill、outer Skill 与人类信号如何转一圈

架构刻意保持极简：**base Skill + improver Skill + 人类反馈**，中间没有黑盒 fine-tune。

**Inner / base Skill** 承载功能域知识。PR 打开时，review Agent 读取 base Skill 里的原则、代码库惯例引用与附属资源，产出 review；triage Agent 则读取 label 语义、调研步骤，对新 issue 打标并建议方向。Skill 的关键设计是 **progressive disclosure**：主 Skill 文件保持短小，细节放在脚本、示例与链接文档里，Agent 按需加载，避免把整本手册塞进 context 窗口。Anthropic 博客里强调，skills 是 file based encodings of knowledge——知识在文件里，不在 raw prompt 里膨胀；这与 agentskills 开放格式方向一致，Warp 是早期大规模实践者之一。

写 base Skill 时，Warp 团队反对 exhaustive variable naming tables，而主张「Look for repeated code」这类原则——像带一个聪明同事，而非写死 if-else 规则表。提供 **why** 让模型在未见过的文件上仍能推理，而不是机械匹配字面 pattern。Skill 还可 bundle Python 脚本：improver 拉 GitHub 数据时复用同一脚本，避免每次 run 现写代码，这也是 resource file 而非 inline code 的原因。

**人类反馈** 是环的中枢，也是 signal 质量的决定因素。可以是 thumbs up/down，但更值钱的是带领域理由的否定——「你建议重命名这个变量，但我们 repo 里全局变量应遵循某某 naming convention」。Warp 把采集点放在人已在工作的地方：PR comment、issue comment，**无额外提交步骤**。Zach 强调 low friction 决定 signal 能否持续流入； friction 一高，团队就会停止纠正，loop 空转。Capture where people already work 这一原则，对 internal tool 同样适用：若 feedback 要填单独表单，多半永远填不满。

**Outer / improver Skill** 扮演 scheduled **observer**，不按单次任务触发，而在 Warp 内部 orchestration 平台 **Oz** 上定时运行。典型流程：improver 认证 GitHub，执行 Skill 捆绑的 Python 脚本，拉取近期带人类 feedback 的 issue 或 PR，汇总为 JSON 再读回 context；对比「Agent 曾建议什么」与「人类如何回应」，提出对 base Skill 的**最小 edit**，开 PR 修改 Skill 文件本身。PR 描述应写清触发了哪些 signal、改了哪条原则；人 review、merge 之后，下一次 inner Skill 运行即继承改进——**进化发生在文件层，不在权重层**。

Issue triage 的公开案例很能说明环如何闭合：首轮 triage 漏打 `ready to spec` label；maintainer 在 issue 原处留言，解释「问题已描述清楚、UI/UX 形态未定也可进入 spec 阶段」以及原因。improver 据此在 inner Skill 里补一条 label 规则，整次更新是可 diff 的 markdown，不是不可解释的模型漂移。Warp 在开源 repo 上为 spec-writing、review、triage 各跑独立 loop，但 improver 模板高度共享——差别主要在 domain 脚本与 base Skill 内容。

公开 webinar 与博客还提到 scale：开源 repo 有数百 contributor、数千次 review，feedback **volume 有帮助但 quality 更关键**——一条 senior 工程师的详细否定，胜过大量无理由 thumbs down。Warp 用同一 loop 管理整个开源仓库，说明双 Skill 架构在多人协作下仍可行，前提是 GitHub 上 feedback 习惯已成熟。对 closed-source 团队，等价物是 PR comment 与内部 issue 系统，关键是 signal 能否被脚本 harvest 且带 rationale。

Warp 团队还总结了写 Skill 的品味：**principles, not rules**——像教聪明人，而非编程计算机；**explain the why**，让 Agent 泛化；improver Skill 值得额外投入，因为 observer 机制可复用到多种 Agent。Skills 与 memory 勿混：前者 run-agnostic、 deliberate 变更；后者 inference 写入、不可控漂移。

## 对照、误区与边界

相对 **DPO / 在线 RL**，这条路径不碰模型权重，优势是可解释、可回滚、可 code review、可设 human gate；代价是进化速度受 PR 吞吐与人类标注质量约束，难以做毫秒级 policy 更新。与 Anthropic 长程 harness（feature list + incremental progress + git 清洁状态）相比，Warp 把「进度与规则」写进 **Skill 文件**而非 progress.txt，更适合多 Agent 并行、每条线独立进化的组织形态。

需要直说的边界：**错误 feedback 一定会来**。improver 必须有 sanity-check、信源过滤与终审 human gate，不能 blind accept。若 domain **可验证**——有 golden output、测试 harness、可复现脚本——应优先让 Agent 对 reference 调 Skill，人类 feedback 作补充；Warp 在 FAQ 里明确建议 **verification harness first**。全局是否在改善，团队应盯 time-to-merge、contributor 数、成本等已有指标，再考虑喂回 improver——公开材料里这仍是 best practice，尚未看到全自动 metrics-driven improver 的完整落地数据。

相对 Claude Managed Agents 等**托管 harness**，Warp 模式偏 repo 内自治进化，适合开源协作与高频 PR；不适合希望零文件运维、全靠平台侧 memory 的产品。对想用 Skill 做组织知识的团队，可复制的是**双 Skill 拓扑 + 低 friction 反馈采集 + PR 合入**——模型可换，环的结构可留。

再往下拆 improver 的「最小 edit」原则：它不是重写 base Skill，而是从 feedback corpus 里抽取可泛化的 delta。一次 triage 漏 label 不应导致 Skill 膨胀成穷举表；maintainer 写清的「为什么」会被 improver 归纳为原则，例如「问题陈述完整且可行动即可进入 spec，UI 细节可后续迭代」。这与 Warp 强调的 **principles not rules** 一致——exhaustive naming rules 会让 Agent 局部 pattern-match，而原则加 rationale 才利于跨文件泛化。

Oz 调度层在公开叙事里角色常被低估：improver 不是 cron 调脚本那么简单，而是 authenticated agent run，能拉 GitHub、写 PR、走与 human 相同的 review 路径。这意味着 **harness 与 Skill 进化同构**——进化本身也是 Agent 任务，受同一套 permission 与 audit 约束。Warp FAQ 还问：需要几个 improver？答案是中间路线——模板化 base loop 覆盖共性，domain 权重分层；少数 improver 各管一类 Agent 即可，上百 Agent 不应上百 improver。

若对照 **Skill Imitation Trap** 一类研究：只从成功轨迹蒸馏 Skill、再 retrieval 放大，可能让 Agent 更敢用错工具。Warp 的双 Skill 环用**人类否定信号**对冲，且改动必须 PR 可见——失败模式不会 silent 进入 base Skill。尚未见 Warp 公布量化曲线（如 review 采纳率随时间），但机制上 credit assignment 落在「哪条原则该改」，比 end-to-end RL 更可审计。

收束一句：**Warp 把组织知识从 prompt 迁到 Skill 文件，把改进从人肉改 prompt 迁到 improver PR**；人类反馈仍是稀缺 signal，环的价值在于让 signal 复利而非蒸发。

## 读者可带走的一个判断

若你已在用 Agent 做 code review 或 triage，却感觉「每次都要重新教」，先查 feedback 是否落在 session 外可持久化处，再查改进是否走可 audit 的文件路径。Warp 证明：**两条 Skill 加 PR 合入**足以构成自我改进闭环，不必等权重微调；难点在 feedback 质量与 improver 写法，不在模型是否最新。宝玉文与 Anthropic 一手材料可交叉验证：Oz 调度、bundled 脚本拉 GitHub、issue triage 漏标案例，均可对照 repo 公开流程复现思路。团队若无法做 scheduled improver，退而求其次也应把否定理由写进 Skill PR，而非留在 Slack——否则 harness 再强，domain 知识仍不可 compounding。

issue triage 漏标案例再推一步：maintainer 在 issue 留言解释「UI 未定也可进 spec」——improver 定时跑，Python 脚本 harvest 带 rationale 的 comment，对比 Agent 当时建议的 label，开 PR 在 base Skill 补 **principles 级** 规则而非穷举 label 表。Merge 后下次 triage 继承；这与 Hermes background review 写 skill patch 同信号源（人类纠正），但 Warp **强制 Git 可见**、Hermes 可静默。相对 DPO：Warp 不碰 logits，偏好对变成 **markdown diff**；优势是可 rollback、可 code review，代价是进化速度绑 PR 吞吐。FAQ 强调 **verification harness first**——若有 golden test，Agent 应先对 reference 调 Skill，人类 feedback 补充 edge case；否则 improver 会把噪声 feedback 也写进 base Skill，组织知识反向 compounding。

Oz 上 improver 是 authenticated agent run，与 human 走同一 review 路径——进化本身受 permission 与 audit 约束，不是 cron 悄悄改文件。开源 repo 数百 contributor、数千 review 说明 **volume 有帮助但 quality 更关键**；一条 senior 详细否定胜过大量无理由 thumbs down。Skills 与 memory 勿混：前者 run-agnostic、deliberate 变更；后者 inference 写入、不可控漂移——Warp 全文都在强化这条边界。

---
**参考**
- [How Warp builds self-improving agents on Claude](https://claude.com/blog/how-warp-builds-self-improving-agents-on-claude)
- [宝玉《Warp 如何让 Agent 自我进化》](https://mp.weixin.qq.com/s/1YaHaOC1veK3dJhlJyvE9Q)
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
