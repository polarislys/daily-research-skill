---
形态: 新方法
主题: Skill自进化
日期: 2026-09-06
---

# 多 Agent 团队该改谁的 Skill？MASkills 把 credit 打到每一次技能调用上

这篇只答一个问题：多 Agent 系统跑完一条轨迹，团队奖励涨了或跌了，**该改哪个 Agent 的哪条 Skill**？arXiv:2609.02094 的 MASkills 把优化对象从参数空间换到 Skill 空间，用 skill-conditioned credit assignment 把「语言版 policy gradient」落到 SKILL.md 文件夹上。

## 为什么 episode 反思改不了多 Agent 的 Skill

Reflexion、经验记忆能记下「发生了什么」，但三条硬伤拦住了 continual improvement。第一，记忆难精确 invoke——堆在 vector store 里的段落，Agent 不知道何时该拉哪一段。第二，库越大噪声越多，有用 lesson 与 stale 记录混在一起。第三，也是多 Agent 特有的：**team reward 归因到 agent 就停住了**，到不了「第 7 步调用的那条检索 Skill」。

想象一个三人协作：Planner 拆任务、Researcher 调搜索 Skill、Writer 调格式化 Skill。最终答案错了，episode 反思写「Researcher 搜到的来源不可靠」——这对，但改哪里？改 Researcher 的系统 prompt？改搜索 Skill 的 query 模板？还是 Planner 的分解 Skill 把子问题切错了，导致 Researcher 的 Skill 根本不该被调用？**Agent-level 反馈回答不了「哪条 Skill artifact 该动刀」**。更麻烦的是多 Agent 的 **positive credit 也会误伤**：Writer 的格式化 Skill 完美，但 Planner 的分解 Skill 错了——team 失败时 Writer 的 Skill 不该被 punish，却常被全局反思一笔带过。

单 Agent 的 EvoSkill、MemSkill 已经在 Skill 空间里做 textual feedback descent：Executor 跑任务，Proposer 诊断失败，Skill-Builder 写进 SKILL.md，held-out 验证不过就 rollback。可一到 Dec-POMDP 式的多 Agent 协作，一条轨迹里多个 Agent、多条 Skill 交错 invocation，counterfactual 变得组合爆炸——缺一条 Skill 的轨迹无法靠「少看一段 memory」模拟。

MASkills 的切入点很直接：Skill 是比自由文本 memory 更可操作的单元。Anthropic 式 Skill 设计——metadata 轻量曝光、按需加载 procedure 与 scripts——正好适合 progressive disclosure：prompt 不炸，行为可特化。难点变成三个：skill-level credit assignment；跨 rollout 的 noisy language feedback；Skill 是离散语言 artifact，改错一步就改 action space，比调神经网络权重危险得多。

跟调参相比，改 Skill 像改源码仓库：merge 一条烂 Skill 等于把 bug 写进默认分支。MASkills 用 held-out validation 和 rollback 当 CI——不过闸就不发布。这跟 EvoSkill 的 Pareto 保留思路一致，但多 Agent 还要问：**一条 Skill 帮了本 Agent 却害了队友**，validation 必须看 team metric，不能各 Agent 各验各的。

## MASkills 的四步环怎么转

框架是 language-space 版的 policy optimization，结构借 TextGrad、LangMARL，但优化变量是各 Agent 的 skill library $\mathcal{K}_i$，不是 $\theta$。

**第一步，Multi-Agent Skill Execution。** 每个 Agent 的 prompt 只注入 skill.yaml 里的 name 与短描述；真正 invoke 时才把 SKILL.md 和辅助资源（脚本、参考文件）动态加载成 tool call。执行日志里留下可观测的 skill trace——哪一步、哪个 Agent、用了哪条 Skill，一目了然。Skill 暴露成 callable tool 而非全文塞进 context，是为长 horizon 留预算。Dec-POMDP 里各 Agent 只看到自己的 observation，但 **skill trace 对 centralized critic 是全队可见的**——这是 attribution 的信息基础；没有 trace，counterfactual 只能猜。

**第二步，Skill-Conditioned Credit Assignment。**  centralized LLM Critic 对轨迹里**每一次 skill invocation** 做 counterfactual 比较：「若这一步没调用 Skill k，团队结果会怎样？」输出结构化自然语言 credit——帮了协调、冗余、致败、该泛化还是该特化。推不到单条 Skill 的效应，还有 agent-level residual credit，专门喂给 **skill induction**：现有 Skill 库解释不了这次失败，可能需要新建一条 Skill 目录。Critic 输入含完整轨迹与各 Agent 的 skill trace，输出不是一句「好/坏」，而是 **可操作的编辑建议**——例如「搜索 Skill 的 site: 过滤器在本任务多余，应特化为学术源」。

这一步是多 Agent 版与单 Agent EvoSkill 的分水岭。Team success 不能平均分给所有 invoked Skill；必须问 **边际贡献**，而边际贡献在语言空间里用 counterfactual 叙述近似。

**第三步，Stabilized Language Gradient。** 原始 critique 噪声大、批次间矛盾——同一 Skill 在轨迹 A 被夸「query 精准」，轨迹 B 被批「漏了关键约束」。Critic 文本先经 LLMGrad 抽成 edit direction，再 hierarchical aggregation：trajectory 级 → skill 级 → agent 级 → interaction topology 级。最后 momentum smoothing 跨 learning cycle，得到 temporally stable 的「语言梯度」，避免 Skill 库在噪声下震荡。LangMARL 已在 language space 做 credit，MASkills 把粒度从 agent prompt 推到 **skill artifact**——这是从「改谁的话术」到「改谁的 playbook」的位移；playbook 可版本化、可 diff、可 rollback，比改 system prompt 更适合团队工程。

**第四步，Credit-Driven Skill-Space Optimization。** 四个算子驱动库演化：**refinement** 改现有 SKILL.md；**induction** 新建 Skill 目录；**consolidation** 合并功能重复的 Skill；**pruning** 删掉持续负 credit 的 Skill。每次更新都过 held-out validation，不过就 rollback——离散编辑的高风险用工程闸门兜住，跟神经网络 weight decay 不一样，这里 rollback 是硬开关。

Refinement 与 induction 的分工像 git 里的 amend 与 new file：前者修措辞、补前置条件、改 tool 列表；后者在 residual credit 说「现有 Skill 覆盖不了」时新建目录。Consolidation 解决多 Agent 各自 induct 出语义重复的「搜论文 Skill」——合并后 team 共享一份 canonical 版本，避免库膨胀。Pruning 则清掉 **长期负 credit 且 validation 证明有害** 的 Skill，比「很久没用到就删」更稳。

HotpotQA、LoCoMo、GAIA 上相对 self-reflection memory 与 TextGrad 式全局 prompt 改写都有提升；代码开源在 github.com/DaRL-GenAI/MASkills。三类任务覆盖检索问答、长对话记忆与开放 agentic 工具链——说明 Skill-space 优化不是只会改「写报告 prompt」，而是能跟着任务形态走。

Interaction topology 也会变 credit 怎么传：中心化 Planner 下发子任务时，Planner 的分解 Skill 先被 invoke，Researcher 的搜索 Skill 后手接棒——Critic 的 hierarchical aggregation 要按拓扑合并，否则 Planner 永远背锅。论文把 LangMARL 的 explicit credit 进一步推进到 **skill invocation 粒度**，这是多 Agent  continual learning 里此前缺的一格。Peer-to-peer 拓扑下 credit 传播更 diffuse——MASkills 用 batch 级 aggregation 压噪声，但极端 decentralized 场景仍是 open question。

## 对照、误区与边界

跟 SkillMAS、Skill-MAS 等同期工作比：SkillMAS 耦合 Utility Learning 与 MAS restructuring——组织拓扑也会动；MASkills 更专注 **decentralized execution + centralized critic**，不改 Agent 拓扑，只 evolve Skill library。跟 BASM（2608.22339）是互补：BASM 解决「检索到了该不该用」，MASkills 解决「跑完了该改哪条 Skill」。若两条线合进同一产品：offline 入库用 BASM 写 boundary，online 用 MASkills 改 procedure——Skill 才既安全又可进化。

误区一：把 Critic 输出当一次性 prompt patch。MASkills 的 credit 要聚合、动量平滑、验证集守门，否则 Skill 库会在几个 batch 内膨胀出互相打架的 duplicate Skill——两条「写 SQL Skill」并存，invoke 时随机命中，比没有库更乱。Consolidation 算子就是为这种 duplicate 准备的。误区二：以为 team success 可以按 invocation 次数平分——没有 counterfactual，Researcher 的 Skill 永远跟 Writer 的 Skill 共担同一句「做得不错」。误区二还有变种：把 **最后一次 invoke 的 Skill** 当成主因——长轨迹里往往是早期 decomposition Skill 设错了搜索空间，晚期 formatting Skill 只是背锅。

误区三：忽略 pruning。只 refine 和 induce 不 consolidate/prune，库会走向 MemSkill 论文里警告的「hard to scale」——MASkills 把四算子绑成闭环，credit 为负且跨 cycle 稳定的 Skill 必须能下线。

Language-space 的「梯度」要读成比喻：没有反向传播，有的是 **自然语言 edit direction 的批次共识**。Momentum smoothing 跨 cycle 相当于 optimizer 里的动量项——防止某一批坏 rollout 把整条「写 SQL 查询 Skill」删光。Held-out validation 则是 early stopping：train 集上 credit 再高，dev 集 team success 掉了就 rollback。这套闸门不性感，却是 discrete Skill 编辑能上线的前提。

还没证实的外推：实验 harness 与 Agent 拓扑有限；Critic 本身也是 LLM，credit 质量上限未单独 ablate；与 RL 参数更新混用的 Pareto 未测。Centralized critic 在超大规模团队上的开销也未讨论。HotpotQA 偏检索、LoCoMo 偏长记忆、GAIA 偏工具链——三 benchmark 覆盖不同 failure mode，但都不含 **实时多用户生产流量**；MASkills 的 rollback 在论文里是 offline batch，上在线 serving 还要补 latency 与版本切换策略。

若你已经在用 Cursor Skills 或 Claude SKILL.md：MASkills 给的启发不是「再雇一个 Critic 模型」，而是 **日志里必须能还原 skill trace**——没有「这一步加载了哪条 Skill」的结构化记录，事后反思只能写散文，无法做 credit assignment。

读者该带走的一句：**多 Agent 自进化若停在「改 prompt、堆 memory」，改不到协作里真正被调用的 Skill；MASkills 把 learning signal 对齐到 skill trace 这一层，Skill 库才像 policy 一样可迭代——而迭代的前提是知道「该改哪一条」。** 参数 frozen 的 frontier 时代，团队级改进 increasingly 发生在 Skill 目录的 git diff 里，不在微调脚本里。论文收进 EMNLP 2026 Findings，与 BASM 同年——Skill 作为 Agent 一等公民，研究侧与实践侧正在对齐同一套 vocabulary：trace、credit、boundary、rollback。

把 credit assignment 落到一条具体 trace：HotpotQA 三人组——Planner invoke `decompose-question` Skill，Researcher invoke `search-academic` Skill，Writer invoke `format-citation` Skill；团队答案错因是检索源偏博客。Episode 反思写「Researcher 搜得不好」停住——MASkills 的 Critic 对 **每一次 invocation** 做 counterfactual：「若第 3 步未调用 `search-academic`、改调 `search-news` 会怎样？」输出「site: 过滤器在本任务多余，应特化为 `.edu` 域」→ **refinement** 改 SKILL.md，held-out 不过则 rollback。Writer 的 formatting Skill 若全程正 credit，不会被 team failure 连坐——这是 multi-agent 版 credit 与单 Agent EvoSkill 的分水岭。与 Warp improver 读 GitHub feedback 比：Warp 改 base Skill 靠人类 PR 合入；MASkills 改 Skill 靠 **Critic 结构化 credit + validation gate**——前者 signal 质量高但慢，后者可 batch 但噪声大，momentum smoothing 是为压 Critic 批次矛盾。

四算子闭环里 **consolidation** 常被忽略：三个 Agent 各自 induct 出语义重复的「搜论文 Skill」，invoke 时随机命中，比没有库更乱——credit 为负且跨 cycle 稳定的 Skill 走 **pruning**。Centralized critic 开销随 Agent 数涨，但相对「每个 Agent 各写各的 memory 散文」仍更可 audit：日志里必须有 skill trace，否则 Critic 只能写团队级废话。与 BASM 叠用：入库带 boundary 四字段，online 用 MASkills 改 procedure——读与写各管一层。

---
**参考** [MASkills: Continual Skills Optimization for Multi-Agent LLM Systems](https://arxiv.org/abs/2609.02094)
