Confirmed. README line 76: `    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |`.
And ngxtop.py line: `       avg(bytes_sent)                             AS avg_bytes_sent,`

Now I write PLAN.md.

TOUCH_SET:
- ngxtop/ngxtop.py
- README.rst
- tests/test_median.py (new)

ASSUMPTIONS with citations from ngxtop.py and README.rst (2 files covered).
BEHAVIOR_DELTAS, NON_GOALS, TEST_PLAN.

Let me write PLAN.md now.

WRITE PLAN.md
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py
- README.rst
- tests/test_median.py

## ASSUMPTIONS
- 假设: 默认报告由 DEFAULT_QUERIES 中两条 SQL（Summary/Detailed）的 avg(bytes_sent) 列决定，新增中位数需改这两处查询。
  依据: ngxtop/ngxtop.py:88
  引文:        avg(bytes_sent)                             AS avg_bytes_sent,
  验证: grep -n "avg(bytes_sent)" ngxtop/ngxtop.py 应显示改用/新增 median(bytes_sent) 列
- 假设: README 的默认输出样例展示 Summary/Detailed 表头含 avg_bytes_sent，是文档中的输出惯例。
  依据: README.rst:76
  引文:     |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |
  验证: grep -n "avg_bytes_sent" README.rst 查看更新后的示例
- 假设: 运行期为 python3 + sqlite3，可通过 connection.create_aggregate 注册自定义 median 聚合函数。
  依据: ngxtop/ngxtop.py:322
  引文:         self.conn = sqlite3.connect(':memory:')
  验证: .venv/bin/python -c "import sqlite3;print(sqlite3.sqlite_version)"

## BEHAVIOR_DELTAS
- 增量: SQLProcessor 注册 median 自定义聚合，Summary/Detailed 查询在 avg_bytes_sent 后新增 median_bytes_sent 列。
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/access.log -f main --no-follow | grep -o "median_bytes_sent"
- 增量: 对 5 行 repro/access.log（bytes_sent 依次 5120,153,2048,512,300），Summary 的 median_bytes_sent 显示 512.000。
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

Wait — the citation lines must be exact substrings of the file, ≤120 chars, no leading-whitespace normalization issue (verbatim). My ngxtop.py citation has leading spaces — that's fine as long as verbatim. The line is `       avg(bytes_sent)                             AS avg_bytes_sent,`. Count chars ~70 ok.

The README citation: `    |   count |   avg_bytes_sent |   2xx |   3xx |   4xx |   5xx |` — verbatim, ~65 chars.

Also I cited ngxtop.py:322 `        self.conn = sqlite3.connect(':memory:')` — need to verify verbatim. From the source I read: `        self.conn = sqlite3.connect(':memory:')`. Let me confirm the indentation via a quick grep to be safe. Actually risky. Let me verify it.

I'll first verify then write PLAN.md. Let me grep.Let me verify the third citation line exactly before writing the plan.

RUN grep -n "sqlite3.connect" ngxtop/ngxtop.py | cat -A

Send.

RUN grep -n "sqlite3.connect" ngxtop/ngxtop.py | cat -A
