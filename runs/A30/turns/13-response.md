Both configs parse correctly. So the config parsing side is fine. The root cause is clear:

When the user provides `-f main`, the value `main` is treated as a literal log format string. It never gets resolved against the nginx config's named `log_format` directives. So the regex becomes just `main` (literal), which matches nothing → 0 records.

The fix: when the `-f` value is a format *name* (not a format string containing `$` and not one of the known aliases), resolve it from the nginx config file (via `-c`/auto-detected config path). Let me inspect `process()` logic carefully and `build_pattern`/`extract_variables` which are also called with the raw value.

Let me look at the whole process function and where format gets resolved, and add resolution logic.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">sed -n '580,606p' ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
