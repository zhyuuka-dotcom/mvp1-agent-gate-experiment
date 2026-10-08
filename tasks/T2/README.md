# T2 状态（盲态保护中——D-006）

- `task.md`：Benchmark-authored 完整规格（D-002(1) 显式标注），已推送。
  项目负责人盲推仅读本文件所在目录的 `task.md`
- `oracle/`：神谕草稿（spec-direct 5 + edge 3 + oracle 侧 fixture 副本 +
  expected_stats）——**未推送**（D-006 盲态保护：推导清单存档前不出现在
  任何项目负责人可见文件）。本地以 .git/info/exclude 排除，防止误提交
- 红绿预验证（本地记录，2026-10-09 04:0x）：未改动仓库 spec 4 红 1 空真
  （invalid 值被 docopt 拒=同可观测行为）/ edge 3 绿；实验者原型 8/8 绿；
  存量 28/28 绿
- 冻结时序（D-002(3) + D-006）：文本+神谕已备 → 待项目负责人盲推清单 →
  匹配审计（映射完备性+重合度≥90%）→ 通过后 oracle 随冻结 commit 入库
