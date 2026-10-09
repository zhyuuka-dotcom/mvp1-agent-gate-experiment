Baseline confirmed: 28 tests pass. Now let me run the current CLI to observe the exact table output.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/tmp/err.txt; echo "EXIT=$?"; echo "=== STDERR ==="; cat /tmp/err.txt</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
