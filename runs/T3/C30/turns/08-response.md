Let me run the existing tests and the CLI to establish baseline behavior.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python -m pytest tests/ -q 2>&1 | tail -20; echo "=== CLI ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f main 2>&1 | head -30</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
