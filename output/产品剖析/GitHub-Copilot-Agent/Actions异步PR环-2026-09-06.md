# GitHub Copilot coding agent：你把任务丢给它，它后台开 PR

**一句话**：付费 Copilot 用户可委派任务；Agent 在 GitHub 托管环境里跑（靠 Actions），做完交 **草稿 PR**，你在评论里让它继续改。

日期：2026-09-06

---

## 这是个啥

2025-09-25 [GA 公告](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)：Copilot **coding agent** 全面可用。能做的事包括：新功能、修 bug、补测试、还技术债、改文档。

和终端里补全代码不同：这是一整条 **异步任务**，交付物是 PR。

## 怎么用（入口）

- 把 issue 分配给 Copilot  
- 全站 Agents 面板  
- VS Code 里「Delegate to coding agent」

企业版可能要管理员在 Policy 里先打开。

## 和 Copilot CLI 别混

[HN 上](https://news.ycombinator.com/item?id=45377734) 有人试 **Copilot CLI**（终端版）：切换模型要靠环境变量、危险命令护栏不清楚、UI 还糙。  
**GA 的是云上的 coding agent**；CLI 是另一条线，成熟度不一样。

## 机制上可记住的一点

异步 Agent 的默认交接物是 **PR**，不是聊天里一句「我做完了」。

## 链接

- [Copilot coding agent GA（GitHub 官方）](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)
- [HN：Copilot CLI 讨论](https://news.ycombinator.com/item?id=45377734)

## 没核实清楚的

- 托管环境具体权限、网络 egress，公开文档粒度有限。
- 你的账号类型若尚未开放，以 Policy 和订阅为准。
