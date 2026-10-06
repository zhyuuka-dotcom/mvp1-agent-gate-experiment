Now I'll implement the fix. The plan:

1. Add a function `resolve_log_format_name(name, arguments)` in config_parser.py that, given a format name like `main`, reads the nginx config (from `--config` or detected path) and returns the matching log_format string.
2. In `process()`, when `-f` is provided but is not a known built-in keyword and contains no `$` (i.e., it isn't already a format string), resolve it as a log_format name before building the pattern.

Let me write the change carefully to preserve the existing behavior (characterization tests use `-f` not at all or with built-ins).

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path">ngxtop/config_parser.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
