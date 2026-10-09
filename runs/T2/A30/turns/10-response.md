Now let me verify against the acceptance examples.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">echo "=== EX1 stdout ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format json 2>/tmp/e1; echo "--- stderr:"; cat /tmp/e1
echo "=== EX2 stdout ==="; .venv/bin/python -m ngxtop.ngxtop -f '$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host "$request" $status $bytes_sent "$http_referer" "$http_user_agent" "$gzip_ratio" "$http_x_forwarded_for" - "$server_addr"' -l repro/access.log --no-follow --output-format json 2>/tmp/e2; echo "--- stderr:"; cat /tmp/e2
echo "=== EX3 ==="; .venv/bin/python -m ngxtop.ngxtop -l repro/combined.log --no-follow --output-format yaml >/tmp/o3 2>/tmp/e3; echo "exit=$?"; echo "stdout:[$(cat /tmp/o3)]"; echo "stderr:[$(cat /tmp/e3)]"</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
