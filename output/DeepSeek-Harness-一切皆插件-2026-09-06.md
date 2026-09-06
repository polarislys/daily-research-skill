---
形态: 产品剖析
主题: DeepSeek-Harness
日期: 2026-09-06
---

# DeepSeek Harness：一切皆插件，连 AgentLoop 也不例外

这篇只答：`dsh` 和「CLI 包一层 chat API」差在哪，以及 **everything-is-a-plugin** 是营销口号还是可替换的架构接缝。DeepSeek 把完整 agent runtime——session、loop、tool pipeline、sandbox、Web UI——拆成 **Cordis** 插件树；核心只留一个薄 loop 与 **capability seams**。改行为不应改 monolith，而应改 composition 层。

## 痛点：一体成型 runtime，改一处牵全身

多数 coding Agent 把 model adapter、tool registry、session store、permission 焊进单体应用。想换 sandbox 实现、在 tool 前加 approval gate、或试验另一种 agent loop，往往 fork 整仓或侵入 core。DeepSeek Harness（`dsh`）的定位是 **独立进程**：自有 `~/.dsh/` 配置、`~/.dsh/sessions/`、权限与 sandbox 系统，**不是** IDE 补全插件。它要同时服务 `dsh web` 工作台、`dsh --profile headless` 一次性任务、以及 JSON-RPC **SDK**——若 runtime 不可组合，三种入口必然三套重复逻辑。

独立进程意味着 lifecycle 与 IDE 解耦：关 VS Code 不会 kill session；permission 与 sandbox 策略在 harness 层统一 enforce，而非每个 editor extension 各写一套。这对企业 audit 友好——安全团队只需 review Cordis profile 与 plugin 清单，而非追十条 IDE 插件的权限声明。

社区文档专门澄清误解：`/plan` **不会**自动切换模型，只维护规划与协调状态；「plan/execute 隐式路由」并不存在。这一点很重要：行为来自 **profile 叠层**与插件挂载，不是 core 内置魔法。用户以为的「智能」常是 composition 结果，误判会导致错误定制。

## 机制：Cordis、Profile/Bundle 与 capability seams

**Cordis**（`@deepseek-ai/cordis`）是组合框架：插件向共享 **Context（`ctx`）** 贡献 service、typed event、可逆 effect。DeepSeek **vendor fork** Cordis 并纳入自有 scope，.harness 完全拥有 framework 层——上游升级是 merge exercise，换的是对 boot 行为与 event 契约的控制权，而非黑盒依赖。

运行中的 `dsh` 是一棵 **plugin tree**，启动时按序叠层：

1. Profile 所列各 **bundle** 的 patch（如 `base`、`web`、`headless`）
2. Profile 级 `cordis.patch.yml`
3. `$DSH_HOME` 级 patch
4. CLI `--patch` overlay

**Profile** 是命名组合，存于 `$DSH_HOME/profiles/`；**bundle** 是带 patch 的 npm 包，在 `package.json` 的 `dsh.bundle` / `dsh.profile` 声明。`dsh web --dump-config` 可打印整棵 compose 树——**没有 privileged core 行不可 patch**；换 LLM、换 loop、换 UI 都是换配置行或插新行，而非发版改内核。

Major 子系统全是插件，经 **seam** 暴露到 `ctx`：

| ctx 键 | 职责 |
|--------|------|
| `ctx.llm` | 多 provider / model 路由 |
| `ctx.tools` | scoped registry + guarded pipeline |
| `ctx.sessions` | append-only SessionEvent log |
| `ctx.agents` | Agent 注册与 `agent/*` 事件 |
| `ctx.agentLoop` | 默认 loop 实现（**可替换**） |
| `ctx.systemPrompt` | prompt section 与 tool schema 组装 |

README 与架构文反复强调：**new behavior should go into a plugin, not here**——指向 agent-loop 内核的注释。这不是谦虚，是硬约束；内核变薄，生态才厚。`core/scope` 提供 per-agent scoped registration，避免多 agent 并行时 tool 或 state 串线——multi-agent 场景下这是常见 silent bug 源，dsh 在框架层用 scope primitive 处理。

`@deepseek-ai/dsh-agent-loop` 是文档所称**唯一 concrete loop**，源码哲学明确：core 极薄——「调 model、跑 tool、循环」；search、compaction、retry、subagent、UI 渲染都挂 **event hook**：`agent/pre-step`、`tools/pre-execute` → `execute` → `post-execute` → `finalizeContent` → `tools/result`。Persistence 靠 `session/event` eager write-behind；`session/flush` 是观察屏障。扩展者写 plugin 订阅事件，**不应改 loop 内核**——这与 Warp 用 improver PR 改 Skill、Codex 用 rules 与 linter 约束环，是同一时代的三种「外环进化」路径。

`agent/request-error` 是另一个关键 hook：`dsh-llm-retry` 在此做 backoff 与恢复；context 溢出则在 `agent/pre-step` 做 compaction 压力检测。官方文档把 canonical fix 写清楚——**新行为写 plugin**，避免 PR 改 loop 内核被拒。ReactLoopAgent 内核 package-internal，外部只能通过 `ctx.agents` 创建 lifecycle owner——这是刻意的 encapsulation，防止 fork 出不可组合的 loop 变体。

能力面还包括：**MCP** 接外部工具、**Skills** 教流程、Goals/tasks 长程推进、subagent/workflow 并行、`session_search` 查历史 session。`web` bundle 加浏览器 UI；`headless` bundle 加 one-shot runner；`packages/sdk` 供外部进程以 JSON-RPC 驱动同一棵 tree——**composition 一次，入口多种**。

内置 profile 模板（`web`、`headless`、`sdk`、`sdk-minimal`、`acp`）降低默认路径选择成本：`headless` 适合 CI 式「一句话跑完退出」；`web` 适合本地 workbench。用户 overlay 写在 `$DSH_HOME/profiles/<name>/cordis.patch.yml`，不必 fork 官方 bundle——这与 Kubernetes kustomize 式 patch 很像。安装 out-of-tree plugin 后，profile 引用其 bundle 行即可挂载，适合企业内部 secret scanner 或 custom LLM gateway 一类扩展。

## 对照 Codex、Warp 与边界

相对 **Codex harness**：Codex 开源 agent loop + **app-server** 协议，强调 embed、streamed events 与 approval RPC；dsh 强调 **运行时每一层可 patch**，含 loop 本身。相对 **Cursor / Claude Code**：后者是产品化 harness；dsh 是 **可自托管、可 fork 的 composition kit**，更像「Agent 应用的 profile 系统」。

DeepSeek 选择 Hermes 式 **Web workbench**（`dsh web` 默认 127.0.0.1:3080）而非只做 IDE 插件，说明其默认 persona 是「独立工作台」：session、permission、sandbox 由进程统一管理，不依赖编辑器生命周期。这与 Codex CLI 在 terminal 里跑 loop 相似，但 UI 与 composition 模型不同——dsh 用 Cordis 树，Codex 用 config.toml + rules + app-server RPC。二者可并存于同一组织：Codex 嵌产品内嵌场景，dsh 做内部 automation workbench，只要 MCP 与 Skill 格式对齐。

相对 **Warp 双 Skill 进化**：dsh 不把「改进」默认建模为 improver PR 改 SKILL.md，但 Skills 仍是插件能力；BASM 等研究所谈的 boundary-aware skill memory，在 dsh 里更自然落在 `tools/pre-execute` 策略插件或 Skill metadata，而非 monolith 硬编码。

**webhook** 包（`ctx.webhookRuntime`）支持 authenticated delivery 与 workspace session 创建——适合把外部事件（CI fail、PagerDuty）接进 harness，而不只依赖人手敲 CLI。Scheduling 插件做提醒与 cron 式任务，与 Goals/tasks 长程状态配合，构成「工作台不仅是 chat，还是 automation hub」。这些能力分散在各 bundle，读 `--dump-default-config` 比读一篇 marketing 更能看清默认 composition 边界。

边界须如实写：`dsh` 处 **Developer Preview**（社区文档标注）；公开 clone 约 45 万行 TypeScript、219 packages，bundle 叠层学习曲线陡。**Agent loop 可替换不等于零成本替换**——event 契约与 session 语义须对齐。Benchmark 与生产 readiness 公开材料仍薄，企业 adoption 需自行压测 permission、sandbox 与多 agent 并发。

与 **OpenSandbox / Kubernetes agent-sandbox** 一类集群原语比，dsh sandbox 在进程级 profile 内解决，偏单机 workbench；要上 K8s 往往要另写 executor plugin 或外层 orchestrator。与 **Temporal** 的 durable execution 比，dsh session event log 提供 replay 语义，但跨机器 fault tolerance 不是默认承诺——长事务可能要外层 workflow 包 session，这与 Codex harness 的边界问题同构。

判断句：**DeepSeek 赌的是 harness 竞争在 composition，不在单点 model**；一切皆插件，是把「改行为」从改 core 改成改 patch 层——与 OpenAI 把规则 mechanical enforce、Warp 把知识 procedural 化，同属 2026 agent 基础设施的三条可并存路线。

tool pipeline 值得单独拆：`tools/pre-execute` 是 policy gate（deny / ask），`tools.guard()` 包执行，`post-execute` 与 `tools/result` 做善后与内容 finalize。想在 bash 前加公司 DLP、或在写文件前二次确认，不必 fork loop——挂 plugin 即可。subagent 走 `ctx.subagents` 与 `ctx.jobs`，background 与 in-process 两条路径；multi-agent 不是 bolt-on，而是 registry 一等能力。

`llm-pi-ai` 路由层让同一 profile 内混用 DeepSeek、OpenAI、本地模型成为可能——**plan 不切模型**不等于 **不能** 在 profile 层为不同 agent 配不同 adapter 行。误读常来自把「用户命令」与「composition 配置」混为一谈；改路由应 edit patch，而非期待 slash command 魔法。

Session 模型用 append-only **SessionEvent**，turn/step 边界清晰，UI 与 SDK 订阅同一 event stream。`session_search` 让 Agent 查自己历史 session——meta 能力也工具化。与 Codex thread/item 比，语义相近但实现完全 plugin 化；换 storage backend 理论上只需换 `core/session` 行。

社区维护的 deepseekdocs 与官方 GitHub 并用时，以 **`--dump-config` 输出**为准验证文档是否过期——Preview 阶段 API drift 快，静态教程容易 lag。first plugin 教程通常从 duplicate `tool-*` 或 `tools/pre-execute` deny rule 开始，一天内可见效果，比读完 453k LOC 更实际。

Cordis 论文提 **spatial / temporal composability**：空间上多插件共存于 ctx，时间上 patch 层序决定谁覆盖谁。DeepSeek vendor fork 意味着 harness 团队能改 event bus 而不等 upstream——代价是 merge 负担。对想深度定制 sandbox 的团队，这比「配置项调参」自由度大一个量级。

启动路径：`npx @deepseek-ai/dsh web` 零安装入口、`headless` profile 跑完即退，降低试用门槛；真正定制从 `--dump-config` 看清树开始，再写 home-level patch。Skills 与 MCP 与 Warp/Codex 概念互通，但 dsh 默认不包 improver 环——组织若要 Skill 进化，需自建 plugin 或在 Git 侧做 PR 流程，与 Warp 双 Skill 形成互补而非替代：dsh 提供 runtime composition，Warp 提供 org 知识 evolution 范式；二者可在同一 repo 并用 Skills 格式与 Git PR 合入。读 DeepSeek Harness 时，先接受「219 packages 是为 patch 边界付的代价」，再评估团队是否真有 composition 需求；否则 Codex 或托管 Agent 可能是更短路径。everything-is-a-plugin 适合「要_own runtime 边界」的团队。

收束：**dsh 把 Agent runtime 拆成可 patch 的插件树，AgentLoop 都不神圣**；适合要控 composition、愿付学习曲线的团队，不适合只想开箱 chat 的用户。

## 读者可带走的一个判断

评估 agent 框架时，问一个问题：**换 sandbox 或换 loop 要不要改 core？** dsh 的答案是 patch 一行配置；monolith 的答案是发版或 fork。everything-is-a-plugin 不是减少代码量——219 packages 说明相反——而是把变更面从「读遍 core」变成「读 dump-config 树」。若你的组织需要 Hermes 式 Web workbench、headless CI、SDK 三入口统一 runtime，dsh 值得读 Cordis 与 agent-loop 文档；若只需 IDE 内联补全，过重。DeepSeek Preview 阶段，生产落地请自验 permission 与 sandbox；架构思想比成熟度更值得先吸收。

写插件的入口文档强调 **extension points first**：先找 event 与 ctx seam，再写业务逻辑。第一个 plugin 通常是 `tools/pre-execute` 策略或自定义 tool package，而不是改 agent-loop。Python SDK 包一层 JSON-RPC，适合 Jupyter 或 data pipeline 里 spawn harness——与 Codex SDK 定位类似，但 boot 的是 Cordis 树而非 app-server thread。license 与 DeepSeek 模型绑定与否需读当前 README；架构上 model adapter 仍是 seam，不锁死自家模型。

举一个 `tools/pre-execute` 插件如何不改 loop 内核就加公司 DLP：企业 patch 订阅 `tools/pre-execute`，在 `bash` 执行前扫描命令是否含 `curl | sh` 或外传路径；deny 则 Agent 收到结构化错误，session event 记 `policy_blocked`——与 Temporal 的 ToolApprovalPolicy 同哲学，但落在 Cordis event 而非 workflow。若改 monolith，每个 fork 都要 merge 上游 loop 变更；dsh 路径是 **一行 patch 引用新 bundle**。与 Warp improver 改 Skill 对照：Warp 进化 domain 知识文件，dsh 进化 **runtime composition**；二者可并存——improver PR 更新 `SKILL.md`，profile patch 决定哪个 Skill 目录挂载、哪条 pre-execute 规则生效。Preview 阶段应用 `--dump-config` 验证文档未过期，第一个 plugin 一天可见效，比通读 45 万行 TypeScript 现实。

`session/event` eager write-behind 对长任务也关键：worker 崩溃后 UI 与 SDK 仍能从磁盘 event 恢复进度条——与 Managed Agents 的 append-only session 同族。subagent 走 `ctx.subagents` 时 scope primitive 防 tool 串线：Researcher 与 Coder 并行各挂 scoped registry，silent bug 常出在 monolith 里全局 tool 表被并发写坏。dsh 默认不包 Warp 式 improver，组织若要 Skill 进化需自建 plugin 或 Git PR——runtime composition 与 domain knowledge evolution 仍是两条可并存的路。

---
**参考**
- [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- [What Is DSH](https://deepseekdocs.com/en/docs/learn/intro/what-is-dsh)
- [DeepSeek Harness Architecture Reference](https://deepseek-harness.github.io/deepseek-harness/en/reference/)
- [The Agent Main Loop](https://deepseekdocs.com/en/docs/learn/core/agent-loop)
