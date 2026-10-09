The harness reports a malformed marker. It seems my parameter with `file_contents` containing the closing marker is being mangled. Let me try the exact documented format: path on the WRITE line, then `<<<FILE_CONTENTS` on the next line.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents"><<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: 默认报表的 Summary 与 Detailed 查询都在 SELECT 中含 avg(bytes_sent) AS avg_bytes_sent，新增列应与之并列。
  依据: ngxtop/ngxtop.py:91-91 | "       avg(bytes_sent)                             AS avg_bytes_sent,"
  验证: grep 两处 DEFAULT_QUERIES 中的 avg_bytes_sent，确认新列紧随其后。
- 假设: bytes_sent 已是默认处理的字段，新统计无需新增 processor field。
  依据: ngxtop/ngxtop.py:116-116 | "DEFAULT_FIELDS = set(['status_type', 'bytes_sent'])"
  验证: 运行 CLI 处理 repro/combined.log，records processed 为 2 且无字段错误。
- 假设: SQLProcessor 在 sqlite3.connect(':memory:') 建立连接，是注册自定义聚合函数的位置。
  依据: ngxtop/ngxtop.py:456-456 | "        self.conn = sqlite3.connect(':memory:')"
  验证: 检查 init_db 前后连接对象存在且可 create_aggregate。

## BEHAVIOR_DELTAS
- 增量: Summary 与 Detailed 报表在 avg_bytes_sent 后新增 median_bytes_sent 列，取 bytes_sent 的中位数。
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 输出中两表均含 median_bytes_sent，Summary 值为 2636.500。
- 增量: SQLite 连接注册 median 聚合函数，使 median(bytes_sent) 可在查询中调用。
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f 主格式串 显示 median 列且无 SQL 错误。

## NON_GOALS
- 非目标: 不修改 print/top/avg/sum 子命令的输出列。
  GUARD: .venv/bin/python -m pytest tests/ -q
- 非目标: 不修改日志解析、格式检测与 Caddy 处理逻辑。
  GUARD: .venv/bin/python -m pytest tests/test_parse_log.py tests/test_caddy_integration.py -q

## TEST_PLAN
1. 先跑 .venv/bin/python -m pytest tests/ -q 确认基线 28 passed。
2. 在 ngxtop/ngxtop.py 中注册 median 聚合函数并修改两处 DEFAULT_QUERIES。
3. 运行 CLI 对 repro/combined.log 与 repro/access.log，确认 median_bytes_sent 列及其数值。
4. 重跑全部测试确认无回归。
FILE_CONTENTS</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
