# T2 Hidden Oracle — Provenance 分类（冻结时随附，2026-10-10）

> 规则（沿用 2026-10-07 T1 审计标准）：issue-direct = 请求明确要求；
> behavior-derived = 冻结公开行为/fixture 合理推出；convention-derived =
> 仓库已有公开惯例。无法归三类 → ORACLE_REVIEW_REQUIRED。
> T2 为 Benchmark-authored 合成规格，无 issue 原文——"请求"= task.md
> 规格 bullet（1-8）与验收例（1-3），逐条映射如下。
> **状态注记（如实）**：hidden 测试文件自 f1e2109 起一字未改（V22 审计
> 点）；其文件头"本目录未推送至公开仓"注释已过时（f1e2109 起在库），
> 按 D-013 §0 裁定冻结不改一字、过时性记此。PROVENANCE 为冻结时新增
> 随附文档（神谕零改动的旁证文件）。

## 逐条分类

| # | 测试 | spec/edge | 分类 | 依据 |
|---|------|-----------|------|------|
| 1 | test_json_structure_and_stdout_purity | spec-direct | **spec-derived**（bullet 3+4） | stdout 恰一 JSON 文档/两键/状态行 stderr——bullet 3、4 原文直述 |
| 2 | test_json_summary_values | spec-direct | **spec-derived**（bullet 4 + 例 1/2） | 键集、整数/数值类型、逐值等于验收例（fixture 手算，spec_notes） |
| 3 | test_json_detailed_values | spec-direct | **spec-derived**（bullet 4 + 例 1/2 + bullet 8 后半） | 行对象键=分组列+统计列、字符串类型、集合语义；-g 换列键随列名（bullet 8"键随分组列名"） |
| 4 | test_table_mode_unchanged | spec-direct | **spec-derived**（bullet 1+2） | 缺省≡显式 table；状态行+两 orgtbl 表现行格式 |
| 5 | test_invalid_format_rejected | spec-direct | **spec-derived**（bullet 5 + 例 3） | 非法值 rc≠0+stderr 一行+stdout 无 JSON |
| 6 | test_default_combined_tables | edge | **behavior-derived** | 冻结公开行为锚点（默认 combined 两表，特征化测试同源） |
| 7 | test_multi_group_by_unchanged | edge | **behavior-derived** | 冻结公开行为（-g a,b 多列分组，T1 oracle edge 同源；bullet 8 前半将其升格为规格要求——归 edge 保持冻结分组） |
| 8 | test_access_direct_records | edge | **behavior-derived** | 冻结公开行为（直传格式串 5 records） |

## 汇总

- spec-direct 5 = spec-derived 5（bullet 1-5 + 例 1-3 + bullet 8 后半）；
  edge 3 = behavior-derived 3；**ORACLE_REVIEW_REQUIRED 0**
- 匹配审计（D-009 修订轮）：GLM-5.3 复审计 8/8 = 100% ≥ 90%
  （comm/PI-20261009-2340.md §2 映射表）；清单 v2 =
  comm/T2-BLIND-DERIVATION-v2-20261009-2310.md（15 项+7 边界候选，
  推导者 flash，资格裁定合格）
- 与 v1 审计差异记录：E2（多分组回归锚点）在 v1 为 text-gap，v2 文本
  bullet 8 闭合后复审计通过——规格完备性由文本修订达成，神谕未动
- 防作弊注记：oracle 断言数值由 oracle 侧 fixture 副本锁死（与冻结
  repro 逐字节一致，expected_stats.md 手算值在案）；-g 换列用例的
  分组值（10.0.0.1/2/3 计数 2/2/1）同源手算
