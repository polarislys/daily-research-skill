# TIGPO / PGPO：长链路 Agent 训练的 credit assignment 两条新路

**一句话**：只有终局奖励时，中间步分不清功过——这是 **credit assignment** 难题；TIGPO 用图跨 update 保留结构，PGPO 用势函数给失败轨迹内部打分。

日期：2026-09-06

---

## 问题

Agent 多步决策（搜网页、点工具、写代码），往往 **最后才知道成败**。  
RL 训练时若整段 trajectory 同一个 return，好步坏步一起挨打。

人工逐步标 **process reward** 太贵，还容易 **reward hacking**。

## TIGPO

把 trajectory 看成 **图**（节点=状态，边=动作）。  
**TIGPO**（Temporal Instance-Graph Policy Optimization）让图结构 **跨 policy update 保留**，用图关系给中间步算贡献，而不是每轮训练完扔掉历史转移。

- [arXiv:2609.03383](https://arxiv.org/abs/2609.03383)

## PGPO

同一批失败 trajectory 里，有的「差一点就对」。  
**PGPO**（Potential-Guided Policy Optimization）用组内 **势函数**（potential）估计「离成功还有多远」，给失败轨迹 **内部** 步级拉开差距。

- [arXiv:2609.02236](https://arxiv.org/abs/2609.02236)

## 读的时候注意

都是预印本，主要在论文环境验证；和 **GRPO**、**iStar** 等可叠在不同层（算法 / 信用分配），本文没跑 head-to-head。

## 链接

- [TIGPO](https://arxiv.org/abs/2609.03383) · [PGPO](https://arxiv.org/abs/2609.02236)
- [Awesome Credit Assignment in LLM RL](https://github.com/xxzcc/Awesome-Credit-Assignment-in-LLM-RL)

## 没核实清楚的

- arXiv 编号以页面为准。
