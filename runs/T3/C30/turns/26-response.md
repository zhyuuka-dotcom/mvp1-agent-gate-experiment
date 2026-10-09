Line 91 has 7 leading spaces. My quote used 7 spaces — that should be right. Wait: the LEN is 70 including newline, so 69 chars content. That's ≤120 fine.

The issue may be that in my PLAN.md the quote line got stripped/normalized, or the harness counts "trim 后" and something. Let me actually read back what was written to PLAN.md to see how it was stored.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cat -A PLAN.md | grep -n "avg(bytes_sent)\|DEFAULT_FIELDS\|sqlite3.connect\|LOG_FORMAT_COMBINED"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter name="command" string="true">cat -A PLAN.md | grep -n "avg\|DEFAULT_FIELDS\|sqlite3\|LOG_FORMAT"</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="command" string="true">cat PLAN.md | grep -n "依据"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter name="command" string="true">cat PLAN.md</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter name="command">cat PLAN.md</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ calls>
