Now I understand the structure. Let me check the test suite baseline and how `report()` is used elsewhere.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">grep -rn "\.report()\|process_log\|DEFAULT_QUERIES" tests/ ngxtop/ && echo "=== baseline ===" && .venv/bin/python -m pytest tests/ -q 2>&1 | tail -5</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
