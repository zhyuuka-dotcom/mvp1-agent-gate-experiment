28 tests pass. `report()` returns a string containing status + tables, and tests assert on that. So I'll keep `report()` returning the string for table mode, and add JSON-specific handling.

Key design decisions:
1. Add `--output-format` docopt option with default `table`.
2. Validate value in `process()` — error to stderr + exit nonzero for invalid.
3. In `SQLProcessor.report()`, I need structured data for JSON. Better: add a method `report_data()` or store rows. I'll refactor `report()` to optionally produce JSON.

Note: `report()` returns string used by table mode and tests. I'll add a separate method that returns the two result sets as data, and have `report()` use it. Then `process_log` chooses output.

Let me check `count()` and row values. SQLite returns ints for counts and floats for avg. Good.

Now let's write the plan.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">
PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents">
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py
- tests/test_output_format.py

## ASSUMPTIONS
- 假设: 默认报表的两张表由 SQLProcessor.report() 用 tabulate 生成字符串并返回
  依据: ngxtop/ngxtop.py:468 | `result = tabulate.tabulate(cursor.fetchall(), headers=columns, tablefmt='orgtbl', floatfmt='.3f')`
  验证: 阅读 report() 方法，确认可复用其游标结果构造 JSON
- 假设: 默认查询的两条 SQL 已在 DEFAULT_QUERIES 中定义，列名即 summary/detailed 的键
  依据: ngxtop/ngxtop.py:100-113 | `('Detailed:',`
  验证: 运行 CLI 观察输出列名与 spec 一致
- 假设: process_log 在 no-follow 模式下用 print(processor.report()) 输出，是切换输出格式的注入点
  依据: ngxtop/ngxtop.py:502 | `print(processor.report())  # this will only run when start in --no-follow mode`
  验证: 修改后用验收例命令验证 stdout/stderr 分流
- 假设: docopt 从 __doc__ 解析选项，新增 --output-format 会出现在 args 字典
  依据: ngxtop/ngxtop.py:609 | `args = docopt(__doc__, version='xstat 0.1')`
  验证: 运行 --output-format json 被识别

## BEHAVIOR_DELTAS
- 增量: 新增 --output-format 选项（默认 table），json 模式 stdout 输出单个 JSON 文档、状态行走 stderr
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json | .venv/bin/python -c "import json,sys; d=json.load(sys.stdin); assert d['summary']['count']==2"
- 增量: 非法取值（如 yaml）输出 stderr 错误行并非零退出，stdout 无 JSON
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml; echo "exit=$?"
- 增量: table 模式（默认与显式 table）输出与现状完全相同
  VERIFY: .venv/bin/python -m pytest tests/ -q

## NON_GOALS
- 非目标: 不改变子命令（top/avg/sum/query）的输出行为
  GUARD: .venv/bin/python -m pytest tests/ -q
- 非目标: 不改变 -g 分组查询能力
  GUARD: .venv/bin/python -m pytest tests/test_characterization.py -q

## TEST_PLAN
1. 先运行 pytest tests/ 确认 28 条基线绿
2. 实现 --output-format 与 json 渲染后，运行验收例 1/2/3 逐值核对
3. 运行 pytest tests/ 确认全部 28 条仍绿
4. 新增 tests/test_output_format.py 覆盖 json 结构、非法取值、分组键回归，再跑全量
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
