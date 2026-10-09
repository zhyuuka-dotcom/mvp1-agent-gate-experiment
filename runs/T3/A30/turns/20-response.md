All 28 tests pass. Let me also verify the `-a` addition path and group-by latitude, plus a `query` command still works with the registered aggregate.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ parameter name="command">cd /repo 2>/dev/null; echo "=== -a add median exp ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/combined.log -f combined -a 'median(bytes_sent)' 2>&1 | grep -v Warning | grep -v "re\." | tail -8; echo "=== group-by host custom ==="; .venv/bin/python -m ngxtop.ngxtop --no-follow -l repro/access.log -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' -g host 2>&1 | grep -v Warning | grep -v "re\." | tail -8</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
