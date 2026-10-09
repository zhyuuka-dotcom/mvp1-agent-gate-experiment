The `-f main` format isn't recognized as a named format (only combined/common/caddy have predefined patterns). Let me check build_pattern and how format strings work.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">grep -n "def build_pattern\|def detect_log_config\|combined\|common\|caddy\|PREDEFINED\|main" ngxtop/config_parser.py | head -40</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
