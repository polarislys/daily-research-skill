# Cursor Automation 配置（复制到网页）

在 https://cursor.com/automations/new 新建 Automation，按下面填。
Cloud Agent 不能代你点保存，需要你在已登录的 Cursor 账号里激活一次。

## 基本信息

- 名称：`Daily research 10:00 CST`
- 权限：Private（记在你个人用量上）
- 状态：保存后立刻启用

## Trigger

- 类型：Scheduled
- 时区：Asia/Shanghai
- 时间：每天 10:00
- 若只有 cron、且按 UTC：`0 2 * * *`（北京时间 10:00）

## 仓库

- 必须选 **单个仓库**：GitHub 上的 `daily-research-skill`
- 分支：`main`
- 不要选「No repository」，否则产物无法提交

## 工具

- 允许提交并推送到 `main`
- 关闭「创建 Pull Request」（个人日报仓库直接落主分支）
- 需要联网搜索

## Prompt（整段粘贴）

```text
运行本仓库的 daily-research skill（.cursor/skills/daily-research/SKILL.md）。

1. 读取 config/topics.md 的主题。
2. 按 Asia/Shanghai 的今天日期，调研过去约 24 小时的信息。
3. 把简报写到 output/YYYY-MM-DD.md，并更新 output/README.md。
4. 提交并推送到 main。提交说明：Daily research briefing for YYYY-MM-DD
5. 不要开 Pull Request。不要改 skill，除非主题文件缺失。
6. 用简体中文。每条事实带来源 URL。搜不到就在当天文件里写明，仍然提交。
```

## 验收

- 激活后可用「Run now」先跑一次
- 仓库 `output/` 应出现当天 markdown
- 本机 `git pull` 能看到简报
