# daily-research-skill

给 Agent 架构 / 训练 / 评估 / 垂域落地岗位用的每日雷达。Cloud Agent 在电脑关机时也能跑；文章只进 git。

远程仓库：https://github.com/polarislys/daily-research-skill

## 每天做什么

1. 读 `config/keywords.md`（JD 会变，关键词跟着变）
2. 检索过去约 24 小时：新仓库、博客、视频、公司/产品/融资、工作模式变化
3. 写成若干篇约 2000 字的金字塔文章（每篇只挖 1～2 个问题，向下两层）
4. 存到 `output/主题-YYYY-MM-DD/article.md` 并推 `main`

定时：Cursor Automation [Daily research 10:00 CST](https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025)，每天 10:00（Asia/Shanghai）。

改检索轴：只改 `config/keywords.md`。改写作规则：改 `.cursor/skills/daily-research/SKILL.md`。

## 本机看文章

```bash
git clone https://github.com/polarislys/daily-research-skill.git
cd daily-research-skill
git pull
```

打开 `output/` 下「主题-日期」文件夹。

## 手动补跑

在本仓库对 Agent 说「运行 daily-research skill」。
