# 新词候选账本（未晋升，不参与主检索）

每日**探索通道**扫到的新叫法先记在这里，不要直接写进 [keywords.md](keywords.md)。
主检索仍然只用 keywords；本表是自我进化的记忆，避免「只在旧词附近打转」。

## 晋升阈值（满足任一且能写清与旧 id 的差）

1. **14 天内 ≥ 3 个独立一手来源**（不同公司 / 不同作者 / 官方文档，转载算同一个）
2. **连续 ≥ 3 个跑次**都出现，且每次至少 2 个来源
3. 已是 **≥ 2 家** OpenAI / Anthropic / Google / Cursor / 字节 / 腾讯 / 阿里 / 月之暗面 的岗位名或职责原词

还要同时满足：能用 2 句中文说出它和已有 `id` 的差别。说不清 → 只当旧 id 的 alias 候选，不新开 id。

产品名（dsh、hermes）进 keywords 的「产品与赛道」aliases，不进概念层。

## 行格式

```text
- token: <原文>
  en:
  zh:
  first: YYYY-MM-DD
  last: YYYY-MM-DD
  days: <出现过的跑次天数>
  sources: <累计独立来源数>
  urls:
    - 
  near: <最像的旧 id，没有写 unknown>
  status: watching | promoted | rejected
  note:
```

`status: promoted` 后把完整对照行写入 keywords，本行留档不删。
`rejected` 写明原因（广告词、公司内部黑话、与旧 id 同义）。

## 在观察

_暂无。第一次跑探索通道后往这里追加。_

## 已晋升

_暂无_

## 已拒绝

_暂无_
