I need to avoid the malformed markers. Let me retry.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null; echo "===STDERR==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>&1 1>/dev/null; echo "---combined.log---"; cat repro/combined.log; echo "---access.log---"; cat repro/access.log</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
