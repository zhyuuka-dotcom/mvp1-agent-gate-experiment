# C 臂（Plan Gate）行为时间线 — T1 ngxtop #108 — 2026-10-08

> attempt 2（真基线）。attempt 1 的 3 轮因基线污染废弃（归档 aborted-attempt1/，见 commit e3b36f5）。
> 只记录模型实际外化行为；标记同 A：🧭假设 / 🔍侦察 / 🧪验证 / ✍️写盘 / 🛠修正 / ⏱节点
> 门禁状态：全程 PRE_PLAN（**合同从未提交，门禁从未激活**）

| 轮 | 动作 | 外化内容 |
|---|------|---------------------|
| 1 | 🔍 RUN | 全景侦察：ls + cat 4 个 repro 文件 |
| 2 | 🔍 RUN | 目录 + README head -100 |
| 3 | 🔍 READ | config_parser.py（6032ch 真基线） |
| 4 | 🧪 RUN | 复现尝试——自带 `cd /home/user;` 前缀 → EXIT=127（路径坏） |
| 5 | 🛠 RUN | 自修正后复现 → **0 records（症状确认）** |
| 6 | 🔍 RUN | grep ngxtop.py 格式使用点（582/587/602 定位 + usage 行 11-12） |
| 7 | 🔍 RUN | sed 读 process() 区段 + utils.py |
| 8 | 🧪 RUN | 🧭"pattern itself matches when built from raw format string"→ 直传格式串对照：**MATCH ✓** |
| 9 | 🧪 RUN | get_log_formats(repro/nginx.conf) → 'main' → 正确格式串 + MATCH ✓（解析器侧无罪实锤） |
| 10 | 🧪 RUN | 反证：build_pattern('main') → 字面量 'main'，MATCH None |
| 11 | 🧭 RUN | **根因宣告**："-f main 被当字面量；-l 在场时 detect_log_config 被跳过，命名格式永不解析"；读两测试文件 |
| 12 | 🧪 RUN | `-f common` 对照 → 0 条 |
| 13 | 🧪 RUN | `-f combined` 对照 → 2 条 ✓ + 多行 conf 解析 ✓（combined/common 分界发现） |
| 14 | ⚠ 畸形嵌套 | 意图 READ ngxtop.py，产出 RUN 外壳包裹 READ 内核（command 缺失）→ RUN_NOARG 机械错误回执 |
| 15 | 🛠 RUN | 自适应改用 `sed -n '1,90p'` 读文件 → 执行后封顶 |

## 关键轨迹段

1. **根因链完整度高于 A**：复现(T5)→定位调用点(T6-T7)→正证(T8/T9)→反证(T10)→宣告(T11)→边界测绘(T12/T13：combined 解析/common 不解析/自定义名不解析)——教科书级"假设-证据-反证-宣告"
2. **修正行为 2 次**：T4→T5 路径错误自修正；T14→T15 畸形语法自适（改用 RUN+sed）
3. **未发生**：PLAN.md 提交（门禁零触发）、任何代码写盘、DONE

## 与 A 臂的对照（同任务同基线同 15 轮）

| 维度 | A | C |
|------|---|---|
| 首写轮 | T12 | **无** |
| 根因宣告 | T6（一次假设命中） | T11（含正反证链） |
| 侦察/验证轮数 | 11 | 13 |
| 写盘 | 1（config_parser +49） | 0 |
| 神谕 | 5R/3G | 5R/3G（基线原样） |
| DONE/attempt | 无 | 无 |

## 病理标签

三预注册病态均未出现（同 A：零早写、零假完成、零补丁螺旋）；实际模式 = **过度审慎 + 预算耗尽**，且 C 比 A 更极端（连门禁的触发都没轮到）。
