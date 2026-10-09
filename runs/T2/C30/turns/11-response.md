<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">
PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents">
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: 默认报表由 `report()` 用 tabulate 生成，并拼接状态行返回字符串。
  依据: ngxtop/ngxtop.py:452
  验证: 阅读 `report()` 实现确认状态行 `status = 'running for %.0f seconds, %d records processed: %.2f req/sec'` 与 orgtbl 表拼接。
- 假设: 默认查询的 Detailed 查询使用 `--group-by` 与 `--order-by`/`--limit` 格式化。
  依据: ngxtop/ngxtop.py:533
  验证: 阅读 `build_processor` 的 else 分支确认 `report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]`。
- 假设: 分组列可含逗号（多列分组），字段以 `,` 分割。
  依据: ngxtop/ngxtop.py:539
  验证: 运行 `-g remote_addr,status` 观察 Detailed 表有两列分组。

## BEHAVIOR_DELTAS
- 增量: 新增 `--output-format` 选项（table/json，默认 table），json 模式把状态行写 stderr、把 summary/detailed 结构写 stdout 为单个 JSON 文档；非法值报错退出非 0。
  VERIFY: `.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>/dev/null | .venv/bin/python -c "import json,sys; d=json.load(sys.stdin); print(d['summary']['count'])"`

## NON_GOALS
- 非目标: 子命令（top/avg/sum/query）与 `--output-format` 的组合行为。
  GUARD: `.venv/bin/python -m pytest tests/ -q`

## TEST_PLAN
1. 先跑 `.venv/bin/python -m pytest tests/ -q` 确认既有 28 条通过。
2. 用验收例 1/2/3 逐条运行 CLI 核对 stdout JSON、stderr 状态行、退出码。
3. 运行 `-g remote_addr,status` 与 `--output-format json` 回归检查分组能力。
4. 复查默认 table 模式输出与现状一致。
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
