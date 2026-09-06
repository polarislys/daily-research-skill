# Cursor Automation 配置（复制到网页）

已有任务：https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025  
名称：`Daily research 10:00 CST`。改 Prompt 时用下面这一段覆盖。

## Prompt

```text
运行本仓库的 daily-research skill（.cursor/skills/daily-research/SKILL.md）与 STYLE.md。

1. 读 config/keywords.md、config/profile.md、config/sources.md、config/rejected.md。日期用 Asia/Shanghai 的今天。
2. Phase 1 — Filter：写 output/收件箱-YYYY-MM-DD.md（Markdown 可点击链接，无子文件夹）。
3. Phase 2 — 深写：按 deep_write_max 写 output/<短标题>-YYYY-MM-DD.md，每篇约 2000 汉字，宝玉体，术语保留（harness/DPO 等）。
4. 不要写岗位。更新 output/README.md。新词进 config/candidates.md。
5. 提交并推送 main。说明：Daily research: YYYY-MM-DD。不要开 PR。不要改 SKILL.md。
```

## 仓库

- GitHub：`polarislys/daily-research-skill`
- 分支：`main`
