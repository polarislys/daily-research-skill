# Cursor Automation 配置（复制到网页）

已有任务：https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025  
名称：`Daily research 10:00 CST`。改 Prompt 时用下面这一段覆盖。

## Prompt

```text
运行本仓库的 daily-research skill（.cursor/skills/daily-research/SKILL.md）。

1. 读 config/keywords.md。日期用 Asia/Shanghai 的今天。
2. 分三类检索，不要混成一篇：
   - 产品剖析：官方博客/文档/仓库，把成熟产品的组成和理念讲透
   - 新方法：论文和实验室博客，讲清新名词或算法原理
   - 新闻动态：发布稿 + 论坛/评测反馈；有公开股价或融资再写
3. 一篇只挖 1～2 个问题点。篇数不限。字数不卡 2000，写透即可，不要注水成长文。
4. 不要写岗位、JD、简历。
5. 落盘：output/<形态>/<大主题>/<短标题>-YYYY-MM-DD.md（日期只在文件名）。同产品多篇放同一文件夹。更新 output/README.md。
6. 探索通道照 skill：论文和资讯优先；新词进 config/candidates.md，达标再晋升 keywords。
7. 提交并推送 main。说明：Daily research: YYYY-MM-DD
8. 不要开 Pull Request。不要改 SKILL.md。
9. 简体中文。每条事实带 URL。搜不到也要留一篇说明并推送。
```

## 仓库

- GitHub：`polarislys/daily-research-skill`
- 分支：`main`
- 关闭自动开 PR
