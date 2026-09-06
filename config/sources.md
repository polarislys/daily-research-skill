# 来源白名单与分级

Filter 阶段用本表判断「一手源质量」。tier 越高，收件箱综合分越高（见 [profile.md](profile.md)）。

## Tier 1（+3）

优先检索、优先深写。

| 类型 | 示例 |
|---|---|
| 论文预印本 | arxiv.org、openreview.net |
| 官方研究/工程博客 | openai.com/blog、anthropic.com/news、deepseek.com、ai.googleblog.com |
| 官方文档与 RFC | docs.*、github.com/*/README、官方架构文 |
| 一手发布稿 | 产品官网 changelog、GitHub Release（官方仓库） |

## Tier 2（+2）

可作主证据；中文深度文需回到 Tier 1 核对机制。

| 类型 | 示例 |
|---|---|
| 严肃科技媒体 | 机器之心、量子位、36氪（有署名与链接） |
| 高质量中文解读 | 宝玉等能圈住问题并链回官方的公众号文 |
| 论坛一手讨论 | news.ycombinator.com、reddit.com/r/LocalLLaMA、v2ex.com |
| 知名实验室博客 | 大学/公司研究组博客（非转载） |

## Tier 3（+1）

仅作线索或市场侧补充，不宜单独支撑深写。

| 类型 | 示例 |
|---|---|
| 二手编译 | 无一手链接的资讯汇总 |
| 视频 | YouTube、B 站（需标频道与日期） |
| 行情/融资 | 雪球、财经稿（必须有可打开数据页） |
| 社交短帖 | X/Twitter 单条（需多源交叉） |

## 默认丢弃

- 招聘站、脉脉职级帖、无来源截图
- 无法打开或明显 AI 洗稿的聚合站
- 域名在 [rejected.md](rejected.md) 的 `domain_block` 列表

## 使用方式

收件箱每条卡片写：

```text
sources: tier1 | <url>
```

若多源，写最高 tier + 主 URL，其余 URL 放 `urls` 列表。
