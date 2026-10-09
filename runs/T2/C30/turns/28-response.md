I malformed the tool call. Let me resubmit cleanly.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">
PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents">
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: 默认报表由 report 生成。
  依据: ngxtop/ngxtop.py:452 |     def report(self):
  验证: 阅读源码。
- 假设: error_exit 负责报错退出。
  依据: ngxtop/utils.py:19 | def error_exit(msg, status=1):
  验证: 阅读源码。

## BEHAVIOR_DELTAS
- 增量: 新增 json 输出模式。
  VERIFY: .venv/bin/python -m pytest tests/ -q

## NON_GOALS
- 非目标: 不改子命令。
  GUARD: .venv/bin/python -m pytest tests/ -q

## TEST_PLAN
1. 跑测试。
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
