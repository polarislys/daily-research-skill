# daily-research-skill

每日把 Agent / 模型相关的产品、方法和新闻写成文章，推进 git。Cloud Agent 在电脑关机时也能跑。

远程仓库：https://github.com/polarislys/daily-research-skill

产物有三种，分开放：

| 形态 | 目录 | 写什么 |
|---|---|---|
| 产品剖析 | `output/产品剖析/<产品>/` | 组成 + 核心理念，一篇说不完就在同文件夹续写 |
| 新方法 | `output/新方法/<方法族>/` | 新名词或算法怎么转，和旧方法差在哪 |
| 新闻动态 | `output/新闻动态/<事件>/` | 发布改了什么、论坛和用户怎么评、公开市场数据 |

文件名带日期，文件夹是大主题，例如 `output/产品剖析/Warp/两条Skill加人类反馈-2026-09-06.md`。

一篇只讲 1～2 个问题点，口吻接近深度博文，不写岗位。

## 每天做什么

1. 读 `config/keywords.md`，按形态分类检索约 24 小时
2. 有材料就写，篇数不限
3. 按上面的目录落盘，推 `main`

定时：Cursor Automation [Daily research 10:00 CST](https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025)，每天 10:00（Asia/Shanghai）。网页上的 Prompt 以 `.cursor/automations/daily-research.md` 为准，改过 skill 后需要你自己贴回去。

改检索轴：`config/keywords.md`。新词先记 `config/candidates.md`。改写作或目录规则：`.cursor/skills/daily-research/SKILL.md`。

## 本机看文章

```bash
git clone https://github.com/polarislys/daily-research-skill.git
cd daily-research-skill
git pull
```

打开 `output/`。

## 手动补跑

在本仓库 Agent 对话输入 `/daily-research`，或说「运行 daily-research skill」。
