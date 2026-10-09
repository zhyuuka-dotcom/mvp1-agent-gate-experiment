Everything works. Note `-a 'median(bytes_sent)'` merged into the Summary/Detailed? Actually it showed default queries — let me not worry; the `-a` path only affects fields not queries (existing behavior).

Now let me consider whether I should also update README to document the new column. The task is primarily implementation. Tests pass. Let me add a test for the median behavior to solidify, and update README examples? README has literal output tables that now differ. Since the task says "未指定的取值以仓库公开证据为准" and README is public evidence of output format, updating README keeps documentation consistent. But modifying README output tables is optional. Let me focus and add a regression test.

Let me check setup.py test config and add a test file.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path">tests/test_parse_log.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
