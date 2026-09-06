# Anthropic 长程 harness 用 planner / generator / evaluator 对抗「过早宣布完成」

形态：产品剖析  
大主题：Anthropic-Harness  
日期：2026-09-06（Asia/Shanghai）  
问题点：跨多会话的长任务，上下文怎么交接？谁负责怀疑「已经做完了」？

## 先说清楚

Anthropic 在 [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025-11）定义长程 agent 的两类典型失败：**过度雄心**（一次吞整个项目，上下文中途耗尽）和 **过早胜利**（后续会话误以为已完成）。.harness 的应对不是单纯加长上下文，而是用 **结构化工件** 在会话之间交接，并用 **多角色** 分工。

后续工程文（如 long-running application development 系列）把环收成 **planner → generator → evaluator**：planner 把一两句需求扩成可执行规格；generator 按块实现；evaluator 对输出持怀疑态度，减少自吹式「做完了」。本文只拆 **角色拆分 + 工件交接** 两点。

**Harness** 在此指包在模型外的循环与工件，不是 chatbot 皮肤；**skill** 若出现，指可 diff 的程序性知识文件，与自动记忆不同。

## 问题只圈这些

1. initializer / 功能列表 / 进度 artifact 各解决哪类断档？  
2. evaluator 针对的是哪种「假完成」？

## 它由什么构成

**Initializer agent（首轮）**：建立环境、写功能清单、铺进度文件（如 `claude-progress` 类 artifact）。解决「新会话零记忆」——没有工件，模型只能猜历史。

**Coding agent（后续轮）**：每次只啃清单上的一小块，更新进度文件再退出。解决 **over-ambition**；块大小随模型能力调整（官方后续笔记：Opus 4.5 → 4.6 后块可更大）。

**Planner（扩展环）**：把用户 1–4 句 prompt 扩成完整产品规格，免去人手写长篇 spec  upfront。

**Generator**：按规格与清单实现；依赖 **结构化 artifact** 而非聊天摘要传递状态。

**Evaluator**：专门质疑「是否真的完成 / 质量是否达标」，对抗 **premature victory** 与 generator 自评偏乐观。和 Warp 式「人类 PR 评论」不同，这里是 **环内角色**；仍可与人审叠加。

**上下文策略演进。** 早期 harness 为 Sonnet 4.5 使用 **context resets** 缓解 context anxiety；换 Opus 4.5 后该行为减轻，reset 可移除，改用 **compaction** 处理增长。机制教训：**harness 假设会随模型贬值**，应写在可替换层。

## 理念怎么落进机制

主线：**状态写在文件里，怀疑写在独立角色里。**

长程软件工程实践里，Anthropic 把「分解里程碑 + 每步跑测试 / lint / 类型检查 / 构建」写成硬环：失败则不得宣称阶段完成。这与 OpenAI Codex 长程文提到的四类 markdown + 验证环同构，但 Anthropic 更强调 **多 agent 人格** 而非单一 agent 自律。

可复查一点：**跨会话连续性靠 artifact，不靠「模型记得上次聊了啥」。**

## 证据

- 官方博客：
  - [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025-11-26；initializer、coding agent、功能列表）
  - [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)（与长程 harness 同系列）
- 二手年表与综述：
  - [Qiita AI/LLM 年表 2026.06](https://qiita.com/yokoto/items/e110fea5892c56946826)（planner/generator/evaluator 与减价实例）
  - [Zenn: harness は消えない、ただ移動する](https://zenn.dev/hongbod/articles/7852387b0a367c)

## 未证实

- planner/generator/evaluator 三体是否已全部产品化进 Managed Agents，需以当前 docs 为准。  
- Scribd 等平台转载的 PDF 可能与官方博文有排版差异，机制以 anthropic.com 为准。  
- 具体块大小、compaction 触发阈值未公开到可复现参数。
