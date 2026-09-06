---
name: daily-research
description: 按 config/topics.md 做每日调研简报，写入 output/YYYY-MM-DD.md，提交并推送到当前分支。用于定时 Cloud Agent / Automation。
---

# 每日调研

这是本仓库的定时调研 skill。电脑关机时由 Cloud Agent 执行；产物只允许写进 git，禁止写本机桌面。

## 何时使用

- 用户说「跑每日调研」「daily research」
- Cursor Automation 按日程启动本仓库
- 需要补做某一天的简报

## 步骤

1. 读取 [config/topics.md](../../../config/topics.md)。没有有效主题就写一份说明到当天文件，然后停止。
2. 日期用 **Asia/Shanghai** 的当天日期，文件名为 `output/YYYY-MM-DD.md`。
3. 对每个主题用网络搜索查**过去约 24 小时**的信息。优先一手来源：官方博客、文档、监管原文、被多家媒体转述的事实。
4. 按下面模板写入 `output/YYYY-MM-DD.md`。已有当天文件则更新，不要另开副本。
5. 更新 [output/README.md](../../../output/README.md)：顶部增加当天条目，最新日期在最前。
6. **提交并推送到当前分支**（通常是 `main`）。
   - 提交说明：`Daily research briefing for YYYY-MM-DD`
   - **不要开 Pull Request**
   - 只暂存 `output/` 和你这次改过的调研文件，不要把无关文件加进去

## 简报模板

```markdown
# 每日调研 · YYYY-MM-DD

时区：Asia/Shanghai  
生成：Cloud Agent

## 摘要

- 用 3～5 条写今天最值得看的变化

## 主题：<主题名>

### <条目标题>

- 事实：
- 为什么重要：
- 来源：

## 未覆盖 / 不确定

- 搜不到或互相矛盾的内容写在这里

## 明日可跟进

- 可选，1～3 条
```

## 硬性规则

- 用简体中文
- 每条事实都要有来源 URL；不要编造链接或新闻
- 不要把密钥、Cookie、本机路径写进简报
- 不要修改 skill 或主题文件，除非用户明确要求
- 搜索失败就在简报里写明失败原因，仍然提交当天文件，让日程留下记录
