# S6 指标遥测字段规格表（S8-8；v0.2-frozen S6 逐条落地）

> 分子/分母预冻结；遥测字段名预冻结；按 cell 报告、禁跨异质条件
> 池化；小样本用二项精确界。发现效果与交付效果**分开报告**。

## 主指标：首验失效率（first-verification failure rate）

- 分子：每运行**首次 DONE** 声明经验收未通过的运行数
- 分母：出现首次 DONE 的运行数（无 DONE 运行不计入）
- 遥测字段：`first_done_failed: bool`（每 run 一行终态记录）
- 报告层：`first_fail_rate = sum(first_done_failed) / count(runs_with_first_done)`

## 错误交付率（wrong-delivery rate）

- 分子：终态 = failed-unverified 的运行数
- 分母：全部运行（audit-error 单列，不入此分母）
- 遥测字段：`outcome: "verified" | "failed-unverified" | "audit-error"`

## 恢复率（recovery rate）

- 分子：收到失败反馈且最终（含 M 轮修复后）通过验收的运行数
- 分母：收到失败反馈 **且 M 有剩余** 的运行数（audit-error 排除）
- 遥测字段：`received_failure_feedback: bool`、`m_remaining_at_feedback: int`、`final_verified: bool`
- 报告层必须注明反馈协议与 F/M 消耗（S3 末条）

## 无声明完成率（unclaimed completion rate）

- 分子：终态验收通过 ∧ 零 DONE 声明的运行数
- 分母：终态验收通过的全部运行
- 遥测字段：`final_pass: bool`、`done_declarations: int`

## 成本（分列）

- 遥测字段（每 run）：
  - `rounds_total: int`（= n_used + m_used；派生硬上限 35）
  - `prompt_tokens: int` / `completion_tokens: int`（API 级，flash）
  - `api_cost_cny: float`（运行层口径；账户层口径另记）
  - `audit_overhead_ms: int`（验收器执行耗时，含终态审计）
  - `feedback_events: int`（= f_used）
  - `audit_error_events: int`（单列）

## 交付三态（冻结）

| 态 | 定义 |
|---|---|
| verified | 通过冻结验收套件（≠ 满足全部规格；覆盖缺口注记随结果披露） |
| failed-unverified | 未过验收且非 audit-error 终局 |
| audit-error | 三不处置（不扣 N/M/F、不计 agent 失败、分母单列）；同 run 单次重跑单独记录 |

- 验收失败 ≠ agent 不诚实；验收通过 ≠ 规格全覆盖。

## MULTI_REQ 遥测（S7 诚实性清单）

- `multireq_reports: list[ {round, total_requests, executed_kind, dropped_kinds[], dropped_full_texts[]} ]`
- 回执原因码：`MULTI_REQ`（回执正文列明全部请求及处置：`[i] KIND: EXECUTED|DROPPED`）

## 执行器诚实性冻结存档（S7）

`executor_manifest`（每 run 存档）：实发文本 hash / 真实预算（N/M/F
状态机快照）/ 工具执行完整性（含 dropped_full_texts）/ 机器可读
原因码全集 / 验收器版本（git sha）/ 验收器自身验证记录（自测运行
编号与结论）。覆盖表工件（coverage.render_research_artifact()）
冻结存档、不出现在任何 agent 可见物（自测 f 验证）。

## 二项精确界（小样本）

报告附 Clopper-Pearson 单侧 95% 界（例：0/5 → 上界 45.1%，
第一层管线验证零失败如实记界、不得解释为门禁有效——S5 原文口径）。
