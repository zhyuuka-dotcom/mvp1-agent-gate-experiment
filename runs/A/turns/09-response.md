Now let me understand the fix approach. The user uses `-f main`, where `main` is a log_format name. ngxtop should support resolving a format name to its actual format string. Let me check how `-f` flows and consider the design.

Let me look at the parse_log tests and the README for documented `-f` behavior.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ parameter name="path">tests/test_parse_log.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">grep -n "\-f \|log-format\|log_format\|main" README.rst | head -40</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
