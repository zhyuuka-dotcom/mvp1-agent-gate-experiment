Works with explicit format. The `-c` case produced 0 records because config's access_log path is used as the -f format fallback? Actually with `-c`, log_format comes from config, and I passed -l so access log is explicit but log_format still from config. Let me check why 0. Actually detect_log_config returns format string, and pattern is built. Let me debug.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">cd /repo 2>/dev/null; .venv/bin/python -m ngxtop.ngxtop --no-follow -c repro/nginx.conf -v 2>&1 | grep -iv warning | grep -i "log_format\|access_log\|pattern" | head; echo "---with -l"; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -c repro/nginx.conf -v 2>&1 | grep -iv "warning\|re\." | head -20</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
