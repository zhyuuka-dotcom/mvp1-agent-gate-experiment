Root cause confirmed. When `-f main` is given, `main` is treated as a literal log format string (regex `main`), not as a named `log_format` directive. The parser never resolves a format *name* to the actual format definition. Combined with `-l` providing the log path, `detect_log_config` is skipped entirely, so named formats are never resolved.

Let me check the existing tests and the debug behavior.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cat tests/test_config_parser.py && echo "===CHAR===" && cat tests/test_characterization.py</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
