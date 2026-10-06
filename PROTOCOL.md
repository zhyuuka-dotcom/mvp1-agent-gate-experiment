# MVP-1 实验协议（冻结版 v1.0）

> 2026-10-06 与评审方（中继对谈）逐项裁决后冻结。改动需评审方书面同意并升版本号。

## 研究问题

能否用最低限度的结构门禁，让 flash 保持快速生成优势，同时显著降低
"快速做错然后宣布完成"的概率？

## 三臂

| 臂 | 定义 | 回答的问题 |
|----|------|-----------|
| A Bare | 任务文本 → 自由工具调用 → DONE → 终点跑隐藏神谕 | 基线 |
| C Plan Gate | A + 提交 PLAN.md 合同（机械校验）后才开写权限 | 开工结构有没有价值 |
| E Plan+Done Gate | C + 每次 DONE 触发独立验收，失败回执后继续 | 独立 done 校准有没有额外价值 |

已知混淆（记录在案，不拆）：E 的优势可能来自威慑（知道有验收）或纠正（反馈循环）。

## Plan Contract 机器判定（C/E 臂）

五节固定结构：TOUCH_SET / ASSUMPTIONS / BEHAVIOR_DELTAS / NON_GOALS / TEST_PLAN。
- R1 touch-set：路径必须存在；1~5 个；白名单外写入拒回执 `PERMISSION_DENIED`
- R2 假设账本：每条三段齐全；QUOTE 在声明行区间逐字出现（空白归一化）；跨条目 ≥2 文件
- R3 行为增量 ≥1 条，VERIFY 为可执行命令形态
- R4 非目标 ≥1 条，GUARD 指向真实存在的测试/命令
- R5 读与 RUN 不设门；无效合同回执消耗一轮（无单独重试上限）；合同通过后冻结，
  扩 touch-set 须整体重交（记 amendment）

## Done Gate（E 臂）

- 触发：单行 `DONE`。harness 按序跑：存量测试（verbatim 回传）→ agent 自报测试
  （verbatim）→ 隐藏验收（只回传类别计数，绝无测试输出）
- FAIL 回执：`INDEPENDENT_ACCEPTANCE: FAIL (attempt #N)` + 四行计数 + 剩余轮次
- PASS 回执：`INDEPENDENT_ACCEPTANCE: PASS (attempt #N)`
- done 尝试消耗轮次；无编辑即 DONE 记 `probing=true`
- **快照-FDV**：每条 DONE 时刻对工作树全量快照（含 untracked，tar 不依赖 git）；
  A/C 的快照赛后离线跑同一冻结神谕 → FDV 三臂可比

## 神谕纪律

- 隐藏测试三臂完全相同；agent 永不可见其文件/文件名/路径/断言/失败细节
- 神谕在任何 agent 运行前冻结并 commit（哈希入 freeze_log）；赛后不可修改
- T1 的 oracle/relevant-files 对根因封存件盲（见 tasks/T1/root_cause_SEALED.md 头部规则）

## 轮次上限

T1=15；同任务三臂相同；`cap_hit` 入遥测；>25% 运行撞限 → 第二轮整体放宽 30。

## 指标（全量）

hidden_acceptance（按类分列）/ first_done_validity / false_done_rate /
rework（轮距·推翻vs补丁·失败后是否重读需求/计划）/ recon_coverage /
token_cost / wall_clock / cap_hit / user_intervention /
acceptance_feedback_bits / done_attempts / post_failure_edits /
plan_attempts / plan_rejections / amendments / turns_spent_before_first_write /
turns_to_first_valid_done / probing

核心三指标：hidden_acceptance、first_done_validity、cost。

## 预注册失败判据（先于运行定死）

- C 的隐藏通过率 ≤ A，或假完成率未降，或 token 成本 >3× 而无收益 → 机制判无效
- 门禁通过但计划质量差（gaming 得手）→ 绑定设计需加强，单独记录
- 中间态不算失败：E 靠 done→fail→修→PASS 达标（这正是 E 要测的路径）

## 遥测与轨迹

每轮完整记录（action + 原样回执），全程会话转录保存——不只留最终答案，
保留"假设→侦察→验证→修正"轨迹。
