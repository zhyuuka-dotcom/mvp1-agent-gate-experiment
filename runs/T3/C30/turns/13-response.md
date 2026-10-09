Now I understand the structure well. Let me check the README report examples to understand the documented output format, and test the config-based run that showed 0 records.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">sed -n '60,100p' README.rst; echo "=== try -f with full format string ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/access.log --no-follow -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' 2>/dev/null</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
