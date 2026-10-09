The `-f main` doesn't work by name directly. Let me check the usage — it seems `main` format needs the config file. Let me try with the repro combined.log default and with config.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">echo "=== default combined ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow 2>/dev/null; echo "=== with config ==="; .venv/bin/python -m ngxtop.ngxtop -c repro/nginx.conf -l repro/access.log --no-follow 2>/dev/null</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
