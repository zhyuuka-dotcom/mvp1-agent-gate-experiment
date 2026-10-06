Reproduced: 0 records processed. The issue is `-f main` — the user passes a format *name* (`main`), not an actual format string. ngxtop builds a pattern from the literal name "main", which doesn't match log lines.

Let me confirm what happens with `--config` and the correct format string.

<｜｜DSML｜｜ calls>
<｜｜DSML｜｜ invoke name="RUN">
<｜｜DSML｜｜ parameter name="command" string="true">.venv/bin/python - <<'EOF' 2>&1
from ngxtop.config_parser import build_pattern, extract_variables, get_log_formats
fmt = "$request_time $upstream_response_time $remote_addr - $upstream_addr [$time_local] $host \"$request\" $status $bytes_sent \"$http_referer\" \"$http_user_agent\" \"$gzip_ratio\" \"$http_x_forwarded_for\" - \"$server_addr\""
p = build_pattern(fmt)
print("VARS:", list(extract_variables(fmt)))
with open('repro/access.log') as f:
    for l in f:
        print(bool(p.match(l)))
EOF</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>
