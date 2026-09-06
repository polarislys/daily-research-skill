# daily-research-skill

每日把 Agent / 模型相关的产品、方法和新闻写成文章，推进 git。

远程仓库：https://github.com/polarislys/daily-research-skill

## 产物（扁平目录）

**`output/` 下无子文件夹**，只有文章 md：

```text
output/<短标题>-YYYY-MM-DD.md    # 深写，约 2000 汉字
output/收件箱-YYYY-MM-DD.md      # 过滤卡片
```

文首 YAML 写 `形态`、`主题`、`日期`。写作规范：`.cursor/skills/daily-research/STYLE.md`（宝玉体 + 术语保留）。

## 每天做什么

1. Filter → 写 `output/收件箱-YYYY-MM-DD.md`
2. 深写 → `output/<短标题>-YYYY-MM-DD.md`（见 `config/profile.md` 的 `deep_write_max`）
3. 推 `main`

定时：[Daily research 10:00 CST](https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025)

## 本机阅读

```bash
git pull
ls output/*.md
```

## 邮件（可选）

复制 `scripts/daily-email-digest.workflow.yml` → `.github/workflows/`，配置 `EMAIL_TO` 等 Secrets。见上文邮件配置或 `scripts/build-daily-digest.py`。
