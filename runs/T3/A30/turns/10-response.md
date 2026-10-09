With `-l` and `-c`, log_format becomes 'combined' — because when access log is explicit only, detect_log_config is only called when access_log is None. Wait, code: `if access_log is None: access_log, log_format = detect_log_config(...)`. log_format stays default 'combined'. So with `-l` given, `-c` is ignored. That's existing behavior; fine.

To use the custom format, I must pass -f with the format string. That worked. Good.

Now let me examine the tests to understand conventions, and check the DEFAULT_QUERIES and expectations. The request: add median of bytes_sent to the report, next to average. Not specified: column name/location/tables. I'll add `median_bytes_sent` to both Summary and Detailed default queries.

Let me check the characterization tests for existing expectations.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">cd /repo 2>/dev/null; grep -rn "avg_bytes_sent\|median\|bytes_sent" tests/ README.rst | head -40</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
