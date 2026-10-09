Still rejected. There must be a structural issue I'm missing. Let me re-read very literally:

```
## ASSUMPTIONS
- 假设: <一句话>
  依据: <文件相对路径>:<起行>-<止行> | <单行引文：该文件中真实存在的一行，≤120 字符，逐字复制>
  验证: <如何验证>
```

The 依据 line: `<path>:<start>-<end> | <quote>`. My path is `ngxtop/ngxtop.py`. Good.

Hmm — maybe the harness disallows the plan being the first write because it needs the contract BEFORE any write, and I've now done many rejected writes. That's fine. 

Maybe the issue: the gate validates "所有条目的依据文件合计覆盖 ≥2 个不同文件" but ONLY counts files listed in TOUCH_SET? No, it says the basis files must cover ≥2 distinct files. utils.py is a distinct file. Good.

Another possibility: maybe there's a hidden requirement that the contract must not exist yet and my repeated attempts are confusing state. Or maybe the validator is looking for a `## BEHAVIOR_DELTAS` VERIFY that is a real command but mine contains a pipe to a python -c with quotes — maybe the parser splits on some char.

Let me simplify drastically and test the minimal contract that should pass, to isolate the failing section.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="WRITE">
<｜｜DSML｜｜ parameter name="path">
PLAN.md</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_contents">
# PLAN

## TOUCH_SET
- ngxtop/ngxtop.py

## ASSUMPTIONS
- 假设: report 方法生成报表。
  依据: ngxtop/ngxtop.py:452-452 |     def report(self):
  验证: 阅读源码。
- 假设: error_exit 退出。
  依据: ngxtop/utils.py:19-19 | def error_exit(msg, status=1):
  验证: 阅读源码。

## BEHAVIOR_DELTAS
- 增量: 新增 json 输出。
  VERIFY: ls

## NON_GOALS
- 非目标: 不改子命令。
  GUARD: ls

## TEST_PLAN
1. 跑测试。
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
