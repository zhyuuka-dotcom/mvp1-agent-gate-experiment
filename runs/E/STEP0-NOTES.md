# Step 0 — INDEPENDENT_ACCEPTANCE 实现说明与自测记录

> 执行序列 v3 Track 1d（块 10）。规格面唯一权威：D-005（DECISIONS.md）。
> D-007（2026-10-09 05:10）落地：TEST 声明语法。本实现照裁决，无自行裁量。

## 实现（runs/E/independent_acceptance.py）

| 函数 | 对应规格 | 说明 |
|------|----------|------|
| is_done_message | 冻结 DONE 语义 | `^DONE\s*$`（re.M）——A/C 臂 exec_request 同源同正则 |
| parse_self_reports | **D-007** | DONE 行后精确前缀 `TEST `（大写+一空格）行=声明；不要求紧邻；重复各计一次；非精确前缀/DONE 前内容不是声明；n=0 合法 |
| run_self_reports | 5.2(a)(b)+D-007 | 声明两形态机械执行：repo 内存在且 .py → venv pytest；其余 shell（报错自然计 n 不计 w）；通过=rc0 |
| run_existing_suite | 5.1 z/28 | venv 直调 pytest tests/（冻结调用协议） |
| run_oracle | 5.1 x/5, y/3 | MVP1_REPO 参数化 + -v 逐行解析；结果集与配置清单不重合→熔断（D-004(4)） |
| count_new_test_files | 5.2(c) | 工作副本 tests/ vs 冻结基线 → 遥测"新建测试文件数 vs 声明数" |
| snapshot_working_tree | PROTOCOL FDV | 每 DONE 全工作树快照（含 untracked，排除 .venv/__pycache__） |
| run_acceptance | 5.1/5.3 | PASS=spec5/5∧edge3/3∧存量28/28∧自报w=n（n=0 空真） |
| 回执 | 防泄露条款 | 恰 5 行：ACCEPTANCE PASS/FAIL + 四行计数，绝无测试名/神谕输出/断言细节 |
| 遥测 | D-001(3)+5.2(c)+D-007(5) | counts/per-test/自报明细（含 form 与 rc）/新测试文件/integrity/DSML 记录位 |

E 臂 mechanics（D-007 落地文本）：runs/E/mechanics_e_draft.md（候放行
时 PI 审；冻结 A/C mechanics 运行记录不动，替代关系=D-007 条目）。

## 自测（runs/E/test_independent_acceptance.py，19 条，全绿）

覆盖映射（块 10d 四项 + D-007(4) 四类）：
1. **DONE 触发路径**：test_done_detection_frozen_regex + test_cli_done_trigger_end_to_end
2. **四行计数**：test_four_line_counts_pass / _spec_red / _existing_red_and_new_files
3. **PASS 边界含 n=0**：test_pass_boundary_n0_vacuous + test_self_reports_stub_is_n0 + test_self_report_executor_pass_fail_error + test_integrity_fuse_on_config_mismatch
4. **回执防泄露**：test_receipt_anti_leak 三路径（14 泄露标记零命中）
5. **D-007 四类**：test_d007_zero_declarations（零声明）/ 
   test_d007_multiple_and_duplicate_declarations（多条+重复）/ 
   test_d007_error_declaration_n_not_w（含错：文件不存在+exit 7）/ 
   test_d007_prefix_variants_not_declared（小写/裸 TEST/行首空白/前置于 DONE）
6. **D-007 补充**：test_d007_path_form_pytest_execution（路径形态→venv
   pytest；命令形态同过）+ test_d007_integration_receipt_self_report_line
   （集成：声明通过→自报 1/1 PASS；声明失败→自报 0/1 FAIL）
辅助：test_fdv_snapshot_created

结果：**19/19 passed（2026-10-09 05:3x）**；上一版本 13/13（04:2x）。

## D-008 修正（T1 神谕 spec#1）——见 freeze_log.md 修正条目

- summary_row 最小 diff：数据行判据=以 | 起始且首列可解析为数值
  （表头行首列为列名、分隔行首列为 ---，均自然排除）——锚定 docstring
  "第一条数据行"原意（D-008(1)）
- 复验三件全档：runs/E/integration-records/post-d008/
- 替代关系：冻结 commit 34f1d8c 的该函数实现（D-008 授权，PROVENANCE
  追加条目）

## 遗留（非阻塞）

- E 运行器（exec_request E 版 + DSML 逐轮记录）：E 放行后组装，
  mechanics 用 runs/E/mechanics_e_draft.md
- git ls-files 清单：PI 保留待办
