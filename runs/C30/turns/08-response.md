Now let me reproduce the issue to understand exactly what happens.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cd /Users/z 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop -f main -l repro/access.log --no-follow 2>&1 | head -40; echo "EXIT=$?"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
