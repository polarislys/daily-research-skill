# GitHub Copilot coding agent：你把 issue 丢给它，它后台给你开 PR

2025-09-25 [GA 了](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)：Copilot **coding agent**。付费用户可以把 feature、bugfix、补测试、还技术债、文档更新 **委派** 给 Agent；它在 GitHub 托管环境里跑（靠 **GitHub Actions** 当 runtime），做完交 **draft PR**，你在评论里让它继续改。

和 IDE 里补全完全不同：这是 **异步 harness** 跑完整 software task，状态落在 PR 上，不是聊天里一句「做完了」。

入口很多：分配 issue、全站 Agents 面板、VS Code「Delegate to coding agent」。Enterprise/Business 可能要管理员开 Policy。

## 别和 Copilot CLI 混

[HN 上](https://news.ycombinator.com/item?id=45377734) 有人试终端 **Copilot CLI**：切模型靠 `COPILOT_MODEL` 环境变量、危险命令护栏不清楚、UI 还糙。**GA 的是云 coding agent**；CLI 是另一条 harness 线，成熟度不一样。

---

**参考**

- [Copilot coding agent GA](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/)
- [HN：Copilot CLI](https://news.ycombinator.com/item?id=45377734)

托管环境权限、egress 公开文档粒度有限；账户是否开放以订阅和 Policy 为准。
