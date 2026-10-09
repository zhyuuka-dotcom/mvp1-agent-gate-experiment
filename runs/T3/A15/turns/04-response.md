Now let me look at the tests and repro files to understand conventions and expected behavior.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">for f in repro/nginx.conf repro/nginx_multiline.conf repro/access.log repro/combined.log; do echo "=== $f ==="; cat "$f"; done</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
