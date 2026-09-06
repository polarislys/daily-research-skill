# Cursor Automation 配置（复制到网页）

已有任务：https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025  
名称：`Daily research 10:00 CST`。改 Prompt 时用下面这一段覆盖。

## Prompt

```text
运行本仓库的 daily-research skill（.cursor/skills/daily-research/SKILL.md）。

1. 读 config/keywords.md、config/profile.md、config/sources.md、config/rejected.md。日期用 Asia/Shanghai 的今天。
2. Phase 1 — Filter：分三类检索，打分写收件箱 output/收件箱/YYYY-MM-DD.md（模板见 templates/inbox.md）。遵守 profile 的 inbox_max。
3. Phase 2 — 深写：从「建议深写: yes」按分数取 deep_write_max 条，写长文：
   - 产品剖析：官方博客/文档/仓库
   - 新方法：论文和实验室博客
   - 新闻动态：发布稿 + 论坛/评测；有公开股价或融资再写
4. 一篇只挖 1～2 个问题点。字数不卡 2000，写透即可，不要注水。不要写岗位、JD、简历。
5. 落盘：output/<形态>/<大主题>/<短标题>-YYYY-MM-DD.md。更新 output/README.md 和收件箱「深写链接」。
6. 探索通道照 skill；新词进 config/candidates.md，达标再晋升 keywords。
7. 提交并推送 main。说明：Daily research: YYYY-MM-DD
8. 不要开 Pull Request。不要改 SKILL.md。
9. 简体中文。每条事实带 URL。搜不到也要写收件箱说明并推送。
```

## 仓库

- GitHub：`polarislys/daily-research-skill`
- 分支：`main`
- 关闭自动开 PR

## 邮件（可选）

Automation 本身不发邮件。推送 main 后 GitHub Actions `Daily email digest` 会读收件箱 + 当日文章发 digest。需在仓库 Secrets 配置 `EMAIL_TO` 等，见根目录 README。
