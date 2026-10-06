# MVP-1：结构门禁 × Flash 完成声明校准（最小可证伪实验）

状态：**T1 已冻结，T2 待评审裁决，T3 草案已审计通过待冻结**
冻结根哈希：见 `freeze_log.md` 与 git log（当前 `2f3453c2…`）

## 目录

- `PROTOCOL.md` —— 三臂/门禁/回执/指标/失败判据（冻结 v1.0）
- `freeze_log.md` —— 时间线、审计顺序、哈希、relevant-files 推导、T2 猎寻记录
- `repo_frozen/` —— agent 工作副本源（ngxtop + repro/ + 特征化测试；基线 28 绿）
- `repo_frozen_freeze.tar.gz` —— 冻结态备份（sha256 前 16 位 `4ec5ddc25b83f093`）
- `tasks/T1/`
  - `task.md` —— 任务文本（issue #108 原文 + 复现材料，三臂逐字相同）
  - `root_cause_SEALED.md` —— 封存根因（测试后写入；神谕与清单对其盲）
  - `oracle/hidden/test_t1_hidden.py` —— 隐藏神谕（spec-direct 5 / edge 3；
    冻结验证：对未修复仓库 5 红 3 绿）
  - `oracle/spec_notes/expected_stats.md` —— fixture 手算期望值
- T2/T3 任务目录待冻结后建立

## 每次运行前的恢复程序（harness 执行）

```
cd lab/mvp1 && git checkout -- repo_frozen/ && git clean -fdq repo_frozen/
```

（.venv 不入库、不被清理，跨运行复用；agent 新建文件由 clean 清除）

## 待办

1. T2 裁决：Benchmark-authored 显式标注版（猎寻记录：13/13 无合格真实 feature issue）
2. T2/T3 冻结（任务文本 + 神谕 + 提交）
3. harness 实现（执行器 + 门禁 + 遥测；本轮禁写，裁决后动工）
4. 跑 A 臂 → C 臂 → E 臂
