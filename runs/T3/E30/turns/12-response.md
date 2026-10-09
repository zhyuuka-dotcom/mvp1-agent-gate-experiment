The parser likely splits on the first ` | ` only, or needs the format exactly `path:start-end | quote`. The issue may be that my 依据 line contains the leading spaces in the quote which get trimmed fine... but "R2 条目1: 依据段格式须为「路径:起-止 | 单行引文」" — perhaps it requires the exact token `起-止` meaning line-range as `start-end` with no other colon, OR the field must literally be on one physical line but my markdown wrapped. 

Another possibility: the parser expects the key exactly `依据:` followed by `path:start-end | quote` and my `ngxtop/ngxtop.py:88` — the colon after path plus `:88`... "路径:起-止" means `path:START-END`, i.e. a RANGE like `88-88` or `88-92`, not a single line number! "起-止" = start-end. So I must write `ngxtop/ngxtop.py:85-95`.

That's it. Let me use line ranges.

WRITE PLAN.md
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py
- README.rst
- tests/test_median.py

## ASSUMPTIONS
- 假设: 默认报告由 DEFAULT_QUERIES 两条 SQL 的 avg(bytes_sent) 列决定，新增中位数需改这两处查询。
  依据: ngxtop/ngxtop.py:85-95 |        avg(bytes_sent)                             AS avg_bytes_sent,
  验证: grep -n "avg(bytes_sent)" ngxtop/ngxtop.py
- 假设: README 默认输出样例的表头含 avg_bytes_sent，是文档中的输出惯例。
  依据: README.rst:70-78 |     |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
  验证: grep -n "avg_bytes_sent" README.rst
- 假设: 运行期为 python3 + sqlite3，可通过 connection.create_aggregate 注册自定义 median 聚合。
  依据: ngxtop/ngxtop.py:320-324 |         self.conn = sqlite3.connect(':memory:')
  验证: .venv/bin/python -c "import sqlite3;print(sqlite3.sqlite_version)"

## BEHAVIOR_DELTAS
- 增量: SQLProcessor 注册 median 自定义聚合，Summary/Detailed 查询在 avg_bytes_sent 后新增 median_bytes_sent 列。
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f main --no-follow | grep -o median_bytes_sent
- 增量: 对 5 行 repro/access.log（bytes_sent 5120,153,2048,512,300），Summary 的 median_bytes_sent 显示 512.000。
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f main --no-follow | grep "512.000"

## NON_GOALS
- 非目标: 不改变现有 avg_bytes_sent 列或其它既有列的名称与位置语义。
  GUARD: .venv/bin/python -m pytest tests/test_characterization.py -q
- 非目标: 不改动 Caddy/日志解析逻辑与既有测试。
  GUARD: .venv/bin/python -m pytest tests/ -q

## TEST_PLAN
1. 先跑表征测试确认基线：.venv/bin/python -m pytest tests/test_characterization.py -q
2. 实现 median 聚合与查询列后，跑 CLI 验证 repro/access.log 输出 median_bytes_sent=512.000
3. 跑 tests/test_median.py 新测试
4. 全量回归：.venv/bin/python -m pytest tests/ -q
FILE_CONTENTS
