---
形态: 新方法
主题: Skill记忆
日期: 2026-09-06
---

# Skill 记忆越多越错？BASM 把「何时不该模仿」写进技能里

这篇只答一个问题：给 Agent 塞更多「成功经验」式的 Skill，为什么有时反而更 confidently 地选错工具？arXiv:2608.22339 用 probe 把机制钉死，并给出 Boundary-Aware Skill Memory（BASM）——不是换 RAG 模型，而是换 Skill 的写法与检索后的用法。

## 旧假设为什么会在边界上翻车

Agent 自进化的主流叙事很顺：从成功轨迹里蒸馏 Skill，下次语义相近就检索复用，探索成本下降、成功率单调上升。Voyager、ExpeL 一路走下来，大家默认「检索到了就该用」。论文把这种失败模式命名为 **Skill Imitation Trap（技能模仿陷阱）**：任务看起来跟过去成功很像，但当前状态其实不该走那条工具链。

举个贴近工程的场景：用户说「帮我把这份文件发给同事」——上次成功用的是 Slack 发附件，这次文件在本地且同事邮箱在通讯录里，该走邮件 API。语义检索会把「发文件给同事」的 Slack Skill 顶到前面；模型读到的 procedure 一步步教你怎么调 `slack.files.upload`，却没有任何字段说「收件人只有邮箱、没有 Slack 账号时别走这条链」。于是 Agent 不是不会发文件，而是 **在错误的状态下更自信地选错工具**。

Probe 用 wrong-tool margin 量化这一点：在 BFCL 上，procedure Skill 把 margin 从 7.31 抬到 10.71，相对无记忆基线高出 **47%**。更刺的是：在 inapplicable 状态下，Skill 记忆甚至跑输 memory-free baseline——记忆成了负资产。

Attention 分析给出了因果链条：检索命中时，模型注意力从「该不该用」滑向「上次怎么做的」，procedure 字段被当成**无条件动作模板**。语义相关不等于决策有效，而旧 Skill 几乎只存「怎么做」，不存「什么条件下别做」。这跟人类新手看教程时的毛病一样：步骤背得滚瓜烂熟，前置条件全漏。

论文把决策点分成三个桶，读懂这三个桶就读懂了问题形状。$T_{\mathrm{ok}}$：检索到的 Skill 匹配正确工具，该用。$T_{\mathrm{wrong}}$：语义相近但工具不该用，该 suppress。$T_{\mathrm{repair}}$：局部已失败，该读 recovery 而不是再模仿 procedure。Success-distilled 记忆在 $T_{\mathrm{wrong}}$ 上 worst——越多 Skill，越像「以前都这么干」。这跟 RAG 文献里「相关性不等于可采纳性」同源，但 Agent 场景更毒：工具名往往只差一个词，logit 层面几乎并列，procedure 一推就翻。

## BASM 怎么把环转回来

BASM 的核心不是更聪明的 embedding，而是给每条 Skill 补全 **七槽 schema**：goal、procedure、tools，外加四类 boundary 字段——applicability conditions（适用条件）、risk cues（风险信号）、avoidance rules（回避规则）、recovery notes（失败修复）。Skill 从「成功剧本」变成 **state-conditioned guidance**：条件成立才执行，不成立就 suppress 工具调用，执行偏了走 targeted repair。

整条链路分三层，环是闭合的：

**离线抽取。** 从 logged trajectories 建 boundary-aware skill library。boundary 证据跟 procedure 一起入库，而不是事后贴标签。抽取器要从成功轨迹里同时看到「什么状态触发了这条链」以及「若状态不满足本不该走」——后者往往要从失败邻域或对比轨迹里反推。七槽 schema 不是写给人看的文档模板，而是 **检索、排序、gate、repair 四环节共享的结构化接口**；缺任何一槽，下游就只能退回「procedure 当模板」的旧路。

**检索与格式化。** 在固定 token budget 下 rerank，boundary relevance 参与排序，避免「procedure 相似度最高但 applicability 为零」的 Skill 独占上下文。Prompt 里 selective expose boundary evidence：安全状态下 procedure 可以占主；进入 $T_{\mathrm{wrong}}$ 或 $T_{\mathrm{repair}}$ 桶时，boundary 字段权重上调。这不是简单把 Skill 写长，而是 **按决策风险动态分配注意力预算**。

**决策与运行时。** boundary checker 在 prompt 侧拦截 inapplicable 的工具提议——相当于 harness 里多一道 gate，不全靠模型自觉。Stateful 环境里还有 runtime repair module：局部失败时读 recovery notes，做 targeted 修复而不是从头再模仿一遍 procedure。AgentDojo 上 attack success rate 降 4.6 个百分点，说明 boundary 不只防「用错工具」，还防 **把 Skill 当越狱模板**——攻击者塞进的 procedure 若没有 applicability 校验，同样会被 suppress。

Probe 验证 boundary 真是「反模仿通道」。在适用状态 $T_{\mathrm{ok}}$，boundary 相对 procedure 的 attention ratio 约 0.15；到了 inapplicable 的 $T_{\mathrm{wrong}}$ 升到 1.23；需要修复的 $T_{\mathrm{repair}}$ 峰值 1.81——模型在危险状态下会主动「读说明书里的注意事项」。Knockout boundary-span attention 能恢复 **69.4%** 的 imitation-trap 效应；随机 knock 同样长度的 procedure span 没有同等效果——说明不是 prompt 变长带来的泛化 soften，是 boundary 字段在因果上起作用。Same-length padding 控制组也失败，进一步排除「上下文变长所以变保守」的廉价解释——模型是在读 boundary 语义，不是在数 token。

实验覆盖 BFCL、AppWorld、AgentDojo 与 Qwen 8B 到 397B 四档规模。相对 success-distilled baseline：AppWorld 成功率最高 +23.8%，BFCL overall +5.0%，AgentDojo 攻击成功率降 4.6 个百分点，AppWorld 平均步数还比无记忆基线少 6.6%——suppress 无效模仿的同时，有效复用没丢，Qwen3-14B 上出现 utility 与 safety 的 Pareto 改进。步数下降值得单独记：很多团队怕「加字段会拖慢 Agent」，BASM 说明 **少走错路比少读字更省步数**。

## 对照、误区与还没证实的一点

跟「只加 applicability 段落」的 App. Skill baseline 比：App. Skill 有时能缓解，但在 $k=2$ 检索深度下 wrong-tool margin 仍高于 BASM——说明 boundary 要 **结构化、可检索、可 gate**，一段自由文本 disclaimer 不够。

常见误区：以为「多检索几条成功案例」就能覆盖边界。论文 Figure 2 明确显示 success-distilled 曲线随 $k$ 上升，BASM 则下降——**多给错误模板只会加强错误偏好**。另一个误区是把 recovery notes 写成泛泛「失败了请重试」；有效 recovery 要绑定具体异常状态与替代工具链，否则 repair 模块没有抓手。第三个误区是以为 bigger model 免疫：论文在四档 Qwen 上都观察到 trap——模型越大，procedure 写得越 convincing，边界缺失时 **错得更像对的**。

跟在线 Skill 进化（如 MASkills）的关系：BASM 解决 **读** 的问题——检索到了该不该用；进化框架解决 **写** 的问题——跑完该不该改 Skill。两者可以叠：进化产 Skill 时就应该带 boundary 字段，否则进化越快，imitation trap 越深。若你的 Skill 库只有成功轨迹蒸馏，建议先把 BASM 四字段补进模板，再谈 online refine——顺序反了，等于用自动化加速堆错模板。

论文在 RL 的 options 框架里找先例：initiation set 规定 Skill 何时启动。BASM 做的是 **用自然语言 initiation set 替换符号谓词**，让 LLM 在 tool-use harness 里读得懂、gate 得住。这不是全新范式，是把老问题在新栈里命名清楚——Skill Imitation Trap 这个名字值得进团队 postmortem 词汇表：一见到「加 Skill 后工具调用更离谱」，先查 boundary 有没有写，而不是先换 embedding 模型。

还没完全外推的：实验集中在工具调用与 API 编排 benchmark；对纯对话 Agent、对 Claude/Codex 式 SKILL.md 生态的长程在线表现，论文没系统测。boundary 字段谁写、写多准，论文用离线抽取加人工校验，尚未证明完全自动化抽取在开放域不掉链子。

工程上值得记的一条：你手写 Skill 若只有 procedure 没有「何时不用」，等于人工制造 imitation trap——BASM 相当于把 Pitfalls/Anti-Patterns 升格为与 procedure 并列的一等字段。落地时可以先在 Skill 模板里强制四问：什么状态才用？什么信号说明快越界？哪些工具名相似但必须回避？失败后第一步修什么？答不全的不入库。Skill-RAG 的下一轮竞争，可能不在 embedding 模型，而在 **Skill 作者契约**——procedure 只是技能的一半，另一半是边界。EMNLP 2026 Findings 收录说明社区已开始认真对待「何时不模仿」——这比又多一个 retrieval trick 更值得跟进。

把七槽 schema 写进一个 Slack-vs-Email 例子：`send-file-to-colleague` Skill 的 procedure 教 `slack.files.upload`；**applicability** 写「收件人 Slack workspace 已验证且 file 已在 cloud」；**risk cues** 写「通讯录仅有 email」「文件路径在本地」；**avoidance rules** 写「上述信号出现则 suppress slack 工具，改走 `email.send_attachment`」；**recovery notes** 写「若 slack 404 user_not_found，回退 email 并记录 thread」。检索命中时 rerank 把 applicability 为零的 Skill 降权；boundary checker 在 prompt 侧拦截 inapplicable 提议——AgentDojo 攻击成功率降 4.6 点说明 **procedure 也可被越狱**，boundary gate 同样防恶意 Skill。与 MASkills 叠用：offline 入库走 BASM 四字段，online 跑完用 skill trace credit 做 refinement——「读」与「写」各管一层，进化才不会加速堆错模板。

Knockout 实验值得写进 postmortem：boundary-span attention 被 knock 掉能恢复 69.4% imitation-trap 效应——模型在读 **注意事项语义**，不是上下文变长所以变保守。Figure 2 显示 success-distilled 随检索深度 $k$ 上升、BASM 下降——**多给错误模板只会加强错误偏好**；手写 Skill 若只有 procedure，等于人工制造这条曲线。落地先补 boundary 四字段，再谈 online refine。

---
**参考** [When Not to Imitate: Boundary-Aware Skill Memory for Reliable Tool-Use LLM Agents](https://arxiv.org/abs/2608.22339)
