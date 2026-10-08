Now let me look at how `-f common` works (a name) vs literal, and check the tests for parse_log to understand expected behavior.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -m ngxtop.ngxtop -f common -l repro/combined.log --no-follow; echo "EXIT=$?"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
