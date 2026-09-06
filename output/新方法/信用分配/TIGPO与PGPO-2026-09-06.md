# TIGPO 和 PGPO：长链路 Agent 训练里，credit assignment 的两条新路

多步 Agent（搜网页、点 tool、写代码）往往 **最后才知道成败**。RL 训练时若整段 trajectory 同一个 return，好步坏步一起挨打——这是 **credit assignment** 老问题。

人工逐步标 **process reward** 太贵，还容易 **reward hacking**。最近预印本里 TIGPO、PGPO 各走一条路。

## TIGPO：图别每轮训练就扔

[TIGPO](https://arxiv.org/abs/2609.03383)（Temporal Instance-Graph Policy Optimization）把 trajectory 看成 **图**（节点=状态，边=动作），让图结构 **跨 policy update 保留**，用图关系给中间步算贡献，而不是每轮把历史转移全扔掉。

## PGPO：失败轨迹里也有「差一点」

[PGPO](https://arxiv.org/abs/2609.02236)（Potential-Guided Policy Optimization）在同一批失败 trajectory 里，用 **势函数**（potential）估计离成功还有多远，给失败轨迹 **内部** 的步拉开差距——哪步更该背锅，哪步更值得保留。

## 读的时候

都是预印本，主要在论文环境验证。和 **GRPO**、**iStar** 等可以叠在不同层；本文没跑 head-to-head。

---

**参考**

- [TIGPO](https://arxiv.org/abs/2609.03383) · [PGPO](https://arxiv.org/abs/2609.02236)
- [Awesome Credit Assignment in LLM RL](https://github.com/xxzcc/Awesome-Credit-Assignment-in-LLM-RL)
