# 执行者状态报告 #8 — mechanics_T2 终文候批

> 发件：执行者 | 2026-10-10 00:55
> 短触发词：**mechanics_T2 终文候批**
> D-014（采丙）已全执行；终文+自测六用例落库（commit `ab35bab`），
  候你通读批准（v8(2)：E 臂实际运行文本必读，不接受摘要代读——
  runs/T2/mechanics_T2_E_final.md 全文 74 行）。

## 1. 终文清单（runs/T2/）

| 文件 | 性质 |
|------|------|
| mechanics_T2_A.md | A 臂运行文本 = T1 冻结原文逐字（无门禁无占位，即终文） |
| mechanics_T2_C_final.md | C 臂终文（T1 文本 + 丙条款全文替换占位） |
| mechanics_T2_E_final.md | **E 臂终文（你的必读项）**：T1 批准文本 + 丙条款 |
| validate_plan_T2.py | 丙机械校验器（R2-T2 全新；R3/R4/R5 与 T1 逐字同；R1-T2 见 §2） |
| exec_request_T2.py | C/E 执行器（exec_request_e + validator 换丙 + 见 §3） |
| run_t2.py | 运行驱动器（参数全同 T1：flash/2048/disabled/3 重试；cap 15/30） |
| selftest-quotes/ | D-014(d) 六用例记录（6/6 符合预期） |

丙条款五条件对照（D-014 缺一退回项）：a 适用范围+新建豁免明文 ✓
（终文 ASSUMPTIONS 规则段）；b 机械规格 ✓（单行/trim≤120/exact
substring/多引不拒/整体拒）；c 代差标注 → 已写入 T2 E-report 模板槽位
（报告时随运行数据出）；d 自测六用例 ✓（1过/2拒/3拒/4拒/5过/6自然
失败）；e 修正案纪律 ✓（D-014 条目记替代关系，T1 mechanics 原文零改动）。

## 2. R1-T2 启用性改动（披露，候你批准时一并裁）

D-014(a) 新建文件豁免 + (d)⑤ 豁免用例"过" ⇒ TOUCH_SET 须可含新建文件；
而 PROTOCOL v1.0 R1 冻结条款="路径必须存在"（T1 校验器如此实现）——
两文交互构成推断张力。实现取最小启用改动：**R1-T2 = 路径存在 或 父
目录存在**（保留防拼错保护）；用例⑤经此通过。若你裁定 R1 维持 T1
原案（新建文件不可入 TOUCH_SET），我回退该改动+改用例⑤为"结构性
拒"并重跑自测——裁量在你，批准即视为采 R1-T2。

## 3. Harness 缺陷发现与修复（披露）

自测⑥发现 T1 执行器承袭 quirk：**截断 WRITE 分支正则缺 re.M**（闭合
分支有）→ 文中截断写入落入 NO_ACTION（空转回执，反馈误导）。处置：
- T2-C/E（exec_request_T2.py）：补 re.M 对齐 → 截断合同回执"WRITE
  块未闭合"，自然失败路径正确（§1.2 判读落地：计 n 不计 w，无特殊
  机制）
- T1 冻结件（runs/A|C|E 执行器）：不动；T2-A 沿用 runs/A/exec_request.py
  （quirk 原样，可比性优先）——臂间不对称已在 selftest 记录披露
- 该修复属 harness 缺陷对齐，非门禁语义变更

## 4. 下一步

你通读 mechanics_T2_E_final.md（及 C/A 如需）→ 批准（含 §2 R1-T2
裁量）→ 触发「T2 已启动」→ flash×{A,C,E}×{15,30} 六次（零干预）→
T2 E-report（代差标注 + D-007 TEST 首样本判读槽位）→ T3（D-003 序）

**mechanics_T2 终文候批**
