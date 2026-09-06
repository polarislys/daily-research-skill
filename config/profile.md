# 兴趣画像（Filter 用）

每日调研**先过滤、再深写**。本文件定义「什么值得进收件箱、什么值得花字数深写」。

改这里不用动 SKILL.md。Agent 每次跑 daily-research 时读本文件 + [keywords.md](keywords.md) + [sources.md](sources.md)。

## 兴趣域（命中加分）

按优先级从高到低。命中多个域可叠加，但单条卡片最多标 2 个主域。

| 域 id | 说明 | 典型命中 |
|---|---|---|
| harness | 智能体执行环、夹具、runtime | harness、agent loop、Temporal、沙盒 |
| skills | Skill 文件化、检索、自进化 | SKILL.md、skill-rag、MASkills、Warp Skill |
| training | Agent 训练、信用分配、RL 微调 | TIGPO、PGPO、GRPO、reward shaping |
| sandbox | 隔离执行、代码沙盒 | OpenSandbox、E2B、container sandbox |
| product-launch | 可验证的产品/模型发布 | 官方 announcing、版本 changelog、开源仓库 |
| eval | 评测、基准、hands-on | benchmark、评测视频、论坛实测 |

## 排除（命中则默认丢弃）

- 招聘、JD、职级、简历、「对 XX 岗意味着什么」
- 无 URL 的转载、标题党、纯营销通稿
- 与上表兴趣域完全无关的泛 AI 评论（除非当天有硬新闻由头）
- 已在 [rejected.md](rejected.md) 登记且未过期的模式

## 每日预算

控制「先扫一眼」和「写长文」的量，避免每天 10 篇深写。

```yaml
inbox_max: 20        # 收件箱卡片上限（通过+待定合计）
deep_write_max: 6    # 当日深写篇数上限（三形态合计）
min_deep_score: 7    # 建议深写：综合分 ≥ 此值（满分 10）
```

综合分（Agent 自评，写入收件箱卡片）：

- 兴趣域命中：+2/域（最多 +4）
- 一手源质量（见 sources.md tier）：tier1 +3，tier2 +2，tier3 +1
- 24h 新鲜度：+2（有明确今日由头）/+0（仅背景续写）
- 可写问题清晰度：+2（能一句话说清 1～2 个问题点）/+0（模糊）
- 重复惩罚：同大主题 7 天内已有深写 → -3

## 深写优先级

1. `建议深写: yes` 且分数最高
2. 同产品文件夹可续写（有新材料）优先于全新主题
3. 新闻动态：有官方发布 + 论坛可核对反应
4. 新方法：有预印本或实验室一手文
5. 产品剖析：有官方架构/文档，或高质量中文解读能回到一手源

当日已达 `deep_write_max` 时：其余「建议深写」留在收件箱标 `queued`，次日可优先。

## 形态倾向（软约束，非硬配额）

```yaml
prefer:
  产品剖析: 2
  新方法: 2
  新闻动态: 1
```

只是排序参考；某天只有新闻也可以全写新闻。
