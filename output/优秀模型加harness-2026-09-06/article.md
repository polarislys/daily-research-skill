# 开源侧已经把「优秀模型 + harness」拆成可替换的产品层

日期：2026-09-06（Asia/Shanghai）  
问题点：为什么同一周里，DeepSeek Harness（dsh）和 Nous Hermes Agent 都被当成「产品」而不是又一个聊天框？岗位该优化模型还是优化环？  
关键词：harness, work-mode-shift, new-harness-product, new-agent-product, skills, skill-evolution

## 结论

过去约一周，开源社区把「套件比单次换更强模型更值钱」写成了可检查的代码，而不是口号。OpenAI 把 Codex 的可复用部分明确叫作 **harness**（执行环）：管上下文、工具、沙盒、审批、跨轮状态；并给出 `codex exec` / SDK / app-server 三层接入。DeepSeek 把同一层做成 **everything-is-a-plugin** 的 `dsh`。Nous 的 **hermes-agent** 则把「会自己写 skill、会跨会话记你」做成产品卖点，9 月 5–6 日再次出现在中文资讯和 GitHub 热榜。

对 AI 应用研发 / Agent 优化岗，这意味着工作模式已经从「追最强模型」挪到「选够用模型 + 自己能改的环」。明天该动手的是 **搭**：把你们现有 agent 拆成「模型适配 / 工具与审批 / 会话与 skill / 沙盒」四条缝，而不是再换一次 API。

## 问题界定

只讨论一件事：harness 作为**可拆产品层**，和「换模型」差在哪，岗位该改哪一层。  
不讨论哪家模型榜单更高，也不把汽车数字座舱项目 OpenDSH 误认成 DeepSeek 的 `dsh`。

## 第一层：对象是什么

**harness（智能体夹具 / 执行环）**：包在模型外面的循环。它决定模型何时读文件、何时跑命令、失败是否重试、写操作要不要人批、上下文何时压缩。它不是 chatbot 皮肤。OpenAI 自己的定义是：理解任务、维持上下文、检查信息、调用工具、暴露进度、处理失败、必要时请求批准、再交回结果。他们在 ARC-AGI-3 上给出可核对数字：保留推理轨迹并做 context compaction 后，GPT-5.6 Sol 从 13.3% 升到 38.3%，输出 token 降到约六分之一。同一套权重，换环，分数会变。

**work-mode-shift（优秀模型 + harness）**：不再默认「上更强的 frontier model」。默认变成：选一个你们评测过、成本可接受的模型，把失败预算花在环上——权限、重试、工具路由、上下文裁剪。

**dsh / DeepSeek Harness**：DeepSeek 于 2026-08-13 开源的开发者预览，仓库 `deepseek-ai/deepseek-harness`，CLI 名就是 `dsh`。设计原则是一切皆插件：模型、工具、skill、会话、沙盒、存储、循环、调度、UI 都是 Cordis 插件，用 profile 组合，不改核心源码。它和 Unix 老命令 `dsh`（distributed shell）、汽车座舱 OpenDSH **不是同一个东西**。

**hermes-agent**：Nous Research 的自进化 agent 产品，仓库 `NousResearch/hermes-agent`。卖点不是「又一个 Claude Code 克隆」，而是内置学习环：任务后自动写 skill、使用中改 skill、FTS5 搜旧会话、兼容 [agentskills.io](https://agentskills.io)。终端后端宣称有本地 / Docker / SSH / Singularity / Modal / Daytona / Vercel Sandbox。中文站 2026-09-06 把它当作「开源发布」再传播；更准确的说法是：仓库 2025-07 已建，本周热度再次起来。

**loop engineer（循环工程师）**：优化的是「模型 → 行动 → 观察 → 再进入」，不是单次 prompt。同一条失败若反复出现在「工具返回太大」或「审批被跳过」，改的是环上的门闩，不是再写一句 system prompt。

**skill 与 skill-rag**：skill 是可版本化的说明书 + 可选脚本（常见形态是 `SKILL.md`）。skill-rag 是用检索**选中或填空** skill，而不是把二十个文件一次性塞进窗口。Hermes 兼容 agentskills.io，说明 skill 开始按文件格式流通；你们若仍把全部 skill 平铺进系统提示，窗口会被过期说明书占满，环看起来「模型变笨」，其实是上下文被自己污染。

**skill 自进化**：skill 根据失败轨迹改自己的说明书或脚本，必须有写入路径和人审，不是模型「自己变聪明」。Hermes 把它做成默认行为；你们若没有评审，这只是往仓库里堆不可复现的 markdown。Karpathy 的 LLM Wiki 把「规范文件」和「编译后的笔记」分开，Hermes 把它收成 bundled skill：人负责供料和提问，模型负责交叉引用。这能解释为什么「记忆产品」最近都在往**可 diff 的文件**靠，而不是只做向量库。

过去 24 小时里具体出现了什么：中文资讯把 hermes-agent 推上「今日发布」叙事；GitHub 上 `hermes-agent` 与 `deepseek-harness` 仍是高星公开仓库；OpenAI 开发者博文把 Codex 定位成「open agent harness 平台」，数字和三层接入写在原文里。dsh 官方仓库可打开，社区文档补充了「独立进程、`~/.dsh/` 会话、权限与沙盒」的运行形态——这已经是 runtime，不只是 prompt 模板。

## 第二层：机制与岗位含义

主线是工作模式，不是再比一家 CLI。

三家把同一层切成不同缝，方便你对号入座：

| 缝 | Codex | dsh | Hermes |
|---|---|---|---|
| 环怎么暴露 | exec / SDK / app-server（JSON-RPC） | Cordis 插件 + profile | TUI + 消息网关 + cron |
| 模型 | 权重仍收费，harness 开源 | 可换，预览期接口会破 | OpenRouter / 自建端点可切 |
| 写操作 | sandbox + approval | 权限与沙盒也是插件 | 命令审批、DM 配对 |
| skill | 仓库侧 Skills/Plugins | 插件包 | 从经验创建、使用中改 |

工程含义：你们内部 agent 若还是「一个 prompt + 一堆 tool schema」，换模型只会把同样的权限事故换一家供应商重放。环上的失败通常是：工具一次返回太大、没有审批、沙盒与宿主机共享家目录、skill 平铺进系统提示却从不按失败改。Codex 用 app-server 把「创建线程 / 开一轮 / 收事件 / 回审批」收成协议，等于承认这些状态机不该每个产品重写。dsh 用插件缝承认「循环本身也可以被替换」。Hermes 用网关 + cron 承认「环要活过一次聊天窗口」。三家吵的不是聊天皮肤，是状态机归谁。

落地时还有一个容易混的层：**产品 UI** 和 **harness**。OpenAI 的 Relay 示例把货运看板、业务 MCP、写操作审批留在应用里，环只负责转和跑。你们若把业务规则写进超长 system prompt，以后换 harness 厂商等于重做项目。正确切法是：应用拥有队列、记录、权限矩阵；harness 拥有重试、工具调度、沙盒策略。

**明天能做的一个动作**：打开你们现网 agent 的一次失败轨迹，只改环、不换模型。用一张表写下：这次失败卡在「上下文爆了 / 工具选错 / 没人审批 / 沙盒不够 / skill 过期」哪一格。然后选最小补丁——例如给写文件加审批，或把 8 个 skill 改成按任务检索 2 个。不要同时改模型和环，否则分不清是谁赢的。补丁合并前，把同一条任务再跑 3 次，看失败是否从同一格消失；这就是最小回归，不必先上完整 eval 平台。

若你们在看 dsh：先跑官方仓库的 web/headless profile，看 profile / 插件清单里哪些是可替换缝，对照自己的硬编码。若看 Hermes：只验证「skill 写入 + 评审」有没有，不要被星数带跑。若看 Codex：先读 app-server 能管哪些事件，再决定要不要把业务 UI 接到环上，而不是再做一个聊天窗。

## 证据（24h）

- 仓库：
  - [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（自进化 agent，兼容 agentskills.io）
  - [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)（Everything is a Plugin，CLI 名 dsh）
  - [openai/codex](https://github.com/openai/codex) 及相关 SDK 文档（开源的是 harness，不是权重）
- 博客 / 文档：
  - [Codex as a platform: build on the open agent harness](https://developers.openai.com/blog/codex-as-a-platform)（2026-08-19；ARC-AGI-3 13.3%→38.3%）
  - [Unlocking the Codex harness: App Server](https://openai.com/index/unlocking-the-codex-harness/)
  - [What Is DSH](https://deepseekdocs.com/en/docs/learn/intro/what-is-dsh)（社区文档，需对照官方仓库）
- 视频：本日未见一手新片，不编。
- 公司 / 产品 / 融资：
  - [hermes-agent 中文再传播（2026-09-06）](https://aitoolly.com/zh/ai-news/article/2026-09-06-nousresearch-unveils-hermes-agent-a-new-paradigm-for-intelligent-agents-that-grow-with-users)
  - 汽车座舱 [OpenDSH](https://opendsh.com/) 与 DeepSeek `dsh` 同名不同物，已排除。

## 未证实

- 二手文把 Codex harness 与「DeepSeek Harness」做成对照表时，部分「未开源清单」无法从 OpenAI 原文逐条核对。
- dsh 的「367 个 npm 插件」来自社区站扫描，不是 DeepSeek 官方公告。
- Hermes README 自称「唯一内置学习闭环」是营销句，不是可证伪评测。
- 用户点名的「dsh harness 新产品」已落到 DeepSeek Harness；若另有未公开内部项目，本日没有一手链接。
