# 新词候选账本（未晋升，不参与主检索）

每日**探索通道**扫到的新叫法先记在这里，不要直接写进 [keywords.md](keywords.md)。
主检索仍然只用 keywords；本表是自我进化的记忆，避免「只在旧词附近打转」。

来源权重：论文预印本 / 会议论文 ＞ 官方研究或产品博客 ＞ 严肃资讯 ＞ 新仓库 README / 视频 ＞ 招聘 JD（滞后，只印证）。

## 晋升阈值（满足任一且能写清与旧 id 的差）

1. **14 天内 ≥ 3 个独立一手来源**，且其中至少 **2 个来自论文或资讯**（不同作者/机构；转载算同一个）
2. **连续 ≥ 3 个跑次**都出现，且每次至少 2 个来源，其中至少 1 个不是招聘页
3. **禁止**：仅因「≥ 2 家公司 JD 写了这个词」就晋升。JD 出现只给 `sources` +1，并在 note 标 `lagging:jd`

还要同时满足：能用 2 句中文说出它和已有 `id` 的差别。说不清 → 只当旧 id 的 alias 候选，不新开 id。

产品名（dsh、hermes）进 keywords 的「产品与赛道」aliases，不进概念层。

## 行格式

```text
- token: <原文>
  en:
  zh:
  first: YYYY-MM-DD
  last: YYYY-MM-DD
  days: <出现过的跑次天数>
  sources: <累计独立来源数>
  urls:
    - 
  kinds: <paper|news|repo|video|jd，可多个>
  near: <最像的旧 id，没有写 unknown>
  status: watching | promoted | rejected
  note:
```

`status: promoted` 后把完整对照行写入 keywords，本行留档不删。
`rejected` 写明原因（广告词、公司内部黑话、与旧 id 同义）。

## 在观察

- token: TIGPO
  en: Temporal Instance-Graph Policy Optimization
  zh: 跨更新实例图策略优化
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.03383
  kinds: paper
  near: agent-training
  status: watching
  note: 与 GraphGPO 的差是图跨 policy update 保留，历史转移不进当前 loss。仅 1 篇预印本，不晋升。

- token: PGPO
  en: Potential-Guided Policy Optimization
  zh: 势函数引导的策略优化
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://arxiv.org/abs/2609.02236
  kinds: paper
  near: agent-training
  status: watching
  note: 用组内状态势差给失败轨迹内部打步级分。仅 1 篇，不晋升。

- token: credit assignment
  en: credit assignment
  zh: 信用分配
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://arxiv.org/abs/2609.03383
    - https://arxiv.org/abs/2609.02236
  kinds: paper
  near: agent-training
  status: watching
  note: 长程稀疏奖励下给中间步打分。可能只是训练术语，先观察是否稳定出现在资讯标题。

- token: SWE-rebench
  en: SWE-rebench
  zh: 持续更新的去污染 SWE 评测
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://swe-rebench.com/about
    - https://proceedings.neurips.cc/paper_files/paper/2025/file/21bec6ace947b1b58967b945c8ac0f10-Paper-Datasets_and_Benchmarks_Track.pdf
  kinds: paper,news
  near: agent-eval
  status: watching
  note: 产品/数据集名，不是新概念。与 agent-eval 的差是「按时间切分标记污染 + 持续挖题」。暂不新开 id。

- token: OpenSandbox
  en: OpenSandbox
  zh: 阿里开源沙盒平台
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://github.com/alibaba/OpenSandbox
    - https://github.com/opensandbox-group/OpenSandbox/releases/tag/server%2Fv0.2.3
  kinds: repo
  near: sandbox
  status: watching
  note: 产品名。证实后可写入 sandbox 或单独产品 aliases，不新开概念 id。

- token: kubernetes-sigs/agent-sandbox
  en: agent-sandbox
  zh: Kubernetes SIG 智能体沙盒 CR
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://github.com/alibaba/OpenSandbox/blob/main/oseps/0002-kubernetes-sigs-agent-sandbox-support.md
  kinds: repo
  near: sandbox
  status: watching
  note: 集群原语，不是新概念。待官方 SIG 仓库与资讯同时出现再考虑 alias。

- token: agentskills.io
  en: agentskills.io
  zh: Agent Skill 开放格式
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 1
  urls:
    - https://github.com/NousResearch/hermes-agent
  kinds: repo
  near: skills
  status: watching
  note: Hermes README 声称兼容。需官方站点或第二篇资讯才能当 skills 的稳定 alias。

- token: Cordis
  en: Cordis
  zh: dsh 的插件内核
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://github.com/deepseek-ai/deepseek-harness
    - https://deepseekdocs.com/en/docs/learn/intro/what-is-dsh
  kinds: repo
  near: harness
  status: watching
  note: 框架名，绑在 DeepSeek Harness 上。不新开 id。

- token: LLM Wiki
  en: LLM Wiki
  zh: 由模型维护的交叉引用笔记库
  first: 2026-09-06
  last: 2026-09-06
  days: 1
  sources: 2
  urls:
    - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
    - https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-llm-wiki
  kinds: repo
  near: context-management
  status: watching
  note: 模式名，不是协议。与 context-management 的差是「编译后的可 diff 页面 + schema」，先观察。

## 已晋升

_暂无_

## 已拒绝

_暂无_
