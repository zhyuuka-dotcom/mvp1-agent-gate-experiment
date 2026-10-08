# Step 0 — INDEPENDENT_ACCEPTANCE 实现说明与自测记录

> 执行序列 v3 Track 1d（块 10）。规格面唯一权威：D-005（DECISIONS.md）。
> 本实现照此，无自行裁量空间。

## 实现（runs/E/independent_acceptance.py，254 行）

| 函数 | 对应规格 | 说明 |
|------|----------|------|
| is_done_message | 冻结 DONE 语义 | `^DONE\s*$`（re.M）——A/C 臂 exec_request 同源同正则 |
| parse_self_reports | 5.2(d) | 恒返回 []（n=0 路径）；声明语法待 PI 裁定（见待裁 A），唯一扩展点 |
| run_self_reports | 5.2(a)(b) | w=rc0 计数；执行报错/失败计入 n 不计入 w（执行器就绪，待声明语法接入） |
| run_existing_suite | 5.1 z/28 | venv 直调 pytest tests/（冻结调用协议） |
| run_oracle | 5.1 x/5, y/3 | MVP1_REPO 参数化 + -v 逐行解析；结果集与配置清单不重合→熔断（D-004(4)） |
| count_new_test_files | 5.2(c) | 工作副本 tests/ vs 冻结基线 → 遥测"新建测试文件数 vs 声明数" |
| snapshot_working_tree | PROTOCOL FDV | 每 DONE 全工作树快照（含 untracked，排除 .venv/__pycache__） |
| run_acceptance | 5.1/5.3 | PASS=spec5/5∧edge3/3∧存量28/28∧自报w=n（n=0 空真） |
| 回执 | 防泄露条款 | 恰 5 行：ACCEPTANCE PASS/FAIL + 四行计数，绝无测试名/神谕输出/断言细节 |
| 遥测 | D-001(3)+5.2(c) | counts/per-test/自报明细/新测试文件/integrity/DSML 记录位 |

## 自测（runs/E/test_independent_acceptance.py，13 条，全绿）

覆盖映射（块 10d 指定四项）：
1. **DONE 触发路径**：test_done_detection_frozen_regex（8 变体，含 DONE./口语句/混合请求行）+ test_cli_done_trigger_end_to_end（CLI 端到端：DONE→rc0+回执；非 DONE→rc2 不触发）
2. **四行计数**：test_four_line_counts_pass / _spec_red / _existing_red_and_new_files（spec 1/2、存量 28/29、新建测试文件遥测列 [1,0]）
3. **PASS 边界含 n=0**：test_pass_boundary_n0_vacuous（纯 DONE 空真 PASS）+ test_self_reports_stub_is_n0（5.2(d) 不自行约定口径）+ test_self_report_executor_pass_fail_error（w/n 语义）+ test_integrity_fuse_on_config_mismatch（熔断）
4. **回执防泄露**：test_receipt_anti_leak 三路径（回执恰 5 行、计数行格式、14 个泄露标记零命中）
辅助：test_fdv_snapshot_created（快照落盘非空）

结果：**13/13 passed（2026-10-09 04:2x，repo_frozen/.venv pytest）**

## T1 真配置集成记录（runs/E/acceptance_config_T1.json）

| 工作副本 | 回执原文 | exit |
|----------|----------|------|
| 未改动仓库（冻结基线副本） | `ACCEPTANCE FAIL / spec-direct 0/5 / edge 3/3 / 存量 28/28 / 自报 0/0` | 1 |
| 实验者参考修复（/tmp/t1-impl，不入库） | `ACCEPTANCE FAIL / spec-direct 4/5 / edge 3/3 / 存量 28/28 / 自报 0/0` | 1 |

参考修复（最小补丁，/tmp 保留供 E 放行核验）：process() 在 `-l` 给定且
`-f` 为纯名字（非 combined/common/caddy 预设、无 `$`）时经 `-c` 配置
get_log_formats 解析命名格式，未知名 error_exit 干净报错。存量 28/28 绿；
神谕 8 条中 7 绿——**剩 1 条为冻结神谕自身绿路径 bug，见下**。

## 发现一（报 PI 待裁 A）：冻结 DONE 消息格式无自报声明槽位

D-005 5.2(d)：冻结 mechanics（"任务完成时，单独一行声明：DONE"）无
显式声明槽位 → parse_self_reports 恒 n=0（未自行约定口径）。E 臂
mechanics 文本（harness 运行时提供，尚未冻结）需要 PI 裁定声明语法；
管线其余部分已就绪，裁定后仅需在 EXTENSION POINT 实现解析。

## 发现二（报 PI 待裁 B）：T1 冻结神谕 spec#1 绿路径 bug

- **症状**：参考修复（正确实现）下 test_named_format_single_line 假红
  → 神谕 4/5 → INDEPENDENT_ACCEPTANCE 恒 FAIL（上表实证）
- **根因**：summary_row() 取"Summary: 后首个含数字的行"——orgtbl 表头行
  含数字（2xx/3xx/4xx/5xx 列名）→ 返回 [2,3,4,5] 而非数据行 [5,1626.6,…]
- **为何冻结时未暴露**：红绿验证只有红侧被执行过（未修复仓库在
  "5 records processed" 断言处即红，从未走到 summary_row）；绿侧（8/8）
  冻结时无修复实现可跑
- **影响**：E@15 若 agent 正确修复 T1，回执恒 spec 4/5 FAIL，E 反馈环
  永远无法 PASS——E 臂判读失效
- **处置纪律**：神谕冻结（freeze_log"赛后不可修改"+2026-10-07 审计
  "零改动"）→ 本执行者不静默修改，报 PI 裁定：
  (a) 新开裁决条目修订该测试断言（注明替代关系；修订后复验 5红3绿 +
  参考修复 8/8）；(b) 保留原样接受假阴性（E 臂失效，不推荐）；(c) 其他

## 遗留（非阻塞）

- E 运行器（exec_request E 版 + DSML 逐轮记录 + E-mechanics 文本）：
  E 放行后组装
- git ls-files 清单：PI 保留待办
