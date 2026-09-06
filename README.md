# daily-research-skill

每日把 Agent / 模型相关的产品、方法和新闻写成文章，推进 git。Cloud Agent 在电脑关机时也能跑。

远程仓库：https://github.com/polarislys/daily-research-skill

## 产物

| 形态 | 目录 | 写什么 |
|---|---|---|
| **收件箱** | `output/收件箱/YYYY-MM-DD.md` | 先过滤：通过 / 待定 / 丢弃 + 是否建议深写 |
| 产品剖析 | `output/产品剖析/<产品>/` | 组成 + 核心理念，一篇说不完就在同文件夹续写 |
| 新方法 | `output/新方法/<方法族>/` | 新名词或算法怎么转，和旧方法差在哪 |
| 新闻动态 | `output/新闻动态/<事件>/` | 发布改了什么、论坛和用户怎么评、公开市场数据 |

一篇只讲 1～2 个问题点，口吻接近深度博文，不写岗位。

## 每天做什么（两阶段）

1. **Filter**：读 `config/keywords.md` + `config/profile.md`，分形态检索约 24 小时，写收件箱
2. **深写**：按 `profile.md` 的 `deep_write_max` 预算写长文
3. 推 `main`；可选邮件 digest（见下）

定时：Cursor Automation [Daily research 10:00 CST](https://cursor.com/automations/285afd37-a9b1-11f1-b532-320a589b8025)，每天 10:00（Asia/Shanghai）。网页 Prompt 以 `.cursor/automations/daily-research.md` 为准，改过 skill 后需要你自己贴回去。

配置文件：

| 文件 | 作用 |
|---|---|
| `config/keywords.md` | 检索轴（可选 `weight` / `depth`） |
| `config/profile.md` | 兴趣域、排除、每日预算 |
| `config/sources.md` | 来源 tier 白名单 |
| `config/rejected.md` | 模式级缩网 |
| `config/candidates.md` | 新词账本 |

改写作或目录规则：`.cursor/skills/daily-research/SKILL.md`。

## 本机看文章

```bash
git clone https://github.com/polarislys/daily-research-skill.git
cd daily-research-skill
git pull
```

打开 `output/收件箱/` 扫一眼，再点进深写文。

## 手动补跑

在本仓库 Agent 对话输入 `/daily-research`，或说「运行 daily-research skill」。

## 邮件推送（可选）

Cursor Automation **不能直接发邮件**。推荐链路：

```text
10:00 Automation 跑 skill → push main
       ↓
GitHub Actions（Daily email digest）读收件箱 + 当日文章 → 发到你邮箱
```

### 配置步骤

1. 打开 GitHub 仓库 → **Settings → Secrets and variables → Actions**
2. 必填：`EMAIL_TO`（你的收件地址）
3. 二选一：
   - **Resend**（简单）：`RESEND_API_KEY` + `EMAIL_FROM`（已验证域名下的发件地址）
   - **SMTP**（QQ/163/Gmail 等）：`SMTP_HOST`、`SMTP_PORT`、`SMTP_USER`、`SMTP_PASSWORD`，可选 `EMAIL_FROM`、`SMTP_TLS=true`
4. 保存后，下次 `output/` 有 push 会自动发；也可在 Actions 页手动 **Run workflow**

### 本机试发

```bash
python3 scripts/build-daily-digest.py --date 2026-09-06 --out-dir /tmp/digest
export EMAIL_TO=you@example.com
# Resend:
export RESEND_API_KEY=re_xxx EMAIL_FROM=onboarding@yourdomain.com
python3 scripts/send-email.py --digest-dir /tmp/digest
```

未配置 `EMAIL_TO` 时 workflow 会自动跳过，不影响日常 push。

## 落地之后还能做什么

在现有「每日收件箱 + 限量深写」之上，可以逐步加：

| 方向 | 做法 |
|---|---|
| **只扫收件箱** | 把 `deep_write_max` 设为 0，只跑 Phase 1；周末再手动 `/daily-research` 深写高分项 |
| **周度续写** | 同一 `output/产品剖析/<产品>/` 文件夹多篇递进；收件箱标 `续写` 优先 |
| **缩网** | 把误伤词写进 `rejected.md`，把噪声域从 `profile.md` 兴趣表删掉 |
| **加权检索** | 在 `keywords.md` 给重点 id 加 `weight: high` |
| **Slack / 飞书** | 仿 `send-email.py` 加一个 webhook 脚本，在 workflow 里并行一步 |
| **RSS** | 用 GitHub Pages 或 Actions 把 `output/` 转成 feed（静态站生成器读 md） |
| **人工批复** | 收件箱「待定」区你改 `建议深写: yes` 后，次日 Automation 优先深写 |
