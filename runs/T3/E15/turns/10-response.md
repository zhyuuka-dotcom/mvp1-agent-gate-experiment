Now I have a clear picture. Let me write the PLAN.md.

I'll register a `median` SQLite aggregate and add `median(bytes_sent) AS med_bytes_sent` to both DEFAULT_QUERIES. I need to ensure grouped queries work. The `median` aggregate works per-group naturally.

Let me write the plan now.Now I have enough understanding. Let me write the plan.

WRITE PLAN.md
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py
- tests/test_median_bytes_sent.py

## ASSUMPTIONS
- 假设: 默认报表用 `avg(bytes_sent) AS avg_bytes_sent` 一列展示均值，中位数应作为相邻的新列加入同一报表
  依据: ngxtop/ngxtop.py:89-93 | `       avg(bytes_sent)                             AS avg_bytes_sent,`
  验证: 运行 `.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow`，确认输出中出现中位数名列且与 avg_bytes_sent 相邻
- 假设: SQLiteProcessor 用 sqlite3 连接内存库，可在连接上注册自定义聚合函数供报表查询使用
  依据: ngxtop/ngxtop.py:397-403 | `        self.conn = sqlite3.connect(':memory:')`
  验证: 在 SQLProcessor.__init__ 注册 median 聚合后，用 `select median(bytes_sent) from log` 查询返回正确中位数
- 假设: report() 用 cursor.description 的列名直接作为表头，故 SQL 别名即为输出列名
  依据: ngxtop/ngxtop.py:361-364 | `                columns = (d[0] for d in cursor.description)`
  验证: 新列别名 med_bytes_sent 在 stdout 表头中原样出现

## BEHAVIOR_DELTAS
- 增量: 在 DEFAULT_QUERIES 的 Summary 与 Detailed 查询中，于 avg_bytes_sent 之后加入 median(bytes_sent) AS med_bytes_sent 列
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow | grep -c med_bytes_sent
- 增量: 在 SQLProcessor 初始化时为 sqlite 连接注册 median 聚合函数，使 median(bytes_sent) 可在分组/非分组查询中正确求中位数（偶数个取中间两值平均）
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f "$(grep log_format repro/nginx.conf | sed "s/.*main *//; s/';.*//; s/'//g")" | grep med_bytes_sent

## NON_GOALS
- 非目标: 不改变既有列（count/avg_bytes_sent/2xx-5xx）的名称、顺序与语义
  GUARD: .venv/bin/python -m pytest tests/test_characterization.py -q
- 非目标: 不新增 CLI 子命令或选项（median 仅作为默认报表新列）
  GUARD: .venv/bin/python -m pytest tests/ -q

## TEST_PLAN
1. 先运行现有测试 `.venv/bin/python -m pytest tests/ -q` 确认基线全绿
2. 实现 median 聚合与两处查询列改动
3. 运行 CLI 于 combined.log 与 access.log，核对 med_bytes_sent 列值与手算中位数一致
4. 运行新增 tests/test_median_bytes_sent.py 及全部测试确认无回归
FILE_CONTENTS

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents" string="true"># PLAN

## TOUCH_SET
- ngxtop/ngxtop.py
- tests/test_median_bytes_sent.py

## ASSUMPTIONS
- 假设: 默认报表用 `avg(bytes_sent) AS avg_bytes_sent` 一列展示均值，中位数应作为相邻的新列加入同一报表
  依据: ngxtop/ngxtop.py:89-93 | `       avg(bytes_sent)                             AS avg_bytes_sent,`
  验证: 运行 `.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow`，确认输出中出现中位数名列且与 avg_bytes_sent 相邻
- 假设: SQLiteProcessor 用 sqlite3 连接内存库，可在连接上注册自定义聚合函数供报表查询使用
  依据: ngxtop/ngxtop.py:397-403 | `        self.conn = sqlite3.connect(':memory:')`
  验证: 在 SQLProcessor.__init__ 注册 median 聚合后，用 `select median(bytes_sent) from log` 查询返回正确中位数
- 假设: report() 用 cursor.description 的列名直接作为表头，故 SQL 别名即为输出列名
  依据: ngxtop/ngxtop.py:361-364 | `                columns = (d[0] for d in cursor.description)`
  验证: 新列别名 med_bytes_sent 在 stdout 表头中原样出现

## BEHAVIOR_DELTAS
- 增量: 在 DEFAULT_QUERIES 的 Summary 与 Detailed 查询中，于 avg_bytes_sent 之后加入 median(bytes_sent) AS med_bytes_sent 列
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow | grep -c med_bytes_sent
- 增量: 在 SQLProcessor 初始化时为 sqlite 连接注册 median 聚合函数，使 median(bytes_sent) 可在分组/非分组查询中正确求中位数（偶数个取中间两值平均）
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f "$(grep log_format repro/nginx.conf | sed "s/.*main *//; s/';.*//; s/'//g")" | grep med_bytes_sent

## NON_GOALS
- 非目标: 不改变既有列（count/avg_bytes_sent/2xx-5xx）的名称、顺序与语义
  GUARD: .venv/bin/python -m pytest tests/test_characterization.py -q
- 非目标: 不新增 CLI 子命令或选项（median 仅作为默认报表新列）
  GUARD: .venv/bin/python -m pytest tests/ -q

## TEST_PLAN
1. 先运行现有测试 `.venv/bin/python -m pytest tests/ -q` 确认基线全绿
2. 实现 median 聚合与两处查询列改动
3. 运行 CLI 于 combined.log 与 access.log，核对 med_bytes_sent 列值与手算中位数一致
4. 运行新增 tests/test_median_bytes_sent.py 及全部测试确认无回归
FILE_CONTENTS
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
