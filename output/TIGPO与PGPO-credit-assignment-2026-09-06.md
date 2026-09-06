---
形态: 新方法
主题: 信用分配
日期: 2026-09-06
---

# 长程 Agent 的信用分配，正在从「这一批 rollout」走向「跨更新记忆」与「失败轨迹内部分」

这篇把两篇 2026 年 9 月预印本放在同一张图里读：**TIGPO**（Temporal Instance-Graph Policy Optimization）解决 graph 信用 **跨 policy update 断裂**；**PGPO**（Potential-Guided Policy Optimization）解决 **失败轨迹里好步坏步被一视同仁**。二者都挂在 ALFWorld、WebShop 等多轮 agent benchmark 上，和 GRPO、GiGPO、GraphGPO 同赛道——但改的是 credit assignment 的不同一刀。均仅一篇 arXiv，代码待释，下文机制来自论文一手描述。

## 旧路为什么不够

多轮 LLM agent 的 reward 往往 **稀疏、延迟**：整局结束才知道成败。GRPO 用同 task 下 K 条 rollout 的组内相对优势 \(\hat{A}^{\mathrm{ep}}_i = \mathrm{Norm}(R_i; \mathcal{Z}_x)\)，免 critic，但 **一条轨迹里所有 step 共享同一 episode advantage**——中间哪步做对了，信号粗，长 horizon 方差大。

GiGPO 引入 episode-level 与 **anchor-state-level** 分组；GraphGPO 把 **当前 batch** 转移合成有向图 \(G_x\)，用 successor 到成功节点最短距离 \(d_G(s_{i,t+1}, g_x)\) 得 graph return，再与 episode advantage 加权混合 \(\hat{A}_{i,t} = \lambda_{\mathrm{step}}\hat{A}^G_{i,t} + \lambda_{\mathrm{ep}}\hat{A}^{\mathrm{ep}}_i\)。这在「同一 update、同一 batch」内明显更细。但 GraphGPO 的图 **每轮 policy update 重建、用完即弃**：早期 policy 探到的好 prefix，和后期 policy 从重叠状态接上的 suffix，若落在不同 update，batch-local 图 **连不起来**——小 batch 时图覆盖稀疏，relative advantage 还对单条成败过敏。

另一条线是 **replay 历史轨迹** 进 policy loss——会带进 stale action 与旧 log-prob，off-policy mismatch，常需 correction。TIGPO 的核心问题：**能否用历史结构改当前 rollout 的 credit，却不 replay 历史轨迹进 loss？**

PGPO 则盯另一个洞：GiGPO 等 step-level 方法仍 **依赖每条轨迹自己的终局结果**。失败轨迹里，有效 prefix 与致命错误 **常拿到同样的负 advantage**——组内归一化救不了「失败内部的排序」；成功轨迹里的步也被 episode 级信号平均涂抹。

## TIGPO：跨更新的 instance graph

TIGPO 给每个任务 stable identity \(\kappa(x)\)（同目标、同初始环境配置），维护 **persistent graph** \(\mathcal{H}_x^{(k-1)}\)。当前 update 图 \(G_x^{(k)}\) 与历史 **并集** \(\overline{G}_x^{(k)} = \mathcal{H}_x^{(k-1)} \cup G_x^{(k)}\)，在 temporal graph 上重算距离，得 **temporal graph advantage** \(\widehat{A}^{\mathrm{TG}}_{i,t}\)。更新后把新观测边写入 \(\mathcal{H}_x^{(k)}\)。历史边只参与 **连通与距离**；**梯度只打在 fresh current-policy 轨迹上**——与 TIGPO related work 里 critic-free group RL 的 on-policy 约束一致。

光有图不够——独立采样可能很久不再碰到同一任务。TIGPO 把固定 budget \(N=BK\) 切成 **Exploration**（正常抽新 task group）与 **Revisit**（延迟后用 **当前 policy** 重试旧 task，不增总 budget）。Revisit 时把 **当前组 outcome** 与 **早前 Exploration 组的 detached score** 拼成 enlarged reference，算 **cross-temporal episode advantage**——同一任务上比「以前 vs 现在」，稳定小 K 下的相对估计；**只给 Revisit 轨迹梯度**，旧分数是 reference statistic，不进 loss replay。

直观例子：早期 rollout 找到去厨房的好 prefix 但没拿到物体；后期 rollout 从重叠状态成功通关——temporal graph 把两段连成完整成功路径，当前失败步的 graph credit 会因 **更短后继距离** 变亮。Revisit 保证 **当前 policy** 再探同一 \(\kappa(x)\)，否则 graph 只是冷存储。Cross-temporal episode advantage 则回答「同一任务上，我现在是否比第一次探索更好」——这是 **policy improvement 信号**，与 pure graph distance 互补。

GraphGPO 的 step advantage 来自 **同一 source state 的 transition 组内归一化**；TIGPO 换成 temporal graph 上的距离，归一化仍只针对 **当前 policy 产生的边**，历史边不参与梯度——论文反复强调 **detached statistical references**，这是与 experience replay 的法定分界线。PGPO 不用图，而在 anchor state 上估计 \(\hat{\Phi}(s)\)，势差给出 **局部 progress 感**，对 **失败轨迹内部** 尤其敏感：同一组里一条全败、一条晚败，前缀共享状态的步不应同罪。

## PGPO：势函数在组内传播步级 credit

PGPO 仍 critic-free、不持久化图。在每个 rollout group 内，对 **anchor state** 聚合组内 return 统计，估计 **empirical state potential** \(\hat{\Phi}(s)\)。相邻状态的 **势差** \(\hat{A}^{\mathrm{PG}}_{i,t} \propto \hat{\Phi}(s_{i,t+1}) - \hat{\Phi}(s_{i,t})\) 构成 action advantage，使 credit **跨轨迹传播**——当失败轨迹 A 与成功轨迹 B 在相近状态分叉，B 拉高该状态势，A 里 **走到该状态之前的步** 可获相对更正信号，与 B 里 **之后走错** 的步区分开。

与 TIGPO 对照：PGPO **零额外 rollout schedule**，训练开销论文称 negligible；擅长 **失败侧细粒度**。TIGPO 擅长 **跨训练阶段拼路径、小 batch 稳定**；PGPO 擅长 **同 batch 内失败轨迹内部区分**。是否 stacking 未系统测。

与 GraphGPO：GraphGPO 用 **几何距离到 goal**；PGPO 用 **组内势差**——都不学 neural critic，但 inductive bias 不同。GraphGPO 批内；TIGPO 批间+图；PGPO 批内+跨轨迹势。

## 还不能信什么

两篇都是 **单篇预印本**（TIGPO: arXiv:2609.03383；PGPO: arXiv:2609.02236），环境是 **ALFWorld / WebShop** 可验证模拟；与 open-ended 语言 observation **分布差大**。TIGPO 假设 **状态可 merge**——文本态噪声高时 persistent graph 可能 **错误连边、污染 credit**。PGPO 的 anchor-state 在对话 agent 里能否复现 GiGPO 前提未知。超参 \(\lambda_{\mathrm{step}}\)、Revisit 比例、graph discount \(\gamma\) 敏感性需复现。GraphGPO 原文的 batch-local 图已比 GRPO 吃 **更多 rollout 才能连通**；TIGPO 把存储成本换成 **跨 step 的 graph 索引**，工程上要估 **任务 cardinality**——百万 ticket 训练是否可行，论文未讨论。

读 credit assignment 文献时有个实用启发：**先问你的 verifier 在哪一层**——环境终局、组内相对、图距离、势差、偏好 RM。TIGPO/PGPO 假设 verifier 主要是 **稀疏终局 reward**；若你已有 CI 逐步信号（单测通过），可能不必上复杂 RL，harness 层 densify 更便宜。RL 论文解决的是 **只有终局 0/1 时怎么训 policy**，别误用到 **已有 process signal** 的场景。

训练环上，TIGPO 与 PGPO 都仍采样 current policy rollout、仍用 group-relative 归一化——**改的是 advantage 估计器，不是环境接口**。这意味着它们可以接在同一套 SWE-agent 或 web-agent 框架里，替换 GRPO 的 \(\hat{A}_{i,t}\) 即可；真正贵的是 **状态抽象**：ALFWorld 的状态是模拟器对象，WebShop 是结构化 observation；换成纯 HTML 字符串，graph merge 与 anchor state 是否还有意义，论文没有答案。

与 **iStar 隐式 PRM** 对照：TIGPO/PGPO 不训额外 reward model，inductive bias 在 **图拓扑** 或 **组内势**；iStar 用 trajectory DPO 学 \(\pi_\phi\)，更依赖 outcome verifier 排序质量。三者可视为 credit assignment 的三条轴——**结构记忆（TIGPO）**、**组内势传播（PGPO）**、**偏好学 reward（iStar）**——尚未见系统 ablation 谁对谁错，很可能 **环境可验证度** 决定哪条轴 dominant。

工程上若你已在用 GRPO 训 tool agent，优先试 **PGPO** 成本低（无 graph store）；若任务 **重复率高、同一 ticket 多轮尝试**（修同一 SWE issue），TIGPO 的 Revisit + persistent graph 叙事更贴；若你有强测试 harness 产 outcome 排序，iStar 路径更自然。预印本阶段 **不要期待 plug-and-play 库**，应先复现 ALFWorld 曲线再谈迁移。

GiGPO 的 anchor group 要求 **同一环境状态可重复访问**；GraphGPO 要求 **batch 内能拼出连通图**；TIGPO 再加 **跨 update 索引同一 \(\kappa(x)\)**；PGPO 用 **组内势** 绕开 state 字面重复，但对 anchor 选择仍敏感。四条线共同说明：**agent RL 的瓶颈 increasingly 是 credit 几何**，不是 sample 数 alone。失败轨迹在 SWE-agent 里极常见——若只用 episode return，等于告诉模型「这 fifty steps 全错」；PGPO/iStar 类方法的价值 proposition 正在于此，而非刷榜 ALFWorld  alone。

## TIGPO 与 PGPO 如何选一

若 rollout budget 固定、任务会 **反复出现同一 instance**（同一 ALFWorld 关卡、同一购物 query），TIGPO 的 persistent graph + Revisit 是在 **不增 sample 的前提下增信息**；若 batch 内常有 **成功/失败分叉** 但很少 revisit 同一 task，PGPO 的势差更轻。二者都不需要 neural critic，GPU 主要仍花在 rollout generation——适合已有 GRPO 栈、只想换 advantage 估计器的 lab。合并 TIGPO graph advantage 与 PGPO potential advantage 是否稳定，论文未做，理论上 **一个管跨时间结构、一个管组内失败排序**，噪声来源不同，值得当作 ablation 课题而非默认配方。

Implementation sketch：TIGPO 需要 **per-task graph store** 与 Revisit scheduler——工程上像给 RL 训练加一个小型 episodic memory；PGPO 只需在 advantage 计算阶段多几行 **anchor 聚合**，更接近 drop-in。选哪条，先看 **任务是否 repeat、状态是否可 hash**；再看 **团队能否维护 graph 一致性**。预印本没有开源实现时，复现顺序建议 **PGPO → GraphGPO baseline → TIGPO**，逐步加组件，避免一次堆满无法 ablate。ALFWorld/WebShop 上的 gain 可能部分来自 **benchmark 本身 repeat instance**——迁移到 unique ticket 宇宙时，TIGPO 优势未必线性外推。PGPO 在 **失败组内** 的 lift 同样依赖 anchor 能否对齐；open-ended 文本 agent 上二者都可能退化回 GRPO，这是读 paper 时应有的默认预期。

我的判断：**credit assignment 下一波竞争点，从「图内最短路径」进到「图何时跨 update 保留」和「失败轨迹里谁该少背锅」**——TIGPO 用 detached 历史 + Revisit 答前者，PGPO 用势差答后者；落地还取决于状态抽象与 verifier 质量，不是换 loss 就能端到端上生产 web agent。

ALFWorld 直觉例子：第 1 次 rollout 学会「去厨房拿苹果」但没完成任务；第 5 次 update 从重叠状态成功通关——GraphGPO 的 batch-local 图连不起第 1 次 prefix 与第 5 次 suffix，TIGPO 的 persistent graph \(\mathcal{H}_x\) 把两段合成更短后继距离，当前失败步的 graph credit 变亮。Revisit 用 **当前 policy** 再探同一 \(\kappa(x)\)，cross-temporal episode advantage 回答「比第一次探索是否更好」——旧 rollout **不进 loss**，只当 detached reference，与 experience replay 的 off-policy 污染划界。PGPO 则在 **同一 batch** 里：失败轨迹 A 与成功轨迹 B 在「打开冰箱」状态分叉，B 拉高该状态势，A 里走到该状态之前的步获相对更正 signal——适合 **unique ticket 多、instance 不 repeat** 的 SWE 场景。与 iStar 对照：TIGPO/PGPO 不训 PRM，iStar 用 trajectory DPO 学 step reward——三条轴正交，环境可验证度决定哪条 dominant。

复现顺序建议 **PGPO → GraphGPO → TIGPO**：PGPO 最接近 drop-in；TIGPO 要 graph store 与 Revisit scheduler。open-ended 文本 agent 上 state merge 可能错误连边——读 paper 时默认预期可能退化回 GRPO。若 harness 已产 CI 逐步信号，优先 densify 环境再考虑 RL credit 几何——别误用到已有 process signal 的场景。

---
**参考**
- [TIGPO: Temporal Instance-Graph Policy Optimization for Long-Horizon LLM Agents](https://arxiv.org/abs/2609.03383)
- [PGPO: Potential-Guided Policy Optimization for Multi-Turn Agentic Tasks](https://arxiv.org/abs/2609.02236)
