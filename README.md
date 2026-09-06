# daily-research-skill

个人每日调研仓库。Cloud Agent 在电脑关机时也能跑；简报只写进 git，方便任意电脑 `git pull` 查看。

## 它做什么

1. 读取 `config/topics.md` 里的主题
2. 每天 **10:00（北京时间）** 调研过去约 24 小时的信息
3. 把简报写到 `output/YYYY-MM-DD.md` 并推送到 `main`

Skill 定义在 `.cursor/skills/daily-research/SKILL.md`。改主题只改 `config/topics.md`。

## 1. 在 GitHub 建个人仓库

这个 Cloud Agent 会话**没有 GitHub 登录**，不能替你在 github.com 点「New repository」。请在本机已登录 `gh` 的终端、于本仓库目录执行：

```bash
gh auth login
bash scripts/publish-to-github.sh
```

默认建成**私有**仓库 `daily-research-skill`。要公开：

```bash
VISIBILITY=public bash scripts/publish-to-github.sh
```

或在网页创建空仓库 `daily-research-skill`（不要勾选自动加 README），然后：

```bash
git remote add github https://github.com/<你的用户名>/daily-research-skill.git
git push -u github main
```

## 2. 设置每天 10 点定时跑

Cursor Automation 不能从仓库文件自动启用，需要你在账号里保存一次。完整字段见 [`.cursor/automations/daily-research.md`](.cursor/automations/daily-research.md)。

摘要：

1. 打开 [cursor.com/automations/new](https://cursor.com/automations/new)
2. Trigger：Scheduled，时区 `Asia/Shanghai`，每天 10:00  
   若界面是 UTC cron，用 `0 2 * * *`
3. 仓库选 GitHub 上的 `daily-research-skill`，分支 `main`（必须选仓库，否则无法提交）
4. Prompt 粘贴 `.cursor/automations/daily-research.md` 里的那一段
5. 关闭自动开 PR；允许推送到 `main`
6. 保存并启用，点一次 **Run now** 验收

## 本机看产物

```bash
git clone https://github.com/<你的用户名>/daily-research-skill.git
cd daily-research-skill
git pull
```

打开 `output/` 下当天的 markdown。也可以直接在 GitHub 网页浏览。

## 手动补跑

在本仓库开 Agent，说「运行 daily-research skill」即可。本地 Agent 同样会往 `output/` 写文件；要让其它设备看到，需要推送到 GitHub。
