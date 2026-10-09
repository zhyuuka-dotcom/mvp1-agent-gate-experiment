Now let me check the characterization test since it may snapshot output.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">cd /repo 2>/dev/null; grep -n "Summary\|Detailed\|avg_bytes_sent\|report\|default" tests/test_characterization.py | head -40; echo "=== lines ==="; wc -l tests/*.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
