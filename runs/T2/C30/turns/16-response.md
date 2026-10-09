My line references were slightly off (457 is correct for status). The rejection message says the contract "尚未通过" (not yet passed), which is the generic gate message. Let me reconsider the format. Perhaps the issue is that BEHAVIOR_DELTAS/NON_GOALS VERIFY/GUARD must be real commands **without backticks**? Or the `- <path>（1~5 个...）` note. 

Actually, re-reading the rejection: it might be that the harness cannot even parse because I'm missing something structural. Let me try a very careful re-submission, matching the template exactly including the `（1~5 个；写清单外文件将被拒绝）` being just a comment. Let me write it as plainly as the spec shows.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">
PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents">
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: 默认报表由 report() 生成并拼接状态行与两张 orgtbl 表。
  依据: ngxtop/ngxtop.py:456-456 |         status = 'running for %.0f seconds, %d records processed: %.2f req/sec'
  验证: 运行 `.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow` 观察输出。
- 假设: 默认查询用 arguments 格式化 DEFAULT_QUERIES 得到 report_queries。
  依据: ngxtop/ngxtop.py:533-533 |         report_queries = [(name, query % arguments) for name, query in DEFAULT_QUERIES]
  验证: 阅读 build_processor 的 else 分支。
- 假设: error_exit 写 stderr 并以状态码退出。
  依据: ngxtop/utils.py:19-19 | def error_exit(msg, status=1):
  验证: 阅读 utils.py。

## BEHAVIOR_DELTAS
- 增量: 新增 --output-format 选项，json 模式状态行写 stderr、JSON 写 stdout；非法值报错退出非 0。
  VERIFY: .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>/dev/null | .venv/bin/python -c "import json,sys; d=json.load(sys.stdin); print(d['summary']['count'])"

## NON_GOALS
- 非目标: 子命令 top/avg/sum/query 与 --output-format 的组合行为。
  GUARD: .venv/bin/python -m pytest tests/ -q

## TEST_PLAN
1. 跑 pytest tests/ -q 确认既有 28 条通过。
2. 用验收例 1/2/3 逐条运行 CLI 核对 stdout JSON、stderr 状态行、退出码。
3. 运行 -g remote_addr,status 加 --output-format json 回归检查分组能力。
4. 复查默认 table 模式输出与现状一致。
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
