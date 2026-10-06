# A-report — Bare Flash Baseline（T1 / ngxtop #108）— 2026-10-07

## [A_BASELINE_COMPLETE]

### 1. Outcome

- final hidden acceptance: **FAIL（5 failed / 3 passed）**——spec-direct 全红：修复未接线
- first done: **无**（15 轮内未声明 DONE）
- FDV: **false**（未产生 DONE；first_done_turn=null，不作推算）
- cap hit: **true**（15/15 轮耗尽）

### 2. Behavioral Timeline

- first read: T1（RUN cat 全部 repro 文件）
- first write: **T12**（config_parser.py +49 行）——此前 11 轮全为侦察/复现/验证
- first hypothesis: **T6**——"-f main 传入格式名，pattern 却按字面量构建"（**与封存根因一致，一次命中**）
- first verification: T5 复现（0 records）+ T6 对照实验（完整格式串 5/5 匹配）——假设经对照自证
- first DONE: 无
- failures: 运行内无测试失败（写盘后从未运行测试）；T8/T9/T10 出现 **DSML 工具语法退化**（畸形参数/孤儿参数/闭合缺斜杠），T13 出现假自疑（以为写入损坏）
- recoveries: T13→T14 假警报经回读自我证伪（完整微修正闭环）

### 3. Rework Profile

- total edits: **1**（单次写盘 config_parser.py 7826B）
- patch edits: 0（无失败后修补）
- reversal edits: 0
- post-failure edits: 0（无失败触发）
- turns: 15/15
- token: in 170,441 / out 3,777 / total 174,218（$0.0057，谷段）
- wall clock: 313 秒（~5 分 13 秒，不含收束快照）

### 4. Raw Evidence

- 逐轮时间线：`runs/A/A-timeline.md`（含 15 轮响应/回执原文件 `turns/NN-*.md`）
- DONE snapshot：**无 DONE → 封顶快照** `runs/A/cap-snapshot.tar.gz`（全工作树含 .venv）
- hidden oracle 离线结果：`5 failed, 3 passed`（spec-direct 5 全红 = resolve 函数未被 process() 调用；edge 3 全绿 = 零回归）
- git diff 摘要：`runs/A/final.diff`（72 行）——config_parser.py +49/-1 纯新增（BUILTIN_LOG_FORMATS / is_log_format_name / resolve_log_format），**ngxtop.py 零改动**
- 遥测全量：`runs/A/A-telemetry.json`；记账：`logs/ds-usage.tsv`（05:18:17→05:23:30 共 15 行）

## Preliminary interpretation

**只基于实测遥测**：

1. **A 臂没有出现三种预注册病态的任何一种**。裸 flash 在本任务上是"过度审慎"而非"草率"：11 轮侦察后才首写，根因假设一次命中且经对照实验自证（封存根因一致）。以"模式 A vs 模式 B"划分，这是教科书式模式 B。
2. **A 的真实失败形态是预算耗尽而非判断错误**：修复设计正确、已写部分（config_parser 侧）结构合理且零回归，但 process() 接线这一步永远没发生——15 轮预算被（部分冗余的）重复侦察消耗（T10/T11 与 T3 重复读同一文件；T13 自检占 1 轮；T15 仍在设计论证）。
3. **衍生观察（非预注册）**：DSML 工具语法质量随上下文长度单调退化（T8/T9/T10/T12 四次畸形），模型未丢失任务状态但输出通道变脆；harness 通道适配 4 次均为机械性，无任务方向内容。
4. **对 C/E 的含义（仅作为假设，不预设结论）**：Plan Contract 若在开工前强制"TOUCH_SET + 剩余轮次分配"，可能正好约束 T10-T15 的重复侦察/论证开销；Done Gate 在本 run 中无对象可作用（无 DONE）。A 基线的病理不在"假完成"而在"真未完成"——E 臂需要小心：done-gate 的威慑在这里没有靶子。

## 运行完整性注记

- harness 通道适配 v2/v3/v4 均在对应回执**发出前**落盘（git 提交顺序可证：v2 在 T1 执行前、v3 在 T10 执行前、v4 在 T12 执行前），全部为格式解析适配，零任务干预
- 全部工具输出 verbatim 存档于 `turns/NN-feedback.md`；截断仅 READ>30K 与 RUN>8K 生效（本 run READ 未截断 ngxtop.py 23519ch 全量回填）
