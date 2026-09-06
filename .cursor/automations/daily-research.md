# Cursor Automation 配置（复制到网页）

已有任务：https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025  
名称：`Daily research 10:00 CST`。改 Prompt 时用下面这一段覆盖。

## Prompt

```text
运行本仓库的 daily-research skill（.cursor/skills/daily-research/SKILL.md）。

1. 读取 config/keywords.md，按关键词检索过去约 24 小时的中英文信息。
2. 日期用 Asia/Shanghai 的今天。
3. 只挑 2～4 个问题点，写成 2～4 篇金字塔文章；每篇 1～2 个问题，约 2000 汉字，向下挖两层并解释术语。
4. 每篇存到 output/主题-YYYY-MM-DD/article.md，更新 output/README.md。
5. 必须跑 skill 里的探索通道：优先论文和国内外资讯，其次新仓库/视频；招聘只作滞后印证，不能单独晋升新词。新词写入 config/candidates.md；达到阈值再晋升到 config/keywords.md。
6. 提交并推送到 main。说明：Daily research: YYYY-MM-DD
7. 不要开 Pull Request。不要改 SKILL.md。
8. 简体中文。每条事实带 URL。搜不到也要留一篇说明并推送。
```

## 仓库

- GitHub：`polarislys/daily-research-skill`
- 分支：`main`
- 关闭自动开 PR
