Works. Median of [5120, 153, 2048, 512, 300] sorted = [153,300,512,2048,5120], median 512. Correct. Even count works too.

Now let me make sure the median aggregate works with the `-a` addition and `query` path, and run the full test suite.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cd /repo 2>/dev/null; .venv/bin/python -m pytest tests/ -q 2>&1 | tail -15</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
