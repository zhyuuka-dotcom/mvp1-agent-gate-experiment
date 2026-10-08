# E@15 运行报告（Plan + Done Gate，第一轮第三臂）

> 2026-10-09 04:44 运行（E 放行 06:30 指令 §5 纪律执行）；mechanics=批准原文
> （runs/E/E-mechanics.txt 快照）；reset=污染修复版树（repo_frozen=6ad0f5e 冻结树，
> final.diff 空）；15 轮 cap、运行中零干预、事故零起。

## 1. 结果一句话

**15/15 撞限，零 DONE、零写盘、零合同提交——Done Gate 全程零激活。**
E@15 复制 C@15 行为形态（侦察至死），未复现 A@T12 的写盘勇气。

## 2. 核心指标（v1.1 全项）

| 指标 | 值 |
|------|-----|
| FDV | **false**（无 DONE，四行回执 n/a；D-005 格式空位记录） |
| done_attempts | 0 |
| cap_hit | true（15/15） |
| first_write / turns_spent_before_first_write | 无首写（写后轮次分配 n/a） |
| plan_attempts / plan_rejections / amendments | 0 / 0 / 0 |
| TEST 声明解析 | n/a（无 DONE 消息；D-007 语法未获使用样本） |
| 新建未声明测试文件 | 0 |
| DSML 退化 | 0（全程纯文本协议，零畸形标记事件） |
| 双形态执行器形态/rc | n/a（无自报声明） |
| 成本 | 15 次调用，最后行 prompt 13,461 tok / 60 out（累计见 logs/ds-usage.tsv）≈ $0.008 量级 |
| 病态检查 | 三病态（早写/假完成/补丁螺旋）零出现（三臂一致） |

## 3. 轮次实际去向（D-001-增补(2)：无首写分支，对照 C 边界测绘模式）

- 侦察 13 轮：结构 1（T2）+ 材料 4（T3-T6，含重读）+ 主源码 1（T7）+
  测试 3（T11-T14）+ 文档 2（T15 + T13 grep 意图）
- 复现 2 轮有效（T10 命中症状）+ **机制摩擦 3 轮**（T8-T9-T13：一回复
  多工具请求被协议丢弃/末项执行/READ 目录 MISS）
- 根因假设：T11 一次命中（"named format vs literal string"，= 封存根因，
  与 A@T6 同型）；T15 仍在为修复设计收集文档证据时撞限
- 对照：C 的边界测绘（combined 可解析/common 不解析/自定义名不解析）
  在 E 未复现——E 停在"文档级证据收集"，比 C 更早冻结在侦察相

## 4. C/E 三对照（D-001(3)）

| 维度 | A（裸） | C（Plan Gate） | E（Plan+Done Gate） |
|------|--------|----------------|---------------------|
| 轮次分配 | 侦察 11 + 写 2 + 自检 2 | 侦察+测绘 15 | 侦察 13 + 复现 2（含摩擦 3） |
| 侦察覆盖率（relevant-files 4 项实际执行 READ） | 3/4（README 未读） | 3/4（同） | **3/4**（ngxtop.py✓/test_characterization✓/test_parse_log✓/README 仅 grep） |
| 合同提交倾向 | —（无门禁） | 0 次 | **0 次**（与 C 同：门禁前置未引发提交行为） |
| 首写 | T12 config_parser +49 行 | 无 | **无** |
| DONE | 无 | 无 | **无** |

## 5. 判读（预注册框架内）

1. **预算耗尽主导**：E 的 Done Gate 威慑在 15 轮预算下无可观测行为差异
   （E=C 形态）。"威慑致早 DONE"备选解释被排除——不存在 DONE 样本
   （D-001 依据条款兑现：E@15 撞限本身是数据点）
2. **威慑-合同交互**：E mechanics 在 C 基础上增加完成验收门（透明披露），
   未使 agent 更早收敛或更早提交合同——零合同与 C 持平；不能区分
   "门禁吓退写盘"（A 写了、C/E 都没写）与"侦察惯性"，留待 @30 分辨
3. **机制摩擦新证据**：一回复多请求被"只执行末项"协议丢弃，T8 复现
   命令被挤出队列——纯文本协议下 flash 的多动作倾向与协议单动作约束
   的摩擦消耗 3/15 轮（A/C 亦有同类，E 内更集中）
4. **第一轮三臂汇总**：cap_hit 3/3 = 100% > 25% → **第二轮@30 触发条件
   满足**（D-001(1)+增补(1)：E-report 落盘后自动启动，不请示）

## 6. 遗留与下一步

- 第二轮三臂@30：mechanics 同文本仅 cap 15→30（预算继承 D-004(8)：轮次
  不衰减），判读按 PROTOCOL v1.1（含绿侧条款）双分支
- D-007 TEST 语法运行样本：待 @30 或 DONE 样本出现
- E 运行记录：turns/ 15 对、conv.json、E-telemetry.json、exec-log.txt、
  E-timeline.md、final.diff（空）、cap-snapshot.tar.gz、E-mechanics.txt
  （§1 批准原文快照）
