The line 456 in my quote (`sqlite3.connect(':memory:')`) was actually at a different line number. Let me find its real line and check config_parser lines for a second file quote.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">grep -n "sqlite3.connect" ngxtop/ngxtop.py; echo "---"; grep -n "LOG_FORMAT_COMBINED" ngxtop/config_parser.py | head -2; echo "---"; sed -n '15,18p' ngxtop/config_parser.py | cat -A</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
