<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command">cd /repo 2>/dev/null; echo "=== -a add median exp ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/combined.log -f combined -a 'median(bytes_sent)' 2>&1 | grep -v Warning | grep -v "re\." | tail -8; echo "=== group-by host custom ==="; FMT='$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"'; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -f "$FMT" -g host 2>&1 | grep -v Warning | grep -v "re\." | tail -8</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
