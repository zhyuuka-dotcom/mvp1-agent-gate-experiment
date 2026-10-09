Now I understand the conventions. The average column is named `avg_bytes_sent`. The convention for median would naturally be `median_bytes_sent`, placed right after `avg_bytes_sent` in both Summary and Detailed tables. Let me check the config_parser and utils, then run the tests to get a baseline.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cat ngxtop/utils.py && echo "=== config_parser ===" && sed -n '1,60p' ngxtop/config_parser.py && echo "=== baseline tests ===" && .venv/bin/python -m pytest tests/ -q 2>&1 | tail -20</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
