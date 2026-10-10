# SPEC.md｜任务 top-n（agent 可见规格文本，冻结）

> 冻结：2026-10-11（D-022 §3(b)）；sha256 见 MANIFEST.sha256
> 版本：v1.0-frozen

## 任务：为 ngxtop 新增 --top N 数据行限流

功能规格：

1. 命令行新增 `--top <N>`（N 为正整数或 0）：**作用于 Detailed
   表数据行**——按既有排序键取前 N 行（平序按现有稳定顺序）；
   Summary 聚合行不受影响。
2. `--top 0`：Detailed 仅保留表头（零数据行），Summary 照常。
3. **非整数或负数 N：参数层报错**（退出码非零；报错不得晚于
   查询执行层）。
4. 与既有 `-n/--limit` 相互独立：组合时 `--top` 优先于 `--limit`
   生效于数据行数；不改变 `-n` 的任何现有行为。
5. 无 `--top`：输出与现状逐字节一致（零回归，含 -n 现状）。

验收例（逐值；输入数据可读：<DATA_DIR>/access.log 共 5 条记录、
Detailed 基线 4 个数据行）：

- `--top 3`：Detailed 恰 3 行；首行 == 无 --top 基线首行
- `--top 99`：Detailed 全量 4 行
- `--top 0`：Detailed 0 数据行，rc=0
- `--top 2147483647`：rc=0，全量
- `--top abc`：rc != 0
- `--top -1`：rc != 0
- `--top 3 -n 10`：Detailed 3 行（--top 优先）

> 定稿修订登记（2026-10-11，冻结动作内）：草案 §1 原为"Summary
> 与 Detailed 均保留前 N 行"——设计核对发现 ①Summary 聚合恒
> 1 行、截断无对象 ②既有 -n/--limit 与原草案重叠（--limit 作用于
> 查询 LIMIT）。修订为 --top 独立作用于 Detailed 数据行+组合
> 优先级语义，使暗区（参数层校验/组合优先级）与 -n 现状形成
> 可测对照。登记于 MANIFEST 与 WP2 包末报告。

## mechanics 基座条款（v1.0 §0/§1/§2）

按 mvp2/MECHANICS.md v1.0（裸 A 基线：无门禁/无审计条款）。
