The format resolves and parses correctly. The root cause is clear: **the `-f <format>` option treats its argument as a literal format string only; it never resolves a named `log_format` from the nginx config.** The user's `-f main` should look up the `main` format definition.

Let me check how the pipeline expects log_format, and look at build_pattern/extract_variables for how to resolve names. Let me also check the multiline conf and the process flow more.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">sed -n '290,470p' ngxtop/ngxtop.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
