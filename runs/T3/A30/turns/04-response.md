Now let me look at the tests and repro materials to understand conventions.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cd /repo 2>/dev/null || true; cat repro/nginx.conf; echo "=== access.log ==="; cat repro/access.log; echo "=== combined.log ==="; cat repro/combined.log</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
