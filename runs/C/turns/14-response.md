Now I have a clear picture. The root cause: `-f main` passes the *name* `main` which is treated as a literal format string producing regex `main` → no matches. The fix should resolve a `-f <name>` to a `log_format` directive from the nginx config.

Let me check the actual upstream fix for this issue to align. Let me look at the issue context — the canonical ngxtop fix resolves `-f <name>` from config. Let me examine how `detect_log_config` and the CLI options interact more fully.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path">ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
