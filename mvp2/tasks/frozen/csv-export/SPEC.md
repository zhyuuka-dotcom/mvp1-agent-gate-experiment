# SPEC.md｜任务 csv-export（agent 可见规格文本，冻结）

> 冻结：2026-10-10（D-022 §3(b)）；sha256 见 MANIFEST.sha256
> 版本：v1.0-frozen

## 任务：为 ngxtop 新增 --csv 输出开关

功能规格：

1. 命令行新增 `--csv` 布尔开关（与既有 `-l/-f/--no-follow`
   参数共存）。
2. 开启后 **Summary 与 Detailed 两段**均输出为 CSV：各段首行
   为列头（逗号分隔），随后每行一条记录，列顺序与各自人类可读
   表列一致。
3. 不开启时输出与现状逐字节一致（零回归）。

> 定稿修订登记（2026-10-10，冻结动作内）：草案 §2 原为
> "Summary 表输出为 CSV"——冒烟验证发现 Summary 列全数字，
> 逗号转义暗区（EC-3）不可测；修订为两段均 CSV 使暗区可测。
> 登记于 MANIFEST.sha256 附注与 WP2 包末报告。

验收例（逐值；输入数据可读：<DATA_DIR>/access.log 共 5 条
记录；<DATA_DIR>/edge.log 含 3 条特殊记录；<DATA_DIR>/
empty.log 为空文件）：

- `-l <DATA_DIR>/access.log -f <main 格式串> --csv --no-follow`：
  首行 = Summary 列头行（逗号分隔，与表列一致）
- 同输入：CSV 数据行数值与人类可读模式 Summary 表逐条一致
- 不加 `--csv`：输出与当前基线逐字节一致
- `-l <DATA_DIR>/empty.log -f <main 格式串> --csv --no-follow`：
  合理输出（本任务不限定形态）
- `-l <DATA_DIR>/edge.log -f <main 格式串> --csv --no-follow`：
  合理输出（本任务不限定形态）

## mechanics 基座条款（v1.0 §0/§1/§2）

按 mvp2/MECHANICS.md v1.0（裸 A 基线：无门禁/无审计条款）。
