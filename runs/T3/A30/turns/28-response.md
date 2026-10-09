Everything is in place. Let me do one final end-to-end verification with the default combined report and confirm the median column appears and values are correct.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ parameter name="command">cd /repo 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/combined.log 2>&1 | grep -v Warning | grep -v "re\." | tail -12; echo "EXIT=$?"</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
