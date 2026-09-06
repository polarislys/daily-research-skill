# GitHub Copilot coding agent：异步 harness，交付物是 draft PR

**一句话**：付费 Copilot 可委派任务；Agent 在 GitHub 托管环境跑（**GitHub Actions** 当 runtime），做完交 **draft PR**，你在评论里让它继续改。

日期：2026-09-06

---

## 这是个啥

[2025-09-25 GA](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)：Copilot **coding agent** 全面可用。任务类型包括 feature、bugfix、补测试、还技术债、文档。

和 IDE 补全不同：这是 **异步 harness** 跑完整 software task，状态落在 PR 上。

## 入口

- 分配 issue 给 Copilot  
- 全站 Agents 面板  
- VS Code「Delegate to coding agent」

Enterprise/Business 可能要管理员开 Policy。

## 和 Copilot CLI

[HN 讨论](https://news.ycombinator.com/item?id=45377734) 里 CLI 仍偏 bare：切模型靠 `COPILOT_MODEL` 环境变量、护栏不透明、UI 问题多。**GA 的是云 coding agent**；CLI 是另一条 harness 线。

## 机制上记住

异步 Agent 默认交接物是 **PR**，不是聊天里一句「做完了」。

## 链接

- [Copilot coding agent GA](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)
- [HN：Copilot CLI](https://news.ycombinator.com/item?id=45377734)

## 没核实清楚的

- 托管环境权限、egress 公开文档粒度有限。  
- 账户是否开放以订阅和 Policy 为准。
