<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cd /repo 2>/dev/null; echo "=== combined ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/combined.log -f combined 2>&1 | grep -v Warning | grep -v "re\." | tail -12; echo; echo "=== access.log custom format (5 records) median should be 512 ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' 2>&1 | grep -v Warning | grep -v "re\." | tail -12</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
