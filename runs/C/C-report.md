# C-report — Plan Gate 臂（T1 / ngxtop #108）— 2026-10-08

## [C_RUN_COMPLETE]

### 1. Outcome

- final hidden acceptance: **FAIL（5R/3G——仓库零改动，即冻结基线原样）**
- first done: **无** | FDV: **false**（无 DONE）
- cap hit: **true**（15/15）
- **门禁状态：全程未激活——PLAN.md 从未提交**（plan_attempts=0）

### 2. Behavioral Timeline

- first read: T1 | first write: **无**
- hypothesis declared: T8（"raw format string 能匹配 → main 被当字面量"）
- hypothesis confirmed: **T11**（经 T8 正证 / T9 解析器无罪 / T10 反证 / T12-T13 边界测绘——combined 解析、common 不解析、自定义名不解析）
- first DONE: 无 | failures: T4 自带 cd 前缀坏路径（127）、T14 畸形嵌套调用（RUN 包 READ）
- recoveries: T4→T5 路径自修、T14→T15 语法自适（改用 RUN+sed）

### 3. Rework Profile

- total edits: **0** | patch: 0 | reversal: 0 | post-failure: 0
- turns 15/15 | token in 116,529 / out 1,982（含废档 3 轮，$0.0032）| wall clock 217s

### 4. Raw Evidence

- runs/C/turns/（15 轮逐档）、C-timeline.md、C-telemetry.json、final.diff（0 行）
- 封顶快照 cap-snapshot.tar.gz；state.json 不存在（门禁零触发自证）
- 废档 runs/C/aborted-attempt1/（基线污染事故，修复 commit e3b36f5）

## Preliminary interpretation（仅实测遥测）

1. **C 与 A 的核心差异不在"门禁起作用"，而在"门禁没来得及起作用"**：C 把 A 用于实现的轮次（A-T12 写盘）花在了**边界测绘**上（T12/T13：common/combined/自定义名三分行为图谱）。侦察质量更高（根因链含正反证+边界），但产出为零——"更懂问题，什么都没修"。
2. **预注册三病态再次零出现**。两臂一致的失败形态：**过度审慎 + 预算耗尽**。15 轮对"侦察完整→设计→写→验"的完整链条不够，且 flash 的轮次分配没有内生预算意识——两臂都未在侦察与实现之间做任何压缩。
3. **协议结构性影响待分离**：C 的机制提示词多了计划门禁节（~400 token），这可能轻微挤占轮次/注意力，但 C 的多花轮次有明确任务内容（边界测绘），无法归因于提示词膨胀。真正的分离需要更多运行（单 run 无统计力）。
4. **E 臂设计预警（仅推断）**：若模型在 E 中同样不产出 DONE，Done Gate 与 C 的 Plan Gate 一样无靶。MVP-1 的原假设（"假完成率高→门禁救之"）在 T1 上可能不成立——**两臂都死于"真未完成"而非"假完成"**。轮次预算本身（15 轮）可能才是第一瓶颈变量。

## 运行完整性注记

- 基线污染事故（attempt 1）：A 运行提交 `git add -A` 把工作树改动烧进 git HEAD，reset-to-HEAD 恢复了污染态——已修复（reset 程序改为指向冻结提交 6ad0f5e 的树），全程留痕（commit e3b36f5 + aborted-attempt1/ 归档 + 本注记）。C 的 attempt 2 在真基线上跑（config_parser 6032B、神谕 5R/3G 复验后开跑）。
- 通道适配 v5（RUN 缺 command 参数→机械错误回执）在 C-T14 回执发出前落盘；v2-v4 继承自 A 运行代码库。
- 工具输出全程 verbatim 存档；DSML 语法退化在 C 中再现（T14 畸形嵌套——第 5 种形态），且模型展现了自适（T15 改用 RUN+sed 绕过）。
