The format string works fine. The problem is that `-f main` passes a format *name*. Users reasonably expect ngxtop to resolve that name from the nginx config. Let me verify the config parser also handles the log_format correctly and check tests.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python -m pytest tests/ -q 2>&1 | tail -20</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
<｜｜DSML｜｜ calls>
