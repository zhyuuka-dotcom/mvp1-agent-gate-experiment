Baseline: 28 tests pass. Now let me check the current default report output to confirm exact column names.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f main 2>&1 | head -20; echo "=== combined ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>&1 | head -20</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
