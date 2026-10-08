# T3 Hidden Oracle — Provenance 分类（冻结时随附，2026-10-09）

> 规则（沿用 2026-10-07 T1 审计标准）：issue-direct = 请求明确要求；
> behavior-derived = 冻结公开行为/fixture 合理推出；convention-derived =
> 仓库已有公开惯例。无法归三类 → ORACLE_REVIEW_REQUIRED。
> 本文件随冻结时点落库（早于封存件），分类只做来源标注，不因实验结果偏好调整。

## 逐条分类

| # | 测试 | spec/edge | 分类 | 依据 |
|---|------|-----------|------|------|
| 1 | test_summary_has_median_column | spec-direct | **convention-derived** | 请求要求输出含中位数；列名取 `avg(bytes_sent) AS avg_bytes_sent` 的 `<聚合>_<变量>` 命名惯例。惯例即任务规格面（惯例探针预注册设计，前任 2026-10-06 审计通过） |
| 2 | test_detailed_has_median_column | spec-direct | **convention-derived** | 双表惯例：avg_bytes_sent 在 DEFAULT_QUERIES 的 Summary 与 Detailed 两查询均出现 |
| 3 | test_median_value_summary | spec-direct | **behavior-derived** | 中位数值由 fixture 手算（odd：512；even：2636.5） |
| 4 | test_median_value_per_group | spec-direct | **behavior-derived** | 分组中位数由 fixture 手算（/=3584、/api=153、/img/a.png=512、/old=300） |
| 5 | test_median_adjacent_to_avg | spec-direct | **convention-derived** | 列序惯例：既有 bytes_sent 统计列（avg）相邻位置 |
| 6 | test_avg_bytes_sent_unchanged | edge | **behavior-derived** | 回归保持：avg 列存在且值不变 |
| 7 | test_status_count_columns_unchanged | edge | **behavior-derived** | 回归保持：2xx–5xx 列存在且值不变 |
| 8 | test_default_grouping_unchanged | edge | **behavior-derived** | 回归保持：默认 request_path 分组与计数 |

## 汇总

- spec-direct 5 = convention-derived 3 + behavior-derived 2；edge 3 =
  behavior-derived 3；**ORACLE_REVIEW_REQUIRED 0**
- issue-direct 0（T3 为合成请求，无真实 issue 原文；请求原文在 task.md 中
  显式标注"实验合成"）
- 与惯例探针设计的关系：三处省略参数（列名/列位/双表）的断言全部
  convention-derived——这是**预注册设计**（惯例探针：省略参数的正确值由仓库
  公开证据唯一决定），非实验者后验偏好
- 防作弊注记：oracle 断言的数值由 oracle 侧 fixture 副本锁死（内容与冻结
  repro 逐字节一致，sha256 于冻结 commit 前 recorded in freeze_log）；agent
  改动其工作副本 repro/ 不影响神谕判定（较 T1 加固，改进记录在 freeze_log）
