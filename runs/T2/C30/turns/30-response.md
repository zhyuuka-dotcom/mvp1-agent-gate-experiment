I've now tried many variants. Something systematic is wrong. Let me reconsider the possibility that the WRITE tool's `<<<FILE_CONTENTS` heredoc-style parameterization I'm using via the `<parameter name="file_contents">` is being interpreted differently — maybe the harness expects the raw format shown:

```
WRITE <path>
<<<FILE_CONTENTS
(content)
FILE_CONTENTS
```

The instruction says: "WRITE <path>（全量覆写文件，格式如下）" then shows that heredoc format. But the tool interface I'm using is XML `<parameter>`. Perhaps the harness actually parses the `file_contents` parameter content fine (it produced "file exists" checks)...

Actually, the fact that it says "计划合同尚未通过" means it READ my content and validated it. So content is being received.

Let me hypothesize the validator is strict about the quote being ≤120 chars AFTER stripping. All mine are fine.

New idea: maybe the validator requires the ASSUMPTIONS `依据` line to have exactly the format `path:start-end | quote` and it splits on the LAST `|`... no pipes in quotes.

Could the problem be the full-width characters like `：` inside my 假设 text? I used ASCII colon. 

Let me try a COMPLETELY ASCII contract to rule out encoding issues.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">
PLAN.md</｜｜DSML｜｜ parameter name="file_contents">
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: report builds the default report.
  依据: ngxtop/ngxtop.py:452-452 |     def report(self):
  验证: read source.
- 假设: error_exit writes stderr and exits.
  依据: ngxtop/utils.py:19-19 | def error_exit(msg, status=1):
  验证: read source.

## BEHAVIOR_DELTAS
- 增量: add json output.
  VERIFY: .venv/bin/python -m pytest tests/ -q

## NON_GOALS
- 非目标: no subcommand changes.
  GUARD: .venv/bin/python -m pytest tests/ -q

## TEST_PLAN
1. run pytest.
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
