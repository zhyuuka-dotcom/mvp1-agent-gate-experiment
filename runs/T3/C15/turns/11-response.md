Let me check how median can be computed. SQLite has no built-in median, so I need a subquery approach. Let me check the access.log against the main format and see how the CLI can use it.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">.venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f main 2>&1 | head -30; echo "==="; cat repro/access.log</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
