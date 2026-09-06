# Anthropic 长任务 harness：Planner、Generator、Evaluator 分开，防「以为做完了」

跑几小时改项目，Agent 常见两种翻车：[Anthropic 这篇](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 总结得很清楚——

一是 **over-ambition**，一口吃太大，context 撑爆；二是 **premature victory**，下一会话以为都做完了，其实漏一堆。

解法不是单纯加长上下文，而是 **artifact 文件交接 + 角色拆分**。

## 三个角色在干什么

**Planner** 把你一两句话扩成能执行的 spec / 清单。  
**Generator** 每次只啃一小块，更新 progress 文件再退出。  
**Evaluator** 专门挑刺——是不是自嗨式完工。

第一轮还有 **initializer**：建环境、功能列表、进度文件，给后面会话当交接棒。

核心原则：**跨会话靠文件，不靠「模型还记得上次聊了啥」。** 模型升级后，为 context anxiety 写的强制 reset 可能反而拖后腿——harness 假设会贬值，接口要能换。

这和 OpenAI「repo + CI 当约束」是不同路线，但都在答长任务怎么不破。

---

**参考**

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Managed Agents（同系列）](https://www.anthropic.com/engineering/managed-agents)

三角色是否已全部产品化进 Managed Agents，以当前 docs 为准。
