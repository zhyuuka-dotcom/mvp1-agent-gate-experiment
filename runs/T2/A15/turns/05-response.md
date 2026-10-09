Now let me look at the tests, utils, and run the existing tests.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">cat ngxtop/utils.py && echo "===TESTS===" && ls tests/ && echo "===RUN===" && .venv/bin/python -m pytest tests/ -q 2>&1 | tail -20</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
