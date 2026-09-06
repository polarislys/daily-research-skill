# 拒绝账本（缩网用）

Filter 阶段命中下列项时默认 **丢弃**，除非当天有极强一手由头（需在卡片 `note` 说明例外）。

与 [candidates.md](candidates.md) 的 `status: rejected` 不同：本表是**模式级**过滤，candidates 是**词级**观察。

## 主题模式（topic_block）

```text
- 岗位解读 / JD 变化 / 简历怎么写
- 纯股价预测、无产品机制的财经水文
- 「十大趋势」「一文看懂 2026」类无出处综述
- 未证实传闻当已发布写（需 candidates 或官方源证实）
```

## 域名（domain_block）

一行一个域名或后缀。Agent 发现稳定低质源可追加，**不要**把 Tier 1/2 官方域加入。

```text
<!-- 示例，按需增删 -->
<!-- example-spam-aggregator.com -->
```

## 已拒绝词（token_block）

从 candidates 晋升失败或反复误伤的词，可登记 here 避免重复进收件箱：

```text
<!-- 格式
- token: <原文>
  reason: <一句话>
  since: YYYY-MM-DD
-->
```

## 维护

- 每周扫一眼：是否误杀（删掉或加例外说明）
- 深写阶段若发现某 rejected 词其实有价值 → 移到 candidates 重新观察
