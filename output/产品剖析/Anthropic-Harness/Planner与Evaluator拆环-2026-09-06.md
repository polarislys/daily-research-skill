# 长任务 Agent 容易「以为做完了」——Anthropic 用三个角色拆开

**一句话**：规划写清单 → 干活按小块推进 → 单独一个角色负责挑刺「真的完成了吗」；状态写在文件里，不靠聊天记忆。

日期：2026-09-06

---

## 这是个啥

Agent 跑几小时改项目时，常见两种翻车：

1. **一口吃太大**：上下文撑爆，做到一半断掉  
2. **过早喊完工**：下一会话以为都做完了，其实漏一堆

Anthropic 在 [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 里用 **文件化进度 + 多角色** 来治。

## 三个角色（白话）

| 角色 | 干什么 |
|---|---|
| 规划（Planner） | 把你一两句话需求扩成能执行的清单/规格 |
| 干活（Generator） | 每次只啃清单里一小块，更新进度文件 |
| 验收（Evaluator） | 专门怀疑「是不是自嗨式完成」，质量不过关打回 |

第一轮还会有 **初始化**：建环境、写功能列表、铺进度文件，给后面会话当「交接棒」。

## 关键原则

**跨会话靠文件，不靠「模型还记得上次聊了啥」。**  
模型升级后，以前为了防「上下文焦虑」写的强制清空，可能反而拖后腿——夹具要能换，别焊死。

## 链接

- [长程 Agent 夹具（Anthropic）](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Managed Agents（同系列）](https://www.anthropic.com/engineering/managed-agents)

## 没核实清楚的

- Planner/Generator/Evaluator 是否已全部产品化进 Managed Agents，以当前 docs 为准。
- 具体「一块」多大，会随模型能力变，没有固定数字。
