# GitHub Copilot coding agent 的 harness 是「GitHub Actions 上的异步 PR 工厂」

形态：产品剖析  
大主题：GitHub-Copilot-Agent  
日期：2026-09-06（Asia/Shanghai）  
问题点：异步 agent 跑在哪、人怎么介入、和终端 Copilot CLI 差在哪？

## 先说清楚

GitHub 在 2025-09-25 宣布 [Copilot coding agent 全面可用（GA）](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)：付费 Copilot 用户可把任务 **委派给 Copilot**，它在 **独立开发环境** 里后台工作，通过 **GitHub Actions** 驱动，完成后开 **draft PR** 并请求人工 review；人可在 PR 上评论让 Copilot 继续改。

这和 Copilot 补全单行代码的差别是：整单 feature / bugfix / 补测试 / 文档更新被当成 **长时程自治任务**；harness 核心是 **平台托管的 Actions runtime + PR 协议**，而不是本地终端里的 REPL。

## 问题只圈这些

1. 任务从哪进、artifact 是什么（PR）、人卡在哪？  
2. HN 上对 Copilot CLI 的反馈暴露了哪些 harness 缺口？

## 它由什么构成

**入口多样化。** 可分配 issue、用全站 Agents 面板、或在 VS Code 点「Delegate to coding agent」。解决「agent 只能从 CLI 启动」的摩擦。

**异步与隔离。** agent 在自有 dev environment 跑，不占用开发者本机 shell。与 **sandbox** 的关系：隔离由 GitHub 托管环境承担，具体权限边界以官方 Policies 为准（Business/Enterprise 需管理员开启）。

**PR 作为状态工件。** 所有变更落在 draft PR；review 评论是反馈通道。这和 Anthropic 长程 harness「进度文件」同族：**git 上的可 diff 对象** 承载状态，而不是聊天窗口。

**任务类型（官方列举）。** 新功能、修 bug、还技术债、提测试覆盖、更新文档——偏软件工程闭环，不是泛聊天。

**Copilot CLI（公测，HN 2025-09）作为姊妹形态。** 终端里跑 agent，默认 Claude Sonnet 4，可用环境变量 `COPILOT_MODEL=gpt-5` 切模型。HN 用户反馈：缺 `/model`、上下文余量展示弱、危险命令（如 `rm -rf`）护栏不透明、工具输出 live 刷新会花屏。说明 **同一品牌的 harness 在「云异步 PR」与「本地 CLI」两条线成熟度不一致**——GA 的是 coding agent，CLI 仍偏 bare。

## 理念怎么落进机制

主线：**把 agent 嵌进已有代码协作协议（issue → PR → review），而不是新造一套聊天工单。**

对企业客户，Policy 开关决定能否用 coding agent——harness 不仅是技术环，还是 **治理环**。机制上可复查：**异步 agent 的默认可交付物是 PR，不是「我说做完了」。**

## 证据

- 官方：
  - [Copilot coding agent is now generally available](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)（2025-09-25）
  - GitHub Docs：Copilot coding agent（博文链接）
- 论坛：
  - [HN: GitHub Copilot CLI public preview](https://news.ycombinator.com/item?id=45377734)（模型切换、护栏、UI 缺口）
- 视频：未见本日逐条转写。

## 未证实

- 「独立开发环境」的具体镜像、网络 egress、密钥注入方式，公开文档粒度有限。  
- GA 公告日期为 2025-09-25；若读者环境尚未开放，以账户类型与 Policy 为准。  
- HN 对 CLI 的体验为匿名用户样本，不代表 GA coding agent 全貌。
