# Anthropic 长程 harness：Planner / Generator / Evaluator 拆开，防过早喊完工

**一句话**：长任务常见翻车是 over-ambition 和 premature victory；用 **artifact 文件交接** + 三角色 harness，状态不靠聊天记忆。

日期：2026-09-06

---

## 这是个啥

跑几小时改项目时：

1. **over-ambition**：一口吃太大，context 撑爆  
2. **premature victory**：下一会话以为都做完了，其实漏一堆  

[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 用文件化进度 + 多角色解决。

## 三角色

| 角色 | 干什么 |
|---|---|
| **Planner** | 一两句话需求 → 可执行 spec / 清单 |
| **Generator** | 每次只啃一小块，更新 progress artifact |
| **Evaluator** | 专门质疑「真的完成了吗」，打回自嗨式完工 |

首轮还有 **initializer**：建环境、功能列表、进度文件，给后续会话当交接棒。

## harness 要点

跨会话靠 **artifact**，不靠「模型还记得上次聊了啥」。  
模型升级后，为 context anxiety 写的强制 reset 可能反而拖后腿——**harness 假设会贬值**，接口要能换。

## 链接

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Managed Agents（同系列）](https://www.anthropic.com/engineering/managed-agents)

## 没核实清楚的

- 三角色是否已全部产品化进 Managed Agents，以 docs 为准。  
- 「一块」多大随模型变，无固定参数。
