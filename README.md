# MVP-1 — 结构门禁 × LLM 完成声明校准（最小可证伪实验）

> Minimal falsifiable experiment: can low-cost structural gates make a fast model's
> "declare DONE" trustworthy — without slowing it down?
> 研究问题：能否用最低限度的结构门禁，让快速生成模型保持速度优势，同时显著降低
> "快速做错然后宣布完成"的概率？

## 这是什么

一个单任务（T1）、三臂（A/C/E）的 agent 行为基准实验，全部工件冻结可复现：

- **任务**：真实开源 bug（[lebinh/ngxtop#108](https://github.com/lebinh/ngxtop/issues/108)）——命名日志格式 `-f main` 无法解析
- **神谕**：隐藏验收测试 8 条（spec-direct 5 + edge 3），冻结前验证红绿逻辑（对未修复仓库 5 红 3 绿）
- **指标**：FDV（First-Done Validity，首次 DONE 时神谕已通过）、假完成率、返工结构、成本
- **纪律**：oracle/相关文件对实验者根因封存件盲写；预注册失败判据；全程轨迹保留

## 三臂

| 臂 | 定义 | 状态 |
|----|------|------|
| A | Bare flash baseline（任务文本 + 自由工具调用） | ✅ 已跑（15/15 封顶，无 DONE，FDV=false，神谕 5R/3G） |
| C | A + 计划合同门禁（PLAN.md 机械校验 R1-R5，通过后 WRITE 白名单） | ✅ 已跑（门禁未触发：合同从未提交，零写盘，封顶） |
| E | C + DONE 独立验收回执 | ⏸ 待运行 |

## 两臂初步结论（单 run，无统计力）

预注册的三种病态（早写代码 / 早假完成 / 补丁螺旋）**零出现**；两臂一致死于
**过度审慎 + 轮次预算耗尽**——A 花了 11 轮侦察后才首次写盘（修复未接线），
C 把预算花在边界测绘上零产出。裸模型的轮次分配缺乏内生预算意识；
"假完成"假设在本任务上暂无靶。

## 目录

```
PROTOCOL.md              三臂协议/门禁规则/指标/预注册失败判据（冻结 v1.0）
freeze_log.md            冻结时间线、哈希链、T2 猎寻记录、调用约定
repo_frozen/             agent 工作副本（ngxtop 冻结快照 + repro/ 复现材料 + 特征化测试）
tasks/T1/task.md         任务文本（issue #108 原文，三臂逐字同文）
tasks/T1/root_cause_SEALED.md  根因封存件（测试之后写入，git 顺序可证）
tasks/T1/oracle/         隐藏神谕 + 手算期望值 + provenance 分类
runs/A/                  A 臂全档（15 轮逐档、遥测、时间线、封顶快照、报告）
runs/C/                  C 臂全档（含 attempt1 基线污染事故归档）
```

## 复现

```
cd repo_frozen && uv venv .venv && uv pip install --python .venv/bin/python \
  docopt tabulate pyparsing pytest
.venv/bin/python -m pytest tests/ -q          # 基线 28 绿
MVP1_REPO=$PWD .venv/bin/python -m pytest ../tasks/T1/oracle/hidden/ -q   # 5 红 3 绿
```

模型：deepseek-flash（thinking 关闭，max-tokens 8192，15 轮/臂）。
agent 循环 harness：`runs/A/exec_request.py`（READ/RUN/WRITE 通道 + DSML 原生
工具调用语法适配，全部通道适配均对应回执发出前落盘，见各 report 注记）。

## 归属与许可

- `repo_frozen/` 是 [lebinh/ngxtop](https://github.com/lebinh/ngxtop) 的冻结快照，
  **MIT License**（见 repo_frozen/LICENSE.txt），冻结目的为实验可复现性；上游
  后续演进不在本仓库范围。
- 其余文件（协议、神谕、运行档案、报告）为本实验原始工件，随仓库公开。
- 运行数据中不含任何凭据/个人信息（上传前经六类秘密模式扫描复验）。

## 状态

- 2026-10-06 冻结 T1 + 神谕；2026-10-07 A 臂；2026-10-08 C 臂（含一次基线污染
  事故的发现与修复，全程留痕）；E 臂待运行。
- git 历史即审计链：冻结 → 神谕封存 → A → 污染修复 → C。
