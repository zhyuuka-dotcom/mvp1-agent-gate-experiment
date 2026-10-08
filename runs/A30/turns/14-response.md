Now I'll implement format-name resolution. I'll add a helper in `config_parser.py` that resolves a possibly-named format, and call it in `process()`. Let me write a `resolve_log_format` function.

Key design:
- Known aliases: `combined`, `common`, `caddy` → pass through.
- If the value contains `$` (a real format string) → pass through.
- Otherwise treat it as a format *name*: look it up in the nginx config (from `-c` / `--config`, or auto-detected path). If found, use it. If not found, error_exit with a helpful message.

Let me add this to config_parser.py.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="READ">
<｜｜DSML｜｜ parameter name="path" string="true">ngxtop/config_parser.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
