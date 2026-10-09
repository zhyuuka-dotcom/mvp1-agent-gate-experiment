Now I have full clarity. Let me design the approach:

1. Add `--output-format <fmt>` to docopt usage, default `table`.
2. Refactor `SQLProcessor.report()` to optionally return structured JSON data. Cleanest: add a method `report_json()` that returns a dict, and modify `report()` to print. But `process_log` calls `print(processor.report())`. I'll make the processor aware of output format.

The summary query returns columns `count, avg_bytes_sent, 2xx, 3xx, 4xx, 5xx`. The detailed query returns group-by columns + those stats.

I'll build a `report_json()` that executes the two default queries and returns `{"summary": {...}, "detailed": [...]}`. But the report_queries structure is generic (could be subcommands). Per spec scope: only default reports. I'll implement JSON based on the actual report_queries: first query → summary (first row), subsequent queries → detailed.

Actually cleaner: JSON mode maps report_queries[0] rows to a single object for "summary" (take first row), and last query rows to "detailed" array. Given spec only requires default report.

Let me write the plan.

WRITE PLAN.md
<<<FILE_CONTENTS
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py
- tests/test_output_format.py

## ASSUMPTIONS
- 假设: 默认报表的两个查询中，第一个是 Summary、第二个是 Detailed，且 JSON 顶层即 summary/detailed
  依据: ngxtop/ngxtop.py:92-92 | `    ('Summary:',`
  验证: 运行 CLI `--output-format json` 并 json.loads，检查键为 summary/detailed
- 假设: report() 中状态行是 JSON 模式需转到 stderr 的那一行
  依据: ngxtop/ngxtop.py:453-453 | `        status = 'running for %.0f seconds, %d records processed: %.2f req/sec'`
  验证: 运行 json 模式，断言 stderr 含 "records processed" 且 stdout 可 json.loads
- 假设: docopt 解析 usage 块中的选项，新增选项需写入 usage
  依据: ngxtop/ngxtop.py:128-128 | `    args = docopt(__doc__, version='xstat 0.1')`
  验证: `--output-format json` 被 docopt 接受且不报错

## BEHAVIOR_DELTAS
- 增量: 新增 --output-format 选项，json 模式下 stdout 只输出一个 JSON 文档，状态行到 stderr
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json
- 增量: 非法 --output-format 取值时报错到 stderr 并以非零退出码退出
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml; echo $?

## NON_GOALS
- 非目标: 不改变 table 模式既有输出（含状态行与两张 orgtbl 表）
  GUARD: .venv/bin/python -m pytest tests/test_characterization.py -q
- 非目标: 不改变 -g 分组能力
  GUARD: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow -g remote_addr,status

## TEST_PLAN
1. 写 ngxtop/ngxtop.py 实现选项与 JSON 输出
2. 写 tests/test_output_format.py 覆盖例 1/2/3 与 -g
3. 运行 tests/test_output_format.py 与 tests/（全部 28 条 + 新增）
4. 手动跑三个验收例核对数值
FILE_CONTENTS
